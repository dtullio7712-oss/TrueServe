# TrueServe

A single-player, top-down 2D game fusing Elin-style sandbox depth with Epic Seven / FFBE-style Momentum-driven tactical combat. See `docs/PROJECT_CONTROL.md` for the full session log and current state.

## Docs
- `docs/PROJECT_CONTROL.md` — session control / handoff (read this first)
- `docs/Game_Design_Doc.md` — master design doc
- `docs/combat_slice_spec.md` — implementable spec for the first playable fight
- `docs/combat_prototype_handoff.md` — build brief for the browser prototype
- `docs/progression_slice_spec.md` — spec for the progression & rewards layer wrapping combat
- `docs/progression_prototype_handoff.md` — build brief extending the combat prototype with progression

## Combat prototype
`prototype/combat_prototype.html` is a throwaway, self-contained browser prototype — open it directly in a browser, no build step. It implements the full combat slice spec: the Momentum turn-order track, all four virtue kits (Diligence / Patience / Charity / Justice) with cooldown-gated ults, Momentum push/pull, the Potency-vs-Resolve debuff contest, the affinity wheel, a 3-unit enemy team with priority-list AI, win/loss, and the game-feel juice pass (hit-pause, screenshake, flash, damage numbers, sound, turn-track pulse).

It's also where the progression layer is being built, per `docs/progression_prototype_handoff.md`, extending this same file in ordered playable steps rather than starting a new project:
- **Step 1 (done):** persistence. Each player unit's level/XP/HP now survives across battles and across sessions (saved to `localStorage`). Win a fight and the roster overlay shows updated levels/XP/HP; a unit that took damage or leveled up carries that state into the next battle.
- **Step 2 (done):** stat + allocation math and a management hub. Growth is percentage-of-own-base per point, hard-clamped per stat, calibrated so every rarity can reach the same per-stat ceiling (a bigger rarity's extra points buy room for a *second* maxed stat, not a higher single-stat cap). Click "Manage Roster" from the start/continue screen to spend points per unit with live before/after stat deltas, or respec for free.
- **Step 3 (done):** equipment + substats. 6 typed slots per unit (Weapon/Armor/Emblem fixed-main, Boots/Charm/Relic choosable-main), substats including `DualAttackChance`, gear rarity driving substat count, and the spec's budget guard (gear capped at 40% of a stat's allocated+base value, so it augments allocation rather than replacing it). Use "+ Generate Sample Piece" in the hub to get test gear (a placeholder stand-in for the real drop/crafting systems landing in Steps 5–6), then assign it per-slot per-unit with live stat deltas. The run/escrow structure lands in the next step.

Tunable constants live at the top of the `<script>` block (`TUNING` for combat/XP dials, `ALLOC` for the allocation-growth dials, and the gear config block for substat ranges/rarity tiers/the budget cap) — tune by feel per the spec's playtest discipline.
