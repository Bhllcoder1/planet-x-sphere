/**
 * Alan D - Görev 05-08 & 10-09: Bayrak (Flag) Katmanı Düğmeleri, Table 16 Bitleri,
 * İki Ana Maske Profili (Centroid / Mover-search) ve Kalabalık Alan Uyarısı
 *
 * Kural [V: PLAN_spherex_v3.md §2.1, SITE_SPEC W9]:
 * - Hiçbir piksel gizlenmez; bayrak katmanı yalnızca renkli kenarlık (outline) olarak çizilir.
 * - Fit-mask oranı > %50 olduğunda (örn. gc3 karesi %67.8) "Unusable for astrometry / Crowded field"
 *   uyarısı gösterilir.
 */

export const TABLE16_FLAGS = [
  { bit: 0, name: "TRANSIENT", color: "#f0e442", role: "caution" },
  { bit: 1, name: "OVERFLOW", color: "#d55e00", role: "centroid_masked" },
  { bit: 2, name: "SUR_ERROR", color: "#d55e00", role: "fit_masked" },
  { bit: 6, name: "NONFUNC", color: "#d55e00", role: "fit_masked" },
  { bit: 7, name: "DICHROIC", color: "#e69f00", role: "centroid_masked" },
  { bit: 9, name: "MISSING_DATA", color: "#d55e00", role: "fit_masked" },
  { bit: 10, name: "HOT", color: "#d55e00", role: "fit_masked" },
  { bit: 11, name: "COLD", color: "#56b4e9", role: "fit_masked" },
  { bit: 14, name: "NORM_FACTOR", color: "#e69f00", role: "fit_masked" },
  { bit: 15, name: "PERSIST", color: "#cc79a7", role: "caution" },
  { bit: 19, name: "OUTLIER", color: "#009e73", role: "never_mask_mover" },
  { bit: 20, name: "CROSSTALK", color: "#f0e442", role: "caution" },
  { bit: 21, name: "SOURCE", color: "#56b4e9", role: "never_mask_mover" },
  { bit: 22, name: "GHOST", color: "#e69f00", role: "centroid_masked" },
  { bit: 23, name: "GHOST_FPA", color: "#e69f00", role: "centroid_masked" },
  { bit: 24, name: "GHOST_EXT", color: "#e69f00", role: "centroid_masked" },
  { bit: 25, name: "STREAK", color: "#d55e00", role: "centroid_masked" },
];

export const BASE_FIT_MASK = 0x3c028e44 >>> 0;
export const CENTROID_PROFILE_MASK = (BASE_FIT_MASK | (1 << 1) | (1 << 7) | (1 << 22) | (1 << 23) | (1 << 24) | (1 << 25)) >>> 0;
export const MOVER_SEARCH_PROFILE_MASK = BASE_FIT_MASK >>> 0;
export const BACKGROUND_PROFILE_MASK = (CENTROID_PROFILE_MASK | (1 << 19) | (1 << 21)) >>> 0;

export const FLAG_PRESETS = {
  centroid: {
    id: "centroid",
    label: "Centroid / Photometry Profile",
    mask: CENTROID_PROFILE_MASK,
    hex: `0x${CENTROID_PROFILE_MASK.toString(16).toUpperCase().padStart(8, "0")}`,
  },
  mover_search: {
    id: "mover_search",
    label: "Mover-Search Profile (OUTLIER & SOURCE Never Masked)",
    mask: MOVER_SEARCH_PROFILE_MASK,
    hex: `0x${MOVER_SEARCH_PROFILE_MASK.toString(16).toUpperCase().padStart(8, "0")}`,
  },
  background: {
    id: "background",
    label: "Background Profile",
    mask: BACKGROUND_PROFILE_MASK,
    hex: `0x${BACKGROUND_PROFILE_MASK.toString(16).toUpperCase().padStart(8, "0")}`,
  },
};

export function decodeFlagWord(flagUint32) {
  const w = Number(flagUint32) >>> 0;
  const active = [];
  for (const item of TABLE16_FLAGS) {
    if (((w >>> item.bit) & 1) === 1) {
      active.push(item.name);
    }
  }
  return active;
}

export function evaluateFlagWindowStats(flagArray, unusableThreshold = 0.5, crowdedSourceThreshold = 0.5) {
  const n = flagArray.length || 1;
  let fitCount = 0;
  let centroidCount = 0;
  let sourceCount = 0;
  let outlierCount = 0;

  for (let i = 0; i < flagArray.length; i++) {
    const w = Number(flagArray[i]) >>> 0;
    if ((w & BASE_FIT_MASK) !== 0) fitCount++;
    if ((w & CENTROID_PROFILE_MASK) !== 0) centroidCount++;
    if (((w >>> 21) & 1) !== 0) sourceCount++;
    if (((w >>> 19) & 1) !== 0) outlierCount++;
  }

  const fitFraction = fitCount / n;
  const centroidFraction = centroidCount / n;
  const sourceFraction = sourceCount / n;
  const unusableForAstrometry = fitFraction > unusableThreshold;
  const crowdedField = sourceFraction > crowdedSourceThreshold;

  return {
    totalPixels: flagArray.length,
    fitMaskedPixels: fitCount,
    centroidMaskedPixels: centroidCount,
    outlierPixels: outlierCount,
    fitFraction,
    centroidFraction,
    sourceFraction,
    unusableForAstrometry,
    crowdedField,
    bannerText:
      unusableForAstrometry || crowdedField
        ? `Unusable for astrometry / Crowded field (fit-mask ${(fitFraction * 100).toFixed(1)}%, SOURCE ${(sourceFraction * 100).toFixed(1)}%)`
        : null,
  };
}
