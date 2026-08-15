# PROJECT CONTROL — [Working Title: TBD]

> **This is the file we open FIRST at the start of every session.**
> Read "Current State" and "Next Session Starts Here" and we're immediately oriented.

---

## What this project is (the 30-second version)

A **single-player, top-down 2D** game fusing:
- **Elin-style sandbox depth** — town-building, farming, crafting, breeding, scaling dungeons, steady multi-system wealth buildup.
- **Epic Seven / FFBE-style gacha combat** — Momentum turn-based tactical battles with a deep, collectible roster.

**Non-predatory / single-player.** Summon dopamine (rarity, pity, banners) powered by *earned* currency, never a wallet. Collection is completable.

**Theme:** reverent treatment of the sacred, religion-agnostic under the hood. Roster = original units; **affinity = the unit's TYPE**, unit name is independent.

**Design pillar:** every unit stays valuable — rarity buys *flexibility + stats + passive potency*, not *permission to matter*. Generalists (high rarity) vs. irreplaceable specialists (low rarity).

---

## Who's building this & how we work

- **Owner (you):** technical product owner / systems designer. Ships spec-driven `.md` + data files to Claude Code + Fable. **Not writing engine code by hand.** Strength = precise, unambiguous specs.
- **Primary goal:** design a game *you* would replay.
- **Implementation path:** thorough per-system `.md`/data specs → Claude Code / Fable implements.

### The ONE discipline that keeps this alive
> **Spec deeply, but build in playable vertical slices, and PLAYTEST each slice before speccing the next.**
> A game is *feel-defined*: only playtesting reveals fun. Deep spec for the slice we're building now; light sketches downstream until it proves out.

### Session discipline
- Each session has **one named deliverable.**
- Each session **ends by updating this file** (Current State + Next Session Starts Here).

---

## Tech stack
**Production engine deferred** (Godot vs Unity — a late, reversible "weekend choice"). Not committed. **Prototype tool = browser / HTML5 canvas** (throwaway, feel+math validation only). A great browser prototype does NOT validate the engine choice.

**Data-driven is mandatory.** Units, affinities, abilities, effects, items = data files (JSON), not hardcoded. This is now real: `roster.json` + `effects.json` are the canonical data spine.

---

## Deliverables ledger

| # | File | Status | Purpose |
|---|---|---|---|
| 0 | `PROJECT_CONTROL.md` | ✅ this file | Session control + handoff |
| 1 | `Game_Design_Doc.md` | ✅ | Master design doc (why + systems overview) |
| 2 | `combat_slice_spec.md` | ✅ v0.1, playtested | The combat vertical slice (Momentum, proven fun) |
| 3 | `progression_slice_spec.md` | ✅ v0.1 → building | Progression/rewards layer: persistence, levels, gear, dungeons, run structure |
| 4 | `roster.json` / `roster.xlsx` | ✅ v0.3 | **All 100 units as data** — kits reworked onto the glossary; 3 designed passives each |
| 5 | `effects.json` / `effects.xlsx` | ✅ v0.3 | **Canonical effect glossary** — 97 effects (added `dot_amp`); ability-field convention added |
| 6 | `GEARING.md` | ✅ | Gear power envelope: 7 rarity tiers, 4+2 set system, substat grind engine |
| 7 | `power_model_v3.py` | ✅ | Magnitude/duration-aware unit power scorer (K=1000, BUILD_MULT=2.5); xlsx out, JSON clean |
| 8 | `ENCOUNTERS.md` | ✅ | The 14-type encounter MENU (Phase 0 of encounter plan) |
| 9 | `enemy_profiles_scaling.md` | ✅ | Enemy roles (5) + scaling curve + per-archetype sub-boss premium (Story/Grind) |
| 10 | `encounter_sim.py` | ✅ | Run simulator / **regression harness** — full run (3–9 fights → sub-boss), HP+CD attrition |
| 11 | `SIM_RESULTS.md` | ✅ | Sim findings: healing flattens HP-attrition; difficulty = kit design; enrage-boss HP finding |
| 12 | `dungeon_select_mock.jsx` | ✅ | Interactive mockup of the 5-dungeon selection screen (feel reference) |
| … | (economy, bridge, town, summon) | ⬜ later | One spec at a time, in build order |

---

## Design decisions LOCKED (don't relitigate without reason)

**Core / meta**
- Single-player; non-predatory; completable collection.
- Combat gets built & playtested FIRST; other systems spec later.
- Feel-first, fidelity-later: build with placeholder art + juice; real art after fun is proven.

