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
- **Step 1 (done):** persistence. Each player unit's level/XP/HP now survives across battles and across sessions (saved to `localStorage`). Win a fight and the roster overlay shows updated levels/XP/HP; a unit that took damage or leveled up carries that state into the next battle. Stat allocation, gear, and the run/escrow structure land in later steps.

Tunable constants live at the top of the `<script>` block (`TUNING`) — tune by feel per the spec's playtest discipline.
