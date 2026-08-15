#!/usr/bin/env python3
"""
encounter_sim.py  —  Story/Grind dungeon run simulator  (Phase 2 harness)

Generates a full dungeon run at a given level (3-9 normal fights -> sub-boss) and
simulates it fight-by-fight, carrying HP + cooldowns across the whole chain. Answers
the questions the mockup + enemy spec set up but couldn't test:
    - Does a well-built same-level team clear a same-level run?
    - How much does attrition bite by the time you reach the sub-boss?
    - Does an under-geared / badly-composed team actually fail (as designed)?

Grounded in the real model:
    - roster.json statlines + ability schema (mult / cooldown / target / effects / bonus_vs)
    - K=1000 mitigation; affinity wheel advantage; level+gear power curves
    - enemy roles + scaling curve from enemy_profiles_scaling.md

This is a *balance harness*, not the shipping combat engine. It is deliberately
deterministic-ish (seeded) and simplifies AI to "use highest-impact ready ability".
Run:  python3 encounter_sim.py --level 40 --seed 7
      python3 encounter_sim.py --sweep         # scan levels 1..100, well-built team
      python3 encounter_sim.py --level 40 --team badcomp   # 4-tank failure demo
"""
import argparse, json, os, random, statistics as st
from dataclasses import dataclass, field

K = 1000
MENDER_HEAL_PCT = 0.28   # enemy Mender: % of ally max HP restored per cast (tunable)
PLAYER_HEAL_PCT = 0.30   # player healer: % of ally max HP restored per cast (tunable)
ROSTER_PATHS = ["/mnt/project/roster.json", "roster.json", "/mnt/user-data/uploads/roster.json"]

# ---------- power curves (mirror progression_slice_spec + enemy spec) ----------
def lvl_mult(L):  return 1.0 + 0.5 * ((L - 1) / 99)          # 1.0 -> 1.5
def player_gear(D): return min(0.45 + ((D - 1) / 100) * 0.5, 0.95)
def enemy_gear(D):  return max(0.0, min(0.9, (D - 1) / 100 * 0.9))  # 0 at L1
def gear_mult(f): return 1.0 + 0.7 * f
def mitig(raw, dfp): return raw * K / (K + dfp)

# ---------- affinity wheel ----------
TRIANGLE = {"judgment": "life", "life": "revelation", "revelation": "judgment"}  # key beats value
OFFWHEEL = {"majesty", "mystery"}
def wheel_bonus(att_aff, def_aff):
    """+15% dmg when attacker has advantage; off-wheel never penalized vs RGB."""
    if att_aff in TRIANGLE and TRIANGLE[att_aff] == def_aff: return 1.15
    if att_aff == "majesty" and def_aff == "mystery": return 1.15
    if att_aff == "mystery" and def_aff == "majesty": return 1.15
    return 1.0

# ---------- enemy anchors (player L1 medians by role, from roster.json) ----------
ENEMY_ANCHOR = {
    "bruiser": {"hp": 820,  "atk": 225, "def": 160, "spd": 118},
    "warden":  {"hp": 1300, "atk": 160, "def": 250, "spd": 93},
    "mender":  {"hp": 900,  "atk": 172, "def": 185, "spd": 109},
    "hexer":   {"hp": 810,  "atk": 200, "def": 165, "spd": 118},
    "zealot":  {"hp": 800,  "atk": 210, "def": 170, "spd": 108},
}
ENEMY_AFF = ["judgment", "life", "revelation", "majesty", "mystery"]

# =====================================================================
# Combatant
# =====================================================================
@dataclass
class Ability:
    name: str; mult: float; cooldown: int; target: str
    effects: list = field(default_factory=list)
    bonus_vs: dict = None
    heal: bool = False        # flags a support ability (heal/shield) — treated as sustain
    _cd_ready: int = 0        # turns until usable (0 = ready)

@dataclass
class Combatant:
    name: str; aff: str; role: str
    hp: int; max_hp: int; atk: int; dfp: int; spd: int
    abilities: list
    is_enemy: bool = False
    alive: bool = True
    # persistent debuffs on this unit (id -> turns remaining), simplified
    debuffs: dict = field(default_factory=dict)

    def def_effective(self):
        d = self.dfp
        if "def_break" in self.debuffs: d *= 0.55
        return d

    def tick_cds(self):
        for a in self.abilities:
            if a._cd_ready > 0: a._cd_ready -= 1
        for k in list(self.debuffs):
            self.debuffs[k] -= 1
            if self.debuffs[k] <= 0: del self.debuffs[k]

# =====================================================================
# Build player combatants from roster.json
# =====================================================================
def load_roster():
    for p in ROSTER_PATHS:
        if os.path.exists(p):
            return json.load(open(p))["units"]
    raise SystemExit("roster.json not found")

