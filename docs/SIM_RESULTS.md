# encounter_sim.py — Results & Findings (Phase 2 complete)

The harness is built and runs full generated runs (3–9 fights → sub-boss) with **HP +
cooldowns carrying across the chain**, grounded in the real `roster.json` statlines,
K=1000 model, affinity wheel, and the enemy scaling curve from `enemy_profiles_scaling.md`.

## What it does
- **Generates** a run at any dungeon level (RNG-lite: fight count 3–9, compositions, tint, sub-boss archetype).
- **Simulates** each fight turn-by-turn (SPD order, cooldown-gated ability choice, mitigation, wheel bonus, def_break).
- **Carries attrition** — 15% between-fight regen only, so runs are a resource-management arc, not isolated fights.
- **Reports** per-fight result, team HP %, survivors, and whether the sub-boss was reached.
- Modes: single verbose run, `--sweep` (clear-rate across all 10 tiers), `--team badcomp/glass` for failure demos.

## ⚠️ CORRECTION (owner caught this) — healing flattens HP-attrition

An earlier version of this writeup reported a clean "attrition arc" (HP steadily declining to
the sub-boss, 75% clears at cap) and built a difficulty narrative on it. **That was an artifact
of a bug: the player's healer only healed *itself*, not allies** — the team's dedicated healer
was doing almost nothing, so of course HP only went down.

With the healer fixed to actually heal allies (single-target, team-heal, and drain shapes all
handled), the real picture is very different:

| Dungeon Lv | Clear rate | Median HP at sub-boss |
|---|---|---|
| 10–100 | **100% everywhere** | **95–100%** |

A working healer **flattens the entire 100-level curve.** HP barely dips (a Lv55 run reads
100% → 97% → 97% → 95% → 98%) and the team reaches the sub-boss essentially full. HP even
*recovers* between and during fights.

### The real lesson (more valuable than the wrong one)
**HP-as-attrition is a weak difficulty lever in a game with dedicated healing.** Raw enemy ATK
and HP totals barely matter — the healer just refills the tank. Difficulty has to come from
pressures a healer *can't* simply answer:

1. **Burst > heal-rate** — an enemy alpha that kills a unit in one turn, before the heal lands.
   A survivability/positioning check, not an HP-pool check.
2. **Heal denial** — anti-heal / heal-block debuffs (a Hexer speciality). Turn the healer off
   and HP attrition becomes real again.
3. **Time pressure** — enrage or a **turn-cap loss**. "Out-heal forever" should still lose,
   which forces real DPS.
4. **Resource denial** — silence/stun aimed at the healer. A control check.

**Implication:** normal-fight difficulty should be driven by **damage spikes + enemy debuff
pressure (heal denial) + the turn-cap**, NOT by enemy HP/ATK totals. The scaling curve validated
earlier still correctly keeps enemies on the player's scale — but scaling ATK/HP is not what
makes a dungeon hard. **Enemy kit design (burst concentration, heal-denial, control) is the real
difficulty lever.** This reframes the difficulty model and should propagate into
`enemy_profiles_scaling.md`.

---

## ✅ CONFIRMED — an enrage boss naturally breaks the mono-tank team (no turn-cap needed)

Owner's model: *don't* add an artificial turn-cap loss. As enemies scale — especially at the
boss, which hits like a hammer repeatedly and can carry an enrage — a pure-tank team should be
naturally overwhelmed, unable to out-sustain the incoming damage. **The sim confirms this holds
— but only under specific boss settings, and finding them corrected two more sim gaps:**

1. **Enrage was inert.** The boss's `Rising Fury` (`atk_up`) was flagged "modeled lightly" and
   never actually raised the boss's ATK. Fixed: self `atk_up`/`def_up` now apply and **stack per
   cast**, so enrage genuinely ramps.
2. **Roster tanks are NOT low-DPS.** Four tanks at ~250–300 ATK push ~1,167 dmg/round at Lv100 —
   real damage. So "4 tanks" is a *tanky-bruiser* team that both survives and kills, not a
   weak-damage team. With the default ×1.6 sub-boss HP, it kills the boss in ~3 rounds — before
   enrage can ramp at all.

**The lever that makes the model real is boss HP (fight duration) × enrage rate, NOT enemy ATK
scaling.** Solved for it directly (Lv100, boss enrage sweep):

| Boss HP premium | Enrage | CD | Balanced | 4-TANK |
|---|---|---|---|---|
| 1.6× (current) | 20% | 3 | 100% | 100% |
| 1.6× | 50% | 2 | 100% | 100% |
| 3.5× | 20% | 3 | 100% | 100% |
| **3.5×** | **35%** | **2** | **100%** | **0%** ✅ |
| **3.5×** | **50%** | **2** | **100%** | **0%** ✅ |

At **~3.5× HP + a 35%+ enrage on a 2-turn cooldown**, the boss outlives the tank team's damage,
the enrage spirals, and the mono-tank team is wiped — while a balanced team with real DPS kills
it *before* the spiral. Exactly the owner's model, achieved with zero artificial timers.

