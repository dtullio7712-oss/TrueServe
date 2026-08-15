# HANDOFF — Build the Story/Grind Playtest (HTML)

> **Read `PROJECT_CONTROL.md` first, then this.** This handoff drives the next 1–2 sessions:
> get a **playable Story/Grind loop in the browser** and **play it for FEEL.** That is the
> single goal. Nothing downstream (the wide-net content phase, the tier power-envelope table,
> content authoring) begins until the loop proves fun.

---

## The one question this playtest answers
**Is the core loop fun?** Specifically: is the run tempo right (3–9 fights → sub-boss)? Do the
teambuilding + dungeon-choice decisions feel good? Does attrition across a run create meaningful
tension? Everything else is out of scope.

**Balance is explicitly NOT the goal.** Tune numbers freely *during* play to keep it enjoyable,
but treat those tweaks as **disposable** — real balance happens later, against the full feature
set, per the locked efficiency-first plan. Don't sink time into balance you'll redo.

---

## What already exists (inputs — reuse, don't rebuild)
- **Combat engine:** the playtested Momentum prototype (`prototypes/combat-slice/`). Momentum turn order, cooldown-gated abilities, K=1000 damage, affinity wheel, debuffs. **This is the combat core — extend it, don't rewrite it.**
- **Roster data:** `roster.json` — 100 units, real statlines, abilities (mult/cooldown/target/effects/bonus_vs), passives. The playtest uses a **hand-picked subset** (see below), not all 100.
- **Effect glossary:** `effects.json` — canonical effect ids the engine already resolves.
- **Enemy design:** `enemy_profiles_scaling.md` — 5 enemy roles + scaling curve + per-archetype sub-boss premium. **The build implements this.**
- **Dungeon-select feel:** `dungeon_select_mock.jsx` — the 5-dungeon selection screen, already built as a React mock. **Port its interaction/feel into the prototype** (it's a reference, not production code).
- **Balance reference:** `encounter_sim.py` — the run simulator. Not shipped in the playtest, but its **numbers/curves are the source of truth** for enemy scaling. The HTML build should mirror its formulas so the playtest matches what we simmed.

---

## THE PLAYER FLOW (what the playtest build must deliver end-to-end)

The playtest is now a fuller vertical slice — not just the run loop, but the front-end that
leads into it. The full flow the owner will walk through:

```
SUMMON (30 pulls) → TEAM MANAGEMENT (pick your team) → MAIN MENU (neutral hub)
     → [Dungeon button] → DUNGEON SELECT (pick 1 of 5) → RUN (3–9 fights → sub-boss) → RESULT
                          ↑ [Team Management button] can also return here to re-pick
```

This makes the playtest feel like a real session: you build your account by summoning, decide who
plays, then go fight. Four new systems (the combat engine already exists — extend it):

### NEW THING #1 — Summon screen (run-start acquisition)
The owner performs **30 summons** to open a play session, pulling units from the roster. This is
the collection-dopamine moment. For the playtest: pulls come from `roster.json` (respecting rarity
odds — see build spec), animate/reveal simply, and land in the player's owned-units pool. **No
currency/economy** — the 30 pulls are just granted for the playtest (summon *currency* is a later
system; here we validate the *feel* of pulling and building around what you got).

### NEW THING #2 — Team Management screen
After summoning, the owner **chooses which of their pulled units form the active team** (team of
4). Shows owned units (role, affinity, rarity, abilities), lets the player select/swap the 4-unit
team, and confirms. Reachable again later from the main menu so the team can be re-picked between
runs.

### NEW THING #3 — Main Menu (neutral hub)
A simple neutral position with two buttons: **Team Management** and **Dungeon**. This is the
"home base" the owner returns to. Clicking Dungeon → Dungeon Select.

### NEW THING #4 — Dungeon Select + Run Manager (the loop)
Unchanged from before — 5 dungeons below→at→above level, pick one, play a 3–9 fight run with
carried attrition into an RNG'd sub-boss. (Detail below and in the build spec.)

---

## THE RUN LOOP DETAIL (was "the couple of new things")

### Dungeon-Select screen
Port `dungeon_select_mock.jsx`'s core: show **5 dungeons spanning below→at→above the player's
level** (offsets −10/−5/0/+8/+15), each with tier/level, a difficulty verdict, fight count (3–9),
and the sub-boss archetype. Picking one starts a run. Difficulty is a **player choice** — a core
feel pillar, present even in a rough playtest.

### The Run Manager (the loop wrapper)
The engine fights one battle; the Run Manager chains them:
1. Generate a run: F fights (3–9) of RNG'd enemy compositions, ending in one RNG'd sub-boss.
2. **Carry attrition:** unit HP + ability cooldowns persist across all fights in the run (per the
   locked attrition rule). Apply ~15% between-fight HP regen (NOT a full heal).
3. Between fights, show a brief run-progress screen (which fight you're on, team HP state).
4. **Lose any fight → run ends** (escrow model: rewards only commit on sub-boss clear). For the
   playtest, a simple "run failed, restart" is enough — the reward economy is out of scope.
5. Sub-boss clear → "run complete" screen. (Rewards can be a placeholder toast; not the point.)

**Enemy instantiation** (supports both new things): a small generator that builds enemy
combatants from `enemy_profiles_scaling.md` — role anchor × the level+enemy-gear scaling curve,
with the per-archetype HP premium on sub-bosses. Mirror `encounter_sim.py`'s formulas exactly.

---

## The summon pool (what the 30 pulls draw from)
The 30 pulls draw from `roster.json`. For a legible playtest you can either use the **full 100**
or a **curated pool of ~30–50** legible, distinct units — either is fine; curated keeps the
team-management screen less overwhelming. Respect rarity odds so pulls feel meaningful (Common
common, Legendary rare — exact odds in the build spec). The point is the owner ends up with a
*semi-random owned roster* and must build a good team of 4 from what they actually got — that's
the collection→teambuilding decision the playtest is validating.

---

## Scope guardrails (what NOT to build)
- ❌ No reward economy / currency / summons — placeholder toast on run-complete is fine.
- ❌ No gear system in the playtest — units fight at their level-scaled base (gear is a *later*
  power layer; the playtest validates the *loop*, not itemization).
- ❌ No persistence between sessions — in-memory run state is fine.
- ❌ No production-engine concerns — throwaway HTML5/canvas, feel+math only.
- ❌ Don't rebuild the combat engine — extend the existing prototype.
- ❌ Don't implement all 5 enemy archetypes' bespoke boss kits richly — the 3 in the sim
  (Sprint/Bulwark/Plague or similar) are enough to make sub-bosses feel distinct.

---

## Deliverable of the next session
A browser build where the owner can, end to end: **summon 30 units → manage/pick a team of 4 →
land on a main menu → click Dungeon → pick from 5 dungeons → play a 3–9 fight run with carried
attrition → face an RNG'd sub-boss → win/lose the run → return to the main menu.** Then **play it
and report on feel** — both the front-end (summon/teambuild dopamine) and the run loop.

**The Claude Code build spec is: `playtest_build_spec.md`** (generated alongside this handoff).
Hand that to Claude Code to implement.

---

## After the playtest (do NOT start until feel is confirmed)
Per `PROJECT_CONTROL.md` → "THE PLAN": cast the **wide net** (all content as a dependency graph
with a power-budget column), whose **first deliverable is the player-power envelope per tier** —
the table every enemy and every power source is authored against. Then implement in dependency
order with the sim as the regression check.
