/**
 * Alan D - Ana Uygulama Denetleyicisi (d_site/pages/app.js)
 * Tüm Alan D modüllerini (Mode N, Blink, Overlays, Flags, Stretch/ZODI, Metadata Strip,
 * 5 Yarışma Hedefi ve Klavye Kısayollarını) birleştirir.
 */

import { COMPETITION_TARGETS, formatTargetCardViewModel, formatFrameMetadataStrip } from "./targets_and_cards.js";
import { BlinkController } from "../viewer/blink_controller.js";
import { evaluateModeNRule, computePixelGridLines, getZoomGuaranteeLabel } from "../viewer/mode_n_renderer.js";
import { buildCentroidOverlayDescriptor, buildGaiaOverlayDescriptors } from "../viewer/overlays.js";
import { DEFAULT_DISPLAY_STATE, getBackgroundBadge, applyStretchValue, maximizeDynamicRangePreset } from "../viewer/stretch_controls.js";
import { attachKeyboardShortcuts } from "../design/accessibility_and_onboarding.js";

const DEMO_FRAMES = [
  {
    frame_id: "level2_2025W35_2A_0233_1D2",
    utc_date: "2025-08-29 17:19 UTC",
    mjd_avg: 60916.7215,
    detector: "D2",
    cwave_um: 1.85,
    cband_um: 0.02,
    pass_id: 0,
    release: "DR1",
    procver: "l2b-v27-2026-231",
    pa_deg: 181.03,
    sps_epa: 180.0,
    target_x: 15.0,
    target_y: 15.0,
  },
  {
    frame_id: "level2_2026W11_1A_0444_1D2",
    utc_date: "2026-03-11 03:47 UTC",
    mjd_avg: 61110.1576,
    detector: "D2",
    cwave_um: 1.85,
    cband_um: 0.02,
    pass_id: 1,
    release: "DR1",
    procver: "l2b-v27-2026-232",
    pa_deg: 0.887,
    sps_epa: 0.0,
    target_x: 15.0,
    target_y: 15.96, // Barnard ~0.96 px motion Pass 0 -> 1 [V: PLAN_spherex_v3.md §4]
  },
  {
    frame_id: "level2_2026W36_1A_0512_1D2",
    utc_date: "2026-09-04 11:20 UTC",
    mjd_avg: 61287.4722,
    detector: "D2",
    cwave_um: 1.85,
    cband_um: 0.02,
    pass_id: 2,
    release: "QR3",
    procver: "l2b-v27-2026-243",
    pa_deg: 181.16,
    sps_epa: 180.0,
    target_x: 15.0,
    target_y: 16.7, // Barnard ~1.70 px motion Pass 0 -> 2 [V: PLAN_spherex_v3.md §4]
  },
];

