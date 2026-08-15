# progression_prototype_handoff.md — Build brief for Claude Code / Fable

> **What this is:** an ordered, playable build brief for the progression & rewards layer.
> You are **extending the existing throwaway combat-slice browser prototype**, not starting a
> new project and not rebuilding combat. Same disposable single-file (or small-file) browser
> build. The engine decision (Godot vs Unity) is deliberately deferred — do **not** introduce a
> framework or build step. Plain HTML5 canvas + JS, as before.

---

## Read first (in this order)
1. `progression_slice_spec.md` — **the spec you are implementing.** Source of truth.
2. `PROJECT_CONTROL.md` — project discipline + LOCKED decisions. Note especially: throwaway
   browser build, feel-first / math-proven, no engine commitment.
3. `combat_slice_spec.md` — the combat layer you are wrapping. **Reconcile baseline stat
   constants in the progression spec against the statline this prototype actually shipped with;
   where they differ, keep the values the first playtest proved fun. The progression spec's
   formulas are authoritative; its raw numbers are a starting position, not gospel.**
4. The existing prototype code at `prototype/combat_prototype.html`.

---

## Prime directive
Extend the existing prototype so that a fight is no longer a one-off: units **persist and grow**
across a **10-battle attrition run**, loot is **escrowed and committed on clear**, and between
runs the player **allocates levels, crafts/upgrades gear, and equips**. Everything hangs on the
persistence layer — build that first.

Do **not** refactor or re-tune the existing combat feel unless a step requires it. Combat was
playtested and is fun; you are adding a shell around it.

---

## Build in ordered, individually-playable steps
After **each** step, the build must run in a browser and be playable/inspectable. Do not batch
steps. This mirrors the project's vertical-slice discipline: prove each layer before the next.

### Step 1 — Persistence layer (the foundation)
- Give each unit a persistent object: `level, xp, allocatedPoints{...}, gear[6], baseStats`.
- State survives across battles **and** across runs (in-memory + a save blob to `localStorage`
  is fine for the throwaway build).
- **Playable checkpoint:** run two consecutive battles; a unit that leveled/took damage in the
  first reflects that state entering the second.

### Step 2 — Stat + allocation math + management-hub stub (spec §3–4, §11)
- Implement the 6-stat model, rarity multipliers, the per-point allocation table (now
  **percentage-of-own-base**, per the growth-budget revision), the SPD soft cap, XP curve to
  level cap 100, milestone levels every 10.
- Build a minimal **management hub** screen to spend pooled points, with **live before/after
  stat deltas**.
- Free respec for now.
- **Playable checkpoint:** win a fight → gain XP/level → open hub → spend points → see the unit's
  stats change → those changes carry into the next fight.

### Step 3 — Equipment + substats (spec §5)
- 6 typed slots, main stats, substat pool (**include DualAttackChance**), roll ranges, the gear
  budget cap, gear leveling milestones.
- Assign/unassign in the hub with live stat deltas.
- **Playable checkpoint:** equip a piece, watch stats update, take the change into a fight.

### Step 4 — Run structure: attrition + escrow (spec §10.1–10.2, §13)
- Dungeon select screen (5 entries, stub scaling for now).
- A run = 10 sequential battles. **HP + cooldowns carry across all 10 (attrition).** No heal
  between fights (leave the §10.1 battle-5 rest valve OFF by default; make it a one-line toggle).
- Drops go to **escrow**. **Clear battle 10 → commit escrow to permanent. Lose any battle →
  wipe escrow, restart at battle 1.** Brought-in levels/gear persist regardless.
- **Playable checkpoint:** a full run that can be won (commit) or lost (wipe + restart), with
  attrition visibly biting by the later battles.

### Step 5 — Enemy scaling + drops (spec §10.3–10.5)
- Per-dungeon power multiplier + intra-dungeon +6%/battle + boss bonus on battle 10.
- Enemy drop tables (materials always; gear on a roll; boss guarantees).
- **Playable checkpoint:** dungeon 1 is clearable at low level; dungeon 3 clearly demands
  building first.

### Step 6 — Crafting MVP (spec §9)
- Two actions only: **Forge** (random main + substats from slot pool) and **Upgrade** (level a
  piece, roll substats at milestones). Material tiers Shard/Core/Sigil.
- **Playable checkpoint:** turn escrowed-then-committed materials into a usable gear piece.

### Step 7 — In-fight profile viewer (spec §12)
- Tap/click any unit (ally or enemy) mid-battle → read-only card: 6 stats (current vs base),
  level, affinity, rarity, buffs/debuffs w/ counters, cooldowns, gear summary (allies only).
- **Playable checkpoint:** you can inspect an enemy's DEF/RES mid-fight and it informs a decision.

### Step 8 — Playtest pass
- Stop and make the whole loop playable end-to-end. Surface the §16 playtest questions in a
  short notes file so the owner can evaluate feel, not just correctness.

---

## Guardrails
- **Data-driven:** units, affinities, skills, gear, enemies, drop tables = data structures/JSON,
  not hardcoded logic. Adding "a 10th Justice unit" or a new dungeon must be a data edit.
- **Affinity ≠ Unit:** a unit references an affinity id; many units share one affinity. Do not
  hardcode one-unit-per-affinity anywhere.
- **All constants in one tunable config block** (stat rates, K=1000, dungeon mults, XP curve,
  substat ranges, caps). The owner will dial these during playtest; make that a one-file edit.
- **Don't over-build art.** Rectangles + juice, per the feel-first pillar. No asset pipeline.
- **Don't commit to an engine or add a bundler.** Keep it throwaway and instantly runnable.

---

## Definition of done for this handoff
A browser build where a player picks a dungeon, fights a 10-battle attrition run, loses the run
(and its escrow) if sloppy, wins it to commit loot, then between runs levels units (manual
allocation), crafts/upgrades gear, equips across 6 slots, and can inspect any unit's real stats
mid-fight — all persisting across sessions, all constants in one config block.
