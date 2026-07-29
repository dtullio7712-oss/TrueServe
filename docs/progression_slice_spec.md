# progression_slice_spec.md — v0.1 (DRAFT → needs playtest)

> **Deliverable of this session:** the progression & rewards layer that wraps combat.
> Turns "a fight" into "a run of fights that matter because loot + growth carry forward."
> Build target: extend the existing throwaway browser prototype. Feel-first, math-proven.
>
> **Reconcile-on-build note:** baseline stat numbers below are set from the design doc's
> LOCKED mechanics, not read from the built prototype (that file wasn't in this session's
> mount). Before implementing, diff these against the prototype's actual statline and keep
> whichever the first playtest proved fun; the *formulas* are the deliverable, the *constants*
> are tunable dials.

---

## 0. What this spec locks vs. sketches

**Specced DEEP (the spine):** stat model, level-up allocation, equipment + substats, the
attrition run structure, and the reward→growth loop math.

**Specced as buildable MVP (thin but real):** crafting, the 5-dungeon curve, the in-fight
profile viewer.

**NOT in this spec:** the outside-combat sandbox feeders (town/farming), summoning/banners,
overworld. Those are downstream per PROJECT_CONTROL.

---

## 1. Decisions locked THIS session (update PROJECT_CONTROL)

1. **Affinity ≠ Unit.** Affinity is the unit's **type** (combat archetype). Unit **name**
   is independent. Many units can share one affinity (10 different Justice units is expected
   and supported). *This corrects the design doc, which conflated virtue-identity with the unit.*
2. **Roster fork — RETIRED.** Combat units = a **separate summoned roster**. Overworld = a
   single character; unit-followers are deferred cosmetic. (Closes a v0.1 open question.)
3. **Loss model — run-based escrow.** A dungeon = **10 sequential battles**, #10 is a boss.
   Rewards drop into a **temporary run inventory (escrow)**. Win all 10 → escrow commits to
   permanent inventory. **Lose any battle → escrow wiped, restart the dungeon at battle 1.**
   Character levels/gear you brought *in* persist; you lose the *run's* loot and position.
4. **Attrition run.** HP and cooldowns **carry across all 10 battles**. No free heal between
   fights. This is the core tension: sloppy early fights bleed you before the boss.
5. **Stat allocation — full min-max.** Per-level assignable points + respec + gear substats.

---

## 2. Affinity vs. Unit — the corrected model

### 2.1 Affinity (the TYPE)
An **Affinity** is a reusable combat archetype. It defines:
- The unit's place on the **Affinity Wheel** (see §7) for advantage math.
- A **kit template** — the mechanical shape of its skills (e.g. Patience = per-turn scaling,
  Diligence = Momentum engine). Salvaged from the design doc's virtue-as-mechanic table, but
  now these are *archetypes* that many named units instantiate.
- **Stat-growth leanings** (§4.3) — soft nudges, not locks, since allocation is manual.

Affinities for this slice (7, from the design doc, renamed as *types* not units):
`Patience, Charity, Diligence, Fortitude, Temperance, Hope, Justice`
*(Humility deferred — its "amplify others" kit needs more roster to matter.)*

### 2.2 Unit (the CHARACTER)
A **Unit** is a named instance with:
- a **name** (independent of affinity),
- an **affinity** (one of the above),
- a **base statline** (§3),
- a **kit** (2 skills + 1 ult for this slice) that *varies within* the affinity template so
  two Justice units aren't identical,
- a **rarity** (drives base stats + flexibility per the locked pillar, NOT relevance).

Data-driven: units are JSON/resource entries referencing an affinity id. Adding "a 4th Justice
unit" = a new data row, zero code.

---

## 3. The stat model (6 core stats)

Every unit and enemy uses the **same 6-stat model** (matches the design doc's shared-stat-model
bridge principle):

| Stat | Symbol | Role in math |
|---|---|---|
| **HP** | HP | Health pool. Attrition resource across the run. |
| **Attack** | ATK | Scales outgoing damage. |
| **Defense** | DEF | Reduces incoming damage (diminishing, §6). |
| **Speed** | SPD | Fills the Momentum gauge → turn frequency. |
| **Potency** | POT | How hard your debuffs land (§8). |
| **Resolve** | RES | Resistance to incoming debuffs (§8). |

