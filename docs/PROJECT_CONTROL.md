# PROJECT CONTROL — [Working Title: TBD]

> **This is the file we open FIRST at the start of every session.**
> It exists so no session wastes time reconstructing context, and so every session ends on a clean handoff. Read the "Current State" and "Next Session Starts Here" sections, and we're immediately oriented.

---

## What this project is (the 30-second version)

A **single-player, top-down 2D** game fusing:
- **Elin-style sandbox depth** — town-building, farming, crafting, breeding, scaling dungeons, mini-games, steady multi-system wealth buildup.
- **Epic Seven / FFBE-style gacha combat** — Combat-Readiness turn-based tactical battles with a deep, collectible roster.

**Non-predatory / single-player.** Summon dopamine (rarity, pity, banners) powered by *earned* currency, never a wallet. Collection is completable.

**Theme (v0.1):** reverent treatment of the sacred. Roster = original **human virtue-embodiments** (virtue = combat identity). Angels = rare un-ownable *interventions* above the collection layer. Tier ladder = celestial-hierarchy *skin*, not naked power rank. Systems religion-agnostic under the hood.

**Design pillar:** every unit stays valuable — rarity buys *flexibility + stats*, not *permission to matter*. Generalists (high rarity) vs. irreplaceable specialists (low rarity).

---

## Who's building this & how we work

- **Owner (you):** technical product owner / systems designer. Manages a dev team, ships spec-driven `.md` work to Claude Code + Fable for implementation (has built a servicing engine this way). **Not writing engine code by hand.** Strength = precise, unambiguous specs.
- **Primary goal:** design a game *you* would replay. Commercial success is a welcome bonus, not the driver.
- **Implementation path:** thorough per-system `.md` specs → Claude Code / Fable implements.

### The ONE discipline that keeps this alive
> **Spec deeply, but build in playable vertical slices, and PLAYTEST each slice before speccing the next.**
> A servicing engine is *correctness-defined* (a spec can be complete). A game is *feel-defined* (only playtesting reveals fun). The failure mode to avoid: writing a huge spec, building it all, then discovering the core loop is boring. Deep spec for the slice we're building now; light sketches for everything downstream until the slice proves out.

### Session discipline
- Each session has **one named deliverable.**
- Each session **ends by updating this file** (Current State + Next Session Starts Here).
- Get more specialized/dedicated per session as we go. No sprawl.

---

## Tech stack
**Production engine: deliberately deferred.** Godot vs Unity is a reversible, late decision (a "weekend choice" once systems are known). Leaning Godot 4 as a placeholder; not committed. Not scoping until the design is coherent on paper.

**Prototype tool ≠ production engine (resolved this session).** "Build combat first" and "defer the engine" only conflict if you assume the slice must be built in the shipping engine. It doesn't. The combat slice is a *question-answering artifact* — its only job is to answer "is this fight fun?" per §8 of the slice spec. That needs the cheapest thing that puts rectangles on screen with juice, not the engine we ship in.
- **Prototype tool = browser / HTML5 canvas** (plain JS, or a tiny lib if needed). Fastest path to playable feel, plays to the Claude Code / Fable pipeline's strengths, zero install/build friction, throwaway by design.
- **This keeps the engine decision genuinely open** — we make Godot-vs-Unity *later*, with real data about how the combat code wants to be structured.
- **Known limit, stated plainly:** a browser prototype validates *feel + math only*. It says nothing about engine performance, asset pipelines, or the overworld↔combat transition. Those are real questions — just not *this* slice's questions. A great-feeling browser prototype does NOT validate the engine choice; don't let it pretend to.

---

## Deliverables ledger

| # | File | Status | Purpose |
|---|---|---|---|
| 0 | `PROJECT_CONTROL.md` | ✅ this file | Session control + handoff |
| 1 | `Game_Design_Doc.md` | ✅ v0.1 | Master design doc (why + systems overview) |
| 2 | `combat_slice_spec.md` | ✅ v0.1 drafted → 🔲 **needs playtest** | Implementable spec for a playable single fight — the first thing to build & playtest |
| 3 | `combat_prototype_handoff.md` | ✅ ready | Build brief for the throwaway browser prototype — hand to Claude Code / Fable to build the slice in ordered, playable steps |
| … | (economy, bridge, town, roster) | ⬜ later | One spec at a time, in build order, each after the prior slice playtests |

