# CLAUDE.md — read this first

## Start here

**Open `PROJECT_CONTROL.md` (repo root) before doing anything else.** It is the session-control
file: current state, locked decisions, build state, and "next session starts here". Its LOCKED
list is authoritative — where any other document disagrees with it, PROJECT_CONTROL wins.

## What this project is

A single-player, top-down 2D game fusing Elin-style sandbox depth with Epic Seven / FFBE-style
Momentum-driven tactical combat. Non-predatory: summon dopamine powered by *earned* currency,
never a wallet. The collection is completable.

## Where things live

| Path | What |
|---|---|
| `PROJECT_CONTROL.md` | **Open first.** Locked decisions, current state, build state, handoff |
| `data/roster.json` | The 100 units — the canonical data spine |
| `data/effects.json` | The 94-effect glossary the engine resolves (`data/effects.md` = readable render) |
| `data/roster.xlsx` | Human-review companion; the build reads the JSON, not this |
| `docs/` | Design docs and specs |
| `prototype/combat_prototype.html` | The playable build — combat slice + progression Steps 1–3 |
| `prototype/dungeon_select_mock.jsx` | UI feel reference (React mock, not production code) |
| `sim/encounter_sim.py` | Run simulator / regression harness. Runs from the repo root |
| `sim/power_model_v3.py` | Unit power scorer (design/validation, not the build) |

Both `sim/` scripts resolve `data/` relative to themselves — run them from anywhere.

## Locked rules that constrain almost every change

- **Damage:** `mitigated = raw × K/(K+DEF)`, **K = 1000** (playtested — do not change).
- **Power ceiling ~2.5×.** Levels give ~1.5×, gear ~1.7×, combined ceiling **~2.5×** a naked
  level-1 unit. This is the anti-overtuning spine. **If content is too hard, lower enemy scaling —
  never raise the ceiling.**
- **Debuffs:** `chance = skill_base × (1 + POT − RES)`, clamped `[0.05, 1.00]`.
- **6-stat model:** HP / ATK / DEF / SPD / POT / RES (+ derived CritRate/CritDmg). Same for units
  and enemies — an enemy is just a unit the AI drives.
- **Momentum** is the per-unit turn-order gauge (fills by SPD). Ults are gated by **per-unit
  cooldowns**, not a resource meter.
- **Affinity = the unit's TYPE, not its identity.** 5 affinities: Judgment(Red), Life(Green),
  Revelation(Blue), Majesty(Gold), Mystery(Dark). Wheel: Red→Green→Blue→Red; Gold↔Dark mutual.
  Gold and Dark are **off-wheel sidegrades** — never penalized vs RGB. Advantage = **+15% CritRate
  and +15% POT** on that action, *not* a flat damage multiplier.
- **Enemies are FROZEN content**, authored once against a tier power band. They do **not** live-scale
  off the player's loadout — a Lv100 boss's difficulty is absolute.
- **Difficulty comes from enemy KIT design, not stat scaling.** Dedicated healing flattens
  HP-attrition. The levers that work: burst > heal-rate, heal denial, enrage/time pressure, control
  on the support.
- **No artificial turn-cap loss** and **no instant-death timers** (Doom is removed; timed pressure
  uses `debuff_bomb`, which detonates a debuff payload, never a guaranteed kill).
- **Every unit stays valuable.** Rarity buys flexibility + stats + passive potency, never permission
  to matter. Slot-1 abilities are CD 0 and deal damage on all 100 units.

## Working discipline

**Spec deeply, build in playable vertical slices, and PLAYTEST each slice before speccing the next.**
A game is feel-defined. Constants are dials; the formulas are the deliverable.

When a doc and the data disagree, the data spine (`roster.json` / `effects.json`) is the truth for
units and effects; `PROJECT_CONTROL.md` is the truth for decisions.

## Known reconciliation debt

`docs/progression_slice_spec.md` is a v0.1 draft whose affinity list, rarity ladder, and run shape
predate later locks — it carries a banner listing exactly what is superseded. `docs/SIM_RESULTS.md`
has a retired turn-cap recommendation, likewise bannered. Read the banners before implementing from
either file.