def build_player(u, level):
    m = lvl_mult(level) * gear_mult(player_gear(level))
    b = u["baseStats"]
    abs_ = []
    for a in u["abilities"]:
        mult = a.get("mult")
        heal = mult is None or any(e.get("id","").startswith(("regen","shield","heal")) for e in a.get("effects",[]))
        abs_.append(Ability(a["name"], float(mult) if mult else 0.0, int(a.get("cooldown",0)),
                            a.get("target","one_enemy"), a.get("effects",[]), a.get("bonus_vs"), heal))
    return Combatant(u["name"], u["affinity"], u["role"],
                     hp=round(b["hp"]*m), max_hp=round(b["hp"]*m),
                     atk=round(b["atk"]*m), dfp=round(b["def"]*m), spd=round(b["spd"]*lvl_mult(level)),
                     abilities=abs_)

# =====================================================================
# Build enemies
# =====================================================================
def make_enemy(role, D, aff, boss=False, name=None):
    a = ENEMY_ANCHOR[role]; m = lvl_mult(D) * gear_mult(enemy_gear(D))
    hp_mult, ad_mult = (1.6, 1.25) if boss else (1.0, 1.0)
    abils = [Ability("Strike", 1.0, 0, "one_enemy")]
    if boss:
        # >=2 significant abilities (locked). Pick by archetype.
        arche = {"bruiser":"sprint","warden":"bulwark","mender":"purist",
                 "hexer":"plague","zealot":"siege"}[role]
        if arche == "sprint":
            abils += [Ability("Rising Fury", 1.2, 3, "self", [{"id":"atk_up","mag":20,"dur":3}]),
                      Ability("Cleave", 1.4, 2, "all_enemies")]
        elif arche == "bulwark":
            abils += [Ability("Molten Guard", 0.0, 4, "self", [{"id":"def_up","mag":40,"dur":3}], heal=True),
                      Ability("Ground Slam", 1.5, 3, "all_enemies", [{"id":"slow","mag":15,"dur":2}])]
        elif arche == "purist":
            abils += [Ability("Renewing Tide", 0.0, 3, "self", [{"id":"regen","mag":5,"dur":4}], heal=True),
                      Ability("Wither", 1.3, 3, "one_enemy", [{"id":"def_break","mag":30,"dur":3}])]
        elif arche == "plague":
            abils += [Ability("Rot Bloom", 1.2, 2, "all_enemies", [{"id":"def_break","mag":25,"dur":3}]),
                      Ability("Fester", 1.0, 5, "all_enemies", [{"id":"debuff_bomb","mag":0,"dur":5}])]
        else:  # siege
            abils += [Ability("Sweep", 1.0, 0, "all_enemies"),
                      Ability("Ashen Vigil", 0.0, 4, "self", [{"id":"regen","mag":4,"dur":4}], heal=True)]
        nm = name or f"{role.title()} Sub-Boss [{arche}]"
    else:
        if role == "mender":
            abils.append(Ability("Mend", 0.0, 2, "self", [{"id":"heal","mag":28,"dur":0}], heal=True))
        nm = name or role.title()
    return Combatant(nm, aff, role,
                     hp=round(a["hp"]*m*hp_mult), max_hp=round(a["hp"]*m*hp_mult),
                     atk=round(a["atk"]*m*ad_mult), dfp=round(a["def"]*m*ad_mult),
                     spd=round(a["spd"]*lvl_mult(D)), abilities=abils, is_enemy=True)

# =====================================================================
# Run generation (RNG-lite per enemy spec)
# =====================================================================
def gen_run(D, rng):
    fights = 3 + rng.randrange(7)          # 3..9 normal fights
    tint = rng.choice(ENEMY_AFF)
    comps = []
    for _ in range(fights):
        n = 2 + (rng.randrange(3) if D < 40 else rng.randrange(2)+1)  # 2-4, more up high
        roles = []
        # variety-over-guarantee: weight toward a "question" but don't force it
        pool = ["bruiser","bruiser","warden","zealot","hexer","mender"]
        for _ in range(n):
            r = rng.choice(pool)
            roles.append(r)
        comps.append(roles)
    boss_role = rng.choice(["bruiser","warden","mender","hexer","zealot"])
    return {"D": D, "fights": fights, "tint": tint, "comps": comps, "boss_role": boss_role}

def spawn_enemies(roles, D, tint, rng):
    out = []
    for r in roles:
        aff = tint if rng.random() < 0.6 else rng.choice(ENEMY_AFF)  # 60% tint
        out.append(make_enemy(r, D, aff))
    return out

