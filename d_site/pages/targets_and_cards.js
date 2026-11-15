/**
 * Alan D - Görev 10-02, 10-06, 10-13, 10-14, 10-16, 11-23:
 * - 5 Hazır Yarışma Hedefi Kartı ve Kapsam/Hata Durumları (10-02, 10-14)
 * - Kare Başına Metadata Şeridi (10-06)
 * - Yığın (Stack) ve Fark (A-B Diff) Görünümü Seçicisi - Mod S (10-13)
 * - Arama Geçmişinde 160x160 Küçük Resim (Thumbnail) Gösterimi (11-23)
 */

export const COMPETITION_TARGETS = [
  {
    id: "barnard",
    name: "Barnard's Star",
    raDeg: 269.452075,
    decDeg: 4.693391,
    pmRaMasYr: -801.55,
    pmDecMasYr: 10362.39,
    coverageStatus: "verified",
    honestyTag: "[V: s0_A, s0_B, s0_C]",
    totalFrames: 358,
    totalPasses: 3,
    release: "DR1 + QR3 (7.0.5)",
    detectionOutcome: "Detected (S/N > 80 in wings; 2×2 NaN saturated core)",
    motionSummary: "Pass 0→1: ~0.96 px, Pass 0→2: ~1.70 px (agrees with Gaia DR3 within σ)",
    caveats: "2×2 NaN core in IMAGE and VARIANCE; measured via forced ePSF wing fit ('saturated-fit' badge).",
  },
  {
    id: "eps_indi_b",
    name: "Epsilon Indi B",
    raDeg: 330.872408,
    decDeg: -56.793797,
    pmRaMasYr: 3966.67,
    pmDecMasYr: -2536.19,
    coverageStatus: "verified",
    honestyTag: "[V: s0_A]",
    totalFrames: 458,
    totalPasses: 4,
    release: "DR1 + QR3 (7.0.5)",
    detectionOutcome: "Unresolved binary brown dwarf pair (Ba+Bb) next to bright ε Indi A",
    motionSummary: "~4.7 arcsec/yr (~0.76 px/yr); shown as one blended source",
    caveats: "Unresolved pair next to bright ε Indi A; halo/crosstalk caution flags monitored.",
  },
  {
    id: "wise_0855",
    name: "WISE 0855−0714",
    raDeg: 133.795129,
    decDeg: -7.245147,
    pmRaMasYr: -8118.0,
    pmDecMasYr: 680.0,
    coverageStatus: "not_measured",
    honestyTag: "[NV: sync TAP timed out in s0_A; async TAP 01-02 queued]",
    totalFrames: null,
    totalPasses: null,
    release: "DR1 / QR3",
    detectionOutcome: "not measured (sync TAP failed; forced photometry in D5/D6 pending 04-04)",
    motionSummary: "Expected ~8.1 arcsec/yr (~0.66 px per 6 months) [arith]",
    caveats: "Coldest known brown dwarf (~250 K). If S/N < 3 in SPHEREx bands, reported honestly as not detected — never replaced by another target.",
  },
  {
    id: "rw_aur",
    name: "RW Aurigae",
    raDeg: 76.956525,
    decDeg: 30.401408,
    pmRaMasYr: 3.4,
    pmDecMasYr: -20.8,
    coverageStatus: "not_measured",
    honestyTag: "[NV: sync TAP timed out in s0_A; async TAP 01-02 queued]",
    totalFrames: null,
    totalPasses: null,
    release: "DR1 / QR3",
    detectionOutcome: "not measured (T Tauri variable star; λ-binned light curve panel mandatory)",
    motionSummary: "Negligible proper motion; primary signal is flux variability across passes",
    caveats: "Variable star: shared sequence stretch limits required so brightness changes are not hidden by per-frame normalization.",
  },
  {
    id: "r_dra",
    name: "R Draconis",
    raDeg: 248.172546,
    decDeg: 66.754983,
    pmRaMasYr: -11.2,
    pmDecMasYr: -33.1,
    coverageStatus: "not_measured",
    honestyTag: "[NV: sync TAP timed out in s0_A; async TAP 01-02 queued]",
    totalFrames: null,
    totalPasses: null,
    release: "DR1 / QR3",
    detectionOutcome: "not measured (Mira-type variable star; λ-binned light curve panel mandatory)",
    motionSummary: "Small proper motion; large-amplitude infrared variability",
    caveats: "Variable star warning: wavelength changes with detector stepping inside a pass; compare identical detector/λ bins across passes.",
  },
];

