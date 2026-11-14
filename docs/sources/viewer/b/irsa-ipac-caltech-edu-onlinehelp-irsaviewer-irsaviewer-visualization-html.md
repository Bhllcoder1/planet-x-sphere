---
source: https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/visualization.html
fetched: 2026-11-14
status: 200
---

IRSA Viewer: Visualization

IRSA Viewer: Visualization
--------------------------

At its core, IRSA Viewer is a way of visualizing and interacting
with image files, both [FITS ![](img/jumpout.jpg)](https://en.wikipedia.org/wiki/FITS) and
[HiPS ![](img/jumpout.jpg)](https://ui.adsabs.harvard.edu/#abs/2015A&A...578A.114F/abstract)
formats. You can also overlay catalogs. See [the Catalogs section](catalogs.html) for more on catalogs.
This section covers interacting with the images -- the visualization
tools. The basics of [searching for and loading
images](images.html) are in another section.

All of the interactive image visualization tools work the same basic
way, and here we describe these basic options, in roughly the order
in which you might encounter them in the window.

*Contents of page/chapter:*  
+[FITS/HiPS Viewer](#fitsViewer)  
+[Image Information](#imageinfo)  
+[Navigating Within a FITS (or HiPS) File: HDUs and Planes (Cubes)](#withinfile)  
+[Breaking Out of the Pane (and Going Back)](#breakingout)  
+[Image Navigation](#imagenavigation)  
+[Image Toolbar](#toolbar)  
+[Color Stretches](#stretches)  
+[Image Layers: Viewing/Changing the Layers on the Image](#layers)  
+[World Coordinate System (WCS) Alignment](#wcs)  
+[Extraction Tools](#extraction)  
+[HiPS Debug Tools](#hipsdebug)  
+[Region Selection](#selectregion)  
+[Footprints](#footprints)

---

### FITS/HiPS Image Viewer

You can interactively explore the image with the mouse. Move your
mouse over any image that is loaded into the viewer. Details about the
image, specifically, the pixel beneath your mouse cursor, appear
along the bottom left of the image window. Some information is updated
in real time (coordinates); some information (pixel value) is updated
when you stop moving your mouse for a second or two. The image can be
interactively investigated in this fashion.   
![](img/pixelreadout.png)

You can change the units of what is being read out, in terms of
coordinates or pixel values.

|  |  |
| --- | --- |
|  | If you click on the label of the coordinates, "EQ-J2000" in the screenshot example above, you get this pop-up, from which you can choose the coordinates from among:  * Equatorial (RA/Dec) J2000 in hh:mm:ss ddd:mm:ss format * Equatorial (RA/Dec) J2000 in decimal degrees * Galactic in decimal degrees * Equatorial B1950 * Ecliptic J2000 * Ecliptic B1950 * FITS Image Pixel * Zero-based Image Pixel  If you click on the "click lock" toggle, the coordinates stop dynamically updating when you move your mouse, and they update only when you click on the image. When you do that, little clipboards appear next to each coordinate readout; clicking on those copies the position to your clipboard. From this pop-up window here as shown, you can control the format of the coordinates that are copied to your clipboard -- they can be as shown in the readout, or in the format that Python is expecting (for easy pasting into code). |

|  |  |
| --- | --- |
|  | If you have a FITS image loaded, you have an additional readout. Click on the label of the readout, "Flux" in the tiny snippet of a screenshot example above, and you get this pop-up, from which you can choose the pixel readout from among:  * Integer data readout in decimal * Integer data readout in hexadecimal * Floating point data readout in decimal * Floating point data readout in hexadecimal  If you choose the hexadecimal options, it will suppress all rescaling corrections found in the header, like BZERO or BSCALE. It will just show you the raw binary number in the file. (For example, if the value in decimal is 5.13795757, the binary value in the file is 0x40a46a26; [here](https://www.h-schmidt.net/FloatConverter/IEEE754.html)  is a conversion tool between decimal and hex.) |

|  |  |
| --- | --- |
| In the lower left of the images, if you click on this: , you get this pop-up. If you have a FITS image loaded, at the top of this pop-up, it shows the whole image; the orientation of the image is given with a compass rose. There is also a zoom-in of the image at the location under your cursor. Underneath that in the pop-up, whether you have a FITS or HiPS image loaded, you can get a readout of the pixel size, a readout of location on the image in two different coordinate systems, and a readout of the pixel value. You can change the units of those values by clicking on the name of the field: "Pixel Size," "EQ-J2000," "Image Pixel," and "Value." Each results in a pop-up, as above. |  |

You can make the cursor 'stick' on a particular place on the image --
flip the "Click Lock: off" switch to "on" (either in the pop-up or in
the lower right of the image window), and then click on the image at
your desired location. When this is clicked, small "clipboards" appear
near the position readout. Click on that icon to copy that position to
your clipboard.  
![](img/lockposition.png)

---

### Image Information

The upper left corner of the loaded image has a label that tells you
basic things about the image you are viewing. The telescope and/or
instrument and/or channel and/or data release is first, in black. The
field of view follows, in a paler font; this corresponds to the
(horizontal) width of the image window. The currently selected image
is outlined in brown; other images are outlined in gray.

![](img/iraclabel.png)![](img/mipslabel.png)![](img/uvlabel.png) Here are three examples of image labels. The first is
from Spitzer Enhanced Imaging Products (SEIP), IRAC channel 4, which
is 8 micron data, and the field of view is 12 arcmin. The second is
from data delivered by the Local Volume Legacy (LVL) project, and it
is from MIPS channel 3, which is 160 micron data; the field of view is
1.5 degrees. The third is also from the LVL project, but it is
far-ultraviolet (FUV) data, and the field of view is 32 arcseconds.

If the file has more than one HDU or image plane, controls for stepping
through them appear just above the label; see [Navigating Within a FITS (or HiPS) File](#withinfile) below.

The concept of [coverage images](images.html#coverage) (and
the issues unique to them) is covered in another section, but the
basic interactions with them are the same as for any other images.
They are, however, HiPS images. Choices of what you can do and what
you can manipulate with HiPS images can be different than your choices
for FITS images, but are largely the same as discussed in the rest of
this chapter.

For HiPS images, the FOV is the angular size of the width of the
HiPS viewer. Even if the image as displayed is smaller than the
window, the FOV readout is the width of the window, not the image. If
you shrink your browser screen, the FOV can get smaller because the
viewer gets smaller. If you load more than one image, the FOV can get
smaller because two viewers must fit in the same pane. As a result,
the HiPS FOV requested in the search panel is approximate.

For FITS images, the FOV label on FITS images works analogously to the
FOV label on HiPS images. If you zoom out, the FOV will increase even
when the FITS image is entirely within the viewer. That's because the
FOV is what the viewer can show you based on the pixel size. If you
drag the image so that it is only partially seen through the viewer,
the FOV will not change. For FITS images, the cutout size is not the
same as the FOV.

|  |  |
| --- | --- |
|  | The target on which you searched is overlaid on the main image with a crosshair marker, sometimes called a "reticle." You can remove this (or change its color) from the layers pop-up, described below. |

---

### Navigating Within a FITS (or HiPS) File: HDUs and Planes (Cubes)

A single FITS (or sometimes HiPS) file can contain more than one image. It can have
multiple HDUs (header data units), and any image HDU can itself be a
multi-plane data cube. (See the [Images
section](images.html#fits) for more on HDUs and planes.) The controls described here
let you move around within one file. (To move among different images
you have loaded, see [Image Navigation](#imagenavigation)
below.)

**HDUs (Header Data Units)**

When a file has more than one HDU, an HDU control appears just above
the image label:  
![](img/imagelabel.png)  
Here, "HDU (#1): IMAGE" tells you which HDU you are viewing, including
its name, if the file provides one, and "/ 5" tells you that there are
5 image HDUs. You can step among the image HDUs by using the arrows
(the "greater than" and "less than" symbols) next to the HDU label.
When there are enough HDUs (as here), there is also a box in which you
can type an HDU number, or use the small up and down arrows to change
the number. When there are only a few HDUs, you get just the arrows and
a count.

You can also navigate among the HDUs using the "File Contents" menu
near the upper left of the image:  
![](img/hdulist.png)  
This menu lists all of the HDUs in the file, including any tables.
When it is set to "All Images in File" (the default), you get the HDU
arrows described above.

**Image Cubes (3-D FITS or HiPS): Stepping Through
the Planes**

You can interactively step through the individual planes of a 3-D FITS
or HiPS image cube (much like the Cube dialog in DS9). When the image (or image
HDU) you are viewing has more than one plane, a "Plane" control
appears. In this example, there are multiple HDUs and multiple
planes, and the plane control appears to the right of the HDU
control:  
![](img/cubenav.png)  
Here, the file has 3 HDUs, each with 102 planes. The HDU
control shows the first of the 3 HDUs, and the Plane control shows the
first of the 102 planes, at 0.7530 μm. To step through the planes:

* click on the arrows next to the "Plane" label to go to the
  previous or next plane, or
* type a plane number into the box to jump directly to that plane
  (or use the small up and down arrows in the box).

As for HDUs, when there are only a few planes, you get just the arrows
and a count. The HDU and Plane controls are independent: choose an
HDU, and then step through the planes of that HDU. When the FITS or HiPS header
provides the information, the label tells you the wavelength (or name)
of the current plane, as with the 0.7530 μm plane here. Not every
cube is a set of wavelengths, though; the planes can represent other
things, and then they will not be labeled with wavelengths.

Currently, there is no automatic "play" or animation through the
planes; you step through them yourself.

To get a "quick look" at the values at a given position through all
of the planes of a cube (e.g., a spectrum), use the [drill tool](#extractshort); see the [Extraction Tools section](#extraction) for more details.

---

### Breaking Out of the Pane (and Going Back)
**Panes**: If you have both images and catalogs
loaded into IRSA Viewer, the screen is broken up into panes -- one
for images, one for catalogs, and one for plots from the catalog. If
you have more than one image loaded in, the image pane is further
subdivided.

**Make it big!** For some purposes, it is useful to
individually view just the table, or the images, or the plots, as
large as possible. In any pane, this icon ![](img/expand.png) appears in the upper right of the pane.
Clicking on it will expand the pane into a larger window, as big as
possible given your browser size.

**Go back the way it was:** ![](img/close.png) The
large "Close" arrow at the upper left is always available in the
expanded views, and enables you to return to the pane view.

**Special case of images only:** If you have only images
loaded in, then the images are taking up all of your browser window,
and it is already, by default, in this expanded mode. There's no
'close' arrow in the upper left since there is nothing else loaded
in.

**Removing things:** To remove an image (or catalog)
entirely, click on the small 'x' in the upper right of the image in
the tiled view, or on the small 'x' in the corner of the catalog tab
in the window pane view.

Note that you can also change the relative layout of [the image, table, and plot panes](overview.html#layout) from
the side menu.

Also see the next section on image navigation.

---

### Image Navigation

**Single or Tiled Images**
:   When you have many images loaded in, you can have icons like this:
    ![](img/imagetiles.png) that portray (in icon form) the
    different views you can have of the images you have loaded. The first
    icon (the big square) denotes "show one image at a time." The second
    icon (the cluster of four squares) denotes "show smaller images of all
    the images I have loaded at once," i.e., tiled images. Whether the
    images (tiled or not) take up all the space or not depends on whether
    you are viewing in panes or in the full-screen mode (see immediately
    above on [Breaking out of the pane](#breakingout)).

**Image List**
:   Depending on what you have loaded, you may have an additional
    icon: ![](img/imagelist.png)  
     Clicking on this icon brings
    up a list of the images you have loaded, with some additional
    information on each one. This list is a [table
    like any other](tables.html) in this tool. There are two important things about
    it, though, that apply to this special case: (1) You can sort this
    table, and the images are sorted in response. (2) You can remove
    selected rows, or delete the failed images, with one click; click on
    the corresponding button on the lower right of this window.

    The power of this table is best demonstrated by an example.

    Example: Load the tool. Search on M101, with the default image size.
    Select all bands from the following data sets: SEIP, DUSTiNGS, LVL,
    MIPS\_LG. Search. When the tool comes back, click on the image list
    icon above and obtain this pop-up:  
    ![](img/imagelisttable.png)  
     This
    table shows that it found images of M101 from SEIP, and some LVL
    bands, but nothing in DUSTiNGS or MIPS\_LG. You can use the table to
    omit the failed images all at once. You can click on "Delete Failed"
    on the bottom right, or you can do the following: click the down arrow
    at the top of the "Status" column, check the box next to "Success" and
    then click "Filter." The failed images are removed all at once from
    the table and your display. Now, click the top of the "Wavelength"
    column. The table is sorted by wavelength, and the images in your
    display are now sorted that way as well.

    The "help" links in the far right of this table take you to a master
    list of all data sets available in IRSA Viewer, from which you can
    obtain standard information about the data sets (mission, wavelengths,
    links to more information about the program or delivery, and more).

**Paging through single image views**
:   If you have many images loaded in and click on the single big square
    to view one image at a time, you are provided with navigation aids in
    the upper right, like this:  
    ![](img/paging.png)  
     The
    arrows allow you to scroll through your list of images, sorted as
    specified in the image table. The filled dot in the list of circles
    shows you where your currently displayed image is in the set of loaded
    images. The "auto play" checkbox on the left triggers automatic
    scrolling through each of the loaded images.

**Scrolling through multi-image views**
:   If you have several images loaded in and click on the cluster of four
    squares to view them all at once, you will also have this as a choice:
    ![](img/scrollimagesoff.png)  
    If you toggle this on: ![](img/scrollimageson.png)  
    then each image tile becomes bigger, and you can use your mouse to
    scroll through the collection of images. If you are on a Mac, your
    scrollbar may be hidden until you try to scroll.

    **⚠ Tips and Troubleshooting**

    * If your mouse is in a currently active (selected) image (that is,
      highlighted in brown), then your image will zoom rather than scroll.
      Just move your mouse over to another image, and then your window will
      scroll rather than zoom. Or, find your scrollbar.

**Removing things**
:   To remove an image (or anything else removable) entirely, click on the
    small 'x' in the upper right of the image in the tiled view. Closing
    the upper-right image leaves your mouse on or near the x for the next
    image that fills that corner, allowing multiple images to be closed
    with minimal mouse movement.

---

### Image Toolbar (FITS and HiPS)

The image toolbox is always present as a row of tools associated with
the images you have loaded, or that are loaded on your behalf. They're
generally located above the images you have loaded, with most of them
on the upper right. Letting your mouse hover over any of these icons
will result in a "tool tip" that appears in order to remind you what
the icon does. Most items apply equally to FITS and HiPS images, but
some only apply to FITS images.

This is the image toolbox when you have clicked on a FITS image you
have loaded:  
![](img/toolbox.png)

And, this is the image toolbox when you have clicked on a HiPS image
you have loaded:  
![](img/toolbox-hips.png)

The two toolbars are different, but if the same icon appears, it has
the same effect on the image. Many of the icons have a downward-pointing
black triangle, which means that there are additional options in a
drop-down menu that appears when you click on the icon.

We now discuss the icons in the order in which they appear.

![](img/toolsdropdown-small.png)*Tools drop-down*
:   The choices here look like this:  

    |  |  |
    | --- | --- |
    |  | *[jump to save](#saveimage)*  *[jump to rotate](#rotateImage)*  *[jump to layers](#compass)*  *[jump to extract](#extractshort)*  *[jump to HiPS debug](#hipsdebug)* |

    ![](img/save.png)*Saving the image*
    :   The
        diskette icon will allow you to save the current image. You can save
        files to your local disk or to the [IRSA Workspace ![](img/jumpout.jpg)](/docs/workspace/). Note that **you** control where the
        file is saved on your disk through your browser; your browser may be
        configured to store all downloads in a particular location on your
        disk.

        If the current image is a FITS file, you can save it as a FITS or PNG
        or region file to your local disk. If it is a HiPS file, your only
        choices are PNG or region file. Saved FITS images will not save the
        color stretches or overlays; the tool will just save the underlying FITS
        image. Saved PNG files WILL include any overlays or annotations you
        have placed on the image, but will not include the underlying FITS
        image. Saved region files will not save the underlying image, but
        will just save the overlays as a DS9 region file. See the [DS9
        website ![](img/jumpout.jpg)](http://ds9.si.edu/doc/ref/region.html) for more
        information on the syntax of these DS9 region files.

        Note that you can save the original or a cropped version of a FITS
        file; see the "select region" icon below to crop, then click on the
        save icon. Be sure to save the cropped FITS image (see annotated
        figure). This feature is not available for HiPS images.  
        ![](img/savecropped.png)

        Note that if you [overlay a large catalog](catalogs.html)
        on an image, then turn around and save a region file from the
        catalog overlay, the full catalog may not be saved to the regions
        file. If you have >1000 sources, it's entirely likely that not
        every source will be overlaid on the image (because of [hierarchical catalogs display](catalogs.html#hier)), and thus
        will not be in the region file. If you want to save your entire
        catalog as a region file, **save the catalog from the [table pane](tables.html)**.

        The saved PNG is the same size as it is on your screen. If you want a
        big version, make the desired image big on your screen (view
        one-at-a-time; see [here](#imagenavigation)) before saving
        the PNG.

        You can't save HiPS images from within IRSA's tool. To download your
        own copy, you will have to track down the original source of the
        image.

    ![](img/undoall.png)*Restoring everything to the defaults*
    :   If you've played around a lot with the image, you may want to undo
        everything you've done. Click this button to restore everything to
        its original default values. Some layers may persist; remove them
        via the layers icon.

    ![](img/infolink.png)*Viewing the image header*
    :   This icon displays a pop-up window with information about the
        image. If a FITS image is selected, it will show the FITS header of
        the image; if a HiPS image is selected, it will show the HiPS
        properties of the image. These are Firefly tables like all the other
        [tables](tables.html) in this tool, so they are sortable
        and filterable, etc. If you click on the columns in the pop-up, it
        will sort the keywords alphabetically by that column. This is useful
        for finding individual keywords in particularly densely populated FITS
        headers. Click the header again to sort in reverse-alphabetical order,
        and a third time to return to the default order. Below are examples of
        an original and sorted FITS header. To make this window go away,
        click on the 'x' in the upper right of the pop-up, or click "Close" on
        the bottom left.  
        ![](img/unsortedfitsheader.png)![](img/sortedfitsheader.png)

        For comparison, an example of the HiPS properties window is here:  
        ![](img/hipsinfo.png)

    ![](img/rotate.png)*Rotating the image to any angle*
    :   This feature allows you to rotate the image about the displayed
        center of your image to any angle of your choice, in degrees. (This
        option is only available for FITS, not HiPS, images.) It will rotate
        the image counterclockwise (to the left) East of North if the image
        has a WCS embedded in it.   
        ![](img/rotatepopup.png)  
         You can type a number in the
        "angle" box, or use the slider, to rotate the image. To bring it back
        to North-up, click on the "North up" icon in the pop-up or in the main
        image toolbar. To exit the pop-up without making further changes, hit
        'Close' or the 'x' in the upper right of the pop-up.

    ![](img/northup.png)*Rotating the image so that North is up*
    :   Images retrieved from IRSA Viewer are frequently (but not
        always!) already oriented such that North is up, or close to it.
        However, when interactively investigating images, or loading images
        from other sources, you could find yourself in a situation where North
        is not necessarily up. Clicking this icon will orient the selected
        image so that North is up.

    ![](img/flip.png)*Flipping the image on the y-axis*
    :   Clicking on this icon flips the image on the y-axis. (This option
        is only available for FITS, not HiPS, images.)

        ![](img/compass.png)*Add a compass rose*

        :   When you click this icon, arrows appear on the image showing
            which direction is North and which is East. Clicking on this icon a
            second time removes this compass rose. (You can also remove
            this layer via the layers icon, described below.)

    ![](img/coordinates.png)*Add a coordinate grid*
    :   Click on this icon to overlay a coordinate grid on the image.
        Click it again to remove it. Customize the units of the grid (to,
        e.g., Galactic coordinates) via the "layers" icon (described
        below). (Also see information on the HiPS grid in the [WCS
        section](#wcs).)

        ![](img/ruler.png)*Measuring a distance*

        :   When you click this icon, at first, nothing seems to happen.
            However, you can now click and drag to draw a line on the image, and
            the length of the line is displayed (in the middle of the line). The
            units for the measured distance (and the color of the overlay) can be
            changed from the "layers" icon (described below). You can
            calculate the difference in RA and Dec separately via the layers icon
            as well; find the layer associated with the distance measurement and
            check the "offset calculation" box. When it displays the offset
            calculation, it will give you the angle in degrees in one corner, and
            the length of the line segment in the RA and Dec directions, in the
            units you have specified. When you are done with the distance tool,
            you can click on the ![](img/enddistance.png) that appears
            next to the image toolbar, or click on this icon a second time to remove
            the distance tool. (You can also remove this layer via the layers
            icon.)

            ![](img/ds9icon.png)*Read in a DS9 region file*

            :   When you click this icon, you get a pop-up window from which you
                can read in a DS9 region file from your local disk. See the [DS9
                website ![](img/jumpout.jpg)](http://ds9.si.edu/doc/ref/region.html) for more
                information on the syntax of these DS9 region files. The supported
                regions are text, circle, box, polygon, line, and annulus. To make
                this window go away without doing anything, click on the 'x' in the
                upper right of the pop-up.

                **⚠ Tips and
                Troubleshooting**: If you overlay a list of sources you created
                in DS9 regions format from your disk, it will only be overlaid on the
                current image, not all of the images you have loaded. If you want to
                have it overlaid on all the images you have loaded, create a catalog
                from your source list and overlay it as a [catalog](upload.html#catalogs). Then it will appear on
                all of the images you have loaded, provided that the positions overlap
                on the sky.

    ![](img/marker.png)*Put a marker on the image*
    :   When you click this icon, a drop-down menu appears with several
        possible options:  
        ![](img/markeroptions.png)  
         The first overlay choice (simply
        called 'marker') is a red circle. Initially, it appears in the center
        of the images, and is meant to be moved to wherever you first click in
        the image. It looks like this:  
        ![](img/circlemarker.png).
        The dash-dot line around it means that it is 'active,' so you can move
        (click and drag the marker) or resize it (click and drag the dash-dot
        boundary). You can change the color of the marker (and change the
        label) via the "layers" icon (described below). You can also remove
        this layer via the layers icon. There are several additional options
        in the drop-down, enough that they have their own [section below](#footprints).

        ![](img/drill.png)*Drill down through the image*

        :   If your FITS image has multiple planes or HDUs, especially if
            each plane or HDU represents a different wavelength, it can be useful
            to "drill" down through the image cube at a given position on the sky.
            This tool allows you to do just that. When activated, this tool
            extracts the data at the place your mouse clicks down through the
            cube. For more information on saving the information, see the [extraction section below](#extraction).

    ![](img/line.png)*Draw a line in the image*
    :   When this tool is activated, you can draw a line in your FITS
        image with your mouse, and it will extract for you the pixel values
        along that line. If you have more than one image loaded and visible,
        you can shift-click in another image to see the same line in another
        image. For more information on saving the information, see
        the [extraction section below](#extraction).

    ![](img/points.png)*Make points in the image*
    :   When this tool is activated, you can click in your FITS image with
        your mouse, and it will extract for you the pixel values at the
        location of your click, creating a catalog for you as you click. If
        you have more than one image loaded and visible, you can shift-click
        in another image to extract points from another image. For more
        information on saving the information, see the [extraction section below](#extraction).

    ![](img/hipsgrid.png)*Show the HiPS grid*
    :   When this tool is activated, the HiPS grid corresponding to your
        current view of a HiPS image is shown. For more information, see the
        [HiPS debug section below](#hipsdebug).

    ![](img/hipstile.png)*Retrieve the FITS tile*
    :   When this tool is activated, by clicking on the HiPS image, the
        FITS file corresponding to the HiPS tile is retrieved, if possible.
        For more information, see the [HiPS debug section
        below](#hipsdebug).

![](img/zoom.png)*Zoom*
:   When your mouse is in an image, these options appear in the upper
    left of the image.

    ![](img/zoominout.png)*Zooming in or out*
    :   Clicking on these magnifying glass icons zooms in or out of the image.
        The readout of the net effect of your zooming on the displayed field
        of view (FOV) appears at the top left of each image.

        If you click zoom in or out rapidly, a pop-up window appears to allow
        you to more rapidly select the zoom level (field of view) you want.
        Select the desired level, or click on the 'x' in the upper right to
        make the window go away. Here is an example:   
        ![](img/zoomlevel.png)

        You can alternatively zoom using the mouse wheel (or drag forward
        and backward on a touchpad or Magic Mouse).

        Note that there are maximum (and minimum) allowed zoom levels, and they
        are different for FITS and HiPS images. A notification will appear
        when you have reached the maximum (or minimum) allowed zoom level for
        a given image. To enlarge images more (or less) than that, please
        repeat your search to obtain new images with smaller (or larger)
        spatial extent. HiPS images are specifically designed for large areas,
        so if you need a big area, use HiPS. If you want to zoom in close
        enough to see individual original pixels, your best choice is FITS.

        See also the section in the Images chapter on [changing coverage images](images.html#changing), specifically
        that on automatic transitions while zooming.

    ![](img/fitandfill.png)*Fit image to screen or fill screen*
    :   These two icons are designed to maximize the available space in your
        browser window. The first one automatically picks a zoom level such
        that the image entirely fits within the available space (which could
        be your whole browser window, or just the portion of it where that
        image is loaded). The second one automatically picks a zoom level such
        that the image fills as much of the available space as possible (i.e.,
        it is zoomed such that the short axis of the window is filled with the
        image, whether that short axis is left-right or up-down).

        By default, the images that are returned are frequently but not always
        centered on your search target. Clicking on these icons lets you see
        the whole image that is returned, whether or not it is centered on
        your target.

        This is available for both FITS and HiPS images, though note that FITS
        images retrieved from IRSA using this tool are typically square, and
        HiPS images cover the sky, so fitting the image to the screen
        might not be what you want to do.

    ![](img/zoomoriginalsize.png)*Zooming to a 1-to-1 size*
    :   Clicking this icon will zoom the image such that one pixel in the
        image is one pixel on your screen. This option is only available with
        FITS images; HiPS images by their nature have pixels of varying sizes,
        so this button would have no meaning in this case.

![](img/colortable.png)*Color table drop-down*
:   This icon enables you to change the color table of the
    displayed image. (This option is available for FITS and HiPS
    images.) When you click the button, a drop-down menu appears.

    |  |  |
    | --- | --- |
    |  | * The top of the menu either says "Color, stretch & overlays locked" or   "Color, stretch & overlays unlocked" -- by default, all of the (FITS) images   that you have loaded are locked together for color, stretch, and overlays. What   that means is if you change the color table (via this menu), then the   color table for all the (FITS) images is changed. (Or, if you add a   layer to one image, then the layer is added to all the images; see   below.) If you don't want this to happen, select "Color, stretch & overlays   locked" to unlock it. Select the text again to lock it again. * The arrow in the upper right creates a pop-up window out of this   drop-down menu so that you can leave the choices up while settling on   the best option. * The next portion of the menu has a wide variety of color table   choices. Select your new color table from the options shown. * The sort of swirly, hurricane-like icon at the end of each color   table means "invert this color table." If you click on this icon, it   will invert the specific color table and then implement it in your   image(s). * Alternatively, you can use the "color bar" slider to move   among the color tables by number. These numbers correspond to the   color bar number used in the Python implementation of the Firefly   tools. * Pixels that are NaNs in the image are portrayed as the color shown   by the swatch next to "NaN Pixel Color (Auto)." The tool is finding a   color that is most different from the colors used in the image(s) as   currently shown, and using that to render the NaNs in the image. If   you want to change that, click on the color swatch to bring up a   pop-up from which you can click on a different color, enter the hex   code, OR enter the RGB numerical values; the color you pick will   persist until you pick a different color table: * At the bottom, there are sliders controlling the bias and   contrast. Click or drag the slider to change the image display. * If you create a 3-color image, the color table drop-down allows you   to turn individual color planes (red, green, and blue) on and off, and   also to change the bias and contrast individually for the 3 color planes. |

![](img/stretch.png)*Color stretch drop-down*
:   This icon enables you to change the color stretch of the displayed
    image. (This option is only available for FITS, not HiPS, images.)
    Because this is complicated, for much more information, please [see below](#stretches).

![](img/recenter.png)*Re-center the image drop-down*
:   Clicking this icon produces a drop-down menu:  
    ![](img/recenterpulldown.png)  
    By default, "Pan by table row" is turned on (checked), but, depending
    on how you have loaded your images, or whether you have catalogs
    loaded, it may not seem to do very much. However, if you have a
    catalog loaded and are zoomed in on your images, as you scroll through
    your catalog, the FITS image underneath will move as needed when you
    have selected an observation in a different part of the sky than was
    originally shown.

    **Example of "Pan by table row" functionality:** Load the
    tool. Search on M101, and ask for all SEIP channels (4 IRAC, 1 MIPS).
    When it returns, search on catalogs. Select a WISE/AllWISE catalog,
    and ask it for a polygon search covering the image that is loaded.
    When the catalog loads, go up to the image toolbox and be sure to
    select Align and Lock by WCS (see [WCS Alignment](#wcs)
    below for more information). Sort the catalog by RA by clicking on the
    top of the RA column. Note that the images are all now slewed to
    center the first object (the farthest east) in the catalog. Click on a
    source in the plot near the west edge of the image. Note that the
    images are all now slewed to center that newly selected source.

    Other choices are to center on the target of the observation, center
    the image in the window, or center on a target of your choice. For the
    last of those, you can simply center on that target, or center and
    leave a marker on the image at that location.

    That last option may or may not appear, depending on what you have been
    doing before getting to this screen. If it can, it gives you a choice
    to center on recent positions. Move your mouse over to the arrow to
    select from a list.

![](img/selectregion.png)*Selecting a region drop-down*
:   When you click this icon, you can select a region of the image for
    further actions. Because this is complicated, for much more information,
    please [see below](#selectregion).

![](img/layers.png)*Image Layers: Viewing/Changing the Layers on the Image*
:   Every time you add something new to the image, you add a 'layer'
    to the image. This is complex, so please [see
    below](#layers) for much more information.

![](img/lockimages.png)![](img/unlockimages.png)*Lock/unlock images*
:   You may have this "lock images" icon appear in your toolbar; it
    will appear as the first icon if they are locked and the second icon
    if they are unlocked. The
    main purpose of this icon is to lock all the images you have loaded
    for zooming, scrolling, etc. You need to specify how it locks and for
    how long. Clicking it produces this drop-down menu:  
    ![](img/lockimagespulldown.png)  
    The first set of options aligns the images only once, temporarily; the
    second set of options makes the alignment persist ("lock") when you
    move the images (that is, when you move one, they all move). You can
    align by the images' WCS (e.g., RA and Dec), by the target, by the
    pixels according to the origin of the coordinate system in the image
    header, or by the pixel at the image center. The most common choice is
    likely the WCS align and lock. You can align FITS and HiPS images to
    each other. This is discussed in more detail in the [WCS
    section](#wcs).

    ![](img/pinchartbutton.png)*Pin image*

    :   This icon does not always appear. If you do have this icon, you
        can "pin" the image. Within this tool, "pinning" just means "hold on
        to this item within this tool." It doesn't mean "save this data to
        disk," nor does it mean "download all the data that goes with this";
        it means "retain this item in this tool for now." Think of it as if
        you have a metaphorical bulletin board behind your computer monitor
        and you want to put an image you see on that bulletin board
        temporarily (with a pushpin!) to remember it while you continue to
        look through other images. In many cases, the tool will treat images
        as already pinned for you. In other cases, you have to actually pin
        them before it will create a pinned images tab.

![](img/help.png)*Getting help*
:   Clicking on this icon takes you to this help page, usually to a
    spot in the help relevant to whatever you're currently doing.

To remove an image (or anything else removable) entirely, click on the
small 'x' in the upper right of the image in the tiled view, or on the
small 'x' in the corner of the image (or catalog) tab in the window
pane view.

---

### Color Stretches
![](img/stretch.png) This icon enables you to change the color
stretch of the displayed image. (This option is only available for
FITS, not HiPS, images.) When you click the button, a drop-down menu
appears with a variety of choices.

|  |  |
| --- | --- |
|  | The top of the menu either says "Color, stretch & overlays locked" or "Color, stretch & overlays unlocked" -- by default, all of the (FITS) images that you have loaded are locked together for color, stretch, and overlays. What that means is if you change the color stretch (via this menu), then the color stretch for all the (FITS) images is changed. (Or, if you add a layer to one image, or change the color table of one image, then the change is made to all the images; see other sections of this chapter.) If you don't want this to happen, select "Color, stretch & overlays locked" to unlock it. Select the text again to lock it again. |

Below that, you can choose from a set of pre-selected options. If you
pick the first one, "color stretch," you can customize the stretch. A
pop-up window appears with a histogram of the values in the image, and
you can change the stretch type and range.   
![](img/customstretch.png)  
 If you
pick a color stretch from the pre-defined options, the pop-up window
reflects this change. If you change the color stretch in the pop-up
window, the drop-down menu changes correspondingly.

**Example:** Display the pop-up for color stretch. From
the main drop-down, pick 'Linear stretch to 99%'. Go back to the color
stretch pop-up. Note that it has filled out the stretch type and
ranges to reflect the current choice. Then -- either with the pop-up
window still up or not -- go back and pick a different pre-defined
stretch from the standard options. Note that the values in the pop-up
change to reflect this current choice. From the pop-up, pick a
different stretch type -- try "histogram equalization." Select
"Refresh" to update the images. Go back to the drop-down menu. The
last 7 items have changed to be based on histogram equalization, as
opposed to the "linear" default.

If you have a 3-color image, you can change the stretch in each color
plane separately; select the tab at the top accordingly for red,
green, or blue. By default, it stretches each band independently, and
you can set the parameters in the stretch pop-up accordingly.

![](img/3colorstretch.png)

As described in [Lupton et al. (2004) ![](img/jumpout.jpg)](https://ui.adsabs.harvard.edu/#abs/2004PASP..116..133L), a different algorithm may be useful for creating
3-band color images. Select "Hue preserving stretch" to invoke this
option. This stretch should be a brightness-independent
color-preserving asinh stretch, though in practical terms, it seems to
work best for optical images.

![](img/luptonstretch.png)

It may be useful to scale individual channels; sliders allow you to do
so. The Q parameter has another slider. For a linear stretch, Q=0;
increase Q to change what features are emphasized. Pedestal values can
also be set to allow the level assigned to "black" to change.

---

### Viewing/changing the layers on the image
Every time you add something new to the image, you add a 'layer'
to the image. You can have an image with a lot of annotations on
it.

![](img/layers.png) The number that appears circled in blue
over the layers icon tells you at any given time how many layers you
have on the currently selected image (the image outlined in brown).

|  |  |
| --- | --- |
| If you click this layers icon, you will get a pop-up window with a list of all the layers you have on top of the image. Here (on the right) is an example of a well-populated layers pop-up; in real life, this is scrollable to see several more layers. From this pop-up, you can:  * turn layers off and on (click on the switch on the left of the   corresponding row); * remove layers entirely (click on the 'x' on the right of the   corresponding row); * change colors of overlays (see below); * change symbol shapes and sizes (for [overlaid catalogs](catalogs.html)), including [hierarchical catalog   settings](catalogs.html#hier); * change annotations (for markers); * or change units (for the coordinate grid or the [distance tool](#distancetool)).  To add entirely new layers, though, you need to go to other options within the toolbar. You can "show all" or "hide all" with the buttons on the lower left of the pop-up window. To make this pop-up window go away, click on the 'x' in the upper right of the pop-up.  Note the target description:  This reminds you of the target on which you searched -- here, it was M101, where the coordinates were resolved by NED (as opposed to SIMBAD). The two icons next in that row indicate, respectively, "copy this location to the clipboard" and "center image on this position." |  |

|  |  |
| --- | --- |
| Where it's possible to change colors of a layer, click on the 'colors' link to be taken to a new pop-up from which you can select a new color. From here, you can click on your desired color in the top colorful box. Immediately below that box, you can change the color and saturation of the top box so that you can select from a different range of colors. Below that, you can enter numerical hex codes or RGBA values (where the value for RGB is between 0 and 255, and A is in units of percent, e.g., 50 = 50%). Finally, you can also select from a pre-defined set of 15 colors by clicking on any of the small boxes. Note that the numerical codes update as you select different colors. Your choices are implemented as soon as you select them. Click 'Close' to close the window, or click 'x' in the upper right.  If you have a [catalog](catalogs.html) loaded into the tool, you can also obtain this pop-up by clicking on the color swatch in the heading of the catalog tab. |  |

|  |  |
| --- | --- |
| For catalogs or the search target, you can also select the symbol shape and size. To adjust the size, type in the symbol size in pixels or use the up/down arrow keys to change the size by one pixel at a time. Your choices are implemented as soon as you select them. Click 'Close' to close the window, or click 'x' in the upper right. |  |

Note that if you load both FITS and HiPS images at the same time, it
can include a marked layer on the HiPS image that is the footprint of
the FITS images you have loaded. A label appears at the center of that
footprint, which may be disconcerting if you are not zoomed out enough
to see the region itself. Here is an example, zoomed out so it is
clear what is going on:  
![](img/hipsregion.png)

Once you have loaded a HiPS image into IRSA Viewer, if you select
the HiPS image and click on the layers icon (![](img/layers.png)), you will have new, HiPS-specific choices in the
layers:  
![](img/hipslayers.png)

**HEALPix (HiPS) Grid**
:   To turn on these choices, toggle the switch to the left of "HEALPix
    (HiPS) Grid." (See [here](images.html#hips) for more
    information on HiPS images in general.)

    **Auto**: This option overlays a position grid, with the
    tile numbers marked in the center of each box. As you continue to zoom
    in, when smaller tiles are needed, they are drawn, with the new tile
    numbers marked. You may not zoom beyond HiPS Norder level 14 tiles.
    The numbers after the "/" are in the "NESTED" (as opposed to RING or
    NUNIQ) numbering system; see [the IVOA
    standards document ![](img/jumpout.jpg)](http://www.ivoa.net/documents/HiPS/) for
    more information.

    **Grid Match Image Depth**: If you select this option,
    the grid will adjust to a new level when you zoom in and a new level
    of HiPS image both exists and is used for the display.

    **Grid Level Lock**: Selecting this option yields an
    additional numerical drop-down menu. The higher the number you pick, the
    smaller the grid boxes that are drawn. When this option is
    selected, the boxes stay the same size regardless of how zoomed in on
    the image you are.

**HiPS MOC**
:   To turn on these choices, toggle the switch to the left of "MOC."

    (See [here](images.html#moc) for more
    information on MOCs in general.)
    A MOC tells you via a simple boolean yes/no whether there is
    sky coverage from this data set in this region. The choices here are:

    * Outline - an attempt to outline the entire region covered by the
      data; it still sometimes struggles near the edges of coverage, so zoom
      in to get a better sense of the coverage edges.
    * Fill - filled regions, where you can control the opacity of the
      overlay by going to the [color picker](#colorpicker); you
      control the opacity by changing the number above the "A".
    * MOC Tile Outline - individual tile outlines, where the tiles are
      set by the MOC tiles themselves (as opposed to tiles created by the
      mosaic tiles that make up the data set).

**⚠ Tips and Troubleshooting**:

* The entire concept of a MOC is built upon the "tiles" that are
  inherent to the [HiPS concept](images.html#hips). As a result, those tiles are imprinted
  on how the MOC is rendered, especially near edges or corners of
  coverage. Strange behavior may result; you can always zoom in to get a
  better sense of the coverage. For authoritative information, download
  the actual data for the region you are concerned about.
* For the "fill" option for a MOC, depending on how you
  display a MOC, you may see two shades of color in the MOC. It is
  important to note, though, that the
  information it is displaying does not include depth of coverage,
  merely boolean "is there data there or not." Why is it displaying
  shading? Well, it's rounding. For example, a given WISE MOC might be
  generated at order 13. At this order, there are 805,306,368 HEALPixels
  on the sky, and they are about 26 arcseconds across. When zoomed out
  far, there is no point in trying to show each of these pixels, so the
  application "rounds up" the MOC to an order in which there are roughly
  100-200 displayed HEALPixel polygons horizontally across the image.
  When it does this, it flags the rounded-up polygons with the paler
  color. So the boundaries of a coverage region in the MOC all get a
  paler color. If you zoom in far enough on a MOC, the two-tone colors
  go away.
* You might be here in the documentation looking for more
  information on [hierarchical catalog
  settings](catalogs.html#hier); this is also related to HEALPix.

---

### World Coordinate System (WCS) Alignment
As described above, there is a way to lock/unlock images to each
other ![](img/lockimages.png)![](img/unlockimages.png)
for position matching. This section describes
the image locking in more detail.

When aligning images, you can specify how the images align and for
how long. Clicking the lock images icon produces this drop-down
menu:  
![](img/lockimagespulldown.png)

The first set of options aligns the images only once; the second set
of options makes the alignment persist ("lock") when you move (zoom,
etc.) the images.

You can align by the images' WCS (world coordinate system,
e.g., RA and Dec), by the target (align by target on the screen,
regardless of position in the sky), by the pixels according to the
origin of the coordinate system in the image header, or by the pixel
at the image center. The most common choice is likely the WCS align
and lock.

Here are examples of different alignments, in this order: align by
WCS, by pixel origin, and by pixel at image centers.  
![](img/alignbywcs.png)![](img/alignbypxorigin.png)![](img/alignbyimgcenter.png)

Note that aligning by WCS puts North up and aligns the images so that each
has the same angular scale.

In contrast, here is an align
by target -- six different galaxies, but the target used for each
image is in the center of each image tile.  
![](img/alignbytarget.png)

Aligning images by position on the sky is likely to be the most common
use of locking. You can align FITS and HiPS images to each other.

**⚠ Tips and
Troubleshooting**

* When you have both FITS and HiPS images loaded,
  if you select a HiPS image to be active when you select "lock by WCS,"
  the HiPS image will not lock to the FITS image unless the image is either
  J2000 or galactic north up. If you want the HiPS image to align to the
  FITS image, select the FITS image first and then select "lock by WCS."

---

### Extraction Tools
Several tools allow you to extract information from images or image
planes, but only for FITS (and [sometimes even
HiPS](#hipsdebug)) files. **All of these extraction tools are meant for
quick-look assessments, not science-ready analyses.** They
don't do any pixel interpolation, for example.

* ![](img/drill.png) -- Extract down through image planes
* ![](img/line.png) -- Extract a line from the image
* ![](img/points.png) -- Extract points from the image

All three of these follow the same basic structure --

1. Initiate extraction mode
2. Set aperture
3. Try extraction; repeat if desired
4. Pin (retain) extraction if desired
5. Download (as table or chart) if desired
6. Repeat extraction if desired
7. Click on "end extraction" to finish the process

The drill pokes down through multiple planes, the line moves across
pixels in a plane, and the points tool extracts points from a plane.

Here, we cover the basic approach, with specifics of each
tool integrated as we go along.

**Initiate extraction mode.**
When you click on one of these icons, you enter into the extraction
mode. Text appears next to the image toolbar to remind you that
you are in this mode: ![](img/endextraction.png) When you are
done, to end this mode, click on this "end extraction."

When starting out, the pop-up window that you get depends on the tool
you pick.

|  |  |  |
| --- | --- | --- |
| For the drill: | for the line: | and for the points: |
  |  |  |

**Set aperture.** In all three cases, the top center of
the extract pop-up window has a drop-down from which you can select
the aperture value. For the drill and points, you can choose, in
pixels, 1x1, 3x3, 5x5, or 7x7. Values can be summed or averaged. For
the line, it's a little different. The apertures are 1x1, 1x3, 1x5, or
1x7, and you control whether the points are summed or averaged. You
can have it extract along a line that you draw with your mouse on the
image (useful for examining brightness profiles, e.g., across spiral
arms of a galaxy), or you can have it extract an entire line or column
of the image that you specify (useful in the cases where the 'image'
is a file where the first row is an extracted spectrum, the second row
is the error, the third row is a mask, etc.).

**Try extraction.**
From this point, you can click on your image, or click and drag for
the line tool. The pop-up then contains a plot of your extraction.

|  |  |  |
| --- | --- | --- |
| For the drill: | for the line: | and for the points: |
  |  |  |

In each of these cases, it does the best that it can to label the axes
accordingly. The cube that is used for the drill example here follows
the spectral data model so that it is recognized as a spectrum, and it
plots against wavelength. The line extraction is a 1x3 average and
plots the offset in arcseconds from the initial mouse click, given the
WCS information in the header of the image. The point extraction is a
3x3 sum, and is plotted in image x coordinates, but can be changed to
show image y coordinates.

Note that for the line, if you have more than one image loaded and
visible, you can shift-click on a new image to see the same line on a
new image. Similarly, for the points, you can shift-click to change images
without extracting points.

For the line extraction, if you want to change at this point to
extract along a line or column, use the drop-down menu at the bottom
of the pop-up. It's shown here as "free hand selection," but the other
choices are line or column selection; you click on the image to select
a line or a column, which is particularly useful for quick looks at
semi-extracted spectral images.

**Pin extraction.**
Once you have an extraction that you like, you can retain the
extraction for further analysis. "*Pin
chart/table*" extracts the information as a [table](tables.html), just like any of the other tables in
this tool, with an accompanying [plot](plots.html). You can
then manipulate the table/plot just like any other table or plot in
this tool. If the tool recognizes the extraction as a [spectrum](spectra.html), you may have additional
capabilities.

Once you pin or save your extraction, the tool leaves a "footprint" of
your extraction on the image so that you can remember what the
extraction was. **NOTE THAT it is not interpolating**
across fractional pixels here. It averages if you have asked it to
average, but it does not interpolate. This is most obvious when your
pixels are large and you draw a line diagonally across them; such a
line gets rendered as these pixels:  
![](img/notinterpolating.png)  
The point appears on the image at the lower left corner of the
relevant pixel.

You can pin as many different extractions as you want.

From the line extraction pop-up, when you click on "Pin Chart/Table,"
you get another pop-up:  
![](img/pinextract.png)  
From this pop-up, you can choose to extract the line from:

* just the currently selected image (most likely where you drew your line);
* all the images, with all of the extracted lines in one big table (and tab); or
* all the images, with each extracted line in its own table (and tab).

When you do this, the question
naturally arises as to how the tool should specify which column (or
tab) goes with which image. Some of the images have long, sometimes
cryptic titles. You can choose to have the tool use the full image
titles in the column headers or tab titles, or abbreviations.

If you choose to have the tool generate one table for each image you
have loaded, you may suddenly have a lot of new tabs at the bottom of
the screen. There are navigation aids within the [tables section](tables.html#navigation) that may help.

**Download extraction.** You can download the extraction
as a table or plot without pinning it. *Download as Table*
saves the table to your local disk. First, you have the same three
choices as when pinning (see immediately above): the selected image
only, all images in one table, or all images in separate tables. Then
you have [all the same save options as a regular
table](tables.html#save). *Download Chart* saves the plot as shown, as a PNG
file.

After pinning an extraction, you also have the extraction appearing as
a table in the tables section of your window and as a plot in the
plots section of your window. As with [any
table](tables.html#save) in this tool, you can save the table by clicking on the
diskette icon in the table. You can choose from a variety of formats;
[see the tables chapter for more
information](tables.html#save). Similarly, as with [any
plot](plots.html#saving) in this tool, you can save the plot by clicking on the
diskette icon in the plot. See the [plots
chapter](plots.html#saving) for more information.

**Repeat extraction.** As long as the extraction pop-up
is still open, you can continue to click points or draw lines to make
additional extractions.

**End extraction mode.** ![](img/endextraction.png)
When you are done, click on "end extraction." Alternatively, just click on the 'x' in the upper
right corner of the extraction pop-up.

**Advanced capabilities.** If you have a complicated
multi-extension FITS file with HDUs that are labeled things like
image, uncertainty, variance, flags, etc., you have some additional
options for extraction. When you pin the extraction, you can specify
an aperture larger than 1x1, which then raises the question of how the
pixel values are combined. When you have information that the tool
recognizes, and when you choose a larger aperture, you then get an
additional drop-down from which you can choose how the pixels are
combined: average, sum, or even logical "OR," depending on the
data:  
![](img/extractionadv.png)

---

### HiPS Debug
These "HiPS Debug" tools are listed near the [extraction tools](#extraction) because they are in the same
family as the extraction tools in that they can be used on the image
to extract additional information.

[HiPS images](images.html#hips) are constructed from FITS
images, and if the metadata are assembled correctly, the HiPS image
should be able to communicate to this tool where and how to obtain the
corresponding FITS image. It is complicated, there can be some really
obvious projection effects, and the phrase "if the metadata are
assembled correctly" is doing a lot of heavy lifting in that sentence.
Your mileage may vary. This is why it's called "HiPS Debug."

There are two icons here:
![](img/hipsgrid.png)![](img/hipstile.png)

To use these tools in the most efficient way possible, after you
have loaded a HiPS image, first enable the HiPS grid overlay by
clicking on the grid icon, which turns on the grid. (This is the same
grid overlay as [here](#hipsgrid).) If you zoom in and out
on your loaded HiPS image, the grid will respond and show you the
corresponding HiPS tiles. When you find a tile you want to retrieve,
click on the HiPS tile icon. This initiates a tile selection mode.
(Note that you have to have selected a HiPS image before you can do
this.) You get this pop-up window:  
![](img/hipstileextract.png)

You can grab and drag the top of the window to reposition it if need
be. Then click on the tile you want in the HiPS window and click on
"Extract Tile" in the pop-up. The corresponding FITS image will appear
on the right-hand side. To select another FITS image, go back to the
HiPS image and select again. When you're done, close the pop-up or
click on "End Extraction."

By default, the images should all be [WCS-matched](#wcs);
i.e., move one and they all should move together.

**Note that** if these tools appear, you may also
be able to perform the [other kinds of
extractions](#extraction) *on the HiPS image*. What this is doing is
reaching down to the underlying FITS images, much like these "HiPS
Debug" tools, and running the (drill, line, point) extractions on the
underlying FITS files, just as described [above](#extraction), with all the corresponding caveats.

**⚠ Tips and
Troubleshooting:**

* This is a complex and often confusing process. You will have better
  luck **in all of the issues listed here** by zooming in
  farther on the HiPS images, as far as you can go, before requesting
  the corresponding FITS tiles.
* Any given HiPS file may not have enough information to go back to
  the constituent FITS images properly.
* HiPS tiles are rarely square, but the FITS tiles are pretty much
  always square. The distortions can be super obvious and disconcerting.
  (Ellipsoidal stars! Substantial diamonds rather than squares!)
  Projection effects are real (HiPS are spherical projections), and can
  be worse in some locations.
  **When in doubt, before doing science on the FITS images, go
  back to the original archive and retrieve original FITS
  files.**
* Positional uncertainties may be large.
* For extractions, see all the [caveats
  above](#extraction), plus the caveats here.

---

### Region Selection
![](img/selectregion.png) When you click this icon, you can
select a region of the image, from which then you can do a whole host
of things to the image and to the catalog you may have overlaid upon
it.

|  |  |
| --- | --- |
| First, from the drop-down, you are given a choice of a cone selection or a rectangular selection: |  |

After you make that choice, you can click and drag in the image,
selecting a circle or box on the image. For the circle, your click
is the center of the circle and the drag sets its size;
for the box, your first click is one corner of the rectangle, and the
drag is the opposite corner of the rectangle. This region can be
resized by grabbing and dragging the corners of the box or the pixels
delineating the corners of a box around your circle. If you need to
move the image underneath, you can hold the shift key and click and
drag.

When you have selected a region of the image, additional icons
appear above the image, and exactly which icons you see is a function
of whether you are working on a FITS or HiPS image, and whether or not
you have a catalog overlaid: ![](img/selectoptions.png) These
icons allow you to do several things:

![](img/crop-small.png)*Crop the image*
:   (FITS only) Crop the image to the selected region. Then you can
    save the cropped FITS image via the save icon described above.

    **Note that** if you have a rotated FITS image such that
    a crop would have to bisect pixels, it will show you the region that
    encompasses your selection. If you crop at that point, then, it will
    crop in image space (such that pixels are not bisected). See the
    figure below -- in the original image, North is up. This has been
    rotated 45 degrees. The selected region is in white. The yellow
    dash-dot line is the crop in pixel space that encompasses the selected
    region.   
    ![](img/cropregion.png)

![](img/checkmark-small.png)![](img/cancelselection.png)*Select sources* (and *cancel selection*)
:   (Only if a catalog is overlaid) Select the catalog sources overlaid on
    the image within the region. Selecting highlights the sources in the
    list and plot with a different color row or symbol. Once there are
    selections made, the second icon appears to give you an option to
    cancel the selection.

![](img/filter.png)*Filter sources*
:   (Only if a catalog is overlaid) Filter the overlaid catalog down to the
    sources within the enclosed area. When you choose to impose a
    filter via this selection mechanism, the filters icon changes above
    the catalog to indicate that there is a filter applied (![](img/filtersapplied.png)). To clear the filters, click on the
    cancel filters icon (which also appears after you impose filters):
    ![](img/cancelfilters.png). There is much more on [filters](tables.html#filters) in the Tables section.

![](img/zoom-small.png)*Zoom the image*
:   Zoom the image to fit the selected area into your field of
    view.

![](img/recenter-small.png)*Recenter the image*
:   Recenter the image on the selected area.

![](img/stats-small.png)*Obtain statistics*
:   (FITS only) Obtain statistics from the image on the region.
    The statistics option results in a pop-up that looks
    something like this:  
    ![](img/imagestatistics.png)  
     Note
    that it calculates the location of the minimum and maximum fluxes, and
    the aperture and flux-weighted centroids; the flux values given are in
    the same units as the FITS file. If you put your mouse over the row of
    the table in the pop-up, that location appears as an 'x' on the
    image.

![](img/searchaction.png)*Search*
:   |  |  |
    | --- | --- |
    | This tool implements a new search, an "action," on the region you have selected. It results in this drop-down (right), where this example is based on a region centered on 84.036131, -69.224431, J2000 decimal degrees, over a 4-cornered polygon. (You can also use the region tool to define a cone; this example happens to be a rectangle.) From this drop-down, you can launch:  * A TAP polygon search over this region ([more   information about TAP searches](othersearches.html#generaltap)) * A NED cone search at this position with a radius attempting to   correspond to this polygon ([more   information about NED searches](othersearches.html#nedcatalogs)); results loaded into this tool. * A SIMBAD cone search at this position with a radius attempting to   correspond to this polygon; results loaded into this tool. * A SIMBAD cone search at this position with a radius attempting to   correspond to this polygon, but launch another browser window or tab   at SIMBAD with the results. * A TAP cone search at this position with a radius attempting to   correspond to this polygon ([more   information about TAP searches](othersearches.html#generaltap)); results loaded into this tool. * A FITS [image search](images.html) at this position (at IRSA, via this tool); results   loaded into this tool. * A HiPS [image search](images.html) at this position (via this tool); results loaded   into this tool. * A cone search of the SOFIA archive at this position with a radius   attempting to correspond to this polygon; results loaded into the   SOFIA tool. * A cone search of the WISE Image Service at this position with a   radius attempting to correspond to this polygon; results loaded into   the WISE tool. * Refine the search region |  |

    The last option brings up another pop-up window (similar to [this](othersearches.html#interactivetarget)) that allows you
    to refine the search region iteratively by choosing a cone or polygon,
    setting the center, and setting the cone size or polygon vertices.  
    ![](img/imageactionrefinesearch.png)  
     From here, you can change the kind
    of search, refine the positions, launch searches from your refined
    position (blue button on lower left), and select from the image again
    (drop-down on the lower right).

When you are working with the selection tool, this: ![](img/endselect.png) appears next to the image toolbar
to remind you that you are in that mode. If you are refining
positions for a search, it will be ![](img/endsearchmarker.png). Either way, when you are done with the selection tool,
if your other actions don't turn off the selection tool, click on that
text to turn it off.

**⚠ Tips and Troubleshooting**

* The "region selection" tool also appears in the slightly different
  context of [interactive
  target refinement](othersearches.html#interactivetarget) in several other places in this tool, where it
  works in a very similar fashion.

---

### Footprints
The marker icon (![](img/marker.png)) has a drop-down menu with
several possible options:  
![](img/markeroptions.png)  
 Any
of the options with an arrow on the right can expand to additional
subsidiary choices, e.g.:  
![](img/markeroptionsp1.png)  
We now describe these various footprints.

For each of these choices, the markers appear initially in the center
of the loaded images. The first mouse click you make in any of the
images will move the marker to that location.

Each of these marker choices, when overlaid and/or selected as
'active', has a dash-dot square around it. If it is asymmetrical (most
of them are), it has an additional "appendage" and a red plus at the
center of the footprint:  
![](img/activeregion.png)  
These so-called "handles" allow you to resize and/or rotate the
marker, depending on the nature of the marker. These handles only
appear when the marker is selected as active; if you wait a few
seconds, they vanish.

**⚠ Tips and Troubleshooting**

* Some of these footprints are *large*. If you have a small
  image, some of these footprints will be larger than your image. Zoom
  out to see them, or find a larger image to use. If you overlay, say, a
  Nancy Grace Roman Space Telescope (formerly WFIRST) footprint on a
  2MASS Atlas FITS image, you may need to zoom out a considerable amount
  before you can see the Roman footprint. You will see the center
  indicator of the marker before you will see the Roman footprint
  itself.
* You can add multiple copies of the same marker using the [layers pop-up](#layers) (described generally above). From
  the layers pop-up, there is a link right under the 'angle' option that
  says "Add another [marker type]" -- click on that to get an additional
  marker of the same type. You can also add a label to the marker from
  the layers pop-up, or change its color.
* If you have many footprints on the same image, you may have
  trouble grabbing and moving footprints lower in the stack of layers on
  the image. For example, overlay footprint 1, then footprint 2, and you
  might have a hard time grabbing and rotating footprint 1 after
  footprint 2 has been added. The only workaround here is to use the
  layers pop-up (described generally above) to temporarily hide
  footprint 2, then move footprint 1, then restore footprint 2.
* If you have images of very different resolutions loaded (e.g.,
  IRAS and really anything else), sometimes it struggles to render the
  marker on each image. You may need to place markers on one image at a
  time. (Select "Color, stretch & overlays locked" to unlock it, and then place
  markers one image at a time.)

![](img/circlemarker.png) The first overlay choice (simply
called 'marker') is a red circle.

The remaining markers are all footprints from various telescopes:
Spitzer, SOFIA, HST, JWST, and Roman. HST, JWST, and Roman are derived
from information provided via MAST (see [http://gsss.stsci.edu/webservices/footprints/help.html
![](img/jumpout.jpg)](http://gsss.stsci.edu/webservices/footprints/help.html).) For Roman in
particular, they are pre-launch values.

![](img/iracfoot.png)**Spitzer/IRAC 3.6 and 4.5 micron
footprints.** These two footprints are placed separately
from each other. The footprint can be moved or rotated. Click and drag
the center of the footprint. A circle appears with four small circles
("handles") around it. Grab and drag the small circles to rotate it,
or drag the big circle to move it. Change the color, delete, or add
more copies of the IRAC footprints from the layers pop-up.

![](img/sofiafoot.png)**SOFIA footprints.**
Several different SOFIA footprints are available; the graphic here
shows a selection of them. The available footprints (all of which are
placed separately) are:

* FIFI-LS
  + Blue (50-120 microns)
  + Red (110-200 microns)
* FLITECAM
  + Imaging
  + Grism ABBA
  + Grism AB
* FORCAST
  + Imaging
  + Grism a
  + Grism b
* FPI+
* HAWC+
  + 53 microns (Band A), Total Intensity
  + 53 microns (Band A), Polarization
  + 89 microns (Band C), Total Intensity
  + 89 microns (Band C), Polarization
  + 154 microns (Band D), Total Intensity
  + 154 microns (Band D), Polarization
  + 214 microns (Band E), Total Intensity
  + 214 microns (Band E), Polarization

Change the color, delete, or add
more copies of the SOFIA footprints from the layers pop-up.

![](img/hst.png)**HST footprints.**
You can overlay the whole focal plane footprint, shown here, or
individual instrument footprints (NICMOS, WFPC2, ACS/WFC, ACS/HRC,
ACS/SBC, WFC3/UVIS, and WFC3/IR). Consult the [HST documentation ![](img/jumpout.jpg)](http://www.stsci.edu/hst/observatory/apertures) for specifics on which apertures are which. The
footprint can be moved or rotated. Click and drag the center of the
footprint. A circle appears with four small circles ("handles") around
it. Grab and drag the small circles to rotate it, or drag the big
circle to move it. **Note that** if you overlay the
footprint on a very small image, nothing will appear to have happened.
You need at least a 45 arcmin image to comfortably see the footprint.
Change the color, delete, or add more copies of the HST footprints from
the layers pop-up.

![](img/jwstall.png)**JWST footprints.**
You can overlay the whole focal plane footprint, shown here, or
individual instrument footprints (FGS, MIRI, NIRCAM, NIS, and NIRSPEC).
**Note that** if you overlay the footprint on a very
small image, nothing will appear to have happened. You need at least a
30 arcmin image to comfortably see the entire JWST focal plane. Please
consult the [JWST
documentation ![](img/jumpout.jpg)](http://www.stsci.edu/jwst/) for details
about the footprints. In all cases, if the footprint is 'active', a
circle near the middle of the footprint will appear with four small
circles ("handles") around it. Grab and drag the small circles to
rotate it, or drag the big circle to move it. Change the color,
delete, or add more copies of the footprints from the layers pop-up.

![](img/wfirst.png)**Nancy Grace Roman Space Telescope
focal plane footprint.** As above, the footprint can
be moved or rotated. Click and drag the boresight (the crosshairs),
which appears by default to the upper right of the array of squares.
A circle appears, centered on the boresight, with four small circles
("handles") around it. Grab and drag the small circles to rotate it,
or drag the big circle to move it. **Note that** if you
overlay the footprint on a very small image, nothing will appear to
have happened. You need at least a 60 arcmin image to comfortably see
the footprint, and even then you will probably have to click and drag
to see the entire footprint. Consult the [Roman
documentation ![](img/jumpout.jpg)](https://wfirst.ipac.caltech.edu/) for
specifics on the apertures. Change the color, delete, or add more
copies of the Roman footprint from the layers pop-up.

---

## Links found on page

- http://ds9.si.edu/doc/ref/region.html
- http://gsss.stsci.edu/webservices/footprints/help.html
- http://www.ivoa.net/documents/HiPS/
- http://www.stsci.edu/hst/observatory/apertures
- http://www.stsci.edu/jwst/
- https://en.wikipedia.org/wiki/FITS
- https://irsa.ipac.caltech.edu/docs/workspace/
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/catalogs.html
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/catalogs.html#hier
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/images.html
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/images.html#changing
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/images.html#coverage
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/images.html#fits
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/images.html#hips
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/images.html#moc
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/othersearches.html#generaltap
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/othersearches.html#interactivetarget
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/othersearches.html#nedcatalogs
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/overview.html#layout
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/plots.html
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/plots.html#saving
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/spectra.html
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/tables.html
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/tables.html#filters
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/tables.html#navigation
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/tables.html#save
- https://irsa.ipac.caltech.edu/onlinehelp/irsaviewer/irsaviewer/upload.html#catalogs
- https://ui.adsabs.harvard.edu/#abs/2004PASP..116..133L
- https://ui.adsabs.harvard.edu/#abs/2015A&A...578A.114F/abstract
- https://wfirst.ipac.caltech.edu/
- https://www.h-schmidt.net/FloatConverter/IEEE754.html
