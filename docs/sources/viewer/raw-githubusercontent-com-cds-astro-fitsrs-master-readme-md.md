---
source: https://raw.githubusercontent.com/cds-astro/fitsrs/master/README.md
fetched: 2026-11-14
status: 200
---

FITS file reader written in pure Rust
-------------------------------------
[![](https://img.shields.io/crates/v/fitsrs.svg)](https://crates.io/crates/fitsrs)
[![](https://img.shields.io/crates/d/fitsrs.svg)](https://crates.io/crates/fitsrs)
[![API Documentation on docs.rs](https://docs.rs/fitsrs/badge.svg)](https://docs.rs/fitsrs/)
![testing CI](https://github.com/cds-astro/fitsrs/actions/workflows/rust.yml/badge.svg)
This parser was initiated for reading FITS images mapped onto HEALPix cells in the sky (See the [HiPS IVOA](https://www.ivoa.net/documents/HiPS/) standard) in order to use it in the [Aladin Lite](https://github.com/cds-astro/aladin-lite) web sky atlas.
Currently, fitsrs supports reading multiple HDU and is mainly dedicated to image extension reading.
For interpreting WCS keywords, see [wcs-rs](https://github.com/cds-astro/wcs-rs).
A very new support of binary table extension has been added. This has been done mainly for supporting the [tiled compressed image convention](https://fits.gsfc.nasa.gov/registry/tilecompression.html) that describes the storing of tile images in variable length arrays of a binary table.
The ASCII table extension parsing has not been implemented but it is possible to get an iterator over the data bytes as well as its mandatory cards from the header.
Contributing
------------
> [!WARNING]
> Running the test involves test files you can download [here](https://alasky.cds.unistra.fr/Aladin-Lite-test-files/fits-rs-test-files.tar). This tar is 2.2GB.
Once the tar file has been downloaded, put it into the root on your cloned repo and extract it:
```bash
tar -xvf fits-rs-test-files.tar
```
Once the files have been extracted you can run the tests locally:
```bash
cargo test --release
```
Features
--------
\* [X] Support single typed data block (i.e. image type data)
\* [X] Single HDU parsing, header and data units
\* [X] Support FITS files that may not fit in memory (iterator, possibility to seek directly to a specific pixel index/row)
\* [X] Async reading (requires to read the whole data. Seeking is not possible)
\* [X] Keeping COMMENTS, HISTORY and cards in the same order.
\* [X] CONTINUE Long String Keyword convention
\* [X] Keep all the cards in the original order
\* [X] Basic support of Bintable
\* [X] Tiled image convention for storing compressed images in FITS binary tables
- [X] Compression supported, GZIP, GZIP2 and RICE on u8, i16, i32 and f32.
- [ ] H\_compress and PLI0 compressions
- [X] Dithering techniques for floating point images. Not well tested (test samples are welcome)
- [ ] `NULL\_PIXEL\_MASK` column and `ZMASKCMP` keyword is not supported
\* [ ] FITS writer/serializer
\* [ ] ESO HIERARCH keyword convention
\* [ ] ASCII table extension parsing
\* [X] Support of multiple HDU. Image and binary tables extension support. Provide an idiomatic Rust iterator over the list of HDU.
\* [X] WCS parsing, see [wcs-rs](https://github.com/cds-astro/wcs-rs)
- [X] Simple Imaging Polynomial (SIP) supported but not well tested
- [ ] TNX, TPV, ZPX (non-standard conventions)
> [!NOTE]
> Features not done are not planned to be done. If you want fitsrs to support a specific convention, please open an issue or send us a mail to inform us of your use case(s) and we can manage to support them. The FITS standard and its conventions are massive and it is a huge work to support all of it.
License
-------
fitsrs has the double license MIT/Apache-2.0.
It uses code adapted from the famous [CFITSIO](https://github.com/HEASARC/cfitsio/blob/main/licenses/License.txt) library. Especially the RICE decompression source code has been ported from the original cfitsio [code](https://github.com/HEASARC/cfitsio/blob/main/ricecomp.c) to Rust.
Example
----------
```rust
use std::fs::File;
use std::io::Cursor;
use fitsrs::{Fits, ImageData, Pixels, HDU, hdu::header::Xtension};
use fitsrs::wcs::{ImgXY, LonLat};
use std::io::{BufReader, Read};
let f = File::open("samples/fits.gsfc.nasa.gov/EUVE.fits").unwrap();
let reader = BufReader::new(f);
let mut hdu\_list = Fits::from\_reader(reader);
while let Some(Ok(hdu)) = hdu\_list.next() {
match hdu {
// skip the primary HDU
HDU::Primary(\_) => (),
HDU::XImage(hdu) => {
let xtension = hdu.get\_header().get\_xtension();
let [naxis1, naxis2] = xtension.get\_naxis() else {
panic!("Expected two axis in the image");
};
let num\_pixels = (naxis1 \* naxis2) as usize;
// Try to access the WCS for an HDU image
if let Ok(wcs) = hdu.wcs() {
// Get the lonlat position on the sky of the pixel located at (0, 0) on the image
let xy = ImgXY::new(1.0, 1.0);
if let Some(lonlat) = wcs
.unproj\_lonlat(&xy) {
// Get the pixel position in the image of a sky location
let xy\_2 = wcs
.proj\_lonlat(&lonlat)
.unwrap();
assert!((xy.x() - xy\_2.x()).abs() <= 1e-9);
assert!((xy.y() - xy\_2.y()).abs() <= 1e-9);
}
}
let image = hdu\_list.get\_data(&hdu);
match image.pixels() {
Pixels::U8(it) => {
let data = it.collect::>();
assert\_eq!(num\_pixels, data.len())
},
Pixels::I16(it) => {
let data = it.collect::>();
assert\_eq!(num\_pixels, data.len())
},
Pixels::I32(it) => {
let data = it.collect::>();
assert\_eq!(num\_pixels, data.len())
},
Pixels::I64(it) => {
let data = it.collect::>();
assert\_eq!(num\_pixels, data.len())
},
Pixels::F32(it) => {
let data = it.collect::>();
assert\_eq!(num\_pixels, data.len())
},
Pixels::F64(it) => {
let data = it.collect::>();
assert\_eq!(num\_pixels, data.len())
},
}
},
HDU::XBinaryTable(hdu) => {
/\*let data: Vec<\_> = hdu\_list
.get\_data(&hdu)
.table\_data()
// Select specific fields with the select\_fields method
.select\_fields(&[
ColumnId::Name("mag"),
ColumnId::Name("phot\_bp\_mean\_mag"),
ColumnId::Name("phot\_rp\_mean\_mag"),
])
.collect();
\*/
let num\_rows = hdu.get\_header()
.get\_xtension()
.get\_num\_rows();
let rows: Vec<\_> = hdu\_list
.get\_data(&hdu)
.row\_iter()
.collect();
assert\_eq!(num\_rows, rows.len());
},
HDU::XASCIITable(hdu) => {
let num\_bytes = hdu.get\_header()
.get\_xtension()
.get\_num\_bytes\_data\_block();
let data = hdu\_list.get\_data(&hdu)
.bytes()
.collect::>();
assert\_eq!(num\_bytes as usize, data.len());
},
}
}
```
Integration with `image`
------------------------
Enable the optional `image` feature and register the decoding hook to let the `image` crate read FITS files:
```toml
[dependencies]
fitsrs = { version = "0.4.1", features = ["image"] }
```
```rust,ignore
use fitsrs::image\_integration::register\_fits\_decoding\_hook;
use image::ImageReader;
fn main() -> image::ImageResult<()> {
register\_fits\_decoding\_hook();
let img = ImageReader::open("samples/hipsgen/Npix8.fits")?
.decode()?;
println!("decoded FITS dimensions: {}x{}", img.width(), img.height());
Ok(())
}
```
The decoder scans all HDUs and picks the first suitable 2D image (including the first plane of image cubes). `BZERO` and `BSCALE` header keywords are applied during decoding when present.
FITS does not mandate a display range for floating-point or high-bit-depth integer data. The pixel type mapping is therefore:
| BITPIX | `ColorType` | Notes |
|--------|-------------|-------|
| 8 | `L8` | exact |
| 16 | `L16` | BZERO/BSCALE applied; common case BZERO=32768 recovers unsigned u16 |
| −32 | `Rgb32F` | full precision; R=G=B (grayscale stored as colour) |
| 32 | `Rgb32F` | cast to f32; may lose precision for large integers |
| 64 | `Rgb32F` | cast to f32; lossy |
| −64 | `Rgb32F` | cast to f32; lossy |
For the float/integer depths the `Rgb32F` output preserves the original dynamic range; downstream consumers are responsible for tone-mapping or normalisation.
For async input readers:
```rust
#[tokio::test]
async fn parse\_fits\_async() {
use std::fs::File;
use std::io::Cursor;
use fitsrs::hdu::AsyncHDU;
use fitsrs::hdu::data::stream::Stream;
use fitsrs::async\_fits::AsyncFits;
use fitsrs::hdu::header::extension::Xtension;
use std::io::{BufReader, Read};
// reader needs to implement futures::io::AsyncRead
let f = File::open("samples/fits.gsfc.nasa.gov/EUVE.fits").unwrap();
let reader = BufReader::new(f);
let mut hdu\_list = AsyncFits::from\_reader(reader);
while let Some(Ok(mut hdu)) = hdu\_list.next().await {
match hdu {
AsyncHDU::Primary(\_) => (),
AsyncHDU::Image(hdu) => {
let xtension = hdu.get\_header().get\_xtension();
let [naxis1, naxis2] = xtension.get\_naxis() else {
panic!("Expected two axis in the image");
};
let num\_pixels = (naxis1 \* naxis2) as usize;
match hdu\_list.get\_data(hdu) {
Stream::U8(st) => {
let data = st.collect::>().await;
assert\_eq!(num\_pixels, data.len())
},
Stream::I16(st) => {
let data = st.collect::>().await;
assert\_eq!(num\_pixels, data.len())
},
Stream::I32(st) => {
let data = st.collect::>().await;
assert\_eq!(num\_pixels, data.len())
},
Stream::I64(st) => {
let data = st.collect::>().await;
assert\_eq!(num\_pixels, data.len())
},
Stream::F32(st) => {
let data = st.collect::>().await;
assert\_eq!(num\_pixels, data.len())
},
Stream::F64(st) => {
let data = st.collect::>().await;
assert\_eq!(num\_pixels, data.len())
},
}
},
AsyncHDU::XBinaryTable(hdu) => {
let num\_bytes = hdu.get\_header()
.get\_xtension()
.get\_num\_bytes\_data\_block();
let it\_bytes = hdu\_list.get\_data(hdu);
let data = it\_bytes.collect::>().await;
assert\_eq!(num\_bytes as usize, data.len());
},
AsyncHDU::XASCIITable(hdu) => {
let num\_bytes = xhdu.get\_header()
.get\_xtension()
.get\_num\_bytes\_data\_block();
let it\_bytes = hdu\_list.get\_data(hdu);
let data = it\_bytes.collect::>().await;
assert\_eq!(num\_bytes as usize, data.len());
},
}
}
}
```

## Links found on page