export function formatTargetCardViewModel(target, simulatedTapState = null) {
  const fallback = "not measured";
  const state = simulatedTapState || target.coverageStatus;

  let statusBadge = "Verified Coverage [V]";
  let statusBanner = null;
  if (state === "archive_busy") {
    statusBadge = "Archive Busy — Retry Queued";
    statusBanner = "Archive busy (TAP timeout / HTTP 502): retry queued. This is NOT 'no coverage'.";
  } else if (state === "no_coverage") {
    statusBadge = "No Coverage in Release (0 frames)";
    statusBanner = `SPHEREx does not show ${target.name} in release ${target.release} (0 frames in the field).`;
  } else if (state === "not_measured" || state === "processing") {
    statusBadge = "Coverage Not Verified [NV]";
    statusBanner = "Sync TAP timed out; frame count is marked 'not measured' until async TAP completes.";
  }

  return {
    id: target.id,
    name: target.name,
    coordinatesExact: `RA ${target.raDeg.toFixed(6)}°, Dec ${target.decDeg >= 0 ? "+" : ""}${target.decDeg.toFixed(6)}°`,
    framesLabel: target.totalFrames !== null && target.totalFrames !== undefined ? String(target.totalFrames) : fallback,
    passesLabel: target.totalPasses !== null && target.totalPasses !== undefined ? String(target.totalPasses) : fallback,
    detectionOutcome: target.detectionOutcome || fallback,
    motionSummary: target.motionSummary || fallback,
    caveats: target.caveats || fallback,
    honestyTag: target.honestyTag,
    statusBadge,
    statusBanner,
  };
}

/**
 * Görev 10-06: Kare başına metadata şeridi. Eksik alanlara 'not measured' / 'ölçülmedi' yazar,
 * hiçbir zaman değer uydurmaz.
 */
export function formatFrameMetadataStrip(meta = {}, lang = "en") {
  const missing = lang === "tr" ? "ölçülmedi" : "not measured";
  const valOrMissing = (v) => (v !== undefined && v !== null && v !== "" && !Number.isNaN(v) ? String(v) : missing);

  const cwave = meta.cwave_um !== undefined && meta.cwave_um !== null ? Number(meta.cwave_um).toFixed(3) : null;
  const cband = meta.cband_um !== undefined && meta.cband_um !== null ? Number(meta.cband_um).toFixed(3) : null;
  const wavelength = cwave && cband ? `${cwave} ± ${cband} μm` : cwave ? `${cwave} μm` : missing;

  return {
    utcDate: valOrMissing(meta.utc_date),
    mjdAvg: meta.mjd_avg !== undefined && meta.mjd_avg !== null ? Number(meta.mjd_avg).toFixed(5) : missing,
    detector: valOrMissing(meta.detector ? `D${String(meta.detector).replace(/^D/i, "")}` : null),
    wavelength,
    passId: meta.pass_id !== undefined && meta.pass_id !== null ? `Pass ${meta.pass_id}` : missing,
    release: valOrMissing(meta.release),
    procTag: valOrMissing(meta.procver),
  };
}

/**
 * Görev 10-13: Yığın (stack) ve Fark (diff = A - B) görünümü (Mod S).
 * - Yalnızca aynı dedektör ve uyumlu dalga boyu çiftlerine izin verir.
 * - Her zaman "S: resampled, view only, no astrometry" uyarısı taşır ve ölçüm panelini gizler.
 */
export function buildModeSStackDiffDescriptor({
  subMode = "stack", // "stack" | "diff"
  detectorA = "D2",
  detectorB = "D2",
  passA = 0,
  passB = 1,
  wavelengthChannelsUm = [1.82, 1.85, 1.88],
}) {
  if (detectorA !== detectorB) {
    return {
      valid: false,
      mode: "S",
      error: `Incompatible pair: ${detectorA} vs ${detectorB}. Difference/Stack requires identical detector and wavelength channel.`,
      showMeasurementPanel: false,
    };
  }
  if (subMode === "diff" && passA === passB) {
    return {
      valid: false,
      mode: "S",
      error: "Difference mode (A − B) requires two distinct passes.",
      showMeasurementPanel: false,
    };
  }
  return {
    valid: true,
    mode: "S",
    subMode,
    detector: detectorA,
    passA,
    passB: subMode === "diff" ? passB : null,
    wavelengthsUsedUm: wavelengthChannelsUm,
    bannerText: "S: resampled, view only, no astrometry",
    showMeasurementPanel: false, // Mod S'de ölçüm paneli kesinlikle kapalıdır
  };
}

/**
 * Görev 11-23: Arama geçmişi satırı ve 160x160 küçük resim (thumbnail) modeli.
 */
export function buildHistoryEntryRow(entry) {
  return {
    id: entry.id,
    timestampUtc: entry.ts,
    targetLabel: entry.target_name || `RA ${Number(entry.ra).toFixed(4)}°, Dec ${Number(entry.dec).toFixed(4)}°`,
    thumbnailUrl: entry.thumbnail_path || `/cache/thumbnails/${entry.id}_160x160.png`,
    thumbnailWidth: 160,
    thumbnailHeight: 160,
    thumbnailDisclaimer: "overview copy, not measurement",
    settingsSummary: `Mode ${String(entry.mode || "N").toUpperCase()} | ${entry.det || "D2"} | z=${entry.zoom || 16} | bg=${entry.bg || "zodi"} | ${entry.clip || "percent"} (${entry.lo ?? 0.5}/${entry.hi ?? 99.5}) | ${entry.stretch || "asinh"}`,
    outcome: entry.outcome || "found",
    restoreQueryString: entry.query,
  };
}
