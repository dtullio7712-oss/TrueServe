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
- ✅ **Step 1 — Persistence layer.** Each player unit has a persistent record (level, xp, unspentPoints, allocatedPoints, gear[6] stub, baseStats, currentHP) saved to `localStorage`. HP and XP/level carry from battle to battle, and state survives a full page reload.
- ✅ **Step 2 — Stat + allocation math + management hub.** Derived `POINT_PCT` numbers (shown to and confirmed by the owner) are wired in: growth is percentage-of-own-base per point, hard-clamped per stat at `ALLOC.TARGET_PCT` (HP 50%/ATK 45%/DEF 45%/SPD 30%/POT 20%/RES 20%), calibrated against the Common rarity's full 357-point career pool so every rarity can reach the same per-stat ceiling — a higher rarity's extra points/level buy genuine flexibility (room to also max a 2nd stat) rather than a bigger single-stat ceiling. SPD uses the spec's soft-cost guard (points past +50% of base cost double) instead of a hard clamp. The 4 prototype units were assigned placeholder rarities for points/level purposes only (Diligence R, Patience C, Charity E, Justice L) — their hand-tuned base stats are *not* additionally multiplied by rarity, per the Step-1 reconciliation. A management hub (Manage Roster, reachable from the pre/post-battle screen) lets the player spend/undo points per stat with live before/after deltas, and free respec per unit. Verified via headless-browser playthrough: spending points changes a unit's effective stats immediately in the hub, those changes carry into the next battle's in-combat maxHP/ATK/etc., respec correctly refunds points (including the SPD soft-cost math), and it all survives a page reload.
- ✅ **Step 3 — Equipment + substats.** 6 typed slots (Weapon/Armor/Emblem fixed-main ATK%/HP%/DEF%; Boots/Charm/Relic choosable-main) per spec §5.1. Gear values for ATK/HP/DEF/POT/RES are %-of-base, same convention as allocation — SPD gear is a flat add, matching spec. Substat pool includes `DualAttackChance` per the locked decision, rolled per the §5.2 ranges, with gear rarity (C/R/E/L) driving substat count (1→4, spec §5.3). The §5.2 budget guard is enforced at stat-computation time: gear's contribution to any of the 6 core stats is capped at 40% of that unit's *allocated+base* value (so the cap grows as a unit levels), verified directly — a piece set that rolled +84% raw ATK was correctly clamped to the intended +40%. CritRate/CritDmg/DualAttackChance are gear-native (outside the 6-stat allocation model per spec §3) and left uncapped. The hub's per-stat rows now show alloc% and gear% as separate live deltas, with a `(capped)` flag when the guard engages. No crafting (Step 6) or drops (Step 5) yet — the hub has a placeholder "Generate Sample Piece" button so equip/unequip is testable now; it gets replaced, not extended, once Forge/drops land. Verified via headless-browser playthrough across 4 full battles with gear equipped throughout — no regressions to combat, no console errors, and gear/equip state survives a page reload.
- ⬜ Steps 4–8 remain (run/escrow structure, enemy scaling + drops, crafting MVP, profile viewer, playtest pass).

## NEXT SESSION STARTS HERE
**Deliverable:** Step 4 of `progression_prototype_handoff.md` — run structure: attrition + escrow (spec §10.1–10.2, §13).

- Dungeon select screen (5 entries; stub the per-dungeon scaling numbers for now — that's Step 5).
- A run = 10 sequential battles. **HP + cooldowns carry across all 10** (attrition) — cooldowns don't currently persist between battles at all (Step 1–3 only carried HP), so this is new plumbing, not just an extension. No heal between fights; leave the spec's battle-5 rest valve OFF by default as a one-line toggle.
- Drops go to a **temporary run inventory (escrow)**, separate from the permanent `roster`/`gearInventory` state. Clear battle 10 → commit escrow to permanent. Lose any battle → wipe escrow, restart the dungeon at battle 1. Levels/gear brought *in* persist regardless of run outcome — only the *run's own* loot and position are at stake.
- Playable checkpoint: a full run that can be won (commit) or lost (wipe + restart), with attrition visibly biting by the later battles.

Note there's no drop *content* yet (no materials/gear tables — that's Step 5), so Step 4's escrow will mostly hold placeholder/empty drops until then; the structural win/lose/commit/wipe loop is what this step proves.

**Reminder for whenever full playtest lands (§16):** the derivation in this session's log found only the Legendary rarity's natural "max primary stat then max secondary" allocation lands both stats in the spec's "balanced spread → 40–60%" band; lower rarities land below it by construction (the hard 2.5× combined ceiling doesn't leave room for more). Worth a specific playtest read on whether that reads as intended specialist/generalist texture or as lower rarities feeling flat.

**The process lesson still holds:** playtest each step before the next. Don't build Steps 3+ until Step 2's allocation moment is confirmed to feel good, not just to compute correctly.