**Archive note:** Jan 2026 "Angels" design bible (folder: *Archangels' Oath / For His Glory*) reviewed this session. It was a *different game* — F2P-monetized, PC 3D Unity, named biblical figures as the roster — and is **superseded**, NOT the current direction. Two mechanics were salvaged from it into the combat slice (see LOCKED list). Everything else in that folder (monetization economy, named-saint roster, 10%-resource-loss-on-death) is **explicitly not carried forward.**

---

## Design decisions LOCKED (don't relitigate without reason)
- Single-player; non-predatory; completable collection.
- Roster = original human virtue-embodiments; angels = interventions, not units.
- Tier ladder is a flavor skin; balance handled underneath.
- Every unit stays valuable (rarity = flexibility, not relevance).
- No duplicate-shredding; dupes unlock new roles/kits.
- Lite async "PvP" = uploaded teams become PvE AI defense fights.
- **Combat gets built & playtested FIRST**, before other systems are fully specced.
- **Visual direction:** *simpler* overworld (many assets → keep per-asset cost low), *more substantial* combat (attention + asset reuse concentrated there). BUT the combat goal is FF7-**feel**, not FF7-**fidelity** — "impactful" comes mostly from *animation & game-feel* (hit-pause, screenshake, particles, sound), not resolution/poly count. Real references: Sea of Stars, Chained Echoes, Octopath Traveler — NOT literal FF7 (original = 100+ person Squaresoft; Remake = AAA). **Feel-first, fidelity-later:** build combat with placeholder art, prove the fight is fun with juice layered on rectangles, invest in real art only after. Art/animation is where solo projects die — defer and abstract it. Also watch overworld↔combat *cohesion* (shared palette/design language + intentional transition) so the fidelity gap reads as stylized, not unfinished.
- Other systems (farming→defense/endurance, crafting mini-games→character gains, town→unit buffs) are acknowledged as *feeders into combat* and will be specced later. Direction noted, details deferred.
- **Momentum = the turn-order gauge (from combat slice v0.1).** Per-unit gauge, fills by Speed, decides **who acts** (the CR system, renamed). Placeholder name; Initiative is the alternate. Mechanics don't depend on the word.
- **Ults gated by per-unit turn-based cooldowns**, not a resource meter. Simple and legible for the first slice. *(The earlier team-shared "Glory" meter is **shelved, not deleted** — parked as a possible downstream team-tempo layer if cooldowns feel flat in playtest. "Gloria" survives as victory-beat flavor.)*
- **Potency vs. Resolve** = the debuff-application contest stat axis (renamed from E7's "Effectiveness / Effect Resistance"). Potency = how hard your effects land; Resolve = the will to resist them. `chance = skill_base × (1 + Potency − Resolve)`.
- **Affinity wheel salvaged from Angels bible.** Judgment→Life→Revelation (3-cycle) + Majesty↔Mystery (mutual-weakness pair). Advantage = **+15% crit rate / +15% Potency for that action** (NOT a flat damage multiplier — more nuanced, less snowbally). Names are Jan placeholders → rename religion-agnostic later.
- **Dual/assist attacks are gearable.** Players can build *into* dual-attack chance as a stat/substat, making off-turn assists a deliberate teambuilding axis, not just ambient RNG.
- **4th starter = Justice** (conditional finisher: big damage only into debuffed/broken enemies). Chosen over "Zeal" so the enabler-heavy party (Diligence/Patience/Charity) gets a real win condition, and to avoid the wrath/violence tonal edge under the reverence pillar.

## Design decisions OPEN (to resolve later)
- Are combat units the same as overworld character+pets, or a separate summoned roster? *(Note: the Jan Angels bible silently assumed **separate summoned roster** throughout — worth acknowledging we've leaned that way longer than the docs admit. Combat slice works under either answer.)*
- Permadeath: Elin has roguelike DNA; gacha never deletes units. Reconcile (likely: overworld body can fall, roster persists).
- Core loop diagram (minute-to-minute session shape) — not yet drawn.
- Economy currencies & the multi-system wealth spine — not yet designed.
- Rewards/ranking wrapper for lite-PvP without reintroducing FOMO.

---

## CURRENT STATE
`Game_Design_Doc.md` at **v0.2** (combat table cleaned up: CR→Momentum, ult cooldowns, Potency-vs-Resolve, dual-attack gearing, Glory shelved). **`combat_slice_spec.md` v0.1** drafted — full Momentum turn system, per-unit cooldown-gated ults, 4 complete virtue-kits (Diligence / Patience / Charity / Justice), damage + Potency-vs-Resolve contest math, affinity wheel, and a feel-first juice spec. Affinity wheel salvaged from the reviewed-and-superseded Jan "Angels" bible; team-Glory meter drafted then **shelved** in favor of cooldowns. **Spec is written but NOT yet built or playtested** — that's the whole point of the next phase.

## NEXT SESSION STARTS HERE
**Deliverable:** build the throwaway combat prototype and **playtest it** — per the ONE discipline, no new specs until this slice proves fun.

**How:** hand `combat_prototype_handoff.md` to Claude Code / Fable (or a fresh build session). It builds the slice as a single self-contained browser HTML file, placeholder rectangles only, in four ordered playable steps:
1. **Momentum turn loop** (dry, no juice) → see turn order flow.
2. **Game-feel pass** (hit-pause, shake, flash, number-pop, sound) on that dry loop → *first real playtest; the make-or-break checkpoint.*
3. **Full 4 kits + Momentum push/pull** → feel the tactic land.
4. **Debuffs, affinities, win/loss** → the complete setup→execute fight.

**The process lesson this is teaching:** a game slice is *done when it feels right*, not when it's spec-complete — the opposite of the servicing-engine loop. Build the smallest playable thing, play it, react, tune the constants by feel. The spec's numbers are starting guesses, not final.

**After it plays well:** decide whether to refine combat depth or move to the next system spec (leading candidate: the capture→roster→battle *bridge*, proving one unit crosses from overworld into a fight).

Reminder: resist speccing downstream systems until the slice is *fun in your hands*.