export function initApp(doc = typeof document !== "undefined" ? document : null) {
  if (!doc) return null;

  let displayState = { ...DEFAULT_DISPLAY_STATE };
  let activeTarget = COMPETITION_TARGETS[0];
  const blink = new BlinkController(DEMO_FRAMES, { intervalMs: 400 });

  const cardsEl = doc.getElementById("target-cards");
  const canvas = doc.getElementById("sky-canvas");
  const metaEl = doc.getElementById("meta-strip");
  const epochEl = doc.getElementById("epoch-bar");
  const counterEl = doc.getElementById("frame-counter");
  const motionEl = doc.getElementById("motion-summary");
  const badgeMode = doc.getElementById("badge-mode");
  const badgeTheta = doc.getElementById("badge-theta");
  const badgeBg = doc.getElementById("badge-bg");
  const guaranteeEl = doc.getElementById("pixel-guarantee");

  function renderTargetCards() {
    if (!cardsEl) return;
    cardsEl.innerHTML = "";
    for (const t of COMPETITION_TARGETS) {
      const vm = formatTargetCardViewModel(t);
      const div = doc.createElement("div");
      div.className = `target-card${t.id === activeTarget.id ? " active" : ""}`;
      div.innerHTML = `
        <strong>${vm.name}</strong> <span class="badge">${vm.statusBadge}</span>
        <div style="font-size:12px;color:var(--text-muted);margin-top:4px;">${vm.coordinatesExact}</div>
        <div style="font-size:12px;margin-top:4px;">Frames: <b>${vm.framesLabel}</b> | Passes: <b>${vm.passesLabel}</b></div>
        <div style="font-size:12px;color:var(--text-secondary);margin-top:4px;">${vm.motionSummary}</div>
      `;
      div.addEventListener("click", () => {
        activeTarget = t;
        renderTargetCards();
        renderFrame();
      });
      cardsEl.appendChild(div);
    }
  }

  function renderFrame() {
    const frame = blink.getCurrentFrame();
    if (!frame) return;

    const modeCheck = evaluateModeNRule({
      sameDetector: true,
      paRefDeg: DEMO_FRAMES[0].pa_deg,
      paFrameDeg: frame.pa_deg,
      spsEpaRef: DEMO_FRAMES[0].sps_epa,
      spsEpaFrame: frame.sps_epa,
      subpixelOffsetPx: 0.03,
    });

    if (badgeMode) badgeMode.textContent = `Mode ${modeCheck.mode}`;
    if (badgeTheta) badgeTheta.textContent = modeCheck.badgeText;
    if (badgeBg) badgeBg.textContent = getBackgroundBadge(displayState.bg) || "Raw (no ZODI subtracted)";
    if (guaranteeEl) guaranteeEl.textContent = getZoomGuaranteeLabel(displayState.zoom);
    if (counterEl) counterEl.textContent = `Frame ${blink.getCounterLabel()}`;

    const strip = formatFrameMetadataStrip(frame);
    if (metaEl) {
      metaEl.textContent = `${strip.utcDate} | MJD-AVG ${strip.mjdAvg} | ${strip.detector} | λ ${strip.wavelength} | ${strip.passId} | ${strip.release} (${strip.procTag})`;
    }

    if (epochEl) {
      epochEl.innerHTML = blink
        .getEpochBarItems()
        .map(
          (it) =>
            `<span class="epoch-cell${it.isLoopStartBorder ? " loop-start" : ""}${it.isCurrent ? " active" : ""}">${it.symbol} P${it.pass_id}</span>`
        )
        .join("");
    }

    if (motionEl) {
      const vm = formatTargetCardViewModel(activeTarget);
      motionEl.innerHTML = `
        <div><strong>${vm.name}</strong> (${vm.honestyTag})</div>
        <div>Outcome: ${vm.detectionOutcome}</div>
        <div>Cross-Pass Motion: ${vm.motionSummary}</div>
        <div style="color:var(--text-muted);font-size:12px;margin-top:4px;">Caveats: ${vm.caveats}</div>
      `;
    }

    if (canvas && canvas.getContext) {
      const ctx = canvas.getContext("2d");
      if (ctx) {
        const z = displayState.zoom;
        const winSize = 31;
        canvas.width = winSize * z;
        canvas.height = winSize * z;
        ctx.imageSmoothingEnabled = false;

        for (let y = 0; y < winSize; y++) {
          for (let x = 0; x < winSize; x++) {
            const dx = x - frame.target_x;
            const dy = y - frame.target_y;
            const r2 = dx * dx + dy * dy;
            // Barnard 2x2 NaN saturated core
            if (activeTarget.id === "barnard" && Math.abs(dx) < 0.8 && Math.abs(dy) < 0.8) {
              ctx.fillStyle = "rgb(0, 114, 178)";
            } else {
              const flux = Math.exp(-r2 / 2.2) * 0.9 + 0.05;
              const stretched = applyStretchValue(flux, displayState.stretch, displayState.a, displayState.invert);
              const g = Math.round(stretched * 255);
              ctx.fillStyle = `rgb(${g}, ${g}, ${g})`;
            }
            ctx.fillRect(x * z, y * z, z, z);
          }
        }

        if (displayState.grid) {
          const lines = computePixelGridLines(winSize, winSize, z);
          ctx.strokeStyle = "rgba(255,255,255,0.12)";
          ctx.lineWidth = 1;
          for (const vx of lines.vertical) {
            ctx.beginPath();
            ctx.moveTo(vx, 0);
            ctx.lineTo(vx, canvas.height);
            ctx.stroke();
          }
          for (const hy of lines.horizontal) {
            ctx.beginPath();
            ctx.moveTo(0, hy);
            ctx.lineTo(canvas.width, hy);
            ctx.stroke();
          }
        }

        if (displayState.cen) {
          const cen = buildCentroidOverlayDescriptor(
            { x_px: frame.target_x + 0.5, y_px: frame.target_y + 0.5, sigma_x_px: 0.08, sigma_y_px: 0.08, saturated_core: true },
            z
          );
          ctx.strokeStyle = cen.color;
          ctx.lineWidth = 2;
          ctx.beginPath();
          ctx.moveTo(cen.screenX - 6, cen.screenY);
          ctx.lineTo(cen.screenX + 6, cen.screenY);
          ctx.moveTo(cen.screenX, cen.screenY - 6);
          ctx.lineTo(cen.screenX, cen.screenY + 6);
          ctx.stroke();
        }

        if (displayState.gaia) {
          const [gaia] = buildGaiaOverlayDescriptors(
            [{ source_id: "GaiaDR3_Barnard", x_px: frame.target_x + 0.5, y_px: frame.target_y + 0.5 }],
            z
          );
          ctx.strokeStyle = gaia.color;
          ctx.lineWidth = 1.5;
          ctx.beginPath();
          ctx.arc(gaia.screenX, gaia.screenY, z * 0.45, 0, Math.PI * 2);
          ctx.stroke();
        }
      }
    }
  }

  attachKeyboardShortcuts(
    {
      togglePlay: () => {
        blink.stepForward();
        renderFrame();
      },
      stepBackward: () => {
        blink.stepBackward();
        renderFrame();
      },
      stepForward: () => {
        blink.stepForward();
        renderFrame();
      },
      toggleGrid: () => {
        displayState.grid = !displayState.grid;
        renderFrame();
      },
      toggleInvert: () => {
        displayState.invert = !displayState.invert;
        renderFrame();
      },
      restartBlink: () => {
        blink.restart();
        renderFrame();
      },
      slowerBlink: () => blink.setSpeed(blink.intervalMs + 100),
      fasterBlink: () => blink.setSpeed(blink.intervalMs - 100),
    },
    doc
  );

  doc.getElementById("btn-next")?.addEventListener("click", () => {
    blink.stepForward();
    renderFrame();
  });
  doc.getElementById("btn-prev")?.addEventListener("click", () => {
    blink.stepBackward();
    renderFrame();
  });
  doc.getElementById("btn-restart")?.addEventListener("click", () => {
    blink.restart();
    renderFrame();
  });
  doc.getElementById("btn-max-dyn")?.addEventListener("click", () => {
    displayState = maximizeDynamicRangePreset(displayState);
    renderFrame();
  });

  renderTargetCards();
  renderFrame();
  return { blink, displayState, renderFrame };
}

if (typeof document !== "undefined") {
  initApp(document);
}