Crit is handled as **Crit Rate / Crit Damage** derived stats (base 5% / +50%), pushed mainly
by gear substats and affinity advantage (§7), not core allocation — keeps the 6-stat spine clean.

### 3.1 Per-unit level-1 statlines (NOT a shared anchor)
**Every unit has its own hand-authored level-1 statline.** A glass cannon *starts* glassy
(high ATK, low HP); a tank *starts* tanky. Units are distinct characters from level 1, not
clones that diverge later. These live in each unit's `baseStats` data row (§2.2).

**Use the prototype's 4 real statlines as the canonical `baseStats` rows** (Justice = glass
cannon, Charity = tank, etc.). They were playtested and are the truth — do not overwrite them
with a generic anchor.

**Generic fallback anchor (new/un-tuned units + enemies only):** the block below exists ONLY
so a brand-new data row that nobody has hand-designed yet still functions. Real units never use
it. Reconcile these placeholder numbers against the prototype's actual scale before shipping —
prototype DEF sits ~150–260 and HP up into the ~1300 range, so this fallback should be raised
to sit inside that real range, not left at the old tiny values.

```
// FALLBACK ONLY — real units carry their own hand-tuned baseStats
HP   = (mid of prototype range)     // e.g. ~600, NOT 100
ATK  = (mid of prototype range)
DEF  = (mid of prototype range)     // prototype DEF ~150–260
SPD  = 100        // Momentum baseline; see combat slice
POT  = 0.00
RES  = 0.00
CritRate = 0.05
CritDmg  = 0.50
```

**Reconcile note:** the old anchor (HP 100 / ATK 20 / DEF 12) was a placeholder written before
the prototype existed. It is superseded by the prototype's real per-unit stats. Its only lingering
role is as the *shape* of a fallback, not as real numbers.

### 3.2 Rarity multipliers (stats + flexibility, per LOCKED pillar)
Rarity multiplies the **base** statline and grants **more level-up points** (flexibility),
never exclusive access to being useful.

| Rarity | Base stat mult | Points/level (§4.1) |
|---|---|---|
| Common (C)   | 1.00× | 3 |
| Rare (R)     | 1.12× | 4 |
| Epic (E)     | 1.26× | 5 |
| Legendary (L)| 1.42× | 6 |

A Common specialist with a niche key (locked pillar) stays relevant; a Legendary is a flexible
generalist with more points to spread. The gap is ~1.42× stats + 2 pts/level — meaningful but
not a different tier of existence.

---

## 4. Leveling & manual stat allocation (dopamine spine)

### 4.0 The growth budget (READ THIS FIRST — it governs all the numbers below)
Two owner decisions set the entire math:
- **Level cap = 100.** This is a time-sink game with many difficulty milestones.
- **Levels alone give ~1.5× a unit's level-1 stats** at max. **Gear gives ~1.7×** (slightly
  more — gear is the bigger lever). **Combined ceiling ≈ 2.5×** a naked level-1 unit.

This is a **deliberately tight budget** — the #1 defense against overtuning. Enemy dungeon
scaling (§10) is tuned to sit *just under* 2.5×, so players must build to keep pace, but numbers
never run away.

**The hard problem this creates, and how we solve it:** 1.5× growth spread evenly over 99
level-ups is ~0.4%/level — *invisible*, the dopamine-death failure. So growth is **NOT** evenly
felt. Instead:
- **Growth is percentage-of-own-base** (§4.2) so a point is always meaningful regardless of
  whether the unit has 200 HP or 1300 HP.
- **Ordinary levels are a steady drip; every 10th level is a milestone drumbeat** (§4.1b) that
  delivers a chunky bump + a non-stat unlock. The 10 milestones carry the *felt* dopamine; the
  90 ordinary levels carry the *rhythm*.

### 4.1 The level-up moment (the dopamine beat)
On an **ordinary** level-up a unit gains a small **pool of assignable points**. The player opens
the unit and spends them — the tangible "I made this unit stronger, my way" beat. Even-ish
curve: ordinary levels feel similar to each other, steady and earned.

### 4.1b Milestone levels (every 10th level — the drumbeats)
At levels **10, 20, 30 … 100** (10 milestones total) the unit gets a **larger point pool that
level** *plus* a **non-stat reward**:

