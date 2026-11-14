---
source: https://raw.githubusercontent.com/ericmandel/js9/master/help/changelog.html
fetched: 2026-11-14
status: 200
---

JS9 ChangeLog

![js9](../images/js9logo.png)

### JS9 ChangeLog

### Security updates, etc.

* security/archive release v3.9 20241213
* fix bug in exec validity check in js9 helper 20241213
* add additional exec validity check to js9 helper 20241213
* restrict wrapper script names to use alphanumerics, underscore 20241213
* update emscripten to v3.1.72 20241123
* update emscripten to v3.1.59 20240519
* update socket.io to v4.7.5 20240519
* update npm module uuid to v1.2.8 20240519
* update npm module minimist to v9.0.1 20240519
* update emscripten to v3.1.40 20230531
* update socket.io to v4.6.2 to close security vulnerability 20230531
* update emscripten to v3.1.27 20221204
* update socket.io to v4.5.4 to close security vulnerability 20221203
* update npm modules uuid, minimist 20221203
* js9Electron.js: hack around breaking changes in v20 20221203

### Public Release 3.8 (June 21, 2022)

* fix bug preventing flip, rotate, rot90 from working in Load() opts
* update emscripten to v3.1.13
* update socket.io to v4.5.1
* update astroem/cfitsio library to v4.1.0

### Public Release 3.7 (May 16, 2022)