**Combat engine**
- **Momentum** = the per-unit turn-order gauge (fills by SPD, decides who acts). (CR system, renamed.)
- **Ults gated by per-unit cooldowns**, not a resource meter.
- **Potency vs. Resolve** = debuff-application contest: `chance = skill_base × (1 + POT − RES)`, clamped [0.05, 1.00].
- **6-stat model:** HP / ATK / DEF / SPD / POT / RES (+ derived CritRate/CritDmg). Same model for units & enemies.
- **Damage:** `mitigated = raw × K/(K+DEF)`, **K = 1000** (playtested value).
- **Affinity wheel** = 5 affinities as a TYPE chart (see Roster below). Advantage = **+15% CritRate & +15% POT** on that action (not a flat damage multiplier).

**Progression (progression_slice_spec)**
- Combat units = a **separate summoned roster**; overworld = single character (fork RETIRED).
- **Run-based dungeons:** 5 dungeons × 10 battles (10th = boss). Rewards → **escrow**; clear boss → commit; **lose any battle → escrow wiped, restart**. Brought-in levels/gear persist.
- **Attrition:** HP + cooldowns carry across all 10 battles (no free heal).
- **Full min-max:** per-level assignable points + respec + gear substats.
- **Level cap 100.** Levels give ~1.5× base; gear ~1.7×; **combined ceiling ~2.5×** (anti-overtuning spine — never exceed it; if content is too hard, lower enemy scaling, don't raise the ceiling).
- **Percentage-of-own-base growth** (a point adds a % of the unit's own base stat) + **milestones every 10 levels** carry the felt dopamine.
- **6 equipment slots** (Weapon/Armor/Emblem fixed mains; Boots/Charm/Relic chosen mains) + substats incl. **DualAttackChance**.

**Roster (roster.json v0.2)**
- **Affinity = TYPE, not unit.** Unit name is independent; many units share one affinity (e.g. many "Judgment" units).
- **5 affinities:** Judgment(Red), Life(Green), Revelation(Blue), Majesty(Gold), Mystery(Dark).
- **Wheel:** Red→Green→Blue→Red (triangle). **Gold↔Dark** mutual advantage. **Gold & Dark are off-wheel** — never penalized vs RGB, only interact with each other. (Balance watch: keep them SIDEGRADES, not upgrades, or the wheel collapses — constraint content matters.)
- **Color identities:** Red = aggression / Green = outlast-sustain / Blue = control-tempo-precision / Gold = command-permanence / Dark = sacrifice-risk. Wheel bleeds into kits (Red punishes healing, Blue answers aggression, etc.).
- **100 units:** Red 25 / Green 25 / Blue 25 / Gold 12 / Dark 13.
- **3 rarities:** Common(3★) / Epic(4★) / Legendary(5★). Multipliers 1.00 / 1.25 / 1.50; points/level 3 / 4 / 5.
- **Distribution:** 29 Legendary / 35 Epic / 36 Common (per-affinity Legendaries 7/7/7/4/4).
- **Every unit has 3 passives.** Rarity sets passive **potency**, not count (Common = modest/flat, Epic = conditional/mechanical, Legendary = potent/unique + hand-authored signature). Unlock mechanic **PARKED** — all unlocked for now; `unlock`/`unlocked` fields present for later gating.

**Effect system (effects.json v0.3)**
- **97 effects** (added `dot_amp` in the v0.3 roster audit). **Ability-field convention (v0.3):** conditional damage / hit-shape / def-pen / triggers live on the ability (`bonus_vs`, `hits`, `ignore_def`, `triggers`), NOT in `effects[]`. `effects[]` = valid glossary status ids only.
- **Categories:** buff / debuff / dot / control / instant / special.
- **Stacking:** only DoTs (Poison/Bleed/Burn/Curse) + a few flagged stack; everything else **refresh-if-stronger**.
- **Removal:** buffs die to STRIP, debuffs die to CLEANSE; any effect can be **undispellable/uncleansable**.
- **Team-wide is a MODIFIER, not a separate effect** — the ability sets target/duration; team versions get shorter duration or rarer-unit gating. Never author `team_x` entries.
- **Control ladder (each blocks ONE action type):** Disarm=no basics · Silence=no skills · Sealed=no ults. **Stun**=full lockout + still takes damage. **Freeze**=lose turn but immune to *direct* damage (DoTs still tick), 1 turn then breaks. **Sleep**=lose turns + self-heal 20%/turn, breaks on damage. **Bind dropped** (absorbed into Freeze).
- **Brand kept, Exposed cut** (were redundant). Brand = universal +dmg-taken; Marked = synergy-tag amplify.
- **Enrage family (Berserk/Frenzy/Overload):** UNCLEANSABLE, **trigger-bound** (hp_threshold/phase/turn_count/on_effect/manual), enemy-focused, rarely a player buff. Pairs with **Last Line** (`prevent_death_team`) for the signature un-killable-but-deadly survival window.

**Encounters & difficulty model (LOCKED this session — the efficiency spine)**
- **Enemies are FROZEN content, authored ONCE.** Enemy statlines are generated at *authoring time* from the formula `player_tier_scale × level × tier-expected-gear`, then baked as static data and never recomputed. **Enemies do NOT scale off the acting player's live loadout** (owner rejected live-scaling: a Lv100 boss must not get harder because you found better gear — its difficulty is absolute; your gear is what changes your ability to clear it).
- **The player-power ENVELOPE per tier is the master reference.** For each of the 10 tiers: the min / expected / max effective power a tier-appropriate team can field. Enemies are built against the *expected* band. **This table is the foundational artifact — enemies, gear budgets, and content power-costs all hang off it. It must exist before enemies are authored.** (Not yet built — first deliverable of the wide-net phase.)
- **The sim is a REGRESSION CHECK, not a balancing tool.** You don't sim to *find* balance; you sim to *confirm a change didn't break it*. When a new power-injecting mechanic (crafting, gear tier, unlock, side content) lands, the only question is: *do tier-appropriate players stay inside their tier's power band?* In-band → zero enemy work. Out-of-band → fix the **new mechanic's budget**, not the frozen bosses. This makes power-creep visible and cheap to fix at the source.
- **Every power source must express itself as a contribution to effective power** (a multiplier/addend into the single power currency), so it can be budgeted against the band. No system injects power that isn't costed.
- **Difficulty comes from enemy KIT DESIGN, not stat scaling** (sim finding). Raw enemy HP/ATK scaling only keeps enemies on the player's scale; it does NOT create difficulty, because dedicated player healing flattens HP-attrition. Real difficulty levers a healer can't answer: **burst > heal-rate, heal-denial (anti-heal debuffs), enrage/time-pressure, control on the support.**
- **No artificial turn-cap loss** (owner call). A scaling boss with an **enrage** naturally overwhelms low-DPS / mono-tank teams — but ONLY if it *outlives* their damage. Sim finding: **enrage/Sprint sub-bosses need ~×3.0–3.5 HP premium + a real stacking enrage (~35%+ atk per ≤2-turn cast)**; signature-threat bosses (Bulwark/Plague/lock) keep ~×1.6 HP (their threat is the mechanic). Per-archetype HP premium, not flat.

**Story/Grind dungeon (the core-of-the-core loop — specced this session)**
- **RNG-lite selection:** player is always shown **5 dungeons spanning below → at → above their level** (offsets −10/−5/0/+8/+15). Difficulty is a visible *player choice*, not a settings toggle.
- **Run shape:** 3–9 randomized normal fights → 1 RNG'd sub-boss. Sub-boss archetype rolls from the template pool; carries **≥2 significant abilities** (not a stat-stick).
- **Enemy roles (5, anchored to player role medians):** Bruiser / Warden / Mender / Hexer / Zealot. The *composition* is the puzzle (a Mender behind Wardens = DPS check, etc.).
- **Variety over guarantee:** normal fights aren't forced to include a comp-puzzle; the sub-boss carries the run's guaranteed tactical moment.
- **POT/RES held flat** at player-median for this encounter type (oppressive-debuff scaling deferred to a future encounter type).

## Design decisions OPEN (resolve later)
- Passive **unlock mechanic** (milestone / capstone / investment) — parked.
- Permadeath reconciliation (likely: overworld body can fall, roster persists).
- Economy currencies & the multi-system wealth spine.
- Rewards/ranking wrapper for lite-PvP without FOMO.
- **Step 2 allocation math** (`POINT_PCT` values) — Claude Code was mid-build, awaiting a sanity-check on the derived numbers. Still open on the build side.

---

## CURRENT STATE  *(updated — Story/Grind + sim + strategy-reframe session)*

**Where we are:** the **Story/Grind randomized dungeon** (the core-of-the-core loop) is designed, the **enemy layer** is specced, and a **run-simulation harness** is built and working. We also reached a **strategic reframe** on how to balance efficiently that reshapes the roadmap. The project is now ready for **one feel-focused playtest**, then a wide-net content-definition phase.

**Done this session:**
- **`dungeon_select_mock.jsx`** — interactive mockup of the dungeon-select screen (5 dungeons below→at→above player level). Grounded in the real level+gear math. Proves the "difficulty as a player choice" feel.
- **`enemy_profiles_scaling.md`** — 5 enemy roles anchored to player role-medians; the enemy scaling curve; per-archetype sub-boss HP premium. Composition is the tactical puzzle.
- **`encounter_sim.py` + `SIM_RESULTS.md`** — a full-run simulator (3–9 fights → sub-boss, HP+cooldown attrition). Built as the **regression harness**, not a balancing tool.
- **Key sim findings (these reshaped the design):**
  1. **Dedicated healing flattens HP-attrition** → raw HP/ATK scaling is a *weak* difficulty lever. **Difficulty must come from enemy KIT design** (burst, heal-denial, enrage, control), not stat scaling.
  2. **Owner's "enrage naturally breaks mono-tank teams" model is CONFIRMED** — but only when the boss *outlives* the team's damage. So enrage/Sprint sub-bosses need ~×3.0–3.5 HP + a real stacking enrage. No artificial turn-cap needed.
- **STRATEGIC REFRAME (the important part — now locked, see Locked Decisions):**
  - Balance is impossible to hand-tune across many power-injecting mechanics without infinite tickets. The fix is **systems that self-balance by construction**, with the sim demoted to a **regression check**.
  - **Enemies are FROZEN content**, authored ONCE against a *tier power band* — they do **not** live-scale off the player's gear (owner correction: a Lv100 boss's difficulty is absolute; your gear changes your ability to clear it, not the wall's height).
  - The **player-power envelope per tier** is the new foundational artifact everything hangs off. It doesn't exist yet — it's the first deliverable of the wide-net phase.

<details><summary>Prior CURRENT STATE (encounter-design session — superseded, kept for history)</summary>

Encounter design opened: `ENCOUNTERS.md` (14-type menu, Phase 0) and `encounter_BOSS_archetype_flip.md` ("The Warden of Ash", a worked 2-phase-boss example, flagged premature — reference only, do not build more bespoke bosses). Two-axis principle: difficulty tier (vertical) × archetype-question (horizontal). Before that: the v0.3 roster ability audit (all 100 kits on the glossary, 3 designed passives each, off-wheel Legendary premium). Build side: persistence done; Step 2 `POINT_PCT` math paused.

</details>

## THE PLAN (locked this session — the efficiency-first roadmap)

1. **Playtest NOW — for FEEL, not balance.** Wire the Story/Grind loop into an HTML prototype and play it. Answer only: *is the core loop fun? is the tempo right? do the teambuilding decisions feel good?* Minor tuning tweaks during the playtest are fine but **disposable** — do not treat them as real balance (the whole point is we balance properly later, against the defined feature set). If the loop's fun, the rest of the plan is justified; if not, better to know before outlining content.
2. **Cast the WIDE NET — time-boxed.** Enumerate all intended features/content (crafting, gearing depth, unlocks, side content, encounter types, economy…). Capture it NOT as a flat wishlist but as a **dependency graph with a power-budget column** — which systems feed which, and how much effective power each injects. Time-box this so it doesn't become its own infinite-scope trap.
3. **Refine the net into deliverables** in **dependency order** (foundations before dependents). The **player-power envelope per tier** is deliverable #1 of this phase — everything else power-costs against it.
4. **Implement**, letting the **sim be the regression check** after each layer lands. One `--sweep` confirms tier-appropriate players stayed in-band. In-band → no enemy work. Out-of-band → fix the new mechanic's budget, never the frozen bosses.

> The through-line: **don't balance at the end — build so balance is a property the systems maintain, and the sim just verifies it.**

## NEXT SESSION STARTS HERE

**→ See `HANDOFF_playtest_build.md`** (in `/mnt/user-data/outputs/`) — the next session implements the playtest. It introduces the couple of new things needed for the playtest, then generates the Claude Code build files for the HTML prototype.

**First, drop this session's files into the project** (project copies are read-only): `PROJECT_CONTROL.md`, `enemy_profiles_scaling.md`, `encounter_sim.py`, `SIM_RESULTS.md`, `dungeon_select_mock.jsx`, and the `HANDOFF_playtest_build.md` + build files.

**The one job of the next 1–2 sessions:** get a playable **front-end + Story/Grind loop** in HTML and *play it for feel*. Full flow: **summon 30 → pick a team of 4 → main-menu hub → pick 1 of 5 dungeons → play a 3–9 fight attrition run → RNG'd sub-boss → back to menu.** Nothing downstream (the wide net, the power-envelope table, content authoring) happens until the loop proves fun.

**Watch for:** keep playtest tuning DISPOSABLE (don't over-invest in balance that'll be redone); ~2.5× power ceiling still holds; keep Gold/Dark sidegrades.

**Still deferred (unchanged):** production engine; passive unlock mechanic; Step 2 `POINT_PCT` math; the Doom→bomb + slot-1-CD-0 + unit-budget roster reworks (banked below); the sandbox half.

---

## OWNER FEEDBACK on the v0.3 roster audit (banked — action items, NOT yet applied to the data)

> These are corrections to what the v0.3 pass produced. They are recorded here so they survive a topic switch. **The roster.json / effects.json shipped this session do NOT yet reflect these** — apply them in a follow-up pass.

**BIG PICTURE — the real gap this audit exposed (top priority, owner has a plan):**
The v0.3 kits were authored by *design judgment*, not by a *mathematical budget*. There is currently no formula governing how much damage / utility / control / value a unit is "allowed" given its rarity, role, and affinity. Result: potency is eyeballed and inconsistent unit-to-unit. **Before the next kit revision we need a points/budget system** — a per-unit value budget (by rarity + role) that abilities and passives spend against, so damage, utility, and control are all costed and comparable. Owner has an idea for this and will drive it. **Do not do another kit pass until this math layer is defined** — otherwise we re-bake the same un-costed guesses.

**Specific corrections to apply in the follow-up pass:**

1. **Remove Doom (death timers) from the game.** Owner is not OK with unavoidable-death-on-a-timer mechanics. **Rework Doom into a "bomb"-style effect:** a countdown that, on expiry, applies a *burst of debuffs* (analogous to how a damage-bomb dumps a big hit when it ticks down) — NOT a guaranteed kill. This keeps the "inevitable payoff after a timer" tension without the death-timer feel.
   - Retire/replace the `doom` glossary effect accordingly (likely a new `debuff_bomb` / `delayed_debuff_burst` effect, or fold into the existing `delayed_charge` family).
   - **Units to rework** (they were built around `doom`): **Nyssa (drk_004, the Doomspeaker)** — her whole kit + signature ("Doom timers unreducible, Doom kills spread") is doom-centric; and **Umbra (drk_008, the Veilwalker)** — ult `Long Dark` uses field `doom` + `prevent_death_team`. Both need new payoff mechanics under the bomb model. Re-check any other `doom` references before shipping.

2. **Every unit's FIRST ability must have 0 cooldown.** The opener/basic (ability slot 1) is always CD 0 across all 100 units. Normalize all slot-1 abilities to `cooldown: 0`; if that makes a currently-strong slot-1 effect too spammable, move that effect to slot 2 and give slot 1 a cleaner basic. (Ties into the budget system: a 0-CD ability is costed as *repeatable* and should carry proportionally less per-use value.)

**Scope counts (from the shipped v0.3, for the follow-up pass):**
- **Doom references: 2 units** — Nyssa (drk_004: abilities `Mark of Doom` + `Final Hour`, signature, `Doomspeaker` passive — fully doom-built) and Umbra (drk_008: ult `Long Dark`, signature, `Veilwalker` passive). Plus the `doom` glossary entry itself.
- **Slot-1 CD>0: 32 units** need their first ability set to CD 0. Notable pattern: nearly all **buff/tank/support** units carry a cd2–cd3 slot-1 (e.g. all Gold's slot-1 buffs are cd2–3; most Blue/Green enablers too), because those effects (team buffs, taunts, shields, permanence) are strong to spam. These are exactly the ones where the effect likely moves to slot 2 and slot 1 becomes a clean basic attack/heal. Full list lives in the session's scope check; regenerate with a one-line script over `abilities[0].cooldown != 0`.

---

## POWER VALUATION MODEL v0.1 (banked — `power_model.py` + `power_scores.json`)

> The "mathematical controls" the audit was missing. Scores every unit into ONE number by costing stats + abilities + passives + affinity, all RELATIVE to a baseline unit (~100 = average Common). Numbers are dials; the **structure** is the deliverable. Re-run after any kit change to see its effect on every unit's value.

**Architecture (four costed buckets → total):**
1. **Stat power** — each stat vs a baseline statline. Non-linear where it should be: **SPD super-linear** (`(spd/100)^1.4` — more turns compounds), **DEF via effective-HP** on the K=1000 curve, HP/ATK linear, POT/RES light additive.
2. **Ability power** — `(damage + Σ effect_power) × targeting × duration ÷ cooldown_amortization`. Damage scales off `mult × hits`, boosted by `ignore_def`/`bonus_vs`. **Every effect has a granular power rating** (`EFFECT_POWER` table): control ladder ranked **Stun 14 > Sleep 11 > Freeze 9 > Silence 8 > Disarm 7**; `def_break_major 11 > def_break 7`; `atk_up_major 10 > atk_up 6`; `aura_all_stats 14`; specials (Doom/Last Line/execute/extra_action) high. Targeting: team/AoE ≈ `4^0.83 ≈ ×3.2` (slight discount, not full ×4). Duration: longer buffs worth more (sublinear). Cooldown: **0-CD = full value (repeatable); higher CD amortized** (ults amortize gentler since they're meant to be high-CD payoffs).
3. **Passive power** — stat passives costed by their %; enhance/unlock passives by potency tier.
4. **Affinity modifier** — **Gold/Dark ×1.06** (their wheel bonus is unconditional/never-penalized vs RGB's situational advantage — the off-wheel premium is now PRICED, not asserted).

**Validation (the model earns trust):** rarity ladders cleanly **Common 91 → Epic 111 → Legendary 143** without being tuned toward it. Off-wheel premium reads correctly: **Gold Legendaries 176, Dark 148 vs RGB Legendaries 131–140** — the medium(Gold)/slight(Dark) bump the owner asked for, now measured.

**KEY FINDING (what the model caught in the v0.1/v0.3 kits):** a **systematic AoE overvaluation**. Nearly every `aoe_dmg` unit scores above its rarity band (AoE Legendaries mean **168.6** vs solo-damage Legendaries **120.5**). Cause: the AoE targeting multiplier (~×3.2) is applied to the *whole* ability incl. its damage multiplier, so AoE nukers get paid ~3× for damage a single-target carry gets paid ×1 for. **Fix (a dial, not a rebuild):** split targeting so AoE *effects* keep ~×3.2 but AoE *damage* scales gentler (~×1.8, a shared damage pool doesn't quadruple threat). Re-tune + re-score in the balance pass. This is exactly the eyeballing inconsistency the owner predicted — the model made it visible and measurable.

**How this plugs into the budget system:** once weights are settled, read a **value ceiling per (rarity × role)** off the score distribution → that becomes the budget a unit's abilities+passives may spend. Then the flow inverts: instead of authoring kits and hoping they're balanced, we **allocate a budget and spend it** on costed effects. That's the "algebraically account for multipliers × effect ratings × cooldowns" system the owner asked for.

**Deliverables:** `power_model.py` (the scorer, runs on any roster.json), `power_scores.json` (current 100-unit scores), and a **PowerScores** sheet added to `roster.xlsx` (sortable, per-unit stat/ability/passive/total breakdown).

**Next on this thread:** owner has a budget idea to layer on top. (Model + Doom + 0-CD + AoE + Dark all APPLIED in the v0.4 pass below — this section is the original v0.1 note, kept for history.)

---

## v0.4 BALANCE PASS (DONE — applied to the data this session; scorer is now `power_model_v2.py` v0.3)

Acted on the banked feedback + the valuation model. `roster.json` (v0.4) and `effects.json` (v0.4) now reflect all of it; `roster.xlsx` shows powerscores at every level.

**1. Powerscores made VISIBLE (xlsx only — json stays clean for the eventual Claude Code handoff).** Five sheets: **Units** (PS_stat / PS_abilities / PS_passives / aff_mult / PS_TOTAL), **Abilities** (PS_damage + per-effect PS + PS_ability, plus a `durations` column so effect durations read on the tab), **Passives** (PS_passive each), **Effects** (PS_rating per glossary effect), **PowerScores** (sortable summary). Scores flow effect → ability → passive → summed unit total.

**2. Doom REMOVED (no instant deaths).** `doom` retired; replaced by **`debuff_bomb`** — a visible countdown that on expiry **detonates a debuff payload, never a guaranteed kill** (cleansing before detonation defuses it). Two doom units rebuilt:
- **Nyssa → "the Hexbinder"** (drk_004): plants Hex Bombs (0-CD), compounds them, detonates the field early on her ult. Payload = def_break + atk_down + res_down; signature makes bombs tick faster + spread half their payload.
- **Umbra → "the Veilwalker"** (drk_008): plants a Shadow Bomb (control payload: spd_down + accuracy_down + silence), hides the team, and while stealthed makes enemy bombs tick twice as fast. Kept the un-killable-window ult (stealth + prevent_death_team) minus the old field-doom.

**3. Cooldowns reworked across the whole roster.** Monotone 0/3/5 gone. **Slot 1 = 0 CD on all 100 units.** Slots 2 + ults spread across **0–7**, tuned so cooldown is the primary lever turning raw effect power into *fielded* value — cheap repeatable utility stays low-CD (the "amazing low-CD team debuff" pattern), big swings cost more, ults 4–7 by payoff. Distribution: 100×cd0, 55×cd2, 27×cd3, 47×cd4, 36×cd5, 31×cd6, 4×cd7.

**4. AoE vs single-target damage reweighted (relative-to-content).** Single-target and AoE *damage* now score ~equal per point (AoE only ×1.1) — a single-target nuke concentrates value in boss/low-count fights, AoE distributes it across swarms; they net out. AoE premium (~×3.2) applies to **effects**, and even that **diminishes when spammable** (0-CD team effect ≈ ×2.3) plus **stacked effects on one ability diminish** (2nd 70%, 3rd 49%…). Fixed the v0.1 AoE-overvaluation.

**5. Dark raised to ~tie with Gold.** Dark Legendaries **≈154 vs Gold ≈156, RGB ≈128** — ~94% of the way from RGB to Gold. Via a higher Dark affinity mult (×1.055) + raw-stat/passive bumps on the 4 Dark Legendaries. Gold flagship (Solomon) reeled in from a 207 spike.

**Distribution now:** Common 86 (71–115) → Epic 104 (87–138) → Legendary 135 (109–167). Clean ladder.

**Deliberately left strong (design > statistic):** **Grimm**, **Lysa** (Common AoE-utility specialists — every ability a near-0-CD team debuff/control) and **Rurik** (all-damage Epic bruiser) read ~2z high. The model rates efficient repeatable AoE utility highly *by design* — the low-CD-team-debuff value + Common niche-key pillar. Nerfing them to hit a number would flatten good design. Re-validate once enemy fights exist.

**Open for the budget system:** validate against real enemy encounters (none designed yet — some "outliers" may prove correct); set per-(rarity×role) budget ceilings off this distribution; then invert kit-building to *spend a budget on costed effects*.

---

## v0.5 MODEL OVERHAUL (DONE — magnitude-aware, fight-duration-aware, dual-column)

Addressed four owner critiques of the v0.4 model. Scorer is now `power_model_v3.py`; data is roster.json v0.5 / effects.json v0.5.

**1. Effects now carry REAL MAGNITUDES (the core fix).** Every effect on an ability is an object `{id, mag, dur, chance, stacks}` instead of a bare token. Magnitude is TYPED: PERCENT_STAT (mag=% stat delta), PERCENT_HP (% max HP), DOT (% target HP/tick), MOMENTUM (% gauge), CONTROL (dur+chance), SPECIAL (bespoke, e.g. execute mag=threshold%). Value now DERIVES from the number, not a flat rating. **`atk_up_major`/`def_break_major`/`regen_major` folded into base id + high mag** (glossary 97→94). Magnitudes resolve at a **build-state stub (~1.8× = level-55+mid-gear)** — flagged as a stub until progression/gear math lands (the honest downstream layer the owner asked about).

**2. Fight-duration weighting — DUAL SCORES, no blend.** Every unit scored twice: **PS_Skirmish (~4 turns)** and **PS_Boss (~20 turns)**, tunable. Mechanism: an ability fires ~`fight_len/(cd+1)` times (saturating), so low-CD sustain/DoT/control/momentum SCALE with fight length while burst front-loads. The **gap between the two columns is the teambuilding signal** — e.g. a DoT specialist (Vespera) gains ~+120 Skirmish→Boss while a burst nuke (Talia) gains ~+25. This fixes the "regen felt overvalued / SPD-down undervalued" critique: per-turn value is now length-dependent.

**3. Passive scores rebuilt (was a BUG).** Old scorer regex-counted % signs in the prose, so "20% DEF while >50% HP" outscored "control_immunity each turn" (the Alcuin inversion). Now every passive carries a structured `ps_tag` ({kind: effect|stat|mechanic, ...}) and is scored off the GRANTED EFFECT using the same vocab as abilities. Alcuin now sorts correctly (control_immunity 14.8 > DR 6.7 > conditional-DEF 3.9); **roster-wide scan confirms 0 remaining inversions.**

**4. Cooldowns: cap 7 + interactive reduction.** Hard cap at 7 (enforced). Added the owner's "S1 accelerates ult" tactic to 5 fitting high-SPD/helper units (Marek, Aurelia, Rowan, Vane/Bloodpact, Cassian): each basic use cuts their ult's CD by 1 via a `cooldown_reduction {on: skill1_used}` trigger — rewards SPD/momentum team-building.

**Resulting bands (dual):** Skirmish — C 68 / E 76 / L 95. Boss — C 116 / E 123 / L 172. Clean ladder in both; Boss numbers run higher by design (attrition favors sustained kits).

**xlsx now shows:** Units (PS_stat, PS_Skirmish, PS_Boss, gap), Abilities (effects with mag/dur, triggers, dual PS), Passives (structured type/basis/conditional + dual PS), Effects (magnitude_type + ref_value), PowerScores (sortable dual + gap).

**Known stubs / still open:** the 1.8× build-state is a placeholder until level/gear math exists; fight anchors (4/20) are provisional (owner to set exact); no enemy encounters yet to validate against — some high scorers (Vespera DoT, the AoE-utility Commons) may prove correct once fights exist. Next: the budget-ceiling layer on top of these dual scores.

---

## v0.6 — universal S1 damage rule (DONE)

**Owner rule: every unit's S1 must deal damage**, even if it also heals/buffs/debuffs (a healer's attack can heal too). 45 units had pure-utility openers (mostly healers/buffers/tanks targeting allies/self). All reworked into damage attacks that RETAIN their utility as riders — the "smite that heals / strike that buffs" pattern (e.g. Thornlash: a life-siphon strike that damages an enemy and heals the lowest ally; Radiant Strike: hits an enemy, heals the whole team). Ally-side rider effects on an enemy-targeted attack are tagged `applies_to: 'ally_side'` so damage resolves on the enemy while heal/buff/shield resolve on allies. S1 mults kept modest (0.9–1.1, openers are cheap) and CD stays 0. Bands essentially unchanged (healers/buffers gained a little S1 value, as intended). Verified: 0 units have a non-damage S1.

---

## GEARING ENVELOPE defined (DONE — see `GEARING.md`)

Decided the gear system's power envelope + shape so encounters can be tuned against real numbers. **E7/FFBE-native** (six pieces, sets by count-threshold not slot-matching, %-main-stats with static ranges per rarity×level, ~4 heavily-RNG substats as the grind engine). **D2 contributes texture only** — rarity-ladder feel + set-collection satisfaction — NOT its literal slot structure (owner corrected an early over-import of D2 here).

Key decisions:
- **Power envelope: ~2.5× mid-game, up to ~3× endgame** (Large / E7-style — gear is a major power source). **Model stub killed:** `power_model_v3.py` `BUILD_MULT` moved 1.8 → **2.5**; scores now reflect a geared unit. New bands: Skirmish C70/E78/L97, Boss C118/E125/L171.
- **Sets by count:** 4-piece = build identity (Speed/Attack/Crit/etc.), 2-piece = filler; builds read as "4-X + 2-Y". No slot-locking.
- **Main stats:** % stats, static ranges per rarity×level, slot-gated main-stat pools = archetype choice.
- **Substats:** ~4/piece, E7 roll-to-upgrade, heavily RNG, wide axis variety = the grind.
- **Effect-set hook (my recommendation, reversible):** most sets stat-only for legibility; a handful of rarest sets grant real effects (Ember→Burn/dot_amp, Piercer→ignore_def, Executioner→execute, Tempo→momentum, Vampiric→lifesteal, Detonator→detonate_dot) — the aspirational chase that ties gear into the "chess" layer. Owner had no preference; easy to drop to stat-only.
- **Non-predatory:** earned by play, no real-money gear/loot-boxes.

**This unblocks encounter design** — the connected next step. Gear envelope (done) → design a few encounters (4-turn swarm, 20-turn boss) tuned to naked×2.5 → run sample teams to sanity-check the model AND the gear assumption at once. Open gear details (slot names, full set list, substat roll math, rarity tiers, drop sources) are non-blocking and listed in GEARING.md §7.

**Gearing expanded (v2 of GEARING.md):** three additions per owner —
- **7 rarity tiers as gated power spikes** (Cracked→Common→Fine→Rare→Epic→Legendary→Mythic). Tier obtainable is capped by content level — legendary/mythic gear is impossible early; each tier is a felt spike. Tiers distribute *within* the 2.5–3× envelope (early tiers ~1.3–1.5×, top tiers deliver the bulk). The core hours-sink.
- **Unique gear = unit-earned, TRADEABLE** (FFBE Trust-Master-style). Unlock by mastering a specific unit (playtime + creative unit-flavored conditions), then equip on ANY unit. Creates a farm-units-to-graduate-uniques meta-layer. Balancing rule: uniques are best-in-slot per slot but DON'T complete a set, so running them trades set-bonus identity for raw power (can't invalidate set gear).
- **Full set list written** (GEARING.md §8): 11 stat sets (Swift/Fury/Bloodlust/Savage/Vigor/Bastion/Malice/Warding/Focus/Mending/Leech) in 2pc+4pc; 8 rare effect-sets (Ember/Piercer/Executioner/Tempo/Vampiric/Detonator/Warden/Hexward) gated to top 2–3 tiers, 4pc-only, hooking real effects.json ids. Builds read "4-identity + 2-filler".