# =====================================================================
# Fight resolution (one fight; mutates the player team's HP + cooldowns)
# =====================================================================
def choose_ability(actor, allies, foes):
    ready = [a for a in actor.abilities if a._cd_ready == 0]
    # supports: heal if an ally is hurt (proactive — real healers top up, not just emergency)
    if not actor.is_enemy:
        hurt = [c for c in allies if c.alive and c.hp < 0.75*c.max_hp]
        heals = [a for a in ready if a.heal]
        if hurt and heals: return max(heals, key=lambda a: (a.mult, a.cooldown))
    else:
        heals = [a for a in ready if a.heal]
        if heals and actor.hp < 0.6*actor.max_hp: return max(heals, key=lambda a:a.cooldown)
    dmg = [a for a in ready if a.mult > 0]
    if not dmg: return actor.abilities[0]     # fallback basic
    # highest-impact ready damage ability (mult * cd as a rough value proxy)
    return max(dmg, key=lambda a: a.mult * (1 + 0.3*a.cooldown))

def pick_target(actor, foes, rng):
    """Realistic target selection. Enemies spread aggro with tank pulling extra threat
    (stands in for taunt/positioning the real engine has). Players focus the lowest-HP foe."""
    live = [c for c in foes if c.alive]
    if not live: return None
    if actor.is_enemy:
        weights = []
        for c in live:
            w = 2.5 if c.role == "tank" else 1.0
            w *= 1.0 + 0.3*(1 - c.hp/c.max_hp)   # slight lean toward hurt targets
            weights.append(w)
        return rng.choices(live, weights=weights, k=1)[0]
    return min(live, key=lambda c: c.hp)          # players focus-fire lowest

def apply_ability(actor, ab, allies, foes, log, rng):
    tgt_all = "all" in ab.target
    if ab.mult > 0:
        if ab.target == "self":
            targets = []
        elif tgt_all:
            targets = [c for c in foes if c.alive]
        else:
            t = pick_target(actor, foes, rng)
            targets = [t] if t else []
        for t in targets:
            raw = ab.mult * actor.atk
            if ab.bonus_vs and ab.bonus_vs.get("condition")=="target_hp_below_50" and t.hp < 0.5*t.max_hp:
                raw *= (1 + ab.bonus_vs["amount"])
            raw *= wheel_bonus(actor.aff, t.aff)
            dmg = mitig(raw, t.def_effective())
            t.hp -= dmg
            if t.hp <= 0: t.alive = False
    # effects
    for e in ab.effects:
        eid = e.get("id","")
        if ab.target == "self":
            if eid == "atk_up":
                actor.atk = round(actor.atk * (1 + e.get("mag",0)/100.0))   # enrage ramp; stacks per cast
            elif eid == "def_up":
                actor.dfp = round(actor.dfp * (1 + e.get("mag",0)/100.0))
        else:
            for t in ([c for c in foes if c.alive]):
                if eid in ("def_break","slow"): t.debuffs[eid] = e.get("dur",2)
    # sustain (regen/heal). Ally-healers (player 'heal' role, enemy 'mender') restore HP.
    # Handles: single-ally heal, all-ally (team) heal, and heal-on-attack (drain) kits.
    if ab.heal:
        ally_healer = (actor.is_enemy and actor.role == "mender") or \
                      (not actor.is_enemy and actor.role == "heal")
        pct = MENDER_HEAL_PCT if actor.is_enemy else PLAYER_HEAL_PCT
        if ally_healer:
            heal_targets = []
            if "all" in ab.target:                       # team heal (e.g. Lifeblood)
                heal_targets = [c for c in allies if c.alive]
            elif ab.target == "self":                    # self-only sustain
                heal_targets = [actor]
            else:                                        # attack that heals (drain) -> heal most-hurt ally
                live = [c for c in allies if c.alive]
                if live: heal_targets = [min(live, key=lambda c: c.hp/c.max_hp)]
            per = pct if "all" not in ab.target else pct*0.6   # team heal weaker per-head
            for t in heal_targets:
                t.hp = min(t.max_hp, t.hp + per*t.max_hp)
        else:
            actor.hp = min(actor.max_hp, actor.hp + 0.12*actor.max_hp)
    ab._cd_ready = ab.cooldown

def resolve_fight(team, enemies, log, rng, max_rounds=40):
    for e in enemies: e.alive = True
    rnd = 0
    while rnd < max_rounds:
        rnd += 1
        order = sorted([c for c in team+enemies if c.alive], key=lambda c:-c.spd)
        for actor in order:
            if not actor.alive: continue
            allies = team if actor in team else enemies
            foes   = enemies if actor in team else team
            if not any(f.alive for f in foes): break
            ab = choose_ability(actor, allies, foes)
            apply_ability(actor, ab, allies, foes, log, rng)
        for c in team+enemies: c.tick_cds()
        if not any(e.alive for e in enemies): return "WIN", rnd
        if not any(c.alive for c in team):    return "LOSS", rnd
    return "TIMEOUT", rnd

