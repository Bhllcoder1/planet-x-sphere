---
source: https://raw.githubusercontent.com/ericmandel/js9/master/help/user.html
fetched: 2026-11-14
status: 200
---

The JS9 Help Facility

![js9](../images/js9logo.png)

### JS9: astronomical image display everywhere

Eric Mandel, Alexey Vikhlinin
  
Center for Astrophysics | Harvard & Smithsonian
  
Cambridge, MA 02138

### Introduction to JS9

JS9 is the latest in the SAOimage line of astronomical image display
programs developed at
the [Center for Astrophysics |
Harvard & Smithsonian (CfA.)](https://www.cfa.harvard.edu/) Our previous effort,
[SAOimage DS9](http://ds9.si.edu), has been
the de facto standard desktop image display for more than 30
years. Now, with JS9, you can view and manipulate astronomical image
data in your browser as well as on the desktop.

Please choose from the following topics:

* [Getting Started with JS9](#start)
* [JS9 Menus](#menus)
* [JS9 Mouse Interaction](#mouse)
* [JS9 Regions](#regions)
* [Meta Key Accelerator](#meta)
* [Drag and Drop Images](#dragdrop)
* [Resizing the Display](#resize)

### Getting Started with JS9

JS9 provides astronomical image display capabilities both on the
desktop and in your browser. JS9 takes its name as well as its core
functionality from the de facto standard
[DS9](http://ds9.si.edu) image display
program for desktop use. JS9, on the other hand, can be run either on
the desktop or in a browser. It also can be used without any
installation at all by dragging/dropping a FITS file onto the
[JS9 website](https://js9.si.edu). In all
three cases, the JS9 display consists of one or more HTML components
that are added to a web page. At a minimum, the JS9 display will
contain an image display canvas. It usually also will display a
menubar containing several pull-down menus and a
colorbar. Traditionally, the menubar is placed on top of the image
canvas and the colorbar below, but web page designers (as well as
individual users) have complete control over component placement. JS9
also can display an info box, a command-line window, a pan window, a
zoom window, as well as other plugins. All of these plugin windows can
be brought up dynamically from the View menu.

Astronomical image data usually is offered on a JS9 web page as one or more
clickable URLs. When you click on a data URL, it is displayed on the JS9 image
canvas. Multiple images can be loaded into a single JS9 display. The **File**
menu allows you to switch between these images.

Once an image is loaded, you can move the mouse (or a single finger on
a touch screen) to display position and pixel value information.
Pressing the left mouse button and moving the mouse (or using two
fingers on a touch screen) will change the contrast/bias of the
displayed image, bringing image features into relief.

These mouse/touch actions are configurable, both by web page
developers and by users. See
the [Mouse Touch plugin](../plugins/help/mousetouch.html) for
more information.

Menu options allow you to change the scaling algorithm and/or color
map, add geometric regions of interest, change world coordinate system
(WCS) parameters, and run site-specific astronomical analysis tasks on
the original FITS data.

### JS9 Menus

The following menus are in the default JS9 menu bar. Of course, web
designers have control over which menus are displayed (or even whether
the menu bar itself is displayed.) Thus, not all of the menus listed below
will be found on all JS9-enabled web pages.

Some menu options have keystroke accelerators and these are shown on
the right-hand side of the menu option. Thus, for example, to open a
local file, you can select the **File:open...:local file** menu
option, or press the **Meta-o** key combination when the mouse is
inside the JS9 display.

Note that the default menubar has a style in which all of the
major menus are shown at the top-level of the menubar. This is
the **classic** style. JS9 also supports a **mac** style
menubar, in which the **File**, **Edit** and **View** menus
are placed on the left side of the menubar and the **Help** menu on the
right. The other main menus are displayed as submenus within
the **View** menu.

The default top-level JS9 menus are:

* **File:** The File menu displays the currently loaded images,
  either directly in the menu, or, if there "too many" images (as
  defined by the JS9.globalOpts.imagesFileSubmenu variable), using
  an **images** submenu. The displayed image is marked with a
  starburst. To display a different image, simply choose it from the
  menu. The File menu also contains the following submenus and options:

  + **open local...** bring up a file browser dialog box to choose a FITS,PNG, or JPEG file for display
  + **open remote ...** bring up a dialog box to load a remote URL either using a JS9 proxy server (if configured), the cgi proxy on js9.si.edu, or directly using a CORS-enabled server (if available)
  + **display ...**: components and sections:
    - **FITS header** display FITS header of the current image
    - **FITS HDUs** display a list of HDUs in a multi-extension FITS file
    - **refreshed image** an advanced option that will call the
      internal redisplay routine for the displayed image (useful, for
      example, if you are reprocessing the image on disk and want to view
      the new data)
    - **full image** an advanced option that tries to
      load and display the entire image (might cause the page to crash if
      the image is too large)
    - **selected cutouts** selected region(s) are used to define the center and size of new image section(s); note that image sections are always rectangles and region angles are ignored
    - **display pageid**, a unique ID for this page that can be used to communicate externally with a JS9 instance when multiple JS9 instances are running (js9 --pageid [pageid])
  + **move ...** move the current image to an existing displays or
    a new display. (The new display will either be a in a light window or
    a CSS grid, depending on how the web page is constructed.)
  + **separate ...** separate/gather two or more images
    - **separate these images** move each image in this display to a
      new display. (The new display will either be a in a light window or a
      CSS grid, depending on how the web page is constructed.)
    - **gather all images here** move all images from other displays to this display
  + **save ...**the currently displayed image data. You can save
    the currently loaded image (or the currently loaded image section, if
    an image section was extracted) in standard FITS image format. Or you
    can save only the currently displayed image section in any of the
    following formats:
    - **FITS** (standard astronomical image file, without 2D graphics)
    - **JPEG** (also includes 2D graphics, such as regions)
    - **PNG** (also includes 2D graphics, such as regions)
  + **close ...** one or more images (or internal image memory)
    - **this image** to clear the current image and release browser resources
    - **all images** to clear all images and release browser resources
    - **free image's memory** free up memory used to store the FITS file internally (which is needed for WCS reprojections, viewing FITS extensions and data cubes)
    - **proxy file** to clear a server proxy file and release browser resources
  + **catalog ...** load or save catalogs
    - **load ...** load a tab-delimited catalog file into the display
    - **save active** save the currently active catalog (Shape Layers plugin has more general support)
  + **mosaic ...** create a mosaic image using:
    - **images in the current file**
    - **images in this display**
  + **session ...** load or save sessions
    - **load ...** load a previously saved local session file into the display
    - **save ...** save information about the current image or all images loaded into this display: filename, scaling, colormap, contrast/bias, zoom, regions, catalogs, etc. are stored in a json file
  + **window ...** create a new JS9 display window:
    - **light window** create a light window containing a JS9 instance
    - **separate window** create a separate window containing a JS9 instance
  + **remove this display** close images and remove this display. This
    option is available for displays contained in light windows and for displays
    contained in JS9 Grid Containers (although the latter requires that at least
    one display to remain in a container.) The display is removed immediately
    and without a confirmation dialog box (unlike a light window being closed
    via its **close** button.)
  + **print ...** print the current image display window (including 2D graphics)
* **Edit:** allows you to copy and paste regions, positions,
  and pixel values to/from the clipboard:

  + **edit** if a single region is selected, display its edit window;
    if multiple regions or no regions are selected, display the multi-region window;
  + **copy** copy selected region(s) (or all regions, of none are
    selected) to the system clipboard, so that you can transfer to other
    JS9 displays or to programs outside of JS9
  + **paste to current pos** paste previously copied region(s) to
    the current mouse (or arrow key) position in a JS9 display. Usually
    you would use the keyboard shortcut (currently 'p') for this
    sort of pasting, but you also can use the meta key to freeze the mouse
    position and then use this menu option
  + **paste to original pos** paste previously copied region(s) to
    their original region position(s), usually in another JS9 display.
  + **undo remove** restore the last removed region (or set of removed regions, if more than one was removed in a single operation)
  + **copy wcs pos** copy the current WCS position to the system clipboard
  + **copy value/pos** copy the current pixel value and WCS position to the system clipboard
* **View:** displays a list of available plugin, including the following core options:

  + **Archive and Catalogs**: allows you to display image data retrieved from various archives and overlay catalog information.
  + **Bin/Filter/Section**: supports binning and column filtering on FITS binary tables.
  + **Blending**: combine selected images using a specified blend
    mode and optional opacity.
  + **Colormaps**: create compatible colormaps from a specified color
  + **Console**: will bring up a movable, light-weight
    console window into which JS9 commands can be entered.
  + **Contours**: generate contour maps
  + **Data Cube**: display slices of a 3D FITS
    data cube.
  + **Extensions**: display images from a FITS multi-extension file.
  + **Imarith**: simple image arithmetic between images
  + **InfoBox**: allows you to display value and position
    information in a separate light-weight window.
  + **Keyboard Actions**: view the current mapping between keys and actions
  + **Magnifier**: will bring up a movable,
    light-weight window showing a blocked image of the data in an area
    surrounding the mouse as it moves. The default magnification of four
    can be changed using command buttons on the magnifier window.
  + **Mouse/Touch**: allows you to change the
    actions performed when you move the mouse over an image with zero,
    one, or two buttons pressed. It also configures touch actions using
    one, two, or three fingers.
  + **Panner**: will bring up a movable,
    light-weight panner window that displays the full image along with a
    viewport rectangle showing the currently displayed image section in
    the primary image window. The viewport can be moved around in order to pan
    to different locations in the primary image. The panner also has
    command button options to zoom the viewport itself. (This makes
    the viewport rectangle larger at the expense of displaying only a
    section of the full image. It is useful for panning in a very large
    image.)
  + **Pixel Table**: displays an array of pixel values around the current mouse position.
  + **Preferences**: set preferences for this session (and/or save for future sessions)
  + **Separate/Gather**: separate images in this display or gather images into this display
  + **Shape Layers**: displays the layers defined for the current
    image and allows you to turn on and off the display of any layer.
  + **Show/Hide Plugins**: displays the currently active plugins and allows
    you to hide plugins defined statically on the web page.

  The **View** menu also contains the following **Display
  Options** submenus:

  + **show ...** options on the display:
    - **value/position ...** a submenu of options for displaying
      the current value/position, including:
      * **update value/position**: specifies whether the image position
        and pixel value is displayed as the mouse (or finger) moves over
        the image. By default, this information is displayed in the upper left
        of the image. The display can be moved anywhere inside the JS9 window by
        clicking on it with the mouse and moving. You also can redirect the
        display to a movable, light-weight window by choosing the
        **InfoBox** menu option.
      * **value/pos color**: allows you to change the color of the
        value/pos display. You can enter color names (e.g., red, lightgreen, steelblue,
        cyan) or values in #RRGGBB format (e.g., #00FF00 is the default bright green).
      * **also show display coords**: specifies whether display coordinates
        are shown in the value/position display when the WCS sys is set to "image".
    - **active shape layers**: toggles display of shape layers
    - **crosshair for this image**: displays a
      crosshair at the mouse position when the Shift key is held down
      (without the Shift key on iOS devices.) It is turned off by default.
    - **match wcs crosshairs**: displays a crosshair in
      other JS9 displays, matching the WCS position of the mouse in this display
      (assuming the other image has its own crosshair enabled.)
    - **toolbar tooltips**: specifies whether tooltips
      are displayed as the mouse hovers over an icon in the **Toolbar**
      plugin. (For mobile devices, a single tap will display the tooltip,
      requiring a second tap to execute the toolbar action.)
    - **new image inherits current params**: specifies whether
      a new image grabs the image params (e.g., colormap, scale, zoom, etc.)
      from the currently displayed image. If false, these params are taken
      from the default JS9.imageOpts object.
  + **resize ...** options to resize the display:
    - **change width/height** specify a new width and height for the
      JS9 display.
    - **set to image size**: set display to current image size
    - **set size to full window**: set display to browser window size
    - **reset to original size**: set display to its original size
* **Zoom:** The **zoomIn** and **zoomOut** menu options
  zoom the primary image in or out by a factor of
  two. The **zoomToFit** options calculates a zoom factor that fits
  the entire image into the JS9 display. You also can set the zoom
  factor to a pre-specified value using menu options or you can specify
  a floating point zoom factor in the **other zoom** text
  box. The **pan to center** option pans to the center of the image,
  while the **reset pan/zoom** sets the zoom to 1 and centers the
  display.

  The **align pan/zoom ...** submenu allows you to change the pan and
  zoom of the current image to match a target image, assuming both have
  WCS info available. Pixel size (i.e. as specified by the FITS CDELT1
  parameter) will be taken into account when zooming, but not image
  rotation or flip (from the WCS params.) This is quicker than
  the **wcs reproject** algorithm for aligning images that are
  similar.

  The Zoom menu also supports **image flip** around the x or y axes,
  **image rotation** by +/- 90 degrees or by an arbitrary
  angle. There also is an option to rotate the image so that north is up
  in the current coordinate system. Flipping and rotation are performed
  on the displayed pixels (so no change is made to the WCS). The
  rotation is much faster than the more general WCS-based
  rotation/reprojection in the **WCS** menu. Note that arbitrary
  rotation is performed in terms of an absolute angle: if you rotate by
  20 degrees and then do it again, there is no change. Also, setting the
  rotation to 0 sets the angle to 0. Flipping and rot90, however, are
  relative to the current state of the display. This differs from DS9,
  where the actions are linked to the x and y axes. Thus, flipping by x
  twice will return you to the original orientation, whereas flipping a
  second time does nothing in DS9.
* **Scale:** Each scale option specifies a different scaling
  algorithm to use when converting image pixel values to RGB
  values. (The procedure for doing this conversion is detailed in the
  DS9 documentation titled ["How It Works"](http://ds9.si.edu/doc/ref/how.html).) The log scale, for example, is
  especially useful with X-ray data. Histogram equalization (histeq)
  tries to maximize contrast across the range of data values and is
  useful in a wide variety of cases. The current scale is marked with a
  starburst.

  You also can change the low and high values used to clip the image
  data before scaling by changing the **low** and/or **high**
  values in the text boxes of the **Data Limits** section. These values are
  set initially with the data's min and max values or the z1,z2 values
  calculated by the **IRAF zscale** algorithm (depending on the value
  of the web site's **JS9.imageOpts.scaleclipping** parameter. The
  default usually is "dataminmax".) Finally, you can use the
  **Scale Controls** plugin to set the clipping values
  to data min/max, zscale z1/z2 or zscale z1/max, or set the clipping
  values using the pixel distribution plot.
* **Colormap:** Each colormap option specifies a different
  distribution of RGB values to use when converting image pixel values to RGB.
  (The procedure for doing this conversion is detailed in the
  DS9 documentation titled "How It Works".) Choose the colormap you like best,
  or try different ones to see how data features can be brought to the fore
  by color and contrast/bias.

  The **image filters** menu option displays the **JS9Filters**
  plugin, which offers a number of well-known image processing functions
  that act directly on the displayed RGB image data (not the underlying
  raw astronomical data, as with the **Gaussian blur** in the **Analysis**
  menu.) Thus, when you can run one of these routines on an image, its
  effect will be undone if you redraw the image by changing the
  contrast/bias, colormap, etc. Also, since these functions act on the
  current RGB image, their effect is cumulative. See the
  **JS9.FilterRGBImage()** section in
  the [JS9 Public API](publicapi.html) for more information
  about the individual functions. Note that not all functions in the
  public API call are implemented here: some of them seemed pretty
  useless for our data (they can be added easily.)

  You can enter a floating point value into the **contrast** and
  **bias** text boxes to set the contrast/bias. Note that the
  contrast value ranges from 0 to 10 and the bias ranges from 0 to 1
  (following DS9 conventions.)

  The **reset contrast/bias** option restores the original
  contrast/bias value (which is especially useful if you changed the
  contrast/bias or scale and now can't see any features at all!)

  The **opacity** option allows you to set the overall opacity for all
  pixels in the image. Values range from 0 (transparent) to 1 (opaque.) More
  opacity options can be found in **Color Controls** (see below.)

  The **load** option brings up a File menu from which you
  can choose a user-defined colormap to load.

  The **save** option saves the active colormap definition
  for the currently displayed image to a file (useful for editing to
  make a new colormap.)

  The **invert** option inverts the colormap (e.g., in the gray map,
  this will change white to black and vice versa.)

  If you have three images of the same size, scale, and pointing
  direction (e.g., three energy cuts of a Chandra data set), you can
  display each one separately and assign to them one of the **red,
  green, or blue** colormaps. If you then select the **rgb mode**
  menu option, they will be displayed as one RGB composite image. The
  current image (as shown in the **File** menu) determines which of
  the three independent colormaps is changed by the contrast/bias
  manipulation. To remove an image from the RGB composite, give it a
  different colormap. Re-join (or add a new image) by assigning one of
  the RGB colormaps. Simply turn off RGB mode to display the images
  separately.
* **Regions:** Astronomical regions format is described
  [here](https://js9.si.edu/regions/regions.html).
  Choose the appropriate menu option to create a
  region of type **annulus**, **box**, **circle**, **ellipse**,
  **line**, **point**, **polygon**, **text**.
  (see below for details on how to use regions.) One or more regions can
  be created and manipulated on a single image.

  By default, a region is created in the center of the image when it is
  selected in the Regions menu. You can turn off auto-creation by
  deselecting the **menu adds region @ center** option. With
  auto-creation turned off, the 'a' key will add the last selected
  region at the current mouse position.

  The **list** menu option will display all regions.

  The **load ...** menu option will load a file of regions and
  display them on the current image. Regions can be specified using the
  a dialect of the widely-used DS9/Funtools regions format, as described
  [here](regions.html).

  The **save ...** display a dialog box allowing you to save selected
  or all regions in one of these formats:

  + **regions** text file in astronomical regions format
  + **csv** comma-separated values
  + **SVG** text file in SVG/XML format (useful for importing into
    programs such as Photoshop for further processing)NB: The file will be saved in the folder where your other browser
  downloads are stored.

  The **copy to ...** menu option will copy regions from the
  current image to a specified image (or to all images.) If one or more
  regions are actively selected in the current image, they alone will be
  copied. Otherwise, all regions will be copied.

  The **remove** menu option will delete all regions.

  The **selected regions ...** submenu contains options that apply to
  the selected region(s), including the ability to edit, list, save,
  remove, or copy the selected region(s). The submenu also allows you
  to change the following properties of selected regions by entering text values:

  + **color**: the color of the region, using either a name
    ("wheat") or #rrggbb syntax ("#f5deb3".)
  + **width**: the numeric width of a region
  + **dash**: two comma or space-delimited numeric values specifying the
    numeric width of a filled segment, followed by the width of a blank segment
  + **tags**: replacement tags for this region

  The selected regions submenu also supports the ability to toggle the
  "source"/"background" or "include"/"exclude" tags (which is heavily
  used in X-ray astronomy.)

  The **onchange** submenu contains the following options:

  + **list on change**: all regions are listed whenever one changes
  + **xeq on change**: toggle whether region onchange callbacks are called
* **WCS:** Use this menu option to select a world coordinate
  system when displaying pixel positions and regions (assuming
  the data file supports WCS.) Available systems are: **FK4**, **FK5**,
  **ICRS**, **galactic**, or **ecliptic**. The **native**
  option chooses the system stored in the data file. The **image**
  and **physical** systems will display only image coordinates (not
  WCS coordinates.) **Physical** coordinates are tied to the original
  (block 1) file coordinates while **image** coordinates are tied to
  the current image data being displayed. Server-side X-ray analysis
  routines operating on the original file generally want physical coords
  rather than image coords. Browser-based plugin routines generally use
  image coordinates to operate on the in-memory image data.

  You also can choose the units in which WCS information is displayed:
  **degrees**, **radians**, or **sexagesimal**. Image and
  physical coordinates are displayed in units of pixels.

  The **alternate wcs** menu option allows you to choose an alternate
  world coordinate system, if one or more are defined in the current
  FITS file. The submenu lists the WCS version (i.e. the letter "A" -
  "Z", or "default") and, if present, the WCSNAME header parameter
  associated with this WCS.

  The **reproject** menu option allows you to reproject the
  image using the WCS associated with another displayed image. The
  reprojected data is placed in a new **raw data layer** called
  "reproject". You can switch between layers using the **View->raw data
  layers** option. If the **display wcs-aligned** option is set,
  the reprojected image will be aligned with the wcs reference image. If
  you change the pan/zoom of the latter, the former will be re-aligned.
  (The converse is not true: changing the reprojected image does not
  change the wcs reference image.) You can also reproject other images
  in this display using the WCS info from the currently displayed image.
* **Analysis:**
  JS9 supports both client-side analysis (i.e.,
  analysis in the browser) and server-side analysis (where requests are
  made to a back-end server, and returned results are displayed in the
  browser.)

  Client-side analysis tasks can be written using the JS9
  [Plugin](localtasks.html) capability, and
  the **Analysis** menu lists the currently loaded **Analysis
  Plugins**. For example, JS9 supplies the
  **Imexam** plugin, which offers the following tasks:

  + 3dPlot
  + Encircled Energy
  + Histogram
  + Radial Proj
  + Region Stats
  + X Proj
  + Y Proj

  JS9 supplies a few other client-side analysis tasks:

  + **Coordinate Grid:** display a WCS-based coordinate grid. The
    coordinate grid parameters can be changed using the **Preferences**
    plugin in the **View** menu.
  + **Counts in Regions:** Run the
    [regcnts](https://js9.si.edu/regions/regcnts.html)
    program (compiled into the browser using
    [Emscripten](https://kripken.github.io/emscripten-site/)) on the specified
    source and background regions and return a text display. This is the
    same task as the server-side task, but running on the internal FITS file.
    (Currently disabled for iOS.)
  + **Radial Profile:** Run the
    [regcnts](https://js9.si.edu/regions/regcnts.html)
    program (compiled into the browser using
    [Emscripten](https://kripken.github.io/emscripten-site/)) on the specified
    source and background regions and return a plot display. The source
    regions consist of circles. This is the same task as the server-side
    task, but running on the internal FITS file.
    (Currently disabled for iOS.)
  + **3D Counts in Regions:** Run the
    [regcnts](https://js9.si.edu/regions/regcnts.html)
    program (compiled into the browser using
    [Emscripten](https://kripken.github.io/emscripten-site/)) on the specified
    source and background regions for each slice in a 3D data cube and return a
    text display.
    (Currently disabled for iOS.)
  + **3D Plot using Regions :** Run the
    [regcnts](https://js9.si.edu/regions/regcnts.html)
    program (compiled into the browser using
    [Emscripten](https://kripken.github.io/emscripten-site/)) on the specified source and background regions for
    each slice in a 3D data cube and plot the background-subtracted results.
    (Currently disabled for iOS.)
  + **Gaussian Blur:** enter a sigma (radius) to create a new raw
    data layer called "gaussBlur", in which the image pixel values are
    blurred using a Gaussian function with the specified sigma. The
    routine uses the fast Gaussian blur algorithm (approximating a full
    Gaussian blur with three passes of a box blur) described [here](http://blog.ivank.net/fastest-gaussian-blur.html).

  In addition, each JS9 site can define server-side analysis
  tasks to be run from the Analysis menu. Server-side tasks are of two types:

  + **immediate tasks:** These tasks are executed directly and
    immediately from the Analysis menu. No parameter setup is needed.
  + **parameter tasks:** These tasks bring up a lightweight
    parameter window allowing various parameters to be set before
    executing the task. Parameter tasks are identified by the presence of
    an ellipsis (...) after the task name.

  For example, the JS9 web page at
  <https://js9.si.edu>
  offers the following tasks:

  + **FITS Header(s):** Display all FITS headers for this FITS file.
  + **Counts in Regions:** Run the
    [regcnts](https://js9.si.edu/regions/regcnts.html)
    program on the specified
    source and background regions and return a text display (immediate task.)
  + **Radial Profile:** Run the
    [regcnts](https://js9.si.edu/regions/regcnts.html)
    program on the specified
    source and background regions and return a plot display. The source regions
    consist of circles or annuli (immediate task.)
  + **Energy Plot:** Create a histogram of the pi column (or energy
    column for Chandra data) of a binary table and return a plot display
    (immediate task.) The column must exist in the data file (e.g.,
    Chandra ACIS data but not Chandra HRC data.)
  + **Light Curve:**Create a histogram of the time column of a binary table
    and return a plot display (immediate task.) The time column
    must exist in the data file.
  + **Histogram Plot:** Create a histogram of the user-specified
    column of a binary table and return a plot display (parameter
    task.) Parameters include: histogram column name, number of bins, use
    bin width instead of bin size, and an option to normalize by bin
    width. A help file is appended to the parameter display.
  + **Event Filter:** filter the events of a binary table and return
    an image representation of the filtered events. Note that when a FITS file
    is loaded directly into JS9, you can use the **Binning/Filtering** plugin
    to filter events instead.

  If you drag and drop a FITS file onto a JS9 web page connected to a
  remove server (such as <https://js9.si.edu>),
  the FITS file will, of course, not be accessible on the server (it's only
  stored in the browser.) As a result, no server-side analysis tasks will
  be available. But if the remote server supports **proxy loading**
  of FITS data, the Analysis menu will display an option to **upload FITS to
  make tasks available**. Select this option and your FITS file will
  be sent to the server so that server-side analysis can be performed.

  The **server-side params** submenu contains the following options:

  + **set data analysis path ...**: specify a colon-separated list
    of directories for JS9 to search when looking for FITS data files that
    have been dropped onto the display. This is used by JS9 when
    performing server-side data analysis on local drag-and-drop FITS
    files. It is necessary to specify data paths explicitly since web
    pages are not allowed to determine the pathname of such files
    automatically (for obvious security reasons.)
  + **set this image file's path**: for local servers only, set the
    path (absolute or relative to the displayed web page) of an image file
    loaded via *Drag and Drop* or *Open Local File*. For
    security reasons, browsers do not expose the path of files loaded in
    these two ways. However, for a local web page, you can safely specify
    the image path in order to refresh the image or run server-based
    analysis.
* **Help:** Show this and other JS9 help pages. The **Help** menu
  also contains help for **Plugins**, including the **Imexam** plugins
  listed above.

### JS9 Mouse Interaction

In keeping with the needs of mobile devices, JS9 utilizes a single
mouse button for user interaction. Keyboard input also is minimized.
Moving the mouse (or a single finger on a tablet) over the image will
display the position/value of individual pixels. Pressing and moving
the mouse (or two fingers) will change the contrast and bias of the
image. A double-click (or double-tap) inside a region will bring up
the configuration menu for that region.

### JS9 Regions

Regions are geometric shapes that can be used to mark part of an image
for analysis. JS9 allows you to create the following region
types: **annulus, box, circle, ellipse, line, point, polygon**.
A **text** region also can be created to annotate an image. When one
of these options is selected, the region is created in the center of
the image. It then can be dragged to the desired location. Arrow keys
also will move the region one screen pixel in the specified direction.
A selected region can be deleted by pressing the **Delete** key (where
available. On a tablet, use the delete option in the configuration menu.)

Click inside a region to select it and display the resize/rotate
controls around its perimeter. Grabbing a handle allows the size of
the region to be adjusted or rotated. In the case of the box and
ellipse regions, the width and height are controlled separately. Click
outside the region to de-select (or click another region to select
that one.)

For a line region, the end-points serve as both resize controls (arrow
icon) and stretch points (hand icon.) You might have to move the mouse
around a bit to switch from one to another. The control action is to
resize the region in both directions (i.e., the same as other regions.)
The stretch action allows you to move this end-point while the other one
remains fixed.

A double-click inside a region brings up a configuration menu. You can
change various values associated with a region by entering new values
in the appropriate text boxes and the clicking **Apply**.

The configuration menu has the following standard options:

* **id:** the id of this region, which can be used programmatically to select it for processing (read-only)
* **type:** the type of region (read-only)
* **image center:** new image pixel values can be entered to change the region position
* **WCS center:** new WCS position values can be entered to change the region position (where WCS is available)
* **Text:** create a child text region with the specified text
* **Color:** change the color of the region (color name or #RRGGBB syntax)
* **Tags:** the default tags (**source, background, include, exclude**)
  are used in X-ray astronomy but you can enter any string to tag this region and then select programmatically using tags
* **WCS Region:** the WCS representation of this region, where applicable (read-only)
* **Image Region:** the image representation of this region, where applicable (read-only)
* **Misc Properties:**use JSON format to specify shape properties not listed above (e.g., {"transparentCorners": true}, see [Fabric.js](http://fabricjs.com/docs/fabric.Object.html) for more info on shape properties.)
* **Options:**
  + **Changeable:** enable/disable move and resize capability
  + **List On Change:** list this region when it's moved or resized
  + **Remove:** remove this region. On an iPad, this currently is
    the only way to delete a region.

In addition, regions of different type support specific configuration
parameters in this menu.
  
The **annulus** region supports:

* **Radii:** change the radii of the region (in pixels)

The **box** region supports:

* **Width:** change the width of the region (in pixels)
* **Height:** change the height of the region (in pixels)
* **Angle:** change the angle of the region (in degrees, counter-clockwise)

The **circle** region supports:

* **Radius:** change the radius of the region (in pixels)

The **ellipse** region supports:

* **Radii:** change the r1 and r2 radii of the region (in pixels)
* **Angle:** change the angle of the region (in degrees, counter-clockwise)

The **polygon** and line regions support:

* **Points:** change the image points of the region (in pixels)
* **Angle:** change the angle of the region (in degrees, counter-clockwise)

The **text** region supports:

* **Text:** change the text of the region
* **Angle:** change the angle of the region (in degrees, counter-clockwise)

A discussion of how JS9 implements DS9/Funtools regions syntax can be found
[here](regions.html).

### Meta Key Accelerator

The **meta** key is the **Command** key on a Mac and the **Control**
key everywhere else.

Pressing the **meta** key disables the value/position display.
It also disables execution of plugin callbacks on
all mouse events. See [Local Tasks](localtasks.html) for
more information about plugins and browser-based analysis.

When a keyboard is available, pressing the **meta** key while
clicking in the primary image window will pan the image so that the
mouse location is in the center of the display (this panning is
disabled inside a region.)

Within a polygon or a line, if you press **meta** and click the
mouse on the polygon or line border, a new point will be added at that
point. If you press the **meta** key and click on an existing
point, it will be deleted.

Within an annulus, if you press **meta** and click the mouse, the
annuli of the annulus region are replaced by an equivalent set of circles
which can be resized (or deleted) individually, but not moved.
Press **meta** and click the mouse again to finalize the region with the
new annuli. Press **shift-meta** and click the mouse to cancel
the edit and restore the original annuli.

### Drag and Drop Images

You can drag and drop FITS images and binary tables, PNG images, and
JPEG images onto JS9 to display the image data. All browser-based
functions (scaling, colormap, pan, zoom, regions, WCS) should work as
expected. You can execute server-side analysis tasks on the FITS files
if the back-end server is running on your local host machine. In this
case, you probably will need to set your DataPath variable in the
Analysis menu to help JS9 locate the original data file.

### Resizing the JS9 Display

The JS9 Display can be resized using the the **View:resize:change
width/height** menu option (or the JS9.ResizeDisplay() JavaScript
routine.) The View menu's resize parameter can be two values (width
and height) or a single value representing both. In addition, if an
image containing wcs info is being displayed, you can append a single
quote to specify a size in arc minutes (e.g., 5') or a double quote to
specify a size in arc seconds (e.g., 300".)

The **View:resize:set to image size** option will set the display size to
the size of the current image. The **View:resize:set size to full
window** option will resize the JS9 display to the size of the
browser window's window.innerWidth and window.innerHeight properties,
and will scroll the display to the center of the window. (Note that
the rest of the web page is still available via scrolling, including
the menubar.) The **View:resize:reset to original size** option will set
the display size back to the original size. Display resize can be
turned off by setting the JS9.globalOpts.resize variable
to **false** in the js9prefs.js file.

Also by default, the JS9 Display can be resized using a grab handle in
the lower right-hand corner of the display. This feature can be
turned off setting the JS9.globalOpts.resizeHandle variable
to **false** in the js9prefs.js file.

See [Known Issues](knownissues.html)
for a discussion of limitations imposed on resize by Webkit
browsers such as Chrome and Safari.

##### Last updated: June 8, 2021

## Links found on page

- 
http://blog.ivank.net/fastest-gaussian-blur.html
- http://ds9.si.edu
- http://ds9.si.edu/doc/ref/how.html
- http://fabricjs.com/docs/fabric.Object.html
- https://js9.si.edu
- https://js9.si.edu/regions/regcnts.html
- https://js9.si.edu/regions/regions.html
- https://kripken.github.io/emscripten-site/
- https://raw.githubusercontent.com/ericmandel/js9/master/help/knownissues.html
- https://raw.githubusercontent.com/ericmandel/js9/master/help/localtasks.html
- https://raw.githubusercontent.com/ericmandel/js9/master/help/publicapi.html
- https://raw.githubusercontent.com/ericmandel/js9/master/help/regions.html
- https://raw.githubusercontent.com/ericmandel/js9/master/plugins/help/mousetouch.html
- https://www.cfa.harvard.edu/
