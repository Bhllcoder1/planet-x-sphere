---
source: https://irsa.ipac.caltech.edu/data/SPHEREx/docs/cutout_tool.html
fetched: 2026-11-14
status: 200
---

SPHEREx Cutout Tool

|  |  |
| --- | --- |
|  | SPHEREx Cutout Capabilities |

The SPHEREx Cutout Service enables users to extract spatial subsets from the large SPHEREx Spectral Image Multi-Extension FITS (MEF) files. These cutouts preserve the structure and metadata of the original files while providing smaller, more manageable datasets for analysis and visualization.

The primary SPHEREx data products are the Spectral Image MEFs, which can be several hundred megabytes in size. Because these files contain multiple Header Data Units (HDUs) with differing formats, World Coordinate Systems (WCSs), and cutout constraints, IRSA provides SPHEREx-specific cutout functionality designed to correctly handle all extensions and maintain spatial and spectral integrity.

  

### Accessing SPHEREx Cutouts

IRSA offers multiple ways to obtain cutouts of SPHEREx Spectral Image MEFs held on-premises at IPAC.

#### 1. Using the [SPHEREx Data Explorer](/applications/spherex)

* Open the Spectral Image Search tab to locate Spectral Images of interest.
* In the Results tab, use the scissors icon above the interactive display to specify a cutout size.
* Select the desired Spectral Images and click Generate Download Script.
* In the Download Options panel, choose cutouts to download a script that retrieves the selected cutout files.

#### 2. Using a Direct URL

If you have obtained on-premises URLs for SPHEREx Spectral Images (e.g., through an API query or by inspection of the browsable directories), you can manually request a cutout by appending position and size parameters to the URL. For example:  
  
curl -o cutout.fits "https://irsa.ipac.caltech.edu/ibe/data/spherex/qr/level2/2025W19\_2B/l2b-v11-2025-163/3/level2\_2025W19\_2B\_0073\_2D3\_spx\_l2b-v11-2025-163.fits?center=156.09328159,-41.64466331&size=0.1"

#### 3. Using Python

IRSA provides Python notebooks tutorials demonstrating how to create SPHEREx cutouts and interpret the associated PSF extensions:

* [SPHEREx Cutouts Tutorial](https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/)
* [SPHEREx PSF Tutorial](https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/)

## Links found on page

- https://caltech-ipac.github.io/irsa-tutorials/spherex-cutouts/
- https://caltech-ipac.github.io/irsa-tutorials/spherex-psf/
- https://irsa.ipac.caltech.edu/applications/spherex
