// Phase 2 token assembly + contrast check for DESIGN.md (Verdigris Ledger).
// Runs palette.mjs twice (muted: neutrals + accent; balanced: functional only),
// adds the aliases palette.mjs does not emit, prints the :root block and a
// WCAG report. Exit 1 if any pair misses its target.
// Usage: node .design-foundations/build/phase-2-tokens.mjs
import { execFileSync } from "node:child_process";

const PALETTE = "/Users/gabriel/.claude/plugins/cache/rtd/design-for-ai/4.2.0/scripts/palette.mjs";
const SEED = "165.61"; // dealt hue, round 2 hand 1
const run = (chroma) => {
  const out = execFileSync("node", [PALETTE, "--seed", SEED, "--chroma", chroma, "--harmony", "mono", "--scheme", "light", "--json"]);
  return JSON.parse(out).schemes.light;
};
const muted = run("muted"), balanced = run("balanced");

// ---- color math (same formulas as palette.mjs) ----
const rgb = (h) => [1, 3, 5].map((i) => parseInt(h.slice(i, i + 2), 16) / 255);
const hex = (c) => "#" + c.map((x) => Math.round(Math.min(1, Math.max(0, x)) * 255).toString(16).padStart(2, "0")).join("");
const lin = (x) => (x <= 0.04045 ? x / 12.92 : ((x + 0.055) / 1.055) ** 2.4);
const lum = (h) => { const [r, g, b] = rgb(h).map(lin); return 0.2126 * r + 0.7152 * g + 0.0722 * b; };
const ratio = (a, b) => { const [x, y] = [lum(a), lum(b)].sort((p, q) => q - p); return (x + 0.05) / (y + 0.05); };
function oklab(h) {
  const [r, g, b] = rgb(h).map(lin);
  const l = Math.cbrt(0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b);
  const m = Math.cbrt(0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b);
  const s = Math.cbrt(0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b);
  return [0.2104542553 * l + 0.793617785 * m - 0.0040720468 * s,
          1.9779984951 * l - 2.428592205 * m + 0.4505937099 * s,
          0.0259040371 * l + 0.7827717662 * m - 0.808675766 * s];
}
const lch = (h) => { const [L, a, b] = oklab(h); return { L, C: Math.hypot(a, b), H: ((Math.atan2(b, a) * 180) / Math.PI + 360) % 360 }; };
function fromOklab([L, a, b]) {
  const l = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3;
  const m = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3;
  const s = (L - 0.0894841775 * a - 1.291485548 * b) ** 3;
  return hex([4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
    -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
    -0.0041960863 * l - 0.7034186147 * m + 1.707614701 * s]
    .map((x) => (x <= 0.0031308 ? 12.92 * x : 1.055 * x ** (1 / 2.4) - 0.055)));
}
// CSS color-mix(in oklab, A p%, B): linear in OKLab.
const mix = (a, b, p) => { const A = oklab(a), B = oklab(b); return fromOklab(A.map((v, i) => v * p + B[i] * (1 - p))); };

// ---- token block ----
const T = {};
for (const [k, v] of Object.entries(muted.tokens)) if (/^--(neutral|accent)-/.test(k)) T[k] = v;
for (const [k, v] of Object.entries(balanced.tokens)) if (/^--(error|success|warning|info)-/.test(k)) T[k] = v;

const MIX_PCT = 0.45; // share of neutral-11 in the control boundary
const alias = {
  "--background": "var(--neutral-1)", "--surface": "var(--neutral-2)", "--surface-hover": "var(--neutral-3)",
  "--surface-active": "var(--neutral-4)", "--rule": "var(--neutral-5)", "--border-subtle": "var(--neutral-6)",
  "--border": "var(--neutral-7)", "--border-strong": "var(--neutral-8)",
  "--border-control": `color-mix(in oklab, var(--neutral-11) ${MIX_PCT * 100}%, var(--neutral-8))`,
  "--text": "var(--neutral-12)", "--text-secondary": "var(--neutral-11)", "--text-muted": "var(--neutral-11)",
  "--accent-bg-subtle": "var(--accent-3)", "--accent-selected": "var(--accent-4)",
  "--accent-solid": "var(--accent-9)", "--accent-solid-hover": "var(--accent-10)", "--accent-edge": "var(--accent-11)",
  "--accent-text": "var(--accent-11)", "--focus": "var(--accent-11)",
  "--data-1": "#2a78d6", // series-1, pinned by the plan; data ink only, never UI
};
const css = [":root {", ...Object.entries({ ...T, ...alias }).map(([k, v]) => `  ${k}: ${v};`), "}"].join("\n");

