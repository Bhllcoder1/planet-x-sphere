---
source: https://irsa.ipac.caltech.edu/cloud_access/
fetched: 2026-11-14
status: 200
---

Cloud Data Access

Cloud Data Access
=================

IRSA datasets are available on Amazon Web Services (AWS) S3 cloud storage.
The files are hosted through the AWS Open Data Sponsorship Program, allowing them to be downloaded or accessed directly without credentials or egress charges.

**Accessing IRSA Data on AWS S3**

Here are some key terms for accessing data on S3:

* Bucket: Container holding objects.
* Object: Analogous to a file. We ignore the minor differences here and just use "file" for simplicity.
* S3 prefix: Path to a directory, relative to the bucket.
* S3 key: Path to a file, relative to the bucket.

There are many ways to access the buckets, including:

* Python: See our [Notebook Tutorials](/docs/notebooks/) for python demonstrations.
* Command line: See the [AWS Command Line Interface](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html) documentation.
  + Basic example:
      
    `aws s3 ls --no-sign-request "s3://${bucket_name}/${prefix}/"`
* Bulk downloads: Download scripts are provided in most buckets.
  Download scripts for catalogs can also be found through the links at [Catalog Bulk Download](/data/download/).

**Note:**
The data are freely available and no special permissions or credentials are required.
However, most tools will look for credentials by default and raise an error when none are found.
To avoid this, make an anonymous connection.
Typically this is done by including a parameter such as `--no-sign-request` or `anonymous=True`.
Consult the tool's documentation for details.

---

[SPHEREx](/Missions/spherex.html)
---------------------------------

