---
source: https://raw.githubusercontent.com/Caltech-IPAC/firefly/dev/src/firefly/js/visualize/rawData/wgsl/imageSingleBand.wgsl
fetched: 2026-11-14
status: 200
---

// -------------
// WebGPU Shading Language - processing single band, false color images
// optimzation: mostly done
// -------------
struct Pixels { p: array, }
struct Params {
contrast : f32,
offsetShift : f32,
}
@group(0) @binding(0) var colorModelPacked : array; // color lookup table
@group(0) @binding(1) var pixelAry : Pixels; // each 32 bit entry contains 4 8 bit pixels
@group(0) @binding(2) var outBuf : array; //each output 32 big contains a r,g,b,a
@group(0) @binding(3) var params : Params;
const SCALE\_MIN= vec4(0);
const SCALE\_MAX=vec4(254);
const NAN\_PIX=vec4(255u);
const NAN\_PIX\_IDX=vec4(255u);
@compute @workgroup\_size(256)
fn main(@builtin(global\_invocation\_id) gid: vec3) {
let idx = gid.x;
let numPixels = arrayLength(&pixelAry.p) \* 4u;
let outBaseIdx= idx\*4;
if (outBaseIdx >= numPixels) { return; }
let outBufLength= arrayLength(&outBuf);
let v= pixelAry.p[idx];
// now we are using vector opperations, so I am working with 4 values at a time
let pixels = vec4( (v>> 0u) & 255u, (v>> 8u) & 255u, (v>> 16u) & 255u, (v>> 24u) & 255u); // extract out 4 pixels into a vector
let scaled = vec4(pixels) \* params.contrast + params.offsetShift; // vector and scalar math produces a vector
let processedIdx= vec4(clamp(vec4(scaled), SCALE\_MIN, SCALE\_MAX)); // make sure all indices fall between 0 and 254
let colorIdx = select(processedIdx, NAN\_PIX\_IDX, pixels == NAN\_PIX); // // vector compare -> produces a vec4 -> then a vec of indexes
let color= vec4(
colorModelPacked[colorIdx.x], colorModelPacked[colorIdx.y],
colorModelPacked[colorIdx.z], colorModelPacked[colorIdx.w]
);
let outPixelCnt = min(4u, outBufLength- outBaseIdx);
if (outPixelCnt == 4u) {
outBuf[outBaseIdx + 0u] = color.x;
outBuf[outBaseIdx + 1u] = color.y;
outBuf[outBaseIdx + 2u] = color.z;
outBuf[outBaseIdx + 3u] = color.w;
}
else {
if (outPixelCnt >= 1u) {outBuf[outBaseIdx + 0u] = color.x;}
if (outPixelCnt >= 2u) {outBuf[outBaseIdx + 1u] = color.y;}
if (outPixelCnt >= 3u) {outBuf[outBaseIdx + 2u] = color.z;}
}
}

## Links found on page


