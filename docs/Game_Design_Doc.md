# Game Design Document — v0.2

*A top-down 2D sandbox life-sim/roguelike (Elin-inspired) fused with a Momentum-based gacha JRPG (Epic Seven / FFBE-inspired).*

> **Authority note (read first):** This is the **vision + not-yet-built-half** document. For any
> detail about **combat, the roster, rarity, affinities, or the effect system**, the authoritative
> sources are **`PROJECT_CONTROL.md`** (the LOCKED decisions list) and the **data files**
> (`roster.json`, `effects.json`) — not this doc. Where this doc and PROJECT_CONTROL disagree,
> PROJECT_CONTROL wins. This GDD exists to hold the whole vision in one place, especially the
> **sandbox half that hasn't been specced or built yet.**
>
> **What's real vs. vision, as of this version:** Combat engine, the full 100-unit roster, the
> rarity system, the affinity wheel, and the effect glossary are **built as data / specced**
> (see the data files). The progression/rewards layer is **mid-build**. The **overworld sandbox
> half — town, farming, breeding, crafting depth, summoning ritual — is still vision**, not yet
> specced. This doc flags each section accordingly.

---

## 1. The One-Sentence Pitch

You live a life in a chaotic procedural world — build a town, farm, craft, capture and breed creatures, explore scaling dungeons — and when combat happens, the game shifts into a deep turn-based tactical battle where your recruited roster fights across attrition-based dungeon runs.

## 2. The Core Design Problem (read this first)

Elin and gacha JRPGs pull in opposite directions, and the whole project lives or dies on how you resolve this:

- **Elin** is single-player. *You* are the protagonist. Companions are things you *raise* over time. No monetization loop; the reward is emergent freedom.
- **Gacha JRPGs** are collection games. The *roster is the content*. Progression is horizontal (more units) and the economy is built to sell pulls.

**The reconciliation:** the two loops share one currency of value — *the units you acquire*. Elin's recruit/summon systems ARE your "gacha roster." Summoning is reframed as an **earned ritual**, not a cash shop. You keep the dopamine of the pull (rarity, pity, banners, shiny reveals) while the "currency" is earned through play, not bought. You can always add real monetization later; you can't easily add soul later.

## 3. The Two Loops

### Loop A — The Overworld (Elin DNA) — ⬜ VISION, not yet specced/built
Top-down, tile-based, real-time-with-pausing sandbox. Pillars:

- **Radical freedom / use-based skills.** No class lock. Skills level by doing (swing swords → sword skill; cook → cooking). The spine of the sandbox.
- **Town-building with autonomous NPCs.** Place buildings, attract citizens, assign jobs; the town runs itself and generates passive resources. The parallel progression track to combat.
- **Creature/unit acquisition + growth.** The bridge that turns overworld activity into combat-roster power (summoning ritual + whatever recruit/breed systems we land on later).
- **Deep crafting & survival.** Weapons, armor, food, potions, furniture. High-skill crafting rivals dungeon loot.
- **Procedural scaling dungeons.** Level-scaled; the primary source of combat encounters, materials, and rewards.

> *Status:* none of Loop A is specced yet. It's the next major frontier AFTER the combat +
> progression + roster spine proves fun. Do not build it early (per the vertical-slice discipline).

### Loop B — Tactical Combat (Epic Seven / FFBE DNA) — ✅ BUILT/SPECCED
When a "real" fight triggers, combat is a dedicated turn-based battle with a party of ~4 units.
**This loop is specced and the core is playtested.** Authoritative detail lives in
`combat_slice_spec.md`, `progression_slice_spec.md`, `roster.json`, and `effects.json`. Summary of
the LOCKED mechanics:

