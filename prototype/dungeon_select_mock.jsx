import React, { useState, useMemo } from "react";

/*
  STORY / GRIND — DUNGEON SELECT MOCKUP
  The core-of-the-core loop. The player is always shown 5 randomized dungeons
  spanning BELOW -> AT -> ABOVE their level. Difficulty is a *player choice*,
  not a settings toggle. Pushing above your level is a visible temptation.

  Grounded in the real math (progression_slice_spec / GDD):
    - Level cap 100, 10 tiers of 10 levels each.
    - Levels give ~1.5x; GEAR gives ~1.7x and is the HEAVIER lever.
    - Combined ceiling ~2.5x. K=1000.
  So "difficulty" here is computed from BOTH the level gap AND a gear-readiness
  read — at equal level, an under-geared team gets a "stretch", proving the
  gear-is-heavier thesis.
*/

// ---- power model (mirrors the bash sanity-check) ----
const lvlMult = (L) => 1.0 + 0.5 * ((L - 1) / 99);
const gearMult = (frac) => 1.0 + 0.7 * frac;
const dungeonGearFrac = (D) => Math.min(0.45 + ((D - 1) / 100) * 0.5, 0.95);

function verdict(ratio) {
  if (ratio > 1.15) return { label: "Faceroll", tone: "faceroll", blurb: "Well below you. Fast clears, thin rewards." };
  if (ratio > 1.02) return { label: "Comfortable", tone: "comfortable", blurb: "A clean run for a current team." };
  if (ratio > 0.92) return { label: "Fair Fight", tone: "fair", blurb: "Matched to you. A good team wins; a lazy one doesn't." };
  if (ratio > 0.82) return { label: "Stretch", tone: "stretch", blurb: "Above you. You'll need real synergy and current gear." };
  return { label: "Brutal", tone: "brutal", blurb: "A gear check. Beating this is a flex." };
}

const TONES = {
  faceroll:    { bar: "#5b6b7a", chip: "#2a3540", text: "#9fb0c0" },
  comfortable: { bar: "#3fa66a", chip: "#173026", text: "#7fd6a3" },
  fair:        { bar: "#d9a441", chip: "#332614", text: "#f0cd7a" },
  stretch:     { bar: "#d9772f", chip: "#331d10", text: "#f0a765" },
  brutal:      { bar: "#c8384a", chip: "#331014", text: "#f07683" },
};

// ---- flavor pools for RNG-lite dungeon + sub-boss ----
const SITES = ["Ashfall Reliquary", "The Sunken Choir", "Embervault Deep", "Hollow Sanctum", "The Weeping Spire", "Cindergate Crypts", "Vault of Pale Light", "The Riven Cloister"];
const SUBBOSS = [
  { name: "a Siege warden", tag: "SURVIVE", hint: "Sustained AoE. Bring heals or shields — glass teams bleed out." },
  { name: "a Sprint enrager", tag: "SPEED", hint: "Enrage clock. Out-tempo it or eat the payload." },
  { name: "a Warden of locks", tag: "CONTROL", hint: "Telegraphed wipe-ult. Stun/Silence it every cycle." },
  { name: "a Bulwark idol", tag: "STRIP", hint: "Self-buffs to a wall. Strip + def-break or you can't scratch it." },
  { name: "a Plague-bearer", tag: "CLEANSE", hint: "Stacking debuffs. No cleanse = your team goes inert." },
];
const AFFINITY = [
  { c: "Judgment", col: "#c8384a" }, { c: "Life", col: "#3fa66a" },
  { c: "Revelation", col: "#3f7fd9" }, { c: "Majesty", col: "#d9b441" }, { c: "Mystery", col: "#8a5fd9" },
];

// deterministic-ish rng from a seed so the mock is stable per player level
function seeded(seed) { let s = seed % 2147483647; if (s <= 0) s += 2147483646; return () => (s = (s * 16807) % 2147483647) / 2147483647; }

