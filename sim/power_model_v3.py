"""
POWER VALUATION MODEL v0.5 — magnitude-aware, fight-duration-aware, dual-column.
Fixes (owner-driven):
 - Effects carry real magnitudes; value DERIVES from mag/dur/chance, not flat tokens.
 - Per-turn effects (regen/dot/momentum/control) valued against FIGHT LENGTH:
   Skirmish=4 turns, Boss=20 turns -> two separate scores. NO blended total.
 - Passives scored off the EFFECT they grant (same vocab as abilities), not regex on prose. (fixes Alcuin)
 - Stat magnitudes resolve at a BUILD STATE (level55+mid gear ~1.8x) [STUB until progression math exists].
"""
import json, math
roster=json.load(open('roster.json'))
effects=json.load(open('effects.json'))
CAT={e['id']:e['category'] for e in effects['effects']}

# ---- dials ----
SKIRMISH=4; BOSS=20
BUILD_MULT=2.5          # gear power envelope (E7-style ~2.5x mid-game). See GEARING.md. Was 1.8 stub.
BASELINE={'hp':9000,'atk':1000,'def':600,'spd':100,'pot':0.0,'res':0.0}

# ---- 1. STAT POWER (resolved at build state) ----
def stat_power(b):
    hp=(b['hp']*BUILD_MULT)/BASELINE['hp']; atk=(b['atk']*BUILD_MULT)/BASELINE['atk']
    dfp=(1000+b['def']*BUILD_MULT)/(1000+BASELINE['def']); spd=((b['spd']*1.0)/BASELINE['spd'])**1.4
    pot=1+b['pot']*1.5; res=1+b['res']*1.5
    W={'hp':1,'atk':1.2,'dfp':0.8,'spd':1.3,'pot':0.5,'res':0.5}
    return (W['hp']*hp+W['atk']*atk+W['dfp']*dfp+W['spd']*spd+W['pot']*pot+W['res']*res)/sum(W.values())*100

# ---- 2. EFFECT VALUE from magnitude, gated by fight length ----
# base "worth" coefficients per effect (value of a REFERENCE magnitude). Magnitude scales via mag^0.8.
REF={ # (reference_mag, base_value_at_ref)
 'atk_up':(22,6),'def_up':(20,5),'spd_up':(16,8),'crit_rate_up':(18,6),'crit_dmg_up':(30,6),
 'pot_up':(15,4),'res_up':(15,4),'atk_down':(22,6),'def_break':(25,7),'spd_down':(22,7),
 'crit_rate_down':(15,4),'pot_down':(15,4),'res_down':(22,6),'accuracy_down':(25,5),
 'damage_reduction':(20,7),'dr_unreducible':(18,10),'dodge_up':(18,5),'damage_taken_up':(22,8),'dot_amp':(25,7),
 'heal':(30,6),'heal_team':(22,6),'regen':(8,4),'shield':(25,7),'shield_unbreakable':(22,11),
 'lifesteal_buff':(30,5),'hp_cost':(15,-4),'revive':(50,12),
 'poison':(7,4),'bleed':(7,4),'burn':(7,4),'curse':(8,5),
 'momentum_push':(28,7),'momentum_pull':(28,7),'momentum_steal':(25,9),'knockback_momentum':(30,6),'momentum_slow_field':(25,8),
}
CONTROL_VAL={'stun':14,'freeze':9,'sleep':11,'silence':8,'disarm':7,'ult_lock':8,'taunt':6,'provoke_all':10}
UTIL_VAL={'brand':8,'marked':5,'anti_heal':7,'healing_block':7,'buff_block':7,'shield_block':5,
 'debuff_immunity':8,'control_immunity':11,'death_immunity':11,'momentum_immunity':7,'stealth':6,
 'reflect':5,'counter':5,'cannot_miss_buff':5,'guaranteed_crit_buff':8,'buff_undispellable':9,
 'permanent_buff_flag':8,'vulnerable_element':5,'taunt_self':4,'dodge_up':5}