For descriptions of the releases, data products, and access methods, see the [SPHEREx Archive User Guide](/spherex-archive-documentation/).
To find a specific product in the bucket, prepend the S3 prefix listed below to the directory names described at [Browsable Directories](/spherex-archive-documentation/spherex-data-access/#browsable-directories).

Bucket: **`nasa-irsa-spherex`**
  
Region: us-east-1
  
[Browse nasa-irsa-spherex](https://nasa-irsa-spherex.s3.us-east-1.amazonaws.com/index.html)

**Data Release 1 (DR1)**

[registry.opendata.aws/**spherex-dr1**](https://registry.opendata.aws/spherex-dr1/) (pending publish by AWS)

* **Spectral Images, calibration, and other products**
    
  S3 prefix: `dr1`

**Quick Release 3 (QR3)**

[registry.opendata.aws/**spherex-qr3**](https://registry.opendata.aws/spherex-qr3/) (pending publish by AWS)

* **Spectral Images, calibration, and other products**
    
  S3 prefix: `qr3`

**Quick Release 2 (QR2)**

[registry.opendata.aws/**spherex-qr**](https://registry.opendata.aws/spherex-qr/)

* **Spectral Images, calibration, and other products**
    
  S3 prefix: `qr2`

[Euclid](/Missions/euclid.html)
-------------------------------

For descriptions of the releases, data products, and access methods, see the [Euclid Archive User Guide](/euclid-archive-documentation/).
To find a specific product in a bucket, prepend the S3 prefix listed below to the directory names described at [Data Products](/euclid-archive-documentation/data-products/).

**Data Release 1 (DR1)**

Bucket: **`nasa-irsa-euclid-dr1`**
  
Region: us-east-1
  
[Browse nasa-irsa-euclid-dr1](https://nasa-irsa-euclid-dr1.s3.us-east-1.amazonaws.com/index.html)
  
[registry.opendata.aws/**euclid-dr1**](https://registry.opendata.aws/euclid-dr1/) (pending publish by AWS)

* **Images, Spectra, and Catalogs**
    
  S3 prefix: `dr1`

Enhanced Contributed Data Products:

* **Catalogs and Spectra in HATS Format** ([HATS Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `contributed/dr1/hats`

**Quick Release 2 (Q2)**

Bucket: **`nasa-irsa-euclid-q2`**
  
Region: us-east-1
  
[Browse nasa-irsa-euclid-q2](https://nasa-irsa-euclid-q2.s3.us-east-1.amazonaws.com/index.html)
  
[registry.opendata.aws/**euclid-q2**](https://registry.opendata.aws/euclid-q2/) (pending publish by AWS)

* **Images and Catalogs**
    
  S3 prefix: `q2`

**Quick Release 1 (Q1)**

Bucket: **`nasa-irsa-euclid-q1`**
  
Region: us-east-1
  
[Browse nasa-irsa-euclid-q1](https://nasa-irsa-euclid-q1.s3.us-east-1.amazonaws.com/index.html)
  
[registry.opendata.aws/**euclid-q1**](https://registry.opendata.aws/euclid-q1/)

* **Images, Spectra, and Catalogs**
    
  S3 prefix: `q1`

Enhanced Contributed Data Products:

* **Merged Objects HATS Catalog** ([HATS Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `contributed/q1/merged_objects/hats`

[WISE](/Missions/wise.html)
---------------------------

Bucket: **`nasa-irsa-wise`**
  
Region: us-west-2
  
[Browse nasa-irsa-wise](https://nasa-irsa-wise.s3.us-west-2.amazonaws.com/index.html)

**AllWISE**

[registry.opendata.aws/**wise-allwise**](https://registry.opendata.aws/wise-allwise/)

* **Images Atlas** (FITS)
    
  S3 prefix: `wise/allwise/images/p3am_cdd`
    
  For file naming conventions, see [AllWISE IBE docs](/ibe/docs/wise/allwise/p3am_cdd/) and [Map IBE to cloud paths](ibe_to_cloud_paths.html).

Enhanced Contributed Data Products:

* **Source Catalog** ([HEALPix Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `wise/allwise/catalogs/p3as_psd/healpix_k5`
    
  Parquet name: `wise-allwise.parquet`

**All-Sky**

[registry.opendata.aws/**wise-allsky**](https://registry.opendata.aws/wise-allsky/)

* **Single-exposure Image Sets** (FITS)
    
  S3 prefix: `wise/allsky/images/4band_p1bm_frm`
    
  For file naming conventions, see [All-Sky IBE docs](/ibe/docs/wise/allsky/4band_p1bm_frm/) and [Map IBE to cloud paths](ibe_to_cloud_paths.html).

**3-Band Cryo**

[registry.opendata.aws/**wise-cryo-3band**](https://registry.opendata.aws/wise-cryo-3band/)

* **Single-exposure Image Sets** (FITS)
    
  S3 prefix: `wise/cryo-3band/images/3band_p1bm_frm`
    
  For file naming conventions, see [3-Band Cryo IBE docs](/ibe/docs/wise/cryo_3band/3band_p1bm_frm/) and [Map IBE to cloud paths](ibe_to_cloud_paths.html).

**Post-Cryo**

[registry.opendata.aws/**wise-postcryo**](https://registry.opendata.aws/wise-postcryo/)

* **Single-exposure Image Sets** (FITS)
    
  S3 prefix: `wise/postcryo/images/2band_p1bm_frm`
    
  For file naming conventions, see [Post-Cryo IBE docs](/ibe/docs/wise/postcryo/2band_p1bm_frm/) and [Map IBE to cloud paths](ibe_to_cloud_paths.html).

[NEOWISE Reactivation](/Missions/wise.html)
-------------------------------------------

Bucket: **`nasa-irsa-wise`**
  
Region: us-west-2
  
[Browse nasa-irsa-wise](https://nasa-irsa-wise.s3.us-west-2.amazonaws.com/index.html)

**NEOWISE-R**

[registry.opendata.aws/**wise-neowiser**](https://registry.opendata.aws/wise-neowiser/)

* **Single-exposure Image Sets** (FITS)
    
  S3 prefix: `wise/neowiser/images/p1bm_frm`
    
  For file naming conventions, see [NEOWISE-R IBE docs](/ibe/docs/wise/neowiser/p1bm_frm/) and [Map IBE to cloud paths](ibe_to_cloud_paths.html).

Enhanced Contributed Data Products:

* **Single-exposure Source Table** ([HEALPix Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `wise/neowiser/catalogs/p1bs_psd/healpix_k5/{PART}`
    
  Parquet name: `neowiser-healpix_k5-{PART}.parquet`
    
  Composed of yearly data releases plus an addendum, stored separately.
  Replace `{PART}` with either `yearN` (where N is an integer, 1‑11) or `addendum`.

[Spitzer](/Missions/spitzer.html)
---------------------------------

Bucket: **`nasa-irsa-spitzer`**
  
Region: us-west-2
  
[Browse nasa-irsa-spitzer](https://nasa-irsa-spitzer.s3.us-west-2.amazonaws.com/index.html)

**Spitzer Enhanced Imaging Products (SEIP)**

[registry.opendata.aws/**spitzer-seip**](https://registry.opendata.aws/spitzer-seip/)

* **Super Mosaics** (FITS)
    
  S3 prefix: `spitzer/seip/seip_science/images`

[Zwicky Transient Facility (ZTF)](/Missions/ztf.html)
-----------------------------------------------------

Bucket: **`ipac-irsa-ztf`**
  
Region: us-east-1
  
[Browse ipac-irsa-ztf](https://ipac-irsa-ztf.s3.us-east-1.amazonaws.com/index.html)

[registry.opendata.aws/**ztf**](https://registry.opendata.aws/ztf/)

**Data Release 24 (DR24)**

Enhanced Contributed Data Products:

* **Objects Table** ([HATS Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `ztf/enhanced/dr24/objects/hats`
* **Lightcurves** ([HATS Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `ztf/enhanced/dr24/lc/hats`

[unWISE](/data/WISE/unWISE/overview.html)
-----------------------------------------

Bucket: **`nasa-irsa-wise`**
  
Region: us-west-2
  
[Browse nasa-irsa-wise](https://nasa-irsa-wise.s3.us-west-2.amazonaws.com/index.html)

[registry.opendata.aws/**wise-unwise**](https://registry.opendata.aws/wise-unwise/)

Enhanced Contributed Data Products:

* **Time-Domain Catalog** ([HEALPix Parquet](/docs/parquet_catalogs/))
    
  S3 prefix: `unwise/neo7/catalogs/time_domain/healpix_k5`
    
  Parquet name: `unwise-neo7-time_domain-healpix_k5.parquet`

[OpenUniverse 2024 Matched Rubin and Roman Simulations](/data/theory/openuniverse2024/overview.html)
----------------------------------------------------------------------------------------------------

Bucket: **`nasa-irsa-simulations`**
  
Region: us-east-1
  
[Browse nasa-irsa-simulations](https://nasa-irsa-simulations.s3.us-east-1.amazonaws.com/index.html)

[registry.opendata.aws/**openuniverse2024**](https://registry.opendata.aws/openuniverse2024/)

**Preview**

* **Preview of Roman simulated data products** (FITS, Parquet)
    
  S3 prefix: `openuniverse2024/roman/preview`
* **Preview of Rubin simulated data products** (FITS, Parquet)
    
  S3 prefix: `openuniverse2024/rubin/preview`

**Full area release**

* **Full area release of Roman simulated data products** (FITS, Parquet)
    
  S3 prefix: `openuniverse2024/roman/full`
* **Full area release of Rubin simulated data products** (FITS, Parquet)
    
  S3 prefix: `openuniverse2024/rubin/full`

---

**Requesting additional datasets:** If there are other IRSA holdings that you would like us to make available on the cloud, please contact IRSA's [Help Desk](/docs/help_desk.html).

## Links found on page

- https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html
- https://ipac-irsa-ztf.s3.us-east-1.amazonaws.com/index.html
- https://irsa.ipac.caltech.edu/Missions/euclid.html
- https://irsa.ipac.caltech.edu/Missions/spherex.html
- https://irsa.ipac.caltech.edu/Missions/spitzer.html
- https://irsa.ipac.caltech.edu/Missions/wise.html
- https://irsa.ipac.caltech.edu/Missions/ztf.html
- https://irsa.ipac.caltech.edu/cloud_access/ibe_to_cloud_paths.html
- https://irsa.ipac.caltech.edu/data/WISE/unWISE/overview.html
- https://irsa.ipac.caltech.edu/data/download/
- https://irsa.ipac.caltech.edu/data/theory/openuniverse2024/overview.html
- https://irsa.ipac.caltech.edu/docs/help_desk.html
- https://irsa.ipac.caltech.edu/docs/notebooks/
- https://irsa.ipac.caltech.edu/docs/parquet_catalogs/
- https://irsa.ipac.caltech.edu/euclid-archive-documentation/
- https://irsa.ipac.caltech.edu/euclid-archive-documentation/data-products/
- https://irsa.ipac.caltech.edu/ibe/docs/wise/allsky/4band_p1bm_frm/
- https://irsa.ipac.caltech.edu/ibe/docs/wise/allwise/p3am_cdd/
- https://irsa.ipac.caltech.edu/ibe/docs/wise/cryo_3band/3band_p1bm_frm/
- https://irsa.ipac.caltech.edu/ibe/docs/wise/neowiser/p1bm_frm/
- https://irsa.ipac.caltech.edu/ibe/docs/wise/postcryo/2band_p1bm_frm/
- https://irsa.ipac.caltech.edu/spherex-archive-documentation/
- https://irsa.ipac.caltech.edu/spherex-archive-documentation/spherex-data-access/#browsable-directories
- https://nasa-irsa-euclid-dr1.s3.us-east-1.amazonaws.com/index.html
- https://nasa-irsa-euclid-q1.s3.us-east-1.amazonaws.com/index.html
- https://nasa-irsa-euclid-q2.s3.us-east-1.amazonaws.com/index.html
- https://nasa-irsa-simulations.s3.us-east-1.amazonaws.com/index.html
- https://nasa-irsa-spherex.s3.us-east-1.amazonaws.com/index.html
- https://nasa-irsa-spitzer.s3.us-west-2.amazonaws.com/index.html
- https://nasa-irsa-wise.s3.us-west-2.amazonaws.com/index.html
- https://registry.opendata.aws/euclid-dr1/
- https://registry.opendata.aws/euclid-q1/
- https://registry.opendata.aws/euclid-q2/
- https://registry.opendata.aws/openuniverse2024/
- https://registry.opendata.aws/spherex-dr1/
- https://registry.opendata.aws/spherex-qr/
- https://registry.opendata.aws/spherex-qr3/
- https://registry.opendata.aws/spitzer-seip/
- https://registry.opendata.aws/wise-allsky/
- https://registry.opendata.aws/wise-allwise/
- https://registry.opendata.aws/wise-cryo-3band/
- https://registry.opendata.aws/wise-neowiser/
- https://registry.opendata.aws/wise-postcryo/
- https://registry.opendata.aws/wise-unwise/
- https://registry.opendata.aws/ztf/
