/**
 * Alan D - Görev 05-09, 05-16, 05-19: İmleç Okuması (Cursor Readout),
 * Tıkla-Ortala / Sürükle-Görüş-Alanı ve Dış Katalog Bağlantıları (SIMBAD, VizieR, Legacy Survey, Pan-STARRS)
 */

import { decodeFlagWord } from "./flag_layer.js";
import { screenToNativeCoord } from "./mode_n_renderer.js";

export function readPixelUnderCursor({
  screenX,
  screenY,
  zoom,
  originX = 0,
  originY = 0,
  width,
  height,
  rawImageFloat32,
  varianceFloat32,
  flagsUint32,
  wcsTransform,
  cwaveUm = null,
  cbandUm = null,
}) {
  const nativeFloatX = screenToNativeCoord(screenX, zoom, originX, false);
  const nativeFloatY = screenToNativeCoord(screenY, zoom, originY, false);
  const ix = Math.floor(nativeFloatX);
  const iy = Math.floor(nativeFloatY);

  if (ix < 0 || iy < 0 || ix >= width || iy >= height) {
    return null;
  }

  const idx = iy * width + ix;
  const rawVal = rawImageFloat32[idx];
  const varVal = varianceFloat32 ? varianceFloat32[idx] : NaN;
  const flagWord = flagsUint32 ? flagsUint32[idx] : 0;
  const isNan = !Number.isFinite(rawVal);
  const sigmaVal = Number.isFinite(varVal) && varVal > 0 ? Math.sqrt(varVal) : null;

  const sky = typeof wcsTransform === "function"
    ? wcsTransform(nativeFloatX, nativeFloatY)
    : { raDeg: null, decDeg: null };

  return {
    nativeFloatX,
    nativeFloatY,
    pixelIndexX: ix,
    pixelIndexY: iy,
    raDeg: sky.raDeg,
    decDeg: sky.decDeg,
    valueMjySr: isNan ? null : Number(rawVal),
    valueLabel: isNan ? "no data (NaN)" : `${Number(rawVal).toFixed(4)} MJy/sr`,
    sigmaMjySr: sigmaVal,
    wavelengthLabel:
      cwaveUm !== null && cbandUm !== null
        ? `${Number(cwaveUm).toFixed(3)} ± ${Number(cbandUm).toFixed(3)} μm`
        : "not measured",
    flagWord: flagWord >>> 0,
    activeFlags: decodeFlagWord(flagWord),
  };
}

/**
 * Görev 05-16: Tıklanan float piksel konumundan yeni merkez (RA/Dec) ve sürüklenen dikdörtgenden
 * yeni görüş alanı (FOV arcsec) hesaplama.
 */
export function computeClickRecenterAndFov({
  clickScreenX,
  clickScreenY,
  dragEndScreenX = null,
  dragEndScreenY = null,
  zoom,
  originX = 0,
  originY = 0,
  wcsTransform,
  pixelScaleArcsec = 6.15,
}) {
  const nx = screenToNativeCoord(clickScreenX, zoom, originX, false);
  const ny = screenToNativeCoord(clickScreenY, zoom, originY, false);
  const centerSky = wcsTransform(nx, ny);

  let fovArcsec = null;
  if (dragEndScreenX !== null && dragEndScreenY !== null) {
    const nx2 = screenToNativeCoord(dragEndScreenX, zoom, originX, false);
    const ny2 = screenToNativeCoord(dragEndScreenY, zoom, originY, false);
    const spanPx = Math.max(Math.abs(nx2 - nx), Math.abs(ny2 - ny));
    fovArcsec = Math.max(60, Math.round(spanPx * pixelScaleArcsec));
  }

  return {
    nativeX: nx,
    nativeY: ny,
    raDeg: centerSky.raDeg,
    decDeg: centerSky.decDeg,
    fovArcsec,
  };
}

/**
 * Görev 05-19 & SITE_SPEC W21: Koordinat dolgulu dış katalog bağlantıları
 * (SIMBAD, VizieR, Legacy Survey, Pan-STARRS, IRSA).
 */
export function buildExternalContextLinks(raDeg, decDeg, radiusArcsec = 120) {
  const ra = Number(raDeg).toFixed(6);
  const dec = Number(decDeg).toFixed(6);
  const signDec = Number(decDeg) >= 0 ? `%2B${dec}` : dec;

  return {
    simbad: `https://simbad.cds.unistra.fr/simbad/sim-coo?Coord=${ra}+${signDec}&CooFrame=ICRS&CooEpoch=2000&CooEqui=2000&Radius=${radiusArcsec}&Radius.unit=arcsec`,
    vizier: `https://vizier.cds.unistra.fr/viz-bin/VizieR-4?-c=${ra}${Number(decDeg) >= 0 ? "+" : ""}${dec}&-c.rs=${radiusArcsec}`,
    legacySurvey: `https://www.legacysurvey.org/viewer?ra=${ra}&dec=${dec}&layer=ls-dr10&zoom=14`,
    panStarrs: `https://ps1images.stsci.edu/cgi-bin/ps1cutouts?pos=${ra}+${signDec}&filter=color&filter=g&filter=r&filter=i&filetypes=stack&size=240`,
    irsaSpherex: `https://irsa.ipac.caltech.edu/applications/spherex/?ra=${ra}&dec=${dec}`,
  };
}
