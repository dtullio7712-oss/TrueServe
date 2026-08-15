# ENEMY PROFILES & SCALING — Story/Grind Dungeon

> The layer beneath the dungeon-select mockup. The mock *assumes* a dungeon has a
> real power level; this spec is what makes that true. It defines **what an enemy IS**
> (roles + statlines) and **how enemies scale** across the 100 levels / 10 tiers.
>
> **Grounded in real data:** all numbers anchor to the actual `roster.json` level-1
> base stats by role, and were validated by simulation against the K=1000 damage model
> and the level+gear power curve from `progression_slice_spec`.

---

## 1. Core principle — enemies share the player's scale

Enemies use the **same 6-stat model** (HP/ATK/DEF/SPD/POT/RES) and the **same effect
glossary** as player units. An enemy is just a unit the AI drives. This means "a level-40
dungeon" is directly comparable to "a level-40 player team" — the whole difficulty read
in the mockup is real, not a label.

Enemies are anchored to the **player level-1 medians by role** (from `roster.json`):

| Player role | HP | ATK | DEF | SPD | (n) |
|---|---|---|---|---|---|
| solo_dmg | 690–**820**–1020 | 170–**225**–288 | 150–**160**–200 | 100–**118**–134 | 21 |
| aoe_dmg | 700–**800**–940 | 156–**210**–250 | 155–**170**–195 | 98–**108**–116 | 17 |
| debuff | 690–**810**–1009 | 165–**200**–304 | 155–**165**–210 | 110–**118**–130 | 19 |
| buff | 720–**800**–1050 | 155–**190**–210 | 160–**175**–230 | 100–**110**–128 | 15 |
| heal | 850–**920**–1050 | 155–**172**–205 | 170–**185**–215 | 100–**109**–120 | 14 |
| tank | 1200–**1300**–1441 | 148–**160**–236 | 235–**250**–275 | 86–**93**–105 | 14 |

---

## 2. Enemy roles (the normal-fight cast)

Five reusable enemy archetypes, each anchored to a player role median. A "well-made team"
must out-solve the *composition*, not just out-stat one enemy — this is where your
"4 tanks can't out-damage a healer" example lives.

| Enemy role | Anchor | L1 statline (HP/ATK/DEF/SPD) | Job in a fight |
|---|---|---|---|
| **Bruiser** | solo_dmg | 820 / 225 / 160 / 118 | Baseline threat. Deals the damage the player must survive/race. |
| **Warden** | tank | 1300 / 160 / 250 / 93 | HP wall. Punishes low-damage teams; must be out-DPS'd or bypassed. |
| **Mender** | heal | 900 / 172 / 185 / 109 | The "gear check in disguise." If the team can't out-damage its heals, they lose. **This is the unit that makes 4 tanks fail.** |
| **Hexer** | debuff | 810 / 200 / 165 / 118 | Applies pressure (slow/def-break/DoT). Punishes no-cleanse teams; rewards fast kills. |
| **Zealot** | aoe_dmg | 800 / 210 / 170 / 108 | Hits the whole team. Punishes low-survivability; the reason a healer/shield matters. |

> **Composition is the puzzle.** A normal fight = 2–4 of these. A fight with a **Mender +
> two Wardens** is a DPS check (out-heal-race it). A fight with **two Zealots + a Hexer**
> is a survivability check. The dungeon generator picks compositions that pose a *question*,
> not just a stat bar (see §5).

---

## 3. The scaling curve (the heart of it)

Enemy power at dungeon level **D** = `anchor_stat × level_mult(D) × gear_mult(enemy_gear(D))`.

- `level_mult(D) = 1.0 + 0.5·((D−1)/99)` → 1.0 at L1, 1.5 at L100 (mirrors player levels).
- `enemy_gear(D) = clamp((D−1)/100 × 0.9, 0, 0.9)` → **0 at L1**, ramps to 0.9 at L100.
- `gear_mult(f) = 1.0 + 0.7·f`.

**Why enemy gear ramps from zero:** a level-1 dungeon must be beatable by a *naked* level-1
team, so level-1 enemies carry no gear premium (mult = exactly 1.00×). The gear wall only
appears as you climb — which is precisely why an under-geared high-level team gets punished.

### Bruiser statline across the ladder (validated)

| Dungeon Lv | Tier | Mult | HP | ATK | DEF | SPD |
|---|---|---|---|---|---|---|
| 1 | 1 | 1.00× | 820 | 225 | 160 | 118 |
| 10 | 1 | 1.10× | 906 | 249 | 177 | 130 |
| 20 | 2 | 1.23× | 1006 | 276 | 196 | 145 |
| 40 | 4 | 1.49× | 1223 | 335 | 239 | 176 |
| 60 | 6 | 1.78× | 1460 | 401 | 285 | 210 |
| 80 | 8 | 2.10× | 1718 | 471 | 335 | 247 |
| 100 | 10 | 2.44× | 1997 | 548 | 390 | 287 |

(Warden/Mender/Hexer/Zealot use their own anchor row × the same mult.)

### Validation — a well-built same-level team trades favorably

Simulated a geared player carry vs a same-level Bruiser through the K=1000 curve:

| Dungeon Lv | Player kills enemy in | Enemy kills player in | Verdict |
|---|---|---|---|
| 1 | 2.6 hits | 4.4 hits | ✅ gentle |
| 40 | 2.9 hits | 4.7 hits | ✅ fair, costs resources |
| 100 | 3.2 hits | 5.1 hits | ✅ holds at cap |

The ~3-to-kill / ~5-to-die gap is the **attrition feel**: you win each fight but spend HP
and cooldowns, so the 3–9 fight chain + sub-boss is a genuine resource-management run, not a
faceroll. An *under-geared* team collapses this gap and loses — the design working as intended.

