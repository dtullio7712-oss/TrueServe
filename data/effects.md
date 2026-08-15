# Effects Glossary

Canonical status-effect glossary — **94 effects**. Schema version **0.5**.

This glossary defines the **effect** (what it does, how it's removed, whether it stacks). The **ability/kit defines the number** (magnitude, duration, chance). `effects[]` on an ability holds ONLY valid glossary status ids; conditional damage, hit-shape, and penetration live on the ability, not here.

## Rules

**Categories:** buff, debuff, dot, control, instant, special

**Duration models:** turns, momentum, permanent, instant

### Removal

- **buffs** — removed by STRIP (enemy) unless dispellable=false
- **debuffs** — removed by CLEANSE (ally) unless cleansable=false
- **dots** — debuff subtype; cleanse removes unless flagged; Doom is uncleansable
- **control** — cleansable unless flagged; Enrage family is uncleansable
- **instant** — resolves once; nothing to remove

**Stacking.** only stacks=true effects stack (DoTs: Poison/Bleed/Burn/Curse + a few flagged). Non-stacking uses REFRESH-IF-STRONGER: a stronger application overwrites; weaker is ignored; equal refreshes duration.

**Undispellable.** any effect may set dispellable=false (buffs) / cleansable=false (debuffs) — used for Gold permanence, Dark/Doom, and the Enrage family.

**Team-wide.** 'team-wide' is NOT a separate effect — it's a target/duration modifier the ABILITY sets. Standard effects (ATK Up, Regen, POT Up, etc.) can be applied single-target OR team-wide; team versions are balanced by shorter duration or by being gated to rarer units. Do not author 'team_x' as its own entry.

**Control ladder.** Action-denial ladder — each blocks exactly ONE action type: Disarm=no basics, Silence=no skills, Sealed=no ults. Stun=full lockout (all three) + still takes damage. Freeze=lose turn but immune to direct damage (DoTs tick), 1 turn then breaks. Sleep=lose turns + self-heal 20%/turn, breaks on damage.

**Enrage system.** Enrage (Berserk/Frenzy/Overload) is UNCLEANSABLE and TRIGGER-BOUND (hp_threshold/phase/turn_count/on_effect:<id>/manual) — almost never a cast skill. Enemy-focused; rarely a (double-edged) player buff. Pair with 'prevent_death_team' (Last Line) for the signature un-killable-but-deadly survival window.

**Trigger field.** effects with a 'trigger' key are applied by a CONDITION, not by casting. The combat engine watches for the trigger and applies the effect when it fires.

**Values.** 'X%' values are set per-ability (the skill defines the magnitude); this glossary defines the EFFECT, the kit defines the NUMBER.

**Ability fields.** Conditional damage, hit-shape, and pen live on the ABILITY, not in effects[]: 'hits' (int, multi-hit), 'ignore_def' (0..1 fraction of DEF ignored), 'bonus_vs' ({condition, amount} conditional damage/crit — the set-up->exploit layer), 'triggers' ([{effect,on}] condition-applied effects using the trigger_field rule). effects[] holds ONLY valid glossary status ids.

**No instant death.** Doom (death-on-timer) is REMOVED. Timed pressure uses debuff_bomb: countdown -> debuff payload on expiry, never a guaranteed kill.

**Magnitude schema.** Effects on abilities are objects: {id, mag(%/value), dur(turns), chance(0-1 base apply), stacks}. Magnitude TYPE by effect: PERCENT_STAT (mag=% stat delta), PERCENT_HP (mag=% max HP), DOT (mag=% target HP/tick), MOMENTUM (mag=% gauge), DURATION_ONLY (value from dur+chance), SPECIAL (bespoke: execute=threshold%, etc). atk_up_major/def_break_major/regen_major FOLDED into base id with high mag.

## Effects

### Buffs (22)

| Effect | id | Duration | Notes | Tags |
|---|---|---|---|---|
| **Attack Up** — +X% ATK. | `atk_up` | 2 turns | — | stat, offense |
| **Bloodthirst** — This unit's damage heals it for X% (temporary). | `lifesteal_buff` | 2 turns | — | heal, offense |
| **Counter Stance** — Counterattacks the next enemy who strikes this unit. | `counter` | 2 turns | — | punish |
| **Crit Damage Up** — +X% Crit Damage. | `crit_dmg_up` | 2 turns | — | stat, offense |
| **Crit Rate Up** — +X% Crit Rate. | `crit_rate_up` | 2 turns | — | stat, offense |
| **Damage Reduction** — Takes X% less damage from all sources. | `damage_reduction` | 2 turns | — | defense |
| **Debuff Immunity** — Cannot receive new debuffs while active. | `debuff_immunity` | 2 turns | — | defense, immunity |
| **Defense Up** — +X% DEF. | `def_up` | 2 turns | — | stat, defense |
| **Evasion Up** — +X% chance to dodge incoming attacks. | `dodge_up` | 2 turns | — | defense |
| **Perfect Focus** — This unit's next X hits are guaranteed crits. | `guaranteed_crit_buff` | 2 turns | stacks (max 3) | offense |
| **Potency Up** — +X% Potency (debuffs land harder). | `pot_up` | 2 turns | — | stat, control |
| **Provoke (self)** — Forces enemies to target this unit. | `taunt_self` | 2 turns | — | tank, aggro |
| **Reflect** — Returns X% of damage taken to the attacker. | `reflect` | 2 turns | — | defense, punish |
| **Regeneration** — Heal X% max HP at end of each turn. | `regen` | 2 turns | — | heal, hot |
| **Resolve Up** — +X% Resolve (resist incoming debuffs). | `res_up` | 2 turns | — | stat, defense |
| **Rooted** — Immune to enemy Momentum push/pull. | `momentum_immunity` | 2 turns | — | tempo, immunity |
| **Shield** — Absorbs up to X damage, then breaks. | `shield` | 2 turns | — | defense, absorb |
| **Speed Up** — +X% SPD (faster Momentum gain). | `spd_up` | 2 turns | — | stat, tempo |
| **True Aim** — This unit's attacks cannot miss while active. | `cannot_miss_buff` | 2 turns | — | offense, accuracy |
| **Undying** — Cannot drop below 1 HP while active (survives lethal). Dispellable — enemies can strip it for counterplay. | `death_immunity` | 2 turns | — | defense, survival |
| **Unstoppable** — Immune to control (Stun/Freeze/Silence/Disarm/Sealed/Taunt/push). | `control_immunity` | 2 turns | — | defense, immunity, tempo |
| **Veil** — Cannot be targeted by single-target attacks (until it acts / X turns). | `stealth` | 2 turns | — | defense, tempo |

### Debuffs (17)

| Effect | id | Duration | Notes | Tags |
|---|---|---|---|---|
| **Anti-Heal** — Healing received reduced by X% (up to 100%). | `anti_heal` | 2 turns | — | control, sustain-denial |
| **Attack Down** — -X% ATK. | `atk_down` | 2 turns | — | stat, offense |
| **Blind** — This unit's attacks have an X% chance to miss. | `accuracy_down` | 2 turns | — | control, accuracy |
| **Brand** — Target takes +X% damage from ALL sources. | `brand` | 2 turns | — | amplify, offense |
| **Crit Rate Down** — -X% Crit Rate. | `crit_rate_down` | 2 turns | — | stat |
| **Dampened** — Gains Momentum X% slower. | `momentum_slow_field` | 2 turns | — | tempo, control |
| **Defense Break** — -X% DEF. | `def_break` | 2 turns | — | stat, defense |
| **DoT Amplify** — Target takes +X% damage from all damage-over-time effects (Poison/Bleed/Burn/Curse). Set per-ability. | `dot_amp` | 2 turns | undispellable | dot, amplify, synergy |
| **Exposed** — Takes +X% damage from a marked source/team. | `damage_taken_up` | 2 turns | — | amplify |
| **Heal Block** — Cannot be healed at all while active. | `healing_block` | 2 turns | — | control, sustain-denial |
| **Marked** — Team deals +X% to this target; enables 'exploit' effects. | `marked` | 2 turns | — | amplify, synergy |
| **Null** — Cannot receive new buffs while active. | `buff_block` | 2 turns | — | control |
| **Potency Down** — -X% Potency (their debuffs fail more). | `pot_down` | 2 turns | — | stat, control |
| **Resolve Down** — -X% Resolve (easier to debuff). | `res_down` | 2 turns | — | stat, control |
| **Shatterproof** — Cannot gain new shields while active. | `shield_block` | 2 turns | — | control |
| **Slow** — -X% SPD (slower Momentum gain). | `spd_down` | 2 turns | — | stat, tempo |
| **Sundered Affinity** — Loses affinity advantage / takes affinity disadvantage. | `vulnerable_element` | 2 turns | — | amplify, affinity |

### Damage Over Time (DoT) (4)

| Effect | id | Duration | Notes | Tags |
|---|---|---|---|---|
| **Bleed** — Deals flat X damage each turn, scales w/ caster ATK. Stacks. | `bleed` | 2 turns | stacks (max 10) | dot |
| **Burn** — Deals X damage each turn; bonus vs low-DEF. Stacks. NOTE: damage-calc method flagged for a future tweak. | `burn` | 2 turns | stacks (max 5) | dot, red, revisit |
| **Curse** — Damage each turn that INCREASES the longer it remains. Stacks. | `curse` | 2 turns | stacks (max 5) | dot, dark |
| **Poison** — Deals X% of target max HP as damage each turn. Stacks. | `poison` | 2 turns | stacks (max 10) | dot, green, dark |

### Control (8)

| Effect | id | Duration | Notes | Tags |
|---|---|---|---|---|
| **Disarm** — Cannot use BASIC ATTACKS (skills & ults still usable). Value spikes when the enemy's skills/ults are on cooldown — then they have nothing to do and lose the turn. | `disarm` | 2 turns | — | softcc, ladder |
| **Freeze** — Loses its turn when Momentum fills, BUT is immune to DIRECT damage while frozen (DoTs still tick). Costs ONE turn, then breaks. Defensive/stall control — you can't burst a frozen enemy, so freezing a low-HP target actually protects it. | `freeze` | 1 turns | — | hardcc, stall |
| **Mass Taunt** — All affected enemies forced to target the caster. | `provoke_all` | 2 turns | — | aggro |
| **Sealed** — Cannot use ULTS (basic attacks & skills still usable). Third rung of the action-denial ladder. | `ult_lock` | 2 turns | — | softcc, ladder |
| **Silence** — Cannot use SKILLS (basic attacks & ults still usable). | `silence` | 2 turns | — | softcc, ladder |
| **Sleep** — Skips turns AND heals 20% max HP per turn; breaks on damage taken. Double-edged risk control — you gift HP for tempo, and the enemy may even want to keep it. | `sleep` | 2 turns | — | hardcc, risk |
| **Stun** — FULL LOCKOUT: skips the turn entirely AND still takes damage normally. The offensive control — lock them and burst them. | `stun` | 1 turns | — | hardcc |
| **Taunt** — Forced to target the taunting unit. | `taunt` | 2 turns | — | aggro |

### Instant (17)

| Effect | id | Duration | Notes | Tags |
|---|---|---|---|---|
| **Cleanse** — Remove X debuffs from a target (skips uncleansable). | `cleanse` | instant | — | support |
| **Detonate** — Consume all DoT stacks on a target for burst damage. | `detonate_dot` | instant | — | dot, burst |
| **Execute** — Instantly kill a target below X% HP. | `execute` | instant | — | burst |
| **Extra Action** — Target immediately gains an extra turn. | `extra_action` | instant | — | tempo |
| **Hasten** — Reduce an ally's cooldowns by X turns. | `cooldown_reduction` | instant | — | support, tempo |
| **Heal** — Restore X% of target max HP (or flat). | `heal` | instant | — | heal |
| **Mass Cleanse** — Remove all cleansable debuffs from the team. | `cleanse_all` | instant | — | support |
| **Momentum Pull** — Increase an ally's Momentum gauge by X%. | `momentum_pull` | instant | — | tempo |
| **Momentum Push** — Reduce target's Momentum gauge by X%. | `momentum_push` | instant | — | tempo |
| **Momentum Steal** — Take X% Momentum from an enemy, give to an ally. | `momentum_steal` | instant | — | tempo |
| **Refund** — Refund this unit's cooldown (often on kill). | `cooldown_refund` | instant | — | tempo |
| **Revive** — Bring a fallen ally back at X% HP. | `revive` | instant | — | heal, survival |
| **Setback** — Push target to the back of the turn order. | `knockback_momentum` | instant | — | tempo |
| **Shrug Off** — This unit removes debuffs from itself. | `dispel_self_debuffs` | instant | — | support |
| **Strip** — Remove X buffs from ONE enemy (skips undispellable). | `strip` | instant | — | control |
| **Strip (Multi)** — Remove X buffs from MULTIPLE enemies (not a full wipe — X per target, skips undispellable). | `strip_multi` | instant | — | control |
| **Team Heal** — Heal all allies. | `heal_team` | instant | — | heal |

### Special (26)

| Effect | id | Duration | Notes | Tags |
|---|---|---|---|---|
| **Aegis (Shield)** — A shield that cannot be bypassed by ignore-DEF/pierce. | `shield_unbreakable` | 2 turns | undispellable | defense, absorb, gold |
| **Berserk (Enrage)** — +big ATK, but takes more damage. Glass-cannon rage — you CAN race it down, but every hit it lands is brutal. | `enrage_berserk` | 2 turns | undispellable; uncleansable; trigger: `hp_threshold` | enrage, enemy, survival |
| **Blood Bond** — Allies share one HP pool for the duration (damage spread). | `shared_hp_pool` | 2 turns | — | dark, defense |
| **Blood Price** — Caster spends X% HP to power an effect. | `hp_cost` | instant | — | dark, cost |
| **Charge** — Plants a charge that detonates on a later turn. | `delayed_charge` | 1 turns | — | setup, burst |
| **Coronation Aura** — +X% to all core stats; unremovable while active. | `aura_all_stats` | 2 turns | undispellable | gold, command |
| **Crimson Bond** — All damage this unit deals also heals the team X%. (Was a buff; promoted to signature-tier special.) | `team_damage_heals` | 2 turns | — | heal, offense, red, signature |
| **Debuff Bomb** — A timed marker that ticks down over N turns (visible counter). On expiry it does NOT kill — it detonates, applying a payload of debuffs defined by the ability. Removing the marker before detonation (cleanse, if cleansable) defuses it. The bomb-planter's kit sets the countdown and payload. | `debuff_bomb` | 3 turns | undispellable | timed, payload, control |
| **Debuff-Spread** — Copy ANY of a target's debuffs (incl. control & stat-downs) to all enemies. Rarer & stronger than DoT-Spread. | `spread_debuff` | instant | — | control, rare |
| **Decree** — Marks the attached stat buff as non-expiring (permanent until dispelled). | `permanent_buff_flag` | 2 turns | — | gold, command |
| **DoT-Spread** — Copy a target's DoTs (Poison/Bleed/Burn/Curse) to all enemies. | `spread_dot` | instant | — | dot, green, dark |
| **Frenzy (Enrage)** — Extra actions / Momentum surge — the enemy acts far more often. The scramble is TEMPO: it takes several turns to your one. | `enrage_frenzy` | 2 turns | undispellable; uncleansable; trigger: `phase` | enrage, enemy, survival, tempo |
| **Immutable** — Caps damage taken per hit at X% of max HP (anti-burst). | `damage_cap` | 2 turns | undispellable | gold, defense |
| **Last Line** — Team cannot drop below 1 HP for the duration. | `prevent_death_team` | 2 turns | undispellable | survival, gold |
| **Last Stand** — Effect strengthens the lower the unit's own HP. | `scale_inverse_hp` | 2 turns | undispellable | scaling, survival |
| **Martyr** — Pulls debuffs off allies onto this unit; may gain from holding them. | `absorb_ally_debuffs` | instant | — | support, dark |
| **Overload (Enrage)** — Ultimates come off cooldown / can be re-used repeatedly. The scramble is BURST: big hits keep landing. | `enrage_overload` | 2 turns | undispellable; uncleansable; trigger: `turn_count` | enrage, enemy, survival |
| **Ramp** — A stat/effect that grows each turn or each use (per-unit defined). | `stacking_scaler` | 2 turns | stacks (max 99); undispellable | scaling |
| **Retribution** — Stored damage taken converts into output on a trigger. | `scale_with_damage_taken` | 2 turns | undispellable | scaling, punish |
| **Shared Agony** — While active on an ally, enemies that damage them take reflected curse damage. (Special debuff/reflect hybrid.) | `shared_agony` | 2 turns | — | dark, punish, reflect |
| **Sovereign Ward** — This unit's buffs cannot be stripped by enemies. | `buff_undispellable` | 2 turns | undispellable | gold, command |
| **Threat** — Alters how much aggro this unit generates (up or down). | `threat_mod` | 2 turns | — | tank, aggro |
| **Unbending (Damage Reduction)** — Damage reduction that cannot itself be reduced/ignored. | `dr_unreducible` | 2 turns | undispellable | defense, gold |
| **Unresistable** — Flags an effect to ignore the Potency/Resolve contest (always lands). | `unresistable` | instant | — | gold, dark, control |
| **Wasting** — Target loses X% max HP each turn AND -healing received. (Special debuff — a %maxHP DoT fused with sustain-denial.) | `wasting` | 2 turns | — | dark, dot, sustain-denial |
| **Wild Magic** — Outcome is randomized within a defined band (the gamble). | `randomized_effect` | instant | — | dark, variance |