# =====================================================================
# Full run
# =====================================================================
def simulate_run(team_units, D, seed=0, verbose=True):
    rng = random.Random(seed)
    run = gen_run(D, rng)
    team = [build_player(u, D) for u in team_units]
    log = []
    if verbose:
        print(f"\n=== RUN @ Lv{D} (Tier {(-(-D//10))}) | {run['fights']} fights + sub-boss "
              f"| {run['tint'].title()}-tinted | seed {seed} ===")
        tot = sum(c.max_hp for c in team)
        print(f"Team: {', '.join(f'{c.name}({c.role})' for c in team)}  | team maxHP {tot}")
    results = []
    for i, roles in enumerate(run["comps"], 1):
        enemies = spawn_enemies(roles, D, run["tint"], rng)
        res, rounds = resolve_fight(team, enemies, log, rng)
        hp_pct = sum(max(0,c.hp) for c in team)/sum(c.max_hp for c in team)
        alive = sum(c.alive for c in team)
        results.append((f"Fight {i}", res, rounds, hp_pct, alive, [r for r in roles]))
        if verbose:
            print(f"  Fight {i}: {res:7} in {rounds:2}r | team HP {hp_pct*100:4.0f}% | {alive}/{len(team)} alive | vs {roles}")
        if res == "LOSS":
            if verbose: print("  >> WIPED before sub-boss.")
            return summarize(results, wiped=True)
        # partial recovery between fights (attrition rule: NOT a full heal)
        for c in team:
            if c.alive: c.hp = min(c.max_hp, c.hp + 0.15*c.max_hp)  # 15% between-fight regen
    # sub-boss
    boss = make_enemy(run["boss_role"], D, run["tint"], boss=True)
    res, rounds = resolve_fight(team, [boss], log, rng)
    hp_pct = sum(max(0,c.hp) for c in team)/sum(c.max_hp for c in team)
    alive = sum(c.alive for c in team)
    results.append(("SUB-BOSS", res, rounds, hp_pct, alive, [boss.name]))
    if verbose:
        print(f"  SUB-BOSS: {res:7} in {rounds:2}r | team HP {hp_pct*100:4.0f}% | {alive}/{len(team)} alive | {boss.name}")
    return summarize(results, wiped=(res!="WIN"))

def summarize(results, wiped):
    cleared = not wiped
    return {"cleared": cleared, "results": results,
            "final_hp": results[-1][3] if results else 0.0,
            "reached_boss": any(r[0]=="SUB-BOSS" for r in results)}

# =====================================================================
# Teams
# =====================================================================
def pick_team(units, kind):
    byrole = {}
    for u in units: byrole.setdefault(u["role"], []).append(u)
    def first(role, n=1): return byrole.get(role, [])[:n]
    if kind == "balanced":
        return (first("solo_dmg") + first("tank") + first("heal") + first("debuff"))[:4]
    if kind == "badcomp":   # 4 tanks — the designed failure (can't out-damage a mender)
        return byrole.get("tank", [])[:4]
    if kind == "glass":     # 4 carries — melts normal fights, risks survivability spikes
        return byrole.get("solo_dmg", [])[:4]
    return byrole.get("solo_dmg", [])[:4]

# =====================================================================
# Main
# =====================================================================
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", type=int, default=40)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--team", default="balanced", choices=["balanced","badcomp","glass"])
    ap.add_argument("--sweep", action="store_true")
    ap.add_argument("--trials", type=int, default=1)
    args = ap.parse_args()
    units = load_roster()

    if args.sweep:
        print("LEVEL SWEEP — balanced team, 20 seeds each, clear-rate + median final HP")
        team = pick_team(units, "balanced")
        for D in range(10, 101, 10):
            outs = [simulate_run(team, D, seed=s, verbose=False) for s in range(20)]
            clears = sum(o["cleared"] for o in outs)/len(outs)
            hp = st.median([o["final_hp"] for o in outs if o["reached_boss"]] or [0])
            print(f"  Lv{D:3}: clear {clears*100:3.0f}% | median final-HP@boss {hp*100:4.0f}%")
        # failure demo
        print("\nFAILURE DEMO — 4-tank badcomp vs Lv40 (should struggle on Mender fights):")
        bt = pick_team(units, "badcomp")
        outs = [simulate_run(bt, 40, seed=s, verbose=False) for s in range(20)]
        print(f"  clear rate: {sum(o['cleared'] for o in outs)/len(outs)*100:.0f}%")
        return

    team = pick_team(units, args.team)
    if args.trials == 1:
        simulate_run(team, args.level, seed=args.seed, verbose=True)
    else:
        outs = [simulate_run(team, args.level, seed=s, verbose=False) for s in range(args.trials)]
        print(f"Lv{args.level} {args.team}: clear {sum(o['cleared'] for o in outs)/len(outs)*100:.0f}% "
              f"over {args.trials} runs")

if __name__ == "__main__":
    main()
