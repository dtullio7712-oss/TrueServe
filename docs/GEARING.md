# GEARING SYSTEM — design envelope

Defines the **power envelope and shape** of gear so encounter design and the valuation model have real ground to stand on. This is the design-envelope level, not the full item implementation — enough to kill the model's 1.8× stub and let bosses be tuned against a real power target. Model reference: `power_model_v3.py`. Numbers are dials.

**Lineage:** primarily **Epic Seven / FFBE** (six pieces, sets by count-threshold, %-main-stats, ~4 heavily-RNG substats, **7 gated rarity tiers**, and **FFBE Trust-Master-style unit-earned unique gear**). **Diablo 2** contributes *texture only* — a rarity-ladder feel and the "neat to collect a set" satisfaction — NOT its literal slot/set-matching structure.

---

## 1. Power envelope (kills the 1.8× stub)

Gear is a **major power source (Large / E7-style)** — a fully-geared unit is a fundamentally different creature than a naked one.

- **Total gear multiplier on naked base stats: ~2.5× mid-game, up to ~3× endgame** (across all six pieces combined, main stats + substats + set bonuses).
- Combined with the ~2.5× level/growth ceiling already locked, a fully-invested endgame unit sits well above its level-1 base — but the ~2.5× *hard ceiling per source* discipline still holds (gear is one source, levels another).
- **Model action:** replace `BUILD_MULT = 1.8` (stub) with **~2.5×** as the mid-game default, and add an endgame ~3× column if useful. This is the single most important downstream effect of this doc — it makes every powerscore reflect a geared unit, not a naked one.

---

## 2. The six pieces + sets (E7-style, count-threshold)

**Six gear slots.** (Exact slot names TBD — e.g. Weapon / Helm / Armor / Boots / Ring / Amulet — but slot identity matters less than main-stat pools below.)

**Sets activate by COUNT, not slot-matching** (the E7 model, per owner):
- **4-piece sets** = your build's IDENTITY — the big commitment (Speed, Attack, Crit, Lifesteal, Defense, an effect-set, etc.).
- **2-piece sets** = FILLER bonuses for your remaining two slots.
- A complete build reads as **"4-[identity] + 2-[filler]"** — e.g. *4-Speed + 2-Crit*, *4-Attack + 2-Lifesteal*. You collect *enough pieces* of a set to hit its threshold; you never need the specific matching helm-of-that-set. No slot-locking.
- This is the core teambuilding-via-gear decision: which 4-set defines this unit, and what 2-set rounds it out.

---

## 3. Main stats — deterministic backbone

- Main stats are **% stats** (e.g. +% ATK, +% HP, +% DEF, +% SPD, +% Crit Rate, +% Crit Dmg, +% Potency, +% Res).
- **Static ranges per (rarity × gear level)** — you know what a piece's main stat *will be* within a tight range; upgrading gear level raises it predictably. No RNG on the main stat's identity, only minor roll within the band.
- **Different slots offer different main-stat pools** — so choosing a piece's slot/main-stat is an archetype choice (a boots with %SPD main vs %ATK main is a real fork). This is where you *choose your build's stat spine*.
- Flat-stat mains may exist as low-value options, but **% mains are the intended primary** (per owner) so scaling stays multiplicative and build-defining.

---

## 4. Substats — the grind engine (E7-style)

- **~4 substats per piece.** Heavily **RNG** — the thing you farm hundreds of pieces chasing.
- **Enhancement rolls upgrade an existing substat** (E7 model): every few gear levels, one of the four substats gets a random boost. Perfect gear = the right four substats *and* the rolls landing on the ones you want. This is the optimization treadmill.
- **Wide substat axis variety is mandatory** to fuel the grind — the more meaningful axes, the deeper the chase. Candidate axes:
  - Offensive: % ATK, flat ATK, % Crit Rate, % Crit Dmg, % effect-hit/Potency.
  - Defensive: % HP, flat HP, % DEF, flat DEF, % Res.
  - Tempo: % SPD, flat SPD (SPD is king — keep it a rare/valuable roll, E7-style).
  - Utility: % lifesteal, % healing, cooldown/momentum-adjacent rolls (TBD against the effect system).
- **RNG texture (D2 nod):** gear rarity tier affects substat *count and quality* (rarer pieces roll more/better substats), giving the D2 rarity-ladder satisfaction on top of the E7 roll mechanic.

---

## 5. Set bonuses & the effect-system hook (RECOMMENDATION — reversible)

Owner had no preference on whether sets grant EFFECTS or stay stat-only. **Recommended split** (flagged reversible):