### Consequence for the enemy spec
**The ×1.6 sub-boss HP premium is too low for enrage-type bosses.** Enrage only threatens
anything if the boss survives long enough to ramp. So:
- **Enrage / Sprint sub-bosses need a much higher HP premium (~3× or more) + a real enrage
  (~35%+ atk per ≤2-turn cast).** This pairing is what punishes low-DPS-flavored comps.
- Non-enrage sub-bosses can keep a lower premium; their threat comes from their signature
  (Bulwark strip-wall, Plague bomb, etc.), not from outliving your damage.
- This should be written into `enemy_profiles_scaling.md` §4 as a per-archetype HP premium,
  replacing the flat ×1.6.

---

## Original headline (NOW SUPERSEDED — kept for the record)

Level sweep, balanced team (carry/tank/heal/debuff), 20 seeds per tier:

| Dungeon Lv | Clear rate | Median HP at sub-boss |
|---|---|---|
| 10 | 100% | 81% |
| 20 | 100% | 75% |
| 30 | 100% | 71% |
| 40 | 100% | 66% |
| 50 | 100% | 65% |
| 60 | 95% | 63% |
| 70 | 85% | 57% |
| 80 | 80% | 60% |
| 90 | 80% | 56% |
| 100 | 75% | 58% |

**This is the target shape.** A well-built same-level team reliably clears its own level, and
the win margin *narrows* as you climb (100%→75%) because the enemy gear curve ramps. Final HP
sitting in the 55–80% band means runs cost real resources without being coinflips. A sample
verbose run (Lv55) shows the attrition arc cleanly: 99% → 86% → 69% → 64% → sub-boss at 66%,
losing one unit to the boss. That "you won, but it cost you" texture is exactly the design.

## Balance bugs the harness caught (the reason it exists)

1. **Unmitigated focus-fire (severe).** First pass had all enemies hard-target the lowest-HP
   unit every round → squishies died in ~1.5 rounds → 0–25% clears even for good teams. Fixed
   with realistic aggro spread (tanks pull ~2.5× threat, mild lean toward hurt targets). This
   stands in for the taunt/positioning the real engine will have. Clear-rate jumped to the
   correct curve above. *Lesson: enemy target AI matters as much as statlines.*

2. **Mender was self-only.** A healer that only heals itself is not a force-multiplier. Fixed
   so Menders heal the most-hurt ally (28% max HP) — now they're a real threat-extender.

## Open finding — "lone healer = DPS wall" is NOT automatic

Your `4 tanks can't out-damage a healer` example is the right *intuition*, but the sim shows it
doesn't hold with a **lone** mender: 4 L40 tanks push ~1,100 raw atk/round, enough to grind
through a mender+2-warden comp regardless of heal size (tested up to 70%/cast on CD1 — still
100% tank clears). The wardens die first, then the mender gets focused before its healing
compounds.

**A DPS check only bites when the healer's throughput can outrun the team's damage over the
fight's length.** Options to make it real (a genuine design call, not a bug):
- Enemy **healer + shielder** pair (peels keep the healer alive long enough to matter), or
- A **3+ warden** wall so low-DPS teams can't reach the healer before enrage/timeout, or
- A mender whose heal **scales with fight length** (regen-style, ramping), or
- A **soft-enrage/timeout loss** so "can't kill fast enough" is an actual failure state (the sim
  currently only loses on wipe, not on timeout — see below).

Recommend: add a **turn-cap loss** to the grind loop (e.g. a fight lost if not won in N rounds).
That single rule turns every low-DPS comp into a real failure, which is what makes the Mender —
and the whole "bring enough damage" lesson — actually teach.

## Known simplifications (harness, not shipping engine)
- No crit, no Momentum/turn-meter (uses flat SPD order), effects limited to def_break/slow/heal.
- Self-buffs (def_up/atk_up/regen on bosses) are modeled lightly.
- Loss = wipe only; **no timeout-loss yet** (the key gap above).
- Player AI = "highest-impact ready ability + focus lowest"; enemy AI = spread aggro.
These are fine for balance-shape validation; the real feel test is Phase 3 (prototype).

## Recommended next tuning pass
1. Add **turn-cap loss** → re-run the badcomp demo; expect 4-tank clears to fall sharply. This
   is the single highest-value change and directly validates the core design promise.
2. Sweep **enemy composition weights** to confirm difficulty per tier feels right with the cap on.
3. Then Phase 3: wire one generated run into the combat prototype and play it for *feel*.

## How to run
```
python3 encounter_sim.py --level 40 --seed 7        # one verbose run
python3 encounter_sim.py --sweep                    # clear-rate across all tiers
python3 encounter_sim.py --level 40 --team badcomp  # 4-tank failure demo
python3 encounter_sim.py --level 60 --trials 50     # clear-rate at one level
```