| Milestone | Non-stat reward (sketch — tune) |
|---|---|
| 10, 30, 50, 70, 90 | Unlock/upgrade a **gear substat slot capacity** or a kit tier |
| 20, 40, 60, 80 | **Kit upgrade** (a skill gains an effect / lower cooldown) |
| **100** | Capstone: a signature passive or the unit's final kit tier |

The point is: a milestone level is a *thing the player looks forward to*, not just more of the
same. Exact rewards are downstream design; the **cadence (every 10) and the "bigger + a bonus"
structure** are what this spec locks.

### 4.2 What a point buys — PERCENTAGE OF THE UNIT'S OWN BASE (the key fix)
The old draft used flat per-point rates (+8 HP, +2 ATK…). **That is retired.** Flat rates are
invisible on a unit whose base is already large. Instead, **each point adds a fixed percentage
of that unit's own level-1 base stat.** A point of HP on a 1300-HP tank adds far more raw HP
than on a 200-HP mage — but the same *proportional* punch. This is what makes growth feel equal
across wildly different statlines.

```
stat_gain_per_point(stat) = base_stat[unit][stat] * POINT_PCT[stat]
```

`POINT_PCT` is tuned so a unit that dumps ALL its level points into one stat over 99 level-ups
reaches roughly **+150% of its base in that stat** (the 1.5× ceiling), and a balanced spread
lands each stat around **+40–60%**. Ratios keep the "no dump stat" shape from the old table
(HP cheapest, SPD guarded):

| Stat | POINT_PCT (per point, as % of base) | Notes |
|---|---|---|
| HP  | highest | cheap bulk; attrition keeps it always relevant |
| ATK | mid | |
| DEF | mid (efficient via the §6 curve) | |
| SPD | lower + **soft-capped** (§4.4) | Momentum compounds; guard it |
| POT | low (these are already %-stats) | |
| RES | low | |

> **Implementation note for Claude Code:** derive the exact `POINT_PCT` values and `points/level`
> so that `(points over 99 levels) × POINT_PCT × single-stat-focus ≈ +1.5× base`, then confirm by
> simulation: a max-level single-stat build should land near 2.5× base *including* gear, and a
> balanced build should feel smooth. Numbers are dials; the **1.5× levels / 2.5× combined ceiling
> is the constraint.** Sanity check against a real prototype statline, not the fallback anchor.

**Milestone check:** because milestones grant bigger pools, a level-10 or level-50 unit should
show a visibly larger single-level jump than the level before it — that contrast IS the drumbeat.

### 4.3 Affinity leaning (nudge, not lock)
Each affinity has a **recommended spread** shown as a faint "suggested" overlay in the UI (e.g.
Fortitude → HP/DEF, Diligence → SPD/POT). Purely advisory — the player can ignore it. This
teaches new players without removing min-max freedom. *(This is the compromise for "high-DEF
units naturally earn more DEF" — we surface the nudge but keep it manual for this build.)*

### 4.4 SPD soft cap (anti-degenerate guard)
Because SPD compounds in a Momentum system (more turns = more everything), unbounded SPD
allocation is the #1 degenerate build risk. Guard: **once allocation has raised SPD past ~+50%
of the unit's base SPD, each further SPD point costs 2 allocation points.** (Percentage-of-base,
consistent with §4.2.) Gear SPD is unaffected (gear has its own budget, §5). This keeps a speed
build *viable* but not *free*, so it competes with bulk/damage instead of dominating.

### 4.5 Respec
Full respec available **between dungeon runs** (never mid-run — mid-run respec would trivialize
the attrition puzzle). Cost: a small crafting material (§9) or free for the MVP — **recommend
free for the first playtest** so players experiment and we learn what builds feel good, then
add a cost once we see degenerate patterns.

### 4.6 XP & the level curve
XP is earned per battle won (§10). **Level cap = 100** (time-sink target, per owner). Curve is a
standard **quadratic-ish** shape (fast early levels for dopamine, slowing later) — but stretched
to pace 100 levels across 5 dungeons plus repeat/farm runs, so the back half is a genuine grind:

```
XP_to_next(L) = round( 50 * L^1.5 )
// L1→2 = 50 · L10→11 ≈ 1,581 · L50→51 ≈ 17,678 · L99→100 ≈ 49,247
```

