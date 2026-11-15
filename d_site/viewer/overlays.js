/**
 * Alan D - Görev 05-06, 05-07, 10-10: Float Konum İşaretçileri, 1σ/2σ Hata Elipsleri,
 * Hareket Vektörü (gerçek + x10) ve Gaia DR3 Katmanı (MJD-AVG Epoğuna Taşınmış)
 *
 * Kural [V: DECISIONS_AND_TASK.md, 05-06, 07-03]:
 * - Float konumlar ASLA tam sayıya yuvarlanmaz:
 *   x = 4.47, zoom = 100 -> screenX = 447.0 (±0.5 px içinde, 500 değil!)
 */

import { nativeToScreenCoord } from "./mode_n_renderer.js";

export function computeErrorEllipseParams(sigmaX, sigmaY, covXY = 0.0) {
  const varX = Number(sigmaX) ** 2;
  const varY = Number(sigmaY) ** 2;
  const cxy = Number(covXY);
  const trace = varX + varY;
  const det = varX * varY - cxy * cxy;
  const disc = Math.sqrt(Math.max(0.0, (trace * trace) / 4.0 - det));
  const lambda1 = Math.max(1e-12, trace / 2.0 + disc);
  const lambda2 = Math.max(1e-12, trace / 2.0 - disc);
  const a1SigmaPx = Math.sqrt(lambda1);
  const b1SigmaPx = Math.sqrt(lambda2);
  const angleRad = 0.5 * Math.atan2(2.0 * cxy, varX - varY);
  const angleDeg = (angleRad * 180.0) / Math.PI;

  return {
    a1SigmaPx,
    b1SigmaPx,
    a2SigmaPx: 2.0 * a1SigmaPx,
    b2SigmaPx: 2.0 * b1SigmaPx,
    angleRad,
    angleDeg,
  };
}

export function buildCentroidOverlayDescriptor(source, zoom, originX = 0, originY = 0) {
  const screenX = nativeToScreenCoord(source.x_px, zoom, originX, false);
  const screenY = nativeToScreenCoord(source.y_px, zoom, originY, false);
  const ell = computeErrorEllipseParams(source.sigma_x_px ?? 0.05, source.sigma_y_px ?? 0.05, source.cov_xy_px2 ?? 0.0);

  return {
    id: source.id || "target",
    nativeX: Number(source.x_px),
    nativeY: Number(source.y_px),
    screenX,
    screenY,
    color: "#009e73", // Okabe-Ito Bluish Green (W23)
    shape: "cross-and-ellipse",
    saturatedFitBadge: Boolean(source.saturated_core || source.fit_mode === "saturated-fit"),
    forcedFit: Boolean(source.forced_fit ?? true),
    ellipse1Sigma: {
      rxScreenPx: ell.a1SigmaPx * zoom,
      ryScreenPx: ell.b1SigmaPx * zoom,
      angleDeg: ell.angleDeg,
      strokeStyle: "solid",
    },
    ellipse2Sigma: {
      rxScreenPx: ell.a2SigmaPx * zoom,
      ryScreenPx: ell.b2SigmaPx * zoom,
      angleDeg: ell.angleDeg,
      strokeStyle: "dashed",
    },
  };
}

export function buildMotionVectorDescriptor(startNative, endNative, zoom, originX = 0, originY = 0, includeScaled10x = true) {
  const x0 = nativeToScreenCoord(startNative.x_px, zoom, originX, false);
  const y0 = nativeToScreenCoord(startNative.y_px, zoom, originY, false);
  const x1 = nativeToScreenCoord(endNative.x_px, zoom, originX, false);
  const y1 = nativeToScreenCoord(endNative.y_px, zoom, originY, false);
  const dxScreen = x1 - x0;
  const dyScreen = y1 - y0;

  return {
    trueVector: {
      x0,
      y0,
      x1,
      y1,
      dxNativePx: Number(endNative.x_px) - Number(startNative.x_px),
      dyNativePx: Number(endNative.y_px) - Number(startNative.y_px),
      color: "#009e73",
      label: "true motion",
    },
    scaled10xVector: includeScaled10x
      ? {
          x0,
          y0,
          x1: x0 + 10.0 * dxScreen,
          y1: y0 + 10.0 * dyScreen,
          color: "#e69f00", // Okabe-Ito Orange
          label: "×10 (display scale)",
        }
      : null,
  };
}

export function buildGaiaOverlayDescriptors(gaiaCatalogAtEpoch, zoom, originX = 0, originY = 0) {
  return (gaiaCatalogAtEpoch || []).map((g) => {
    const sx = nativeToScreenCoord(g.x_px, zoom, originX, false);
    const sy = nativeToScreenCoord(g.y_px, zoom, originY, false);
    const trail = Array.isArray(g.trail_epochs)
      ? g.trail_epochs.map((pt) => ({
          epochLabel: pt.epoch_label,
          screenX: nativeToScreenCoord(pt.x_px, zoom, originX, false),
          screenY: nativeToScreenCoord(pt.y_px, zoom, originY, false),
        }))
      : [];
    return {
      sourceId: g.source_id,
      mjdAvg: g.mjd_avg,
      nativeX: Number(g.x_px),
      nativeY: Number(g.y_px),
      screenX: sx,
      screenY: sy,
      gMag: g.phot_g_mean_mag,
      shape: "open-circle",
      color: "#56b4e9", // Okabe-Ito Sky Blue (W10, W23)
      trailColor: "#cc79a7", // Okabe-Ito Red-Purple
      trailPoints: trail,
    };
  });
}
