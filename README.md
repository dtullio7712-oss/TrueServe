# TrueServe

A single-player, top-down 2D game fusing Elin-style sandbox depth with Epic Seven / FFBE-style Momentum-driven tactical combat. See `docs/PROJECT_CONTROL.md` for the full session log and current state.

## Docs
- `docs/PROJECT_CONTROL.md` — session control / handoff (read this first)
- `docs/Game_Design_Doc.md` — master design doc
- `docs/combat_slice_spec.md` — implementable spec for the first playable fight
- `docs/combat_prototype_handoff.md` — build brief for the browser prototype

## Combat prototype
`prototype/combat_prototype.html` is a throwaway, self-contained browser prototype of the combat slice — open it directly in a browser, no build step. It implements the full spec: the Momentum turn-order track, all four virtue kits (Diligence / Patience / Charity / Justice) with cooldown-gated ults, Momentum push/pull, the Potency-vs-Resolve debuff contest, the affinity wheel, a 3-unit enemy team with priority-list AI, win/loss, and the game-feel juice pass (hit-pause, screenshake, flash, damage numbers, sound, turn-track pulse).

Tunable constants live at the top of the `<script>` block (`TUNING`) — tune by feel per the spec's playtest discipline.
