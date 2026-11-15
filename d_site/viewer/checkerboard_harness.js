/**
 * Alan D - Görev 05-01 & 07-02: Dama Tahtası (Checkerboard) Test Donanımı (D1 / T-V1)
 * - 64x64 sentetik dama tahtası karesi (Frame 0 ve +1 px kaydırılmış Frame 1)
 * - Canvas2D (imageSmoothingEnabled = false) ve WebGL2 (texelFetch, filtre yok)
 * - Tam sayı yakınlaştırmada (z = 1, 3, 7, 8, 16, 32) her yerel piksel tam z x z ekran pikseli
 *   çizilir ve en çok 3 farklı gri değer (dama A, dama B, ızgara/işaret) oluşur.
 */

export const WEBGL2_TEXELFETCH_VS = `#version 300 es
in vec2 a_pos;
out vec2 v_uv;
void main() {
  v_uv = a_pos * 0.5 + 0.5;
  gl_Position = vec4(a_pos, 0.0, 1.0);
}
`;

export const WEBGL2_TEXELFETCH_FS = `#version 300 es
precision highp float;
precision highp int;
uniform sampler2D u_tex;
uniform ivec2 u_native_size;
uniform int u_zoom;
uniform ivec2 u_shift;
in vec2 v_uv;
out vec4 outColor;
void main() {
  ivec2 screen_px = ivec2(gl_FragCoord.xy);
  ivec2 native_px = (screen_px / max(u_zoom, 1)) - u_shift;
  if (native_px.x < 0 || native_px.y < 0 ||
      native_px.x >= u_native_size.x || native_px.y >= u_native_size.y) {
    outColor = vec4(0.0, 0.0, 0.0, 1.0);
    return;
  }
  vec4 texel = texelFetch(u_tex, native_px, 0);
  outColor = vec4(texel.rrr, 1.0);
}
`;

export function generateSyntheticCheckerboard(width = 64, height = 64, shiftX = 0, shiftY = 0, lowVal = 40, highVal = 220) {
  const data = new Uint8Array(width * height);
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const sx = x - shiftX;
      const sy = y - shiftY;
      const parity = ((sx & 1) ^ (sy & 1)) & 1;
      data[y * width + x] = parity === 0 ? lowVal : highVal;
    }
  }
  return { width, height, shiftX, shiftY, data };
}

export function renderCheckerboardNearestBuffer(frame, zoom) {
  const isIntZoom = Number.isInteger(zoom) && zoom >= 1;
  const outW = Math.round(frame.width * zoom);
  const outH = Math.round(frame.height * zoom);
  const out = new Uint8Array(outW * outH);

  for (let sy = 0; sy < outH; sy++) {
    const ny = isIntZoom ? Math.floor(sy / zoom) : Math.min(frame.height - 1, Math.floor(sy / zoom));
    for (let sx = 0; sx < outW; sx++) {
      const nx = isIntZoom ? Math.floor(sx / zoom) : Math.min(frame.width - 1, Math.floor(sx / zoom));
      out[sy * outW + sx] = frame.data[ny * frame.width + nx];
    }
  }
  return { width: outW, height: outH, zoom, isIntZoom, pixels: out };
}

export function verifyCheckerboardRender(renderedA, renderedB) {
  const uniqueSet = new Set();
  for (let i = 0; i < renderedA.pixels.length; i++) {
    uniqueSet.add(renderedA.pixels[i]);
  }
  // Satır 0 boyunca blok uzunluklarını (run-length) ölç
  const runs = [];
  let cur = renderedA.pixels[0];
  let len = 0;
  for (let sx = 0; sx < renderedA.width; sx++) {
    const val = renderedA.pixels[sx];
    if (val === cur) {
      len++;
    } else {
      runs.push(len);
      cur = val;
      len = 1;
    }
  }
  if (len > 0) runs.push(len);

  const minRun = Math.min(...runs);
  const maxRun = Math.max(...runs);
  const exactBlocks = renderedA.isIntZoom && minRun === renderedA.zoom && maxRun === renderedA.zoom;

  // 1 yerel piksellik kaymanın ekranda tam zoom piksel kaydığını doğrula
  let shiftVerified = true;
  if (renderedB && renderedA.isIntZoom) {
    const z = renderedA.zoom;
    for (let sx = z; sx < renderedA.width; sx++) {
      if (renderedB.pixels[sx] !== renderedA.pixels[sx - z]) {
        shiftVerified = false;
        break;
      }
    }
  }

  return {
    zoom: renderedA.zoom,
    isIntZoom: renderedA.isIntZoom,
    uniqueValueCount: uniqueSet.size,
    minBlockPx: minRun,
    maxBlockPx: maxRun,
    exactBlockWidth: exactBlocks,
    onePixelShiftEqualsZoomScreenPx: shiftVerified,
    passed: exactBlocks && uniqueSet.size <= 3 && shiftVerified,
  };
}
