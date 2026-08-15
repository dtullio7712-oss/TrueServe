# TrueServe

A single-player, top-down 2D game fusing **Elin-style sandbox depth** with **Epic Seven / FFBE-style
Momentum-driven tactical combat**. Non-predatory by design: the summon dopamine (rarity, pity,
banners) is powered by *earned* currency, never a wallet, and the collection is completable.

**Start with [`PROJECT_CONTROL.md`](PROJECT_CONTROL.md)** — session control, locked decisions,
current state, build state, and where the next session picks up. Where any other doc disagrees with
it, PROJECT_CONTROL wins. [`CLAUDE.md`](CLAUDE.md) is the short orientation for Claude Code.

## Layout

```
PROJECT_CONTROL.md   session control — open first
CLAUDE.md            orientation + locked rules for Claude Code
data/                the canonical data spine
docs/                design docs & specs
prototype/           the playable browser builds
sim/                 balance harness + power model
tools/               build scripts
```

### `data/` — the data spine

| File | What |
|---|---|
| `roster.json` | The **100 units** (v0.6) — statlines, abilities, signatures, 3 passives each |
| `effects.json` | The canonical **94-effect glossary** (v0.5) the engine resolves |
| `effects.md` | Readable render of the glossary — same 94 effects, verified 1:1 against the JSON |
| `roster.xlsx` | Human-review companion with powerscore sheets. **The build reads the JSON** |

Roster: Judgment/Red 25 · Life/Green 25 · Revelation/Blue 25 · Mystery/Dark 13 · Majesty/Gold 12.
Rarity split: 36 Common · 35 Epic · 29 Legendary.

### `docs/` — design docs & specs

| File | What |
|---|---|
| `Game_Design_Doc.md` | Master design doc — the whole vision, especially the un-built sandbox half |
| `combat_slice_spec.md` | The combat vertical slice — **playtested**, the engine's spec |
| `combat_prototype_handoff.md` | Original build brief for the browser prototype (historical) |
| `progression_slice_spec.md` | Levels, gear, dungeons, run rules. ⚠️ v0.1 — read its banner first |
| `progression_prototype_handoff.md` | Step-by-step build brief for the progression layer |
| `enemy_profiles_scaling.md` | 5 enemy roles, the scaling curve, per-archetype sub-boss premium |
| `ENCOUNTERS.md` | The 14-type encounter menu |
| `GEARING.md` | Gear power envelope: 7 rarity tiers, 4+2 sets, substats, unique gear |
| `SIM_RESULTS.md` | Sim findings — difficulty is kit design, not stat scaling |
| `HANDOFF_playtest_build.md` | Handoff for the Story/Grind playtest build |
| `playtest_build_spec.md` | The build spec for that playtest |
| `SIDE_GAMES.md` | Side/mini-game concept backlog (vision-stage) |

### `prototype/` — the playable build

`combat_prototype.html` is a throwaway, self-contained browser build — open it directly, no build
step. It implements the full **combat slice**: the Momentum turn-order track, all four virtue kits
(Diligence / Patience / Charity / Justice) with cooldown-gated ults, Momentum push/pull, the
Potency-vs-Resolve debuff contest, the affinity wheel, a 3-unit enemy team with priority-list AI,
win/loss, and the game-feel juice pass (hit-pause, screenshake, flash, damage numbers, sound,
turn-track pulse).

It is also where the **progression layer** is being built — extending this same file in ordered
playable steps rather than starting a new project (`docs/progression_prototype_handoff.md`):

- **Step 1 (done) — persistence.** Level/XP/HP survive across battles and across sessions via
  `localStorage`. A unit that took damage or levelled up carries that state into the next battle.
- **Step 2 (done) — allocation math + management hub.** Growth is percentage-of-own-base per point,
  hard-clamped per stat, calibrated so every rarity reaches the same per-stat ceiling — a higher
  rarity's extra points buy room for a *second* maxed stat, not a taller single-stat cap. "Manage
  Roster" spends points with live before/after deltas; respec is free.
- **Step 3 (done) — equipment + substats.** 6 typed slots (Weapon/Armor/Emblem fixed-main;
  Boots/Charm/Relic choosable-main), substats including `DualAttackChance`, gear rarity driving
  substat count, and the spec's budget guard (gear capped at 40% of a stat's allocated+base value,
  so it augments allocation rather than replacing it). "+ Generate Sample Piece" yields test gear —
  a placeholder for the real drop/crafting systems in Steps 5–6.
- **Steps 4–8 remain:** run/escrow structure, enemy scaling + drops, crafting MVP, profile viewer,
  playtest pass.

Tunable constants live at the top of the `<script>` block — `TUNING` for combat/XP dials, `ALLOC`
for allocation growth, and the gear config block for substat ranges, rarity tiers, and the budget
cap. Tune by feel, per the spec's playtest discipline.

`playtest_build.html` is the **Story/Grind playtest**: summon 30 → pick a team of 4 from the full
100-unit roster → main menu → a board of 5 dungeons → a 3–9 fight run with HP and cooldowns carrying
→ an RNG'd sub-boss → win/lose. Manual control with 1×/2×/4× speed. It reads the data spine, so it
needs a server:

```bash
python3 -m http.server 8000          # from the repo root
# open localhost:8000/prototype/playtest_build.html
```

**To play it on another machine**, bake a single self-contained file instead — no server, no other
files, just double-click it:

```bash
python3 tools/build_standalone.py    # → prototype/playtest_standalone.html (~0.22 MB)
```

That output is **generated** — edit `playtest_build.html` and re-run the script, never edit the
standalone by hand.

`dungeon_select_mock.jsx` is a React mock of the 5-dungeon selection screen — a feel reference, not
production code.

### `sim/` — balance harness

```bash
python3 sim/encounter_sim.py --level 40 --seed 7        # one verbose run
python3 sim/encounter_sim.py --sweep                    # clear-rate across all 10 tiers
python3 sim/encounter_sim.py --level 40 --team badcomp  # 4-tank failure demo
python3 sim/power_model_v3.py                           # unit powerscore bands
```

`encounter_sim.py` is the **regression check**, not a balancing tool: it confirms a change didn't
break the bands rather than finding balance for you. `power_model_v3.py` scores every unit into dual
Skirmish/Boss numbers. Both resolve `data/` relative to themselves, so they run from anywhere.

## The locked spine

- **Damage:** `mitigated = raw × K/(K+DEF)`, **K = 1000** (playtested).
- **Power ceiling ~2.5×** (levels ~1.5× · gear ~1.7×). If content is too hard, lower enemy scaling —
  never raise the ceiling.
- **Difficulty comes from enemy kit design**, not stat scaling — dedicated healing flattens
  HP-attrition.
- **Enemies are frozen content**, authored once against a tier power band; they never live-scale off
  the player's gear.
- **No instant-death timers, no artificial turn-cap.**

## Working discipline

Spec deeply, build in playable vertical slices, and **playtest each slice before speccing the next.**
Constants are dials; the formulas are the deliverable.
