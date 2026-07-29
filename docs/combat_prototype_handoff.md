# Handoff — Build the Combat Slice (Throwaway Browser Prototype)

> **What this is.** A build brief for a *throwaway* prototype of one turn-based fight, to answer a single question: **is this combat fun and does it feel good?** It is NOT the start of the shipping game. It will be discarded. Optimize for speed-to-playable and feel, not architecture.
>
> **Companion docs:** `combat_slice_spec.md` (the full mechanical spec — the source of truth for numbers and kits) and `Game_Design_Doc.md` (the why). This brief tells you *how to build it and in what order*; the spec tells you *what the systems are*.

---

## Build target
- **Single self-contained HTML file** (HTML + CSS + JS, canvas or DOM — builder's choice, whichever ships juice faster). No build step, no framework required. Opens in a browser by double-click.
- **Placeholder art only.** Units are labeled rectangles. Enemies are rectangles in a different color. No sprites, no imported art. This is a hard rule — art is where prototypes die.
- **No persistence, no menus, no meta.** Boot straight into the one fight. A "restart" button is the only chrome.

## The one question this must answer
Per `combat_slice_spec.md` §8: does the fight feel good to play? If it's mechanically correct but feels like clicking spreadsheet cells, it has **failed**. Feel is the deliverable.

---

## Build in THIS order (each step playable before the next)

Do not build the whole spec then run it. Build in playable increments, and pause at each checkpoint so it can be *seen moving* before the next layer goes on. This ordering is deliberate: it front-loads the two hardest-to-get-right things (turn feel, then game-feel) and leaves content for last.

**Step 1 — Momentum turn loop, nothing else.**
- 4 player rectangles vs. 1 enemy rectangle. Every unit has HP, ATK, DEF, SPD (use the spec's stat lines).
- Implement the Momentum fill (`§1`: `momentum += SPD * TICK_RATE`, act at 100, subtract 100 keeping overflow).
- Render the **turn-order track** (`§1.2`) at the top — the next ~6 actors as labeled boxes. This IS the interface; build it now, not later.
- Only action available: basic attack (S1) on a target. Damage per `§4.2`.
- **Checkpoint:** you can watch turn order flow, attack, and kill the enemy. It will feel dry — that's expected. Ship this before moving on.

**Step 2 — Game-feel pass on the dry loop.**
- Before adding ANY more mechanics, add the `§6.1` juice to the Step-1 loop: hit-pause (60–120ms freeze on impact), screenshake, white impact flash, damage-number pop, and placeholder sounds (a hit, a whiff, a UI blip — free/synth is fine).
- Animate the turn-order track: when a unit acts and resets, its box visibly slides back.
- **Checkpoint:** the *same dry loop* from Step 1 should now feel noticeably better. This step is the whole point — if juice on a trivial loop doesn't feel good, more mechanics won't save it. **This is the first real playtest.**

**Step 3 — The full 4 kits + Momentum manipulation.**
- Add S2/S3/S4 for all four units (Diligence, Patience, Charity, Justice) per `§3`, with cooldowns.
- Implement Momentum push/pull (`§1.3`) — and make the turn-order track *visibly reorder* when it happens (`§6.1`). This is the tactical payoff; it must be legible.
- Implement ult cooldowns (`§2`): per-unit turn counter, button lights up when ready.
- **Checkpoint:** you can pull Diligence's Momentum, watch the track resort, and feel the tactic land.

**Step 4 — Debuffs, affinities, the win condition.**
- Potency-vs-Resolve contest (`§4.3`), the minimum buff/debuff set (`§4.5`), the affinity wheel (`§4.4`).
- Justice's "punish the debuffed" identity (`§3.4`) — the payoff loop: set up → break → execute.
- One authored enemy team of 3–4 (`§5`) with the priority-list AI, including affinities and one Momentum-pusher so the player feels CR-control used *against* them.
- Win → short Gloria victory beat (`§6.4`). Loss → restart.
- **Checkpoint:** a complete, winnable, losable fight that exercises the full setup→execute loop.

---

## Tuning is expected, not a failure
Every constant in the spec (`TICK_RATE 0.07`, DEF softcap `1000`, push/pull `±25–30`, cooldown lengths) is a **first guess**. Expose them somewhere trivially editable (constants at the top of the file, or on-screen sliders if cheap). The playtester will change these by *feel*. Do not treat the spec's numbers as final — treat them as a starting position.

## What NOT to do
- Do not add a second engine, framework, or build system to "do it properly." Throwaway means throwaway.
- Do not import art, model creatures, or build overworld anything. Combat rectangles only.
- Do not build save/load, settings, roster management, or gacha. Out of scope by design.
- Do not skip Step 2 to "get all the mechanics in first." The game-feel pass on the dry loop is the earliest and most important checkpoint.

## Definition of done
The `§8` checklist in `combat_slice_spec.md`, all six items — with item 6 ("it feels good") weighted as the real bar. When it's playable end-to-end and feels good on rectangles, the prototype has done its job and the next decision (refine combat, or move to the capture→battle bridge) gets made from a position of knowing the fight is fun.
