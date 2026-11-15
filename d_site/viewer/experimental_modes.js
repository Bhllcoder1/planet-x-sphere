/**
 * Alan D - Görev 05-12 & 05-13: Deneysel / Sonra Görüntüleme Modları
 * - 05-12: GPU afin Mod R (WebGL2 kare başı afin + en yakın komşu; r_max > 0.01 px ise R-k'ye düşer)
 * - 05-13: Yumuşak kayma (Smooth-shift) görünümü: yalnızca görüntüleme (view-only),
 *   kırmızı uyarı etiketli; ölçüm ve imleç okuması her zaman gerçek ham pikseli verir.
 */

export const SMOOTH_SHIFT_WARNING_LABEL =
  "SMOOTH-SHIFT: interpolated view only — NEVER used for measurement or astrometry";

export function evaluateAffineModeREligibility(affineResidualMaxPx, thresholdPx = 0.01) {
  const rMax = Number(affineResidualMaxPx);
  if (!Number.isFinite(rMax) || rMax > thresholdPx) {
    return {
      mode: "R-k",
      useGpuAffine: false,
      rMaxPx: rMax,
      reason: `Affine residual r_max = ${rMax.toFixed(4)} px > ${thresholdPx} px limit; falling back to server R-k.`,
    };
  }
  return {
    mode: "R",
    useGpuAffine: true,
    rMaxPx: rMax,
    reason: `GPU affine Mode R active (r_max = ${rMax.toFixed(4)} px <= ${thresholdPx} px, NEAREST sampling).`,
  };
}

/**
 * Görev 05-13: Kesirli konum kaymasını komşu piksellere parlaklık yayarak gösteren
 * salt-görüntüleme (view-only) kopyası. Ham ölçüm dizisini ASLA değiştirmez.
 */
export function renderSmoothShiftViewCopy(rawImageFloat32, width, height, fracShiftX = 0.0, fracShiftY = 0.0) {
  const out = new Float32Array(width * height);
  const dx = Number(fracShiftX);
  const dy = Number(fracShiftY);

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const srcX = x - dx;
      const srcY = y - dy;
      const x0 = Math.floor(srcX);
      const y0 = Math.floor(srcY);
      const x1 = Math.min(width - 1, Math.max(0, x0 + 1));
      const y1 = Math.min(height - 1, Math.max(0, y0 + 1));
      const cx0 = Math.min(width - 1, Math.max(0, x0));
      const cy0 = Math.min(height - 1, Math.max(0, y0));
      const wx = srcX - x0;
      const wy = srcY - y0;

      const v00 = rawImageFloat32[cy0 * width + cx0];
      const v10 = rawImageFloat32[cy0 * width + x1];
      const v01 = rawImageFloat32[y1 * width + cx0];
      const v11 = rawImageFloat32[y1 * width + x1];

      if (!Number.isFinite(v00) || !Number.isFinite(v10) || !Number.isFinite(v01) || !Number.isFinite(v11)) {
        out[y * width + x] = NaN;
      } else {
        out[y * width + x] =
          (1 - wx) * (1 - wy) * v00 +
          wx * (1 - wy) * v10 +
          (1 - wx) * wy * v01 +
          wx * wy * v11;
      }
    }
  }

  return {
    viewOnlyBuffer: out,
    measurementBufferRef: rawImageFloat32, // Ölçüm ve okuma her zaman bu ham diziyi kullanır
    warningBadge: SMOOTH_SHIFT_WARNING_LABEL,
    astrometryAllowed: false,
  };
}