---

## 4. Sub-boss profile (the "not a pushover" ending)

The sub-boss is a normal-role enemy **scaled up + given a real kit**, not a bespoke raid boss.

- **Stat premium (locked, per-archetype — updated after sim).** HP premium depends on the
  sub-boss's archetype, because a boss only threatens via enrage/attrition if it *outlives* the
  team's damage (sim finding, `SIM_RESULTS.md`):
  - **Enrage / Sprint bosses: ×3.0–3.5 HP**, ×1.25 ATK/DEF, **+ a real enrage** (~35%+ `atk_up`
    per ≤2-turn cast, stacking). This pairing is what naturally overwhelms low-DPS-flavored /
    mono-tank teams — no turn-cap needed. A well-built team with real DPS kills it *before* the
    enrage spirals; a team that can't simply gets hammered.
  - **Signature-threat bosses (Bulwark / Plague / Warden-lock): ×1.6 HP**, ×1.25 ATK/DEF. Their
    danger is the mechanic (strip-wall, bomb, lock), not outliving your damage, so they don't
    need the big HP pool.
  - (The old flat ×1.6 applied enrage-boss HP that was too low for the enrage to ever matter —
    the boss died in ~3 rounds. Fixed.)
- **≥2 significant abilities (locked).** The stat boost alone does NOT make a sub-boss — a mere stat-stick is a "pushover with more HP." Every sub-boss carries **at least two meaningful abilities** beyond its basic attack, each of which *changes how the fight is played* — e.g. a real AoE, a debuff application (def_break / slow / silence), a self-sustain (regen/shield), a `debuff_bomb`, a summon, or a strip. At least one of the two must be the boss's **archetype signature** (below); the second adds a second axis of pressure so the fight isn't one-note.
- **Archetype roll:** draws one *question* from the template pool (Siege / Sprint / Warden-lock / Bulwark / Plague) — the same tags surfaced in the mockup's boss card. This picks the signature ability and makes each run's ending feel distinct with zero bespoke authoring.
- **Example kits (illustrative, generator-composed):**
  - *Bulwark Warden-anchor:* **A1** `Molten Guard` (self def_up + shield), **A2** `Ground Slam` (AoE + slow). → answer: strip + AoE-survivability.
  - *Plague Hexer-anchor:* **A1** `Rot Bloom` (team def_break + DoT), **A2** `Fester` (`debuff_bomb`, 5-turn). → answer: cleanse + burst before detonation.
  - *Sprint Bruiser-anchor:* **A1** `Rising Fury` (stacking atk_up self-enrage), **A2** `Cleave` (AoE that ramps with the stacks). → answer: race it down.
- **Multi-phase stays out.** One signature + one pressure ability is the ceiling for the grind loop. Multi-phase / phase-flip bosses (the Warden of Ash pattern) are Abyss/Hunt content.
- **Attrition gate:** because HP + cooldowns carry in from the normal fights, a team that *barely* cleared the fights arrives at the sub-boss depleted — the sub-boss is where "did you pace yourself" gets tested, and the second ability is what punishes a depleted team that has no answers left.

---

## 5. Composition generator (RNG-lite, per the mockup)

For a dungeon of level D with F fights (3–9):

1. **Normal fights** each roll a composition of 2–4 enemies from the 5 roles. **Variety over
   guarantee (locked):** runs are NOT forced to contain a comp-puzzle fight — some runs will
   be pure stat-checks, some will stack questions, and that unpredictability is the point.
   The generator weights *toward* including a "question" fight (Mender DPS-check or Zealot
   survivability-check) often, but does not mandate one. The sub-boss always carries the
   run's guaranteed tactical moment, so a stat-check-heavy run still ends on a real question.
2. **Enemy count scales gently with tier:** T1–3 fights are mostly 2–3 enemies; T7–10 push
   3–4 with nastier roles (Hexer/Mender more common up high).
3. **Affinity tint:** each dungeon has a dominant affinity (shown in the mock). ~60% of
   enemies match it — so bringing the advantaged color is *rewarded but not required* at
   low tiers (soft gating). At T7+ the tint hardens toward a real affinity wall.
4. **Sub-boss** rolls its archetype independent of the tint, so a Life-tinted dungeon can
   still end in a Sprint boss — keeps the ending from being predictable.

---

## 6. What this unblocks / open dials

**Unblocks:** with roles + scaling defined, `encounter_sim.py` (Phase 2) can now take
`(dungeon_level, composition)` and output fight-length + win/loss + resource-drain per fight
— i.e. we can *test whole runs* numerically before touching the prototype.

**Locked decisions (this pass):**
1. **Enemy gear floor = 0 at L1.** Kept as-is — earliest dungeon is naked-team-beatable.
2. **Sub-boss = stat premium ×1.6/×1.25 PLUS ≥2 significant abilities** (see §4). A stat
   stick is not a sub-boss; every one poses a real tactical question via its kit.
3. **Variety over guarantee.** Normal fights are NOT forced to include a comp-puzzle;
   pure stat-check runs are allowed. The sub-boss carries the guaranteed tactical moment.
4. **POT/RES held flat at player-median** for this encounter type. (Oppressive-debuff
   fights — scaled POT that outpaces cleanse — are deferred to a future encounter type,
   NOT the grind loop. Owner flagged wanting these later.)

---

## NEXT
With this locked, **Phase 2 = build `encounter_sim.py`**: feed it a dungeon level +
generated composition, get a full-run resource simulation out. Then Phase 3: wire one real
generated run into the prototype and play it — the actual "is the loop fun?" test.