- **Most sets = stat bonuses** (4-Speed = big team/self SPD, 4-Attack = big ATK, 2-Crit = crit rate, etc.). Keeps gear legible and grind-friendly — easy to reason about, easy to farm toward.
- **A handful of the RAREST / hardest-to-farm sets = actual EFFECTS** that hook the combat effect glossary — the aspirational chase that ties gear into the "chess" layer. Candidate effect-sets (all reference real `effects.json` ids):
  - **Ember set** → boosts Burn/DoT (`dot_amp`, longer `burn`) — turns a Red team's whole strategy up a notch.
  - **Piercer set** → grants `ignore_def` / def-pen on attacks — an anti-tank gear identity.
  - **Executioner set** → raises `execute` thresholds or adds execute chance.
  - **Tempo set** → `momentum_pull` on turn / resist `momentum_push` — a speed-team enabler.
  - **Vampiric set** → `lifesteal_buff` scaling — sustain identity.
  - **Detonator set** → `detonate_dot` chance on hit — pairs with DoT teams.

**Why this split:** stat-sets keep the everyday grind clean; effect-sets make gear a *teambuilding decision* (a Burn set literally changes how a unit plays), which is the project's core "chess for chess players" ethos extended into gear — without drowning every piece in mechanical complexity. If we'd rather keep effects purely on kits, drop the effect-sets and sets become stat-only; the rest of the envelope is unaffected.

---

## 6. Rarity ladder — 7 tiers, gated power spikes

**Seven rarity tiers**, each a *felt power spike* (not a marginal step) — the grind backbone that keeps players climbing for hundreds of hours. Proposed ladder (names swappable):

| # | Tier | Feel |
|---|------|------|
| 1 | Cracked | starter junk, barely better than naked |
| 2 | Common | early-game baseline |
| 3 | Fine | first real upgrade |
| 4 | Rare | mid-game workhorse |
| 5 | Epic | late-game, strong substats begin |
| 6 | Legendary | endgame chase, full substat quality |
| 7 | Mythic | best-in-slot, vanishingly rare rolls |

**Gating is the core hours-sink — each tier is a wall:**
- **The tier a piece can drop is capped by the content level you farm it in.** Legendary/Mythic gear is **impossible to obtain at low level** — you physically cannot get it until you've climbed. No shortcuts to top gear.
- Higher tier = **higher main-stat bands + more/better substats + higher substat roll ceilings.** A Mythic piece isn't just "a Common with bigger numbers" — it rolls more substats at better quality, so the *optimization ceiling* rises with tier too.
- **Distribution within the envelope:** the 7 tiers must spread *inside* the ~2.5–3× gear envelope (§1), not blow past it. Early tiers (Cracked–Fine) deliver a small fraction of the multiplier; the top tiers (Legendary–Mythic) deliver the bulk. So the *spikes* concentrate late — which is exactly where a grind game wants its dopamine. Rough shape: a fully-Mythic-geared unit ≈ the ~2.5–3× target; a Common-geared unit ≈ ~1.3–1.5×.
- This is the **D2-flavored collection texture** (rarity ladder + "neat to complete") riding on the E7 substat mechanic.
- **Non-predatory:** gear is earned by play (dungeon/arena/side-game drops, crafting), **never real-money sold**, no gear loot-boxes-with-a-price-tag.

---

## 7. Unique gear — unit-earned, tradeable (FFBE Trust Master style)

A **separate acquisition track** from farmed gear: super-strong **unique pieces you unlock by mastering a specific unit**, not from drop RNG. The best kind of grind reward — earned through *play with a unit*, not a slot machine.

- **How you earn it:** progress a specific unit far enough (playtime/usage counter, à la FFBE TMR) **and/or creative conditions** — e.g. win N arena matches with them, land N executes (Kael), spread Burn to N enemies (Vespera), clear a dungeon with them solo, keep them alive through a boss. Conditions can be **unit-flavored** so the unlock *feels* like mastering that character.
- **TRADEABLE (owner decision):** once earned on a unit, the unique piece can be **equipped by any unit** (FFBE TMR model). This is deliberate and creates a **whole meta-layer / hours-sink** — players farm units purely to graduate their unique piece, then move it to a favorite carry.
- **Design tension (must respect):** because uniques are *account-wide portable*, they **cannot be so strong they invalidate set gear** — otherwise everyone runs 6 uniques and the set system dies. Tuning rule: a unique piece is **best-in-slot for THAT slot but does not complete a set**, so running uniques means *sacrificing set bonuses*. That's the balancing lever — uniques are a trade-off (raw power vs set identity), not a strict upgrade. Some uniques can *count toward* a themed set to reward matching them to a synergistic build.
- **Synergy hook:** a unit's own unique can synergize with *its own kit* (Vespera's boosts Burn, a healer's boosts healing done), so mains are rewarded for graduating their character's signature — tying unique gear into the "chess"/teambuilding layer.
- **Non-predatory by nature:** it's a playtime/mastery unlock, impossible to buy.

