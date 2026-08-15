# BUILD SPEC — Story/Grind Playtest (HTML) — for Claude Code

> **Goal:** a throwaway browser build that makes the Story/Grind loop **playable for feel**.
> Extend the existing combat prototype; add a dungeon-select screen and a run-manager wrapper.
> Read `HANDOFF_playtest_build.md` for the *why* and scope guardrails. This file is the *how*.
>
> **Source of truth for all numbers:** `encounter_sim.py` — mirror its formulas exactly so the
> playable build matches what was simulated. Where this spec and the sim disagree, the sim wins.

---

## 0. Stack & structure
- Plain **HTML5 + canvas/DOM + vanilla JS** (or the prototype's existing setup). No framework required; no build step. Throwaway.
- Load `roster.json` and `effects.json` as data (fetch or inline).
- Keep it **one playable page**. Screens are states, not routes:
  `SUMMON → TEAM_MGMT → MAIN_MENU → DUNGEON_SELECT → RUN → FIGHT → RUN → … → RESULT → MAIN_MENU`.
  From `MAIN_MENU` the two buttons are `TEAM_MGMT` and `DUNGEON_SELECT`.
- All state in-memory; no persistence.

---

## 1. Reuse: the combat engine
The existing `prototypes/combat-slice/` engine resolves ONE fight (Momentum order, cooldown-gated
abilities, `mitigated = raw × K/(K+DEF)` with **K=1000**, affinity wheel = +15% CritRate & +15%
POT on advantaged actions, debuff apply via `chance = skill_base × (1 + POT − RES)` clamped
[0.05,1.00]). **Do not rewrite it.** Wrap it. It must expose/accept:
- `startFight(playerTeam, enemyTeam)` → runs to WIN/LOSS, returns result + surviving unit HP/CD state.
- Player units carry **persistent HP + cooldown state** in across fights (the Run Manager owns this).

---

## 2. Power curves (copy verbatim from encounter_sim.py)
```
lvl_mult(L)     = 1.0 + 0.5 * ((L - 1) / 99)          # 1.0 @L1 -> 1.5 @L100
player_gear(D)  = min(0.45 + ((D-1)/100)*0.5, 0.95)   # (mock/select only; playtest units use base)
enemy_gear(D)   = clamp((D-1)/100 * 0.9, 0, 0.9)       # 0 @L1 -> 0.9 @L100
gear_mult(f)    = 1.0 + 0.7 * f
```
- **Player units in the playtest:** scale base stats by `lvl_mult(playerLevel)` only (NO gear layer — gear is out of scope). HP/ATK/DEF × lvl_mult; SPD × lvl_mult.
- **Enemy stat @ dungeon level D:** `anchor × lvl_mult(D) × gear_mult(enemy_gear(D))`.

---

## 3. Enemy roles (from enemy_profiles_scaling.md)
Anchor statlines (level-1, pre-scale). Each enemy = anchor × the enemy scaling above.

| Role | HP | ATK | DEF | SPD | Behavior |
|---|---|---|---|---|---|
| bruiser | 820 | 225 | 160 | 118 | Basic attacker; spreads aggro. |
| warden | 1300 | 160 | 250 | 93 | HP wall; draws aggro (high threat). |
| mender | 900 | 172 | 185 | 109 | **Heals most-hurt ally** ~28% max HP on CD2. Force-multiplier. |
| hexer | 810 | 200 | 165 | 118 | Applies def_break / slow. |
| zealot | 800 | 210 | 170 | 108 | AoE attacker (hits whole team). |

**Enemy AI (mirror the sim):**
- Enemies **spread aggro**, do NOT hard focus-fire one unit. Weight targets: tanks ~2.5× threat, mild lean toward already-hurt targets. (This prevents the artificial one-round squishy-delete the sim caught.)
- Menders heal the most-hurt living ally when one is below ~75% HP.
- Players (if AI-assisted) or the human choose abilities; enemies pick highest-impact ready ability.

---

## 4. Sub-boss (per-archetype — from enemy_profiles_scaling.md §4)
Sub-boss = a role anchor + premium + **≥2 significant abilities** (never a stat-stick).

- **Enrage / Sprint boss:** **HP ×3.0–3.5**, ATK/DEF ×1.25. Abilities: a **stacking `atk_up` enrage** (~35% per cast, CD ≤2 — it must actually raise the boss's ATK and stack) + an AoE that benefits from the enrage. This is the boss that punishes low-DPS teams by outliving their damage.
- **Signature-threat bosses (Bulwark / Plague):** **HP ×1.6**, ATK/DEF ×1.25. Threat is the mechanic, not HP:
  - *Bulwark:* self `def_up` + shield (strippable), + an AoE. Answer = strip + survive.
  - *Plague:* team `def_break` + DoT, + a `debuff_bomb` (5-turn countdown → debuff payload, NOT a kill). Answer = cleanse + burst.
- Implement **at least the enrage boss + one signature boss** so sub-bosses feel distinct. A third is a bonus.
- **CRITICAL:** self-buffs (`atk_up`/`def_up`) must **actually modify the boss's stats and stack** — the sim originally failed to apply them and enrage did nothing. Verify enrage visibly ramps boss damage over the fight.

---

## 4b. NEW THING #1 — Summon screen (session start)
The owner performs **30 pulls** to open a play session. Pulls draw from the summon pool
(full 100, or a curated ~30–50 — build-time choice; curated is friendlier for team-mgmt).
- **Rarity odds** (playtest values — tune freely, they're disposable): **Common 60% / Epic 30% /
  Legendary 10%.** Within a rarity, pick a random unit of that rarity from the pool. Duplicates are
  allowed (a dupe just means you own two — no shard/merge system in the playtest).
- **Reveal:** simple is fine — reveal pulls one-by-one or as a grid; a light rarity-colored flourish
  sells the dopamine without heavy animation. No currency; the 30 pulls are just granted.
- Result: the pulled units land in `player.ownedUnits[]`. → advance to `TEAM_MGMT`.
- (Optional nicety: a "summon again / reset session" debug button so the owner can re-roll their
  pulls to feel different starting rosters.)

## 4c. NEW THING #2 — Team Management screen
- Show `player.ownedUnits[]` as a grid/list: name, role, affinity, rarity, and abilities
  (name / mult / cooldown / effects) on hover or expand.
- Owner selects a **team of 4**; enforce exactly 4 to proceed. Allow swap/deselect freely.
- Persist the chosen team in `player.activeTeam[]` (in-memory).
- Reachable from `MAIN_MENU` too, so the team can be re-picked between runs.
- Confirm → return to `MAIN_MENU`.

## 4d. NEW THING #3 — Main Menu (neutral hub)
- Minimal neutral screen. Two buttons: **Team Management** (→ `TEAM_MGMT`) and **Dungeon**
  (→ `DUNGEON_SELECT`).
- Show a small summary: active team (4 unit portraits/names) + player level (debug-adjustable).
- This is where a completed/failed run returns to.

## 5. NEW THING #4 — Dungeon-Select screen
Port the feel of `dungeon_select_mock.jsx`:
- Show **5 dungeon cards**, levels = `clamp(playerLevel + offset, 1, 100)` for offsets **[−10, −5, 0, +8, +15]**.
- Each card: tier (`ceil(D/10)`), level, a **difficulty verdict** (compute player/dungeon power ratio as in the mock → Faceroll / Comfortable / Fair / Stretch / Brutal), **fight count 3–9**, and the **sub-boss archetype**.
- RNG-lite: re-roll site name, fight count, sub-boss archetype, and affinity tint each time the board is shown; **level offsets stay fixed** (difficulty must be legible).
- Clicking a card → starts that run.
- Keep player level adjustable in the playtest UI (a debug slider is fine) so the owner can feel below/at/above quickly.

---

## 6. NEW THING #5 — Run Manager (the loop)
Owns run state and chains fights:
```
generateRun(D):
  fights = 3 + randInt(0..6)                 # 3..9
  tint   = randChoice(affinities)
  comps  = [ generateComp(D) for each fight ]
  bossRole = randChoice(5 roles)
  bossArchetype = archetypeFor(bossRole)     # sprint/bulwark/plague...

generateComp(D):
  n = 2..4 (lean 2-3 low tiers, 3-4 high tiers)
  roles = n draws from weighted pool [bruiser,bruiser,warden,zealot,hexer,mender]
  # variety over guarantee: do NOT force a "question" comp; sub-boss carries the guaranteed moment
```
Run flow (entered from `DUNGEON_SELECT` with `player.activeTeam` as the fighters):
1. `DUNGEON_SELECT` → pick dungeon → `generateRun`.
2. For each comp: spawn enemies (`spawnEnemies(roles, D, tint)`; 60% of enemies match the tint), `startFight` with `player.activeTeam`. **Persist player HP + cooldowns** into the next fight.
3. Between fights: brief progress screen (fight i/F, team HP bars) + **15% HP regen** to living units (not a full heal).
4. **Any fight LOSS → run ends** → `RESULT: failed` → back to `MAIN_MENU`. (Escrow: no rewards on fail.)
5. All normal fights cleared → spawn sub-boss (`makeBoss(bossRole, D, tint)`) → final fight.
6. Sub-boss WIN → `RESULT: complete` (placeholder reward toast) → back to `MAIN_MENU`.

---

## 7. The summon pool (what the 30 pulls draw from)
Draw from `roster.json` — either the full 100 or a **curated ~30–50** legible, distinct units
(build-time choice; curated keeps team management cleaner). Rarity odds as in §4b (Common 60 /
Epic 30 / Legendary 10). The owner ends with a semi-random `ownedUnits[]` and must build a good
team of 4 from what they actually pulled — that collection→teambuild decision is a core thing the
playtest validates. Player units fight at `lvl_mult(playerLevel)`-scaled base stats (no gear).

---

## 8. Explicit NON-goals (do not build)
Gear/itemization · reward economy / summon **currency** (the 30 pulls are just granted — no
earning/spending) · dupe shard/merge systems · cross-session persistence · production-engine
concerns · rich bespoke boss kits beyond the 2–3 archetypes above · real balance tuning.
**This build validates the front-end + LOOP feel, nothing else.** (Summoning, team management, and
the main-menu hub ARE in scope now — they're the session's front-end.)

---

## 9. Definition of done
Owner can, in the browser, end to end: **summon 30 units** (rarity odds respected) → **manage/pick
a team of 4** from owned units → land on a **main menu** (Team Management + Dungeon buttons) →
adjust level → **click Dungeon → see 5 dungeons** (below/at/above) → pick one → play **3–9
attrition-linked fights** → face a distinct **RNG'd sub-boss** (enrage boss visibly ramps) → win or
lose → **return to the main menu** (and can re-team or re-run). Then: **play it and report on feel.**

Keep the code readable and data-driven (roles, scaling constants, offsets, summon odds all as named
config at the top) so tuning during the playtest is trivial and disposable.