This is the same proven exponent as before, just uncapped to 100. The **milestone levels (§4.1b)
every 10 give the grind its landmarks** so 100 levels reads as a journey with 10 waypoints, not a
flat slog. Tune the XP-per-battle (§10) so early dungeons carry a player to ~level 15–20 and the
full 100 requires farming the harder dungeons — that repeat-farm demand is what makes it a
time-sink without inflating power (power is still hard-capped at ~2.5×, §4.0).

> **Note:** with 100 levels but only ~1.5× power from them, later levels are intentionally small
> per-level. That is correct and by design — the felt progression at high level comes from
> **milestones + gear**, not from each ordinary level. Do not "fix" small high-level gains by
> inflating them; that breaks the anti-overtuning budget.

---

## 5. Equipment (6 slots + substats)

### 5.1 The 6 slots
Each unit has **6 equipment slots**. Slots are typed so builds are choices, not just "6 of the
same." Proposed types (E7-lineage, renamed neutral):

| Slot | Main-stat pool | Flavor |
|---|---|---|
| 1. **Weapon**   | ATK (fixed main) | offense anchor |
| 2. **Armor**    | HP (fixed main)  | bulk anchor |
| 3. **Emblem**   | DEF (fixed main) | guard anchor |
| 4. **Boots**    | SPD / ATK% / HP% | tempo choice |
| 5. **Charm**    | POT / RES / HP%  | utility choice |
| 6. **Relic**    | CritRate / CritDmg / ATK% | crit/scaling choice |

Slots 1–3 have **fixed main stats** (predictable spine). Slots 4–6 have a **choosable main
stat** from a pool (build identity). This is the proven E7 structure minus the set-bonus
complexity (deferred).

### 5.2 Main stat + substats
Each piece has **1 main stat** (scales with piece level/rarity) and up to **4 substats** rolled
from a pool. Substat pool (this is where **dual-attack chance lives**, per LOCKED decision):

```
Substat pool: ATK%, HP%, DEF%, SPD (flat), CritRate, CritDmg,
              POT, RES, DualAttackChance
```

**Substat roll ranges** (per roll, gear-rarity-scaled) — kept tight so gear *augments* the
allocation spine rather than eclipsing it:

| Substat | Per-roll range |
|---|---|
| ATK% / HP% / DEF% | +3% … +7% |
| SPD (flat) | +2 … +5 |
| CritRate | +2% … +5% |
| CritDmg | +4% … +8% |
| POT / RES | +2% … +5% |
| DualAttackChance | +2% … +5% |

**Budget guard:** total gear contribution to any single stat is capped at roughly **+40% of
that unit's allocated+base value** for the slice, so gear can't create a stat the allocation
never invested in. Prevents "all gear = one stat" degeneracy and keeps allocation meaningful.

### 5.3 Gear rarity & level
Gear has rarity (C/R/E/L) = number of substats it starts with (1→4) and main-stat ceiling.
Gear **levels via crafting materials** (§9), each level bumping main stat and, at milestones
(+3/+6/+9/+12), rolling a new or upgrading an existing substat — the **gear dopamine beat**
mirroring unit level-ups.

**Gear power ceiling (per §4.0):** a full set of 6 fully-upgraded pieces should contribute
**~1.7×** a unit's base power — *slightly more than levels* (the ~1.5× from §4.0), because gear is
the intended primary chase and the between-runs loop's payoff. Tune main-stat ceilings + the
substat budget cap (§5.2) so 6 maxed pieces land near +70% of base, giving the **combined ~2.5×**
level+gear ceiling. Gear is where the *variance* dopamine lives (rolls); levels are the *steady*
dopamine (guaranteed). Both matter; gear matters slightly more.

---

## 6. Damage & defense math (proven, non-degenerate)

Core damage formula — **DEF as a diminishing divisor**, the single most battle-tested
anti-snowball defense curve in the genre (FFBE/E7/Summoners War lineage):

```
raw      = ATK * skill_multiplier
mitigated = raw * ( K / (K + DEF_effective) )      // K = 1000 (playtested value)
crit      = mitigated * (1 + CritDmg)  if crit roll succeeds
final     = crit * affinity_mod (§7) * variance(0.95..1.05)
```