function buildDungeons(playerLvl, playerGear) {
  const offsets = [-10, -5, 0, 8, 15];
  const rng = seeded(playerLvl * 97 + Math.round(playerGear * 100));
  const pPow = lvlMult(playerLvl) * gearMult(playerGear);
  return offsets.map((off, i) => {
    const D = Math.max(1, Math.min(100, playerLvl + off));
    const dPow = lvlMult(D) * gearMult(dungeonGearFrac(D));
    const ratio = pPow / dPow;
    const fights = 3 + Math.floor(rng() * 7); // 3..9 normal fights
    const boss = SUBBOSS[Math.floor(rng() * SUBBOSS.length)];
    const aff = AFFINITY[Math.floor(rng() * AFFINITY.length)];
    const tier = Math.ceil(D / 10);
    return { id: i, D, tier, ratio, v: verdict(ratio), fights, boss, aff, site: SITES[(playerLvl + i) % SITES.length] };
  });
}

export default function DungeonSelect() {
  const [playerLvl, setPlayerLvl] = useState(40);
  const [playerGear, setPlayerGear] = useState(0.45);
  const [picked, setPicked] = useState(null);

  const dungeons = useMemo(() => buildDungeons(playerLvl, playerGear), [playerLvl, playerGear]);
  const pPow = (lvlMult(playerLvl) * gearMult(playerGear)).toFixed(2);

  return (
    <div style={S.root}>
      <div style={S.frame}>
        {/* header */}
        <div style={S.head}>
          <div>
            <div style={S.eyebrow}>EXPEDITION BOARD</div>
            <h1 style={S.h1}>Choose your descent</h1>
            <p style={S.sub}>Five sites surface each cycle — some beneath you, some past your reach. Push if you dare.</p>
          </div>
          <div style={S.playerCard}>
            <div style={S.pcRow}><span style={S.pcLabel}>Roster level</span><span style={S.pcVal}>{playerLvl}</span></div>
            <div style={S.pcRow}><span style={S.pcLabel}>Gear readiness</span><span style={S.pcVal}>{Math.round(playerGear * 100)}%</span></div>
            <div style={{ ...S.pcRow, borderTop: "1px solid #2a2018", paddingTop: 8, marginTop: 4 }}>
              <span style={S.pcLabel}>Effective power</span><span style={{ ...S.pcVal, color: "#e8c979" }}>{pPow}×</span>
            </div>
          </div>
        </div>

        {/* sim controls (mock-only, to feel the gear-is-heavier thesis) */}
        <div style={S.controls}>
          <label style={S.ctrlLabel}>Simulate level
            <input type="range" min="1" max="100" value={playerLvl} onChange={(e) => { setPlayerLvl(+e.target.value); setPicked(null); }} style={S.range} />
            <span style={S.ctrlVal}>{playerLvl}</span>
          </label>
          <label style={S.ctrlLabel}>Simulate gear
            <input type="range" min="0" max="95" value={playerGear * 100} onChange={(e) => { setPlayerGear(+e.target.value / 100); setPicked(null); }} style={S.range} />
            <span style={S.ctrlVal}>{Math.round(playerGear * 100)}%</span>
          </label>
          <div style={S.thesis}>↑ Drag gear low at your own level — watch the “at-level” dungeon slide from Fair to Stretch. Gear is the heavier lever.</div>
        </div>

        {/* the 5 dungeons */}
        <div style={S.grid}>
          {dungeons.map((d) => {
            const t = TONES[d.v.tone];
            const isPicked = picked === d.id;
            return (
              <button key={d.id} onClick={() => setPicked(d.id)} style={{ ...S.card, borderColor: isPicked ? t.bar : "#241b13", boxShadow: isPicked ? `0 0 0 1px ${t.bar}, 0 8px 30px -12px ${t.bar}` : "0 6px 20px -14px #000" }}>
                <div style={S.cardTop}>
                  <div>
                    <div style={{ ...S.tierTag, color: t.text }}>TIER {d.tier} · LV {d.D}</div>
                    <div style={S.site}>{d.site}</div>
                  </div>
                  <div style={{ ...S.affDot, background: d.aff.col }} title={d.aff.c} />
                </div>

                <div style={{ ...S.verdictChip, background: t.chip, color: t.text }}>{d.v.label}</div>
                <div style={S.verdictBlurb}>{d.v.blurb}</div>

                {/* difficulty bar */}
                <div style={S.barTrack}>
                  <div style={{ ...S.barFill, width: `${Math.max(8, Math.min(100, (2 - d.ratio) * 90))}%`, background: t.bar }} />
                </div>

                <div style={S.meta}>
                  <span>{d.fights} fights</span>
                  <span style={S.metaDiv}>·</span>
                  <span>sub-boss: {d.boss.name}</span>
                </div>
              </button>
            );
          })}
        </div>

        {/* detail drawer for the picked dungeon */}
        {picked !== null && (() => {
          const d = dungeons[picked];
          const t = TONES[d.v.tone];
          return (
            <div style={{ ...S.drawer, borderColor: t.bar }}>
              <div style={S.drawerHead}>
                <div>
                  <div style={{ ...S.tierTag, color: t.text }}>TIER {d.tier} · LEVEL {d.D} · {d.v.label.toUpperCase()}</div>
                  <h2 style={S.drawerTitle}>{d.site}</h2>
                </div>
                <div style={{ ...S.affPill, borderColor: d.aff.col, color: d.aff.col }}>{d.aff.c}-tinged</div>
              </div>

              {/* run path: N normal fights -> sub-boss */}
              <div style={S.path}>
                {Array.from({ length: d.fights }).map((_, i) => (
                  <React.Fragment key={i}>
                    <div style={S.node}><div style={S.nodeDot} /><span style={S.nodeLabel}>{i + 1}</span></div>
                    <div style={S.link} />
                  </React.Fragment>
                ))}
                <div style={S.bossNode}>
                  <div style={{ ...S.bossDot, background: t.bar }} />
                  <span style={{ ...S.nodeLabel, color: t.text, fontWeight: 700 }}>BOSS</span>
                </div>
              </div>

              <div style={S.bossCard}>
                <div style={{ ...S.bossTag, background: t.chip, color: t.text }}>{d.boss.tag} CHECK</div>
                <div style={S.bossName}>Ends in {d.boss.name}.</div>
                <div style={S.bossHint}>{d.boss.hint}</div>
              </div>

              <div style={S.rewardRow}>
                <div style={S.rewardBox}><span style={S.rLabel}>Rewards</span><span style={S.rVal}>{d.ratio < 0.92 ? "Rich" : d.ratio < 1.02 ? "Solid" : "Thin"} · staples + gear</span></div>
                <div style={S.rewardBox}><span style={S.rLabel}>Attrition</span><span style={S.rVal}>HP + cooldowns carry across all {d.fights} fights</span></div>
                <button style={{ ...S.enter, background: t.bar }}>Enter descent →</button>
              </div>
            </div>
          );
        })()}

        <div style={S.footnote}>RNG-lite: sites, fight counts (3–9), sub-boss archetype and affinity re-roll each cycle. Level band is fixed (below → at → above) so difficulty is always a legible choice.</div>
      </div>
    </div>
  );
}

