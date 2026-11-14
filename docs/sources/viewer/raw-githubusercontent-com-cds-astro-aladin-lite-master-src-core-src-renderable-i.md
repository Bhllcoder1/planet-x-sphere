---
source: https://raw.githubusercontent.com/cds-astro/aladin-lite/master/src/core/src/renderable/image/mod.rs
fetched: 2026-11-14
status: 200
---

pub mod cuts;
pub mod grid;
pub mod subdivide\_texture;
use al\_core::texture::format::PixelType;
use al\_core::texture::format::RGBA8U;
use al\_core::texture::format::{R16I, R32F, R32I, R8U};
use al\_core::webgl\_ctx::WebGlRenderingCtx;
use fitsrs::hdu::header::Bitpix;
use std::vec;
use al\_api::coo\_system::CooSystem;
use cgmath::Vector3;
use wasm\_bindgen::JsValue;
use web\_sys::WebGl2RenderingContext;
use fitsrs::wcs::{ImgXY, WCS};
use al\_api::fov::CenteredFoV;
use al\_api::hips::ImageMetadata;
use al\_core::webgl\_ctx::GlWrapper;
use al\_core::VecData;
use al\_core::WebGlContext;
use al\_core::{Texture2D, VertexArrayObject};
use crate::camera::CameraViewPort;
use crate::math::sph\_geom::region::Region;
use crate::Colormaps;
use crate::ProjectionType;
use crate::ShaderManager;
use std::ops::Range;
use self::subdivide\_texture::crop\_image;
use self::subdivide\_texture::ImagePatches;
pub struct Image {
/// A reference to the GL context
gl: WebGlContext,
/// The vertex array object of the screen in NDC
vao: VertexArrayObject,
num\_indices: Vec,
indices: Vec,
pos: Vec,
uv: Vec,
/// WCS allowing to locate the image on the sky
wcs: WCS,
/// Some parameters, only defined for image coming from FITS files
blank: Option,
bscale: f32,
bzero: f32,
cuts: Range,
/// The center of the fits
centered\_fov: CenteredFoV,
//+ Texture format
pixel\_type: PixelType,
/// Texture chunks objects
textures: Vec,
/// Texture indices that must be drawn
idx\_tex: Vec,
/// The size of a textured image patch
/// that can be uploaded to the GPU
w\_patch: usize,
h\_patch: usize,
reg: Region,
// The coo system in which the polygonal region has been defined
coo\_sys: CooSystem,
}
const TEX\_PARAMS: &[(u32, u32)] = &[
(
WebGlRenderingCtx::TEXTURE\_MIN\_FILTER,
WebGlRenderingCtx::NEAREST\_MIPMAP\_NEAREST,
),
(
WebGlRenderingCtx::TEXTURE\_MAG\_FILTER,
WebGlRenderingCtx::NEAREST,
),
// Prevents s-coordinate wrapping (repeating)
(
WebGlRenderingCtx::TEXTURE\_WRAP\_S,
WebGlRenderingCtx::CLAMP\_TO\_EDGE,
),
// Prevents t-coordinate wrapping (repeating)
(
WebGlRenderingCtx::TEXTURE\_WRAP\_T,
WebGlRenderingCtx::CLAMP\_TO\_EDGE,
),
];
impl Image {
#[allow(clippy::too\_many\_arguments)]
fn init\_buffers(
gl: WebGlContext,
patches: ImagePatches,
wcs: WCS,
bscale: f32,
bzero: f32,
blank: Option,
coo\_sys: CooSystem,
) -> Result {
let dim = wcs.img\_dimensions();
let (width, height) = (dim[0] as u64, dim[1] as u64);
let ImagePatches {
pixel\_type,
texture\_patches: textures,
initial\_cuts: cuts,
w\_patch,
h\_patch,
} = patches;
for tex in &textures {
tex.generate\_mipmap();
}
let start = cuts.start \* bscale + bzero;
let end = cuts.end \* bscale + bzero;
let cuts = start..end;
let num\_indices = vec![];
let indices = vec![];
let pos = vec![];
let uv = vec![];
// Define the buffers
let vao = {
let mut vao = VertexArrayObject::new(&gl);
#[cfg(feature = "webgl2")]
vao.bind\_for\_update()
// layout (location = 0) in vec2 ndc\_pos;
.add\_array\_buffer\_single(
2,
"ndc\_pos",
WebGl2RenderingContext::DYNAMIC\_DRAW,
VecData::(&pos),
)
.add\_array\_buffer\_single(
2,
"uv",
WebGl2RenderingContext::DYNAMIC\_DRAW,
VecData::(&uv),
)
// Set the element buffer
.add\_element\_buffer(
WebGl2RenderingContext::DYNAMIC\_DRAW,
VecData::(&indices),
)
.unbind();
vao
};
// Compute the fov
let center = wcs
.unproj\_lonlat(&ImgXY::new(
(width as f64 / 2.0) + 0.5,
(height as f64 / 2.0) + 0.5,
))
.ok\_or(JsValue::from\_str("(w / 2, h / 2) px cannot be unprojected"))?;
let center\_xyz = center.to\_xyz();
let inside = crate::coosys::apply\_coo\_system(
CooSystem::ICRS,
coo\_sys,
&Vector3::new(center\_xyz.y(), center\_xyz.z(), center\_xyz.x()),
);
let vertices = [
wcs.unproj\_lonlat(&ImgXY::new(0.5, 0.5))
.ok\_or(JsValue::from\_str("(0, 0) does not lie in the sky"))?,
wcs.unproj\_lonlat(&ImgXY::new(width as f64 - 0.5, 0.5))
.ok\_or(JsValue::from\_str("(w - 1, 0) does not lie in the sky"))?,
wcs.unproj\_lonlat(&ImgXY::new(width as f64 - 0.5, height as f64 - 0.5))
.ok\_or(JsValue::from\_str("(w - 1, h - 1) does not lie in the sky"))?,
wcs.unproj\_lonlat(&ImgXY::new(0.5, height as f64 - 0.5))
.ok\_or(JsValue::from\_str("(0, h - 1) does not lie in the sky"))?,
]
.iter()
.map(|lonlat| {
let xyz = lonlat.to\_xyz();
crate::coosys::apply\_coo\_system(
CooSystem::ICRS,
coo\_sys,
&Vector3::new(xyz.y(), xyz.z(), xyz.x()),
)
})
.collect::>();
let reg = Region::from\_vertices(&vertices, &inside);
// ra and dec must be given in ICRS coo system, which is the case because wcs returns
// only ICRS coo
let centered\_fov = CenteredFoV {
ra: center.lon().to\_degrees(),
dec: center.lat().to\_degrees(),
fov: wcs.field\_of\_view().0,
};
let idx\_tex = (0..textures.len()).collect();
Ok(Self {
gl,
// The positions
vao,
num\_indices,
pos,
uv,
indices,
// Metadata extracted from the fits
wcs,
// CooSystem of the wcs, this should belong to the WCS
bscale,
bzero,
blank,
// Centered field of view allowing to locate the fits
centered\_fov,
// Texture parameters
pixel\_type,
textures,
cuts,
w\_patch,
h\_patch,
// Indices of textures that must be drawn
idx\_tex,
// The polygonal region in the sky
reg,
// The coo system in which the polygonal region has been defined
coo\_sys,
})
}
#[allow(clippy::too\_many\_arguments)]
pub fn from\_fits\_hdu(
gl: &WebGlContext,
// wcs extracted from the image HDU
wcs: fitsrs::WCS,
// bitpix extracted from the image HDU
bitpix: fitsrs::hdu::header::Bitpix,
// bytes slice extracted from the HDU
bytes: &[u8],
// other keywords extracted from the header of the image HDU
bscale: f32,
bzero: f32,
blank: Option,
// Coo sys of the view
coo\_sys: CooSystem,
) -> Result {
let dim = wcs.img\_dimensions();
let (width, height) = (dim[0] as u64, dim[1] as u64);
let max\_tex\_size =
WebGl2RenderingContext::get\_parameter(gl, WebGl2RenderingContext::MAX\_TEXTURE\_SIZE)?
.as\_f64()
.unwrap\_or(4096.0) as usize;
let patches = if width <= max\_tex\_size as u64 && height <= max\_tex\_size as u64 {
// can fit in one texture
// bytes aligned
match bitpix {
Bitpix::I64 => {
// one must convert the data to i32
let bytes\_from\_i32 = bytes
.chunks(8)
.flat\_map(|bytes| {
let l = i64::from\_be\_bytes([
bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5],
bytes[6], bytes[7],
]);
let i = l as i32;
i32::to\_be\_bytes(i)
})
.collect::>();
let texture = Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes\_from\_i32.as\_slice(),
)?;
let mut sub\_pixels = bytes\_from\_i32
.chunks(std::mem::size\_of::())
.step\_by(100)
.filter\_map(|p| {
let p = i32::from\_be\_bytes([p[0], p[1], p[2], p[3]]) as f32;
if let Some(blank) = blank {
if p != blank {
Some(p)
} else {
None
}
} else {
Some(p)
}
})
.collect::>();
let cuts = cuts::first\_and\_last\_percent(&mut sub\_pixels, 1, 99);
ImagePatches::new(
PixelType::R32I,
vec![texture],
cuts,
width as usize,
height as usize,
)
}
Bitpix::F64 => {
// one must convert the data to f32
let bytes\_from\_f32 = bytes
.chunks(8)
.flat\_map(|bytes| {
let d = f64::from\_be\_bytes([
bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5],
bytes[6], bytes[7],
]);
let f = d as f32;
f32::to\_be\_bytes(f)
})
.collect::>();
let texture = Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes\_from\_f32.as\_slice(),
)?;
let mut sub\_pixels = bytes\_from\_f32
.chunks(std::mem::size\_of::())
.step\_by(100)
.filter\_map(|p| {
let p = f32::from\_be\_bytes([p[0], p[1], p[2], p[3]]);
if p.is\_finite() {
Some(p)
} else {
None
}
})
.collect::>();
let cuts = cuts::first\_and\_last\_percent(&mut sub\_pixels, 1, 99);
ImagePatches::new(
PixelType::R32F,
vec![texture],
cuts,
width as usize,
height as usize,
)
}
Bitpix::U8 => {
let texture = Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes,
)?;
let mut sub\_pixels = bytes
.iter()
.step\_by(100)
.filter\_map(|p| {
let p = \*p as f32;
if let Some(blank) = blank {
if p != blank {
Some(p)
} else {
None
}
} else {
Some(p)
}
})
.collect::>();
let cuts = cuts::first\_and\_last\_percent(&mut sub\_pixels, 1, 99);
ImagePatches::new(
PixelType::R8U,
vec![texture],
cuts,
width as usize,
height as usize,
)
}
Bitpix::I16 => {
let texture = Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes,
)?;
let mut sub\_pixels = bytes
.chunks(2)
.step\_by(100)
.filter\_map(|p| {
let p = i16::from\_be\_bytes([p[0], p[1]]) as f32;
if let Some(blank) = blank {
if p != blank {
Some(p)
} else {
None
}
} else {
Some(p)
}
})
.collect::>();
let cuts = cuts::first\_and\_last\_percent(&mut sub\_pixels, 1, 99);
ImagePatches::new(
PixelType::R16I,
vec![texture],
cuts,
width as usize,
height as usize,
)
}
Bitpix::I32 => {
let texture = Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes,
)?;
let mut sub\_pixels = bytes
.chunks(4)
.step\_by(100)
.filter\_map(|p| {
let p = i32::from\_be\_bytes([p[0], p[1], p[2], p[3]]) as f32;
if let Some(blank) = blank {
if p != blank {
Some(p)
} else {
None
}
} else {
Some(p)
}
})
.collect::>();
let cuts = cuts::first\_and\_last\_percent(&mut sub\_pixels, 1, 99);
ImagePatches::new(
PixelType::R32I,
vec![texture],
cuts,
width as usize,
height as usize,
)
}
Bitpix::F32 => {
let texture = Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes,
)?;
let mut sub\_pixels = bytes
.chunks(std::mem::size\_of::())
.step\_by(100)
.filter\_map(|p| {
let p = f32::from\_be\_bytes([p[0], p[1], p[2], p[3]]);
if p.is\_finite() {
Some(p)
} else {
None
}
})
.collect::>();
let cuts = cuts::first\_and\_last\_percent(&mut sub\_pixels, 1, 99);
ImagePatches::new(
PixelType::R32F,
vec![texture],
cuts,
width as usize,
height as usize,
)
}
}
} else {
// We cut the image in 4096x4096 patches. It is already 64MB to allocate for a f32 image of this dimensions.
match bitpix {
Bitpix::U8 => crop\_image::(gl, width, height, bytes, 4096, blank)?,
Bitpix::I16 => crop\_image::(gl, width, height, bytes, 4096, blank)?,
Bitpix::I32 => crop\_image::(gl, width, height, bytes, 4096, blank)?,
Bitpix::F32 => crop\_image::(gl, width, height, bytes, 4096, blank)?,
Bitpix::F64 => {
let bytes\_from\_f32 = bytes
.chunks(8)
.flat\_map(|bytes| {
let d = f64::from\_be\_bytes([
bytes[0], bytes[1], bytes[2], bytes[3], bytes[4], bytes[5],
bytes[6], bytes[7],
]);
let f = d as f32;
f32::to\_be\_bytes(f)
})
.collect::>();
crop\_image::(gl, width, height, &bytes\_from\_f32, 4096, blank)?
}
\_ => {
return Err(JsValue::from\_str(
"I64/F64 for big fits images not supported.",
))
}
}
};
Self::init\_buffers(gl.clone(), patches, wcs, bscale, bzero, blank, coo\_sys)
}
pub fn from\_rgba\_bytes(
gl: &WebGlContext,
// bytes in TextureFormat
bytes: &[u8],
// wcs extracted from the image HDU
wcs: fitsrs::WCS,
// Coo sys of the view
coo\_sys: CooSystem,
) -> Result {
let dim = wcs.img\_dimensions();
let (width, height) = (dim[0] as u64, dim[1] as u64);
let max\_tex\_size =
WebGl2RenderingContext::get\_parameter(gl, WebGl2RenderingContext::MAX\_TEXTURE\_SIZE)?
.as\_f64()
.unwrap\_or(4096.0) as usize;
let bscale = 1.0;
let bzero = 0.0;
let blank = None;
let image\_patches = if width <= max\_tex\_size as u64 && height <= max\_tex\_size as u64 {
// small image case, can fit into a webgl texture
let textures = vec![Texture2D::create\_from\_raw\_bytes::(
gl,
width as i32,
height as i32,
TEX\_PARAMS,
bytes,
)?];
let pixel\_ty = PixelType::RGBA8U;
let cuts = 0.0..1.0;
ImagePatches::new(pixel\_ty, textures, cuts, width as usize, height as usize)
} else {
crop\_image::(gl, width, height, bytes, 4096, None)?
};
Self::init\_buffers(
gl.clone(),
image\_patches,
wcs,
bscale,
bzero,
blank,
coo\_sys,
)
}
pub fn recompute\_vertices(
&mut self,
camera: &CameraViewPort,
projection: &ProjectionType,
) -> Result<(), JsValue> {
let dim = self.wcs.img\_dimensions();
let (width, height) = (dim[0] as f64, dim[1] as f64);
let (x\_mesh\_range, y\_mesh\_range) =
if camera.get\_field\_of\_view().intersects\_region(&self.reg) {
self.idx\_tex = (0..self.textures.len()).collect();
(0.0..width, 0.0..height)
} else {
// out of field of view
self.idx\_tex.clear();
// terminate here
return Ok(());
};
const MAX\_NUM\_TRI\_PER\_SIDE\_IMAGE: usize = 15;
let num\_vertices =
((self.centered\_fov.fov / 180.0) \* (MAX\_NUM\_TRI\_PER\_SIDE\_IMAGE as f64)).ceil() as u64;
let (pos, uv, indices, num\_indices) = grid::vertices(
&(x\_mesh\_range.start, y\_mesh\_range.start),
&(x\_mesh\_range.end.ceil(), y\_mesh\_range.end.ceil()),
self.w\_patch as u64,
self.h\_patch as u64,
num\_vertices,
camera,
&self.wcs,
projection,
self.pixel\_type == PixelType::RGB8U || self.pixel\_type == PixelType::RGBA8U,
);
self.pos = pos;
self.uv = uv;
// Update num\_indices
self.indices = indices;
self.num\_indices = num\_indices;
// vertices contains ndc positions and texture UVs
self.vao
.bind\_for\_update()
.update\_array(
"ndc\_pos",
WebGl2RenderingContext::DYNAMIC\_DRAW,
VecData(&self.pos),
)
.update\_array(
"uv",
WebGl2RenderingContext::DYNAMIC\_DRAW,
VecData(&self.uv),
)
.update\_element\_array(
WebGl2RenderingContext::DYNAMIC\_DRAW,
VecData::(&self.indices),
);
Ok(())
}
// Draw the image
pub fn draw(
&mut self,
shaders: &mut ShaderManager,
colormaps: &Colormaps,
cfg: &ImageMetadata,
camera: &CameraViewPort,
projection: &ProjectionType,
) -> Result<(), JsValue> {
if self.coo\_sys != camera.get\_coo\_system() {
self.coo\_sys = camera.get\_coo\_system();
let dim = self.wcs.img\_dimensions();
let (width, height) = (dim[0] as usize, dim[1] as usize);
// the camera coo system is not sync with the one in which the region
// has been defined
// let's redefine the region
let center = self
.wcs
.unproj\_lonlat(&ImgXY::new(
(width as f64 / 2.0) + 0.5,
(height as f64 / 2.0) + 0.5,
))
.ok\_or(JsValue::from\_str("(w / 2, h / 2) px cannot be unprojected"))?;
let center\_xyz = center.to\_xyz();
let inside = crate::coosys::apply\_coo\_system(
CooSystem::ICRS,
self.coo\_sys,
&Vector3::new(center\_xyz.y(), center\_xyz.z(), center\_xyz.x()),
);
let vertices = [
self.wcs
.unproj\_lonlat(&ImgXY::new(0.5, 0.5))
.ok\_or(JsValue::from\_str("(0, 0) does not lie in the sky"))?,
self.wcs
.unproj\_lonlat(&ImgXY::new(width as f64 - 0.5, 0.5))
.ok\_or(JsValue::from\_str("(w - 1, 0) does not lie in the sky"))?,
self.wcs
.unproj\_lonlat(&ImgXY::new(width as f64 - 0.5, height as f64 - 0.5))
.ok\_or(JsValue::from\_str("(w - 1, h - 1) does not lie in the sky"))?,
self.wcs
.unproj\_lonlat(&ImgXY::new(0.5, height as f64 - 0.5))
.ok\_or(JsValue::from\_str("(0, h - 1) does not lie in the sky"))?,
]
.iter()
.map(|lonlat| {
let xyz = lonlat.to\_xyz();
crate::coosys::apply\_coo\_system(
CooSystem::ICRS,
self.coo\_sys,
&Vector3::new(xyz.y(), xyz.z(), xyz.x()),
)
})
.collect::>();
self.reg = Region::from\_vertices(&vertices, &inside);
}
self.recompute\_vertices(camera, projection)?;
if self.num\_indices.is\_empty() {
return Ok(());
}
//self.gl.enable(WebGl2RenderingContext::BLEND);
let ImageMetadata {
opacity, blending, ..
} = cfg;
let shader = match self.pixel\_type {
PixelType::RGBA8U => crate::shader::get\_shader(
&self.gl,
shaders,
"image\_base.vert",
"image\_sampler.frag",
)?,
PixelType::RGB8U => crate::shader::get\_shader(
&self.gl,
shaders,
"image\_base.vert",
"image\_sampler.frag",
)?,
PixelType::R32F => {
crate::shader::get\_shader(&self.gl, shaders, "fits\_base.vert", "fits\_f32.frag")?
}
PixelType::R32I => {
crate::shader::get\_shader(&self.gl, shaders, "fits\_base.vert", "fits\_i32.frag")?
}
PixelType::R16I => {
crate::shader::get\_shader(&self.gl, shaders, "fits\_base.vert", "fits\_i16.frag")?
}
PixelType::R8U => {
crate::shader::get\_shader(&self.gl, shaders, "fits\_base.vert", "fits\_u8.frag")?
}
};
//self.gl.disable(WebGl2RenderingContext::CULL\_FACE);
// 2. Draw it if its opacity is not null
blending.enable(&self.gl, || {
let mut off\_indices = 0;
for &idx\_tex in self.idx\_tex.iter() {
let texture = &self.textures[idx\_tex];
let num\_indices = self.num\_indices[idx\_tex] as i32;
let shader\_bound = shader.bind(&self.gl);
shader\_bound
.attach\_uniforms\_with\_params\_from(cfg, colormaps)
.attach\_uniform("opacity", opacity)
.attach\_uniform("tex", texture)
.attach\_uniform("scale", &self.bscale)
.attach\_uniform("offset", &self.bzero);
if let Some(blank) = self.blank {
shader\_bound.attach\_uniform("blank", &blank);
}
shader\_bound
.bind\_vertex\_array\_object\_ref(&self.vao)
.draw\_elements\_with\_i32(
WebGl2RenderingContext::TRIANGLES,
Some(num\_indices),
WebGl2RenderingContext::UNSIGNED\_SHORT,
((off\_indices as usize) \* std::mem::size\_of::()) as i32,
);
off\_indices += num\_indices;
}
Ok(())
})?;
//self.gl.enable(WebGl2RenderingContext::CULL\_FACE);
//self.gl.disable(WebGl2RenderingContext::BLEND);
Ok(())
}
#[inline]
pub fn get\_centered\_fov(&self) -> &CenteredFoV {
&self.centered\_fov
}
#[inline]
pub fn get\_cuts(&self) -> &Range {
&self.cuts
}
}

## Links found on page


