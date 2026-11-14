---
source: https://raw.githubusercontent.com/cds-astro/aladin-lite/master/src/glsl/webgl2/fits/f32.frag
fetched: 2026-11-14
status: 200
---

#version 300 es
precision highp float;
precision highp sampler2D;
precision highp int;
out vec4 out\_frag\_color;
in vec2 frag\_uv;
uniform sampler2D tex;
uniform float opacity;
#include ./color.glsl;
void main() {
// FITS y axis looks down
vec2 uv = frag\_uv;
uv.y = 1.0 - uv.y;
out\_frag\_color = uv2c\_f32(frag\_uv);
out\_frag\_color.a = out\_frag\_color.a \* opacity;
}

## Links found on page