// resolve an alias to a hex for checking
const val = (name) => {
  if (name === "--border-control") return mix(T["--neutral-11"], T["--neutral-8"], MIX_PCT);
  const v = alias[name] ?? T[name];
  const ref = /^var\((--[\w-]+)\)$/.exec(v);
  return ref ? val(ref[1]) : v;
};

// ---- checks ----
const rows = [];
const pair = (fg, bg, target, note = "") => {
  const r = ratio(val(fg), val(bg));
  rows.push({ ok: r >= target, line: `${r >= target ? "PASS" : "FAIL"}  ${fg} ${val(fg)} on ${bg} ${val(bg)}: ${r.toFixed(2)}:1 (target ${target}:1)${note}` });
};
for (const bg of ["--background", "--surface", "--surface-hover", "--surface-active", "--accent-bg-subtle", "--accent-selected"]) {
  pair("--text", bg, 4.5); pair("--text-muted", bg, 4.5); pair("--accent-text", bg, 4.5);
}
pair("--accent-on-solid", "--accent-solid", 4.5, "  (primary button label)");
pair("--accent-on-solid", "--accent-solid-hover", 4.5, "  (primary button hover)");
for (const f of ["error", "success", "warning", "info"]) {
  pair(`--${f}-11`, "--background", 4.5); pair(`--${f}-11`, "--surface", 4.5); pair(`--${f}-11`, `--${f}-3`, 4.5);
}
// non-text: focus ring + control boundaries (WCAG 1.4.11)
for (const bg of ["--background", "--surface", "--surface-hover", "--accent-bg-subtle", "--accent-selected"]) pair("--focus", bg, 3);
pair("--focus", "--accent-solid", 3, "  (ring offset 2px sits on background; checked against fill too)");
for (const bg of ["--background", "--surface"]) { pair("--border-control", bg, 3); pair("--accent-edge", bg, 3, "  (primary button edge)"); }
for (const f of ["error", "success", "warning", "info"]) pair(`--${f}-11`, "--background", 3, "  (status glyph)");

// ---- hue checks ----
const s1 = lch("#2a78d6"), acc = lch(val("--accent-solid")), accT = lch(val("--accent-text")), suc = lch(val("--success-11"));
const dH = (a, b) => { const d = Math.abs(a - b) % 360; return d > 180 ? 360 - d : d; };
const dE = (a, b) => Math.hypot(...oklab(a).map((v, i) => v - oklab(b)[i]));
const hueOk = dH(acc.H, s1.H) >= 40;

console.log(css);
console.log("\n/* Contrast report (WCAG 2.x), light only");
rows.forEach((r) => console.log("   " + r.line));
console.log(`   ${hueOk ? "PASS" : "FAIL"}  accent hue ${acc.H.toFixed(1)} vs series-1 #2a78d6 hue ${s1.H.toFixed(1)}: delta ${dH(acc.H, s1.H).toFixed(1)} deg (target >= 40)`);
console.log(`   INFO  accent-text oklch(${accT.L.toFixed(3)} ${accT.C.toFixed(3)} ${accT.H.toFixed(1)}) vs success-11 oklch(${suc.L.toFixed(3)} ${suc.C.toFixed(3)} ${suc.H.toFixed(1)}): dE_ok ${dE(val("--accent-text"), val("--success-11")).toFixed(3)}`);
console.log("*/");
process.exit(rows.every((r) => r.ok) && hueOk ? 0 : 1);