| System | Rule (LOCKED) |
|---|---|
| **Momentum gauge** | Turn order driven by a per-unit Momentum gauge (was "Combat Readiness/CR"). Fills by SPD; at full, the unit acts. |
| **Speed (SPD)** | Determines Momentum fill rate. High SPD = more frequent turns. |
| **Momentum manipulation** | Push enemy Momentum down / pull ally Momentum up / steal / setback. The tactical heart. |
| **Affinity wheel** | 5 affinities as a TYPE chart (see §Roster). Advantage = **+15% Crit Rate & +15% Potency** on that action (not a flat damage multiplier). |
| **Dual/assist attacks** | Off-turn ally chip-in chance (lives as the `DualAttackChance` gear substat). |
| **Potency vs. Resolve** | Debuff application is a contest: `chance = skill_base × (1 + POT − RES)`, clamped [0.05, 1.00]. |
| **Effect economy** | A full canonical glossary of **94 buffs/debuffs/DoTs/controls/instants/specials** (`effects.json`). Team-building is about effect interplay, not just big numbers. |
| **Cooldowns** | Ultimates gated by per-unit cooldown, not a resource meter. |
| **6-stat model** | HP / ATK / DEF / SPD / POT / RES (+ derived CritRate/CritDmg). Same model for units & enemies. |
| **Damage** | `mitigated = raw × K/(K+DEF)`, **K = 1000** (playtested). |
| **Run structure** | 5 dungeons × 10 attrition battles (10th = boss); escrow loot, commit-on-clear, wipe-on-loss. |

### The Bridge Between Loops — partly locked, partly vision
- **Shared stat model.** Overworld-derived traits map onto the same 6-stat combat model. *(Model locked; the overworld feeders that fill it are still vision.)*
- **Town buildings buff the combat roster.** Town-building feeds combat power. *(Vision.)*
- **Crafted gear equips onto combat units.** Overworld crafting = combat itemization (6 slots + substats — the itemization side is specced in `progression_slice_spec.md`; the crafting-depth side is a later reach).
- **"Summoning" = an earned ritual.** Spend earned materials to pull from banners — pity, rate-up, all the gacha feel, none of the wallet. *(Vision — the collection loop, deferred per build order.)*

## 4. Monetization Stance — LOCKED

**Single-player, non-predatory.** No real-money pulls, no energy gates, no FOMO banners, no power-creep treadmill. Summon dopamine is a *design* mechanism powered by *earned* currency, not a wallet. Single-player is a feature: the collection can be *completed*. Optional later: cosmetic-only skins / decor. Never power.

## 4b. Theme — LOCKED (updated model)

**Goal:** treat the sacred with dignity — awe, stewardship, moral weight — reverent by design. Religion-agnostic under the hood so the theme is a *skin* over solid mechanics.

> **IMPORTANT CORRECTION (supersedes the old v0.1 "virtue = unit" model):**
> The roster is built on **affinity as a TYPE, with unit identity independent of it.** The old GDD
> conflated "a virtue" with "a unit" (implying one Patience unit, one Charity unit, etc.). That is
> **retired.** The live model:
> - **Affinity = the unit's combat TYPE** (its place on the wheel + kit archetype). Reusable.
> - **Unit = an independent named character** that *has* an affinity. Many units share one affinity.
> - The 5 affinities are **colors on a wheel**, not virtues: Judgment (Red), Life (Green),
>   Revelation (Blue), Majesty (Gold), Mystery (Dark). (Names are religion-agnostic placeholders.)
> - The old virtue table (Patience/Charity/Diligence/…) survives only as **kit-flavor inspiration**
>   for individual units, NOT as the roster's structure.

**Tier ladder = flavor, not naked power rank.** Rarity (3★/4★/5★) buys flexibility + stat multiplier + passive potency, not "permission to matter" (see §4c). Balance handled by the units underneath so a lower rarity never reads as "lesser."

**Known audience reality:** a game centered on the sacred lands differently for different players. Eyes-open direction decision, not a bug.

