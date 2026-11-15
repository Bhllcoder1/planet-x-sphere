/**
 * Alan D - Görev 05-11, 05-17, 05-20, 10-08: Gerdirme (Stretch) Arayüzü, Kırpma Modları,
 * ZODI Arka Plan Anahtarı, Tema Seçici ve URL Durumu (W8, W19)
 *
 * Kural [V: DISPLAY_LAYER_DESIGN.md §2]:
 * - Ölçüm verisi asla değiştirilmez; gerdirme kopya/LUT üzerinde çalışır.
 * - ZODI arka plan anahtarı: 'raw' | 'zodi' (varsayılan, rozetli) | 'flat'
 * - Kırpma kapsamı: 'sequence' (ortak limit, varsayılan) | 'frame' (kare başına)
 */

export const DEFAULT_DISPLAY_STATE = {
  bg: "zodi",             // raw | zodi | flat (05-20)
  clip: "percent",        // fixed | percent | adapt | zscale (05-17)
  scope: "sequence",      // sequence (ortak) | frame (kare başına) (05-17)
  stretch: "asinh",       // asinh | linear | zscale (05-11, 10-08)
  lo: 0.5,
  hi: 99.5,
  a: 0.1,                 // asinh doğrusallık parametresi (05-17)
  invert: false,
  theme: "dark",          // dark | light (05-11, 10-08)
  view: "n",              // n | rk | s (05-18 WiseView uyumlu)
  zoom: 16,
  grid: true,
  gaia: true,
  cen: true,
  flags: false,
  embed: false,
};

export function maximizeDynamicRangePreset(currentState = DEFAULT_DISPLAY_STATE) {
  return {
    ...currentState,
    clip: "percent",
    lo: 0.5,
    hi: 99.5,
    stretch: "asinh",
    a: 0.1,
  };
}

export function getBackgroundBadge(bgMode) {
  if (bgMode === "zodi") {
    return "ZODI-subtracted (display only, MJy/sr)";
  }
  if (bgMode === "flat") {
    return "ZODI + flat median subtracted (display only, MJy/sr)";
  }
  return null;
}

export function applyStretchValue(normX, stretchMode = "asinh", asinhA = 0.1, invert = false) {
  const clamped = Math.max(0.0, Math.min(1.0, Number(normX)));
  let y = clamped;
  if (stretchMode === "asinh") {
    const a = Math.max(1e-6, Number(asinhA));
    y = Math.asinh(clamped / a) / Math.asinh(1.0 / a);
  }
  if (invert) {
    y = 1.0 - y;
  }
  return y;
}

export function serializeDisplayStateToUrlQuery(state = DEFAULT_DISPLAY_STATE) {
  const merged = { ...DEFAULT_DISPLAY_STATE, ...state };
  const params = new URLSearchParams();
  params.set("bg", String(merged.bg));
  params.set("clip", String(merged.clip));
  params.set("scope", String(merged.scope));
  params.set("stretch", String(merged.stretch));
  params.set("lo", String(merged.lo));
  params.set("hi", String(merged.hi));
  params.set("a", String(merged.a));
  params.set("invert", merged.invert ? "1" : "0");
  params.set("theme", String(merged.theme));
  params.set("view", String(merged.view));
  params.set("zoom", String(merged.zoom));
  params.set("grid", merged.grid ? "1" : "0");
  params.set("gaia", merged.gaia ? "1" : "0");
  params.set("cen", merged.cen ? "1" : "0");
  params.set("flags", merged.flags ? "1" : "0");
  if (merged.embed) params.set("embed", "1");
  return params.toString();
}

export function parseDisplayStateFromUrlQuery(queryString) {
  const params = new URLSearchParams(queryString.startsWith("?") ? queryString.slice(1) : queryString);
  const out = { ...DEFAULT_DISPLAY_STATE };

  if (params.has("bg")) out.bg = params.get("bg");
  if (params.has("clip")) out.clip = params.get("clip");
  if (params.has("scope")) out.scope = params.get("scope");
  if (params.has("stretch")) out.stretch = params.get("stretch");
  if (params.has("lo")) out.lo = Number(params.get("lo"));
  if (params.has("hi")) out.hi = Number(params.get("hi"));
  if (params.has("a")) out.a = Number(params.get("a"));
  if (params.has("invert")) out.invert = params.get("invert") === "1" || params.get("invert") === "true";
  if (params.has("theme")) out.theme = params.get("theme");
  if (params.has("view")) out.view = params.get("view");
  if (params.has("zoom")) out.zoom = Number(params.get("zoom"));
  if (params.has("grid")) out.grid = params.get("grid") === "1";
  if (params.has("gaia")) out.gaia = params.get("gaia") === "1";
  if (params.has("cen")) out.cen = params.get("cen") === "1";
  if (params.has("flags")) out.flags = params.get("flags") === "1";
  if (params.has("embed")) out.embed = params.get("embed") === "1";

  return out;
}
