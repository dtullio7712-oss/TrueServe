# Untitled Project — Design Document v0.2

*A top-down 2D sandbox life-sim/roguelike (Elin-inspired) fused with a Combat-Readiness gacha JRPG (Epic Seven / FFBE-inspired).*

---

## 1. The One-Sentence Pitch

You live a life in a chaotic procedural world — build a town, farm, craft, capture and breed creatures, explore scaling dungeons — and when combat happens, the game shifts into a deep turn-based tactical battle where your recruited companions and bred creatures fight as a summonable roster.

## 2. The Core Design Problem (read this first)

Elin and gacha JRPGs pull in opposite directions, and the whole project lives or dies on how you resolve this:

- **Elin** is single-player. *You* are the protagonist. Companions are things you *raise* over time. There is no monetization loop; the reward is emergent freedom.
- **Gacha JRPGs** are collection games. The *roster is the content*. Progression is horizontal (more units) and the economy is built to sell pulls.

**The reconciliation this doc assumes:** the two loops share one currency of value — *creatures and people you acquire*. Elin's capture/breed/recruit systems ARE your "gacha roster." Summoning is reframed as **recruitment/binding rituals**, not a cash shop. You keep the dopamine of the pull (rarity, pity, banners, shiny reveal animations) while the "currency" is earned through play, not bought. This makes it a *serious* game rather than a monetization vehicle. You can always add real monetization later; you can't easily add soul later.

Decide this now, because it dictates everything below.

## 3. The Two Loops

### Loop A — The Overworld (Elin DNA)
Top-down, tile-based, real-time-with-pausing sandbox. Pillars:

- **Radical freedom / use-based skills.** No class lock. Skills level by doing (swing swords → sword skill; cook → cooking). This is the spine of the sandbox and should be preserved faithfully.
- **Town-building with autonomous NPCs.** Place buildings, attract citizens, assign jobs; the town runs itself and generates passive resources. This is the parallel progression track to combat.
- **Creature capture + breeding + gene-modification.** The single most important bridge system — captured/bred creatures become combat units. Breeding combines parent traits; gene-mod alters specific stats/resistances/abilities. This is your roster-crafting layer.
- **Deep crafting & survival.** Weapons, armor, food, potions, furniture. High-skill crafting rivals dungeon loot.
- **Procedural scaling dungeons ("Nefia"-equivalent).** Level-scaled, the primary source of combat encounters, materials, and recruitable/capturable units.

### Loop B — Tactical Combat (Epic Seven / FFBE DNA)
When an overworld encounter triggers a "real" fight (boss, raid, dungeon floor guardian, arena), transition to a dedicated turn-based battle screen with a party of ~4 units.

Core mechanics to implement:

