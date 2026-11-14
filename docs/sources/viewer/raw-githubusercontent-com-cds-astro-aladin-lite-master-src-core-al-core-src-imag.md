---
source: https://raw.githubusercontent.com/cds-astro/aladin-lite/master/src/core/al-core/src/image/fits.rs
fetched: 2026-11-14
status: 200
---

use crate::texture::format::TextureFormat;
use crate::texture::format::R8U;
use cgmath::Vector3;
use fitsrs::hdu::data::bintable::data::BinaryTableData;
use fitsrs::hdu::data::bintable::tile\_compressed::pixels::Pixels;
use fitsrs::hdu::header::extension::bintable::TileCompressedImage;
use fitsrs::hdu::header::Bitpix;
use fitsrs::WCS;
use fitsrs::{Fits, HDU};
use std::borrow::Cow;
use std::fmt::Debug;
use std::io::Cursor;
use std::ops::Range;
use wasm\_bindgen::JsValue;
use fitsrs::hdu::header::ValueMap;
#[derive(Debug)]
pub struct FitsImage<'a> {
// Margin values for HiPS3D cubic tiles
pub trim1: u32,
pub trim2: u32,
pub trim3: u32,
// Image/cube size
pub width: u32,
pub height: u32,
pub depth: u32,
// Bitpix
pub bitpix: Bitpix,
// 1.0 by default
pub bscale: f32,
// 0.0 by default
pub bzero: f32,
// blank
pub blank: Option,
// optional wcs
pub wcs: Option,
// bytes offset where the data bytes are located inside the fits
pub data\_byte\_offset: Range,
// raw bytes of the data image (in Big-Endian)
pub raw\_bytes: Cow<'a, [u8]>,
// keep the header keywords and their values
pub header: ValueMap,
}
impl<'a> FitsImage<'a> {
/// Get all the hdu images from a fits file
pub fn from\_raw\_bytes(bytes: &'a [u8]) -> Result, JsValue> {
let mut fits = Fits::from\_reader(Cursor::new(bytes));
let mut images = vec![];
while let Some(Ok(hdu)) = fits.next() {
match hdu {
HDU::XImage(hdu) | HDU::Primary(hdu) => {
// Prefer getting the dimension directly from NAXIS1/NAXIS2 instead of from the WCS
// because it may not exist in all HDU images
let naxis = hdu.get\_header().get\_xtension().get\_naxis();
if naxis.len() >= 2 {
let width = naxis[0];
let height = naxis[1];
let depth = if naxis.len() >= 3 { naxis[2] } else { 1 };
let header = hdu.get\_header();
let bscale = header.get\_parsed::("BSCALE").unwrap\_or(1.0);
let bzero = header.get\_parsed::("BZERO").unwrap\_or(0.0);
let blank = header.get\_parsed::("BLANK").ok();
let trim1 = header.get\_parsed::("TRIM1").unwrap\_or(0);
let trim2 = header.get\_parsed::("TRIM2").unwrap\_or(0);
let trim3 = header.get\_parsed::("TRIM3").unwrap\_or(0);
let bitpix = hdu.get\_header().get\_xtension().get\_bitpix();
let off = hdu.get\_data\_unit\_byte\_offset() as usize;
let len = hdu.get\_data\_unit\_byte\_size() as usize;
let data\_byte\_offset = off..(off + len);
let raw\_bytes = Cow::Borrowed(&bytes[data\_byte\_offset.clone()]);
let wcs = hdu.wcs().ok();
let values: &ValueMap = header;
images.push(Self {
trim1,
trim2,
trim3,
width: width as u32,
height: height as u32,
depth: depth as u32,
bitpix,
bscale,
wcs,
bzero,
blank,
data\_byte\_offset,
raw\_bytes,
header: values.clone(),
});
}
}
HDU::XBinaryTable(hdu) => {
let header = hdu.get\_header();
let bin\_table = header.get\_xtension();
if let Some(TileCompressedImage {
z\_bitpix: bitpix,
z\_naxisn: naxis,
..
}) = &bin\_table.get\_z\_image()
{
if naxis.len() >= 2 {
let width = naxis[0] as u32;
let height = naxis[1] as u32;
let depth = if naxis.len() >= 3 { naxis[2] as u32 } else { 1 };
let bscale = header.get\_parsed::("BSCALE").unwrap\_or(1.0);
let bzero = header.get\_parsed::("BZERO").unwrap\_or(0.0);
let blank = header.get\_parsed::("BLANK").ok();
let trim1 = header.get\_parsed::("TRIM1").unwrap\_or(0);
let trim2 = header.get\_parsed::("TRIM2").unwrap\_or(0);
let trim3 = header.get\_parsed::("TRIM3").unwrap\_or(0);
let wcs = hdu.wcs().ok();
let off = hdu.get\_data\_unit\_byte\_offset() as usize;
let len = hdu.get\_data\_unit\_byte\_size() as usize;
let data\_byte\_offset = off..(off + len);
let mut bitpix = \*bitpix;
let raw\_bytes = match fits.get\_data(&hdu) {
BinaryTableData::TileCompressed(Pixels::U8(pixels)) => {
Some(pixels.collect::>())
}
BinaryTableData::TileCompressed(Pixels::I16(pixels)) => {
Some(pixels.flat\_map(|p| p.to\_be\_bytes()).collect::>())
}
BinaryTableData::TileCompressed(Pixels::I32(pixels)) => {
Some(pixels.flat\_map(|p| p.to\_be\_bytes()).collect::>())
}
BinaryTableData::TileCompressed(Pixels::F32(pixels)) => {
Some(pixels.flat\_map(|p| p.to\_be\_bytes()).collect::>())
}
BinaryTableData::TileCompressed(Pixels::F64(pixels)) => {
bitpix = Bitpix::F32;
let raw\_bytes =
pixels.flat\_map(|p| p.to\_be\_bytes()).collect::>();
Some(raw\_bytes)
}
\_ => None,
};
if let Some(raw\_bytes) = raw\_bytes {
let values: &ValueMap = header;
images.push(Self {
trim1,
trim2,
trim3,
width,
height,
depth,
bitpix,
bscale,
wcs,
bzero,
blank,
data\_byte\_offset,
raw\_bytes: Cow::Owned(raw\_bytes),
header: values.clone(),
});
}
}
}
}
\_ => (),
}
}
if !images.is\_empty() {
Ok(images)
} else {
Err(JsValue::from\_str("Image HDU not found in the FITS"))
}
}
}
use crate::{image::Image, texture::Tex3D};
use std::convert::TryInto;
impl Image for FitsImage<'\_> {
fn insert\_into\_3d\_texture(
&self,
// The texture array
textures: &T,
// An offset to write the image in the texture array
offset: &Vector3,
) -> Result<(), JsValue> {
let view = unsafe {
match self.bitpix {
Bitpix::I64 => {
// convert to i64 first
let new\_bytes: Vec<\_> = self
.raw\_bytes
.chunks\_exact(8)
.flat\_map(|chunk| {
let bytes: [u8; 8] = chunk.try\_into().unwrap();
let value = i64::from\_be\_bytes(bytes);
(value as i32).to\_be\_bytes()
})
.collect();
R8U::view(&new\_bytes)
}
Bitpix::F64 => {
// convert to i64 first
let new\_bytes: Vec<\_> = self
.raw\_bytes
.chunks\_exact(8)
.flat\_map(|chunk| {
let bytes: [u8; 8] = chunk.try\_into().unwrap();
let value = f64::from\_be\_bytes(bytes);
(value as f32).to\_be\_bytes()
})
.collect();
R8U::view(&new\_bytes)
}
\_ => R8U::view(&self.raw\_bytes),
}
};
textures.tex\_sub\_image\_3d\_with\_opt\_array\_buffer\_view(
offset.x + self.trim1 as i32,
offset.y + self.trim2 as i32,
offset.z + self.trim3 as i32,
self.width as i32,
self.height as i32,
self.depth as i32,
Some(view.as\_ref()),
);
Ok(())
}
fn get\_size(&self) -> (u32, u32, u32) {
// The true image size is given by ONAXISi keywords
(self.width, self.height, self.depth)
}
}

## Links found on page