**K = 1000** — this is the value the prototype shipped with and playtesting called fun. (The
earlier draft said K=300; that was a placeholder written without the prototype in front of it.
At the prototype's real DEF range ~150–260, K=300 gives ~33–46% mitigation while K=1000 gives
~13–21% — a real feel difference, and 1000 is the played, liked value. Per the "keep what
playtested as fun" rule, **K stays 1000.**)

Why `K/(K+DEF)`: each point of DEF gives *less* raw reduction but *more* effective HP —
so DEF never hard-caps damage to 0 (no invincible walls) and never becomes useless (no
"just stack ATK"). With K=1000: DEF 200 ≈ 17% reduction, DEF 500 ≈ 33%, DEF 1000 ≈ 50%.
Smooth, legible, proven.

`skill_multiplier` examples: basic 1.0, skill 1.4–1.8, ult 2.5–3.5.

---

## 7. Affinity Wheel (advantage) — unchanged, renamed as TYPE math

Per LOCKED: 3-cycle (Judgment→Life→Revelation) + mutual-weakness pair (Majesty↔Mystery).
Advantage = **+15% Crit Rate and +15% Potency for that action** (not a flat damage multiplier).
Now framed explicitly as **affinity-type** interaction — this is the "type chart" that units
inherit from their affinity. Names remain Jan placeholders → religion-agnostic rename later.

```
affinity_mod: advantage → +15% CritRate, +15% POT on that action
              disadvantage → -15% CritRate, -15% POT
              neutral → no change
```

---

## 8. Debuff application (Potency vs Resolve) — unchanged

```
apply_chance = skill_base_chance * (1 + POT_caster - RES_target)
// clamped to [0.05, 1.00] — nothing is ever 0% or guaranteed
```
Affinity advantage adds +15% POT into this on-advantage (§7), making the type wheel matter for
control, not just damage.

---

## 9. Crafting MVP

**Goal:** a real but minimal loop — turn dropped materials into equipment, and upgrade equipment.
Not the full Elin crafting depth (deferred). Between runs only.

### 9.1 Materials
3 material tiers drop from enemies (§10): **Shard (common), Core (uncommon), Sigil (rare)**.
Boss (battle 10) guarantees a Sigil.

### 9.2 Two crafting actions (that's the whole MVP)
1. **Forge a piece:** pick a slot type + target rarity → consume a recipe cost in materials →
   receive a piece with a **random main-stat (from that slot's pool) and random substats**.
   The randomness IS the dopamine (gear-pull feel with earned currency, per the non-predatory
   pillar). Costs scale by rarity.
2. **Upgrade a piece:** spend materials to level a piece (§5.3), bumping main stat + rolling
   substats at milestones.

Forge cost sketch (tune):
```
Common piece:    5 Shard
Rare piece:      8 Shard + 2 Core
Epic piece:      6 Core + 2 Sigil
Legendary piece: 4 Sigil + 10 Core
```

### 9.3 Where crafting happens
A **between-runs management screen** (§11). No town building yet — that's the later sandbox
reach. For now it's a menu: *Craft / Upgrade / Assign Gear / Allocate Levels / Respec / Party*.

---

## 10. The dungeon run structure (the tension engine)

### 10.1 Shape
- **5 dungeons**, selectable from a battle menu. Each is **harder than the last** (§10.3).
- Each dungeon = **10 battles**, each **harder than the last within the dungeon** (§10.4),
  battle 10 = **boss**.
- **Attrition:** party HP + cooldowns carry across all 10. No inter-battle heal.
  *(Optional tuning valve: a single "rest" choice at battle 5 that heals X% — hold in reserve
  if playtest says 10-battle attrition is too brutal. Default: no rest, pure attrition.)*
- **Escrow:** each battle's drops → run inventory. **Clear battle 10 → commit to permanent.**
  **Lose any battle → wipe escrow, restart at battle 1.** Brought-in levels/gear persist.

### 10.2 Why this makes "sloppy play loses" true
Attrition + escrow means the optimal-skill-order pressure the owner asked for is *real*:
overspending HP or dumping cooldowns early leaves you hollow at the boss, and losing costs the
whole run's loot. The player must **read enemy profiles (§12), sequence skills, and manage
resources across 10 fights** — exactly the intended skill expression.

### 10.3 Dungeon-level difficulty curve (harder each dungeon)
Enemy stats scale by a **dungeon power multiplier** applied to the baseline statline (§3.1):

| Dungeon | Enemy power mult | Recommended party level | New mechanic introduced |
|---|---|---|---|
| 1 | 1.00× | 1–15   | teaches basics; clean fights |
| 2 | 1.35× | 15–35  | first debuffers (POT matters) |
| 3 | 1.80× | 35–55  | affinity-wheel pressure (type matters) |
| 4 | 2.40× | 55–80  | CR/Momentum manipulation enemies |
| 5 | 3.20× | 80–100 | all mechanics + boss with 2 phases |

*(Recommended levels rescaled for the 100-cap. Note the level bands are the intended "clear it
around here" targets; because power is capped at ~2.5×, the last dungeon's 3.20× enemy mult is
deliberately reachable only with near-max levels **and** strong gear — that's the wall that makes
the grind matter. If playtest shows dungeon 5 is unclearable even fully built, lower its mult, do
NOT raise the power ceiling.)*

Multipliers follow a **~1.32× geometric step** — proven pacing (each dungeon ~a third harder,
matching the ~1.3–1.4× per-tier curve common to the genre). Party power from levels+gear should
track just *under* the curve so players must actually build, not walk through.

### 10.4 Within-dungeon curve (harder each battle)
Inside a dungeon, battle *b* (1–10) applies an intra-scaling on top of the dungeon mult:

```
enemy_stat = base_stat * dungeon_mult * (1 + 0.06 * (b - 1))    // +6%/battle
boss (b=10): additional * 1.25 boss bonus + a phase/enrave mechanic
```

So battle 10 enemies are ~1.79× the battle-1 enemies of the same dungeon, *before* the boss
bonus — a clear ramp that, combined with attrition, forces resource discipline.

### 10.5 Enemy drops
Each enemy has a **drop table**: materials (§9.1) always; equipment on a roll (higher dungeons →
better gear rarity odds). Boss: guaranteed Sigil + guaranteed 1 gear piece at dungeon-appropriate
rarity. All into escrow until the run completes.

---

## 11. Character management MVP (between runs)

A single **management hub** screen, opened between runs. Tabs/actions:
- **Party:** pick the ~4 units for the next run.
- **Allocate Levels:** spend pooled points (§4) per unit — the level-up dopamine beat.
- **Respec:** free wipe/reassign (§4.5) for this build.
- **Gear:** assign/unassign the 6 slots per unit; see resulting stat deltas live.
- **Craft / Upgrade:** the §9 crafting MVP.
- **Inventory:** permanent materials + gear (escrow shown separately, greyed, "commits on run
  clear").

Design rule: **every management action shows its stat delta immediately** (before/after on the
6 stats). This is what makes min-max satisfying and makes stats *mean something* to the player.

---

## 12. In-fight profile viewer (stats gain meaning)

During any battle the player can **tap/click any unit — ally or enemy — to open a profile card**:
- the 6 core stats (current vs base), level, affinity, rarity,
- active buffs/debuffs with turn counters,
- current cooldowns,
- equipped gear summary (allies only; enemies show stats but not their loadout).

**Why it matters:** the owner's ask — "stats have more meaning." Seeing an enemy's DEF 400 vs
your ATK, or that the boss has high RES so your debuffer will whiff, is what converts raw
numbers into *decisions*. This is a read-only overlay; cheap to build; high value.

---

## 13. The core loop (minute-to-minute) — the diagram open since v0.1

```
PICK DUNGEON (5 choices, escalating)
        │
        ▼
   ┌───────────── RUN (10 battles, attrition) ─────────────┐
   │  BATTLE b:                                            │
   │   read profiles (§12) → sequence skills → win/lose    │
   │     win → drops to ESCROW, XP, maybe level-up         │
   │     HP/cooldowns carry to battle b+1  (attrition)     │
   │   lose → ESCROW WIPED → back to battle 1               │
   └──────────────────────────────────────────────────────┘
        │ clear battle 10 (boss)
        ▼
   ESCROW COMMITS → permanent inventory (materials + gear)
        │
        ▼
   MANAGEMENT HUB (§11): allocate levels · craft/upgrade gear ·
                         assign gear · respec · rebuild party
        │
        ▼
   STRONGER → pick a harder dungeon → repeat
```

This is the reward→growth loop PROJECT_CONTROL asked to draw: **win → earn (escrowed) →
commit → apply (levels+gear) → stronger → harder dungeon.**

---

## 14. Balance philosophy (why these numbers are "proven")

- **Hard power ceiling ~2.5× (levels ~1.5× · gear ~1.7×)** — the anti-overtuning spine. Every
  other number is tuned to live under this ceiling. Overtuning is the stated worst-case failure;
  this cap is the guard. Enemy scaling sits just under it so building matters but nothing runs away.
- **Percentage-of-own-base growth** — a level point adds a % of the unit's *own* base stat, so
  growth feels equal on a 200-HP mage and a 1300-HP tank. This is what lets 100 levels + tiny
  per-level power coexist with a felt sense of getting stronger.
- **Milestones every 10 levels** — the dopamine of a 100-level grind comes from 10 drumbeats
  (bigger bump + a non-stat unlock), not from each ordinary level. High-level ordinary gains are
  *supposed* to be small; don't inflate them.
- **K = 1000 (playtested)** — DEF-as-`K/(K+DEF)` divisor; genre-standard anti-snowball; no
  invincibility, no useless DEF. Value carried from the prototype's proven feel, not the draft's
  K=300 placeholder.
- **Geometric ~1.32× dungeon steps + linear +6%/battle** — the pacing pattern JRPG progression
  curves converge on; each step meaningful, none a wall.
- **Quadratic-ish XP (`50·L^1.5`) to level 100** — fast early dopamine, long grind after;
  repeat-farming harder dungeons is what fills the back half without inflating power.
- **Tight gear substat ranges + budget cap** — gear augments the allocation spine instead of
  replacing it, so *player choice* (levels) stays the dominant progression axis and gear is
  the exciting variance layer. This is the deliberate guard against the min-max failure mode
  the owner opted into.
- **SPD soft cap** — the one place a Momentum system reliably breaks; capped, not banned.

**All constants are dials.** The formulas are the spec; the numbers are the first playtest's
starting position.

---

## 15. Build order for this slice (extend the throwaway browser prototype)

1. **Persistence layer** — unit objects that hold level/XP/allocated-stats/gear across battles
   and runs (in-memory + a save blob). *Nothing else lands without this.*
2. **Stat + allocation math** (§3–4) and a **management hub** stub (§11) to spend points.
3. **Equipment + substats** (§5) with live stat deltas.
4. **Run structure** (§10): dungeon select, 10-battle attrition, escrow, commit/wipe.
5. **Enemy scaling + drops** (§10.3–10.5).
6. **Crafting MVP** (§9).
7. **In-fight profile viewer** (§12).
8. **PLAYTEST** against §16 before speccing anything downstream.

Keep it one throwaway browser build. Engine decision stays deferred (PROJECT_CONTROL).

---

## 16. Playtest questions this slice must answer

- Is the **level-up allocation** moment satisfying, or fiddly? (Dopamine check.)
- Does **percentage-of-base growth** feel meaningful on *every* unit (both the low-HP glass cannon
  and the high-HP tank), or does it feel flat on one of them?
- Do the **milestone levels (every 10)** actually land as drumbeats, or do ordinary levels feel so
  small that the whole grind reads as hollow between milestones? (If hollow → milestones may need
  to hit more often, OR ordinary per-level gains need a touch more — but never past the 2.5× cap.)
- Does the **100-level grind** feel like a rewarding time-sink or a slog? (Pacing check — this is
  the one most likely to need XP-curve tuning.)
- Does **attrition across 10 battles** create real "sequence your skills or lose" tension, or
  just feel punishing?
- Does **losing the run's escrow** read as fair stakes or as rage-quit? (If rage-quit → add the
  battle-5 rest valve or a partial-escrow-keep.)
- Do **enemy profiles** actually change player decisions? (Do stats gain meaning?)
- Is **gear** exciting without eclipsing allocation? (Is the budget cap right?)
- Does the **5-dungeon curve** force building, or can players walk through / hit a wall?

---

*End v0.1. Next session after playtest: either tune this loop, or take the first real reach into
the sandbox half (town/farming feeders) now that combat has stakes and growth.*
