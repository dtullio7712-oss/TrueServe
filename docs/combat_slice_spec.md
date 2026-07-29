# combat_slice_spec.md — Playable Combat Vertical Slice (v0.1)

> **Purpose of this file.** A hand-to-implementation spec for the *first playable fight*: 4 player units vs. one enemy team, resolved on a dedicated turn-based screen. This is the first thing built and the first thing playtested. It is deliberately **basics-first**: enough to prove the fight is *fun and feels good*, not a finished combat system. Refine after playing.
>
> **Anchored to locked decisions** (PROJECT_CONTROL): single-player / non-predatory; roster = original virtue-embodiments; every unit stays valuable; feel-first / fidelity-later; combat built & playtested before other systems are specced.
>
> **Provenance note.** Two mechanics here — the ultimate meter and the affinity wheel — are lifted and adapted from the Jan 2026 "Angels" design bible, which was otherwise superseded (it was a monetized F2P game with named biblical figures as the roster). The reusable *mechanics* are carried forward; the monetization and named-saint roster are not.

---

## 0. Naming (placeholders — find-replace later, mechanics don't depend on them)

Two separate gauges. They must never share a word, or playtesters and implementers will conflate them.

| Concept | Name used in this spec | Alternates (swap the word, keep the mechanic) |
|---|---|---|
| Per-unit turn-order gauge (fills by Speed) | **Momentum** | Tempo, Cadence, Impetus, Drive |
| Ultimate gating (per unit) | **Ult cooldown** (turn-based) | — |
| The five affinities | **Judgment / Life / Revelation / Majesty / Mystery** *(Jan placeholders)* | To be renamed religion-agnostic later; mechanics are affinity-shaped, not name-dependent |

> **Shelved:** an earlier draft used a team-shared **Glory** meter (fills on damage, powers ults). Parked for now in favor of simpler per-unit ult cooldowns — see §2. May return downstream as a team-tempo layer.

**One-line mental model:** *Momentum decides **who** acts; a unit's **cooldown** decides when it can unleash its ult again.*

---

## 1. The Combat-Readiness Turn System (Momentum)

Turn order is **not** fixed rounds. Each unit has a Momentum gauge (0 → 100). Every "tick," each unit gains Momentum proportional to its Speed. First unit to reach 100 acts, spends its Momentum, and the loop continues. This is the E7/FFBE-style CR system and it is the tactical spine.

### 1.1 Fill formula
On each tick, for every living unit:

```
momentum += SPD * TICK_RATE
```