const S = {
  root: { minHeight: "100vh", background: "radial-gradient(120% 80% at 50% -10%, #1c1610 0%, #0d0a07 60%)", color: "#e8ddcf", fontFamily: "'Georgia', serif", padding: "32px 16px" },
  frame: { maxWidth: 1040, margin: "0 auto" },
  head: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", gap: 24, flexWrap: "wrap", marginBottom: 20 },
  eyebrow: { fontFamily: "'Courier New', monospace", fontSize: 11, letterSpacing: 3, color: "#8a6f4f" },
  h1: { fontSize: 38, margin: "6px 0 4px", fontWeight: 400, letterSpacing: -0.5, color: "#f2e8d8" },
  sub: { margin: 0, color: "#9d8f7c", fontSize: 15, maxWidth: 440, fontStyle: "italic" },
  playerCard: { background: "#15100b", border: "1px solid #2a2018", borderRadius: 10, padding: "14px 18px", minWidth: 210 },
  pcRow: { display: "flex", justifyContent: "space-between", gap: 20, padding: "3px 0" },
  pcLabel: { fontSize: 12, color: "#8a7a66", fontFamily: "'Courier New', monospace", letterSpacing: 0.5 },
  pcVal: { fontSize: 15, color: "#e8ddcf", fontWeight: 700 },
  controls: { background: "#120e0a", border: "1px solid #241b13", borderRadius: 10, padding: "14px 18px", marginBottom: 24, display: "flex", gap: 28, alignItems: "center", flexWrap: "wrap" },
  ctrlLabel: { display: "flex", alignItems: "center", gap: 10, fontSize: 12, color: "#8a7a66", fontFamily: "'Courier New', monospace", letterSpacing: 1 },
  range: { width: 130, accentColor: "#d9772f" },
  ctrlVal: { color: "#e8c979", fontWeight: 700, minWidth: 30 },
  thesis: { flex: 1, minWidth: 200, fontSize: 12, color: "#7a6b58", fontStyle: "italic" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(180px, 1fr))", gap: 12 },
  card: { textAlign: "left", cursor: "pointer", background: "linear-gradient(180deg, #16110c, #100c08)", border: "1px solid #241b13", borderRadius: 12, padding: 16, transition: "all .15s", color: "inherit", fontFamily: "inherit" },
  cardTop: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 },
  tierTag: { fontFamily: "'Courier New', monospace", fontSize: 10, letterSpacing: 1.5, fontWeight: 700 },
  site: { fontSize: 16, color: "#e8ddcf", marginTop: 4, lineHeight: 1.2 },
  affDot: { width: 10, height: 10, borderRadius: "50%", flexShrink: 0, marginTop: 3, boxShadow: "0 0 8px currentColor" },
  verdictChip: { display: "inline-block", fontFamily: "'Courier New', monospace", fontSize: 11, fontWeight: 700, letterSpacing: 1, padding: "3px 9px", borderRadius: 5, marginBottom: 8 },
  verdictBlurb: { fontSize: 12.5, color: "#9d8f7c", lineHeight: 1.4, minHeight: 34, fontStyle: "italic" },
  barTrack: { height: 4, background: "#241b13", borderRadius: 3, margin: "10px 0 10px", overflow: "hidden" },
  barFill: { height: "100%", borderRadius: 3, transition: "width .2s" },
  meta: { fontSize: 11.5, color: "#7a6b58", fontFamily: "'Courier New', monospace", display: "flex", gap: 6, flexWrap: "wrap" },
  metaDiv: { color: "#463a2c" },
  drawer: { marginTop: 20, background: "linear-gradient(180deg, #16110c, #0f0b07)", border: "1px solid", borderRadius: 14, padding: 22 },
  drawerHead: { display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 18, flexWrap: "wrap", gap: 12 },
  drawerTitle: { fontSize: 26, margin: "6px 0 0", fontWeight: 400, color: "#f2e8d8" },
  affPill: { fontFamily: "'Courier New', monospace", fontSize: 11, letterSpacing: 1, border: "1px solid", borderRadius: 20, padding: "5px 12px" },
  path: { display: "flex", alignItems: "center", flexWrap: "wrap", gap: 0, marginBottom: 18, padding: "4px 0" },
  node: { display: "flex", flexDirection: "column", alignItems: "center", gap: 4 },
  nodeDot: { width: 14, height: 14, borderRadius: "50%", background: "#2f2519", border: "1px solid #463a2c" },
  nodeLabel: { fontSize: 9, color: "#7a6b58", fontFamily: "'Courier New', monospace" },
  link: { width: 22, height: 2, background: "#2a2018" },
  bossNode: { display: "flex", flexDirection: "column", alignItems: "center", gap: 4, marginLeft: 2 },
  bossDot: { width: 20, height: 20, borderRadius: "50%", boxShadow: "0 0 12px currentColor" },
  bossCard: { background: "#0d0a07", border: "1px solid #241b13", borderRadius: 10, padding: 16, marginBottom: 16 },
  bossTag: { display: "inline-block", fontFamily: "'Courier New', monospace", fontSize: 10, fontWeight: 700, letterSpacing: 1.5, padding: "3px 9px", borderRadius: 5, marginBottom: 8 },
  bossName: { fontSize: 18, color: "#f2e8d8", marginBottom: 6 },
  bossHint: { fontSize: 13.5, color: "#9d8f7c", fontStyle: "italic", lineHeight: 1.5 },
  rewardRow: { display: "flex", gap: 12, alignItems: "stretch", flexWrap: "wrap" },
  rewardBox: { flex: 1, minWidth: 150, background: "#0d0a07", border: "1px solid #241b13", borderRadius: 10, padding: "10px 14px", display: "flex", flexDirection: "column", gap: 3 },
  rLabel: { fontSize: 10, color: "#7a6b58", fontFamily: "'Courier New', monospace", letterSpacing: 1 },
  rVal: { fontSize: 14, color: "#d8cbb8" },
  enter: { border: "none", borderRadius: 10, padding: "0 22px", color: "#100c08", fontWeight: 700, fontFamily: "inherit", fontSize: 15, cursor: "pointer", minWidth: 160 },
  footnote: { marginTop: 20, fontSize: 11.5, color: "#5f5343", fontFamily: "'Courier New', monospace", lineHeight: 1.6, textAlign: "center" },
};