SPECIAL_VAL={'aura_all_stats':16,'execute':12,'strip':6,'strip_multi':9,'cleanse':6,'cleanse_all':9,
 'extra_action':13,'cooldown_reduction':6,'cooldown_refund':7,'detonate_dot':8,'dispel_self_debuffs':4,
 'debuff_bomb':13,'spread_dot':10,'spread_debuff':9,'scale_inverse_hp':8,'scale_with_damage_taken':9,
 'stacking_scaler':9,'shared_hp_pool':6,'shared_agony':9,'wasting':10,'unresistable':9,
 'prevent_death_team':14,'damage_cap':11,'team_damage_heals':11,'absorb_ally_debuffs':7,
 'randomized_effect':6,'delayed_charge':7,'threat_mod':5,'enrage_berserk':10,'enrage_frenzy':9,'enrage_overload':11}

def mag_scale(eid, mag):
    if eid in REF and mag is not None:
        ref,val=REF[eid]
        return val*(mag/ref)**0.8
    return None

def effect_value(e, fight_len):
    """value of one effect object in a fight of `fight_len` turns."""
    eid=e['id']; mag=e.get('mag'); dur=e.get('dur'); chance=e.get('chance',1.0); stacks=e.get('stacks',1)
    cat=CAT.get(eid)
    # --- DoT: per-tick value * ticks (gated by fight length) * stacks(diminishing) ---
    if cat=='dot':
        per=mag_scale(eid,mag) or 4
        ticks=min(dur or 3, fight_len)
        stk=sum(0.8**i for i in range(stacks))   # stacks diminish
        return per*ticks*stk*0.6
    # --- per-turn buffs/debuffs that PERSIST: value * min(dur, fight_len)/ref_dur ---
    if cat in('buff','debuff'):
        if eid in REF:
            base=mag_scale(eid,mag) or 5
        else:
            base=UTIL_VAL.get(eid,6)
        active=min(dur or 3, fight_len)
        # value accrues per active turn but with saturation; ref is 3 turns
        dur_factor=active/3 if active<3 else (1+0.4*math.log2(active/3+ (0 if active==3 else 0)))
        dur_factor=min(dur_factor, 1+0.4*math.log2(fight_len/3)) if fight_len>3 else active/3
        return base*max(dur_factor,0.34)
    # --- control: rating * duration * chance (duration matters more in short fights, relatively) ---
    if cat=='control':
        base=CONTROL_VAL.get(eid,8)
        d=min(dur or 1, fight_len)
        return base*(1+0.5*(d-1))*chance
    # --- momentum (instant tempo swing) ---
    if eid in ('momentum_push','momentum_pull','momentum_steal','knockback_momentum'):
        v=mag_scale(eid,mag) or 7
        # tempo compounds over long fights: a push is worth more the longer the fight
        return v*(1+0.4*math.log2(fight_len/4+1))
    if eid=='momentum_slow_field':
        v=mag_scale(eid,mag) or 8
        active=min(dur or 3,fight_len)
        return v*active/3*(1+0.3*math.log2(fight_len/4+1))
    # --- instant heals/shields ---
    if eid in('heal','heal_team','shield','shield_unbreakable','revive','lifesteal_buff','cleanse','cleanse_all','strip','strip_multi','dispel_self_debuffs'):
        return (mag_scale(eid,mag) if eid in REF else SPECIAL_VAL.get(eid,6)) or SPECIAL_VAL.get(eid,6)
    # --- special ---
    return SPECIAL_VAL.get(eid, 6)

# ---- targeting: EFFECTS scale w/ bodies (diminishing when spammable); DAMAGE ~ flat ----
def eff_target_mult(target, cd):
    if target in('all_enemies','all_allies'):
        et=4**0.83
        if cd<=1: et*=0.72
        elif cd==2: et*=0.85
        return et
    if target=='primary+adjacent': return 2**0.83
    return 1.0

def uses_over_fight(cd, fight_len):
    """Effective firings of an ability (cd) over a fight, with SATURATION so long fights
    don't scale linearly to absurd numbers. A unit can't infinitely stack value; there are
    only so many useful casts. sqrt-like saturation keeps the RATIO between unit types
    meaningful while capping absolute growth."""
    raw = fight_len/(cd+1)
    # saturating curve: ~linear early, compresses as raw grows large
    return max(1.0, 1 + 3.2*math.log2(raw))  if raw>1 else 1.0