- `TICK_RATE = 0.07` (tuning constant; start here, tune in playtest).
- With SPD ~110–125 (see roster), a unit crosses 100 in ~11–13 ticks. Ticks are instant/simulated — the player sees the turn-order bar advance, not literal timesteps.
- When a unit acts, its Momentum resets: `momentum -= 100` (carry the overflow, don't zero it — overflow carry keeps fast units feeling fast and makes CR-manipulation math clean).

### 1.2 Turn-order display (required for the slice)
A horizontal **turn-order track** at the top of the battle screen showing the next ~6 acting units as portraits, left = soonest. Recompute and re-render whenever any Momentum value changes (including from a push/pull). This readout **is** the tactical interface — without it, CR control is invisible and the fight feels random. Do not ship the slice without it.

### 1.3 CR manipulation (the skill ceiling)
Skills can move Momentum directly. This is the heart of the tactic.

- **Push** (enemy): `target.momentum -= PUSH_AMOUNT` (e.g. 30% of a full bar = `-30`). Delays their turn.
- **Pull** (ally): `ally.momentum += PULL_AMOUNT`. Advances their turn.
- Momentum clamps to `[0, 100]` *after* a manipulation resolves; a push that would exceed −100 just floors at 0 (no "negative turn debt" in the slice — keep it legible).

**Slice requirement:** at least one unit (Diligence) must have a pull, and the enemy or one unit must demonstrate a push, so the mechanic is felt in the first fight.

---

## 2. Ultimate Gating — Per-Unit Cooldowns

Ultimates (S4) are gated by a **per-unit, turn-based cooldown** — no shared resource. Simple, legible, and easy to tune in a first slice.

- Each ult has a **cooldown of N turns** (defined per unit below). "Turns" = the unit's *own* turns, counted down by 1 each time that unit acts.
- An ult is **available at the start of the fight** (cooldown 0), then goes on cooldown when used.
- Display: show a small number/pip on the unit's ult button = turns remaining. When it's ready, the button lights up. The player must be able to *see* who has an ult up — this is part of the tactical read alongside the turn-order track.

> **Design intent:** cooldowns keep ults as *punctuation*, not spam, and make turn-order planning matter — you're steering the fight toward the moment your key ult comes back up *and* that unit reaches the front of the Momentum track. Diligence (which pulls Momentum) is the tool for making those two clocks line up.
>
> **Shelved alternative — team "Glory" meter.** A team-shared gauge that fills on damage and powers ults was drafted and set aside. If cooldowns feel too flat in playtest, Glory is the first thing to try layering back in. The "Gloria" victory flavor (§6.4) stays regardless.

---

## 3. The Four-Unit Slice Party (full kits)

Each unit has the locked **4-skill structure** carried from the Jan bible: **S1 basic active, S4 ultimate (cooldown-gated), S2 & S3 flexible active-or-passive.** A virtue defines *what the skills do*; the slot structure is fixed. Each unit's ult lists its **cooldown (CD)** in turns.

Party identity: three enablers + one conditional finisher. **Diligence builds, Patience/Charity sustain, Justice cashes in.**

### 3.1 Diligence — the Momentum engine (affinity: Revelation)
The tempo controller. Rewards steady small actions; bends both gauges.

| Slot | Type | Name | Effect |
|---|---|---|---|
| S1 | Active | Steady Strike | ATK ×1.0 single. On hit: **pull self +6 Momentum** (small self-tempo bonus, reinforcing the engine identity). |
| S2 | Active | Quicken | **Pull an ally +25 Momentum.** CD 3. The signature enabler. |
| S3 | Passive | Persistence | Each of Diligence's own turns: **+5% ATK, stacking**, no cap decay in-fight. Small per turn, large by turn 8+. |
| S4 | Ult | Industry | Full team **+20 Momentum** and **+15% Potency, 2 turns.** Sets up the finisher. **Ult CD 4.** |

### 3.2 Patience — scales over time (affinity: Mystery)
Weak turn 1, dominant turn 10. The team's late-game insurance.

| Slot | Type | Name | Effect |
|---|---|---|---|
| S1 | Active | Forbearance | ATK ×0.8 single. |
| S2 | Passive | Endure | At the **start of each of Patience's turns, gain a Forbearance stack**: +6% ATK and +4% DEF per stack (no cap in the slice — see §7 open Q). |
| S3 | Active | Long Game | Consume all stacks: ATK ×(1.0 + 0.4×stacks) single-target nuke. CD 4. The payoff button. |
| S4 | Ult | The Meek Inherit | ATK ×(2.0 + 0.3×stacks) AoE. Scales with everything Patience has banked. **Ult CD 5.** |

### 3.3 Charity — redirect / transfer (affinity: Life)
Strength = what it gives away. Keeps the team alive while stacks grow.

| Slot | Type | Name | Effect |
|---|---|---|---|
| S1 | Active | Offering | ATK ×0.7 single + heal lowest-HP ally for 50% of damage dealt. |
| S2 | Active | Bear the Burden | For 2 turns, **redirect 50% of all damage** targeting allies onto Charity. CD 4. |
| S3 | Passive | Grace | Whenever Charity is healed, **10% of that healing overflows** to the lowest-HP ally. |
| S4 | Ult | Selfless Vigil | **Transfer Charity's own buffs to the team** and grant team a shield = 30% of Charity's max HP. **Ult CD 4.** |

### 3.4 Justice — conditional finisher (affinity: Judgment) — *the pick*
Chosen over "Zeal" deliberately: the other three set up, Justice closes. It is strong **only** into targets the team has already softened, so it's the payoff for the setup loop rather than a standalone carry. Also avoids the wrath/violence tonal edge that "Zeal" flirts with — important under the reverence pillar.

| Slot | Type | Name | Effect |
|---|---|---|---|
| S1 | Active | Verdict | ATK ×1.1 single. |
| S2 | Active | Weigh the Scales | Apply **Defense Break (−40% DEF, 2 turns)** to target. Contest of Potency vs. Resolve (see §4.3). CD 3. |
| S3 | Passive | The Guilty Fall | Justice deals **+50% damage to enemies suffering any debuff** (Def Break, burn, etc.). This is the whole identity — turn setups into kills. |
| S4 | Ult | Final Judgment | ATK ×4.0 single-target; **ignores DEF** if target is debuffed. The team's win condition. **Ult CD 4.** |

---

## 4. Damage, Crits, and the Potency Contest

### 4.1 Core stats (Lv-relevant, per roster sheet)
`HP, ATK, DEF, SPD, CRIT Rate, CRIT DMG, Potency (POT), Resolve (RES)`.

*(Potency = how forcefully your debuffs land; Resolve = the will to shrug them off. Renamed from E7's "Effectiveness / Effect Resistance.")*

### 4.2 Damage formula
```
raw       = skill_multiplier * ATK
mitigated = raw * (1000 / (1000 + DEF))      # DEF softcap curve — tune 1000
crit?     = roll < CRIT_Rate  → mitigated *= (1 + CRIT_DMG)
affinity  = apply advantage/disadvantage (see §4.4)
final     = mitigated * random(0.95, 1.05)   # small variance for texture
```
- `1000 / (1000 + DEF)` gives diminishing returns on DEF; at DEF 1000, damage is halved. Adjust the constant to taste in playtest.

### 4.3 Debuff application = a contest (not automatic)
Carried from the Jan doc's stat philosophy — this is what makes Potency/Resolve a real axis:
```
apply_chance = skill_base_chance * (1 + caster_POT - target_RES)
```
- Clamp to `[0.05, 1.0]` (debuffs never fully guaranteed nor fully impossible — keeps RNG texture).
- Example: Justice's Def Break at `skill_base 1.0`, caster POT 0.20, target RES 0.30 → 90% apply chance.

### 4.4 Affinity wheel (Jan placeholders, mechanics final)
```
Judgment → Life → Revelation → Judgment      (3-cycle, each beats the next)
Majesty ↔ Mystery                            (mutual weakness pair)
```
On **advantage**, attacker gets **+15% CRIT Rate** and **+15% Potency** for that action (adapted from Jan doc). On **disadvantage**, the inverse penalty. **Deliberately not a flat damage multiplier** — it's a hit-quality/reliability swing (crits land more, debuffs stick more), which is more nuanced and less snowbally. *(Note: Jan's version buffed the attacker's Effect Resistance on advantage, which is defensive and reads oddly on an attack; swapped to Potency so advantage means "your effects land harder." Revisit in playtest.)*

Slice party covers Judgment/Life/Revelation/Mystery; the dummy enemy team should include at least one unit each of Life and Revelation so advantage/disadvantage is *felt* by the player in fight one.

### 4.5 Buff/debuff economy (minimum viable set for the slice)
Only these need to exist for fight one: **Def Break, ATK Up, DEF Up, Potency Up, Shield, Momentum push/pull, Forbearance stack.** Everything else is later content.

---

## 5. The Enemy Team & Win/Loss

- **One enemy team of 3–4 units**, hand-authored (not procedural yet). Include Life + Revelation affinities (see §4.4) and one unit that **pushes** player Momentum (so the player feels CR control used *against* them).
- Enemy AI for the slice = **priority list**, not intelligence: (1) ult if off cooldown, (2) debuff the lowest-DEF target, (3) focus lowest-HP player unit, (4) basic attack. Legible and beatable is the goal.
- **Win:** all enemies at 0 HP → **Gloria / victory beat** (see §6).
- **Loss:** all player units at 0 HP. For the slice, loss just returns to a restart prompt — the "hooded figure prayer" cinematic and any resource-loss mechanic are **out of scope** here (and the 10%-resource-loss idea from Jan is *not* carried forward pending the non-predatory review).

---

## 6. Game-Feel & Art Direction (feel-first, fidelity-later)

**This section is as important as the math.** A mechanically-correct fight that feels like clicking spreadsheet cells is a failed slice. All of the below layers onto **placeholder art (rectangles/sprites)** — prove the fight is fun *juicy* before any real art exists.

### 6.1 The juice checklist (build these on placeholders)
- **Hit-pause / freeze-frame:** 60–120ms freeze on impact of every hit; longer (~200ms) on crits and ults. Single highest-ROI feel trick — do it first.
- **Screenshake:** small on normal hits, pronounced + directional on ults. Cap it so it reads as impact, not nausea.
- **Impact flash:** target flashes white for 1–2 frames on hit; red tint on taking a crit.
- **Number pop:** damage numbers scale-punch out and arc; crits bigger + different color; heals green, floating up.
- **Momentum-bar telegraph:** when a push/pull fires, the turn-order track visibly *slides* the portrait to its new slot (animated, ~250ms) — the player must *see* the tactic land.
- **Ult moment:** brief zoom/vignette, time-dilation on the rest of the board, distinct sound. The one moment per fill that earns "impactful."
- **Sound:** every action needs a hit sound, a whiff sound, a heal chime, an ult sting. Placeholder SFX are fine; *silence* is what kills feel.

### 6.2 The "blessing" feedback beat
From the control doc's "cool rain over a hot head" note — a positive, restorative sensory beat when the team heals/shields/revives: a soft light-wash + rising chime over the affected units. It's the reverence pillar expressed as *game feel*, and it should feel as good to land as a hit does.

### 6.3 Cohesion note (carry into art later)
Overworld will be *simpler* 2D, combat *more substantial* — but shared palette + design language + an intentional overworld→combat transition, so the fidelity gap reads as **stylized**, not **unfinished**. Not built in the slice; flagged so the transition isn't an afterthought.

### 6.4 Victory beat
On win: brief unison "exaltation" pose + light bloom + choral sting (the "Gloria" moment, carried from Jan as flavor, stripped of monetization). Keep it short — 2–3 seconds — it's a reward, not a cutscene.

---

## 7. Open Questions This Slice Deliberately Defers

- **Stack caps.** Patience (Endure) and Diligence (Persistence) stack uncapped in the slice — playtest will reveal if a fight runs long enough for this to break. Add caps only if needed; the point is to *feel* the scaling first.
- **Same roster or separate?** The biggest open fork (combat units = overworld character+pets, or a separate summoned roster) is *not* resolved here. The slice treats the four as an abstract party; it works under either answer. Note: the Jan material silently assumed "separate summoned roster."
- **Tuning constants** (`TICK_RATE`, DEF softcap 1000, ult cooldown lengths, `PULL/PUSH` amounts) are all first-guesses. They *are* the playtest.
- **Permadeath / loss stakes:** out of scope for the slice; loss = restart.

---

## 8. Definition of Done for the Slice

**Target environment: a throwaway browser prototype (HTML5 canvas).** Not the production engine — this artifact exists only to answer "is the fight fun?" as cheaply and fast as possible. It is expected to be discarded once it has answered that question. Do not invest in structure, save systems, or reusability beyond what's needed to playtest.

The slice is done when a player can:
1. Enter one fight, 4 units vs. one enemy team.
2. See a live turn-order track driven by Momentum, and watch a push/pull visibly reorder it.
3. Use a unit's ultimate, see it go on cooldown, and use it again once ready.
4. Apply a debuff via the Potency-vs-Resolve contest and see Justice punish it.
5. Win to a short Gloria beat or lose to a restart.
6. **And it feels good** — hit-pause, shake, flash, sound, number-pop all present on placeholder art.

If 1–5 work but 6 doesn't, the slice has **failed its actual purpose.** Fun and feel are the deliverable; the math is just what makes them possible.