| System | Rule |
|---|---|
| **Momentum bar** (turn-order gauge) ✅ | Turn order driven by a per-unit Momentum gauge, not fixed turns. Units fill Momentum passively; at 100% they act. *(Formerly "Combat Readiness / CR." Renamed to Momentum — the mechanic is unchanged; "CR-control" verbs become "push/pull Momentum." Placeholder name; Initiative is the alternate.)* |
| **Speed stat** ✅ | Determines rate of Momentum gain. High speed = more frequent turns. |
| **Momentum manipulation** ✅ | Skills that push enemy Momentum down or pull ally Momentum up. This is the tactical heart — Momentum control is the skill ceiling. |
| **Elemental advantage** ✅ | Rock-paper-scissors elements modifying hit quality (E7 uses ±15% on advantage/disadvantage). Kept nuanced — a crit-rate / Potency swing (crits land more, debuffs stick more), not a flat damage multiplier. |
| **Dual / assist attacks** ✅ | Chance for an off-turn ally to chip in on a basic attack. Adds RNG texture and roster synergy. **Gearable:** players can build *into* dual-attack chance as a stat/substat, making it a deliberate teambuilding axis, not just ambient RNG. |
| **Ult cooldowns** (per unit) ✅ | Ultimates (S4) are gated by a per-unit, turn-based cooldown — a unit uses its ult, then can't again for N of its own turns. Simple and legible. *(Replaces the earlier team-shared "Glory meter" resource — see shelved note below.)* |
| **Potency vs. Resolve** | Debuff application is a contest: `chance = skill_base × (1 + caster_Potency − target_Resolve)`. Gives a whole stat axis beyond raw damage. *(Potency = how forcefully your effects land; Resolve = the will to shrug them off. Renamed from E7's "Effectiveness / Effect Resistance.")* |
| **Buff/Debuff economy** | Defense break, attack up, Momentum boost, immunity, etc. Team-building is about buff/debuff interplay, not just big numbers. |
| **Skill cooldowns** (S2/S3) | Non-ult actives also run on cooldowns, so kits have rhythm — you're not spamming your best button every turn. |

### The Bridge Between Loops
This is where your game is genuinely novel. Ideas:

- **Bred/gene-modded creatures carry their traits into battle.** A gene-mod that adds fire resistance in the overworld = fire resistance stat in combat. The two systems share one stat model.
- **Town buildings buff your combat roster.** A training hall raises a unit's speed cap; a shrine improves summon rates. Town-building feeds combat power — closing the Elin loop into the JRPG loop.
- **Crafted gear equips onto combat units.** Overworld crafting = combat itemization (E7-style gear with substats).
- **"Summoning" = a town ritual building.** You spend materials earned from farming/dungeons to pull from banners of recruitable heroes/creatures. Pity counter, rate-up banners — all the gacha feel, none of the wallet.

## 4. Monetization Stance — DECIDED

**Single-player, non-predatory.** No real-money pulls, no energy gates, no FOMO banners, no power-creep treadmill. The dopamine of the summon is a *design* mechanism (rarity reveals, pity counters, banners) powered by an *earned* currency from the town economy — not a wallet. Single-player is a feature here: the collection can actually be *completed*, the summon becomes a *reward for building a good town*, and the two loves (collection + economy) reinforce each other directly. Optional later: cosmetic-only skins / town decor. Never power.

## 4b. Theme — DECIDED (v0.1)

**Goal:** a game that treats the sacred with dignity — awe, stewardship, moral weight — rather than as monster-fodder. Reverent by design.

**The roster is human virtue-embodiments, not named real figures.** Each collectible unit *embodies a virtue*, and that virtue IS its combat identity (see kit framework below). This gives full creative + balance freedom, and avoids the disrespect of a named saint being "meta trash," losing fights, or being shredded for materials.

**Angels are above the collection layer.** They are rare, un-ownable *interventions / blessings* earned through play — battle-altering events, not units you roll, rank, and bench. This keeps the celestial *above* the roster and preserves awe. (In most Abrahamic tradition, angels are sent by God, not summoned by humans — so we never "summon" them.)

**The tier ladder is a celestial-hierarchy skin, not a naked power ranking.** Degrees of light / proximity to grace as flavor. Combat balance is handled by the units underneath so "B-tier" never reads as "lesser soul."

**Systems stay religion-agnostic under the hood** — an "affinity" system, a "celestial hierarchy" ladder — so the theme is a coherent skin over solid mechanics, not mechanics that only work if the theme does.

**Known audience reality:** even done respectfully, a game centered on the sacred lands differently for different players; some may feel any interactive use is inappropriate, others will love it. Going in eyes-open; this is a direction decision, not a bug.

### Virtue-as-Mechanic kit framework
The virtue determines the mechanic. Starter sketches:

| Virtue | Combat identity |
|---|---|
| **Patience** | Scales up the longer the fight runs (per-turn stacks). Weak turn 1, dominant turn 10. |
| **Charity / Sacrifice** | Redirects damage off allies, transfers own buffs/HP to others. Strength = what it gives away. |
| **Diligence** | The Momentum-engine / resource builder. Rewards steady small actions. (Fuses with town economy.) |
| **Fortitude** | Immovable wall; stronger as its own HP drops. |
| **Temperance** | Control unit; strips enemy buffs, punishes overextension. |
| **Hope** | Comeback / revive unit; strongest when the team is losing. |
| **Humility** | Enabler; amplifies whoever it supports. High ceiling in the right team — "the least exalted through others." |

## 4c. "Every Unit Stays Valuable" — DESIGN PILLAR

Single-player frees us from needing weak units to sell strong ones. Resolution of the rarity-vs-relevance tension:

**Rarity buys flexibility + stats, NOT permission to be useful.** Higher-rarity units are *generalists* who slot anywhere; lower-rarity units are *specialists* who are irreplaceable in their niche. Pulls stay exciting (a new top-tier is a flexible powerhouse); the bench stays permanently relevant (that low-tier is still the only answer to certain fights).

Supporting mechanisms:
1. **Niche keys.** A low unit is the *only* cleanse for a specific debuff / counter to a specific mechanic.
2. **No duplicate-shredding.** Dupes unlock *new roles/kits/promotion paths* for that unit — every copy is a character, not fodder. (Also the respectful choice.)
3. **Town economy as equalizer.** Buildings buff units, so a well-built town elevates a "weak" unit into viability. Economic depth = roster depth.
4. **Constraint content.** Some dungeons restrict which virtues you may bring, forcing the whole roster into rotation over time. This is how 100 units all get played.

## 5. Suggested Tech Stack

- **Engine:** Godot 4 (free, excellent 2D, GDScript is fast to prototype, C# available). Unity is the alternative if you want more asset-store support.
- **Why Godot for this specifically:** tile-based overworlds, its node system suits turn-based state machines well, and it's friendly for a solo/small team building something this systems-heavy.
- **Data-driven design is mandatory.** Units, skills, items, creatures, gene traits — all defined in data files (JSON/Godot resources), not hardcoded. A systems game like this needs designers to tune hundreds of entities without touching engine code.

## 6. Realistic Scope — Build Order

Do NOT build both full loops at once. Suggested vertical-slice order:

1. **Combat prototype first.** One battle: 4 units, Momentum bar, 3 skills each, one enemy team. Get the turn-based feel *right* before anything else — it's the hardest part to make fun and the easiest to test in isolation.
2. **One creature, capture → roster → battle.** Prove the bridge: capture something in a tiny overworld, have it show up as a combat unit.
3. **Minimal overworld loop.** One town tile, one building, one crafting recipe, one small dungeon that feeds combat.
4. **Breeding/gene-mod.** The roster-crafting depth layer.
5. **Summoning ritual + banners.** The collection loop.
6. **Content scaling.** Only once the systems are proven fun.

A playable, genuinely-fun **combat vertical slice** is your first milestone. Everything else is content on top of proven systems.

## 7. Open Questions To Decide Next

- Is overworld combat *always* the tactical screen, or do trivial fights resolve in real-time (Elin-style) and only "real" fights go turn-based? (Recommend the latter — it respects the sandbox's pace.)
- Are your combat units *the same* as your overworld character + pets, or a separate summoned roster? (This is the single biggest design fork.)
- Permadeath? Elin has roguelike perma-death DNA; gacha games never delete your units. These conflict — pick one, or scope permadeath to the overworld body while the roster persists.
- **Async "lite PvP" — DECIDED direction:** players upload successful teams that become *defense teams* others fight as PvE/AI. Sidesteps netcode, live balancing, and cheating (a cheated team is just a beatable AI, not a ruined ladder). Open sub-question: what rewards/ranking wrap around it without reintroducing FOMO?

---

*Next step: the combat vertical slice is now specced in detail in `combat_slice_spec.md` — Momentum formula, 4 units with full kits (Diligence / Patience / Charity / Justice), cooldown-gated ults, and the Potency-vs-Resolve / damage equations. The next move is to **build and playtest** that slice on placeholder art before speccing further systems.*

---

### Shelved for later (parked, not deleted)
- **Team-shared "Glory" meter.** A team-wide resource that fills on damage dealt/taken and powers ultimates, distinct from Momentum ("Momentum decides *who* acts; Glory decides *when* someone unleashes"). Set aside in favor of simpler per-unit ult cooldowns for the first slice. May return downstream as a second layer if the fight wants a team-level tempo resource. The salvaged Angels-bible "Gloria" flavor still lives on the victory beat regardless.