* add color change option to shape layers plugin
* ?renamedisplay=[old:]new will rename a display when loading the web page
* add experimental support for getting remote FITS URLs via CGI-based proxy
* add cgi proxy support to 'load remote ...' dialog box
* drag/drop url will try cgi proxy if proxy server is not available
* js9.js: private sockopts to JS9.socketioOpts to support user configuration
* js9Helper: helperOpts to socketioOpts, use Object.assign to merge obj prefs
* make cubecol's id more akin to a filename (i.e., without parens)
* remove gz:: and bz:: from saved virtual filename
* evcube: generated cube file cannot be a gzip'ed file (re: cfitsio)
* when saving a section, use the real section instead of recalculating it
* fix bug changing position of a selected region after pan/zoom/flip
* fix regions bug where stack order (send to back) was reset after pan/zoom
* fix bug changing position of a selected region after pan/zoom/flip
* fix bugs in handling text children of grouped regions
* fix bug when saving one slice of a cube, naxis was not always set to 2
* astroem: rearrange a few source files
* add Quit() public access routine (Desktop app only)
* es6: use for( key of Object.keys(opts) ){ ... where possible
* es6: change a few functions to arrow functions
* update astroem/post.js to es6 to match emscripten v3.1.x
* update emscripten to v3.1.10
* update socket.io to v4.5.0
* update fabric.js to v5.2.1

### Patch Release 3.6.2 (January 3, 2022)

* add experimental support for converting event tables to 3D cubes
* add Counts in Each Cube Slice analysis task for files with NAXIS == 3
* optimize psList search for js9 helper
* add UI to change val/pos display color
* region editor: fix annulus edit (width, dashes not always processed)
* improve smoke tests
* update emscripten to v3.0.0
* update socket.io to v4.4.0
* update fabric.js to v4.6.0
* update open to v8.4.0

### Patch Release 3.6.1 (August 16, 2021)

* fix various problems with placement of panner rectangle
* edit annuli: don't multiply by scale factor when generating circles
* update astroem/cfitsio library to v4.0.0

### Public Release 3.6 (July 30, 2021)

* globalOpts.arrowIncrement: parameterize increment used by arrow keys
* selectShapes: if selecting a single shape, don't make a group selection
* add support for fabricOpts in js9prefs.js
* fix display of rotated non-square image in a non-square display
* fix bug that allowed arrow keys to move locked regions
* fix regression when adding/removing polygon points
* improve support for proxying js9 helper through a web server
* change the size of annulus region annuli graphically (meta-click to edit)
* change annulus defaults from 2 rings (0->15,15->30) to 1 ring (15->30)
* globalOpts.editRegions controls GUI region editing (def: true)
* fix magnifier jitter when moving a region with the arrow keys
* changeShapes: fix v3.4 regression that sometimes changed annuli incorrectly
* rearrange npm modules by uninstalling and installing socket.io
* clean up emscripten init in preparation for worker-based experiments
* update open to v8.2.1
* update fabric.js to v4.5.1
* update socket.io to v4.1.2
* update emscripten to v2.0.26

### Public Release 3.5 (June 1, 2021)

* remove the long-deprecated fits2png code
* fix bug in js9helper sometimes preventing fits2fits size check
* add support for displaying the actual png/jpeg image ("overlay" param)
* add overlay parameter to preferences plugin
* add reset to image filter plugin (overlays can't reset via contrast/bias)
* optimize static colormap cell lookup using binary search
* fix bug in JS9.eventToCharStr assigning 46 to delete instead of a dot
* js9prefs.js: add support for a config object to allow merging obj prefs
* update emscripten to v2.0.23

### Public Release 3.4 (May 5, 2021)

* maintain selection when switching between images, panning/zooming images
* ensure infobox displays correctly formatted val string
* add support for bitpix == 64 FITS data
* reg2wcsstr should not perform size calculation, use "cdelt" instead
* changing a region now shows immediately in the magnifier
* push unchangeable regions to back of fabric stack
* add 'locked' as opposite alias to 'changeable' for locking regions
* add support for 'locked' in region editor
* add support for binning tables on alt columns
* make mouseTouchZoom global instead of tied to a display
* turn off clickToFocus by default, way too many clicks (e.g. using menus)
* GetImage: don't throw if named image not available (return null instead)
* changing a region now shows immediately in the magnifier
* region editor now permits parent to change child's text
* changeShapes syncs child text color to main color (via regSyncTextColor)
* getShapes: now returns shapes in order in which they were loaded
* loadproxy: add support for ms-dos gzip files
* handle Infinity when getting scale min,max
* js9helper: change html error message to avoid 'Invalid character' error
* parameterize direction of mouse wheel zoom
* add skip factor to wheel zoom to avoid pileup
* globalOpts.mousetouchLimit limits zoom-out to size of image (def: true)
* don't display regions when GUI zooming an image with many (>500) regions
* don't display regions when GUI panning an image with many (>500) regions
* redesign region multi-selection dialog box to support groups
* add JS9.GroupRegions() and JS9.UngroupRegions() public routines
* add JS9.GroupShapes() and JS9.UngroupShapes() public routines
* add JS9.ListGroups() public routine
* add JS9.UnselectRegions() and JS9.UnselectShapes() public routines
* extend shape (region) selections to support boolean expressions (&&,||,!)
* add "onarrowkey" event for plugins, enable its use with pixel table plugin
* prefs: only save schema props (e.g. not all globalOpts when saving globals)
* fix regression in js9helper limiting size of file transfer
* remove support for fabric.js v1, it's ancient and incompatible with groups
* add deepscan.io checks when pushing to repository
* update eslint to 7.21.0 and make it happy
* update socket.io 3.1.2, then 4.0.1, remove 2.4.1 (now supported by v3+)
* update npm dependencies: uuid, rimraf, open, ps-node, table-parser
* update emscripten to v2.0.18

### Patch Release 3.3.1 (December 15, 2020)

* fix old bug appending "//" to helperProtocol, even if present (breaks socket.io when saving prefs)
* add regMenuCreate property to prefs plugin, remove useless regConfigSize

### Public Release 3.3 (December 14, 2020)

* listRegions: add format='regions' to parallel saveRegions output
* regions config: change color, width, pattern as colorpicker, menus change
* regions: fix regression when panning a grouped polygon or line
* js9Helper: fix regression in uploading FITS files
* fix bug to re-establish focus on js9 display after clipboard copy
* js9worker: worker socketio connection can now be restarted automatically
* update emscripten to v2.0.10
* add support for socket.io v3.0.3, while maintaining support for v2
* update fabric.js to v4.2.0

### Public Release 3.2 (November 6, 2020, a day of hope)

* add js9 shell scripting and desktop hostfs smoke tests
* add checks on filename and id to guard against xss attack
* add js9msg script to send messages using wget or curl (node not required)
* js9 script will now use faster js9msg script, if appropriate
* make JS9's returned data consistent between js9Msg.js, js9Helper.js httpd
* allow --with-cfitsio (without a dir arg) if lib is in a system dir
* desktop: add dialog box for exported script
* desktop: in script, look for webpage in current dir, then in install dir
* desktop: pass resize info if specified width or height is <= 0
* desktop: save cmdline opts on close (use same width, height next time)
* fix problems passing very large FITS headers (> approx. 1Mb) to initwcs()
* fix regression in desktop when using default web page
* fix regression in mouseup cb: updateShapes mode is "update", not "mouseup"
* various changes to generate Linux desktop app as well as macOS app
* js9Electron.js: add support for js9Electron.json file
* add support for editing cmd line opts in preferences plugin
* refactor desktop app to support editing cmd line opts
* modify js/FileSaver.js so that Jupyter notebooks put saveAs() on window
* update FileSaver.js to 2.0.4
* update emscripten to 2.0.5

### Public Release 3.1 (September 8, 2020)

* regions menu: list, remove act on selected or all regions
* edit menu: edit, copy act on selected or all regions
* add GUI inputs to configure style (color, strokewidth, stroke pattern)
* add selection criteria input to multi-selection dialog
* add SelectShapes() and SelectRegions() public routines
* console plugin can now execute public routines
* add ability to turn off auto-create of regions from the Regions menu
* 'a' key creates a region using the last one selected from Regions menu
* set globalOpts.regionsToClipboard to false (breaks copy selected support)
* display (screen) coords can be specified prefixing 'd' to x, y
* display coords can be preserved by specifying preservedcoords property
* view menu option to show display coords in val/pos string in image sys
* add JS9.DisplayNextImage() public access routine
* add 'sticky' property to regions (no change on pan, zoom, rotate, flip)
* refactor dataminmax, mkColorData to avoid Chrome multi-sec delays in for loops
* add support for rotating to North Is Up in current wcssys in SetRotate("northisup")
* add north is up rotation to Zoom menu and zoomcontrols dialog
* rotate/flip panner image as displayed image rotates/flips
* N/E marker now tracks current wcssys, not file's wcssys
* JS9.SetFlip(), JS9.SetRot90() use transform instead of changing image data
* add JS9.SetRotation(), JS9.GetRotation() to rotate image by arbitrary angle
* add JS9.ChangeRegionTags() public routine to add/remove region tags
* reorganize github site (new build directory, src in src, demos in demos)
* make install does not load demos, use make install-demos explicitly
* remove deprecated fitsy code from top level
* add JS9.ListRegions(), JS9.EditRegions() public routines
* regions menu: options to save regions using different wcs, also save csv
* separate: add ability to use a CSS Grid instead of light windows
* sync: add GUI for plugin and change menu GUI to match
* desktop: add searchbar to analysis light windows (ctl-f or cmd-f)
* inline voyager images (remove dax versions from js9inline.js)
* JS9Titlebar plugin adds image id to title (uses globalOpts.updateTitlebar)
* add onregionsmove callback to Magnifier plugin (if intensivePlugins)
* add CopyShapes() to copy shape layers to another image (cf CopyRegions)
* add CopyParams() routine to copy params from one image to another
* add ColorControls plugin to color menu
* rgb mode is now associated with each display separately (not global)
* move rgb info when moving images between displays
* resort preloaded files into their original order
* update node minimist package to avoid prototype pollution bug
* don't use centered scaling for line and box regions
* add length/angle options to line configuration dialog box
* add statusbar plugin
* globalOpts.menuPosition to set menu position (def: below the menu button)
* add sum/avg option to binning plugin
* add support for fractional binning
* add GetOpacity(), SetOpacity()
* add support for opacity floor: an opacity assigned if pixval <= floorval
* extend opacity in menu to include floor opacity support
* sync images: sync all images to facilitate blinking
* sync images: add syncwcs option to force sync using image coords
* desktop: options can now be passed via --switches (e.g., --scale log)
* Load: add ra,dec, px,py, wcs properties to support panning
* Load: regions property can load a region file or add a region
* syncImages: add rot90, flip, and sync blended images
* CloseDisplay now takes an optional regexp of images to close
* add source, destination in/out/over/atop methods to blend plugin
* static colormaps: specify color/opacity and pixel range
* expand MaskImage to support "overlay" as well as "mask" of image data
* add MaskImage() routine to allow one image to mask another
* remove experimental LoadAuxFile() (too fragile, subsumed elsewhere)
* fix region parser to check for exclude regions
* fix bug when sortable GUI changed the image stack with multiple displays
* fix annulus radii text box in regions config
* update uuid and rimraf modules for js9Helper
* update jquery to v3.5.0
* update emscripten to v1.40.1
* update fabric.js to v3.6.3 and enable strokeUniform
* update cfitsio to v3.48 (via astroem repository)
* update ResizeSensor to v1.2.2

### Public Release 3.0 (January 6, 2020)

* improve menu placement for Jupyter support
* replace image filter menu with plugin that supports parameter adjustments
* just redisplay already-loaded slices
* added PanZoom controls to Zoom menu, containing "pan to" support
* wcs menu: don't show wcs options if image has no wcs
* add Google's new turbo colormap
* add analysis plot configuration dialog box to set data range and scale
* improve panner to show display area (not image area)
* infobox: fix bug displaying image coords instead of phys if sys was image
* webworker init: avoid CORS problems when webworker is on a remote location
* add array-based x,y flip and +/- 90 degree rotation to the Zoom menu
* add JS9.SetRot90() and JS9.SetFlip() public access routines
* improve LTM/LTV support, various bug fixes
* avoid weakness in wcslib causing the wrong header length to be used
* fix error handling when called from external message
* update emscripten to v1.39.3 (required several changes to montage)
* upgrade code to use ES6

### Public Release 2.5 (August 30, 2019)

* re-displaying an image now calls the onload callback
* JS9.BlendDisplay('reset') unsets blended images
* JS9.DisplayExtension('all') loads all image extensions
* JS9.ReprojectData('all') uses the current image to reproject others
* JS9.Load('foo.fits', {allext: true}) loads foo.fits, then all extensions
* add 'Display all images' button to Extensions plugin
* add support for loading all images in a multi-extension FITS file at once
* fix typo that made incorrect sections of non-rectangular images at zoom < 1
* fix bug when zooming image with a selected region
* fix bug when loading multiple annuli at once
* fix regression in DisplaySection: new ext was not added to FITS filename

### Public Release 2.4 (July 15, 2019)

* fix double tap to close capability on iPhones
* fix internal regcnts tasks using annuli on iOS devices and re-enable them
* wcs grid: fix high limit display coordinates
* analysis menu: only display 3d analysis menu options for 3d images
* refactor LoadWindow so load waits for the lightwin to be fully created
* desktop app: support merging analysis tasks and loading foreign web pages
* add JS9.GetAnalysis() to return analysis task definitions
* add missing routine in internal CountsInRegions() and RadialProfile()
* add support for "All" selection of regions to include text children
* GetRegions: return text child region id
* desktop app: enabling node mounts local file system for direct FITS access
* desktop app: add security checks
* fix overly-aggressive .gitignore and add missing files
* fix typo that broke createMosaic("all")
* fix bugs in imexam plugins using a rotated line to define the image section
* fix spinner when using open local file dialog
* update emscripten to v1.38.37
* update contextMenu to v2.8.0

### Public Release 2.3 (May 1, 2019)

* support for Mac app, a bit of Windows app: see github/ericmandel/js9app
* Electron desktop app: use internal colorpicker if Electron version >= 5
* add logo support
* add AlignPanZoom() public routine
* add --cmds [cmds] and --cmdfile [file] switches to js9Electron.js
* add --node switch to js9Electron.js, allowing nodeIntegration
* add JS9.globalOpts.onpreload property
* fix wcs alignment of blended images during pan and zoom operations
* fix mosaic code, which needed area mosaic file after all
* redesign Menubar to use more submenus, especially File menu
* fix bug in the supermenu sometimes not displaying the File sub-menus
* work around invalidation of emscripten heap pointers when memory increases
* add ability to change child text options via the parent shape
* add ability to push selected region to bottom of overlapping stack ('d')
* add ability to select all regions ('S' and Regions menu option)
* add SaveDir public routine (desktop app only) to set the save directory
* SavePNG,SaveJPEG: add option to save image RGB pixels instead of display
* SavePNG,SaveJPEG: add option to skip saving the layers (e.g. regions)
* shape layers (incl. regions) can now be exported in SVG format
* closing a light window that displays images now supports: close, move, ask
* add support for unconstrained panning
* dynamically select a JS9 display (supports one plugin for many displays)
* SaveColormap: allow multiple colormaps to be save at once
* add ability to change color, width, dash lines, tags of selected regions
* fix bug in "north is up" rotation: take CDELT values into account
* add direction vector to panner
* display regions in lightwin instead of on display or in infobox
* add region copyToClipboard capability (so 'p' always pastes last region)
* add ability to specify display opts in a FITS header (IMOPTS param)
* add ability to specify colormaps in a FITS header (IMCMAP param)
* add ability to create image cutouts of selected region(s)
* add ability to rename a JS9 display via JS9.RenameDisplay() api call
* ensure saved order of images after session load
* add --title and --renameid options to desktop app to rename display ids
* parameterize initial blending params
* Preload() loads .cmap files as colormaps
* colormaps: specify m colorwheel slices, from which n colormaps are assigned
* add ability to specify {display: id} param to external api calls
* add ability to unremove previously removed regions
* add ability to select regions based on the file from which they were loaded
* calling LoadRegions() twice removes previous regions loaded from the file
* add globalOpts.quietReturn to silence 'OK' messages
* Desktop (Electron.js) version: add --savedir option to skip save dialog
* JS9.Load(): globalOpts.reloadRefresh property to control reloading an image
* add 'revert' option to wcs reproject submenu
* wcs menu: each wcs system has own current units (based on initial defaults)
* fix region parser to see 'linear' as wcs, not a 'line' region
* cmaps: allow color choice via text input in fallback colorpicker
* fix memory leaks in reproject code
* LoadColormap: support file containing array of colormaps
* Infobox: for long filenames, click to see right hand side
* addColormaps now replaces a cmap with same name
* add 3D plot capabilities for data cubes in Analysis menu
* many improvements to user-defined menus
* turn on wasm in js9 Electron.js Desktop app
* menu: allow load/save of cmaps without a loaded image
* when blending, only sync zoom/pan reprojected images that are wcs aligned
* reproject: use float32 instead of float64 if datatype allows (less memory)
* reproject: correctly align images when wcs ref image is panned or zoomed
* reproject: fix memory leaks, always go back to original image
* js9 helper: increase ping timeout to avoid Chrome disconnects
* improve header generation and FITS card handling
* allow DisplaySection() to display the new section in a different display
* add colormaps plugin to create (complementary) colormaps
* fine-tune positioning: arrow keys display small crosshair cursor
* fine-tune positioning: arrow keys change magnifier display center
* regions menu: listonchange can act on "selected" (default) or "all" regions
* preferences plugin: image parameter for "all" or "selected" listonchange
* Meta (or Ctrl) now used for keyboard shortcuts displaying a light window
* edit, region menus: add option to display region configuration window
* add 'M-e' keyboard shortcut to display region configuration window
* add 'M-o' keyboard shortcut to open a local file
* add 'p' keyboard shortcut to paste regions at current mouse position
* (joining 'P' keyboard shortcut to paste regions at their own position)
* add 's' keyboard shortcut to select region that contains the mouse
* fix bug when saving/copying regions inside a rotated group
* Meta key during mouse move no longer updates internal image position
* update emscripten to v1.38.28
* update fabric.js to v2.7.0

### Public Release 2.2 (October 9, 2018)

* add sync plugin: synchronize operations between two or more images
* add JS9.SyncImages() and JS9.UnsyncImages() public access routines
* SetParam(): setting a core param calls the core function
* add support for disabling colormap, pan, regions, scale, wcs, or zoom for a given image
* add Scale Clipping Limits plugin (with pixel distribution plot)
* add support for setting up a proxy from Apache to the Node.js helper
* add Separate/Gather Images plugin
* desktop app: add support for printing entire window
* desktop app: add support for saving entire window to a pdf file
* add support for loading all slices of a data cube separately into JS9
* add support for user-defined menus in the Menubar
* add support for averaging pixels when binning (def: summing)
* add support for Mac-style menubars
* add Edit menu to Menubar (copy/paste regions, positions, values)
* add JS9.DisplayCoordGrid() and associated client-side task to Analysis menu
* add JS9.CountsInRegions() and associated client-side task to Analysis menu
* add JS9.RadialProfile(), and associated client-side task to Analysis menu
* reproject will try to bin large images to avoid memory limits
* add support for wcs-based cross-hair tracking of images
* add support for displaying mosaic images
* add CreateMosaic() public routine
* remove .fz suffix in various places where it breaks things
* fix bug where binning an image was not updating the CD matrix
* update emscripten to v1.38.5
* update socket.io to v2.1.1

### Public Release 2.1 (May 10, 2018)

* allow JS9.SetPan() to accept a single object with x and y properties
* allow JS9.WCSToPix() to accept a single object with ra and dec properties
* allow JS9.PixToWCS() to accept a single object with x and y properties
* add support for Toolbar plugin
* add JS9.SetParam() and JS9.GetParam() public routines
* add JS9.SetToolbar() and JS9.GetToolbar() public routines
* add JS9.SeparateDisplay() public routine to separate images in a display
* add JS9.GatherDisplay() public routine to gather images into a display
* add JS9.LoadColormap() public routine
* add JS9.LightWindow() public routine
* JS9.GetImageData() now returns display size, bin factor
* JS9.RunAnalysis() return types now include "regions" and "catalog"
* include comments and history in display of FITS header
* iOS 11.2.2,5 disable wasm: github.com/kripken/emscripten/issues/6042
* add refresh property to JS9.Load() to re-retrieve data
* add support for refreshing a file/url in JS9.RefreshImage()
* add support for displaying full image to JS9.DisplaySection()
* add 'f' (full) and 'r' (refresh) keyboard actions
* change 'r' (raise region layer) to '^' in keyboard actions
* add refresh and section commands to Console plugin (and js9 script)
* binning plugin: add button to load full image
* sessions: save/re-run dataLayer routines (e.g. reproject, rotate)
* sessions: save/restore blend mode
* sessions: save/restore wcsim from reprojection
* sessions: save/restore display parameters
* SaveSession saves either current image or all images
* ensure correct extension for Save{Session,PNG,JPEG}
* image blending: update GUI when changes are made via API
* image blending: support sizing of static div
* fix imexam routines needing integer section limits
* update emscripten to v1.37.28
* update fabric.js to v1.7.22
* update contextMenu to v2.6.3

### Minor Patch Release 2.0.2 (December 15, 2017)

* add zscale, zmax to SetScale()
* improve display-based routines (separate, gather, resize, center, select)
* improve alignment of differently sized images
* allow zoom during image blending
* add menu support for closing all images
* add support for selecting a target display in a supermenu
* add support for dispersing images from one display into new displays
* add support for gathering images from multiple displays into one
* add support for new image inheriting params from current image
* fix allinone (dont use wasm)
* fix bug loading wasm file in LoadWindow('new')

### Minor Patch Release 2.0.1 (September 29, 2017)

* move helper log file outside www directory
* improve fetchURL() error messages
* fix bug in load catalog menu option
* allow json opts in Load\* family of routines
* fix bug in JS9.Preload by saving a copy of opts

### Public Release 2.0 (September 27, 2017)

* add support for emscripten-based WebAssembly
* add support for HPX projection
* add wcs selection menu to regions config dialog
* aesthetic improvements to regions config dialog
* fix race condition in Electron startup if not codesigned
* fix binning when manually specifying parent file
* fix wcs system display in infobox
* fix bug in js9Helper.js where localhost was not upgrading to use ws
* update emscripten to v1.37.20
* update fabric.js to v1.7.19
* update socket.io to v2.0.3
* update jquery to v3.2.1
* update jquery-ui to v1.12.1

### Public Release 1.12 (July 25, 2017)

* refactor astroem to use astroem repository of emscripten library byte-code
* add DisplaySection() public routine
* add ability to extract a section from images (as well as tables)
* add fits2fits configuration params for large files support
* add large file support in which large files can be handled externally
* allow infoBox to be configured via JS9.globalOpts.infoBox and preferences
* add wcs center and wcs fov display to infoBox
* add js9.app Mac desktops to run js9 script (drag/drop images onto it, etc.)
* add support for specifying URLs on js9 command line (uses proxy load)
* JS9.Preload() will now call JS9.ProxyLoad(), if required
* proxy load now turned on by default (needed for Desktop use)
* add support for drag/drop URLs onto JS9 display (uses proxy load)
* add support for uploading FITS files to a remove server
* add support for displaying bzip2 files
* add support for drag drop of region, catalogs, sessions (by file extension)
* add text, fonts, stroke options to region configuration dialog box
* add support for specifying a text region as a child of a region
* add js9-to-ds9 region conversion to js9 script (-r)
* add support for importing ds9 regions, including properties in comments
* sort overlapping regions so smallest is on top
* fix memory leaks in mef support
* add Divs plugin to show/hide in-page JS9 plugin divs
* allow shape size controls to match shape color at border, corner, or both
* use file extensions when opening local files (fits, regions, catalogs, etc)
* add keyboard action to move selected region in back of other shapes (not a default)
* JS9.RegisterPlugins() will instantiate plugins if scripts load asynchronously
* add JS9.InstantiatePlugins() public routine
* deprecate auto load of js9Prefs.son (load js9prefs.js explicitly instead)
* update emscripten to v1.37.9
* update socket.io to v1.7.3 (big change in module directory structure)

### Public Release 1.11 (January 9, 2017)

* add support for displaying HEALPix files
* add initial support for memory management of internal FITS files
* add menu support for clearing FITS files from internal memory
* add support for running JS9 on the Desktop using Electron.js
* integrate Desktop Electron support into into js9 script
* add ability to load local catalogs and save catalogs to disk
* add JS9.LoadCatalog() and JS9.SaveCatalog() public routines
* add Shape Layer plugin to turn on/off layers and set the active layer
* remove list of shape layers from View menu in favor of Shape Layer plugin
* add JS9.ActiveShapeLayer() public routine
* improve onimagedisplay processing for mef, cube, imarith plugins
* fix bug in cube plugin blink support
* update fabric.js to v1.6.6
* update socket.io to v1.5.1
* update closure-compiler to v20160911

### Public Release 1.10 (October 11, 2016)

* add support for full-display mode
* add support for keyboard actions and shortcuts
* add JS9.SetRGBMode(), JS9.GetRGBMode() public routines
* unclutter the position/value display
* dont update value/position if "special key" is pressed
* buttons and menu/titlebars are now beautiful and Mac-like
* buttons can be beautiful and flat (change via class specification)
* add support for copying regions to another image (JS9.CopyRegions())
* add initial support for plotly plotting library
* improvements to energyplot, evfilter, binning plugins
* add support for alternate WCS (including JS9.GetWCS, JS9.SetWCS routines)
* add JS9.LookupImage() public routine
* generalize and extend plugin callback capability
* extend range of FITS files that can be WCS-projected using Montage
* add support in the File menu for saving and loading sessions
* add JS9.LoadSession() and JS9.SaveSession() public routines
* update imexam,fitsy, archive plugins
* update fabric.js to v1.6.3
* update cfitsio to v3.39
* update socket.io to v1.4.5

### Public Release 1.9 (June 8, 2016)

* add standard RGB image processing functions to the Analysis menu
* add support for gesture-based zoom (scroll wheel and pinch)
* add MouseTouch plugin to change mouse/touch actions
* image id now contains extension name or number for FITS extensions
* add support for histogram equalization scaling
* add support in js9 script for starting up a browser/web page
* add support for displaying slices of a FITS data cube
* add support for image arithmetic (between 2 images or image & constant)
* add support moving images between JS9 displays
* add support for displaying HDUs in multi-extension FITS files
* add 'magma', 'inferno', 'plasma', 'viridis' colormaps from matplotlib
* deprecate the use of funtools when building JS9; please use cfitsio

### Public Release 1.8 (March 21, 2016)

* add image blending plugin to support blending operations between images
* add ability to blend images using W3C composite/blending modes
* add colorbar plugin to display colormap vs intensity information
* add blink plugin to blink images
* add line region (with support for multiple line segments)
* add raw data layers to allow manipulation of underlying raw data
* add JS9.FilterRGBImage() to support RGB image processing routines
* add JS9.GaussBlurData public routine to perform Gaussian blur on data layer
* add JS9.RawDataLayer() public routine for raw data layer manipulation
* add JS9.ShiftData() public routine to shift raw data in x and y
* add JS9.GetDisplayData(), returning data for all images in a given display
* add JS9.SaveJPEG() public routine to save image and overlays as JPEG
* add JS9.AddColormap() public routine to add a colormap to JS9
* add JS9.SaveColormap(), JS9.OpenColormapMenu() public routines
* JS9.SavePNG() public routine now saves image and graphical overlays
* add support for reprojecting images using Montage/mProjectPP
* add JS9.Reproject() public access routine
* change menu option Color->alpha (0 to 255) to Color->opacity (0.0 to 1.0)
* fix bug when interactively changing panner for non-square images
* fix bug in lut colormap, which truncated the first color
* refactor emscripten astroem package into sub-packages
* update emscripten to v1.35.0

### Public Release 1.7 (January 12, 2016)

* add Jupyter/IPython support for iframes
* add keyboard focus support for Jupyter/IPython
* add timeouts to avoid back-end connect() hangs
* add support for using rgb file as the display over a data file
* default helper is "none" (for Jupyter, where js9Prefs.json is not loaded)
* add lower right handle to change width and height of display
* add View menu option to change width and height of display
* add JS9.ResizeDisplay() to change the size of a JS9 display element
* add JS9.DisplayPlugin() public routine for custom menus
* add JS9.GetFITSHeader() (as a string) public routine for custom menus
* add resize handle to display (lower right corner)
* add View menu option to change the display width and height
* add support for handling group events in shape layers (i.e. catalogs)
* add support for handling mouse events in shape layers (i.e. catalogs)
* add support for tooltips to shape layers (i.e. catalogs)
* add return values to saveFITS() and savePNG()
* add spinner while waiting
* fix OpenFileMenu() and OpenRegionMenu() when using multiple displays
* fix text region printing
* fix bug in panner box when panner image does not fill panner width
* fix region configure to "delete" only itself (not all regions)
* fix one pixel bug in WCS region conversion
* update fabric.js to v1.5.0
* update socket.io to v1.3.7
* updated jquery to v1.11.3

### Public Release 1.6 (November 7, 2015)

* add support for extracting image/table sections from "parent" files
* add JS9.LoadProxy() public routine to load FITS URLs via proxy server
* add support for loading Dropbox (and other CORS enabled) shared links
* add support for loading links by proxy through the back-end server
* add SetValPos and DisplayMessage public routines
* add options to create new JS9 windows from the file menu
* add experimental support for JS9 in an iframe, using postMessage
* remove starting "\_" from SUPERMENU id (not legal syntax)
* fix various iOS foibles (scrolling, double-click to close)
* fix memory leak in cfitsio RefreshImage() support
* fix bug in lut colormap limit check
* fix bug in JS9.RefreshImage() blob handler
* fix overflow bug in cfitsio bscale/bzero support
* fix bug in zscale by properly exposing emscripten methods
* update emscripten to 1.34.1
* update wcs library to 3.9.0

### Public Release 1.5 (July 9, 2015)

* add support for specifying regions using Funtools/DS9 syntax
* add support for loading Funtools/DS9 region files
* add support for running the Node.js helper using https protocol

### Public Release 1.4 (May 3, 2015)

* add Preferences plugin to set image and region user prefs
* add ability to save image to FITS and PNG files (limited Safari support)
* add ability to save regions to a text file
* fix bugs in Binning plugin (mainly for cfitsio, but some general bug fixes)

### Public Release 1.3 (March 30, 2015)

* add cfitsio library support to JS9 (emscripten compile to javascript)
* add data-width and data-height attributes to change the size of JS9 divs
* extend tpos and js9helper to use cfitsio (or funtools)
* update tpos js9Protocol to 1.1 to include header comments in the header
* default WCS is now determined in the browser, not by the back-end server
* ensure that section info is maintained during JS9.RefreshImage()
* prevent preload from happening more than once
* fix broken File->Open menu option
* update emscripten to v1.27, add new optimizations to astroem

### Public Release 1.2 (January 4, 2015)

* concurrent release of pyjs9 1.0 on github
* update socket.io to the Engine.IO-driven v1.x (specifically v1.2.1)
* add ability to reconnect to node.js server automatically if latter restarts
* add support for specifying a temp work dir for back-end analysis
* add http support to js9Helper.js so messages can be sent via GET, POST
* JS9.Load: accepts FITS files as blobs and base64-encoded strings
* JS9.RefreshImage: accepts blobs (FITS files), js arrays and typed arrays
* JS9.GetImageData(): returned data can be array or base64-encoded string
* fix bug in arguments to public api routines sent via external message
* fix bug in File List: clicking on same file multiple times now redisplays

### Public Release 1.1 (November 15, 2014)

* NB: api change: added errcode to argument list of RunAnalysis() callback
* new api: AddDivs() to add JS9 displays and/or plugins to the web page
* new api: Send() sends msgs programmatically (useful for 3rd party helpers)
* add support for super-menus that can control multiple JS9 displays
* add support for onload callback when displaying FITS files
* allow xcen, ycen (in image coords), zoom to be passed in obj to JS9.Load()
* re-factor js9Helper.js: each analysis task is its own top-level msg
* allow user-defined msgs to be added to analysis tasks more easily
* ensure correct region size during RefreshImage() and table binning
* add contour plugin to default plugins in js9plugins.js
* add checks for NaN values to imexam plugins
* fix imexam plugins bug when regions are rotated and resized
* fix bug in encircled energy preventing calculation for non-integer radii
* properly handle FITS TFORM cards without a repeat value (XMM data)
* resize regions properly when tables are binned by a block factor
* ensure that datamin and datmamax are updated when a binary table is binned
* dont send image notify events to back-end during contrast/bias changes

### Public Release 1.0 (September 30, 2014)

* NB: change to the Public API: id is no longer first argument. See API doc.
* infobox plugin upgraded to a tabular display
* node.js server sends unique pageid back to JS9
* JS9 menus now cover light windows (higher zindex)
* improved accuracy of polygon points for contours
* moving a polygon point now calls listRegion
* added missing commas in WCS display of polygon points
* corrected WCS for drag/drop of sections of FITS binary tables
* fixed incorrect region size when binning FITS binary tables
* fixed memory leak in astroem reg2wcs routine
* plugin divs can now set height and width using CSS
* added defensive code to remove bash functions from CGI and node calls
* updated fabric.js to 1.4.11

### Release 1-epsilon (July 28, 2014)

* JS9.Load() can now load FITS files directly (rather than converting to PNG)
* added support for FITS binary tables, including binning and filtering
* added support for gzip'ed FITS files
* added support for "physical" coordinates (i.e., tied to original data file)
* changed 2D graphics subsystem from Kinetic.js to fabric.js
* added generalized shape layer support for regions, catalogs, contours, etc.
* region context menu is now a light-weight web page with many new features
* added text and point regions
* position of a pixel is now in the center of the pixel
* accelerator key changed from shift key to meta key (command on Mac, control elsewhere)
* reduced number of js9 files to load in a web page
* redesigned and flattened returned region object
* redesigned public API
* changed Public routines JS9.Pix2WCS and JS9.WCS2Pix to be 1-indexed
* added ability to group and move regions
* box rotation is now around the center of the region
* all image coordinate are now 1-indexed throughout
* fixed bug where adding a polygon pt didn't show until region was selected
* changed polygon points to an array of objects {x, y} instead of just x, y
* fixed various layout bugs in plugins
* updated emscripten to latest version
* updated flot to latest version
* updated jquery to 1.11.1

### Beta Release 13 (April 6, 2014)

* added support for handling NaN values

### Beta Release 12 (March 10, 2014)

* added support for browser-based analysis via plugins (JS9.RegisterPlugin)
* converted Menubar, Info, Panner, Magnifier to plugins
* initial version of imexam plugin available (in plugins directory)
* initial version of archive/catalog server plugin available
* added support for zscale (IRAF min/max algorithm for scaling)
* added support for user scale limits
* regions can now be moved off the image
* shift key disables mouse plugin callbacks
* zooming a small image will use all of the available display canvas
* added support for sub-pixel zooming
* added ability to process all keys in keypress callback
* added arrow key support for moving regions
* added fractional pixel positions for zoomed images
* fixed bug which reset pan when changing colormaps on a zoomed image
* added strict mode
* update emscripten to 1.8.2

### Beta Release 11 (December 18, 2013)

* initial port to iPad
* removed notifyHelper message when mouse enters image window
* fixed tpos crash when converting really large images
* updated jquery.contextMenu.js

### Beta Release 10 (December 9, 2013)

* added support for RGB composite display
* added support for reading in auxiliary files via auxFiles preference
* added support for overlaying FITS image masks
* added support so that drag and drop files can be found by local analysis
* added analOpts.dataPath to specify where to look for drag and drop files
* box regions need to rotate around upper left point to ensure consistency
* changed name of fitshelper to js9helper
* changed JS9.submitAnalysis() to JS9.SubmitAnalysis()
* changed analOpts.datadir to analOpts.dataDir
* removed wcs event processing from node and CGI helper (use browser wcs)
* js9helper not run as a server from js9Helper.js any more (scales better)
* added ability to turn off redraw when creating a large number of regions
* fixed bug in panner display for non-square images
* added work-around for Google Chrome v31 bug (regions not drawn)

### Beta Release 9 (October 23, 2013)

* added support for client-based WCS using emscripten 1.5.6
* added drag and drop of FITS images (binary tables are coming)
* added support for region callbacks (executed when a region changes)
* added JS9.Regions() public routine to retrieve and modify selected regions
* added Close Image button to File menu
* reduced size of panner when created by View menu
* updated Kinetic.js to v4.7.2
* minor bug fixes (e.g., annuli strokeWidth not resizing properly)

### Beta Release 8 (September 23, 2013)

* fixed security in node.js support by requiring use of wrapper scripts
* added support for CGI-based back-end helpers
* implemented automatic discovery of analysis definitions
* added timer-based management of WCS update requests
* updated socket.io to 0.9.16
* changed routine name from JS9.preloadImages() back to JS9.Preload()!

### Beta Release 7 (August 19, 2013)

* fits2png: added support for "%cookie" in odir specification
* js9.js and js9Helper.js both now use js9Prefs.json for setting preferences
* fixed bug in display/manipulation of panner when image is zoomed
* added "none" as an analysis return type to support hidden analysis
* changed routine name JS9.Preload() to JS9.preloadImages()
* added clipping to region manipulation
* fixed region strokewidth problem when zooming image
* fixed magnifier and panner where multiple instances of js9 are present
* numerous changes to pass new JSLint rules
* updated jquery to 1.10.2
* updated jquery.flot to 0.8.2
* removed references to of jquery-ui in demo files (its not used)

### Beta Release 6 (July 22, 2013)

* added support for panner window, including ability to zoom the panner
* added support for magnifier window, including ability to change magnification
* implemented zoom menu (zoomIn, zoomOut, zoom1, zoom2, zoom4, zoom8)
* added support for all FITS data types (silrd) in js9.js and tpos.c
* png file now contains FITS header in json format
* NB: the format of the PNG representation file has changed substantially!
* raw arrays now implemented as a typed array, using DataView to unpack it
* updated Kinetic.js to v4.5.4 (multiple changes required to code)

### Beta Release 5 (May 20, 2013)

* added support for dynamic creation of js9 instances (new or light window)
* added support for pre-loading images into a js9 on page load
* added support for running analysis web page buttons, forms, etc.
* added support for printing the image
* added new demo pages
* changed js9msg script name to js9
* loading javascript files is "generic" (no version numbers in filenames)
* updated Kinetic.js to v4.5.1

### Beta Release 4 (April 26, 2013)

* added support for polygon regions
* added support for fixing (i.e. freezing) regions in place
* added support for container regions (constrain position of other regions)
* added support for shift key accelerator
* fixed multiple bugs in region listOnChange support
* updated Kinetic.js to v4.4.3

### Beta Release 3 (April 2, 2013)

* updated Kinetic.js to v4.4.0 to fix new chrome v26.0.1410.43 (whoah!)

### Beta Release 2 (April 1, 2013)

* added support for executing analysis from console window
* added support for messaging to js9 via Node-based js9Msg.js
* added ability to specify params to region creation
* added server mode and input from stdin to js9Msg.js

### Beta Release 1 (February 27, 2013)

* initial beta release with support for displaying FITS images, scaling,
  colormaps, external analysis, regions, wcs

## Links found on page