def ability_score(a, fight_len):
    team=a.get('target') in('all_enemies','all_allies')
    cd=a.get('cooldown',0)
    n=uses_over_fight(cd,fight_len)
    # --- per-CAST damage ---
    dmg=(a.get('mult') or 0)*(a.get('hits') or 1)
    if a.get('ignore_def'):dmg*=(1+0.5*a['ignore_def'])
    if a.get('bonus_vs'):dmg*=1.15
    dmg*=6*(1.1 if team else 1.0)
    # --- per-CAST effect value ---
    et=eff_target_mult(a.get('target'),cd)
    vals=sorted([effect_value(e,fight_len)*et for e in a.get('effects',[])],reverse=True)
    eff_sum=sum(v*(0.7**i) for i,v in enumerate(vals))
    for t in a.get('triggers',[]):
        te={'id':t['effect'],'mag':t.get('mag'),'dur':t.get('dur')}
        eff_sum+=effect_value(te,fight_len)*et*0.6
    # --- repeat over fight, with DIFFERENT scaling for damage vs sustain/utility ---
    # Damage front-loads: repeats have diminishing value (enemy dies, or overkill). Utility scales cleaner.
    dmg_uses  = 1 + (n-1)*0.55          # damage gains ~55% of each extra cast's value
    util_uses = 1 + (n-1)*0.85          # sustain/control gains ~85% of each extra cast
    per_cast = dmg*dmg_uses + eff_sum*util_uses
    # normalize so a 0-cd single-effect ability in a 4-turn fight ~ its old scale
    per_cast /= (1 + (uses_over_fight(0,SKIRMISH)-1)*0.85)  # keep numbers in familiar range
    return per_cast, dmg, vals

# ---- 3. PASSIVE VALUE — scored off the structured ps_tag, NOT regex on prose ----
STAT_PCT_VAL={'hp':0.30,'atk':0.42,'def':0.28,'spd':0.55,'res':0.22,'pot':0.30,
 'crit rate':0.40,'crit damage':0.30,'crit dmg':0.30,'potency':0.30,'healing':0.30,'dodge':0.30,'lifesteal':0.30}
POTENCY_MECH={'legendary':11,'epic':7,'common':4}

def passive_effect_value(p, fight_len):
    tag=p.get('ps_tag')
    if not tag:  # unmigrated fallback
        return POTENCY_MECH.get(p.get('potency'),5)
    cond = 0.7 if tag.get('conditional') else 1.0
    if tag['kind']=='effect':
        # value the granted effect as an always-on version (permanent -> use a long-ish持续)
        e={'id':tag['effect'],'mag':None,'dur':4}
        base=effect_value(e,fight_len)
        # passives are permanent/always-on -> worth a bit more than a temp cast, but not per-turn stacked
        return base*1.15*cond
    if tag['kind']=='stat':
        return tag['pct']*STAT_PCT_VAL.get(tag['stat'],0.3)*cond
    # mechanic (enhance/unlock with no clean stat or effect) -> potency tier
    return POTENCY_MECH.get(p.get('potency'),5)*cond

AFF={'judgment':1.0,'life':1.0,'revelation':1.0,'majesty':1.06,'mystery':1.055}

def score_unit(u, fight_len):
    sp=stat_power(u['baseStats'])
    abils=[]; ap=0
    for a in u['abilities']:
        s,dmg,vals=ability_score(a,fight_len); abils.append((a,round(s,1),dmg,vals)); ap+=s
    pp=sum(passive_effect_value(p,fight_len) for p in u['passives'])
    return dict(u=u,stat=round(sp,1),ability=round(ap,1),passive=round(pp,1),
                total=round((sp*0.5+ap+pp)*AFF[u['affinity']],1),abils=abils)

def score_both(u):
    sk=score_unit(u,SKIRMISH); bo=score_unit(u,BOSS)
    return dict(u=u,stat=sk['stat'],
                ability_sk=sk['ability'],ability_bo=bo['ability'],
                passive_sk=sk['passive'],passive_bo=bo['passive'],
                PS_skirmish=sk['total'],PS_boss=bo['total'])

if __name__=='__main__':
    import statistics as st
    sc=[score_both(u) for u in roster['units']]
    for lbl,key in [('SKIRMISH','PS_skirmish'),('BOSS','PS_boss')]:
        print(f"\n=== {lbl} ===")
        for rar in['common','epic','legendary']:
            t=[x[key] for x in sc if x['u']['rarity']==rar]
            print(f"  {rar:10} mean={st.mean(t):.0f} range {min(t):.0f}-{max(t):.0f}")
