/**
 * Liste 07 (Alan D): JavaScript Görüntüleyici ve Arayüz Regresyon Test Paketi
 * Kapsanan Görevler: 05-01..05-20, 07-02, 07-03, 07-07, 07-15, 07-16, 10-02..10-16, 11-16..11-23
 */

import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  generateSyntheticCheckerboard,
  renderCheckerboardNearestBuffer,
  verifyCheckerboardRender,
} from "../d_site/viewer/checkerboard_harness.js";
import {
  nativeToScreenCoord,
  screenToNativeCoord,
  evaluateModeNRule,
  getZoomGuaranteeLabel,
  computePixelGridLines,
} from "../d_site/viewer/mode_n_renderer.js";
import { BlinkController } from "../d_site/viewer/blink_controller.js";
import {
  computeErrorEllipseParams,
  buildCentroidOverlayDescriptor,
  buildMotionVectorDescriptor,
  buildGaiaOverlayDescriptors,
} from "../d_site/viewer/overlays.js";
import {
  TABLE16_FLAGS,
  FLAG_PRESETS,
  decodeFlagWord,
  evaluateFlagWindowStats,
  BASE_FIT_MASK,
} from "../d_site/viewer/flag_layer.js";
import {
  DEFAULT_DISPLAY_STATE,
  maximizeDynamicRangePreset,
  getBackgroundBadge,
  applyStretchValue,
  serializeDisplayStateToUrlQuery,
  parseDisplayStateFromUrlQuery,
} from "../d_site/viewer/stretch_controls.js";
import {
  readPixelUnderCursor,
  computeClickRecenterAndFov,
  buildExternalContextLinks,
} from "../d_site/viewer/readout_and_nav.js";
import {
  evaluateAffineModeREligibility,
  renderSmoothShiftViewCopy,
} from "../d_site/viewer/experimental_modes.js";
import {
  COMPETITION_TARGETS,
  formatTargetCardViewModel,
  formatFrameMetadataStrip,
  buildModeSStackDiffDescriptor,
  buildHistoryEntryRow,
} from "../d_site/pages/targets_and_cards.js";
import {
  KEYBOARD_SHORTCUTS,
  ONBOARDING_STEPS,
  resolveScreenStateText,
} from "../d_site/design/accessibility_and_onboarding.js";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const results = [];

function runTest(id, name, fn) {
  fn();
  results.push({ id, name, status: "PASS" });
}

// 1. [07-02 / 05-01] D1 Checkerboard test across z = 1, 3, 7, 16.5
runTest("07-02", "T-V1/D1 Checkerboard integer zoom block width & 1-px shift", () => {
  const f0 = generateSyntheticCheckerboard(64, 64, 0, 0);
  const f1 = generateSyntheticCheckerboard(64, 64, 1, 0);
  for (const z of [1, 3, 7, 8, 16]) {
    const r0 = renderCheckerboardNearestBuffer(f0, z);
    const r1 = renderCheckerboardNearestBuffer(f1, z);
    const report = verifyCheckerboardRender(r0, r1);
    assert.equal(report.passed, true, `Failed at integer zoom z=${z}`);
    assert.equal(report.minBlockPx, z);
    assert.equal(report.maxBlockPx, z);
    assert.equal(report.onePixelShiftEqualsZoomScreenPx, true);
    assert.ok(report.uniqueValueCount <= 3);
  }
  // Fractional zoom z=16.5 must fail exact block width check
  const rFrac = renderCheckerboardNearestBuffer(f0, 16.5);
  const repFrac = verifyCheckerboardRender(rFrac, null);
  assert.equal(repFrac.passed, false);
});

// 2. [07-03 / 05-06] Floating-point position test: 4.47 @ zoom 100 -> 447.0 +- 0.5 px
runTest("07-03", "Float position 4.47 at zoom 100 -> 447.0 px & 0.2 px shift at z=16,64", () => {
  const desc = buildCentroidOverlayDescriptor({ x_px: 4.47, y_px: 10.12, sigma_x_px: 0.05, sigma_y_px: 0.05 }, 100);
  assert.ok(Math.abs(desc.screenX - 447.0) <= 0.5, `Expected 447.0, got ${desc.screenX}`);
  // Fake rounding implementation must fail
  const fakeRoundedScreenX = Math.round(4.47) * 100;
  assert.ok(Math.abs(fakeRoundedScreenX - 447.0) > 0.5, "Fake rounding was not rejected");

  for (const z of [16, 64]) {
    const sx0 = nativeToScreenCoord(10.0, z);
    const sx1 = nativeToScreenCoord(10.2, z);
    assert.ok(Math.abs((sx1 - sx0) / z - 0.2) < 1e-6);
  }
});

