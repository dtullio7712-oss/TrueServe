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
| 4 | `progression_slice_spec.md` | ✅ v0.1 (revised after reconciliation) | Progression & rewards layer spec — persistence, allocation, gear, attrition run, crafting MVP |
| 5 | `progression_prototype_handoff.md` | ✅ ready → 🔨 **build in progress (Step 1 done)** | Build brief for extending the combat prototype with progression, in ordered playable steps |
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
`Game_Design_Doc.md` at **v0.2**. `combat_slice_spec.md` v0.1 — built and **first-playtested positive** (see prior session). `progression_slice_spec.md` v0.1 drafted, then **revised this session** after a reconciliation pass against the built combat prototype:
- **Per-unit stats, not a shared anchor** — the prototype's 4 hand-authored statlines (Justice glass cannon, Charity tank, etc.) are the canonical `baseStats`; the old flat 100/20/12 anchor is retired to a fallback-only role for un-tuned units/enemies.
- **K = 1000, not 300** — the DEF-mitigation divisor keeps the prototype's playtested value; the spec's original K=300 was a placeholder written without the prototype in hand.
- **Growth model changed to percentage-of-own-base** (not flat +N/point) so allocation is meaningful on both a 950-HP and a 1300-HP unit.
- **Owner-set growth budget locked:** level cap 100, milestone levels every 10, hard power ceiling ~2.5× (levels ~1.5× · gear ~1.7×) — the anti-overtuning spine for everything downstream.

**Progression build in progress** (`progression_prototype_handoff.md`, extending `prototype/combat_prototype.html` in place — same throwaway single-file build, no new project):
- ✅ **Step 1 — Persistence layer.** Each player unit now has a persistent record (level, xp, unspentPoints, allocatedPoints stub, gear[6] stub, baseStats, currentHP) saved to `localStorage`. Verified via headless-browser playthrough: HP and XP/level carry from battle 1 into battle 2, a level-up fires and grants a point pool, and state survives a full page reload (cross-session persistence). No stat/allocation math or management hub yet — that's Step 2.
- ⬜ Steps 2–8 remain (allocation math + hub, equipment, run/escrow structure, enemy scaling, crafting, profile viewer, playtest pass).

## NEXT SESSION STARTS HERE
**Deliverable:** Step 2 of `progression_prototype_handoff.md` — the stat + allocation math and a management-hub stub.

**Before building further:** derive the exact `POINT_PCT[stat]` per-point rates and points/level table so that a single-stat-focused build over 99 level-ups lands near +150% of base (the 1.5× ceiling), and confirm by simulation against a real prototype statline (not the fallback anchor) that a maxed single-stat build plus full gear lands near the 2.5× combined ceiling. **Show the derived numbers for a sanity check before wiring the rest of allocation.**

Then: implement the 6-stat model, rarity multipliers, SPD soft cap, the XP curve to level 100, milestone levels every 10 (bigger point pool + non-stat unlock), and a minimal management-hub screen to spend the `unspentPoints` already being tracked from Step 1 — with live before/after stat deltas. Playable checkpoint: win a fight → gain XP/level → open hub → spend points → see the unit's stats change → those changes carry into the next fight.

**The process lesson still holds:** playtest each step before the next. Don't build Steps 3+ until Step 2's allocation moment is confirmed to feel good, not just to compute correctly.
