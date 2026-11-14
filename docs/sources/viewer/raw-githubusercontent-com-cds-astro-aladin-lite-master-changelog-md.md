---
source: https://raw.githubusercontent.com/cds-astro/aladin-lite/master/CHANGELOG.md
fetched: 2026-11-14
status: 200
---

# Changelogs
## Unreleased
### What's Changed
## Released
### 3.9.0-beta
\* [feat] AVM tag reading from PNG extension images by [@bmatthieu3][bmatthieu3] 
\* [feat] Export of aladin lite view with AVM tags [@tboch][tboch] 
\* [fix] Switching back and forth the layer to an image  by [@bmatthieu3][bmatthieu3]
\* [fix] Open settings on catalog with a HiPS3D 
\* [fix] keep the cut values for each tile format 
\* [fix] Keep approx the same level of zoom when the screen is resized 
\* [fix] 
\* [fix] 
\* [feat] Support of SIP astrometry keywords in FITS file 
\* [fix] 
\* [feat] Progressive catalogs: first try loading metadata.xml, switch back on Metadata.xml if it fails 
\* [feat] Support skewer selection for footprints/shapes  by [@tomdonaldson][tomdonaldson]
### 3.8.0
\* [fix] Fix shape hover colors when overlay uses named color (increaseBrightness() accepts names now) 
\* [feat] Selected and hovered items (shapes, sources, ...) are rendered at last. 
\* [feat] Add selectionLineWidth option for shapes and catalogs. 
\* [fix] horizontal/vertical overlay lines appearing correctly 
\* [fix] layer opacity restored when switching from not visible to visible 
\* [feat] dark/light mode for the interface
\* [fix] polylines shapes size not consistent w.r.t to div size 
\* [feat] 'stackChanged' new event informing when a layer has been added, removed or swapped.
\* [ui] a new HiPS browser window to search and find HiPS among the HiPS worldwide network.
\* [ui] new settings panel for Catalog overlays to change the size, color or shapes of sources
\* [ui] possibility to swap 2 layers. Functional but not definitive, it would be better to allow drag and drop amond the layers.
\* [fix] fix local HiPS loading.
\* [ui] WIP. A toolbar object
\* [fix] fix selection of footprints. In the future allow a skew selection mode and a additive selection shortkey.
\* [fix] inertia bug when zooming in/out
\* [license] License change from GPLv3 to LGPLv3-or-later
### 3.7.0-beta
#### What's Changed
\* [feat] flip longitude axis global method on Aladin by [@bmatthieu3][bmatthieu3] in 
\* [feat] add rotation event by [@ManonMarchand][ManonMarchand] in 
\* [docs] just fixing typo in image's doc by [@ManonMarchand][ManonMarchand] in 
\* [docs] change to an image with correct astrometry in example by [@ManonMarchand][ManonMarchand] in 
\* [docs] clarify use of precision in Coo by [@alexgoff][alexgoff] in 
\* [feat] allow setting HiPS CORS and credential options by [@pmatsson][pmatsson] in 
\* [feat] color picker and read pixel(s) API methods by [@bmatthieu3][bmatthieu3] in 
\* [fix] chandra hips display and akari by [@bmatthieu3][bmatthieu3] in 
\* [enhancement] update to the new version of fitsrs by [@bmatthieu3][bmatthieu3] in 
\* [fix] 26 channel color offset by [@bmatthieu3][bmatthieu3] in 
\* [fix] Circle intersectsBBox by [@emellega][emellega] in 
\* [feat] anti aliasing on lines plotted by the GPU by [@bmatthieu3][bmatthieu3] in 
\* [feat] source custom color and size from its data content by [@bmatthieu3][bmatthieu3] in 
\* [feat] catalog new select method by [@bmatthieu3][bmatthieu3] in 
\* [feat] HiPS 3D impl by [@bmatthieu3][bmatthieu3] in 
\* [feat] customize share URL function by [@tboch][tboch] in 
\* enhancement: use TAP entry point to query NED by [@bmatthieu3][bmatthieu3] in 
\* [perf] refac geometrical computations using Vec3/Mat3 instead of Vec4/Mat4 [@bmatthieu3][bmatthieu3] in 
\* [fix] distortion at poles by [@bmatthieu3][bmatthieu3] in 
\* [feat] new aladin option `lockNorthUp` to keep north pole up [@bmatthieu3][bmatthieu3] in 
### 3.6.3
#### What's Changed
\* [maint] remove Shift shorcut for triggering rectangular source selection. Shortcuts will be implemented later. by [@bmatthieu3][bmatthieu3] in 
\* [fix] decide to show the contextual menu only if user has not right click while moving more than 10px. by [@bmatthieu3][bmatthieu3] in 
\* [fix] CSS selector took the whole div in smartphone usage. by [@bmatthieu3][bmatthieu3] in 
\* [fix] smartphone 2 fingers zoom pinching around the 180deg meridian. by [@bmatthieu3][bmatthieu3] in 
\* [fix] use copy2Clipboard utils functions from contextual menu. by [@bmatthieu3][bmatthieu3] in 
\* [fix] improved ID/HiPS url detection (retry if a relative path to a local HiPS is given as it is considered as an ID). by [@bmatthieu3][bmatthieu3] in 
### 3.6.1
#### What's Changed
\* [feat] AVM tags support found in jpeg headers by [@bmatthieu3][bmatthieu3] in 
\* [feat] Merge remove overlay by name to Develop by [@Xen0Xys][Xen0Xys] in 
\* [fix] Restore A.footprint function by [@szpetny][szpetny] in 
\* [testing] Merge playwright tests to Develop by [@Xen0Xys][Xen0Xys] in 
\* [fix] Version 3.5.1 by [@bmatthieu3][bmatthieu3] in 
\* [fix] Also add style sheet in shadow dom context by [@ManonMarchand][ManonMarchand] in 
\* [feat] Add selectionColor, onClick to catalog parameters handled by updateShape by [@simontorres][simontorres] in 
\* [feat] HiPS cube support by [@bmatthieu3][bmatthieu3] in 
\* [feat] PolySelect implementation and miscellaneous selection improvements by [@pmatsson][pmatsson] in 
\* [fix] Request a redraw after adding an array of footprints by [@ManonMarchand][ManonMarchand] in 
\* [fix] Circle opacity not working by [@tboch][tboch] in 
\* [fix] Bug introduced in #218 by [@ManonMarchand][ManonMarchand] in 
\* [fix] CSS style for canvas element is more selective by [@tboch][tboch] in 
\* [maint] Add zenodo.json file by [@ManonMarchand][ManonMarchand] in 
\* [maint] Remove old files using jquery by [@cquiroz][cquiroz] in 
\* [fix] Display of HiPS with maxOrder = 0 by [@bmatthieu3][bmatthieu3] in 
\* [fix] Combine requestedOptions and Aladin.DEFAULT\_OPTIONS with spread operator by [@pcuste1][pcuste1] in 
\* [fix] Add back cmap reverse checkbox by [@bmatthieu3][bmatthieu3] in 
\* [fix] JPEG draw black screen when tiles are missing by [@bmatthieu3][bmatthieu3] in 
\* [fix] Filled moc drawing reverse longitude by [@bmatthieu3][bmatthieu3] in 
\* [doc] Deprecate longitudeReversed HiPS options property by [@bmatthieu3][bmatthieu3] in 
\* [fix] Stop contextmenu event propagation only if context menu enabled by [@alexgoff][alexgoff] in 
\* [ui] Minor fixes and enhancements by [@bmatthieu3][bmatthieu3] in 
\* [fix] Handle NaNs by the GPU (fix for windows) by [@bmatthieu3][bmatthieu3] in 
\* [fix] Grid labels formatting by [@bmatthieu3][bmatthieu3] in 
\* [feat] Shape function given to a catalog by [@bmatthieu3][bmatthieu3] in 
\* [fix] Tooltip pos out of fov by [@bmatthieu3][bmatthieu3] in 
\* [fix] MOC settings after its creation by [@bmatthieu3][bmatthieu3] in 
\* [fix] ICRS to FK5J2000 cooframe renaming by [@bmatthieu3][bmatthieu3] in 
\* [fix] Revert #264 by [@bmatthieu3][bmatthieu3] in 
#### New Contributors
\* [@cquiroz][cquiroz] made their first contribution in 
\* [@pcuste1][pcuste1] made their first contribution in 
\* [@alexgoff][alexgoff] made their first contribution in 
\*\*Full Changelog\*\*: 
### 3.6.1-beta
#### What's Changed
\* [feat] Add selectionColor, onClick to catalog parameters handled by updateShape by [@simontorres][simontorres] in 
\* [feat] HiPS cube support by [@bmatthieu3][bmatthieu3] in 
\* [feat] PolySelect implementation and miscellaneous selection improvements by [@pmatsson][pmatsson] in 
\* [fix] Request a redraw after adding an array of footprints by [@ManonMarchand][ManonMarchand] in 
\* [fix] Circle opacity not working by [@tboch][tboch] in 
\* [fix] Bug introduced in #218 by [@ManonMarchand][ManonMarchand] in 
\* [fix] CSS style for canvas element is more selective by [@tboch][tboch] in 
\* [maint] add zenodo.json file by [@ManonMarchand][ManonMarchand] in 
\* [maint] Remove old files using jquery by [@cquiroz][cquiroz] in 
#### New Contributors
\* [@cquiroz][cquiroz] made their first contribution in 
\*\*Full Changelog\*\*: 
### 3.5.1-beta
\* [feat] Add support for name removing in `removeOverlay` method
\* [test] Add support of playwright. Instructions in the readme for running the test matching snapshots [PR #176]
\* [fix] Order of overlays in the stack now matches the addMOC/addCatalog/addOverlay calls ordering
\* [doc] Expose the API of Coo class
\* [fix] Insert aladin css inside the aladin lite so that it should be compliant with the use of shadow DOMs [cds-astro/ipyaladin#113], [marimo-team/marimo#2106]
\* [feat] Add possibility of giving a local JS FileList to load a locally-stored HiPS without starting an HTTP server 
\* [fix] removeOverlayByName
### 3.5.0-beta
\* [enhancement] add `options.colnames` to A.catalogFromVizieR to tell VizieR we want absolutely want to retrieve specific columns
\* [feat] provide a new drawAxes option to A.ellipse. This is useful for plotting error ellipsis.
### 3.4.5-beta
\* [feat] add `layerChanged` event when a layer is added or removed
\* [deprecate] of `select` event, use `objectsSelected` event instead
\* [ui] add the ability to switch the tile format to download
### 3.4.3-beta
\* [bugfix] zoom control buttons
\* [feat] save a MOC as a JSON file from the UI 
\* [feat] save a source selection from the measurement table as a CSV file
\* [feat] allow to display jpeg/jpg images with a wcs passed as a JS dictionary: 
### 3.4.2-beta
\* [impr] Improve smartphone support by setting media queries + a better logic for deploying the contextual menu sub options.
\* [impr] Improve `WCS` view export with 3rd euler rotation encoding: . Still some cases are to be handled like: crval on the equator or cylindrical with a galactic frame rotation.
\* [fixed] Change `RADECSYS` to `RADESYS` for `Aladin#getViewWCS` to follow fits standard deprecation
\* [feat] Add new method `Aladin#getViewImageBuffer` to get the current view as a PNG buffer
\* [feat] New line rasterizer using GL instancing. This enhances the rendering speed of MOCs.
### 3.3.3
\* [feat] UI: add HiPS basic filter that filters the `hipsList` given
\* [feat] New `hipsList` option parameter when instancing a new Aladin object.
\* [feat] Zoom smoothing using hermite cubic interpolation functions
\* [feat] shape option of Catalog and ProgressiveCat accepts a function returning a Footprint. This allow user to
associate a footprint to a specific source
\* [feat] Hover color support by [@pmatsson][pmatsson] and [@bmatthieu3][bmatthieu3] in 
### 3.3.2
\* [fixed] do not allow to query the properties several times for an imageHiPS
\* [fixed] Detecting raytracing rendering mode. Adapt the rendering mode in function of the fov value and the projection used. Some projections do have more distortions with wide FoVs so it is better to use the raytracing rendering mode when fov >= smaller FoV threshold.
### 3.3.0
\* [fixed] multiple calls to setImageSurvey with the same survey object led to strange behaviour.
\* [perf] Display the first tile received instantly with no blending. Should enhance the slow reported in issue #88.
\* [fixed] A.on('select') (debugged from ipyaladin)
\* [fixed] Simbad pointer in galactical frame, cone search of simbad/vizier cats/other cone search services in galactical frame and MOC creation from selection in galactical frame => there is now a new `frame` optional param to Aladin.pix2world. If not given, the coo returned are in the frame of the view.
\* [doc] Add doc for image survey definition
\* [deprecation] A.createImageSurvey/A.newImageSurvey are now deprecated (but still in the API). Please use `A.imageHiPS` instead by providing a valid url or CDS ID conformed to 
\* [refac] Simplify the instanciation of an imageHiPS/ imageFITS. Add a `A.imageHiPS` method for defining a HiPS object
\* [fixed] At initialisation, giving a fov > 180 was clamped back to 180 even if we specify allsky projection (i.e. accepting fov > 180). This is now fixed.
\* [fixed] MeasurementTable now display the full cell values (no ellipsis anymore)
\* [fixed] aladin.on('select') has been implemented. Callback is triggered on a circle and rect selections for not on polygonal selection.
\* [fixed] the cooFrame UI selector is updated if the user calls `aladin.setFrame`
\* [fixed] `reticleColor` and `reticleSize` options in the public API
\* Restore setFoVRange
\* Add CSS class for positioning the UI elements as the user wants. See the API doc aladin options for the class names to use.
\* [style] The default grid color is now `rgb(178, 50, 178)` to fit the classic Aladin color palette
\* [feat] The object of grid options `gridOptions` is now available in the public API
\* [fixed] The parameters `gridColor` and `gridOpacity`, `gridOptions.showLabels` now work as expected
\* New documentation API (W.I.P) here: 
\* New release page here: 
\* A major UI update by [@bmatthieu3][bmatthieu3]
1. Some API new classes A.box, A.button
2. A status bar where the user can enque messages for a specific amount of time (Aladin.addStatusBarMessage)
\* Remove of JQuery and autocompletejs dependencies by [@bmatthieu3][bmatthieu3]
\* Fix some performances issues, i.e. a bug when resizing the aladin lite view and which launched several parallel requestAnimationFrame by [@bmatthieu3][bmatthieu3]
\* Polygon and circular selection (see Aladin class API documentation for how to use it)
\* ObsCore and Datalink votable parsing and interpretation. This work is still in progress and made in the frame of the SKA radio mission by [@bmatthieu3][bmatthieu3] in 
\* SODA service query window formular by [@bmatthieu3][bmatthieu3] in 
\* read only catalog option by [@szpetny][szpetny] in 
\* Small changed regarding drawing a footprint by [@szpetny][szpetny] in 
\* Object and footprint click/hover events expose mouse coordinates by [@szpetny][szpetny] in 
\* A proposal of a new feature - fill the polygon with a color by [@szpetny][szpetny] in 
\* update getViewWCS to adapt to projection by [@ManonMarchand][ManonMarchand] in 
\* New SAMP support by [@bmatthieu3][bmatthieu3] in 
\* A possibility to create Coo and Footprint objects by [@szpetny][szpetny] in 
\* new method aladin.getFrame() that returns the name of the current coordinate system
\* `getViewWCS` now adapts to the `cooFrame` and the `projection`
\* `getFov` is no longer capped at 180°
\* bugfix `setProjection` now also updates for 'PAR' and 'SFL' projections
### 3.2.0
\* MOC rendering perf enhanced. Possibility to draw only the perimeter of a MOC object (perimeter set to True)
\* Many fixes e.g. footprint rendering for all sky projections
\* A line/shape webgl rasterizer thanks to the use of the `lyon`crate. MOCs and grid lines are rendered that way. Therefore, it is possible to change the grid lines thickness
\* Use of vite for the project management and deployment
### 3.1.0
\* Add message for safari users to enable WebGL2 feature and reload the page by [@bmatthieu3][bmatthieu3] in 
\* Starting fits support by [@bmatthieu3][bmatthieu3] in 
\* display fits images with the drag and drop by [@bmatthieu3][bmatthieu3]
![Kapture 2023-03-23 at 14 34 28](https://user-images.githubusercontent.com/2772384/227264124-8e05a3d8-1565-497f-a118-39fab3c6ed83.gif)
\* support `webp` tile format by [@bmatthieu3][bmatthieu3] and [@tboch][tboch]
\* planetary name resolver by [@tboch][tboch]
\* small ui changes and bug fixes by [@bmatthieu3][bmatthieu3]
\* add codemeta and its validatior action by [@ManonMarchand][ManonMarchand] in 
### 3.0.0
Official release of Aladin Lite v3, [as announced in CDS news](https://cds.unistra.fr/news.php?fn\_mode=fullnews&fn\_incl=0&fn\_id=958).
\* Fix missing tiles issue by [@tboch][tboch] in 
\* Hips catalogue filtering by [@tboch][tboch] in 
\* Make footprint selection easier by [@tboch][tboch] in 
\* Bug fix: enable different colors for multiple polylines in same layer by [@tboch][tboch] in 
\* Method remove to delete individual source from a catalogue layer by [@tboch][tboch] in 
\* Stop animation by [@tboch][tboch] in 
\* Add message for safari users to enable WebGL2 feature and reload the page by [@bmatthieu3][bmatthieu3] in 
## Version: 2.x.x
### 2020-08
\* polyline improvements (by [@imbasimba][imbasimba])
### 2020-07
\* new method stopAnimation
### 2020-06
\* new method in Catalog layer to \*remove\* individual \*Source\* objects
### 2019-10
\* displayFITS can now take a base64 data URL as input
### 2019-05-03
\* https URLs for Simbad pointer
### 2019-04-30
\* empty Downloader queue when changing displayed HiPs
### 2019-02-06
\* bug fix: MOC cells at order 0 were not displayed
### 2019-01
\* add method getViewWCS
### 2018-10-30
\* bug fix affichage MOC order>11
### 2018-09-24
\* bug fix in VOTable parsing: CDATA text was always blank in  |### 2018-09-18
\* drawing algorith improved: no more flickering when zooming in
### 2018-09-17
\* improvement on mobile device: pinch zoom works, panning works better
### 2018-08-30
\* URL generated for a VizieR cone search now take into account the option 'limit', as to limit the size of the retrieved VOTable
### 2018-06-11
\* Bug fix for rectangular selection of sources (aladin.on('select', ... )
### 2018-05-16
\* Add variable View.CALLBACKS\_THROTTLE\_TIME\_MS to control minimal time between two callbacks
### 2018-05-14
\* HTTPS support for Logger
### 2018-04-20
\* partially fix the all-sky view (the cells borders were visible) --> delta in method HpxImageSurvey.drawOneTile2
\* add option showAllskyRing
\* all-sky is shown at orders 3 and 4
### 2018-04
\* Add method zoomToFoV (zoom with animation)
\* doc : ajout Tour navigator library dans Plugins
### 2018-01-09
\* Add option simbadPointer
### 2018-01-08
\* Add option realFullscreen
### 2017-12-20
\* Catalog.onClick can now also be a function
### 2017-12-14
\* add function udpateShape for Catalog and ProgressiveCatalog object
\* ajout shape 'circle' pour les catalogues
\* bug fix: les cats progressifs ne s'affichaient pas quand on était zoomé et qu'on ne bougeait pas
### 2017-12-13
\* support Circle when generating footprints from STC-S descriptions
### 2017-11-30
\* improve positionChanged listener: no more called when clicking on an object
\* improve object shown when clicking ; it's really the closest one now
### 2017-11-24
\* add dragging attribute to positionChanged listener callback param
### 2017-10-09
\* add listener for 'mouseMove' event
### 2017-09-28
\* MOC display is way faster when panning
\* Sesame bug fix when used in a local file web page
### 2017-09-27
\* bug fix : MOC display with norder>9 (thanks to Raffaele D'Abrusco)
\* improve MOC display speed
### 2017-09-21
\* add listener for 'click' event
\* dimensions can be specified for getViewDataURL method
### 2017-09-08
\* gotoObject: can now take a success callback function
\* improve AITOFF display
### 2017-09-07
\* improvement: MOCs, catalogs and overlays have now different logos in the "stack"
### 2017-09-06
\* fix: export PNG was not working any longer in latest version of Chrome, as top frame navigation to data URL was no longer allowed
### 2017-08-28
\* add J2000d option for frame selection
### 2017-08-25
\* all graphical overlays (footprints, MOCs) in addition to catalogs are now visible and can be shown/hidden from the control panel
\* add skyFraction method to MOC class
\* fix: when going full screen, background is now all white (no more HTML elements visible in the background)
\* style: layer labels in Overlay layers panel are rounded at both ends
### 2017-08-24
\* add adaptativeDisplay option for MOCs
\* try first to load MOC through given URL, and only if it fails, try through proxy (allows to load local/not publicly accessible MOCs)
### July 2017
\* bug fix MOC
\* add method adjustFovForObject
\* add listeners on positionChanged zoomChanged
\* fix pour Andre Moitinho pour que Sesame fonctionne en HTTPS
### February 2017
\* shape parameter when creating a catalogue can now be a custom draw function
\* bug fix, when superimposing a HiPS over a HiPS with a different coordinate frame
### January 2017
\* added method to query SkyBot: A.catalogFromSkyBot
### September 2016
\* support of HiPS catalog (new format)
### June 2016
\* fix astrometry offset by subdividing HEALPix cells too distorted
\* new method A.MOCFromJSON to create a MOC from the JSON serialization
### March 2016
\* added raField and decField options when creating catalogue
### December 2015
\* added cubehelix color map
\* added option in A.catalogFromURL to bypass proxy
\* access to Simbad and VizieR data (catalogFromVizieR and catalogFromSimbad) are now done directly, without the proxy
### Novembre 2015
\* ajout méthodes getShareURL et getEmbedCode
### Octobre 2015
\* ajout méthodes accès facile à Simbad, NED et VizieR
\* ajout onClick comme option de Catalog: 'showTable' ou 'showPopup'
\* nouvelle version de jquery mousewheel (ça déconnait un peu sous Mac avec la précedente)
### Décembre 2014
\* ajout displayLabel pour afficher un label d'un overlay Catalog
\* ajout option lineWidth pour objet A.graphicOverlay
\* bug fix : la liste déroulante est mise à jour correctement quand on change de frame programmatiquement
### Novembre 2014
\* ajout nouvelles formes pour les sources
### 23 octobre 2014
\* bug fix méthode on('objectClicked') était appelée de manière intempestive
quand la souris quittait le canvas
### 21 octobre 2014
\* ajout option shape (plus ou square) pour les catalogues
### 20 octobre 2014
\* amélioration on objectClicked et objectHivered. On envoie une valeur nulle pour signifier qu'on quitte l'objet
\* ajout méthode pour dessiner un cercle (A.circle)
### 16 septembre 2014
\* bug fix pour nouvelle version de Firefox. Aladin lite freezait. On ne crée plus les textures individuelles pour le allsky
### 24 avril 2014
New in the API:
\* getSize
\* getFov
\* world2pix
\* pix2world
\* getFovCorners
### Novembre 2013
\* ajout catalogues progressifs
\* ajout option pour fullScreen mode au démarrage
\* ajout méthode setFOVRange
\* polyfill pour Function.prototype.bind (pour Firefox < 4)
### Septembre 2013
\* color maps
### Août 2013
\* ajout page exemple full-screen.html
\* ajout bouton maximize in fullscreen
\* CSS dans fichier séparé
\* image réticule "cachée"
\* options pour personnaliser le réticule
\* revamped UI for layers
\* export PNG (nécessite support CORS)
### Juillet 2013
\* ajout boutons zoom
\* ajout sélection d'objets
### Fin 2013
\* ajout catalogue progressif
\* ajout on select, objectClicked, objectHovered
## Contributors
Aladin Lite is made possible thanks to those people:
\* [@alexgoff][alexgoff]
\* [@bmatthieu3][bmatthieu3]
\* [@cquiroz][cquiroz]
\* [@imbasimba][imbasimba]
\* [@ManonMarchand][ManonMarchand]
\* [@pcuste1][pcuste1]
\* [@pmatsson][pmatsson]
\* [@simontorres][simontorres]
\* [@szpetny][szpetny]
\* [@tboch][tboch]
\* [@tomdonaldson][tomdonaldson]
\* [@Xen0Xys][Xen0Xys]
[alexgoff]: https://github.com/alexgoff
[bmatthieu3]: https://github.com/bmatthieu3
[cquiroz]: https://github.com/cquiroz
[imbasimba]: https://github.com/imbasimba
[ManonMarchand]: https://github.com/ManonMarchand
[pcuste1]: https://github.com/pcuste1
[pmatsson]: https://github.com/pmatsson
[simontorres]: https://github.com/simontorres
[szpetny]: https://github.com/szpetny
[tboch]: https://github.com/tboch
[tomdonaldson]: https://github.com/tomdonaldson
[Xen0Xys]: https://github.com/Xen0Xys

## Links found on page