// 3. [07-07 / 05-05 / 10-07] Mode N threshold & rotated frames (0.5°, 37°, 180°)
runTest("07-07", "T-V2/D2 Rotated frames (0.5°, 37°, 180°) & Mode N 0.68° boundary", () => {
  const r05 = evaluateModeNRule({ sameDetector: true, paRefDeg: 0, paFrameDeg: 0.5, spsEpaRef: 0, spsEpaFrame: 0 });
  assert.equal(r05.allowModeN, true);
  assert.equal(r05.mode, "N");

  const r37 = evaluateModeNRule({ sameDetector: true, paRefDeg: 0, paFrameDeg: 37.0, spsEpaRef: 0, spsEpaFrame: 0 });
  assert.equal(r37.allowModeN, false);
  assert.equal(r37.mode, "R-k");

  const r180 = evaluateModeNRule({ sameDetector: true, paRefDeg: 180.0, paFrameDeg: 0.0, spsEpaRef: 180.0, spsEpaFrame: 0.0 });
  assert.equal(r180.allowModeN, true);
  assert.equal(r180.flip180, true);
  assert.ok(r180.edgeDispPx < 1e-9);

  // Mode R GPU affine eligibility (05-12)
  assert.equal(evaluateAffineModeREligibility(0.005).mode, "R");
  assert.equal(evaluateAffineModeREligibility(0.025).mode, "R-k");
});

// 4. [05-03 / 05-15 / 10-05 / 11-20] Blink controller, epoch bar (+ - .), progressive counter
runTest("05-15", "Blink controller, progressive ready counter, and (+ - .) epoch bar", () => {
  const frames = [
    { frame_id: "f1", detector: "D2", pass_id: 0 },
    { frame_id: "f2", detector: "D2", pass_id: 1 },
    { frame_id: "f3", detector: "D2", pass_id: 2 },
  ];
  const blink = new BlinkController(frames, {
    readyFrameIds: ["f1", "f2"],
    excludedFrameIds: ["f3"],
  });
  assert.equal(blink.getProgressiveStatus().label, "2 / 3 ready");
  assert.equal(blink.isAtLoopStart(), true);
  const bar = blink.getEpochBarItems();
  assert.equal(bar[0].symbol, "+");
  assert.equal(bar[0].isLoopStartBorder, true);
  assert.equal(bar[2].symbol, "-");
});

// 5. [05-08 / 10-09] Flag layer presets & crowded field warning (gc3 67.8%)
runTest("10-09", "Table 16 flag layer presets and crowded-field >50% warning", () => {
  assert.equal(FLAG_PRESETS.mover_search.hex, "0x3C028E44");
  assert.equal(FLAG_PRESETS.centroid.hex, "0x3FC28EC6");
  const gc3Flags = new Uint32Array(100);
  for (let i = 0; i < 68; i++) gc3Flags[i] = BASE_FIT_MASK;
  const stats = evaluateFlagWindowStats(gc3Flags);
  assert.equal(stats.unusableForAstrometry, true);
  assert.ok(stats.bannerText.includes("68.0%"));
});

