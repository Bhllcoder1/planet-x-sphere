---
source: https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/searching.html
fetched: 2026-11-14
status: 200
---

SPHEREx Data Explorer at IRSA: Searching

SPHEREx Data Explorer at IRSA: Searching
----------------------------------------

This section is an overview of how to do a Spectral Image search in
the SPHEREx Data Explorer at IRSA. (Other tabs at the top, such as the
[Spectrophotometry Tool](sp.html), are covered elsewhere.)
To execute a Spectral Image search, after entering your search
parameters, click on the blue "Submit" or "Search" button to actually
launch the search.

*Contents of page/chapter:*  
+[Searching using a HiPS image](#hips)   
+[Spectral Image Position Search](#byPosition)   
+[Multi-Object Search](#byTable)   
+[Timing Constraints](#byTime)   
+[Spectral Constraints](#byWavelength)   
+[No Constraints](#noconstraints)   
+[Tools](#tools)   
+[Results](#results)

---

### Searching using a HiPS image

When you start a Spectral Image search, you have a [HiPS image](images.html#hips) loaded that takes up
most of the browser area (see screenshot below). Overlaid on top of
the HiPS image, there are colorful polygons indicating the sky
coverage for the data currently available in the archive. This
representation is also called a [multi-order coverage map (MOC)](images.html#moc), and
it's initially a bit confusing because nearly the entire sky has been
covered at least once (yellow polygons), the deep field coverage (red
polygons) is at the ecliptic poles, and the Galactic Center is
problematic so hasn't been released (the gap in the yellow is
apparent). There is an explicit legend in the top right of the default
view; you can toggle these layers off and on quickly from here. As of
November 2026, the HiPS image used by default in the background is the
multi-plane SPHEREx all-sky HiPS image.

Because of the way these MOCs are calculated and rendered, which is
on HEALPixels (the gray grid-like lines), the polygon 'cells' get
smaller and smaller near the edges of the coverage as it tries to
match the reality of the covered data. As you zoom in, the coverage
adapts and the edges of the coverage become smaller polygons to get
closer to the true coverage. The opacity of the rendered MOC changes
such that it becomes easier to see through it; once your entire field
of view is entirely in a region where there are data, the overlay
disappears to make it easier for you to place your target on top of
the background.

![](img/examplemocs.png)

You can click, pan, and zoom in the image, and even define
a region, to select a search location; many of the same visualization
tools are available for this image as for any other image in this
tool. ([Interacting with images](visualization.html) is
covered in another chapter, including [how to change the background HiPS
image](images.html#upperleft) and [how to scroll
through the planes of a multi-plane image](visualization.html#withinfile).) In order to get a more
complete view of the sky, you can collapse or expand the target
specification window in the lower left by clicking on the collapse
arrow in the upper right of the box.

**⚠ Tips and
Troubleshooting**

* The sky may look strange in this tool. SPHEREx is a polar
  orbiter, so the part of the sky that it observes every orbit (e.g.,
  the Deep Fields) "makes sense" (in terms of visualization) in ecliptic
  coordinates. The default HiPS representation is in galactic
  coordinates, and you can see the Galactic Plane in the HiPS image used
  for the background. You may be used to thinking about the sky in
  equatorial coordinates (RA/Dec), which is yet a third coordinate
  system. Moreover, all of these things are curved surfaces being
  represented on your flat screen, so distortion is inevitable. You can
  click and drag the HiPS image around, turn off overlays, add a grid
  overlay with coordinates in a variety of units, ask it to put
  north-up, ask it to show you things in ecliptic coordinates
  explicitly, add more MOCs from other missions, etc. See [the visualization chapter](visualization.html) for more
  detailed information about interacting with images. There is an
  example immediately below -- the HiPS image is from SPHEREx; the
  coordinates are ecliptic; the spectral images coverage has been
  changed to outlines (so only the Galactic Center is faintly visible in
  yellow outlines); the Deep Fields coverage is still there in red; the
  brown is planned Euclid coverage (which avoids both the Galactic and
  ecliptic planes).

![](img/examplemocs2b.png)

---

### Spectral Image Position Search

![](img/possearch.png)

Searching the archive is straightforward -- the most common search is
a search by position on the sky for a single-target cone search.

**Spatial type**
:   Single object or multiple object -- [searching a
    list of positions](#byTable) is covered below.

**Query Type**
:   You can specify exactly which kind of query type you would like --
    that is, what kind of relationship your search results have with your
    entered position or shape, and the subsequent options change
    accordingly, as follows:

    * *Observation boundary contains point* (default)
      + The next option is simply the target coordinates.
    * *Observation boundary contains shape*
      + The next options become "Cone Shape" or "Polygon Shape" -- you
        can enter just the [center position](#position) and the cone radius, or the list of
        vertices for a polygon. You can list between 3 and 15 vertices, where
        each vertex is given by a J2000 RA/Dec position pair, separated by
        commas. Because you are requesting that the images meeting your
        search criteria cover the entire region you are requesting, if you
        make the shape large, it's likely that you will be left with no images
        matching your criteria.
    * *Observation boundary is contained by shape*
      + The next options become "Cone Shape" or "Polygon Shape" -- you
        can enter just the [center position](#position) and the cone radius, or the list of
        vertices for a polygon. You can list between 3 and 15 vertices, where
        each vertex is given by a J2000 RA/Dec position pair, separated by
        commas. Because you are requesting that the images meeting your
        search criteria are entirely contained by the region you are requesting,
        if you don't make the shape large enough, it's likely that you will be
        left with no images matching your criteria.
    * *Observation boundary intersects shape*
      + The next options become "Cone Shape" or "Polygon Shape" -- you
        can enter just the [center position](#position) and the cone radius, or the list of
        vertices for a polygon. You can list between 3 and 15 vertices, where
        each vertex is given by a J2000 RA/Dec position pair, separated by
        commas.
    * *Central point (s\_ra, s\_dec) is contained by shape*
      + The next options become "Cone Shape" or "Polygon Shape" -- you
        can enter just the [center position](#position) and the cone radius, or the list of
        vertices for a polygon. You can list between 3 and 15 vertices, where
        each vertex is given by a J2000 RA/Dec position pair, separated by
        commas.

**Coordinates or Object Name**.
:   By default, it assumes you are searching on a single target. You
    may enter a target name, and have either NED-then-SIMBAD or
    SIMBAD-then-NED resolve the target name into coordinates. After it
    resolves the name, it will tell you which resolver service it used,
    and also what that service has for the object type:  
    ![](img/objecttype.png)

    Alternatively, you may enter coordinates directly. These coordinates
    can be in decimal degrees or in hh:mm:ss dd:mm:ss format, or
    Jhhmmss+ddmmss format. By default, it assumes you are working in J2000
    coordinates; you can also specify galactic, ecliptic, or B1950
    coordinates as follows:

    * '46.53, -0.251 gal' means 46.53, -0.251 degrees in galactic
      coordinates
    * '12.7, +4.3 ecl' means 12.7, +4.3 degrees in ecliptic coordinates
    * '19h17m 11d58m b1950' means 19h17m 11d58m in B1950 coordinates
    * a source name like 'J140320.67+542028.6' is parsed as 14h03m20.67s
      +54d20m28.6s.
    * a source name like 'G102.0360+59.7715' is parsed as 102.0360
      +59.7715 in galactic coordinates

    Examples are given below the text entry box before you start typing in
    the box.

    As you are completing a valid coordinate entry, the tool echoes
    back to you what it thinks you are entering. Look right below the box
    in which you are typing the coordinates to see it dynamically change.

**⚠ Tips and
Troubleshooting**

* Pick your units from the drop-down first, and
  then enter a number; if you enter a number and then select from the
  drop-down, it will convert your number from the old units to the new
  units. There are both upper and lower limits to your search radius;
  the tool will tell you if you request something too big or too small.
* You do not have to have a position search to execute a search. You
  can deselect the position checkbox and just search the entire archive
  with other constraints as described here, or none at all. Note that
  there are plenty of calibration files that are in the archive that
  have no position attached to them, so searching with position
  constraints automatically omits calibration files from the results.

**Title**
:   All of these searches will be managed in the [Job Monitor](downloads.html#jobmon). If you are submitting a
    lot of jobs, keeping track of which job is which in the list in the Job
    Monitor can be difficult. Using the "Title" field near the bottom of
    the search window, you can change the title by which the search will
    be listed in the Job Monitor. You don't have to change it from the
    default to be able to search, however. (Once you change it, though,
    all subsequent searches you make will still have that same title.)

Click on the blue "Search" button to launch the search.

---

### Multi-Object Search

![](img/searchscreen2.png)

You can submit a list of targets to search. When you select this
choice, you can select a table that is already loaded in the tool, or
you can upload a list of targets. The [chapter
on uploading](upload.html) covers file formats and syntax. In some cases, you
may need to help the tool understand the positions by specifying what
the position columns are -- if there are RA/Dec columns, it will
likely guess those properly.

You can also help it understand what the position columns are, like
this:  
![](img/searchscreen2b.png)

After you have uploaded your list of targets, the rest of the search
form looks the same as for the [single position
search](#byPosition), with all the same choices.

---

### Timing Constraints

These search options are generally of the same sort as you get for the
[ObsCore Timing
constraints](othersearches.html#tapSearches.exposure). Activate these options by checking the box to the left
of "Timing" on the search screen.

|  |  |
| --- | --- |
|  | This is the default option, where you want data overlapping a specified date range, where you can specify UTC or MJD times. |
|  | This is the alternate option, where you want data completed in the last x days (or other unit of time). |

Click on the blue "Search" button to launch the search.

**⚠ Tips and
Troubleshooting**

* SPHEREx launched on 11 March 2025 and began nominal operations on
  1 May 2025. There are no data in the archive earlier than that.
* SPHEREx data are scheduled to be delivered to IRSA on an
  approximately weekly basis. The most recent data in the archive could
  be up to 60 days old.
* You can launch a search that is unconstrained by position and
  constrained solely by time to, e.g., obtain the most recently observed
  data.

---

### Spectral Constraints

These search options are very similar to those you get for the [ObsCore Spectral Coverage
constraints](othersearches.html#tapSearches.wavelength). Activate these options by checking the box to the left
of "Spectral Coverage" on the search screen.

|  |  |
| --- | --- |
|  | This is the default option, where you can specify that you want data from a particular SPHEREx band. If you check the box asking for the spectral coverage constraints to be applied, then at least one band has to be selected. If you select just one band, then it will serve you only images from that band. |
|  | Here, you can request data containing a given wavelength. |
|  | This is the alternate option, where you want data overlapping a specified wavelength range. |

Click on the blue "Search" button to launch the search.

**⚠ Tips and
Troubleshooting**

* You can launch a search that is unconstrained by position and
  constrained solely by wavelength to, e.g., obtain all the data taken
  at a given wavelength, or combine it with a time constraint to get all
  the data taken within a certain time at a certain wavelength.

---

### No Constraints

If you unselect all of the checkboxes and ask for an unconstrained
Spectral Image search, you will return all of the files in the
archive, including calibration files. These kinds of results will
become more and more overwhelming in time, as more files are added to
the SPHEREx archive.

---

### Tools

The [Spectrophotometry Tool](sp.html) was the first
tool to be integrated into the SPHEREx Data Explorer. Its
initial screen looks very similar to the spectral image search screen,
but it's different, so it is covered in [its own
section](sp.html).

The [Mosaic Tool](mosaic.html) is the most recent
tool to be integrated into the SPHEREx Data Explorer. Its
initial screen looks very similar to the spectral image search screen,
but it's different, so it is covered in [its own
section](mosaic.html).

---

### Results

Results are described in detail in [another
section](results.html).

The [Visualization section](visualization.html) has
much more information about interacting with images.

The [Tables section](tables.html) has
much more information about interacting with tables in general.
The [Catalogs section](catalogs.html) has much more
information about searching for IRSA catalogs. You can do
[many other searches as well](othersearches.html).

When you load a table, you get an x-y plot displayed as well. See the
[Plots section](plots.html) for lots more information.

## Links found on page

- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/catalogs.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/downloads.html#jobmon
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/images.html#hips
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/images.html#moc
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/images.html#upperleft
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/mosaic.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/othersearches.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/othersearches.html#tapSearches.exposure
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/othersearches.html#tapSearches.wavelength
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/plots.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/results.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/sp.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/tables.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/upload.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/visualization.html
- https://irsa.ipac.caltech.edu/onlinehelp/spherex/spherex/visualization.html#withinfile
