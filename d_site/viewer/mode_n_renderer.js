/**
 * Alan D - Görev 05-02, 05-05, 10-07: Görüntüleyici Mod N, θ_res Rozeti ve Piksel Izgarası
 * Kurallar [V: PLAN_spherex_v3.md §2.2, SITE_SPEC W6 & W7]:
 * 1. Mod N: Her kare kendi doğal ızgarasında, tam sayı zoom (z = 8..32), NEAREST örnekleme.
 * 2. Kayıt (registration): yalnızca tam sayı kayma (+ SPS_EPA farklı ve dedektör aynıysa tam 180° dönüş).
 * 3. Otomatik varsayılan: yalnızca aynı dedektör VE r_edge * θ_res <= 0.25 px olduğunda Mod N seçilir;
 *    aksi halde tek satırlık gerekçeyle R-k moduna geçilir.
 * 4. Sabit kesin-piksel metni:
 *    "Each native pixel is drawn exactly z × z screen pixels; a 1-pixel shift is exactly z screen pixels; positions are never rounded."
 */

export const EXACT_PIXEL_GUARANTEE_TEXT =
  "Each native pixel is drawn exactly z × z screen pixels; a 1-pixel shift is exactly z screen pixels; positions are never rounded.";

export const OVERVIEW_NOT_EXACT_TEXT = "overview, not exact";

export function nativeToScreenCoord(nativeCoord, zoom, origin = 0, halfPixelCenter = false) {
  const offset = halfPixelCenter ? 0.5 : 0.0;
  return (Number(nativeCoord) - Number(origin) + offset) * Number(zoom);
}

export function screenToNativeCoord(screenCoord, zoom, origin = 0, halfPixelCenter = false) {
  const offset = halfPixelCenter ? 0.5 : 0.0;
  return Number(screenCoord) / Number(zoom) + Number(origin) - offset;
}

export function evaluateModeNRule({
  sameDetector = true,
  paRefDeg = 181.0,
  paFrameDeg = 181.0,
  spsEpaRef = 180.0,
  spsEpaFrame = 180.0,
  subpixelOffsetPx = 0.0,
  windowWidth = 31,
  windowHeight = 31,
  maxEdgePx = 0.25,
}) {
  if (!sameDetector) {
    return {
      mode: "R-k",
      allowModeN: false,
      flip180: false,
      thetaResDeg: null,
      edgeDispPx: null,
      badgeText: "R-k | cross-detector resampled (k=4 NN)",
      reasonText: "Left Mode N: detector differs from reference frame.",
    };
  }

  const flip180 = Math.abs(Number(spsEpaFrame) - Number(spsEpaRef)) > 90.0;
  const expectedFlip = flip180 ? 180.0 : 0.0;
  let diff = (Number(paFrameDeg) - Number(paRefDeg) - expectedFlip) % 360.0;
  if (diff < 0) diff += 360.0;
  if (diff > 180.0) diff -= 360.0;

  const thetaResDeg = Math.abs(diff);
  const thetaResRad = (thetaResDeg * Math.PI) / 180.0;
  const rEdge = Math.hypot((windowWidth - 1) / 2.0, (windowHeight - 1) / 2.0);
  const edgeDispPx = rEdge * thetaResRad;
  const allowModeN = edgeDispPx <= maxEdgePx;
  const mode = allowModeN ? "N" : "R-k";

  const badgeText = `leftover rotation ${thetaResDeg.toFixed(2)} deg, offset ${Number(subpixelOffsetPx).toFixed(2)} px, <= ${edgeDispPx.toFixed(2)} px at window edge`;
  const reasonText = allowModeN
    ? `Mode N active: same detector and edge rotation displacement ${edgeDispPx.toFixed(2)} px <= ${maxEdgePx} px.`
    : `Switched to Mode R-k: leftover rotation ${thetaResDeg.toFixed(2)} deg produces ${edgeDispPx.toFixed(2)} px at window edge (> ${maxEdgePx} px limit).`;

  return {
    mode,
    allowModeN,
    flip180,
    thetaResDeg,
    edgeDispPx,
    badgeText,
    reasonText,
  };
}

export function getZoomGuaranteeLabel(zoom) {
  if (Number(zoom) < 1) {
    return OVERVIEW_NOT_EXACT_TEXT;
  }
  return EXACT_PIXEL_GUARANTEE_TEXT;
}

export function computePixelGridLines(widthPx, heightPx, zoom) {
  if (!Number.isInteger(zoom) || zoom < 4) {
    return { vertical: [], horizontal: [] };
  }
  const vertical = [];
  const horizontal = [];
  for (let x = 0; x <= widthPx; x++) {
    vertical.push(x * zoom);
  }
  for (let y = 0; y <= heightPx; y++) {
    horizontal.push(y * zoom);
  }
  return { vertical, horizontal };
}