---

## 8. Set list — the full menu

Sets activate by **count** (§2): 2-piece = filler bonus, 4-piece = build identity. Values are placeholder dials.

### Stat sets (available across tiers; higher tier = bigger numbers)

| Set | 2-piece | 4-piece | For |
|-----|---------|---------|-----|
| **Swift** (SPD) | +8% SPD | +25% SPD | speed-team enablers, tempo carries, everyone who wants to act first |
| **Fury** (ATK) | +12% ATK | +45% ATK | raw damage carries |
| **Bloodlust** (Crit Rate) | +12% Crit Rate | +40% Crit Rate | crit carries (pair w/ Crit Dmg) |
| **Savage** (Crit Dmg) | +15% Crit Dmg | +55% Crit Dmg | crit carries; the damage half of a crit build |
| **Vigor** (HP) | +12% HP | +45% HP | tanks, sustain units, HP-scalers |
| **Bastion** (DEF) | +12% DEF | +45% DEF | tanks, defensive walls |
| **Malice** (POT) | +10% Potency | +35% Potency | debuffers/control — makes effects land & stick |
| **Warding** (RES) | +10% RES | +35% RES | anti-control / anti-debuff bruisers |
| **Focus** (Effect Hit) | +10% effect hit | +30% effect hit | debuff appliers who need reliability (alt to POT) |
| **Mending** (Healing) | +10% healing done | +35% healing done | healers |
| **Leech** (Lifesteal) | +8% lifesteal | +25% lifesteal | self-sustaining bruisers |

Typical builds read as **"4-identity + 2-filler"** — e.g. *4-Savage + 2-Bloodlust* (crit carry), *4-Swift + 2-Malice* (fast debuffer), *4-Vigor + 2-Bastion* (tank).

### Effect sets (RARE — gated behind the top 2–3 tiers, Epic/Legendary/Mythic only)

These hook the combat effect glossary — the aspirational chase that changes *what a unit does*. All reference real `effects.json` ids. **4-piece only** (they're identity-defining, not filler).

| Set | 4-piece effect | For |
|-----|----------------|-----|
| **Ember** | attacks apply/extend `burn`; +`dot_amp` to your DoTs | Burn/DoT teams (Red engine 2) |
| **Piercer** | attacks gain `ignore_def` (def-pen %) | anti-tank / anti-wall carries |
| **Executioner** | raises `execute` threshold / adds execute chance | finisher carries (Red kill-chain) |
| **Tempo** | `momentum_pull` on your turn; resist enemy `momentum_push` | speed/tempo teams (Blue) |
| **Vampiric** | scaling `lifesteal_buff` on all damage | aggressive self-sustain (Red/Dark) |
| **Detonator** | chance to `detonate_dot` on hit | DoT-payload teams |
| **Warden** | grants allies periodic `damage_reduction` / `debuff_immunity` | support/defensive cores (Green/Gold) |
| **Hexward** | your debuffs gain duration / harder to cleanse | control/debuff specialists (Dark/Blue) |

Gating effect-sets to high tiers means they're a **late-game power+identity spike** — you climb the rarity ladder *and* unlock strategy-changing gear at the top, a double reward that deepens the endgame chase.

---

## 9. Downstream impact & open decisions

**Model:** `BUILD_MULT` moved 1.8 → **2.5** in `power_model_v3.py` (mid-game geared state). Scores now reflect a geared unit. The 7-tier ladder means a *naked* unit, a *Common-geared* (~1.4×), and a *Mythic-geared* (~2.5–3×) unit are three different power levels — a future model refinement could expose a tier column.

**Feeds the budget system:** value ceilings must read at a geared build state; units that scale hard with gear (crit carries, effect-set users) are worth more in a geared meta than their naked score. Effect-sets especially amplify kit identity — a Burn unit in Ember gear is worth more than its naked Burn.

**Feeds encounter design (the connected next step):** bosses/dungeons tune against naked×(tier multiplier) — early content vs Common-geared teams, endgame vs Mythic+effect-set teams. Gate content difficulty to the gear tier players could plausibly have farmed by then.

**Open decisions (not blocking):**
- Exact slot names + which slots gate which main-stat pools.
- Final set-bonus numbers (above are placeholders) and the full unique-gear list (one per unit? per Legendary?).
- Unique-gear unlock conditions per unit + whether/which uniques count toward sets.
- Substat roll math (rolls, boost ranges, reforge mechanics).
- Rarity tier names (proposed above) + drop sources per tier (dungeon escrow / arena / side-game shops / crafting).
- Exact per-tier multiplier distribution within the 2.5–3× envelope + endgame soft cap.
