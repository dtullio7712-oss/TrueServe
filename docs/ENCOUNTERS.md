# ENCOUNTERS.md — the encounter-type menu

> The menu we build encounters FROM. One short spec per type, tagged by:
> **Archetype-question** (what team-shape it forces) · **Reward-type** · **Gating-axis** (what
> caps entry) · **Authoring cost** (how expensive to make more of).
> Discipline: **prove the core loop with ONE type before authoring the menu.** (See plan, §end.)
>
> Cross-refs: `power_model_v3.py` (K=1000, BUILD_MULT=2.5), `GEARING.md` (7 gear tiers),
> `encounter_BOSS_archetype_flip.md` (the Warden of Ash — first fully-specced example),
> archetype templates: Siege(survivability) / Sprint(SPD+burst) / Plague(cleanse) /
> Bulwark(strip+def-pen) / Purist(heal) / Warden(control) / Zealot(affinity) / Gauntlet(depth).

---

## Owner's four (sharpened)

**1. Abyss — the fixed-climb crucible.** Static floors (mastery = memorization) but each floor
carries a randomized **mutator** from a deck ("no cleanse," "enemies enrage at 50%," "only Blue
acts first," "team shares one HP pool"). Ultra-good STATIC rewards on first clear; a randomized
"resonance" reward on repeat clears so it never goes dead. The skill-ceiling flagship.
*Archetype: Gauntlet (rotating). Reward: top-tier static + RNG repeat. Gate: raw power wall + roster depth. Cost: HIGH (bespoke floors) — offset by the mutator deck making reruns free.*

**2. Story / Grind — the bread-and-butter loop.** Randomized dungeon → RNG'd sub-boss, basic-
but-good rewards. Sub-boss rolls from a small pool of archetype templates (Siege/Sprint/Warden)
so it stays fresh with ZERO extra writing. No novel needed — flavor is light, systems are the game.
*Archetype: rolls per run. Reward: basic staples (the daily loop). Gate: content level = gear tier. Cost: LOW (template-driven — the reason to build this FIRST).*

**3. Hunts — gear-specific bosses.** Each boss themed to a gear set and drops it. The boss
**demands the thing it drops** (the Speed-hunt out-tempos you unless you already have some SPD;
the Bulwark-hunt walls you unless you brought def-pen) — a self-teaching curve where the reward
is the answer to the next difficulty.
*Archetype: matches the set (Sprint-hunt, Bastion-hunt…). Reward: targeted gear set. Gate: soft affinity + the set's own stat. Cost: MED (one boss per set, ~11 stat + 8 effect sets).*

**4. Event / Holiday / Affinity / Material bosses — rotating farm.** Affinity bosses = the
HARD-gate content (mono-color walls, per "hard gating begins Tier 7"). Material bosses = pure
farm, low skill floor, high throughput. Holiday/event = limited-window reskins of existing
templates with cosmetic/currency rewards (non-predatory: earned, never sold).
*Archetype: varies. Reward: currency / mats / cosmetics / event gear. Gate: window + affinity. Cost: LOW (template reskins).*

---

## New types — the creative expansion

**5. The Mirror.** The boss is a COPY of your own team — snapshots the units + gear you bring and
fights you with them. Out-play your own comp. Zero authoring cost, infinite variety, teaches
players their own weaknesses. Reward scales to how fast you beat "yourself."
*Archetype: whatever YOU built (self-referential). Reward: scaling. Gate: your own power. Cost: NEAR-ZERO — highest value-per-effort on the list.*

**6. The Living Puzzle.** A boss with a stated rule you must discover + exploit — "immune to all
damage except the turn after it's Silenced," "reflects damage unless a debuff is on it." Not a
stat check — a logic lock. Creates community "how do I beat X" moments.
*Archetype: none (puzzle). Reward: prestige + one-time gear. Gate: knowledge, not power. Cost: MED (each needs a unique clever rule) but each is memorable.*

**7. Endless / Attrition Tower.** No clear condition — HP + cooldowns carry across infinite
escalating waves (the attrition rule to its limit). Farm until you break; reward scales to depth.
Leaderboard-lite / bragging rights WITHOUT PvP FOMO.
*Archetype: Gauntlet (endless). Reward: depth-scaled. Gate: sustain + roster depth. Cost: LOW (one scaling curve, procedural waves).*

**8. Gauntlet-of-One (roster-lock).** Each unit usable only ONCE across N sequential bosses —
win and those units are spent. Forces spreading the whole collection, not spamming a god-team.
Makes every Common matter. Deeply on-ethos ("every unit stays valuable").
*Archetype: Gauntlet + depth-hard. Reward: big (collection-completion flex). Gate: roster BREADTH. Cost: LOW (reuses existing bosses under one rule).*

**9. Escort / Protect.** An allied NPC you don't control must survive. Flips "kill fast" to
"control + peel + threat-management." Tests taunt/control in a way DPS races never do.
*Archetype: Warden-adjacent (control/peel). Reward: staple + unique. Gate: control tools. Cost: MED (needs NPC-ally AI).*

**10. The Reckoning (affinity roulette).** Each floor forces a DIFFERENT required affinity
(floor 1 Red-only, floor 2 Green-only…). Can't clear without a broad, invested roster across all
colors. The ultimate "did you build EVERYONE" gate.
*Archetype: Zealot (all colors). Reward: big + affinity mats. Gate: full-roster investment. Cost: LOW (reskin + affinity lock per floor).*

**11. Corruption / Curse boss.** Applies a permanent-for-the-run debuff each phase that you CARRY
into the next fight (a compounding `wasting`). A single boss becomes a race against your own decay
— rewards burst + sequencing over grind.
*Archetype: Sprint under pressure. Reward: strong. Gate: burst + tempo. Cost: MED (persistent-debuff plumbing).*

**12. Puzzle-Boss with a "solution unit."** Trivially beaten if you bring the specific niche Common
whose kit answers its gimmick — hard otherwise. Makes obscure units suddenly the hero. THE single
best mechanic for making 100 units feel deep, not "top 10 + filler."
*Archetype: none (key-lock). Reward: staple + the satisfaction. Gate: owning/knowing the key unit. Cost: MED — design each around one underused unit; enormous roster-depth payoff.*

**13. Combo / Chain boss.** Rewards SEQUENCED effects — takes bonus damage only when hit by 3
different affinities in one round, or when a DoT is detonated on it. The fight becomes an execution
puzzle. Straight-up the "chess player" audience.
*Archetype: Combo (sequencing). Reward: strong + prestige. Gate: kit synergy. Cost: MED.*

**14. Condition / Sandbox-tied boss.** Beatable only under a condition the SANDBOX generates
(a "night" boss; a boss that appears when the town hits X). Ties the two game-halves together —
gives the sandbox teeth in combat.
*Archetype: varies. Reward: bridges economies. Gate: sandbox progress. Cost: MED (needs the sandbox half online — LATER).*

---

## Reward-type map (so no two encounters overlap)

- **Story/Grind** → basic staple currency + common gear (the daily faucet)
- **Hunts** → targeted gear SETS
- **Abyss / Endless / Gauntlet-of-One** → top-tier gear + prestige (the chase)
- **Material bosses** → upgrade mats (the sink-feeder)
- **Puzzle / Combo / Living Puzzle** → one-time uniques + prestige
- **Affinity / Reckoning** → affinity-specific mats + roster-breadth rewards
- **Event/Holiday** → cosmetics + event currency (time-limited, earned)

---

## THE PLAN → playtest (build order)

- **Phase 0 (this file, ~DONE):** the taxonomy menu. Prevents redundant designs. ✅
- **Phase 1 (next session):** fully-spec **ONE** type — recommend **Story/Grind randomized dungeon** (exercises the most systems: run structure, escrow, attrition, RNG sub-boss, rewards). Tune to the real math like the Warden.
- **Phase 2:** build `encounter_sim.py` — the Warden sim generalized. Feed boss statline + team → get fight-length + gate pass/fail. The multiplier: every future encounter verified in minutes.
- **Phase 3:** wire the Story dungeon + 3–4 real roster teams into the prototype and PLAY IT. Answer only: **is the core loop fun?**
- **Phase 4 (post-proof, ongoing):** fan out the exciting types (Mirror → Puzzle-Boss → Abyss) via the harness. Cheap now.

**Rule (from PROJECT_CONTROL):** prove the loop with one encounter type before authoring the menu. This file IS the menu — bank it, build ONE, playtest, then unleash.

---

## NEXT SESSION STARTS HERE
Phase 1: fully-spec the **Story/Grind randomized dungeon** (template-rolled sub-boss pool:
Siege / Sprint / Warden), tuned to K=1000 / BUILD_MULT at an early-mid tier. Then Phase 2 sim harness.