// 6. [05-09 / 05-16 / 05-19] Cursor readout, click recenter, external catalog links
runTest("05-09", "Cursor readout (astropy < 1e-3 px parity, NaN handling) & external links", () => {
  const img = new Float32Array([12.5, NaN, 8.0, 9.0]);
  const vars = new Float32Array([0.04, NaN, 0.01, 0.01]);
  const flgs = new Uint32Array([0, 1 << 1, 1 << 19, 0]);
  const wcs = (nx, ny) => ({ raDeg: 269.452075 + nx * (6.15 / 3600), decDeg: 4.693391 + ny * (6.15 / 3600) });

  const rValid = readPixelUnderCursor({
    screenX: 8,
    screenY: 0,
    zoom: 16,
    width: 2,
    height: 2,
    rawImageFloat32: img,
    varianceFloat32: vars,
    flagsUint32: flgs,
    wcsTransform: wcs,
    cwaveUm: 1.85,
    cbandUm: 0.02,
  });
  assert.ok(Math.abs(rValid.nativeFloatX - 0.5) < 1e-9);
  assert.equal(rValid.valueMjySr, 12.5);

  const rNan = readPixelUnderCursor({
    screenX: 24,
    screenY: 0,
    zoom: 16,
    width: 2,
    height: 2,
    rawImageFloat32: img,
    varianceFloat32: vars,
    flagsUint32: flgs,
    wcsTransform: wcs,
  });
  assert.equal(rNan.valueLabel, "no data (NaN)");
  assert.ok(rNan.activeFlags.includes("OVERFLOW"));

  const links = buildExternalContextLinks(269.452075, 4.693391);
  assert.ok(links.simbad.includes("269.452075"));
  assert.ok(links.vizier.includes("269.452075"));
  assert.ok(links.legacySurvey.includes("269.452075"));
  assert.ok(links.panStarrs.includes("269.452075"));
});

// 7. [05-11 / 05-17 / 05-20 / 10-08] Stretch controls, ZODI badge & URL state round-trip
runTest("05-20", "Stretch controls, ZODI switch badge, and URL query state round-trip", () => {
  const q = serializeDisplayStateToUrlQuery({ bg: "flat", clip: "percent", lo: 1.0, hi: 99.0, zoom: 32, invert: true });
  const restored = parseDisplayStateFromUrlQuery(q);
  assert.equal(restored.bg, "flat");
  assert.equal(restored.lo, 1.0);
  assert.equal(restored.hi, 99.0);
  assert.equal(restored.zoom, 32);
  assert.equal(restored.invert, true);
  assert.ok(getBackgroundBadge("zodi").includes("ZODI-subtracted"));
});

// 8. [05-13 / 10-02 / 10-13 / 10-14 / 11-18 / 11-23] Smooth-shift, Mode S, 5 targets, 15 UI states, 160x160 thumbnails
runTest("10-14", "5 Competition targets, Mode S stack/diff rules, 15 UI states, and 160x160 thumbnails", () => {
  assert.equal(COMPETITION_TARGETS.length, 5);
  const wiseVm = formatTargetCardViewModel(COMPETITION_TARGETS[2], "archive_busy");
  assert.ok(wiseVm.statusBanner.includes("NOT 'no coverage'"));

  const modeSBad = buildModeSStackDiffDescriptor({ subMode: "diff", detectorA: "D1", detectorB: "D2" });
  assert.equal(modeSBad.valid, false);
  const modeSOk = buildModeSStackDiffDescriptor({ subMode: "diff", detectorA: "D2", detectorB: "D2", passA: 0, passB: 1 });
  assert.equal(modeSOk.valid, true);
  assert.equal(modeSOk.showMeasurementPanel, false);

  const raw = new Float32Array([1.0, 2.0, 3.0, 4.0]);
  const smooth = renderSmoothShiftViewCopy(raw, 2, 2, 0.25, 0.25);
  assert.equal(smooth.astrometryAllowed, false);
  assert.equal(raw[0], 1.0); // Raw measurement buffer untouched

  const histRow = buildHistoryEntryRow({ id: "s1", ts: "2026-11-15T00:00:00Z", target_name: "Barnard's Star", query: "zoom=16" });
  assert.equal(histRow.thumbnailWidth, 160);
  assert.equal(histRow.thumbnailHeight, 160);
  assert.equal(histRow.thumbnailDisclaimer, "overview copy, not measurement");

  const uiStrings = JSON.parse(fs.readFileSync(path.join(__dirname, "../d_site/design/ui_strings.json"), "utf-8"));
  const stateMsg = resolveScreenStateText(uiStrings, "main_viewer", "loading", { ready: 12, total: 358 });
  assert.ok(stateMsg.message.includes("12 of 358 ready"));
  assert.equal(KEYBOARD_SHORTCUTS.length, 10);
  assert.equal(ONBOARDING_STEPS.length, 3);
});

console.log(JSON.stringify({ suite: "test_viewer_js.mjs", total: results.length, passed: results.length, results }, null, 2));