### Roster structure (LOCKED — see `roster.json` for the data)
- **100 units:** Judgment/Red 25 · Life/Green 25 · Revelation/Blue 25 · Majesty/Gold 12 · Mystery/Dark 13.
- **Wheel:** Red→Green→Blue→Red (triangle); **Gold↔Dark** mutual advantage; **Gold & Dark are off-wheel** (never penalized vs RGB, only interact with each other — must stay *sidegrades*, not upgrades).
- **Color identities:** Red = aggression · Green = outlast/sustain · Blue = control/tempo/precision · Gold = command/permanence · Dark = sacrifice/risk. The wheel bleeds into kits (Red punishes healing, Blue answers aggression, Gold's permanence beats strip, Dark's Wasting/bomb pressure beats Green's sustain).
- **3 rarities:** Common(3★)/Epic(4★)/Legendary(5★), multipliers 1.00/1.25/1.50, points/level 3/4/5. Distribution 29 Leg / 35 Epic / 36 Common (per-affinity Legendaries 7/7/7/4/4).
- **Every unit has 3 passives**; rarity sets passive *potency*, not count. Unlock mechanic parked (all unlocked for now).

## 4c. "Every Unit Stays Valuable" — DESIGN PILLAR (LOCKED)

Single-player frees us from needing weak units to sell strong ones.

**Rarity buys flexibility + stats + passive potency, NOT permission to be useful.** Higher rarity = *generalists* who slot anywhere; lower rarity = *specialists* irreplaceable in their niche.

Supporting mechanisms:
1. **Niche keys.** A Common is the *only* answer to a specific mechanic (e.g. a specific cleanse, a DEF-shred, an anti-speed tool).
2. **No duplicate-shredding.** Dupes unlock new roles/kits/promotion paths — every copy is a character, not fodder.
3. **Town economy as equalizer** *(vision).* Buildings buff units, elevating "weak" units into viability.
4. **Constraint content.** Some dungeons restrict which affinities you may bring, forcing the whole roster into rotation — and (critically) keeping off-wheel Gold/Dark from being the universal safe pick.

## 5. Tech Stack

- **Production engine: DEFERRED** (Godot 4 vs Unity — a late, reversible choice). Not committed.
- **Prototype tool:** throwaway **browser / HTML5 canvas** for feel + math validation only. A good browser prototype does NOT validate the engine choice.
- **Data-driven is mandatory and now real:** `roster.json` and `effects.json` are the canonical data spine; units/abilities/effects are data, not hardcoded.

## 6. Realistic Scope — Build Order

Vertical slices, playtest each before speccing the next:

1. **Combat prototype.** ✅ Built & playtested (Momentum, 4 units, kits, one enemy team).
2. **Progression/rewards layer.** 🔄 Mid-build — persistence done; allocation math (Step 2) paused awaiting a numbers sanity-check. (`progression_slice_spec.md`)
3. **Roster + effect system as data.** ✅ 100 units + 94-effect glossary authored (`roster.json`, `effects.json`). The kit rework onto the glossary is **done** — carried through the v0.3 audit and the v0.4/v0.5/v0.6 passes (see `PROJECT_CONTROL.md`). *(The old pointer to `HANDOFF_roster_ability_audit.md` is retired; that handoff's work is complete and the file is not in this repo.)*
4. **The bridge (one creature/summon → roster → battle).** ⬜ Vision.
5. **Minimal overworld loop** (one town tile, one building, one recipe, one dungeon feeding combat). ⬜ Vision.
6. **Summoning ritual + banners** (the collection loop). ⬜ Vision.
7. **Content scaling.** ⬜ Only once systems are proven fun.

## 7. Open Questions To Decide Next

*(Several former open questions are now LOCKED — see PROJECT_CONTROL. Remaining:)*
- **Passive unlock mechanic** — how a unit's 3 passives come online (milestone / capstone / investment). Parked; all unlocked for now.
- **Permadeath** — likely resolution: the overworld body can fall, the roster persists. Not finalized.
- **Overworld combat trigger** — trivial fights resolve real-time (Elin-style), only "real" fights go to the tactical screen. (Recommended, not locked.)
- **Economy currencies** — the multi-system wealth spine that powers the summon ritual. Unspecced.
- **Async "lite PvP"** — DECIDED direction: players upload teams that become AI defense teams others fight as PvE (sidesteps netcode/cheating). Open: what rewards/ranking wrap it without FOMO.

*Already RESOLVED (moved to LOCKED in PROJECT_CONTROL): combat units = separate summoned roster; run-based escrow + attrition; full min-max progression; affinity = type not unit; 3-tier rarity; the effect system.*

---

*Where to look:* **PROJECT_CONTROL.md** = open first, the authority + session handoff · **combat_slice_spec.md** = combat detail · **progression_slice_spec.md** = levels/gear/dungeons/runs · **roster.json / roster.xlsx** = the 100 units · **effects.json / effects.xlsx** = the effect glossary · **this doc** = the whole vision, especially the un-built sandbox half.
