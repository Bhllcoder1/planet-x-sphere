---
source: https://raw.githubusercontent.com/ericmandel/js9/master/js9.js
fetched: 2026-11-14
status: 200
---

/\*
\*
\* JS9: astronomical image display everywhere (December 10, 2012)
\*
\* Principals: Eric Mandel, Alexey Vikhlinin
\* Organization: Center for Astrophysics | Harvard & Smithsonian, Cambridge MA
\* Contact: emandel@cfa.harvard.edu
\*
\* Copyright (c) 2012 - 2022 Smithsonian Astrophysical Observatory
\*
\*/
/\*global JS9Prefs, JS9Inline, $, jQuery, fabric, io, sprintf, Astroem, dhtmlwindow, saveAs, Spinner, ResizeSensor, Jupyter, gaussBlur, ImageFilters, Plotly, tinycolor, regSelect \*/
"use strict";
// ensure Emscripten's Module object is available so we can pass properties
// (e.g. wasmBinary) in js9prefs.js and during JS9.init()
// (use var to add to global scope because it's how Emscripten does it)
var Module;
if( typeof Module !== "object" ){ Module = {}; }
// generate and expose JS9 module
// (use var to add to global scope for backward compatibility with previous ES5)
var JS9 = (function(){
// module header
const JS9 = {};
JS9.NAME = "JS9"; // The name of this namespace
JS9.VERSION = "3.9"; // The version of this namespace
JS9.COPYRIGHT = "Copyright (c) 2012-2024 Smithsonian Institution";
JS9.ABOUT = `JS9 ${JS9.VERSION}: astronomical image display everywhere\nEric Mandel, Alexey Vikhlinin\n${JS9.COPYRIGHT}`;
// internal defaults (not usually changed by users)
JS9.DEFID = "JS9"; // default JS9 display id
JS9.WIDTH = 512; // width of js9 canvas
JS9.HEIGHT = 512; // height of js9 canvas
JS9.ANON = "Anonymous"; // name to use for images with no name
JS9.PREFSFILE = "js9Prefs.json";// prefs file to load
JS9.WORKERFILE = "js9worker.js";// js9 web worker file to load
JS9.ZINDEX = 0; // z-index of image canvas: on bottom of js9
JS9.SHAPEZINDEX = 4; // base z-index of shape layers layers
JS9.MESSZINDEX = 80; // z-index of messages: above graphics
JS9.BTNZINDEX = 90; // z-index of buttons on top of plugin canvases
JS9.MENUZINDEX = 1000; // z-index of menus: always on top!
JS9.COLORSIZE = 1024; // size of contrast/biased color array
JS9.SCALESIZE = 16384; // size of scaled color array
JS9.INVSIZE = 1024; // size of inverse array
JS9.HISTSIZE = 16384; // size of histogram equalization array
JS9.INSTALLDIR=""; // prefix to get to js9 install directory
JS9.TOROOT=""; // prefix to get to data file from install
JS9.PLUGINS=""; // regexp list of plugins
JS9.LIGHTWIN = "dhtml"; // light window type: choice of dhtml
JS9.ANTIALIAS = false; // use anti-aliasing?
JS9.SCALEIREG = true; // scale interactive regions by zoom factor?
JS9.NOMOVE = 3; // number of pixels before we recognize movement
JS9.DBLCLICK0 = 5; // < millisec => same event
JS9.DBLCLICK = 300; // < millisec => double-click
JS9.TIMEOUT = 250; // millisec before assuming light window is up
JS9.SPINOUT = 250; // millisec before assuming spinner is up
JS9.WORKEROUT = 2000; // millisec before restarting worker socket
JS9.SUPERMENU = /^SUPERMENU\_/; // base of supermenu id
JS9.RESIZEDIST = 20; // size of rectangle defining resize handle
JS9.RESIZEFUDGE = 5; // fudge for webkit resize problems
JS9.RAWID0 = "raw0"; // default raw id
JS9.RAWIDX = "alt"; // default "alternate" raw id
JS9.IDFMT = " (%s)"; // format for light window id
JS9.MINZOOM = 0.125; // min zoom using scroll wheel
JS9.MAXZOOM = 32.0; // max zoom using scroll wheel
JS9.ADDZOOM = 0.1; // add/subtract amount per mouse wheel click
JS9.MODZOOM = 2; // skip factor with wheel to avoid pileup
JS9.DIRZOOM = 1; // sign (+/-) determines zoom direction
JS9.CHROMEFILEWARNING = true; // whether to alert chrome users about file URI
JS9.CLIPBOARDERROR = "the local clipboard (which only holds data copied from within JS9) does not contain any content. Were you trying to paste something copied outside JS9?";
JS9.CLIPBOARDERROR2 = "the local clipboard (which only holds data copied from within JS9) does not contain any regions";
JS9.URLEXP = /^(https?|ftp):\/\//; // url to determine a web page
JS9.WCSEXP = /^(fk4|fk5|icrs|galactic|ecliptic|image|physical|linear)$/;
JS9.REGSIZE = 0; // 0 -> cdelt, 1 -> ang sep (regions use #0)
JS9.useStatusbarDictionary = false;
// flag that is used to indicate that expandMacro should further use
// the statusbar dictionary to expand its output
// https://hacks.mozilla.org/2013/04/detecting-touch-its-the-why-not-the-how/
JS9.TOUCHSUPPORTED = ({}.hasOwnProperty.call(window, "ontouchstart") || (navigator.maxTouchPoints > 0) || (navigator.msMaxTouchPoints > 0));
// modified from:
// http://stackoverflow.com/questions/2400935/browser-detection-in-javascript
// https://stackoverflow.com/questions/58019463/how-to-detect-device-name-in-safari-on-ios-13-while-it-doesnt-show-the-correct
JS9.BROWSER = (function(){
const P = navigator.platform;
const N = navigator.appName;
const ua = navigator.userAgent;
const tem = ua.match(/version\/([.\d]+)/i);
let M = ua.match(/(opera|chrome|safari|firefox)\/?\s\*(\.?\d+(\.\d+)\*)/i);
if( M && tem !== null ){ M[2] = tem[1]; }
M = M? [M[1], M[2], P]: [N, navigator.appVersion,"-?", P];
M.push(/Android|webOS|iPhone|iPad|iPod|BlackBerry/i.test(ua) ||
(navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1));
return M;
}());
// convenience to allow plugins to deal with HiDPI ratio blurring
// http://stackoverflow.com/questions/15661339/how-do-i-fix-blurry-text-in-my-html5-canvas
JS9.PIXEL\_RATIO = (function(){
const ctx = document.createElement("canvas").getContext("2d"),
dpr = window.devicePixelRatio || 1,
bsr = ctx.webkitBackingStorePixelRatio ||
ctx.mozBackingStorePixelRatio ||
ctx.msBackingStorePixelRatio ||
ctx.oBackingStorePixelRatio ||
ctx.backingStorePixelRatio || 1;
return dpr / bsr;
}());
// global options
JS9.globalOpts = {
helperType: "none", // one of: sock.io, get, post, none
helperPort: 2718, // default port for node.js helper
requireHelper: false, // throw error if helper is not available?
allinoneHelper: false, // allow allinone to use helper?
processQueryParams: true, // process query parameters from url?
quietReturn: false, // should API return empty string or "OK"?
useWasm: true, // use WebAssembly if available?
transforms: ["flip", "rot90", "rotate"], // order for processing transforms
rotateRelative: false, // is setRotate() relative or absolute?
clickToFocus: false, // how to change focus on the display
winType: "light", // plugin window: "light" or "new"
sortPreloads: true, // sort preloads into original order after load?
defcolor: "#00FF00", // graphics color when all else fails
fits2fits: "never", // convert to repfile? always|never|size>x Mb
requireFits2Fits: false, // throw error if fits2fits can't be run?
localAccess: true, // access files locally, when available?
prependJS9Dir: true, // prepend $JS9\_DIR to relative fitsFile paths?
dataDir: null, // path to FITS data (def: use incoming path)
alerts: true, // set to false to turn off alerts
valposTarget: null, // target element for valpos updates
valposWidth: "medium", // small, medium, large
valposDCoords: false, // show display coords in valpos?
internalValPos: true, // a fancy info plugin can turns this off
internalContrastBias: true, // a fancy colorbar plugin can turns this off
containContrastBias: false, // contrast/bias only when mouse is in display?
arrowIncrement: 1, // how much to move a region using arrow keys
wcsCrosshair: false, // enable wcs crosshair matching?
localLoadFormat: "image", // current format when loading local files
remoteLoadMethod: "proxy", // proxy or cors when loading remote file
csvIncludeWCS: true, // does Get/SaveRegions(csv) include wcs info?
regWhichDefault: "auto", // "auto" => selected or all, "all" is all
regIncludeJSON: true, // does SaveRegions(reg) include the json info?
regIncludeComments: true, // does SaveRegions(reg) include the comments?
regListDCoords: false, // ListRegions(reg) list preserved disp coords?
regSaveDCoords: false, // SaveRegions(reg) save preserved disp coords?
regExpandDCoords: false, // ExpandMacro(reg) use preserved disp coords?
regCopyDCoords: true, // CopyRegions(reg) copy preserved disp coords?
regArrowCrosshair: true, // does move with arrow keys display crosshair?
regSaveWCS: "", // def wcs for saving regions
regSaveFormat: "reg", // def format for saving regions (reg,cvs,svg)
regSaveWhich1: "all", // def 'which' for saving regions (all,selected)
regSaveWhich2: "selected", // def 'which' for saving in configure dialog
regMenuCreate: true, // menu select a region creates it immediately
regMenuSelection: "circle", // region selected during last menu select
regToClipboard: false, // copy all region changes to pseudo-clipboard?
regGroupConflict: "skip", // group conflicts: error or skip
regConfigAddParens: true, // does the reg configure gui try to add parens?
regSyncTextColor: true, // sync region text color with main color?
regDisplay: "lightwin", // "lightwin" or "display"
reConfigSize: "medium", // "small", "medium"
htimeout: 10000, // connection timeout for the helper connect
lhtimeout: 10000, // connection timeout for local helper connect
ehtimeout: 500, // connection timeout for Electron connect
ehretries: 20, // connection retries Electron connect
xtimeout: 600000, // connection timeout for fetch data requests
extlist: "EVENTS STDEVT", // list of binary table extensions
imopts: "IMOPTS", // basename of FITS param containing json opts
imcmap: "IMCMAP", // basename of FITS param containing cmaps
table: {xdim: 4096, ydim: 4096, bin: 1, bitpix: 32},// image section size to extract from table
image: {xdim: 4096, ydim: 4096, bin: 1},// image section size (unlimited=0)
binMode: "s", // "s" (sum) or "a" (avg) pixels when binning
reprojSwitches: "", // Montage reproject switches
reprojectLimits: false, // internal: check for reprojection limits?
rotationCenter: "file", // "current" display center or "file" (CRPIX1,2)
runOnCR: true, // Run forms such as binning when  pressed?
clearImageMemory: "heap", // rm vfile: always|never|auto|noExt|noCube|size>x Mb heap=>free heap
helperProtocol: location.protocol, // http: or https:
reloadRefresh: false, // reload an image will refresh (or redisplay)?
reloadRefreshReg: true, // reloading regions file removes previous?
nextImageMask: false, // does nextImage() show active image masks?
panMouseThreshold: 1, // pixels mouse must move before we pan
panzoomRefreshLimit: 500, // # of shapes before avoiding refresh
panWithinDisplay: false, // keep panned image within the display?
pannerDirections: true, // display direction vectors in panner?
magnifierRegions: true, // display regions in magnifier?
editRegions: true, // double-click to edit regions?
svgBorder: true, // border around the display when saving to svg?
unremoveReg: 100, // how many removed regions to save
resetEmptyShapeId: false, // reset nshape counter if all shapes removed?
maxMemory: 2000000000, // max heap memory to allocate for a fits image
loadURL: "params/load.html",// location of param html file
corsURL: "params/loadcors.html", // location of param html file
proxyURL: "params/loadproxy.html", // location of param html file
loadProxy: false, // do we allow proxy load requests to server?
imsectionURL: "params/imsection.html", // location of param html file
postMessage: false, // allow communication through iframes?
localStorage: true, // use localStorage for session params?
waitType: "spinner", // "spinner" or "mouse"
spinColor: "#FF0000", // color of spinner
spinOpacity: 0.35, // opacity of spinner
resize: true, // allow resize of display?
resizeHandle: true, // add resize handle to display?
resizeRedisplay: true, // redisplay image while resizing?
logoDisplay: false, // show JS9 logo on each display?
logo: "images/js9logo.png", // show JS9 logo on each display?
lightWinPos: "center=1", // "left=n,top=m" offset from left,top of window
lightWinClose: "ask", // ask, close, move images when closing lightwin
fallbackDisplay: true, // displayMessage fallback to display window?
refreshDragDrop: true, // refresh on drag/drag and open file?
reduceMosaic: "js9", // "js9" or "shrink" ("js9" seems to be faster)
internalRegcnts: true, // make internal regcnts analysis available?
reduceRegcnts: true, // reduce image when doing counts in regions?
plot3d: {cube:"\*:\*:all", mode:"avg", areaunits:"pixels", color: "green"}, // plot3d options: avg/sum, pixels/arcsecs
imexamLineHeight: 1, // "height" of line region section
copyWcsPosFormat: "$ra $dec $sys", // format for copy wcs pos to clipboard
floatPrecision: 6, // precision for floatToString()
mouseActions: ["display value/position", "change contrast/bias", "pan the image"],// 0,1,2 mousepress
touchActions: ["display value/position", "change contrast/bias", "pan the image"],// 1,2,3 fingers
keyboardActions: {
a: "add last region selected in regions menu",
b: "toggle selected region: source/background",
c: "toggle crosshair",
d: "send selected region to back",
e: "toggle selected region: include/exclude",
"M-e": "edit selected region(s)",
i: "refresh image",
I: "display full image",
"M-i": "display selected cutouts",
"M-k": "toggle keyboard actions plugin",
l: "toggle active shape layers",
"M-l": "new JS9 light window",
m: "pan to mouse position",
"M-m": "toggle mouse/touch plugin",
"M-o": "open local file",
P: "paste regions from local clipboard",
p: "paste regions to current position",
"M-,": "toggle preferences plugin",
"M-p": "toggle preferences plugin",
r: "copy region(s) to clipboard",
s: "select region",
S: "select all regions",
"M-s": "toggle shape layers plugin",
u: "undo remove of region(s)",
U: "unselect all regions",
x: "flip image around x axis",
y: "flip image around y axis",
"9": "rotate image by 90 degrees",
"/": "copy wcs position to clipboard",
"?": "copy value and position to clipboard",
"0": "reset zoom",
"=": "zoom in",
"+": "zoom in",
"-": "zoom out",
"^": "raise region layer to top",
">": "display next image",
"<": "display previous image",
"delete": "remove selected region",
"leftArrow": "move region/position left",
"upArrow": "move region/position up",
"rightArrow": "move region/position right",
"downArrow": "move region/position down"
}, // keyboard actions
mousetouchZoom: false, // use mouse wheel, pinch to zoom?
mousetouchLimit: true, // limit zoom-out to size of image?
metaClickPan: true, // metaKey + click pans to mouse position?
// statusBar: "$mag; $scale($scaleclipping); $img(images/voyager/color\_$colormap.png) $colormap; $wcssys; $image", // status display
statusBar: "$colorbar; $colormap; $mag; $scale ($scalemin,$scalemax); $wcssys; $image0", // status display
statusBarDictionary: {},
toolbarTooltips: false, // display tooltips on toolbar?
updateTitlebar: true, // update titlebar when image changes?
centerDivs: ["JS9Menubar"], // divs which take part in JS9.Display.center()
resizeDivs: ["JS9Menubar", "JS9Colorbar", "JS9Toolbar", "JS9Statusbar"], // divs which take part in JS9.Display.resize()
pinchWait: 8, // number of events to wait before testing pinch
pinchThresh: 6, // threshold for pinch test
xeqPlugins: true, // execute plugin callbacks?
extendedPlugins: true, // enable extended plugin support?
intensivePlugins: false, // enable intensive plugin support?
dynamicSelect: "click", // dynamic plugins: "click", "move", or false
dynamicHighlight: true, // highlight dynamic selection
corsProxy: "https://js9.si.edu/cgi-bin/CORS-proxy.cgi", // CORS proxy
simbadProxy:"https://js9.si.edu/cgi-bin/simbad-proxy.cgi", // simbad proxy
cgiProxy: "https://js9.si.edu/cgi-bin/FITS-proxy.cgi", // CGI proxy
catalogs: {ras: ["RA", "\_RAJ2000", "RAJ2000"], // cols to search for ..
decs: ["Dec", "\_DEJ2000", "DEJ2000"],// when loading catalogs
shape: "circle", // object shape
color: "yellow", // object color
width: 7, // box object width
height: 7, // box object height
radius: 3.5, // circle object radius
r1: 5.0, // ellipse object r1
r2: 3.5, // ellipse object r2
wcssys: "ICRS", // wcs system
skip: "#\n", // skip # and blank lines
save: true, // save cat cols in shapes
tooltip: "$data.ra $data.dec"}, // tooltip format
topColormaps: ["grey", "heat", "cool", "turbo", "viridis", "magma", "sls", "red", "green", "blue"], // toplevel colormaps
infoBox: ["file", "object", "wcsfov", "wcscen", "wcspos", "impos", "physpos", "value", "regions", "progress"],
infoBoxResize: true, // is size based on wcs?
menuBar: ["file", "edit", "view", "zoom", "scale", "color", "region", "wcs", "analysis", "help"],
menubarStyle: "classic", // mac or classic
menuPosition: "right-5 bottom-5", // where menus pop up
menuClickEvent: "mouseup", // "click" or "mouseup"
menuSelected: "check", // selected option icon
menuImages: true, // show pngs in menu?
userMenus: false, // add user menus?
userMenuDivider: "   ", // divide before user menu
imagesFileSubmenu: 5, // how many images trigger a submenu?
toolBar: ["annulus", "box", "circle", "ellipse", "line", "polygon", "text", "zoom+", "zoom-", "zoom1", "zoomtofit"],
syncOps: ["alignment","colormap","contrastbias","flip","pan","regions","rotate", "rot90","scale","wcs","zoom"], // which ops are sync'ed?
syncReciprocate: true, // default value for reciprocal sync'ing
syncWCS: true, // default value for using WCS to sync
hiddenPluginDivs: [], // which static plugin divs start hidden
separate: {layout: "auto", leftMargin: 10, topMargin: 10}, // separate a display
imageTemplates: ".fits,.fts,.png,.jpg,.jpeg,.fz,.ftz,.gz", // templates for local images
wcsUnits: {FK4:"sexagesimal", FK5:"sexagesimal", ICRS:"sexagesimal",
galactic:"degrees", ecliptic:"degrees", linear:"degrees",
physical:"pixels", image:"pixels"}, // def units for wcs sys
wcsSetUpdatesDef: true, // does setWCSUnits() update the default?
wcsHlength: 256000, // hlength passed to astroem wcsninit()
regTemplates: ".reg", // templates for local region file input
sessionTemplates: ".ses,.js9ses",// templates for local session file input
colormapTemplates: ".cmap", // templates for local colormap file input
catalogTemplates: ".cat,.tab", // templates for local catalog file input
localTemplates: ".fits,.fts", // templates for local file access
controlsMatchRegion: false, // true, false, "corner" or "border"
internalColorPicker: true, // use HTML5 color picker, if available?
newWindowWidth: 530, // width of LoadWindow("new")
newWindowHeight: 625, // height of LoadWindow("new")
debug: 0 // debug level
};
// favorites are used in dialog boxes and control boxes
JS9.favorites = {
scales: ["linear", "log", "histeq"],
colormaps: ["cool", "heat", "viridis", "magma"],
regions: ["annulus", "box", "circle", "ellipse"],
wcs: ["FK5", "ICRS", "galactic:Galactic", "physical", "image"]
// you can specify a display string using a colon-separated string or array:
// wcs: ["FK5:fk5", ["ICRS","icrs"], "galactic", "physical", "image"]
};
// desktop (i.e. Electron.js) defaults
// always wrap access in if( window.electron ){}
JS9.desktopOpts = {
currentPath: true, // files relative to current dir?
sessionPath: true // session files relative to session file?
};
// image param defaults
JS9.imageOpts = {
inherit: false, // inherit props from previous image?
contrast: 1.0, // default color contrast
bias: 0.5, // default color bias
invert: false, // default colormap invert
exp: 1000, // default exp value for scaling
colormap: "grey", // default color map
overlay: true, // display png/jpeg overlay?
scale: "linear", // default scale algorithm
scaleclipping: "dataminmax", // "dataminmax", "zscale", or "user" (when scalemin, scalemax is supplied)
scalemin: Number.NaN, // default scale min is undefined
scalemax: Number.NaN, // default scale max is undefined
flip: "none", // default flip state
rot90: 0, // default 90 deg rotation state
rotate: 0, // default rotation state
zscalecontrast: 0.25, // default from ds9
zscalesamples: 600, // default from ds9
zscaleline: 120, // default from ds9
wcssys: "native", // default WCS sys
lcs: "physical", // default logical coordinate system
valpos: true, // whether to display value/position
sigma: "none", // gauss blur sigma or none
opacity: 1.0, // opacity between 0 and 1
alpha: 255, // alpha for image (but use opacity!)
nancolor: "#000000", // 6-digit #hex color for NaN values
nocolor: {red:0,green:0,blue:0,alpha:0} , // static color map no color
// xcen: 0, // default x center pos to pan to
// ycen: 0, // default y center pos to pan to
zoom: 1, // default zoom factor
zooms: 6, // how many zooms in each direction?
topZooms: 2, // how many zooms are at top level?
wcsalign: true, // align image using wcs after reproj?
rotationMode: "relative", // default: relative or absolute?
crosshair: false, // enable crosshair?
disable: [], // list of disabled core services
ltvbug: false, // add 0.5/ltm to image LTV values?
listonchange: false, // whether to list after a reg change
whichonchange: "selected" // which to list ("all" or "selected")
};
// allows regions opts (in Regions.opts) to be overridden via js9prefs.js
JS9.regionOpts = {};
// allows catalog opts (in Catalogs.opts) to be overridden via js9prefs.js
JS9.catalogOpts = {};
// allows crosshair opts (in Crosshair.opts) to be overridden via js9prefs.js
JS9.crosshairOpts = {};
// allows grid opts (in Grid.opts) to be overridden via js9prefs.js
JS9.gridOpts = {};
// allows emscripten opts (in Module) to be overridden via js9prefs.js
JS9.emscriptenOpts = {};
// allows fabric opts (in Fabric.opts) to be overridden via js9prefs.js
JS9.fabricOpts = {};
// socket.io options
JS9.socketioOpts = {
reconnection: true,
reconnectionDelay: 1000,
reconnectionDelayMax : 10000,
reconnectionAttempts: 100,
timeout: JS9.globalOpts.htimeout
};
// defaults for blending
JS9.blendOpts = {
active: true,
mode: "screen",
opacity: 1.0
};
// defaults for masking
JS9.maskOpts = {
active: false,
mode: "overlay", // "overlay", "mask", "opacity"
opacity: 1, // overlay opacity
vopacity: 0, // mask opacity
value: 0, // mask value
syncops: ["flip", "pan", "rot90", "zoom"],
invert: false
};
// defaults for analysis (macro expansion)
JS9.analOpts = {
// if this pattern is matched in stderr, throw a real error
epattern: /^(ERROR:[^\n]\*)\n/,
// location of datapath's param html file
dpathURL: "params/datapath.html",
// location of filepath's param html file
fpathURL: "params/filepath.html"
};
// light window opts
JS9.lightOpts = {
nclick: 0,
dhtml: {
topid: "#dhtmlwindowholder",
top: ".dhtmlwindow",
drag: ".drag-contentarea",
dragBar: ".drag-handle",
format: "width=%spx,height=%spx,resize=%s,scrolling=0",
textWin: "width=830px,height=400px,resize=1,scrolling=1",
// NB: dimensions are tied to .JS9Plot CSS params
plotWin: "width=830px,height=420px,resize=1,scrolling=1",
dpathWin: "width=830px,height=175px,resize=1,scrolling=1",
lcloseWin:"width=512px,height=190px,resize=1,scrolling=1",
paramWin: "width=830px,height=235px,resize=1,scrolling=1",
regWin0: "width=640px,height=130px,resize=1,scrolling=1",
regWin1: "width=640px,height=200px,resize=1,scrolling=1",
regWin: "width=640px,height=470px,resize=1,scrolling=1",
imageWin: "width=512px,height=598px,resize=1,scrolling=1",
lineWin: "width=400px,height=60px,resize=1,scrolling=1"
},
lcloseURL: "params/lightclose.html"
};
// colors for text messages
JS9.textColorOpts = {
regions: "#00FF00",
info: "#00FF00",
inimage: "#000000"
};
// help pages
JS9.helpOpts = {
user: {
heading: "JS9Help",
type: "help", url:"user.html",
title: "User Manual"
},
install: {
heading: "JS9Help",
type: "help", url:"install.html",
title: "Installing JS9"
},
webpage: {
heading: "JS9Help",
type: "help", url:"webpage.html",
title: "Adding JS9 to a Web Page"
},
yourdata: {
heading: "JS9Help",
type: "help", url:"yourdata.html",
title: "Adding Data to a Web Page"
},
localtasks: {
heading: "JS9Help",
type: "help", url:"localtasks.html",
title: "Adding Local Analysis Tasks and Plugins"
},
helper: {
heading: "JS9Help",
type: "help", url:"helper.html",
title: "Adding Server-side Analysis Tasks"
},
serverside: {
heading: "JS9Help",
type: "help", url:"serverside.html",
title: "Server-side Analysis with JS9"
},
publicapi: {
heading: "JS9Help",
type: "help", url:"publicapi.html",
title: "The JS9 Public API"
},
extmsg: {
heading: "JS9Help",
type: "help", url:"extmsg.html",
title: "External Messaging"
},
desktop: {
heading: "JS9Help",
type: "help", url:"desktop.html",
title: "JS9 on the Desktop"
},
python: {
heading: "JS9Help",
type: "help", url:"python.html",
title: "JS9 with Python and Jupyter"
},
archives: {
heading: "JS9Help",
type: "help", url:"archives.html",
title: "Accessing Data Archives"
},
preferences: {
heading: "JS9Help",
type: "help", url:"preferences.html",
title: "Setting Site Preferences"
},
regions: {
heading: "JS9Help",
type: "help", url:"regions.html",
title: "Regions Format"
},
changelog: {
heading: "JS9Help",
type: "help", url:"changelog.html",
title: "ChangeLog"
},
repfile: {
heading: "JS9Help",
type: "help", url:"repfile.html",
title: "Dealing with Large Files"
},
memory: {
heading: "JS9Help",
type: "help", url:"memory.html",
title: "Dealing with Memory Limitations"
},
issues: {
heading: "JS9Help",
type: "help", url:"knownissues.html",
title: "Known Issues"
},
security: {
heading: "JS9Help",
type: "help", url:"securityissues.html",
title: "Security Issues"
}
};
// containers for groups of JS9 objects
JS9.images = []; // array of current images
JS9.displays = []; // array of current display canvases
JS9.colormaps = []; // array of current colormaps
JS9.commands = []; // array of commands
JS9.plugins = []; // array of defined plugins
JS9.preloads = []; // array of images to preload
JS9.auxFiles = []; // array of auxiliary files
JS9.supermenus = []; // array containing supermenu instances
JS9.preloadwaiting = []; // array of images currently being preloaded
JS9.publics = {}; // object containing defined public API calls
JS9.helper = {}; // only one helper per page, please
JS9.fits = {}; // object holding FITS access routines
JS9.userOpts = {}; // object to hold localStorage opts
JS9.tmp = {}; // global temp area
// misc params
// list of scales in mkScaledCells
JS9.scales = ["linear", "log", "histeq", "power", "sqrt", "squared", "asinh", "sinh"];
// list of known wcs systems
JS9.wcssyss = ["FK4", "FK5", "ICRS", "galactic", "ecliptic",
"physical", "image", "native"];
// list of known wcs units
JS9.wcsunitss = ["degrees", "sexagesimal", "pixels"];
// list of known regions
JS9.regions = ["annulus", "box", "circle", "cross", "ellipse", "line", "point",
"polygon", "text"];
// known bugs and work-arounds
JS9.bugs = {};
// sometimes hiding the menu does not refresh the image properly
// JS9.bugs.hide\_menu = true;
// turned off: 6/30/16
JS9.bugs.hide\_menu = false;
// firefox does not repaint as needed (last checked FF 24.0 on 10/20/13)
if( (JS9.BROWSER[0] === "Firefox") && JS9.BROWSER[2].search(/Linux/) >=0 ){
JS9.bugs.firefox\_linux = true;
}
// webkit resize is not quite up to par
// if( (JS9.BROWSER[0] === "Chrome") || (JS9.BROWSER[0] === "Safari") ){
// only safari seems to need the extra border (4/18/20)
if( (JS9.BROWSER[0] === "Safari") ){
JS9.bugs.webkit\_resize = true;
}
// wasm broken in ios 11.2.2, 11.2.5 and on, fixed in 11.3beta1 (1/22/2018)
// see: https://github.com/kripken/emscripten/issues/6042
if( /iPad|iPhone|iPod/.test(navigator.platform) &&
/11\_2\_(?:[2-9])/.test(navigator.userAgent) ){
JS9.globalOpts.useWasm = false;
}
// iOS and presumably android has severe memory limits (05/2017)
// also force user to turn on crosshair, since it works with one finger
// also, iOS requires wider region dialog boxes to fit the buttons
if( JS9.BROWSER[3] ){
JS9.globalOpts.maxMemory = Math.min(JS9.globalOpts.maxMemory, 350000000);
JS9.globalOpts.table.xdim = 2048;
JS9.globalOpts.table.ydim = 2048;
JS9.globalOpts.image.xdim = 2048;
JS9.globalOpts.image.ydim = 2048;
JS9.imageOpts.crosshair = false;
JS9.globalOpts.reproj = {xdim: 2048, ydim: 2048};
JS9.lightOpts.dhtml.regWin0="width=660px,height=130px,resize=1,scrolling=1";
JS9.lightOpts.dhtml.regWin1="width=660px,height=200px,resize=1,scrolling=1";
JS9.lightOpts.dhtml.regWin="width=660px,height=470px,resize=1,scrolling=1";
}
// Jupyter doesn't seem to be able to load wasm (7/4/2018)
if( {}.hasOwnProperty.call(window, "Jupyter") ){
JS9.globalOpts.useWasm = false;
}
// JS9 desktop app using Electron.js
if( window.electron ){
// Emscripten mount point for local file system, based on hostname
if( window.electron.hostFS ){
JS9.hostFS = window.electron.hostFS;
}
// if multiple instances are running, turn off localStorage
if( window.electron.multiElectron ){
JS9.globalOpts.localStorage = false;
}
// once recommended by Electron, they removed this by 8.0.0
// still seems worthwhile, but let's put it here instead of passing it in
if( typeof window.eval === "function" ){
window.eval = function(){
throw new Error('For security reasons, Desktop JS9 does not support window.eval()');
}
}
// cmdlineOpts are opts used by the app to specify the command line
if( window.electron.cmdlineOpts ){
try{ JS9.cmdlineOpts = JSON.parse(window.electron.cmdlineOpts); }
catch(e){ delete JS9.cmdlineOpts; }
}
// guiOpts used mainly by Voyager
if( window.electron.guiOpts ){
// voyager mode?
JS9.Voyager=window.electron.guiOpts.voyager;
// change root to local dir for dialogs?
JS9.localRootDir=window.electron.guiOpts.localRootDir;
}
}
// ---------------------------------------------------------------------
// JS9 Image object to manage images
// ---------------------------------------------------------------------
JS9.Image = function(file, params, func){
let i, card, pars, nzoom, display, txeq, tval;
let localOpts = null;
let nhist = 0;
let ncomm = 0;
// called with current image context
const mkscale = (opts) => {
// do zscale, if necessary
opts = opts || {};
if( JS9.isNull(opts.scaleclipping) ){
if( this.params.scaleclipping === "zscale" ){
this.zscale(true);
} else if( this.params.scaleclipping === "zmax" ){
this.zscale("zmax");
}
} else {
if( opts.scaleclipping === "zscale" ){
this.zscale(true);
} else if( opts.scaleclipping === "zmax" ){
this.zscale("zmax");
}
}
if( JS9.notNull(opts.scalemin) ){
this.params.scalemin = opts.scalemin;
}
if( JS9.notNull(opts.scalemax) ){
this.params.scalemax = opts.scalemax;
}
};
// called with current image context
const finishUp = (func) => {
let i, s, topts, tkey, id, pre, waiting, plen, im;
const imopts = JS9.globalOpts.imopts;
const imcmap = JS9.globalOpts.imcmap;
const oalerts = JS9.globalOpts.alerts;
const rregexp = /(annulus|box|circle|ellipse|line|polygon|point|text) \*\(/;
// add to list of images
JS9.images.push(this);
// clear previous messages
this.display.clearMessage();
// if flip, rotate, rot90 opts were supplied, set transform
if( localOpts ){
if( JS9.notNull(localOpts.flip) ||
JS9.notNull(localOpts.rotate) ||
JS9.notNull(localOpts.rot90) ){
this.setTransform();
}
}
// display image, 2D graphics, etc.
this.displayImage("all", localOpts);
// notify the helper
this.notifyHelper();
// show regions layer
this.showShapeLayer("regions", true, {local: true});
if( localOpts ){
// pan, if necessary
if( (JS9.notNull(localOpts.x) && JS9.notNull(localOpts.y)) ||
(JS9.notNull(localOpts.px) && JS9.notNull(localOpts.py)) ||
(JS9.notNull(localOpts.ra) && JS9.notNull(localOpts.dec)) ||
(JS9.notNull(localOpts.wcs)) ){
this.setPan(localOpts);
}
// add regions, if necessary
if( localOpts.regions ){
if( localOpts.regions.match(rregexp) ){
this.addShapes("regions", localOpts.regions);
} else {
JS9.LoadRegions(localOpts.regions, {display:this.display});
}
}
}
// no alerts while processing imopts or cmaps
JS9.globalOpts.alerts = false;
// looks for imcmap (json-formatted colormap object) in FITS header
if( this.raw && this.raw.header && this.raw.header[imcmap] ){
// try to convert to object and set as image params
try{ topts = JSON.parse(this.raw.header[imcmap]); }
catch(e){ topts = null; }
if( topts ){
try{ JS9.AddColormap(topts); }
catch(e){ /\* empty \*/ }
}
}
// look for multi-line colormap (imcmap1, imcmap2, ...) in FITS header
tkey = `${imcmap}1`;
if( this.raw && this.raw.header && this.raw.header[tkey] ){
// gather up the json string
for(i=1, s=""; i<100; i++){
tkey = imcmap + String(i);
if( this.raw.header[tkey] ){
s += this.raw.header[tkey];
} else {
break;
}
}
// try to convert to object and set as image params
if( s ){
try{ topts = JSON.parse(s); }
catch(e){ topts = null; }
if( topts ){
try{ JS9.AddColormap(topts); }
catch(e){ /\* empty \*/ }
}
}
}
// looks for imopts (json-formatted image param object) in FITS header
if( this.raw && this.raw.header && this.raw.header[imopts] ){
// try to convert to object and set as image params
try{ topts = JSON.parse(this.raw.header[imopts]); }
catch(e){ topts = null; }
if( topts ){
try{ this.setParam("all", topts); }
catch(e){ /\* empty \*/ }
}
}
// look for multi-line imopts (imopts1, imopts2, ...) in FITS header
tkey = `${imopts}1`;
if( this.raw && this.raw.header && this.raw.header[tkey] ){
// gather up the json string
for(i=1, s=""; i<100; i++){
tkey = imopts + String(i);
if( this.raw.header[tkey] ){
s += this.raw.header[tkey];
} else {
break;
}
}
// try to convert to object and set as image params
if( s ){
try{ topts = JSON.parse(s); }
catch(e){ topts = null; }
if( topts ){
try{ this.setParam("all", topts); }
catch(e){ /\* empty \*/ }
}
}
}
// restore alerts
JS9.globalOpts.alerts = oalerts;
// plugin callbacks
this.xeqPlugins("image", "onimageload");
// load is complete
this.setStatus("load","complete");
// done loading, reset wait cursor
JS9.waiting(false);
// everything else is done so call onload func, if necessary
if( func ){
try{ JS9.xeqByName(func, window, this); }
catch(e){ JS9.error("in image onload callback", e, false); }
}
// might need to finish processing of preloads
if( JS9.preloadwaiting && JS9.preloadwaiting.length ){
plen = JS9.preloadwaiting.length;
id = this.proxyURL || this.file;
// flag that this preload is loaded
for(i=0, waiting=0; i {
let ai = 0, bi = 0;
for(i=0; i 0 ){
this.displayExtension("all");
}
};
// params can be an object containing local params, or the display string
if( params ){
if( typeof params === "object" ){
localOpts = params;
if( localOpts.display ){
display = localOpts.display;
}
} else {
display = params;
}
}
// make sure we have a valid display
if( !display ){
if( JS9.displays.length > 0 ){
display = JS9.displays[0].id;
} else {
display = JS9.DEFID;
}
}
// save url, if available
// it's an image
this.type = "image";
// set the display
this.display = JS9.lookupDisplay(display);
// initialize image params
this.params = {};
// region stack for saving removed regions
this.regstack = [];
// image-specific scratch space
this.tmp = {};
// current groups for each layer
this.groups = {};
// xeq callback for region changes?
this.params.xeqonchange = true;
// copy image parameters
this.params = $.extend(true, this.params, JS9.imageOpts, localOpts);
// inherit properties, if necessary
if( this.display.image ){
this.params.inherit = this.display.image.params.inherit;
if( this.params.inherit ){
this.params = $.extend(true,
this.params, this.display.image.params);
}
}
// (turn off plugin call, since we are not fully loaded)
txeq = JS9.globalOpts.xeqPlugins;
// save overlay (setting colormap turns it off)
tval = this.params.overlay;
JS9.globalOpts.xeqPlugins = false;
this.setColormap(this.params.colormap);
this.params.overlay = tval;
JS9.globalOpts.xeqPlugins = txeq;
// do we display?
this.displayMode = true;
// initialize click state
this.clickState = 0;
// initialize click in region
this.clickInRegion = false;
this.clickInLayer = null;
// no helper queried yet
this.queried = false;
// is this a proxy image?
if( localOpts && localOpts.proxyFile ){
this.proxyFile = localOpts.proxyFile;
}
// is there a proxy parent?
if( localOpts && localOpts.proxyParent ){
this.proxyParent = localOpts.proxyParent;
}
if( localOpts && localOpts.proxyURL ){
this.proxyURL = localOpts.proxyURL;
}
// was a "parent" FITS file specified?
if( localOpts && localOpts.parentFile ){
this.parentFile = localOpts.parentFile;
}
// was "parent" info specified?
if( localOpts && localOpts.parent ){
this.parent = localOpts.parent;
// convert card string to header
if( this.parent.cardstr && this.parent.ncard ){
this.parent.raw = {header: {}, history:[], comments: []};
for(i=0; i {
let ss;
if( (this.png.image.width !== this.raw.width) ||
(this.png.image.height !== this.raw.height) ){
ss = sprintf("rgb dims [%s,%s] don't match image [%s,%s]",
this.png.image.width,
this.png.image.height,
this.raw.width,
this.raw.height);
JS9.error(ss);
}
// store png data in an offscreen canvas
this.mkOffScreenCanvas();
// finish up
finishUp(func);
}).on("error", () => {
// done loading, reset wait cursor
JS9.waiting(false);
JS9.error(`could not load image: ${this.id}`);
});
// set src to download the display file
this.png.image.src = this.rgbFile;
} else {
// finish up
finishUp(func);
}
break;
default:
JS9.error(`unknown specification type for Load: ${typeof file}`);
break;
}
};
// return the image data in a relatively standard format
JS9.Image.prototype.getImageData = function(dflag){
let data = null;
const {xdim, ydim} = this.fileDimensions();
const atob64 = (a) => {
let i;
let s = '';
const bytes = new Uint8Array(a.buffer);
const len = bytes.byteLength;
for(i=0; i=0; i--){
tim = JS9.images[i];
if( this.display === tim.display ){
// display image, 2D graphics, etc.
tim.displayImage("all");
tim.refreshLayers();
// signal we're done
iscurrent = JS9.images.length;
break;
}
}
for(i=JS9.images.length-1; i>iscurrent; i--){
tim = JS9.images[i];
if( this.display === tim.display ){
// display image, 2D graphics, etc.
tim.displayImage("all");
tim.refreshLayers();
break;
}
}
}
};
// make offscreen canvas to hold RGB data from the png file
JS9.Image.prototype.mkOffScreenCanvas = function(){
// sanity check
if( !this.png || !this.png.image ){ return this; }
// offscreen object holds canvas into which we draw to get RGB values
// no need for jquery here, we only manipulate this via the canvas API
this.offscreen = {};
this.offscreen.canvas = document.createElement("canvas");
this.offscreen.canvas.setAttribute("width", this.png.image.width);
this.offscreen.canvas.setAttribute("height", this.png.image.height);
this.offscreen.context = this.offscreen.canvas.getContext("2d");
// turn off anti-aliasing
if( !JS9.ANTIALIAS ){
this.offscreen.context.imageSmoothingEnabled = false;
}
// draw the png to the offscreen canvas
this.offscreen.context.drawImage(this.png.image, 0, 0);
// read the RGBA data from offscreen
try{
this.offscreen.img = this.offscreen.context.getImageData(0, 0,
this.png.image.width, this.png.image.height);
} catch(e){
if( JS9.CHROMEFILEWARNING &&
(JS9.BROWSER[0] === "Chrome") && (document.domain === "") ){
alert("When using the file:// URI, Chrome must be run with the --allow-file-access-from-files switch to permit JS9 to access data.");
} else {
alert("could not read off-screen image data [same-origin policy violation?]");
}
}
// allow chaining
return this;
};
JS9.Image.prototype.useOffScreenCanvas = function(){
return this.offscreen && (this.rgbFile || this.params.overlay);
};
// initialize keywords for various logical coordinate systems
JS9.Image.prototype.initLCS = function(iheader){
let i, tval, rrot, frot, a, sina, cosa;
const arr = [[0,0,0], [0,0,0], [0,0,0]];
// header usually is raw header
const header = iheader || this.raw.header;
const cx = header.CRPIX1 || 1;
const cy = header.CRPIX2 || 1;
// seed rotation matrix and its inverse, if necessary
if( header.LCSROTA2 && header.CROTA2 ){
// screen rotation angle is reversed from FITS convention
a = -header.CROTA2 \* Math.PI / 180.0;
sina = Math.sin(a);
cosa = Math.cos(a);
frot = [[0,0,0], [0,0,0], [0,0,0]];
frot[0][0] = cosa;
frot[0][1] = -sina;
frot[0][2] = 0;
frot[1][0] = sina;
frot[1][1] = cosa;
frot[1][2] = 0;
rrot = JS9.invertMatrix3(frot);
if( !rrot ){
frot = null;
}
}
// physical coords
arr[0][0] = JS9.defNull(header.LTM1\_1, 1.0);
arr[1][0] = header.LTM2\_1 || 0.0;
arr[0][1] = header.LTM1\_2 || 0.0;
arr[1][1] = JS9.defNull(header.LTM2\_2, 1.0);
arr[2][0] = header.LTV1 || 0.0;
arr[2][1] = header.LTV2 || 0.0;
if( this.imtab === "image" && this.params.ltvbug ){
// There seems to be a tiny misalignment between wcs->image and
// physical->image when ltv is involved. No idea why, but the fix is:
// (set default to false after implementing rot90/flip 10/6/2019 ...
// on the fear this is doing more harm than good)
if( JS9.notNull(header.LTV1) ){
for(i=0; i<2; i++){
tval = Math.abs(arr[0][i]);
if( tval > 0 && tval < 1 ){ arr[2][0] += tval \* 0.5; }
}
}
if( JS9.notNull(header.LTV2) ){
for(i=0; i<2; i++){
tval = Math.abs(arr[1][i]);
if( tval > 0 && tval < 1 ){ arr[2][1] += tval \* 0.5; }
}
}
}
this.lcs.physical = {forward: $.extend(true, [], arr),
reverse: JS9.invertMatrix3(arr)};
if( this.lcs.physical.reverse ){
if( frot ){
this.lcs.physical.frot = $.extend(true, [], frot);
this.lcs.physical.rrot = $.extend(true, [], rrot);
// zero-index center
this.lcs.physical.cx = cx - arr[2][0] - 1;
this.lcs.physical.cy = cy - arr[2][1] - 1;
}
} else {
delete this.lcs.physical;
}
// detector coordinates
arr[0][0] = JS9.defNull(header.DTM1\_1, 1.0);
arr[1][0] = header.DTM2\_1 || 0.0;
arr[0][1] = header.DTM1\_2 || 0.0;
arr[1][1] = JS9.defNull(header.DTM2\_2, 1.0);
arr[2][0] = header.DTV1 || 0.0;
arr[2][1] = header.DTV2 || 0.0;
this.lcs.detector = {forward: $.extend(true, [], arr),
reverse: JS9.invertMatrix3(arr)};
if( this.lcs.detector.reverse ){
if( frot ){
this.lcs.detector.frot = $.extend(true, [], frot);
this.lcs.detector.rrot = $.extend(true, [], rrot);
// zero-index center
this.lcs.detector.cx = cx - arr[2][0] - 1;
this.lcs.detector.cy = cy - arr[2][1] - 1;
}
} else {
delete this.lcs.detector;
}
// amplifier coordinates
arr[0][0] = JS9.defNull(header.ATM1\_1, 1.0);
arr[1][0] = header.ATM2\_1 || 0.0;
arr[0][1] = header.ATM1\_2 || 0.0;
arr[1][1] = JS9.defNull(header.ATM2\_2, 1.0);
arr[2][0] = header.ATV1 || 0.0;
arr[2][1] = header.ATV2 || 0.0;
this.lcs.amplifier = {forward: $.extend(true, [], arr),
reverse: JS9.invertMatrix3(arr)};
if( this.lcs.amplifier.reverse ){
if( frot ){
this.lcs.amplifier.frot = $.extend(true, [], frot);
this.lcs.amplifier.rrot = $.extend(true, [], rrot);
// zero-index center
this.lcs.amplifier.cx = cx - arr[2][0] - 1;
this.lcs.amplifier.cy = cy - arr[2][1] - 1;
}
} else {
delete this.lcs.amplifier;
}
// reset lcs to image, if necessary
if( this.params && !this.lcs[this.params.lcs] ){
this.params.lcs = "image";
}
// set current, if not already done
if( this.params && !this.params.wcssys0 ){
this.setWCSSys("physical");
this.params.wcssys0 = this.params.lcs;
}
// save original physical
if( this.lcs.physical && !this.lcs.ophysical ){
this.lcs.ophysical = $.extend(true, {}, this.lcs.physical);
}
// allow chaining
return this;
};
// read input object and convert to image data
JS9.Image.prototype.mkRawDataFromHDU = function(obj, opts){
let i, s, ui, clen, hdu, pars, card, got, rlen, rmvfile, done, frheap;
let oraw, owidth, oheight, obitpix, owcssys, owcsunits;
let header, x1, y1, bin;
let nhist = 0;
let ncomm = 0;
opts = opts || {};
if( $.isArray(obj) || JS9.isTypedArray(obj) || obj instanceof ArrayBuffer ){
// flatten if necessary
if( $.isArray(obj[0]) ){
obj = obj.reduce( (a, b) => { return a.concat(b); });
}
// javascript array or typed array
hdu = {image: obj};
} else if( typeof obj === "object" ){
// fits object
hdu = obj;
} else {
JS9.error("unknown or missing input for HDU creation");
}
// allow image to be passed in data property
if( hdu.data && !hdu.image ){
hdu.image = hdu.data;
}
// better have the image ...
if( !hdu.image ){
JS9.error(`data missing from JS9 FITS object: ${JSON.stringify(hdu)}`);
}
// quick check for 1D images (in case naxis is defined)
if( hdu.naxis < 2 ){
JS9.error("can't image a FITS file with less than 2 dimensions");
}
// save old essential values, if possible (for use as defaults)
// free previous WCS, if possible
if( this.raw ){
oraw = this.raw;
owidth = this.raw.width;
oheight = this.raw.height;
obitpix = this.raw.bitpix;
owcssys = this.params.wcssys;
owcsunits = this.params.wcsunits;
this.freeWCS();
}
// initialize raws array?
this.raws = this.raws || [];
rlen = this.raws.length;
if( !rlen ){
// create object to hold raw data and add to raws array
this.raws.push({from: "hdu"});
// assign this object to the high-level raw data object
this.raw = this.raws[rlen];
// ignore rawid, this is the default raw data
this.raw.id = JS9.RAWID0;
} else {
opts.rawid = opts.rawid || JS9.RAWIDX;
// reuse raw object with the same id, after re-initializing it
got = 0;
for(i=0; i { return a.concat(b); });
}
// make the raw data: note in the case of a typed array coming from
// the Emscripten heap, this is a copy, so we can free the heap immediately
// (done below iff clearImageMemory contains the "heap" directive).
// I didn't realize new XXXArray(typedArray) makes a copy, but see:
// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global\_Objects/TypedArray
switch(this.raw.bitpix){
case 8:
this.raw.data = new Uint8Array(hdu.image);
break;
case 16:
this.raw.data = new Int16Array(hdu.image);
break;
case -16:
this.raw.data = new Uint16Array(hdu.image);
break;
case 32:
this.raw.data = new Int32Array(hdu.image);
break;
case -32:
this.raw.data = new Float32Array(hdu.image);
break;
case -64:
this.raw.data = new Float64Array(hdu.image);
break;
default:
JS9.error(`unsupported bitpix: ${this.raw.bitpix}`);
break;
}
// array of cards
this.raw.card = hdu.card;
// cfitsio returns these:
this.raw.cardstr = hdu.cardstr;
this.raw.ncard = hdu.ncard;
// look for header
if( hdu.head ){
this.raw.header = hdu.head;
} else if( this.raw.card ){
this.raw.header = {};
// make up header from array of raw cards
clen = this.raw.card.length;
for(i=0; i 0) ){
this.file = this.file.replace(/\[.\*\]/, "");
this.file += `[${opts.extnum}]`;
}
if( hdu.fits ){
if( opts.extname ){
hdu.fits.extname = opts.extname;
}
if( opts.extnum && (opts.extnum > 0) ){
hdu.fits.extnum = opts.extnum;
}
}
} else if( hdu.fits ){
if( hdu.fits.extname ){
this.file = this.file.replace(/\[.\*\]/, "");
this.file += `[${hdu.fits.extname}]`;
} else if( hdu.fits.extnum && (hdu.fits.extnum > 0) ){
this.file = this.file.replace(/\[.\*\]/, "");
this.file += `[${hdu.fits.extnum}]`;
}
} else if( this.raw.header ){
if( this.raw.header.EXTNAME ){
this.file = this.file.replace(/\[.\*\]/, "");
this.file += `[${this.raw.header.EXTNAME}]`;
}
}
}
// last chance: get it from the file
if( !this.id ){
// save id in case we have to change it for uniqueness
this.id0 = (this.parentFile||this.file).split("/").reverse()[0];
// get a unique id for this image
this.id = JS9.getImageID(this.id0, this.display.id, this);
}
// is this a proxy image?
if( opts.proxyFile ){
this.proxyFile = opts.proxyFile;
}
// save filter, if necessary
this.raw.filter = opts.filter || "";
this.raw.columns = opts.columns || "";
// image or table?
if( hdu.imtab ){
this.imtab = hdu.imtab;
} else {
this.imtab = hdu.table ? "table" : "image";
}
// also associate imtab with this raw layer
this.raw.imtab = this.imtab;
// min and max data values
if( hdu.dmin !== undefined && hdu.dmax !== undefined ){
// data min and max in object
this.dataminmax(hdu.dmin, hdu.dmax);
} else {
// calculate data min and max
this.dataminmax();
}
// object, telescope, instrument names
this.object = this.raw.header.OBJECT;
this.telescope = this.raw.header.TELESCOP;
this.instrument = this.raw.header.INSTRUME;
// see if binning was passed to us in opts, e.g. from external imsection
// (internally, it's ordinarily in hdu or hdu.table)
if( opts.binstr ){
try{ s = opts.binstr.split(/\s+/);
if( s && s.length === 2 ){
if( (this.imtab === "table") && hdu.table ){
hdu.table.bin = parseFloat(s[0]);
hdu.table.binMode = s[1];
} else {
hdu.bin = parseFloat(s[0]);
hdu.binMode = s[1];
}
}
}
catch(ignore){ /\* empty \*/ }
}
// reset binning properties, as necessary
if( (this.imtab === "table") && hdu.table ){
this.binning.bin = hdu.table.bin || 1;
} else if( hdu.bin ){
this.binning.bin = hdu.bin > 0 ? hdu.bin : 1 / Math.abs(hdu.bin);
} else {
this.binning.bin = 1;
}
// make sure obin matches bin for previous load of data
if( !oraw ){
this.binning.obin = this.binning.bin;
}
// reset the wcssys and wcsunits to previous, if necessary
if( owcssys ){
this.setWCSSys(owcssys);
}
if( owcsunits ){
this.setWCSUnits(owcsunits);
}
// init WCS, if necessary
if( oraw && oraw.header.CTYPE1 && oraw.header.CTYPE2 &&
this.raw.header.CTYPE1 && this.raw.header.CTYPE2 &&
(oraw.header.CTYPE1 !== this.raw.header.CTYPE1 ||
oraw.header.CTYPE2 !== this.raw.header.CTYPE2) ){
this.initWCS();
}
// save offscreen data if necessary
if( JS9.notNull(hdu.offscreen) ){
this.png = {image: hdu.offscreen};
this.mkOffScreenCanvas();
}
// re-init wcs
this.initWCS();
// init the logical coordinate system, if possible
this.initLCS();
// get hdu info, if possible
try{
if( opts.hdus ){
this.hdus = opts.hdus;
} else if( this.parentFile &&
JS9.helper.connected && JS9.helper.js9helper ){
obj = {
id: this.expandMacro("$id"),
cmd: this.expandMacro("js9Xeq listhdus $filename"),
image: this.file,
fits: this.parentFile,
rtype: "text"
};
JS9.helper.send("listhdus", obj, (obj) => {
if( obj.stderr ){
return;
}
if( obj.errcode ){
return;
}
if( obj.stdout ){
try{ this.hdus = JSON.parse(obj.stdout); }
catch(e) { this.hdus = null; }
}
});
} else if( this.raw.hdu && this.raw.hdu.fits ){
s = JS9.listhdu(this.raw.hdu.fits.vfile);
if( s ){
try{ this.hdus = JSON.parse(s); }
catch(e) { this.hdus = null; }
}
}
}
catch(ignore){ /\* empty \*/ }
// can we remove the virtual file?
if( this.raw.hdu && this.raw.hdu.fits && this.raw.hdu.fits.vfile ){
s = JS9.globalOpts.clearImageMemory;
if( s === false ){
s = ["never"];
} else if( s === true ){
s = ["always"];
} else {
s = s.toLowerCase().split(/[,>]/);
}
rmvfile = false;
frheap = false;
// all conditions must be met ...
for(i=0, done=false; i s[i+1]\*1000000 ){
rmvfile = true;
} else {
rmvfile = false;
done = true;
}
} else {
rmvfile = false;
done = true;
}
break;
default:
break;
}
}
// remove virtual file and/or heap space
if( rmvfile ){
if( JS9.DEBUG > 2 ){
JS9.log("removing underlying FITS vfile for %s: %s",
this.id, this.raw.hdu.fits.vfile);
}
JS9.cleanupFITSFile(this.raw, true);
} else if( frheap ){
if( JS9.DEBUG > 2 ){
JS9.log("freeing heap space for %s: %s",
this.id, this.raw.hdu.fits.vfile);
}
JS9.cleanupFITSFile(this.raw, false);
}
}
// plugin callbacks
this.xeqPlugins("image", "onrawdata");
// allow chaining
return this;
};
// store section information
JS9.Image.prototype.mkSection = function(...args){
let s, xtra;
const sect = this.rgb.sect;
const getWidth = (zoom) => {
let len;
let canvas = this.display.canvas;
if( this.params.transformAngle ){
len = Math.max(canvas.width, canvas.height);
return Math.min(this.raw.width \* zoom, len);
} else {
return Math.min(this.raw.width \* zoom, canvas.width);
}
};
const getHeight = (zoom) => {
let len;
let canvas = this.display.canvas;
if( this.params.transformAngle ){
len = Math.max(canvas.width, canvas.height);
return Math.min(this.raw.height \* zoom, len);
} else {
return Math.min(this.raw.height \* zoom, canvas.height);
}
};
// save zoom in case we are about to change it (regions have to be scaled)
sect.ozoom = sect.zoom;
// process args
switch(args.length){
case 0:
// no args: init to display central part of image
sect.xcen = Math.floor(this.raw.width/2);
sect.ycen = Math.floor(this.raw.height/2);
sect.width = getWidth(1);
sect.height = getHeight(1);
break;
case 1:
if( !JS9.isNumber(args[0]) ){
JS9.error(`invalid input for generating section: ${args[0]}`);
}
sect.zoom = parseFloat(args[0]);
sect.width = getWidth(sect.zoom);
sect.height = getHeight(sect.zoom);
break;
case 2:
// two args: x, y
if( !JS9.isNumber(args[0]) || !JS9.isNumber(args[1]) ){
JS9.error(`invalid input for generating section: ${args[0]} ${args[1]}`);
}
sect.xcen = parseFloat(args[0]);
sect.ycen = parseFloat(args[1]);
// reset width and height if there was a section offset
if( JS9.notNull(sect.ix) ){
sect.width = getWidth(sect.zoom);
}
if( JS9.notNull(sect.iy) ){
sect.height = getHeight(sect.zoom);
}
break;
case 3:
// three args: x, y, zoom
if( !JS9.isNumber(args[0]) ||
!JS9.isNumber(args[1]) ||
!JS9.isNumber(args[2]) ){
JS9.error(`invalid input for generating section: ${args[0]} ${args[1]} ${args[2]}`);
}
sect.xcen = parseFloat(args[0]);
sect.ycen = parseFloat(args[1]);
sect.zoom = parseFloat(args[2]);
sect.width = getWidth(sect.zoom);
sect.height = getHeight(sect.zoom);
break;
default:
break;
}
// assume no offset when displaying section
delete sect.ix;
delete sect.iy;
// calculate section limits from center and dimensions
sect.x0 = sect.xcen - (sect.width/(2\*sect.zoom));
sect.y0 = sect.ycen - (sect.height/(2\*sect.zoom));
sect.x1 = sect.xcen + (sect.width/(2\*sect.zoom));
sect.y1 = sect.ycen + (sect.height/(2\*sect.zoom));
// make sure we're within bounds while maintaining section dimensions
if( sect.x0 < 0 ){
if( JS9.globalOpts.panWithinDisplay ){
sect.x1 -= sect.x0;
} else {
sect.ix = sect.x0 \* sect.zoom;
}
sect.x0 = 0;
}
if( sect.y0 < 0 ){
if( JS9.globalOpts.panWithinDisplay ){
sect.y1 -= sect.y0;
} else {
sect.iy = sect.y0 \* sect.zoom;
}
sect.y0 = 0;
}
if( sect.x1 > this.raw.width ){
if( JS9.globalOpts.panWithinDisplay ){
sect.x0 -= (sect.x1 - this.raw.width);
} else {
sect.ix = (sect.x1 - this.raw.width) \* sect.zoom;
}
sect.x1 = this.raw.width;
}
if( sect.y1 > this.raw.height ){
if( JS9.globalOpts.panWithinDisplay ){
sect.y0 -= (sect.y1 - this.raw.height);
} else {
sect.iy = (sect.y1 - this.raw.height) \* sect.zoom;
}
sect.y1 = this.raw.height;
}
// for offset images, maybe display more of the image
if( sect.ix > 0 && sect.x0 > 0 ){
xtra = Math.min(sect.ix, sect.x0);
sect.x0 -= xtra;
sect.ix += xtra \* sect.zoom;
}
if( sect.ix < 0 && sect.x1 < this.raw.width ){
xtra = Math.min(this.raw.width - sect.x1, Math.abs(sect.ix));
sect.x1 += xtra;
sect.ix -= xtra \* sect.zoom;
}
if( sect.iy > 0 && sect.y0 > 0 ){
xtra = Math.min(sect.iy, sect.y0);
sect.y0 -= xtra;
sect.iy += xtra \* sect.zoom;
}
if( sect.iy < 0 && sect.y1 < this.raw.height ){
xtra = Math.min(this.raw.height - sect.y1, Math.abs(sect.iy));
sect.y1 += xtra;
sect.iy -= xtra \* sect.zoom;
}
// final check: make sure we're within bounds
sect.x0 = Math.max(0, sect.x0);
sect.x1 = Math.min(this.raw.width, sect.x1);
sect.y0 = Math.max(0, sect.y0);
sect.y1 = Math.min(this.raw.height, sect.y1);
// final integer dimensions
sect.x0 = Math.floor(sect.x0);
sect.y0 = Math.floor(sect.y0);
sect.x1 = Math.floor(sect.x1);
sect.y1 = Math.floor(sect.y1);
// final section limits: derive new width and height
sect.width = Math.ceil((sect.x1 - sect.x0) \* sect.zoom);
sect.height = Math.ceil((sect.y1 - sect.y0) \* sect.zoom);
// sanity check
if( sect.width <= 0 || sect.height <= 0 ){
s = sprintf("invalid image section: %s,%s [%s,%s, %s,%s, %s]",
sect.width, sect.height,
sect.x0, sect.y0, sect.x1, sect.y1,
sect.zoom);
JS9.error(s);
}
// put zoom back into params
this.params.zoom = sect.zoom;
// allow chaining
return this;
};
// create colormap index array from data values and specified data min/max
// from: tksao1.0/frame/frametruecolor.C
JS9.Image.prototype.mkColorData = function(){
let i, dd, idata, odata;
const ss = JS9.SCALESIZE;
const length = ss - 1;
const dmin = this.params.scalemin;
const dmax = this.params.scalemax;
const dlen = this.raw.width \* this.raw.height;
const diff = dmax - dmin;
const dval = length / diff;
// skip if colormap is static
if( this.cmapObj.type === "static" ){
return this;
}
// allocate array
if( !this.colorData || this.colorData.length < dlen ){
this.colorData = new Int32Array(dlen);
}
// Important note 7/13/2020:
// Chrome 83.0.4103.116 was taking either 4ms ... or 2+ seconds to do
// this loop on a 2048x2048 int image (casa.fits in js9debug.html).
// Replacing this.raw.data and this.colorData with local variables seems
// to fix this slowdown. omg ...
idata = this.raw.data;
odata = this.colorData;
// for each raw value, calculate lookup offset into scaled array
for(i=0; i= dmax ){
odata[i] = ss - 1;
} else {
odata[i] = Math.floor(((dd - dmin) \* dval) + 0.5);
}
}
// allow chaining
return this;
};
// generate colorcells array from current colormap
// from: tksao1.0/colorbar/colorbar.C
JS9.Image.prototype.calcContrastBias = function(i){
let r, result;
let bias = this.params.bias;
const cs = JS9.COLORSIZE;
const contrast = this.params.contrast;
// check for (close to) default
if( ((bias - 0.5) < 0.0001) && ((contrast - 1.0) < 0.0001) ){
return i;
}
// map i to range of 0 to 1.0
// shift by bias (if invert, bias = 1 - bias)
// multiply by contrast
// shift to center of region
// expand back to number of dynamic colors
if( this.params.invert ){
bias = 1 - bias;
}
r = Math.floor((((i / cs) - bias) \* contrast + 0.5) \* cs);
if( r < 0 ){
result = 0;
} else if( r >= cs ){
result = cs - 1;
} else {
result = r;
}
return result;
};
// generate colorcells array from current colormap
// from: tksao1.0/colorbar/colorbartruecolor.C
JS9.Image.prototype.mkColorCells = function(){
let i, j, idx;
const cs = JS9.COLORSIZE;
// skip if colormap is static
if( this.cmapObj.type === "static" ){
return this;
}
// allocate array for color cells
if( !this.colorCells ){
this.colorCells = [];
}
// fill in colorcells
for(i=0; i {
let i, k, int1, int2;
const hex\_alphabets = "0123456789ABCDEF";
const value = [];
//Remove the "#" char - if there is one.
if(hex.charAt(0) === "#"){
hex = hex.slice(1);
}
hex = hex.toUpperCase();
for(i=0, k=0; i<6; i+=2, k++){
int1 = hex\_alphabets.indexOf(hex.charAt(i));
int2 = hex\_alphabets.indexOf(hex.charAt(i+1));
value[k] = (int1 \* 16) + int2;
}
return value;
};
// sanity check
if( !this.colorCells ){ return this; }
// skip if colormap is static
if( this.cmapObj.type === "static" ){ return this; }
// allocate array for scaled cells
if( !this.psColors ){
this.psColors = [];
// value for NaN
this.psColors[NaN] = hex2num(this.params.nancolor);
}
// and the inverse array for colorbar ticks
if( !this.psInverse ){
this.psInverse = [];
// value for NaN
this.psInverse[NaN] = 0;
}
// delta for scaling
dd = this.params.scalemax - this.params.scalemin;
low = this.params.scalemin;
// apply the appropriate scale algorithm
switch(this.params.scale){
case "linear":
// scaled cells
for(ii=0; ii= cs ){
ll = cs - 1;
}
this.psColors[ii] = this.colorCells[ll];
}
// inverse
for(ii=0; ii= cs ){
ll = cs - 1;
}
this.psColors[ii] = this.colorCells[ll];
}
// inverse
for(ii=0; ii= cs ){
ll = cs - 1;
}
this.psColors[ii] = this.colorCells[ll];
}
// inverse
for(ii=0; ii= cs ){
ll = cs - 1;
}
this.psColors[ii] = this.colorCells[ll];
}
// inverse
for(ii=0; ii= cs ){
ll = cs - 1;
}
this.psColors[ii] = this.colorCells[ll];
}
// inverse
for(ii=0; ii= cs ){
ll = cs - 1;
}
this.psColors[ii] = this.colorCells[ll];
}
// inverse
for(ii=0; ii= dmin) && (data[ii] <= dmax) ){
jj = Math.floor((data[ii] - dmin) / diff \* hh + 0.5);
if( jj < hh ){
pdf[jj] += 1;
}
}
}
// get average
for(ii=0; ii= avg) && (color < hh) ){
bin -= avg;
color++;
}
}
dval = (hh - 1) /hh;
while( ii < hh ){
this.hist[ii++] = dval;
}
}
// scaled cells
for(ii=0; ii vv ){
break;
}
}
aa = jj / hh;
this.psInverse[ii] = aa \* diff + dmin;
}
break;
default:
JS9.error(`unknown scale '${this.params.scale}'`);
}
// allow chaining
return this;
};
// create RGB image from scaled colorCells
// sort of from: tksao1.0/frame/truecolor.c, but not really
JS9.Image.prototype.mkRGBImage = function(){
let rgb, sect, img, xrgb, yrgb, wrgb, hrgb, rgbimg, ctx;
let inc, zinc, xIn, yIn, xOut, yOut, xOutIdx, yOutIdx, yZoom, xZoom, cobj;
let idx, odx, odxmax, ridx, gidx, bidx, mim, mimg;
let yLen, zx, zy, zyLen, mopacity, cmopacity, val;
let alpha, alpha1, alpha2, alphafloor, alphafloorvalue, curalpha;
let domask = false;
let doalphafloor = false;
let rthis = null;
let gthis = null;
let bthis = null;
let dorgb = false;
let mimmask = false;
let mimopacity = false;
let mimoverlay = false;
let cached = [];
// sanity check
if( !this.rgb ){ return this; }
// image handles for RGB mode
if( this.display.rgb.active &&
((this === this.display.rgb.rim) ||
(this === this.display.rgb.gim) ||
(this === this.display.rgb.bim)) ){
dorgb = true;
if( this.display.rgb.rim ){
rthis = this.display.rgb.rim;
}
if( this.display.rgb.gim ){
gthis = this.display.rgb.gim;
}
if( this.display.rgb.bim ){
bthis = this.display.rgb.bim;
}
}
ctx = this.display.context;
rgb = this.rgb;
sect = rgb.sect;
// supply your own mkRGBImage call (black-magic, used by smart-x)
if( this.MakeRGBImage && typeof this.MakeRGBImage === "function" ){
if( this.MakeRGBImage() ){
return this;
}
}
// backward-compatibility with v1.7
if( this.MakePrimaryImage && typeof this.MakePrimaryImage === "function" ){
if( this.MakePrimaryImage() ){
return this;
}
}
// if we have an RGB file or image overlay, use offsreen RGB colors
if( this.useOffScreenCanvas() ){
wrgb = sect.width / sect.zoom;
hrgb = sect.height / sect.zoom;
xrgb = sect.x0;
yrgb = (this.offscreen.canvas.height - 1) - (sect.y0 + hrgb);
rgbimg = this.offscreen.context.getImageData(xrgb, yrgb, wrgb, hrgb);
if( sect.zoom === 1 ){
// for unzoomed data, we can grab the RGB pixels directly
rgb.img = rgbimg;
} else {
// for zoomed data, we have to replicate each RGB pixel
rgb.img = ctx.createImageData(sect.width, sect.height);
img = rgb.img;
odx = 0;
for(yIn=0, yOut=0; yIn mask value
if( JS9.notNull(this.params.opacity) ){
alpha2 = this.params.opacity \* 255;
} else {
alpha2 = 255;
}
// reverse mask alphas, if necessary
if( this.mask.invert ){
alpha = alpha1;
alpha1 = alpha2;
alpha2 = alpha;
}
} else if( this.mask.mode === "opacity" ){
// opacity mode: alpha = mask value 0 to 1 \* 255
mimopacity = true;
} else if( this.mask.mode === "overlay" ){
// overlay mode: non-zero mask value is blended with image value
mimoverlay = true;
mimg = mim.rgb.img;
if( JS9.isNull(this.mask.opacity) ){
this.mask.opacity = 1;
}
}
} else if( JS9.notNull(this.params.flooropacity) && !dorgb && !domask ){
// flooropacity: image pixels <= floor value use floor opacity
// can't do this with rgb mode because we have 3 different data values
alphafloor = this.params.flooropacity \* 255;
alphafloorvalue = this.params.floorvalue;
doalphafloor = true;
}
// index into scaled data using previously calc'ed data value to get RGB
// reverse y lines
odx = 0;
inc = Math.max(1, Math.floor(1/sect.zoom));
zinc = sect.zoom \* inc;
for(yIn=Math.floor(sect.y1-1), yOut=0; yIn>=sect.y0; yIn -= inc, yOut++){
yLen = yIn \* this.raw.width;
yOutIdx = yOut \* zinc;
for(xIn=Math.floor(sect.x0), xOut=0; xIn this.mask.value ){
alpha = alpha2;
} else {
alpha = alpha1;
}
} else if( mimopacity ){
// opacity mode: masked value is the opacity
alpha = mim.raw.data[yLen +xIn] \* 255;
}
if( dorgb ){
// rgb mode: up to three indexes
ridx = rthis ? rthis.colorData[yLen + xIn] : 0;
gidx = gthis ? gthis.colorData[yLen + xIn] : 0;
bidx = bthis ? bthis.colorData[yLen + xIn] : 0;
if( JS9.isNull(ridx) || JS9.isNull(gidx) || JS9.isNull(bidx) ){
this.display.rgb.active = false;
JS9.error("RGB images are incompatible. Turning off RGB mode.", "", false);
this.mkRGBImage();
return this;
}
} else if( !this.staticObj ){
// ordinary case: one index
idx = this.colorData[yLen + xIn];
}
// current alpha to use in most cases
curalpha = alpha;
// use alpha min when data val is below threshold?
if( doalphafloor && this.raw.data[yLen + xIn] <= alphafloorvalue ){
curalpha = alphafloor;
}
xOutIdx = xOut \* zinc;
for(yZoom=0; yZoom {
let context, canvas;
if( !this.offscreenRGB ){
canvas = document.createElement("canvas");
context = canvas.getContext("2d");
// turn off anti-aliasing
if( !JS9.ANTIALIAS ){
context.imageSmoothingEnabled = false;
}
this.offscreenRGB = {canvas, context};
}
this.offscreenRGB.canvas.width= img.width;
this.offscreenRGB.canvas.height = img.height;
this.offscreenRGB.context.putImageData(img, 0, 0);
return this.offscreenRGB.canvas;
};
// opts is optional
opts = opts || {};
// reproject: if reproj wcs header exists, save it for alignment
if( this.rawDataLayer() === "reproject" && opts.wcsim ){
this.wcsim = opts.wcsim;
this.wcsim.isawcsim = true;
}
// get display offsets
this.calcDisplayOffsets(true);
// save context
ctx.save();
// do we need to apply blend mode parameters
if( opts.opacity !== undefined ){ ctx.globalAlpha = opts.opacity; }
if( opts.blend !== undefined ){ ctx.globalCompositeOperation = opts.blend; }
// do we need to apply the canvas transform?
if( this.params.transform ){
// this is the transform matrix
m = this.params.transform;
// translate origin to center of display
w2 = this.display.width / 2;
h2 = this.display.height / 2;
ctx.translate(w2, h2);
// set new transform
ctx.transform(m[0][0], m[0][1], m[1][0], m[1][1], m[2][0], m[2][1]);
// translate back to 0, 0
ctx.translate(-w2, -h2);
}
// display image
ctx.drawImage(img2canvas(rgb.img), this.ix, this.iy);
// restore original context
ctx.restore();
// allow chaining
return this;
};
// display image, with pre and post processing based on comma-separated string
// of options:
// colors: generate colorData
// scaled: generate colorCells and scaledCells
// rgb: generate RGB image (happens automatically for any of the above)
// display: displlay image (always done)
// plugins: execute plugin callbacks
// all: colors,scaled,rgb,display,plugins
JS9.Image.prototype.displayImage = function(imode, opts){
let i, im, bopts, obj;
let nblend = 0;
const allmode = "colors,scaled,rgb,display,plugins";
const blends = [];
const mode = {};
// eslint-disable-next-line no-unused-vars
const modeFunc = (element, index, array) => {
const el = element.trim();
mode[el] = true;
// each step implies the next ones
switch(el){
case "colors":
mode.scaled = true;
mode.rgb = true;
break;
case "scaled":
mode.rgb = true;
break;
}
};
// special checks for displayMode setting
if( imode === false ){
this.displayMode = false;
return this;
}
if( imode === true ){
this.displayMode = true;
imode = "all";
}
// if displayMode is false, just return
if( !this.displayMode ){
return this;
}
// did we just pass the opts params?
if( typeof imode === "object" ){
opts = imode;
imode = null;
}
if( !imode ){
imode = "rgb";
} else if( imode === "all" ){
imode = allmode;
mode.notify = true;
} else if( imode === "rgbonly" ){
imode = "rgb,nodisplay";
mode.notify = true;
} else if( imode === "display" ){
mode.notify = true;
}
// get mode as elements in an object
imode.split(",").forEach(modeFunc);
// by default display the image again (unless nodisplay is set)
mode.display = true;
// and always call plugins
mode.plugins = true;
// if we have an RGB file or image overlay, skip some steps
if( this.useOffScreenCanvas() ){
mode.colors = false;
mode.scaled = false;
}
// opts are optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse displayImage opts: ${opts}`, e); }
}
// do we need to blend?
if( this.display.blendMode && (opts.blendMode !== false) ){
for(i=0; i=0; i--){
im = blends[i];
im.mkRGBImage();
}
}
}
// if we explicitly don't display, return here;
if( mode.nodisplay ){
return this;
}
// display image on screen
if( mode.display ){
// clear image
this.display.context.clear();
if( nblend ){
// pre-calculate image offsets in case of zoom changed for an image
// which acts as wcsim for another blended image ... in case the
// blended image gets loaded before the wcs image ... messy!
for(i=blends.length-1; i>=0; i--){
blends[i].calcDisplayOffsets(false);
}
for(i=blends.length-1; i>=0; i--){
im = blends[i];
// display the image using blend characteristics
bopts = {wcsim: opts.wcsim,
blend: im.blend.mode, opacity: im.blend.opacity};
im.putImage(bopts);
if( im === this ){
// display layers for this image
im.displayShapeLayers();
}
}
} else {
// display the image
this.putImage(opts);
// display layers for this image
this.displayShapeLayers();
}
// mark this image as being in this display
this.display.image = this;
// now this is the displayed image, we can add delayed shapes
while( this.delayedShapes && this.delayedShapes.length ){
this.tmp.syncRunning = true;
obj = this.delayedShapes.shift();
switch(obj.mode){
case "add":
this.addShapes(obj.layer, obj.shape, obj.opts);
break;
case "change":
this.changeShapes(obj.layer, obj.shape, obj.opts);
break;
}
delete this.tmp.syncRunning;
}
delete this.delayedShapes;
}
// post-processing
// plugin callbacks
this.xeqPlugins("image", "onimagedisplay");
// allow chaining
return this;
};
// refresh data for an existing image
// input obj is a fits object, array, typed array, etc.
JS9.Image.prototype.refreshImage = function(obj, opts){
let s, arr, ozoom, ora, odec, olpos, ipos, func;
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse refreshImage opts: ${opts}`, e); }
}
// no obj or obj is a string, this is a load with refresh turned on
if( !obj || typeof obj === "string" ){
if( opts.onrefresh ){
opts.onload = opts.onrefresh;
delete opts.onrefresh;
}
opts.refresh = this;
// for file:// uri, we can use the FITS pathname, where possible
if( !document.domain ){
s = obj || this.fitsFile || this.file;
} else {
// else use the url path relative to the web page
s = obj || this.file;
}
JS9.Load(s, opts, {display: this.display});
return;
}
// check for refresh func
opts.rawid = opts.rawid || JS9.RAWID0;
// allow explicit specification of a func, for backward-compatibility
if( typeof opts === "function" ){
func = opts;
opts = {onrefresh: func};
}
if( !opts.onrefresh && JS9.imageOpts.onrefresh ){
// use global onrefresh, if possible
opts.onrefresh = JS9.imageOpts.onrefresh;
}
// save section center if it's not to be reset
if( !opts.resetSection ){
// always save logical coords
olpos = this.imageToLogicalPos({x: this.rgb.sect.xcen,
y: this.rgb.sect.ycen});
// save wcs pos, if available
if( this.validWCS() ){
s = JS9.pix2wcs(this.raw.wcs,
this.rgb.sect.xcen, this.rgb.sect.ycen);
arr = s.trim().split(/\s+/);
ora = JS9.saostrtod(arr[0]);
if( JS9.isHMS(this.params.wcssys) ){
ora \*= 15.0;
}
odec = JS9.saostrtod(arr[1]);
}
}
ozoom = this.rgb.sect.zoom;
// save old binning
this.binning.obin = this.binning.bin;
// generate new data
this.mkRawDataFromHDU(obj, opts);
// reset or restore section?
if( opts.resetSection ){
// reset section
this.mkSection();
this.mkSection(ozoom);
} else {
// try to restore section using saved coords
if( this.validWCS() && JS9.notNull(ora) && JS9.notNull(odec) ){
arr = JS9.wcs2pix(this.raw.wcs, ora, odec).trim().split(/ +/);
ipos = {x: parseFloat(arr[0]), y: parseFloat(arr[1])};
} else {
ipos = this.logicalToImagePos({x: olpos.x, y: olpos.y});
}
// but if the image position off the new image ...
if( ipos.x > 0 && ipos.x < this.raw.width &&
ipos.y > 0 && ipos.y < this.raw.height ){
this.mkSection(ipos.x, ipos.y, ozoom);
} else {
// ... just reset the section
this.mkSection();
this.mkSection(ozoom);
}
}
// display new image data with old section
this.displayImage("colors", opts);
// redo flip and rot
this.reFlipRot();
// notify the helper
this.notifyHelper();
// update shape layers if necessary
if( opts.refreshRegions ||
opts.resetSection ||
(this.binning.obin !== this.binning.bin) ){
this.refreshLayers();
// update region values
this.updateShapes("regions", "all", "binning");
}
// plugin callbacks
this.xeqPlugins("image", "onimagerefresh");
// all done
JS9.waiting(false);
// everything else is done so call refresh func, if necessary
if( opts.onrefresh ){
try{ JS9.xeqByName(opts.onrefresh, window, this); }
catch(e){ JS9.error("in image refresh callback", e); }
}
// allow chaining
return this;
};
// fileDimensions: get dimensions of "original" file
// this is the hackiest routine in the JS9 module
// why is it so hard???
JS9.Image.prototype.fileDimensions = function(){
let xdim, ydim;
if( this.parent && this.parent.raw.header.XTENSION !== "BINTABLE" ){
if( this.parent.raw.header.TABDIM1 ){
xdim = this.parent.raw.header.TABDIM1;
} else {
xdim = this.parent.raw.header.NAXIS1;
}
if( this.parent.raw.header.TABDIM2 ){
ydim = this.parent.raw.header.TABDIM2;
} else {
ydim = this.parent.raw.header.NAXIS2;
}
} else {
if( this.raw.header.TABDIM1 ){
xdim = this.raw.header.TABDIM1;
} else {
xdim = this.raw.header.NAXIS1;
}
if( this.raw.header.TABDIM2 ){
ydim = this.raw.header.TABDIM2;
} else {
ydim = this.raw.header.NAXIS2;
}
}
return {xdim, ydim};
};
/\*
maybePhysicalToImage: the second hackiest routine in the JS9 module!
The physical position defined by LTM/LTV is not always the file position,
For example, if the file foo.fits was created from another file:
funimage somefile.fits'[\*,\*,2]' foo.fits
its LTM/LTV keywords will referring to the parent, instead of itself.
In such a case, we want to convert physical position to the image position
of the physical file.
This situation is signalled by the presence of a parent lcs object.
This routine is used to display sections and the binning.js plugin.
\*/
JS9.Image.prototype.maybePhysicalToImage = function(pos){
let lpos, ipos, npos;
if( this.imtab === "image" &&
this.parent && this.parent.lcs && pos.x && pos.y ){
lpos = {x: pos.x, y: pos.y};
// call is used because this.parent is not an image object
ipos = JS9.Image.prototype.logicalToImagePos.call(this.parent, lpos,
"ophysical");
npos = {x: Math.floor(ipos.x+0.5), y: Math.floor(ipos.y+0.5)};
}
return npos;
};
// extract and display a section of an image, with table filtering
JS9.Image.prototype.displaySection = function(opts, func){
let s, oproxy, hdu, from, obj, oreg, nim, topts;
let ipos, lpos, npos, tbin, arr, sect;
const getval3 = (val1, val2, val3) => {
let res;
if( !JS9.isNull(val1) ){
res = val1;
} else if( !JS9.isNull(val2) ){
res = val2;
}
return res || val3;
};
// convert region to section (cen and dim)
const reg2sect = (xreg) => {
let i, xdim, ydim, xcen, ycen, npos;
let xx = 0;
let yy = 0;
let minx = 1000000;
let maxx = 0;
let miny = 1000000;
let maxy = 0;
const shape = xreg.shape;
// use physical coords object, if possible
if( !this.parentFile && xreg.lcs ){
xreg = xreg.lcs
xcen = xreg.x;
ycen = xreg.y;
// beware of problems with physical coords not tied to the file
npos = this.maybePhysicalToImage({x: xcen, y: ycen});
if( npos ){
xcen = npos.x;
ycen = npos.y;
}
} else {
xcen = xreg.x;
ycen = xreg.y;
}
switch( shape ){
case "annulus":
xdim = xreg.radii[xreg.radii.length-1]\*2;
ydim = xreg.radii[xreg.radii.length-1]\*2;
break;
case "box":
xdim = xreg.width;
ydim = xreg.height;
break;
case "circle":
xdim = xreg.radius\*2;
ydim = xreg.radius\*2;
break;
case "cross":
xdim = xreg.width;
ydim = xreg.height;
break;
case "ellipse":
xdim = xreg.r1\*2;
ydim = xreg.r2\*2;
break;
case "polygon":
case "line":
for ( i=0; i < xreg.pts.length; i++ ) {
xx += xreg.pts[i].x;
yy += xreg.pts[i].y;
if ( xreg.pts[i].x > maxx ) { maxx = xreg.pts[i].x; }
if ( xreg.pts[i].x < minx ) { minx = xreg.pts[i].x; }
if ( xreg.pts[i].y > maxy ) { maxy = xreg.pts[i].y; }
if ( xreg.pts[i].y < miny ) { miny = xreg.pts[i].y; }
}
xreg.x = xx/xreg.pts.length;
xreg.y = yy/xreg.pts.length;
if( xreg.shape === "line" && xreg.pts.length === 2 ){
xdim = Math.sqrt(((xreg.pts[0].x - xreg.pts[1].x) \*
(xreg.pts[0].x - xreg.pts[1].x)) +
((xreg.pts[0].y - xreg.pts[1].y) \*
(xreg.pts[0].y - xreg.pts[1].y)));
ydim = 1;
} else {
xdim = maxx - minx;
ydim = maxy - miny;
}
break;
case "text":
xdim = 10;
ydim = 10;
break;
default:
break;
}
return({xcen: xcen, ycen: ycen, xdim: xdim, ydim: ydim});
};
// main display routine
const disp = (hdu, opts) => {
let tim, did, arr;
let ss = "";
// make a copy of opts so we can change it
topts = $.extend(true, {}, opts || {});
if( JS9.isNull(topts.refreshRegions) ){
topts.refreshRegions = true;
}
if( JS9.isNull(topts.resetSection) ){
topts.resetSection = true;
}
// start the waiting!
if( topts.waiting !== false ){
JS9.waiting(true, this.display);
}
// the id might have changed if we changed extensions
if( hdu.fits.extname ){
ss = `[${hdu.fits.extname}]`;
} else if( hdu.fits.extnum && hdu.fits.extnum > 0 ){
ss = `[${hdu.fits.extnum}]`;
} else if( this.parent ){
if( this.parent.extname ){
ss = `[${this.parent.extname}]`;
} else if( this.parent.extnum && this.parent.extnum > 0 ){
ss = `[${this.parent.extnum}]`;
}
}
// change id and file if extension changed
if( ss ){
if( !topts.id ){
topts.id = this.id.replace(/\[.\*\]/,"") + ss;
}
// NB: this was removed in v2.3 ... why? ... added back in v2.5
if( !topts.file ){
topts.file = this.file.replace(/\[.\*\]/,"") + ss;
}
}
if( topts.separate ){
// display section as a separate image in the specified display
delete topts.xcen;
delete topts.ycen;
if( typeof topts.separate === "string" ){
arr = topts.separate.split(":");
switch(arr.length){
case 1:
did = arr[0];
break;
default:
did = arr[0];
topts.id = arr[1];
break;
}
// make sure we can find the display
topts.display = JS9.lookupDisplay(did);
} else {
topts.display = this.display;
}
// lame attempt to get to original parentFile
if( from === "parentFile" && this.fitsFile ){
tim = JS9.lookupImage(this.fitsFile);
if( tim && tim.parentFile ){
topts.parentFile = tim.parentFile;
} else {
topts.parentFile = this.fitsFile;
}
}
// save current regions (before displaying new image)
oreg = this.listRegions("all", {mode: 1,
includedcoords: true,
ignoreignore: true,
saveediting: true,
savewcsconfig: true,
sortids: false,
saveid: true});
// func to perform when image is loaded
func = topts.ondisplaysection || topts.onrefresh || func;
// set up new and display new image
nim = new JS9.Image(hdu, topts, func);
// reset obin to be bin, since new images have no previous bin
nim.binning.obin = nim.binning.bin;
// add regions to new image
if( oreg && topts.refreshRegions !== false ){
nim.addShapes("regions", oreg, {restoreid: true});
}
// redo flip and rot
this.reFlipRot();
// set status of new image
nim.setStatus("displaySection", "complete");
} else if( typeof topts.refresh === "string" ){
// refresh the image in the specified display
delete topts.xcen;
delete topts.ycen;
arr = topts.refresh.split(":");
switch(arr.length){
case 1:
did = arr[0];
break;
default:
did = arr[0];
topts.id = arr[1];
break;
}
// make sure we can find the display
topts.display = JS9.lookupDisplay(did);
if( topts.display.image ){
topts.rawid = this.raw.id;
// func to perform when image is refreshed
topts.onrefresh = topts.ondisplaysection ||
topts.onrefresh || func;
// refresh the image with the new hdu
topts.display.image.refreshImage(hdu, topts);
} else {
// no image in the specified display, so make a new one
// lame attempt to get to original parentFile
if( from === "parentFile" && this.fitsFile ){
tim = JS9.lookupImage(this.fitsFile);
if( tim && tim.parentFile ){
topts.parentFile = tim.parentFile;
} else {
topts.parentFile = this.fitsFile;
}
}
// save current regions (before displaying new image)
oreg = this.listRegions("all", {mode: 1,
includedcoords: true,
ignoreignore: true,
saveediting: true,
savewcsconfig: true,
sortids: false,
saveid: true});
// func to perform when image is loaded
func = topts.ondisplaysection || topts.onrefresh || func;
// set up new and display new image
nim = new JS9.Image(hdu, topts, func);
// reset obin to be bin, since new images have no previous bin
nim.binning.obin = nim.binning.bin;
// add regions to new image
if( oreg ){
nim.addShapes("regions", oreg, {restoreid: true});
}
// redo flip and rot
this.reFlipRot();
}
} else {
// this is the default behavior for displaySection:
// refresh the image in the current display
topts.rawid = this.raw.id;
// func to perform when image is refreshed
topts.onrefresh = topts.ondisplaysection || topts.onrefresh || func;
// refresh the current image with the new hdu
this.refreshImage(hdu, topts);
}
// set status of old image
this.setStatus("displaySection", "complete");
// done waiting
JS9.waiting(false);
};
// sanity check
if( !this.raw || !this.raw.hdu || !this.raw.hdu.fits ){
JS9.error("invalid image for displaySection");
}
// opts is optional
opts = opts || {};
// special case: if opts is "full", display full image
if( opts === "full" ){
const {xdim, ydim} = this.fileDimensions();
opts = {xdim: xdim, ydim: ydim, xcen: 0, ycen: 0};
} else if( opts === "selected" ){
this.\_selectShapes("regions", "selected", null, (obj) => {
topts = reg2sect(obj.pub);
topts.from = "virtualFile";
topts.separate = true;
topts.refreshRegions = false;
topts.resetSection = true;
this.displaySection(topts, func);
});
return;
} else if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse displaySection opts: ${opts}`, e); }
}
// cube column
opts.cubecol = opts.cubecol || "";
if( opts.cubecol ){
// string containing filename and indication that this is a cube
s = this.file
.split("/")
.reverse()[0]
.replace(/\[.\*\]/,"")
.replace(".fits", `\_cube\_${opts.cubecol}.fits`)
.replace(/\.ftz$/, `\_cube\_${opts.cubecol}.fits`)
.replace(/\.gz$/, "")
.replace(/\.bz2$/, "")
.replace(/:/g, "\_");
// name of virtual file we will create
if( !opts.file ){
opts.file = s;
}
// and its id
if( !opts.id ){
opts.id = s;
}
// unless explicitly set to false, separate is set to true
if( opts.separate !== false ){
opts.separate = true;
}
}
if( opts.separate ){
// if we are generating a separate image, copy the hdu
hdu = $.extend(true, {}, this.raw.hdu);
} else {
// if we are replacing the current image, use the hdu directly
hdu = this.raw.hdu;
}
// from where do we extract the section?
from = opts.from;
if( !from ){
if( this.parentFile && JS9.helper.connected && JS9.helper.js9helper ){
// we will be processing a parent file to get the section
from = "parentFile";
} else {
// we will be processing a virtual file to get the section
from = "virtualFile";
}
}
// get previous values to use as defaults
if( this.imtab === "table" && hdu.table ){
// tables are easy: all the previous values should be present
sect = hdu.table;
} else {
sect = {};
// start with bin from hdu
sect.bin = hdu.bin || 1;
// images are a bit more difficult
// hack: if a parent file was used to make this image,
// calculate binning from its LTM/TLV parameters
if( from === "parentFile" &&
this.raw.header && JS9.notNull(this.raw.header.LTM1\_1) ){
sect.bin = 1 / Math.abs(this.raw.header.LTM1\_1);
}
// get image center from raw data
ipos = {x: this.raw.width / 2, y: this.raw.height / 2};
// convert to physical (file) coords
lpos = this.imageToLogicalPos(ipos);
// sect.xcen = Math.floor(lpos.x + 0.5);
// sect.ycen = Math.floor(lpos.y + 0.5);
sect.xcen = Math.floor(lpos.x + 0.5\*(sect.bin-1));
sect.ycen = Math.floor(lpos.y + 0.5\*(sect.bin-1));
npos = this.maybePhysicalToImage({x: sect.xcen, y: sect.ycen});
if( npos ){
sect.xcen = npos.x;
sect.ycen = npos.y;
}
sect.xdim = Math.floor(hdu.naxis1 \* sect.bin);
sect.ydim = Math.floor(hdu.naxis2 \* sect.bin);
sect.filter = this.raw.filter || "";
sect.columns = this.raw.columns || "";
}
// allow binning relative to current, e.g., \*2, /4, +1, -3
if( typeof opts.bin === "string" ){
// save and remove mode flag
if( opts.bin.match(/[as]$/) ){
opts.binMode = opts.bin.slice(-1);
opts.bin = opts.bin.slice(0, -1);
}
// temp binning value
tbin = sect.bin || this.binning.bin;
switch( opts.bin.charAt(0) ){
case "\*":
case "x":
case "X":
opts.bin = tbin \* parseFloat(opts.bin.slice(1));
break;
case "/":
opts.bin = tbin / parseFloat(opts.bin.slice(1));
break;
case "i":
case "I":
opts.bin = tbin \* 2;
break;
case "o":
case "O":
opts.bin = tbin / 2;
break;
default:
if( JS9.isNumber(opts.bin) ){
opts.bin = parseFloat(opts.bin);
} else {
JS9.error(`invalid bin for displaySection: ${opts.bin}`);
}
break;
}
}
// now we can make sure opts has sensible defaults
opts.xcen = getval3(opts.xcen, sect.xcen, 0);
opts.ycen = getval3(opts.ycen, sect.ycen, 0);
switch(this.imtab){
case "table":
opts.xdim = getval3(opts.xdim, sect.xdim, JS9.fits.options.table.xdim);
opts.ydim = getval3(opts.ydim, sect.ydim, JS9.fits.options.table.ydim);
opts.bin = getval3(opts.bin, sect.bin, JS9.fits.options.table.bin);
break;
default:
opts.xdim = getval3(opts.xdim, sect.xdim, JS9.fits.options.image.xdim);
opts.ydim = getval3(opts.ydim, sect.ydim, JS9.fits.options.image.ydim);
opts.bin = getval3(opts.bin, sect.bin, JS9.fits.options.image.bin);
break;
}
opts.binMode = getval3(opts.binMode, sect.binMode, JS9.globalOpts.binMode);
// final checks on binning
// handle string bin, possibly containing explicit binMode
if( typeof opts.bin === "string" ){
if( opts.bin.match(/[as]$/) ){
opts.binMode = opts.bin.slice(-1);
}
opts.bin = parseFloat(opts.bin);
}
// sanity check: we need a bin
if( !opts.bin ){
opts.bin = 1;
}
// sanity check: fractional bin must be 1/n for images
if( this.imtab === "image" && opts.bin > 0 && opts.bin < 1 ){
opts.bin = 1.0 / Math.floor((1.0 / opts.bin) + 0.5);
}
// filter
opts.filter = getval3(opts.filter, sect.filter, "");
// save the filter, if necessary
this.raw.filter = opts.filter || "";
// columns
opts.columns = getval3(opts.columns, sect.columns, "");
// save the columns, if necessary
this.raw.columns = opts.columns || "";
// start the waiting!
if( opts.waiting !== false ){
JS9.waiting(true, this.display);
}
// set status
this.setStatus("displaySection", "processing");
// ... start a timeout to allow the wait spinner to get started
window.setTimeout(() => {
// get image section
switch(from){
case "parentFile":
oproxy = this.proxyFile;
// parentFile: image sect. from external parent file of cur file
// arr is for runAnalysis, remove opts for later processing
arr = [];
arr.push({name: "xcen", value: opts.xcen});
delete opts.xcen;
arr.push({name: "ycen", value: opts.ycen});
delete opts.ycen;
arr.push({name: "xdim", value: opts.xdim});
arr.push({name: "ydim", value: opts.ydim});
// load entire image section
if( opts.xdim !== undefined ){ opts.xdim = 0; }
if( opts.ydim !== undefined ){ opts.ydim = 0; }
// recombine bin and binMode, if necessary
if( opts.binMode ){
opts.bin = `${opts.bin}${opts.binMode}`;
delete opts.binMode;
}
arr.push({name: "bin", value: opts.bin});
delete opts.bin;
s = `${opts.filter||""}@@${opts.cols||""}`;
arr.push({name: "filter", value: s});
// hack: pass filter and columns along to reach binning plugin
// delete opts.filter;
// get image section from external file
arr.push({name: "slice", value: opts.slice||""});
delete opts.slice;
obj = {id: this.expandMacro("$id"),
image: this.file,
fits: this.parentFile,
rtype: "text"};
obj.cmd = `js9Xeq imsection ${this.parentFile}`;
// if we are changing the extension, replace the old extension
// with the new one
if( opts.extension ){
obj.cmd = obj.cmd.replace(/\[.\*\]/,"");
obj.cmd += `[${opts.extension}]`;
delete opts.extension;
}
obj.cmd += this.expandMacro(" $xdim@$xcen,$ydim@$ycen,$bin $filter $slice", arr);
JS9.helper.send("imsection", obj, (r) => {
let obj, jobj, rarr, f, pf;
if( typeof r === "object" ){
// with socketio, we get an object
obj = r;
} else {
// with cgi, we just get a text string
if( r.search(JS9.analOpts.epattern) >=0 ){
obj = {stderr: r};
} else {
obj = {stdout: r};
}
}
if( obj.stderr ){
JS9.error(obj.stderr);
return;
}
if( obj.errcode ){
JS9.error(`in displaySection: ${obj.errcode}`);
return;
}
// output is file and possibly parentFile
rarr = obj.stdout.split(/\n/);
// file
f = JS9.cleanPath(rarr[0]);
// relative path: add install dir prefix
if( f.charAt(0) !== "/" ){
f = JS9.InstallDir(f);
}
// this is the proxy file (meaning: delete it on close)
opts.proxyFile = f;
// remove oproxy file if not the same as the current file
if( oproxy && (oproxy !== opts.proxyFile) ){
this.removeProxyFile(oproxy);
}
// json fits info
if( rarr[1] ){
try{
jobj = JSON.parse(rarr[1]);
}
catch(ignore){
JS9.log("couldn't parse imsection as JSON: %s", f);
jobj = null;
}
if( jobj ){
opts.extname = jobj.extname;
opts.extnum = jobj.extnum;
opts.hdus = jobj.hdus;
opts.binstr = jobj.binstr;
opts.parent = jobj;
}
}
// look for parentFile (path relative to helper, not install)
if( rarr[2] ){
pf = JS9.cleanPath(rarr[2]);
opts.parentFile = pf;
}
// retrieve and display newly created image section file
JS9.fetchURL(f, f, opts, (result) => {
// cleanup previous FITS file support, if necessary
// do this before we handle the new FITS file, or else
// we end up with a memory leak in the emscripten heap!
JS9.cleanupFITSFile(this.raw, true);
// start the waiting!
if( opts.waiting !== false ){
JS9.waiting(true, this.display);
}
// process the newly retrieved data as FITS
JS9.fits.handleFITSFile(result, opts, disp);
});
});
break;
case "virtualFile":
// cleanup previous FITS file support, if necessary
// do this before we handle the new FITS file, or else
// we end up with a memory leak in the emscripten heap!
JS9.cleanupFITSFile(this.raw, false);
// extract image section from current virtual file
JS9.getFITSImage(hdu.fits, hdu, opts, (hdu) => {
disp(hdu, opts);
});
break;
default:
JS9.error("image section cannot be extracted from this data file");
break;
}
}, JS9.SPINOUT);
};
// display the specified extension of a multi-extension FITS file
JS9.Image.prototype.displayExtension = function(extid, opts, func){
let i, s, got, extname, im, id;
const dispnext = (i) => {
let hdu;
const topts = $.extend(true, {}, opts);
// hdus are loaded as separate images
topts.separate = true;
// all done, call the supplied func, if any
if( i === this.hdus.length ){
if( func ){
try{ JS9.xeqByName(func, window, this); }
catch(e){ JS9.error("in displayExtension callback", e, false); }
}
return;
}
// next hdu
hdu = this.hdus[i];
if( hdu.type === "image" && hdu.naxis >= 2 ){
// load next hdu and recurse when done
this.displayExtension(hdu.hdu, topts, () => { dispnext(i+1); });
} else {
dispnext(i+1);
}
};
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse displayExtension opts: ${opts}`, e); }
}
opts.waiting = false;
// only makes sense if we have hdus
if( !this.hdus ){
JS9.error("no FITS HDUs found for displayExtension()");
}
// sanity check
if( JS9.isNull(extid) ){
JS9.error("missing extname/extnum for displayExtension()");
}
// display all extensions?
if( extid === "all" ){
// load all image extensions, in order, as separate images
// we start with the first and let the call recurse
dispnext(0);
return;
}
// extname specified?
if( typeof extid === "string" ){
opts.extension = extid;
extname = extid.toLowerCase();
for(i=0, got=0; i 0 ){
if( this.display.id === im.display.id ){
got++;
break;
}
}
}
}
if( got ){
im.displayImage("display", opts);
im.display.clearMessage();
if( func ){
try{ JS9.xeqByName(func, window, this); }
catch(e){ JS9.error("in displayExtension callback", e, false); }
}
return;
}
}
// cleanup previous FITS file support, if necessary
// do this before we handle the new FITS file, or else
// we end up with a memory leak in the emscripten heap!
if( !opts.separate ){
JS9.cleanupFITSFile(this.raw, false);
}
// process the FITS file by going to the extname/extnum
this.displaySection(opts, func);
// allow chaining
return this;
};
// display the specified slice of a 3D or 4d FITS cube
JS9.Image.prototype.displaySlice = function(slice, opts, func){
let i, topts, tim;
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse displaySlice opts: ${opts}`, e); }
}
opts.waiting = false;
// sanity check
if( JS9.isNull(slice) ){
JS9.error("missing slice for displaySlice()");
}
if( this.raw.header.NAXIS !== 3 ){
JS9.error("3D image required for displaySlice()");
}
if( slice === "all" ){
// load and display the slices separately
// ignore the fact that we already are displaying a slice of the image,
// since we don't actually know which slice is being displayed ...
for(i=1; i<=this.raw.header.NAXIS3; i++){
topts = $.extend(true, {}, opts, {separate: true});
this.displaySlice(i, topts, func);
}
} else {
// slicename or slicenum specified?
if( JS9.isNumber(slice) ){
opts.slice = `\*:\*:${slice}`;
} else {
opts.slice = slice;
}
// processing for separate images
if( opts.separate ){
// make new id based on slice
opts.id = sprintf("%s\_%s",
this.id
.replace(/\_?([0-9])+:x:x/, "")
.replace(/\_?x:([0-9])+:x/, "")
.replace(/\_?x:x:([0-9])+/, ""),
opts.slice.replace(/\\*/g, "x"));
// look for existing id and just redisplay, if possible
for(i=0; i 0 ){
tim.displayImage("display", {display: tim});
return this;
}
}
}
}
// cleanup previous FITS file heap before handling the new FITS file,
// or we end up with a memory leak in the emscripten heap
JS9.cleanupFITSFile(this.raw, false);
// process the FITS file by going to the slice
this.displaySection(opts, func);
}
// allow chaining
return this;
};
// convert current image to array
JS9.Image.prototype.toArray = function(opts){
let i, j, k, bpe, idx, le, header, npad, arr, buf, \_dbuf;
let dbuf, sect, xlen, blen, datalen, darr;
// opts is optional
opts = opts || {};
// always perform the header keyword fix
opts.simple = true;
// make a copy of the header, in case we have to change it
header = $.extend(true, {}, this.raw.header);
// are we processing a section of the image?
if( JS9.notNull(opts.sect) ){
// image section
sect = opts.sect;
// header parameters that need to change
header.NAXIS1 = sect.x1 - sect.x0;
header.NAXIS2 = sect.y1 - sect.y0;
if( JS9.notNull(header.CRPIX1) ){
header.CRPIX1 = header.CRPIX1 - sect.x0;
}
if( JS9.notNull(header.CRPIX2) ){
header.CRPIX2 = header.CRPIX2 - sect.y0;
}
if( JS9.notNull(header.LTV1) ){
header.LTV1 = header.LTV1 - sect.x0;
}
if( JS9.notNull(header.LTV2) ){
header.LTV2 = header.LTV2 - sect.y0;
}
// extract image section
// length of a date element
blen = Math.abs(this.raw.bitpix/8);
// length of a row of data
xlen = (sect.x1 - sect.x0) \* blen;
// total data length of the section
datalen = xlen \* (sect.y1 - sect.y0);
// make an array of the required length
darr = new ArrayBuffer(datalen);
// make a vew that we can work with
dbuf = new Uint8Array(darr);
// copy the section into the new array, one row at a time
for(i=sect.y0, j=0; i 0;
if( le ){
idx = header.length;
bpe = Math.abs(this.raw.bitpix)/8;
\_dbuf = new Uint8Array(dbuf);
// swap bytes to big-endian
for(i=0; i<\_dbuf.byteLength; i+= bpe){
for(j=i+bpe-1, k=0; k= 0 ){
return;
}
// default is to pan to center
if( args.length === 0 ){
panx = this.raw.width / 2;
pany = this.raw.height / 2;
}
// one string arg is a json specification
// (two string args is panx, pany in string format)
if( args.length === 1 && typeof panx === "string" ){
if( panx === "mouse" && this.ipos ){
panx = this.ipos.x;
pany = this.ipos.y;
} else {
try{ panx = JSON.parse(panx); }
catch(e){ JS9.error(`can't parse setPan JSON: ${panx}`, e); }
}
}
if( typeof panx === "object" ){
obj = panx;
// passing an object supports image, physical, wcs coordinates
if( JS9.notNull(obj.x) && JS9.notNull(obj.y) ){
// image coords
panx = obj.x;
pany = obj.y;
}
if( JS9.notNull(obj.px) && JS9.notNull(obj.py) ){
// physical coords
pos = this.logicalToImagePos({x: obj.px, y: obj.py});
panx = pos.x;
pany = pos.y;
}
if( typeof obj.wcs === "string" ){
// wcs string: ra dec [wcssys]
arr = obj.wcs.trim().split(/ +/);
obj.ra = arr[0];
obj.dec = arr[1];
if( arr.length >= 3 ){
obj.wcssys = arr[2];
}
}
if( this.validWCS() && JS9.notNull(obj.ra) && JS9.notNull(obj.dec) ){
// wcs coords
// use supplied wcs, if necessary
if( obj.wcssys ){
owcssys = this.getWCSSys();
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
this.setWCSSys(obj.wcssys, false);
}
// convert wcs supplied as strings
if( typeof obj.ra === "string" ){
obj.ra = JS9.saostrtod(obj.ra);
if( JS9.isHMS(this.params.wcssys) ){
obj.ra \*= 15.0;
}
}
if( typeof obj.dec === "string" ){
obj.dec = JS9.saostrtod(obj.dec);
}
// convert to image coords
arr = JS9.wcs2pix(this.raw.wcs, obj.ra, obj.dec)
.trim().split(/ +/);
panx = parseFloat(arr[0]);
pany = parseFloat(arr[1]);
// restore original wcssys
if( owcssys ){
this.setWCSSys(owcssys, false);
JS9.globalOpts.xeqPlugins = txeq;
}
}
}
// generate section from new image coords
if( !JS9.isNumber(panx) || !JS9.isNumber(pany) ){
JS9.error(`invalid input for setPan: ${panx} ${pany}`);
}
if( this.wcsAlign() || this.isawcsim ){
oval = JS9.globalOpts.panWithinDisplay;
JS9.globalOpts.panWithinDisplay = true;
}
this.mkSection(panx, pany);
// set pan for aligned images, if necessary
if( this.wcsAlign() || this.isawcsim ){
for(i=0; i x1 ){ x1 = pts[i].x; }
if( JS9.isNull(y0) || pts[i].y < y0 ){ y0 = pts[i].y; }
if( JS9.isNull(y1) || pts[i].y > y1 ){ y1 = pts[i].y; }
}
w = x1 - x0;
h = y1 - y0;
} else {
w = this.raw.width;
h = this.raw.height;
}
nzoom = Math.min(this.display.width/w, this.display.height/h);
// a little rounding makes the zoom nicer
nzoom = Math.round((nzoom + 0.0000001) \* 1000000) / 1000000;
break;
default:
nzoom = parseFloat(zval);
break;
}
break;
case "number":
nzoom = zval;
break;
default:
return;
}
return nzoom;
};
// set zoom of RGB image
JS9.Image.prototype.setZoom = function(zval){
let i, nzoom, im, ipos, oval;
// is this core service disabled?
if( $.inArray("zoom", this.params.disable) >= 0 ){
return;
}
nzoom = this.parseZoom(zval);
if( !nzoom ){
JS9.error(`invalid input for setZoom: ${zval}`);
}
if( this.wcsAlign() || this.isawcsim ){
oval = JS9.globalOpts.panWithinDisplay;
JS9.globalOpts.panWithinDisplay = true;
}
// remake section
this.mkSection(nzoom);
// set zoom for aligned images, if necessary
if( this.wcsAlign() || this.isawcsim ){
for(i=0; i 0 ){ nobj.flip = "x"; }
if( wcsinfo.cdelt2 < 0 ){ nobj.flip = (nobj.flip|| "") + "y"; }
// only galactic and ecliptic use the algorithm below, others are trivial
switch(wcssys){
case "galactic":
case "ecliptic":
break;
default:
if( wcsinfo.crot ){
nobj.angle = -wcsinfo.crot;
}
return nobj;
}
// algorithm for galactic and ecliptic ... from AV (via trello)
// turn off plugin callbacks
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
// set wcssys to be the same wcssys the north pole coords are in
this.setWCSSys(pole[wcssys].wcssys, false);
// get center of image in that coord system
cx = this.raw.width/2;
cy = this.raw.height/2;
arr = JS9.pix2wcs(this.raw.wcs, cx, cy).trim().split(/\s+/);
// convert strings to float (degrees)
ra = JS9.saostrtod(arr[0]);
// ra hours to degrees, if necessary
if( JS9.isHMS() ){ ra \*= 15.0; }
dec = JS9.saostrtod(arr[1]);
// angular distance between north pole and image center
nobj.angle = JS9.angdist(ra, dec, pole[wcssys].ra, pole[wcssys].dec);
// remove any header-based rotation
if( JS9.notNull(this.raw.wcsinfo.crot) ){
nobj.angle -= this.raw.wcsinfo.crot;
}
// reset to the current coord system
this.setWCSSys(wcssys, false);
// restore plugin callbacks
JS9.globalOpts.xeqPlugins = txeq;
// return info
return nobj;
};
// get transform
JS9.Image.prototype.getTransform = function(){
return this.params.transform;
};
// set transform (basis for setFlip, setRot90, setRotate)
JS9.Image.prototype.setTransform = function(...args){
let a, i, sina, cosa, m3, transform;
let angle = 0;
let scale = 1;
let [arg1] = args;
if( !this || !this.raw || !this.raw.header ){
JS9.error("invalid image for setTransform");
}
// reset -> we're done
if( arg1 === "reset" ){
delete this.params.transform;
delete this.params.transformInverse;
delete this.params.transformAngle;
delete this.params.transformScale;
return;
}
// start with the identity matrix
transform = [[1,0,0], [0,1,0], [0,0,1]];
// for each transform ...
for(i=0; i {
let i, arr;
let nx = 0;
let ny = 0;
let nflip = "";
arr = (flip + (this.params.flip||"")).split("");
for(i=0; i {
if( JS9.globalOpts.rotateRelative ){
rot += this.params.rotate||0;
}
while( rot < 0 ){ rot += 360; }
while( rot >= 360 ){ rot -= 360; }
return rot;
}
// sanity checks
if( JS9.isNull(rot) ){ return this; }
// reset
if( rot === "reset" ){
this.params.rotate = 0;
return this.setRotate(0);
}
// north is up in current wcs system: calculate rotation angle
if( typeof rot === "string" && rot.match(/north/i) ){
nobj = this.getNorthIsUp();
rot = nobj.angle;
if( JS9.notNull(nobj.flip) ){ this.setParam("flip", nobj.flip); }
}
if( typeof rot === "string" ){
rot = parseFloat(rot);
}
if( !JS9.isNumber(rot) ){
JS9.error(`invalid rotation for setRotate: ${rot}`);
}
if( !this || !this.raw || !this.raw.header ){
JS9.error("invalid image for setRotate");
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse setRotate opts: ${opts}`, e); }
}
// save this routine so it can be reconstituted in a restored session
this.xeqStashSave("setRotate", [rot]);
// save normalized value
this.params.rotate = normRot(rot);
// update the transform
this.setTransform();
// non-rectangular canvas: redo section to ensure coverage of display
if( this.params.transformAngle &&
this.display.canvas.width !== this.display.canvas.height ){
this.mkSection(this.getZoom());
}
// redisplay using these data
this.displayImage("all", opts);
// refresh shape layers
this.refreshLayers();
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetrotate");
}
// allow chaining
return this;
};
// get 90-degree rotatation state
JS9.Image.prototype.getRot90 = function(){
return this.params.rot90;
};
// rotate image by multiples of 90 degrees using canvas transform
JS9.Image.prototype.setRot90 = function(...args){
let [rot, opts] = args;
const normRot = (rot) => {
rot += this.params.rot90||0;
while( rot < 0 ){ rot += 360; }
while( rot >= 360 ){ rot -= 360; }
if( rot === 270 ){
rot = -90;
}
return rot;
}
// sanity checks
if( JS9.isNull(rot) ){ return this; }
// reset
if( rot === "reset" ){
this.params.rot90 = 0;
return this.setRot90(0);
}
if( typeof rot === "string" ){
rot = parseFloat(rot);
}
if( !this || !this.raw || !this.raw.header ){
JS9.error("invalid image for setRot90");
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse setRot90 opts: ${opts}`, e); }
}
// only 90 degree rotations
switch(rot){
case 0:
rot = 0;
break;
case 1:
rot = 90;
break;
case -1:
rot = -90;
break;
case 90:
break;
case -90:
break;
default:
JS9.error(`invalid setRot90 rotation value: ${rot} (use: +/1, +/90)`);
break;
}
// save this routine so it can be reconstituted in a restored session
this.xeqStashSave("setRot90", [rot]);
// save normalized value
this.params.rot90 = normRot(rot);
// update the transform
this.setTransform();
// non-rectangular canvas: redo section to ensure coverage of display
if( this.params.transformAngle &&
this.display.canvas.width !== this.display.canvas.height ){
this.mkSection(this.getZoom());
}
// redisplay using these data
this.displayImage("all", opts);
// refresh shape layers
this.refreshLayers();
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetrot90");
}
// allow chaining
return this;
};
// redo the current flip and rot90 in cases where the underyling data changed
// (e.g. displaySection, refreshImage)
JS9.Image.prototype.reFlipRot = function(){
let i, flips, nrot;
let flip = this.params.flip;
let rot90 = this.params.rot90;
let rot = this.params.rotate;
if( flip !== "none" ){
this.params.flip = "none";
flips = flip.split("");
for(i=0; i= 0 ){
return;
}
// do we update the default?
if( JS9.isNull(updatedef) ){
updatedef = JS9.globalOpts.wcsSetUpdatesDef;
}
if( wcssys === "image" ){
this.params.wcssys = "image";
this.params.wcsunits = "pixels";
JS9.wcsunits.image = "pixels";
} else if( wcssys === "physical" ){
this.params.wcssys = "physical";
this.params.wcsunits = "pixels";
if( updatedef ){
JS9.globalOpts.wcsUnits.physical = "pixels";
}
} else if( this.validWCS() ){
// native: original wcs from file
if( wcssys === "native" ){
wcssys = this.params.wcssys0;
}
// set wcs system
s = JS9.wcssys(this.raw.wcs, wcssys);
if( s ){
// store new wcs system param
this.params.wcssys = s.trim();
// get units associated with this wcs system
u = JS9.globalOpts.wcsUnits[this.params.wcssys] || "sexagesimal";
// set the units
this.setWCSUnits(u, updatedef);
}
}
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetwcssys");
}
// allow chaining
return this;
};
// init wcs
JS9.Image.prototype.initWCS = function(header){
let alt, key, varr, s, bufsize, buf;
const hlen = JS9.globalOpts.wcsHlength;
const awcs = /(WCSNAME|WCSAXES|CRVAL[0-9]|CRPIX[0-9]|PC[0-9]\_[0-9]|CDELT[0-9]|CD[0-9]\_[0-9]|CTYPE[0-9]|CUNIT[0-9]|CRVAL[0-9]|PV[0-9]\_[0-9]|PS[0-9]\_[0-9]|RADESYS|LONPOLE|LATPOLE)([A-Z])/;
if( !this.raw.header ){
return this;
}
// usually it's the raw header
header = header || this.raw.header;
// clean up old wcs
this.freeWCS();
// init object to hold alt wcs objects
this.raw.altwcs = {};
// set up the default wcs, using the original header params
alt = "default";
this.raw.altwcs[alt] = {};
this.raw.altwcs[alt].header = header;
// look for wcs alternates
// see: http://www.atnf.csiro.au/people/mcalabre/WCS/wcs.pdf
for( key of Object.keys(header) ){
// is it an alt wcs keyword?
varr = key.match(awcs);
if( varr && varr.length ){
// this is the A-Z version
alt = varr[2];
// init the alt wcs object, if necessary
if( !this.raw.altwcs[alt] ){
this.raw.altwcs[alt] = {};
// start with original header
this.raw.altwcs[alt].header = $.extend({}, header);
}
// wcslib seems to want "RADECSYS", not "RADESYS"
if( varr[1] === "RADESYS" ){
varr[1] = "RADECSYS";
}
// overwrite standard keyword in header with the alt value
this.raw.altwcs[alt].header[varr[1]] = header[varr[0]];
}
}
// init all of the wcs's we found
for( key of Object.keys(this.raw.altwcs) ){
// loop through alt wcs objects
s = JS9.raw2FITS(this.raw.altwcs[key].header);
// too large headers blow Emscripten's stack space
// this.raw.altwcs[key].wcs = JS9.initwcs(s, hlen);
// so we have to copy the header to the heap:
// allocate space for the string in the emscripten heap
bufsize = s.length + 1;
try{ buf = JS9.vmalloc(bufsize); }
catch(e){ JS9.error(`can't malloc for wcsinit: ${bufsize}`, e); }
// copy the string to the heap
try{ JS9.vstrcpy(s, buf); }
catch(e){ JS9.error(`can't copy for wcsinit: ${bufsize}`, e); }
// call the wcsinit routine, passing the heap pointer
this.raw.altwcs[key].wcs = JS9.initwcs(buf, hlen);
// free heap space
JS9.vfree(buf);
// get info about the wcs
if( this.raw.altwcs[key].wcs > 0 ){
try{ this.raw.altwcs[key].wcsinfo =
JSON.parse(JS9.wcsinfo(this.raw.altwcs[key].wcs)); }
catch(ignore){ /\* empty \*/ }
}
}
// set current wcs to the default
this.setWCS("default");
// allow chaining
return this;
};
// close and free wcs resources
JS9.Image.prototype.freeWCS = function(raw){
let key;
// raw defaults to ... default raw
raw = raw || this.raw;
if( raw.altwcs ){
// free all wcs structures
for( key of Object.keys(raw.altwcs) ){
// loop through alt wcs objects
if( raw.altwcs[key].wcs > 0 ){
JS9.freewcs(raw.altwcs[key].wcs);
raw.altwcs[key].wcs = null;
}
}
}
};
// get name of current wcs (from among the alternates)
JS9.Image.prototype.getWCS = function(){
let key, obj;
// loop through wcs objects, looking for a match
for( key of Object.keys(this.raw.altwcs) ){
if( this.raw.wcs === this.raw.altwcs[key].wcs ){
obj = $.extend(true, {}, this.raw.altwcs[key].wcsinfo);
obj.version = key;
obj.wcsname = this.raw.altwcs[key].header.WCSNAME;
return obj;
}
}
return null;
};
// set wcs to default or one of the alternative versions
JS9.Image.prototype.setWCS = function(version){
let key, wcsname, wcssys;
version = version || "default";
// sanity check
if( !this.raw || !this.raw.altwcs ){ return this; }
// loop through wcs objects, looking for a match
for( key of Object.keys(this.raw.altwcs) ){
wcsname = this.raw.altwcs[key].header.WCSNAME;
if( (version === key) || (version === wcsname) ){
// make sure its a valid wcs
if( this.raw.altwcs[key].wcs <= 0 ){
JS9.error("invalid WCS for version: %s", version);
}
// set this wcs up as the current one
this.raw.wcs = this.raw.altwcs[key].wcs;
// get info about the wcs
this.raw.wcsinfo = this.raw.altwcs[key].wcsinfo;
// look for a good wcssys
if( this.raw.wcsinfo && this.raw.wcsinfo.radecsys ){
wcssys = this.raw.wcsinfo.radecsys;
} else {
if( this.params.wcssys !== "native" ){
wcssys = this.params.wcssys.trim();
} else {
wcssys = this.params.lcs;
}
}
// set the wcs system
this.setWCSSys(wcssys);
// this is also the default
if( !this.params.wcssys0 ){
this.params.wcssys0 = wcssys;
}
// set the wcs units
this.setWCSUnits(this.params.wcsunits);
// all done
return this;
}
}
// didn't find it
JS9.error(`could not find WCS version: ${version}`);
};
// is a valid WCS open and active
JS9.Image.prototype.validWCS = function(){
return this.raw && this.raw.wcs && this.raw.wcs > 0;
};
// get the WCS units for this image
JS9.Image.prototype.getWCSUnits = function(){
if( this.params.wcsunits ){
return this.params.wcsunits;
}
return "pixels";
};
// set the WCS units for this image
JS9.Image.prototype.setWCSUnits = function(wcsunits, updatedef){
let s, ws;
// is this core service disabled?
if( $.inArray("wcs", this.params.disable) >= 0 ){
return;
}
// do we update the default?
if( JS9.isNull(updatedef) ){
updatedef = JS9.globalOpts.wcsSetUpdatesDef;
}
if( wcsunits === "pixels" ){
if( JS9.isWCSSys(this.params.wcssys) ){
this.params.wcssys = "physical";
}
this.params.wcsunits = "pixels";
if( updatedef ){
JS9.globalOpts.wcsUnits[this.params.wcssys] = "pixels";
}
} else if( this.validWCS() ){
if( JS9.notWCS(this.params.wcssys) ){
ws = JS9.imageOpts.wcssys;
this.setWCSSys(ws);
}
s = JS9.wcsunits(this.raw.wcs, wcsunits);
if( s ){
this.params.wcsunits = s.trim();
if( updatedef ){
JS9.globalOpts.wcsUnits[this.params.wcssys] =
this.params.wcsunits;
}
}
}
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetwcsunits");
}
// allow chaining
return this;
};
// notify the helper a new image was displayed
JS9.Image.prototype.notifyHelper = function(){
let basedir, image1, image2;
const imexp = new RegExp(`^${JS9.ANON}[0-9]\*`);
const installexp = JS9.INSTALLDIR ? new RegExp(`^${JS9.INSTALLDIR}`) : null;
// notify the helper
if( JS9.helper.connected && !this.file.match(imexp) ){
switch(JS9.helper.type){
case "get":
case "post":
// get pageid from CGI helper (socket.io does this when connecting)
if( !JS9.helper.pageid ){
JS9.helper.send("pageid", null, (s) => {
if( s && s.trim().match(/^[a-fA-F0-9]{8}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{4}-[a-fA-F0-9]{12}$/) ){
JS9.helper.pageid = s;
JS9.helper.js9helper = "js9helper";
}
});
break;
}
}
// get helper info about this image
// but also try removing part of path which gets to install dir
image1 = this.file;
if( image1.charAt(0) !== "/" && installexp ){
image2 = this.file.replace(installexp, "");
}
JS9.helper.send("image", {"image": image1, "image2": image2}, (res) => {
let rstr, r, s, cc, regexp;
if( typeof res === "object" ){
// from node.js, we get an object with stdout and stderr
rstr = res.stdout;
// log stderr but keep going
if( res.stderr && JS9.DEBUG > 1 ){
JS9.log(res.stderr);
}
} else {
// with cgi, we just get stdout
rstr = res;
}
// unless we have no stdout
if( !rstr ){
return;
}
// returns: [file, path, wcs]
// split args, dealing with spaces inside brackets
r = rstr.trim().match(/(?:[^\s[]+|\[[^\]]\*\])+/g);
s = r[1];
if( s !== "?" ){
if( !JS9.globalOpts.dataDir ){
this.fitsFile = s;
// prepend base of png path if fits file has no path
// is this a bad "feature" in tpos?? probably ...
if( !this.fitsFile.includes("/") ){
basedir = this.file.match( /.\*\// );
// but don't add installdir as part of prefix
// (fitsFile path is relative to the js9 directory)
if( basedir && basedir.length ){
regexp = new RegExp(`^${JS9.INSTALLDIR}`);
basedir = basedir[0].replace(regexp, "");
this.fitsFile = basedir + this.fitsFile;
}
}
// prepend JS9\_DIR on files if fits is not absolute
if( JS9.globalOpts.prependJS9Dir ){
if( this.fitsFile &&
!this.fitsFile.match(/^\${JS9\_DIR}/) &&
this.fitsFile.charAt(0) !== "/" ){
this.fitsFile = `\${JS9\_DIR}/${this.fitsFile}`;
}
if( this.parentFile &&
!this.parentFile.match(/^\${JS9\_DIR}/) &&
this.parentFile.charAt(0) !== "/" ){
this.parentFile = `\${JS9\_DIR}/${this.parentFile}`;
}
}
} else {
cc = s.lastIndexOf("/") + 1;
this.fitsFile = `${JS9.globalOpts.dataDir}/${s.slice(cc)}`;
}
if( JS9.DEBUG > 1 ){
JS9.log("JS9 fitsFile: %s %s", this.file, this.fitsFile);
}
}
if( this.fitsFile ){
this.fitsFile = JS9.cleanPath(this.fitsFile);
}
if( this.parentFile ){
this.parentFile = JS9.cleanPath(this.parentFile);
}
// first time through, query the helper for info
if( !this.queried ){
this.queryHelper("all");
this.queried = true;
}
});
}
// allow chaining
return this;
};
// ask helper for various types of information
JS9.Image.prototype.queryHelper = function(which){
const what = which || "all";
// query the helper
if( JS9.helper.connected ){
if( (what === "all") || (what === "getAnalysis") ){
// only retrieve analysis tasks once per image
if( !this.analysisPackages ){
JS9.helper.send("getAnalysis", {"fits": this.fitsFile}, (s) => {
if( s ){
try{ this.analysisPackages = JSON.parse(s); }
catch(e){ JS9.log("can't get analysis", e); }
}
});
}
}
}
// allow chaining
return this;
};
// expand macros for this image
JS9.Image.prototype.expandMacro = function(s, opts){
let cmd, olen;
// sanity check
if( !s ){ return; }
// process each $ token
// eslint-disable-next-line no-unused-vars
cmd = s.replace(/\${?([a-zA-Z][a-zA-Z0-9\_()]+)}?/g, (m, t, o) => {
let i, r, owcssys, pos;
// called in image context
const savewcs = (wcssys) => {
const owcs = this.params.wcssys;
if( wcssys ){
switch(wcssys){
case "wcs":
if( JS9.notWCS(owcs) ){
this.params.wcssys = this.params.wcssys0;
}
break;
case "physical":
case "image":
this.params.wcssys = wcssys;
break;
default:
break;
}
}
return owcs;
};
const restorewcs = (wcssys) => {
if( wcssys ){
this.params.wcssys = wcssys;
}
};
const withext = (r) => {
let e;
// for tables, we might need to add the binning filter
if( this.imtab === "table" ){
if( this.raw.hdu && this.raw.hdu.table.filter &&
!r.match(this.raw.hdu.table.filter) ){
if( r.match(/\]\[/) ){
r = `${r.slice(0,-1)}&&${this.raw.hdu.table.filter}]`;
} else {
r += `[${this.raw.hdu.table.filter}]`;
}
}
} else if( this.imtab === "image" ){
// for images, we might need to add/replace extension info
e = this.file.match(/\[.\*\]/);
if( e ){
if( r.match(/\[.\*\]/) ){
r = r.replace(/\[.\*\]/, e);
} else {
r += e;
}
} else if( this.raw && this.raw.hdu &&
this.raw.hdu.slice ){
// current slice of 3D cube
e = this.raw.hdu.slice
.replace(/:/g, ",").replace(/([0-9][0-9]\*)/, "$1:$1");
r += `[${e}]`;
} else if( this.raw && this.raw.header &&
this.raw.header.NAXIS > 2 ){
// first slice of 3D cube
r += `[\*,\*,1:1]`;
}
}
return r;
};
const u = t.split("(");
if( u[1] ){
u[1] = u[1].replace(/\)$/, "");
}
switch(u[0]){
case "id":
r = this.display.divjq.attr("id");
break;
case "image0":
r = this.id.replace(/\[EVENTS\]/i, "");
break;
case "image":
r = this.id;
break;
case "filename":
// for cubes, process all slices if (all) is specified
if( u[1] == "all" && this.fitsFile &&
this.raw && this.raw.header && this.raw.header.NAXIS === 3 ){
r = this.fitsFile;
} else if( this.parentFile && (u[1] !== "this") ){
// if a filter is defined, add it
if( this.raw && this.raw.filter ){
r = this.parentFile;
// assume parent is a table with EVENTS
if( !r.match(/\[.\*\]/) ){ r += '[EVENTS]'; }
r += `[${this.raw.filter}]`;
} else {
r = withext(this.parentFile);
}
} else if( this.fitsFile ){
r = withext(this.fitsFile);
} else {
JS9.error(`no FITS file for ${this.id}`);
}
break;
case "fits":
if( !this.fitsFile ){
JS9.error(`no FITS file for ${this.id}`);
}
r = withext(this.fitsFile);
break;
case "parent":
if( !this.parentFile ){
JS9.error(`no parent FITS file for ${this.id}`);
}
r = this.parentFile;
break;
case "ext":
if( this.fitsFile ){
r = this.fitsFile.match(/\[.\*\]/);
if( r === null ){
r = "";
}
} else {
JS9.error(`no FITS file for ${this.id}`);
}
break;
case "imcenter":
pos = this.displayToLogicalPos({x: this.display.width/2,
y: this.display.height/2});
r = `${pos.x},${pos.y}`;
break;
case "wcscenter":
pos = this.displayToImagePos({x: this.display.width/2,
y: this.display.height/2});
r = JS9.pix2wcs(this.raw.wcs, pos.x, pos.y).replace(/\s+/g, ",");
break;
case "sregions":
owcssys = savewcs(u[1]);
r = this.listRegions("source",
{mode:0, includedcoords:JS9.globalOpts.regExpandDCoords})
.replace(/\s+/g,"");
restorewcs(owcssys);
break;
case "bregions":
owcssys = savewcs(u[1]);
r = this.listRegions("background",
{mode:0, includedcoords:JS9.globalOpts.regExpandDCoords})
.replace(/\s+/g,"");
restorewcs(owcssys);
break;
case "regions":
owcssys = savewcs(u[1]);
r = this.listRegions("all",
{mode:0, includedcoords:JS9.globalOpts.regExpandDCoords})
.replace(/\s+/g,"");
restorewcs(owcssys);
break;
case "mag":
// hack for statusbar
if( this.params.zoom ){
r = sprintf("%s%", 100 \* this.params.zoom);
} else {
r = "?";
}
break;
case "bin":
// binning factor for image/event file
if( this.binning.bin ){
r = this.binning.bin;
} else {
r = "?";
}
break;
case "flip":
// flip info
if( this.params.flip ){
r = this.params.flip;
} else {
r = "?";
}
break;
case "flipx":
// flipx
if( this.params.flip ){
if (this.params.flip.match('x')) {
r = "x";
} else {
r = "x-none";
}
} else {
r = "?";
}
break;
case "flipy":
// flipy
if( this.params.flip ){
if (this.params.flip.match('y')) {
r = "y";
} else {
r = "y-none";
}
} else {
r = "?";
}
break;
default:
// look for keyword in the serialized opts array
if( opts ){
olen = opts.length;
for(i=0; i {
if( !s1 || !s2 ){
return false;
}
return String(s1).toUpperCase() === String(s2).toUpperCase();
};
// sanity check
if( !atask.title || !atask.name ){ return false; }
// is this task hidden?
if( atask.hidden ){
return false;
}
// file validators
if( atask.files ){
if( atask.files.match(/^fits$/) &&
!this.fitsFile ){
return false;
}
if( atask.files.match(/^table$/) ){
if( this.imtab !== "table" ){
return false;
}
}
if( atask.files.match(/^image$/) ){
if( this.imtab !== "image" ){
return false;
}
}
// header params: fitsHeader(pname,pvalue)
parr = atask.files.match(parexp);
if( parr ){
s = this.raw.header[parr[1].toUpperCase()];
if( !seq(s, parr[2]) ){
return false;
}
}
// win vars: winVar(name,value)
parr = atask.files.match(winexp);
if( parr ){
s = JS9.varByName(parr[1], window);
if( !seq(s, parr[2]) ){
return false;
}
}
// js9 vars: js9Var(name,value)
parr = atask.files.match(js9exp);
if( parr ){
s = JS9.varByName(parr[1], JS9);
if( !seq(s, parr[2]) ){
return false;
}
}
// im vars: imVar(name,value)
parr = atask.files.match(imexp);
if( parr ){
s = JS9.varByName(parr[1], this);
if( !seq(s, parr[2]) ){
return false;
}
}
} // end of file validators
return true;
};
// return object containing analysis task definitions
JS9.Image.prototype.getAnalysis = function(){
let i, j, t, tasks;
const obj = [];
// sanity check
if( !this.analysisPackages ){ return obj; }
// return validated tasks
for(j=0; j {
// shouldn't happen
if( !JS9.helper ){
JS9.error(s, t);
}
switch(JS9.helper.type){
case 'nodejs':
case 'socket.io':
// when socket.io is long-polling, throwing an error prevent the
// polling from completing, leading to a timeout error and disaster.
// to allow the polling to complete, throw the error after a delay
if( JS9.helper.socket &&
JS9.helper.socket.io.engine.transport.name === "polling"){
window.setTimeout(() => {
JS9.error(s, t);
}, 0);
} else {
JS9.error(s, t);
}
break;
default:
JS9.error(s, t);
break;
}
};
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse runAnalysis opts: ${opts}`, e); }
}
// func can be passed, or it can be global
func = func || JS9.globalOpts.analysisFunc;
// sanity check
if( !JS9.helper.connected || !this.analysisPackages ){ return; }
// get analysis task
a = this.lookupAnalysis(name);
if( !a ){
JS9.error(`could not find analysis task: ${name}`);
return;
}
// get command line using macro expansion
if( a.action ){
obj.cmd = this.expandMacro(a.action, opts);
}
// macro expand the strings in the keys array
if( a.keys ){
obj.keys = {};
for(i=0; i {
let s, robj, f, pf, xobj, files;
// return type can be string or object
if( typeof r === "object" ){
// object from node.js
robj = r;
} else {
// string from cgi
if( r.search(JS9.analOpts.epattern) >=0 ){
robj = {stderr: r};
} else {
robj = {stdout: r};
}
}
robj.errcode = robj.errcode || 0;
// if a processing func was supplied, call it and don't display
if( func ){
func.call(this, robj.stdout, robj.stderr, robj.errcode, a);
} else {
// handle errors before we start
if( robj.stderr ){
s = robj.stderr;
// if its only a warning, log it
if( (s.search(/WARNING:/i) >= 0) && (s.search(/ERROR:/i) < 0) ){
JS9.log(s);
} else {
// otherwise, throw an error
analError(s, JS9.analOpts.epattern);
return;
}
} else if( robj.errcode ){
s = `ERROR: running ${a.name} [${robj.errcode}]`;
// not sure what this means, so just log it if stdout exists
if( robj.stdout ){
JS9.log(s);
} else {
// otherwise, throw an error
analError(s, JS9.analOpts.epattern);
return;
}
}
// display according to type
switch(a.rtype){
case "text":
case undefined:
this.displayAnalysis("text", robj.stdout,
{divid: JS9.globalOpts.analysisDiv});
break;
case "plot":
this.displayAnalysis("plot", robj.stdout,
{divid: JS9.globalOpts.analysisDiv});
break;
case "alert":
if( robj.stdout ){
alert(robj.stdout);
}
break;
case "fits":
// output is file and possibly parentFile
files = robj.stdout.split(/\s+/);
if( files && files[0] ){
// file
f = JS9.cleanPath(files[0]);
// relative path: add install dir prefix
if( f.charAt(0) !== "/" ){
f = JS9.InstallDir(f);
}
// which is a proxy file (meaning: delete it on close)
xobj = {proxyFile: f};
// look for parentFile (relative to helper, not install)
if( files[1] ){
pf = JS9.cleanPath(files[1]);
xobj.parentFile = pf;
xobj.proxyParent = pf;
}
// don't convert this FITS file into another FITS file!
xobj.fits2fits = false;
// don't fix the path for desktop
xobj.fixpath = false;
// load new file
JS9.Load(f, xobj, {display: this.display});
}
break;
case "regions":
// output is region file (or region string), optional opts
files = robj.stdout.split(/\s+/);
if( files && files[0] ){
// see if a json opts was returned
if( files.length > 1 ){
try{ ropts = JSON.parse(files[1]); }
catch(e){ ropts = null; }
}
ropts = ropts || {};
if( typeof ropts.remove === "boolean" ){
ropts.remove = "all";
}
if( ropts.type === "string" ){
// region string was passed directly
if( ropts.remove ){
this.removeShapes("regions", ropts.remove);
}
this.addShapes("regions", files[0], opts);
} else {
// region file was passed, we have to fetch it
f = JS9.cleanPath(files[0]);
// relative path: add install dir prefix
if( f.charAt(0) !== "/" ){
f = JS9.InstallDir(f);
}
// load new region file
obj = {responseType: "text"};
JS9.fetchURL(null, f, obj, (regions, opts) => {
if( ropts.remove ){
this.removeShapes("regions", ropts.remove);
}
this.addShapes("regions", regions, opts);
});
}
}
break;
case "catalog":
// output is catalog file
files = robj.stdout.split(/\s+/);
if( files && files[0] ){
f = JS9.cleanPath(files[0]);
// load new catalog file
obj = {responseType: "text"};
JS9.fetchURL(null, f, obj, (catalog, opts) => {
this.loadCatalog(null, catalog, opts);
});
}
break;
case "none":
break;
default:
JS9.error(`unknown analysis result type: ${a.rtype}`);
break;
}
}
// set status
this.setStatus("runAnalysis", "complete");
// done waiting
JS9.waiting(false);
});
// allow chaining
return this;
};
// display analysis results (text or plot)
JS9.Image.prototype.displayAnalysis = function(type, s, opts){
let i, r, id, did, hstr, pobj, divjq, title, titlefile, winFormat;
let divid, plot, pdata, popts, gim, gdiv, nscale;
const a = JS9.lightOpts[JS9.LIGHTWIN];
const flotConfig = () => {
let s;
let winformat = "width=368px,height=110px,resize=1,scrolling=1";
const title = JS9.Plot.opts.title;
// sanity check
if( !divjq || !plot ){ return; }
// call this once window is loaded
$(JS9.lightOpts[JS9.LIGHTWIN].topid)
.arrive("#plotConfigForm", {onceOnly: true}, () => {
JS9.Plot.initConfigForm.call(this, plot, pobj);
});
if( JS9.allinone ){
s = JS9.allinone.plotConfigHTML;
plot.winid = this.displayAnalysis("params", s, {title, winformat});
} else {
s = JS9.InstallDir(JS9.Plot.opts.configURL);
plot.winid = this.displayAnalysis("params", s, {title, winformat});
}
};
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse displayAnalysis opts: ${opts}`, e); }
}
// window format ...
winFormat = opts.winformat;
// ... or target div
if( opts.divid && $(`#${opts.divid}`).length > 0 ){
divid = $(`#${opts.divid}`);
}
// make up title, if necessary
title = opts.title || "";
if( this && !title ){
titlefile = (this.fitsFile || this.id || "");
titlefile = titlefile.split("/").reverse()[0];
title = `AnalysisResults: ${titlefile}`;
// add display to title
title += sprintf(JS9.IDFMT, this.display.id);
}
// unique id for light window
id = `Analysis\_${JS9.uniqueID()}`;
// process the type of analysis results
switch(type){
case "text":
s = s || "";
hstr = "";
hstr += `

```
${s}
```

`;
hstr += "";
// populate div or create the light window to hold the text
if( divid ){
// existing div
divid.html(hstr);
// Electron does not support search so we implement our own ...
if( window.electron ){
JS9.searchbar(divid[0]);
}
} else {
// display light window
winFormat = winFormat || a.textWin;
did = JS9.lightWin(id, "inline", hstr, title, winFormat);
// Electron does not support search so we implement our own ...
if( window.electron ){
JS9.searchbar(did);
}
}
break;
case "plot":
// convert results to js object
if( s && typeof s === "string" ){
try{ pobj = JSON.parse(s); }
catch(e){ JS9.error(`can't plot return data: ${s}`, e); }
} else if( typeof s === "object" ){
pobj = s;
}
// sanity check
if( !pobj ){ return; }
// initialize scale
pobj.curscale = {x: "linear", y: "linear"};
// create an outer div and an inner plot for the light window open call
hstr = ``;
// populate div or create the light window to hold the plot
if( divid ){
divid.html(hstr);
} else {
winFormat = winFormat || a.plotWin;
did = JS9.lightWin(id, "inline", hstr, title, winFormat);
}
// find the inner plot div which now is inside the light window
divjq = $(`#${id} #${id}Plot`);
// when using a div (instead of a lightwin), set the div size
if( divid ){
divjq.css("width", divid.css("width"));
divjq.css("height", divid.css("height"));
divjq.css("margin", 0);
}
// flot data
if( pobj.data ){
switch( JS9.globalOpts.plotLibrary ){
case "plotly":
popts = $.extend(true, {}, JS9.Plot.opts, pobj.opts);
if( pobj.label ){
popts.title = pobj.label;
}
pdata = {x: [], y: [], type: "scatter"};
// flot data format: [[x1,y1], [x2,y2], ..]
// or: [[x1,y1,yerr1], [x2,y2,yerr2], ..]
if( pobj.data[0].length >= 3 ){
// look for flot yerr properties
pdata.error\_y = {type: 'data', array: [], visible: true};
if( pobj.points && pobj.points.yerr ){
if( pobj.points.yerr.color ){
pdata.error\_y.color = pobj.points.yerr.color;
}
}
}
for(i=0; i {
JS9.Plot.annotate(divjq, plt, pobj);
};
}
pobj.color = pobj.color || popts.color;
// log scale?
if( pobj.xscale === "log" ){
popts.xaxis = popts.xaxis || {};
popts.xaxis.transform = JS9.Plot.logfunc;
popts.xaxis.inverseTransform = JS9.Plot.expfunc;
pobj.curscale.x = "log";
}
if( pobj.yscale === "log" ){
popts.yaxis = popts.yaxis || {};
popts.yaxis.transform = JS9.Plot.logfunc;
popts.yaxis.inverseTransform = JS9.Plot.expfunc;
pobj.curscale.y = "log";
}
try{ plot = $.plot(divjq, [pobj], popts); }
catch(e){ JS9.error("can't plot data (flot)", e); }
// annotate, if necessary
if( JS9.Plot.opts.annotate && pobj.annotations ){
JS9.Plot.annotate(divjq, plot, pobj);
}
break;
}
// add key handlers
divjq.css("outline", "none");
divjq.attr("tabindex", 0);
divjq.on("keydown", (evt) => {
const c = JS9.eventToCharStr(evt);
switch(c){
case "c":
flotConfig();
break;
case "x":
case "y":
nscale = pobj.curscale[c] !== "linear" ? "linear" : "log";
JS9.Plot.rescale(divjq, plot, pobj, c, nscale);
break;
default:
break;
}
});
// add the plot config gear
gim = $(`![](${JS9.InstallDir("images/gears.png")})`);
gim.on("click", flotConfig);
gdiv = $("

");
gdiv.append(gim);
divjq.append(gdiv);
}
break;
case "params":
case "regions":
case "textline":
if( divid ){
if( JS9.allinone ){
divid.html(s);
} else {
$.ajax({
url: s,
cache: false, // required for v3 socket.io
dataType: "text",
success: (data) => { divid.html(data); }
});
}
} else {
if( type === "params" ){
winFormat = winFormat || a.paramWin;
} else if( type === "regions" ){
if( JS9.globalOpts.regConfigSize === "small" ){
winFormat = winFormat || a.regWin0;
} else {
winFormat = winFormat || a.regWin;
}
} else {
winFormat = winFormat || a.dpathWin;
}
r = JS9.allinone?"inline":"ajax";
did = JS9.lightWin(id, r, s, title, winFormat);
}
break;
default:
break;
}
return did;
};
// save image as a FITS file
JS9.Image.prototype.saveFITS = function(fname, opts){
let arr, blob, s, sect;
if( {}.hasOwnProperty.call(window, "saveAs") ){
if( fname ){
fname = fname
.replace(/\s+/g, "\_")
.replace(/(png|jpg|jpeg|fz)$/i, "fits");
if( !fname.match(/.fits$/) ){
fname += ".fits";
}
} else {
fname = "js9.fits";
}
opts = opts || {};
if( typeof opts === "string" ){
try{ s = JSON.parse(opts); }
catch(e){ s = null; }
if( s ){ opts = s; }
}
// what do we save?
if( opts === "display" || opts.source === "display" ){
// save currently displayed section
sect = this.rgb.sect;
arr = this.toArray({notab: true, twoaxes: true, sect: sect});
} else if( opts === "virtual" || opts.source === "virtual" ){
if( this.raw.hdu && this.raw.hdu.fits && this.raw.hdu.fits.vfile ){
arr = JS9.vread(this.raw.hdu.fits.vfile, "binary");
} else {
JS9.error("no virtual file available to save");
}
} else {
// save entire image: first convert to array (with two axes)
arr = this.toArray({notab: true, twoaxes: true});
}
// convert array to blob
blob = new Blob([arr], {type: "application/octet-binary"});
// save to disk
JS9.saveAs(blob, fname);
} else {
JS9.error("no saveAs() available to save FITS file");
}
return fname;
};
// save image as an img file of specified type (e.g., image/png, image/jpeg)
JS9.Image.prototype.saveIMG = function(fname, type, opts){
let key, img, ctx, canvas, width, height, quality;
if( {}.hasOwnProperty.call(window, "saveAs") ){
// opts can be opts object or json string or quality value
if( typeof opts === "number" ){
quality = opts;
opts = null;
} else if( typeof opts === "string" ){
if( JS9.isNumber(opts) ){
quality = parseFloat(opts);
opts = null;
} else {
try{ opts = JSON.parse(opts); }
catch(e){ opts = null; }
}
if( opts ){
quality = opts.quality;
}
}
// opts is optional
opts = opts || {};
// filename is optional
fname = fname || "js9.png";
// save as specified type
type = type || "image/png";
// convenience params
width = this.display.width;
height = this.display.height;
// create off-screen canvas, into which we write all canvases
img = document.createElement("canvas");
img.setAttribute("width", width);
img.setAttribute("height", height);
ctx = img.getContext("2d");
// source can be image or display
if( opts.source === "image" ){
// image: save RGB image for this image, which will be different
// from the display, e.g., when blend mode is turned on
ctx.putImageData(this.rgb.img, 0, 0);
} else {
// display: save RGB image as seen on the display,
// e.g. a composite blended image
ctx.drawImage(this.display.canvas, 0, 0);
}
// add graphics layers, unless explicitly specified not to
if( opts.layers !== false ){
for( key of Object.keys(this.layers) ){
// each layer canvas
if( this.layers[key].dlayer.dtype === "main" &&
this.layers[key].show ){
canvas = this.layers[key].dlayer.canvasjq[0];
ctx.drawImage(canvas, 0, 0, width, height);
}
}
}
// sanity check on quality
if( JS9.notNull(quality) ){
if( quality < 0 || quality > 1 ){
quality = 0.95;
}
}
img.toBlob( (blob) => {
JS9.saveAs(blob, fname);
}, type, quality);
} else {
JS9.error("no saveAs() available for saving image");
}
return fname;
};
// save image as a PNG file
JS9.Image.prototype.savePNG = function(fname, opts){
fname = fname || "js9.png";
if( !fname.match(/\.png$/) ){
fname += ".png";
}
return this.saveIMG(fname, "image/png", opts);
};
// save image as a JPEG file
JS9.Image.prototype.saveJPEG = function(fname, opts){
fname = fname || "js9.jpg";
if( !fname.match(/\.jpg$/) && !fname.match(/\.jpeg$/) ){
fname += ".jpg";
}
return this.saveIMG(fname, "image/jpeg", opts);
};
// update (and display) pixel and wcs values (connected to info plugin)
JS9.Image.prototype.updateValpos = function(ipos, disp){
let val, vstr, vstr1, vstr2, vstr3, val3, i, c, d, p, s;
let cd1, cd2, v1, v2, units, sect;
let obj = null;
const sep1 = "\t ";
const sep2 = "\t\t ";
const sp = "    ";
const tf = (fval) => {
return JS9.floatFormattedString(fval, this.params.precision, 3);
};
const tr = (fval, length) => {
length = length || 3;
return fval.toFixed(length);
};
const ti = (ival, length) => {
let r = "";
let prefix = "";
length = length || 3;
if( ival < 0 ){
ival = Math.abs(ival);
prefix = "-";
}
r = r + ival;
while (r.length < length) {
r = `0${r}`;
}
return prefix + r;
};
// only do processing if valpos is turned on
if( this.params.valpos ){
// default is to display
if( disp === undefined ){
disp = true;
}
// if a cached valpos object exists, use it
// this is unset and reset in the mousemove callback
if( this.valpos ){
if( disp ){
this.display.displayMessage("info", this.valpos,
JS9.globalOpts.valposTarget);
}
return this.valpos;
}
// get image coordinates
i = {x: ipos.x, y: ipos.y, sys: "image"};
// get logical coordinates
p = this.imageToLogicalPos(ipos);
// get display coordinates
d = this.imageToDisplayPos(ipos);
d.sys = "display";
// get pixel coordinates in current logical coordinate system;
if( this.params.wcssys === "image" ){
c = i;
} else {
c = p;
}
// get image value: here we need 0-indexed display positions,
// so subtract the 0.5 of the image pixel
val = this.raw.data[Math.floor(ipos.y - 0.5) \* this.raw.width +
Math.floor(ipos.x - 0.5)];
// fix the significant digits in the value
switch(this.raw.bitpix){
case 8:
case 16:
case -16:
case 32:
val3 = ti(val);
break;
case -32:
case -64:
val3 = tf(val);
break;
default:
val3 = ti(val);
break;
}
// create the valpos string
vstr1 = val3;
vstr2 = `${tr(c.x, 3)} ${tr(c.y, 3)} (${c.sys})`;
if( JS9.globalOpts.valposDCoords && c.sys === "image" ){
vstr2 += `${sp}${tr(d.x, 3)} ${tr(d.y, 3)} (${d.sys})`;
}
vstr = vstr1 + sp + vstr2;
// object containing all information
obj = {ix: i.x, iy: i.y, ipos: tr(i.x, 2) + sep2 + tr(i.y, 2),
isys: "image",
px: p.x, py: p.y, ppos: tr(p.x, 2) + sep2 + tr(p.y, 2),
psys: "physical",
dx: d.x, dy: d.y, dpos: tr(d.x, 2) + sep2 + tr(d.y, 2),
dsys: "display",
cx: c.x, cy: c.y, cpos: tr(c.x, 2) + sep2 + tr(c.y, 2),
csys: c.sys,
ra: "", dec: "", wcspos: "", wcssys: "",
racen: "", deccen: "",
wcsfov: "", wcspix: "",
val: val, val3: val3,
id: this.id, file: this.file, object: this.object||""};
if( this.telescope || this.instrument ){
if( obj.object ){ obj.object += " "; }
obj.object += "(";
if( this.telescope ){
obj.object += this.telescope;
if( this.instrument ){
obj.object += ", ";
}
}
if( this.instrument ){
obj.object += this.instrument;
}
obj.object += ")";
}
// Define FOV and center in terms of pixels; will be redefined
// to WCS if WCS is available
sect = this.rgb.sect;
v1 = (sect.x1 - sect.x0).toFixed(0);
v2 = (sect.y1 - sect.y0).toFixed(0);
obj.wcsfovpix = `${v1} × ${v2} pix`;
obj.racen = (sect.x1 + sect.x0)/2;
obj.deccen = (sect.y1 + sect.y0)/2;
obj.wcscen = obj.racen + sep1 + obj.deccen;
// add wcs, if necessary
if( this.validWCS() && JS9.isWCSSys(this.params.wcssys) ){
s = JS9.pix2wcs(this.raw.wcs, ipos.x, ipos.y).trim().split(/\s+/);
vstr3 = `${s[0]} ${s[1]} (${s[2]||"wcs"})`;
vstr = vstr1 + sp + vstr3 + sp + vstr2;
// update object with wcs
obj.ra = s[0];
obj.dec = s[1];
obj.wcspos = s[0] + sep1 + s[1];
obj.wcssys = s[2];
if( this.raw.wcsinfo ){
cd1 = Math.abs(this.raw.wcsinfo.cdelt1);
cd2 = Math.abs(this.raw.wcsinfo.cdelt2);
v1 = 1/60;
if( this.raw.header.CUNIT1 ){
units = this.raw.header.CUNIT1;
}
if( !units || units.match(/^deg/i) ){
if( (cd1 >= 1) || (cd2 >= 1) ){
units = "deg";
} else if( (cd1 >= v1) || (cd2 >= v1) ){
units = "'";
cd1 \*= 60;
cd2 \*= 60;
} else {
units = '"';
cd1 \*= 3600;
cd2 \*= 3600;
}
}
sect = this.rgb.sect;
v1 = ((sect.x1 - sect.x0) \* cd1).toFixed(0);
v2 = ((sect.y1 - sect.y0) \* cd2).toFixed(0);
obj.wcsfov = `${v1}${units} × ${v2}${units}`;
v1 = tr(cd1 / sect.zoom, 3);
obj.wcspix = `${v1}${units}/pix`;
obj.wcsfovpix = `${obj.wcsfov} (${obj.wcspix})`;
s = JS9.pix2wcs(this.raw.wcs,
(sect.x1 + sect.x0)/2, (sect.y1 + sect.y0)/2)
.trim().split(/\s+/);
obj.racen = s[0];
obj.deccen = s[1];
obj.wcscen = s[0] + sep1 + s[1];
}
}
obj.vstrsmall = vstr1 + sp + vstr2;
obj.vstr = vstr;
obj.vstrmedium = vstr;
obj.vstrlarge = vstr + sp + this.file;
if( disp ){
this.display.displayMessage("info", obj,
JS9.globalOpts.valposTarget);
}
}
return obj;
};
// toggle display of value/position
JS9.Image.prototype.toggleValpos = function(){
this.params.valpos = !this.params.valpos;
if( !this.params.valpos ){
this.display.clearMessage();
}
};
// get color map name
JS9.Image.prototype.getColormap = function(){
if( this.cmapObj ){
return {colormap: this.cmapObj.name,
contrast: this.params.contrast,
bias: this.params.bias};
}
};
// set color map
// calling sequences:
// setColormap(name);
// setColormap(name, contrast, bias);
// setColormap(name, staticOpts);
// setColormap(contrast, bias);
// setColormap(staticOpts);
// setColormap("rgb");
// setColormap("invert");
// setColormap("reset");
JS9.Image.prototype.setColormap = function(...args){
let [arg, arg2, arg3] = args;
let arr;
const setCmap = (arg) => {
if( this.cmapObj ){
// unset rgb mode, if necessary
switch(this.cmapObj.name){
case "red":
if( this.display.rgb.rim === this ){
this.display.rgb.rim = null;
}
break;
case "green":
if( this.display.rgb.gim === this ){
this.display.rgb.gim = null;
}
break;
case "blue":
if( this.display.rgb.bim === this ){
this.display.rgb.bim = null;
}
break;
}
}
// remove previous static colormap
delete this.staticObj;
// add the new colormap
this.cmapObj = JS9.lookupColormap(arg);
this.params.colormap = this.cmapObj.name;
// for static colormaps, copy the static object (we might edit it)
if( this.cmapObj.type === "static" ){
this.staticObj = $.extend(true, {}, this.cmapObj);
}
// set rgb mode, if necessary
switch(arg){
case "red":
this.display.rgb.rim = this;
break;
case "green":
this.display.rgb.gim = this;
break;
case "blue":
this.display.rgb.bim = this;
break;
default:
break;
}
// new colormap, turn off image overlay
this.params.overlay = false;
};
const setContrastBias = (arg1, arg2) => {
arg1 = parseFloat(arg1);
if( !Number.isNaN(arg1) ){
this.params.contrast = arg1;
}
arg2 = parseFloat(arg2);
if( !Number.isNaN(arg2) ){
this.params.bias = arg2;
}
};
const setStatic = (a) => {
let i, j, color, dval;
for(i=0; i 0 && dval <= 1 ){
dval = dval \* 255;
}
color.alpha = dval;
}
break;
case 3:
// min and max
color.min = parseFloat(a[i][1]);
if( Number.isNaN(color.min) ){
color.min = -Infinity;
}
color.max = parseFloat(a[i][2]);
if( Number.isNaN(color.max) ){
color.max = Infinity;
}
break;
default:
break;
}
break;
}
}
}
// new colormap, turn off image overlay
this.params.overlay = false;
}
// is this core service disabled?
// (only if the colormap has been set at least once!)
if( $.inArray("colormap", this.params.disable) >= 0 && this.cmapObj ){
return;
}
switch(args.length){
case 1:
switch(arg){
case "rgb":
this.display.rgb.active = !this.display.rgb.active;
break;
case "overlay":
if( this.offscreen ){
this.params.overlay = !this.params.overlay;
}
break;
case "invert":
this.params.invert = !this.params.invert;
break;
case "reset":
this.params.invert = JS9.imageOpts.invert;
this.params.contrast = JS9.imageOpts.contrast;
this.params.bias = JS9.imageOpts.bias;
break;
default:
if( this.cmapObj && this.cmapObj.type === "static" ){
if( $.isArray(arg) ){
setStatic(arg);
} else if( typeof arg === "string" && arg.charAt(0) === '[' ){
try{
arr = JSON.parse(arg);
setStatic(arr);
}
catch(e){
JS9.error(`can't parse JSON in setColormap: ${arg}`, e);
}
} else {
setCmap(arg);
}
} else if( typeof arg === "string" ){
setCmap(arg);
}
break;
}
break;
case 2:
if( JS9.isNumber(arg) && JS9.isNumber(arg2) ){
setContrastBias(arg, arg2);
} else if( this.cmapObj && this.cmapObj.type === "static" ){
setCmap(arg);
setStatic(arg2);
}
break;
case 3:
setCmap(arg);
setContrastBias(arg2, arg3);
break;
default:
break;
}
this.displayImage("colors");
// hack: delete filterRGBImage from stash to avoid restore during reproject
this.xeqStashDiscard("filterRGBImage");
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetcolormap");
}
return this;
};
// get scale factor
JS9.Image.prototype.getScale = function(){
if( this.params.scale ){
return {scale: this.params.scale,
scalemin: this.params.scalemin,
scalemax: this.params.scalemax,
scaleclipping: this.params.scaleclipping};
}
};
// set scale factor
JS9.Image.prototype.setScale = function(...args){
let [s0, s1, s2] = args;
const newscale = (s) => {
if( JS9.scales.includes(s) ){
this.params.scale = s;
} else if( s === "dataminmax" ){
this.params.scaleclipping = "dataminmax";
this.params.scalemin = this.raw.dmin;
this.params.scalemax = this.raw.dmax;
} else if( s === "zscale" ){
if( (this.params.z1 === undefined) ||
(this.params.z2 === undefined) ){
this.zscale(false);
}
this.params.scaleclipping = "zscale";
this.params.scalemin = this.params.z1;
this.params.scalemax = this.params.z2;
} else if( s === "zmax" ){
if( (this.params.z1 === undefined) ){
this.zscale(false);
}
this.params.scaleclipping = "zmax";
this.params.scalemin = this.params.z1;
this.params.scalemax = this.raw.dmax;
} else if( s === "user" ){
this.params.scaleclipping = "user";
} else {
JS9.error(`unknown scale: ${s}`);
}
};
// is this core service disabled?
if( $.inArray("scale", this.params.disable) >= 0 ){
return;
}
if( args.length ){
switch(args.length){
case 1:
newscale(s0);
break;
case 2:
this.params.scalemin = parseFloat(s0);
this.params.scalemax = parseFloat(s1);
this.params.scaleclipping = "user";
break;
default:
newscale(s0);
if( (s0 !== "zscale") && (s0 !== "zmax") ){
this.params.scalemin = parseFloat(s1);
this.params.scalemax = parseFloat(s2);
this.params.scaleclipping = "user";
}
break;
}
this.params.precision =
JS9.floatPrecision(this.params.scalemin, this.params.scalemax);
this.displayImage("colors");
}
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetscale");
}
return this;
};
// get opacity factor
JS9.Image.prototype.getOpacity = function(){
let obj = {};
if( JS9.notNull(this.params.opacity) ){
obj.opacity = this.params.opacity;
} else {
obj.opacity = 1;
}
if( JS9.notNull(this.params.flooropacity) ){
obj.flooropacity = this.params.flooropacity;
obj.floorvalue = this.params.floorvalue;
}
return obj;
};
// set opacity factor:
// set default opacity for all pixels
// setOpacity(0.9)
// set opacity floor: for pixel values <= 1st arg assign 2nd arg as opacity
// setOpacity(5, 0.2)
// set default opacity, for pixel values <= 2nd arg, assign 3rd arg as opacity
// setOpacity(0.9, 5, 0.2)
// reset default opacity to 1
// setOpacity("reset")
// remove opacity floor
// setOpacity("resetfloor")
// reset default opacity to 1, remove opacity floor
// setOpacity("resetall")
JS9.Image.prototype.setOpacity = function(...args){
let [a1, a2, a3] = args;
// is this core service disabled?
if( $.inArray("opacity", this.params.disable) >= 0 ){
return;
}
if( args.length ){
switch(args.length){
case 1:
if( typeof a1 === "string" ){
if( a1.toLowerCase() === "reset" ){
this.params.opacity = 1;
} else if( a1.toLowerCase() === "resetfloor" ){
delete this.params.floorvalue;
delete this.params.flooropacity;
} else if( a1.toLowerCase() === "resetall" ){
this.params.opacity = 1;
delete this.params.floorvalue;
delete this.params.flooropacity;
}
} else if( JS9.isNumber(a1) ){
this.params.opacity = parseFloat(a1);
}
break;
case 2:
if( JS9.isNumber(a1) && JS9.isNumber(a2) ){
this.params.floorvalue = parseFloat(a1);
this.params.flooropacity = parseFloat(a2);
}
break;
case 3:
if( JS9.isNumber(a1) ){
this.params.opacity = parseFloat(a1);
}
if( JS9.isNumber(a2) && JS9.isNumber(a3) ){
this.params.floorvalue = parseFloat(a2);
this.params.flooropacity = parseFloat(a3);
}
break;
default:
break;
}
// if we just set opacity (not reset), it must mean we want to use it,
// so turn off opacity masking, if necessary
if( typeof a1 === "number" ||
(typeof a1 === "string" && !a1.match(/reset/)) ){
if( this.mask.active && this.mask.im ){
this.mask.active = false;
}
}
this.displayImage("colors");
}
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onsetopacity");
}
return this;
};
// get an image param value
JS9.Image.prototype.getParam = function(param){
// sanity check
if( !param ){ return null; }
// return param object
if( param === "all" ){
return this.params;
}
// return value
return this.params[param];
};
// set an image param value
JS9.Image.prototype.setParam = function(param, value){
let i, idx, ovalue, obj;
const getval = (s) => {
if( s === "true" ){
return true;
}
if( s === "false" ){
return false;
}
if( !JS9.isNumber(s) ){
return s;
}
return parseFloat(s);
};
// sanity check
if( !param ){ return null; }
// convert strings to values
value = getval(value);
// merge in new params
if( param === "all" && typeof value === "object" ){
$.extend(true, this.params, value);
// call core methods as needed
if( value.colormap || value.contrast || value.bias ){
obj = this.getColormap();
value.colormap = value.colormap || obj.colormap;
value.contrast = value.contrast || obj.contrast;
value.bias = value.bias || obj.bias;
this.setColormap(value.colormap, value.contrast, value.bias);
}
if( value.scale || value.scalemin || value.scalemax ){
obj = this.getScale();
value.scale = value.scale || obj.scale;
value.scalemin = value.scalemin || obj.scalemin;
value.scalemax = value.scalemax || obj.scalemax;
this.setScale(value.scale, value.scalemin, value.scalemax);
}
if( value.flip ){
this.setFlip("reset");
this.setFlip(value.flip);
}
if( value.rot90 ){
this.setRot90("reset");
this.setRot90(value.rot90);
}
if( value.rotate ){
this.setRotate("reset");
this.setRotate(value.rotate);
}
if( value.invert ){
this.params.invert = value.invert;
this.displayImage("colors");
}
if( value.zoom ){
this.setZoom(value.zoom);
}
if( value.wcssys ){
this.setWCSSys(value.wcssys);
}
if( value.wcsunits ){
this.setWCSUnits(value.wcsunits);
}
return this.params;
} else if( param === "disable" ){
if( !$.isArray(value) ){
value = [value];
}
for(i=0; i= 0 ){
this.params.disable.splice(idx, 1);
}
}
return this.params.disable;
}
// save old value
ovalue = this.params[param];
// set new value
this.params[param] = value;
// call core methods as needed
switch(param){
case "colormap":
this.setColormap(value);
break;
case "invert":
this.displayImage("colors");
break;
case "contrast":
obj = this.getColormap();
this.setColormap(obj.colormap, value, obj.bias);
break;
case "bias":
obj = this.getColormap();
this.setColormap(obj.colormap, obj.contrast, value);
break;
case "overlay":
this.displayImage("colors");
break;
case "flip":
this.setFlip("reset");
this.setFlip(value);
break;
case "rot90":
this.setRot90("reset");
this.setRot90(value);
break;
case "rotate":
this.setRotate("reset");
this.setRotate(value);
break;
case "scale":
this.setScale(value);
break;
case "scalemin":
obj = this.getScale();
this.setScale("user", value, obj.scalemax);
break;
case "scalemax":
obj = this.getScale();
this.setScale("user", obj.scalemin, value);
break;
case "scaleclipping":
obj = this.getScale();
this.setScale(value, obj.scalemin, obj.scalemax);
break;
case "wcssys":
this.setWCSSys(value);
break;
case "wcsunits":
this.setWCSUnits(value);
break;
case "zoom":
this.setZoom(value);
break;
}
// return old value
return ovalue;
};
// copy params from one image to another
JS9.Image.prototype.copyParams = function(params, images, opts){
let i, j, im, param, val;
let xims = [];
// sanity check
if( !params ){ return; }
// opts is optional
opts = opts || {};
if( typeof params === "string" && params.charAt(0) === '[' ){
try{ params = JSON.parse(params); }
catch(e){ JS9.error(`can't parse JSON in copyParams: ${params}`, e); }
}
if( !$.isArray(params) ){ params = [params]; }
// do regions first to avoid problems with changes to the current image
i = $.inArray("regions", params);
if( i >= 0 ){
params.splice(i, 1);
params.unshift("regions");
}
// default is all images
images = images || JS9.images;
if( typeof images === "string" && images.charAt(0) === '[' ){
try{ images = JSON.parse(images); }
catch(e){ JS9.error(`can't parse JSON in copyParams: ${images}`, e); }
}
if( !$.isArray(images) ){ images = [images]; }
// for each image
for(i=0; i 0 ){
// integer data: BLANK header value specifies data value to ignore
if( raw.header.BLANK !== undefined ){
blankval = raw.header.BLANK;
for(i=0; i raw.dmax ){ raw.dmax = val; }
}
}
} else {
for(i=0; i raw.dmax ){ raw.dmax = val; }
}
}
} else {
// float data: ignore NaN, infinity
for(i=0; i raw.dmax ){ raw.dmax = val; }
}
}
}
}
// re-set scaling values, if necessary
if( reminscale ){ params.scalemin = raw.dmin; }
if( remaxscale ){ params.scalemax = raw.dmax; }
// set new precision
params.precision = JS9.floatPrecision(params.scalemin, params.scalemax);
// allow chaining
return this;
};
// the zscale calculation
JS9.Image.prototype.zscale = function(setvals){
let s, rawdata, bufsize, buf, vals;
// sanity check
if( !JS9.zscale || !this.raw || !this.raw.data ){ return this; }
rawdata = this.raw.data;
// allocate space for the image in the emscripten heap
bufsize = rawdata.length \* rawdata.BYTES\_PER\_ELEMENT;
try{ buf = JS9.vmalloc(bufsize); }
catch(e){ JS9.error(`image too large for zscale malloc: ${bufsize}`, e); }
// copy the raw image data to the heap
// try{ JS9.vheap.set(new Uint8Array(rawdata.buffer), buf); }
try{ JS9.vmemcpy(new Uint8Array(rawdata.buffer), buf); }
catch(e){ JS9.error(`can't copy image to zscale heap: ${bufsize}`, e); }
// call the zscale routine
s = JS9.zscale(buf,
this.raw.width,
this.raw.height,
this.raw.bitpix,
this.params.zscalecontrast,
this.params.zscalesamples,
this.params.zscaleline);
// free emscripten heap space
JS9.vfree(buf);
// clean up return values
vals = s.trim().split(/\s+/);
// save z1 and z2
this.params.z1 = parseFloat(vals[0]);
this.params.z2 = parseFloat(vals[1]);
// make z1 and z2 the scale clip values, if necessary
if( setvals === "zmax" ){
this.params.scalemin = this.params.z1;
this.params.scalemax = this.raw.dmax;
} else if( setvals ){
this.params.scalemin = this.params.z1;
this.params.scalemax = this.params.z2;
}
this.params.precision =
JS9.floatPrecision(this.params.scalemin, this.params.scalemax);
// allow chaining
return this;
};
// background-subtracted counts in regions
// eslint-disable-next-line no-unused-vars
JS9.Image.prototype.countsInRegions = function(...args){
let i, s, vfile, bvfile, sect, ext, filter, bin, opts, cmdswitches;
let sregions = "field";
let bregions = "";
const getreg = (arg, def) => {
let ii, rarr, reg, narg;
const regrexp= /(annulus|box|circle|ellipse|line|polygon|point|text) \*\(/;
// if we have no region, we're done
if( !arg ){
return def;
}
if( typeof arg === "string" ){
narg = this.expandMacro(arg);
// if we have no region, we're done
if( !narg ){
return def;
}
// if its a known region, we're done
if( narg.match(regrexp) ){
return narg;
}
}
// look for a region specifier
rarr = this.getShapes("regions", arg);
// no region are returned: this is an error
if( !rarr || !rarr.length ){
JS9.error(`no regions found: ${arg}`);
}
// compose a region string from the returned regions
narg = "";
for(ii=0; ii 1 ){
if( this.imtab === "table" ){
// for tables, regcnts has a -b switch
cmdswitches += ` -b ${bin}`;
} else {
// for images, make a temporary binned file
bvfile = `bin${bin}\_${vfile.split("/").reverse()[0]}`;
sect = `0@0,0@0,${bin}`;
JS9.imsection(vfile, bvfile, sect, "");
vfile = bvfile;
}
}
}
// could take a while ...
JS9.waiting(true, this.display);
// call low-level regcnts
s = JS9.regcnts(vfile, sregions, bregions, cmdswitches);
// all done waiting
JS9.waiting(false);
// remove binned file, if necessary
if( bvfile ){
JS9.vunlink(bvfile);
}
// check for regions or cfitio errors
if( s.match(/^ERROR/) || s.match(/FITSIO status/) ){
JS9.error(s);
}
// display in a lightwin, if necessary
if( opts.lightwin ){
// display counts in a light window
this.displayAnalysis("text", s, {divid: JS9.globalOpts.analysisDiv});
}
// return results, including errors
return s;
};
// radial profile plot
// eslint-disable-next-line no-unused-vars
JS9.Image.prototype.radialProfile = function(...args){
let i, s, xlabel, ylabel, obj, cobj, pobj, res, el, opts;
let color, errorbars, errorcolor;
const carr = [];
const swobj = {cmdswitches: "-G -j -r"};
// make up arg list, add required radial profile switches to opts
for(i=0; i res.radius2 ){
JS9.error("radial profile source region must be an annulus");
}
el = [(res.radius1 + res.radius2)/2, res.surfBrightness, res.surfError];
pobj.data.push(el);
}
// display results
return this.displayAnalysis("plot", pobj,
{divid: JS9.globalOpts.analysisDiv});
};
// plot of a 3D cube a region
// eslint-disable-next-line no-unused-vars
JS9.Image.prototype.plot3d = function(src, bkg, opts){
let i, j, s, arr, jobj, el, pobj, color, mode, divid, xlabel, ylabel;
let index3, xoff, xdelt;
const counts=[];
if( !this.raw.header || this.raw.header.NAXIS !== 3 ){
JS9.error("plot3d requires a data cube with 3 dimensions");
}
// opts is optional
opts = $.extend(true, {}, opts, JS9.globalOpts.plot3d);
// slice
opts.cube = opts.cube || "\*:\*:all";
// make sure 'all' is specified
arr = opts.cube.split(":");
for(i=0; i return name of current raw
if( !args.length ){
return this.raw.id;
}
// opts is optional
opts = opts || {};
// opts is a string with second arg a func: generate opts object
// opts is a string, no func: switch to a different raw data layer
// opts is a string + "remove": remove specified layer
if( typeof opts === "string" ){
if( typeof func === "function" ){
// change: rawDataLayer(id, func) to rawDataLater(obj, func)
opts = {rawid: opts};
} else {
id = opts;
mode = func;
// look for raw layer with the specified id
for(i=0; i= 0 ){
this.raws[cur] = nraw;
} else {
this.raws.push(nraw);
}
// assign this nraw to the high-level raw data object
this.raw = nraw;
// renew bitpix, if necessary
if( this.raw.header.bitpix ){
this.raw.bitpix = this.raw.header.bitpix;
}
// re-calculate min and max, if necesary
if( opts.dataminmax !== false ){
this.dataminmax();
}
// re-init coordinate systems, if necessary
if( opts.updatewcs ){
// init WCS, if possible
this.initWCS();
// init the logical coordinate system, if possible
this.initLCS();
}
// reset pan, if necessary
if( opts.resetpan ){
this.setPan();
}
// refresh shape layers
this.refreshLayers();
// redisplay using these data
this.displayImage("all", opts);
// redo flip and rot
this.reFlipRot();
}
return true;
};
// perform a gaussian blur on the raw data
// creates a new raw data layer ("gaussBlur")
JS9.Image.prototype.gaussBlurData = function(sigma, opts){
if( sigma === undefined ){
JS9.error("missing sigma value for gaussBlurData");
}
// save value
this.params.sigma = sigma;
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse gaussBlur opts: ${opts}`, e); }
}
// the blurred image will be floating point
if( this.raw.bitpix === -64 ){
opts.bitpix = -64;
} else {
opts.bitpix = -32;
}
// use origin of current
opts.oraw = "current0";
// nraw should be a floating point copy of oraw
opts.alwaysCopy = true;
// new layer
opts.rawid = opts.rawid || "gaussBlur";
// pass the options
opts.sigma = sigma;
// save this routine so it can be reconstituted in a restored session
this.xeqStashSave("gaussBlurData", [sigma], opts.rawid);
// call routine to generate (or modify) the new layer
this.rawDataLayer(opts, (oraw, nraw) => {
let tdata;
// nraw contains a floating point copy of oraw
// make a temporary copy of nraw data for calculations
switch(nraw.bitpix){
case -32:
tdata = new Float32Array(nraw.data);
break;
case -64:
tdata = new Float64Array(nraw.data);
break;
default:
JS9.error(`invalid temp bitpix for gaussBlur: ${nraw.bitpix}`);
break;
}
// the heart of the matter!
gaussBlur(tdata, nraw.data, nraw.width, nraw.height, sigma);
return true;
});
// allow chaining
return this;
};
// perform arithmetic operations on the raw data
// creates a new raw data layer ("imarith")
JS9.Image.prototype.imarithData = function(...args){
let im;
let [op, arg1, opts] = args;
// no args means return the available ops
if( !args.length ){
return ["add", "sub", "mul", "div", "min", "max", "reset"];
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse imarith opts: ${opts}`, e); }
}
opts.rawid = opts.rawid || "imarith";
// special case: reset by deleting the layer
if( (op === "reset") || (op === "remove") ){
this.rawDataLayer(opts.rawid, "remove");
return;
}
// sanity check
if( op === undefined || arg1 === undefined ){
JS9.error("missing arg(s) for image arithmetic");
}
// save this routine so it can be reconstituted in a restored session
this.xeqStashSave("imarithData", args.slice(), opts.rawid);
// operation: add, sub, mul, div ...
switch(op){
case "add":
case "sub":
case "mul":
case "div":
case "min":
case "max":
opts.op = op;
break;
default:
JS9.error(`invalid operator for image arithmetic: ${op}`);
break;
}
// arg1: can be an image object or a numeric value
if( typeof arg1 === "object" ){
if( (this.raw.width !== arg1.raw.width) ||
(this.raw.height !== arg1.raw.height) ){
JS9.error("images must be the same size for image arithmetic");
}
opts.argtype = "image";
opts.argval = arg1;
} else if( JS9.isNumber(arg1) ){
opts.argtype = "value";
opts.argval = arg1;
} else {
// lookup the image by name
im = JS9.lookupImage(arg1);
if( !im ){
JS9.error(`imarith arg1 must be an image or a constant: ${arg1}`);
}
opts.argval = im;
opts.argtype = "image";
}
// check for invalid args
if( (opts.op === "div") &&
(opts.argtype === "value") && (opts.argval === 0) ){
JS9.error("imarith can't divide by zero (nor can anyone else)");
}
// choose a decent bitpix
if( !opts.bitpix ){
switch(opts.argtype){
case "image":
if( (this.raw.bitpix > 0) && (opts.argval.raw.bitpix > 0) ){
opts.bitpix = Math.max(this.raw.bitpix, opts.argval.raw.bitpix);
} else if( (this.raw.bitpix < 0) && (opts.argval.raw.bitpix < 0) ){
opts.bitpix = Math.min(this.raw.bitpix, opts.argval.raw.bitpix);
} else if( (this.raw.bitpix < 0) && (opts.argval.raw.bitpix > 0) ){
opts.bitpix = this.raw.bitpix;
} else {
opts.bitpix = opts.argval.raw.bitpix;
}
break;
case "value":
if( this.raw.bitpix === -64 ){
opts.bitpix = -64;
} else {
opts.bitpix = -32;
}
break;
}
}
// nraw should be a opts.bitpix copy of oraw
opts.alwaysCopy = true;
// use current
opts.oraw = "current";
// call routine to generate (or modify) the new layer
this.rawDataLayer(opts, (oraw, nraw, opts) => {
let i, val;
switch(opts.argtype){
case "image":
val = opts.argval.raw.data;
switch(opts.op){
case "add":
for(i=0; i {
let i, oi, oj, ni, nj, nlen, oU8, nU8, ooff, noff, blankval;
const bpp = oraw.data.BYTES\_PER\_ELEMENT;
if( nraw.xoff === undefined ){
nraw.xoff = 0;
}
if( nraw.yoff === undefined ){
nraw.yoff = 0;
}
nraw.xoff += opts.x;
nraw.yoff += opts.y;
if( !opts.fill || opts.fill === "clear" ){
if( nraw.bitpix > 0 ){
blankval = opts.blank || nraw.header.BLANK || 0;
nraw.header.BLANK = blankval;
} else {
blankval = NaN;
}
if( typeof nraw.data.fill === "function" ){
nraw.data.fill(blankval);
} else {
for(i=0; i= oraw.height) ){
continue;
}
oi = 0;
ni = oi + nraw.xoff;
nlen = oraw.width;
if( ni < 0 ){
oi -= ni;
nlen += ni;
ni = 0;
}
if( (ni + nlen) > oraw.width ){
nlen -= (ni + nlen) - oraw.width;
}
if( nlen <= 0 ){
return false;
}
ooff = (oj \* oraw.width + oi) \* bpp;
oU8 = new Uint8Array(oraw.data.buffer, ooff, nlen \* bpp);
noff = (nj \* oraw.width + ni) \* bpp;
nU8 = new Uint8Array(nraw.data.buffer, noff, nlen \* bpp);
nU8.set(oU8);
}
return true;
});
// allow chaining
return this;
};
// rotate image by changing WCS info and calling reprojectData
// creates a new raw data layer ("rotate")
// angle is in degrees (since CROTA2 is in degrees)
JS9.Image.prototype.rotateData = function(...args){
let raw, oheader, nheader, arad, sinrot, cosrot, pos, arr;
let ocdelt1 = 0.0;
let ocdelt2 = 0.0;
let [angle, opts] = args;
// sanity checks
if( !this.raws || !this.raws[0] ){
JS9.error("no raw data for reprojection");
}
// go back to original data for reprojection
raw = this.raws[0];
if( !raw.header || !raw.wcsinfo ){
JS9.error("no WCS info available for reprojection");
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse rotate opts: ${opts}`, e); }
}
// save stash name
opts.stash = "rotateData";
// but make sure we can set the id
opts.rawid = "rotate";
// rotate raw data
opts.oraw = JS9.RAWID0;
// maintain current section, unless specified otherwise
if( opts.resetSection !== true ){
opts.resetSection = false;
}
// old and new header
oheader = raw.header;
nheader = $.extend(true, {}, oheader);
// rotate around current center or file center (i.e., CRPIX1,2)
opts.center = opts.center || JS9.globalOpts.rotationCenter;
if( opts.center !== "file" && this.validWCS() ){
pos = this.getPan();
arr = JS9.pix2wcs(this.raw.wcs, pos.x, pos.y).trim().split(/\s+/);
if( arr && arr.length > 1 ){
nheader.CRPIX1 = pos.x;
nheader.CRPIX2 = pos.y;
nheader.CRVAL1 = JS9.saostrtod(arr[0]);
if( JS9.isHMS(this.params.wcssys) ){
nheader.CRVAL1 \*= 15.0;
}
nheader.CRVAL2 = JS9.saostrtod(arr[1]);
}
}
// normalized values from wcslib
if( raw.wcsinfo ){
ocdelt1 = raw.wcsinfo.cdelt1 || 0;
ocdelt2 = raw.wcsinfo.cdelt2 || 0;
}
// string directives instead of a numeric angle
if( typeof angle === "string" ){
switch(angle.toLowerCase()){
case "northisup":
case "northup":
angle = 0;
if( ocdelt1 > 0 ){ ocdelt1 = -ocdelt1; }
if( ocdelt2 < 0 ){ ocdelt2 = -ocdelt2; }
break;
default:
angle = parseInt(angle, 10);
break;
}
}
// new header same as old, but with a changed angle
// make up new WCS keywords
// use CD matrix if possible, else set CROTA2
if( JS9.notNull(oheader.CD1\_1) ){
arad = -(angle \* Math.PI / 180.0);
sinrot = Math.sin(arad);
cosrot = Math.cos(arad);
nheader.CD1\_1 = oheader.CD1\_1 \* cosrot + oheader.CD1\_2 \* sinrot;
nheader.CD1\_2 = oheader.CD1\_1 \* -sinrot + oheader.CD1\_2 \* cosrot;
nheader.CD2\_1 = oheader.CD2\_1 \* cosrot + oheader.CD2\_2 \* sinrot;
nheader.CD2\_2 = oheader.CD2\_1 \* -sinrot + oheader.CD2\_2 \* cosrot;
} else {
nheader.CROTA2 = angle;
nheader.CDELT1 = ocdelt1;
nheader.CDELT2 = ocdelt2;
}
// flag that we will use CROTA2 to modify LTM matrix
// needed because Montage does not know about LTM
opts.lcsUseRota2 = true;
// save ptype if possible
if( raw.wcsinfo ){
nheader.ptype = raw.wcsinfo.ptype;
}
// save this routine so it can be reconstituted in a restored session
this.xeqStashSave("rotateData", args.slice(), opts.rawid);
// rotate by reprojecting the data
return this.reprojectData(nheader, opts);
};
// low-level reprojection: creates reprojected file, but does not display it
// instead, it returns the name of the reprojected FITS file (emscripten vfile)
// this is the basis for reprojectData, but can be used in other routines which
// require a reprojection
JS9.Image.prototype.reproject = function(wcsim, opts){
let awvfile, awvfile2, wvfile, owvfile;
let wcsheader, wcsstr, oheader, nheader, theader;
let arr, ivfile, ovfile, rstr, key;
let tab, tx1, tx2, ty1, ty2, s;
let n, raw, avfile, earr, cmdswitches;
let i, tid, traw, maxx, maxy, maxpix;
let rcomplete = false;
const twcs = {};
const wcsexp = /SIMPLE|BITPIX|NAXIS|NAXIS[1-4]|AMDX|AMDY|CD[1-2]\_[1-2]|CDELT[1-4]|CNPIX[1-4]|CO1\_[1-9][0-9]|CO2\_[1-9][0-9]|CROTA[1-4]|CRPIX[1-4]|CRVAL[1-4]|CTYPE[1-4]|CUNIT[1-4]|DATE|DATE\_OBS|DC-FLAG|DEC|DETSEC|DETSIZE|EPOCH|EQUINOX|EQUINOX[a-z]|IMAGEH|IMAGEW|LATPOLE|LONGPOLE|MJD-OBS|PC00[1-4]00[1-4]|PC[1-4]\_[1-4]|PIXSCALE|PIXSCAL[1-2]|PLTDECH|PLTDECM|PLTDECS|PLTDECSN|PLTRAH|PLTRAM|PLTRAS|PPO|PROJP[1-9]|PROJR0|PV[1-3]\_[1-3]|PV[1-4]\_[1-4]|RA|RADECSYS|SECPIX|SECPIX|SECPIX[1-2]|UT|UTMID|VELOCITY|VSOURCE|WCSAXES|WCSDEP|WCSDIM|WCSNAME|XPIXSIZE|YPIXSIZE|ZSOURCE|LTM|LTV/;
const ptypeexp = /TAN|SIN|ZEA|STG|ARC/;
const addwcsinfo = (header, wcsinfo) => {
let theader;
if( !wcsinfo ){ return header; }
theader = $.extend(true, {}, header);
if( JS9.isNull(theader.CRVAL1) && !JS9.isNull(wcsinfo.crval1) ){
theader.CRVAL1 = wcsinfo.crval1;
}
if( JS9.isNull(theader.CRVAL2) && !JS9.isNull(wcsinfo.crval2) ){
theader.CRVAL2 = wcsinfo.crval2;
}
if( JS9.isNull(theader.CRPIX1) && !JS9.isNull(wcsinfo.crpix1) ){
theader.CRPIX1 = wcsinfo.crpix1;
}
if( JS9.isNull(theader.CRPIX2) && !JS9.isNull(wcsinfo.crpix2) ){
theader.CRPIX2 = wcsinfo.crpix2;
}
if( JS9.isNull(theader.CDELT1) && !JS9.isNull(wcsinfo.cdelt1) ){
theader.CDELT1 = wcsinfo.cdelt1;
}
if( JS9.isNull(theader.CDELT2) && !JS9.isNull(wcsinfo.cdelt2) ){
theader.CDELT2 = wcsinfo.cdelt2;
}
if( JS9.isNull(theader.CROTA2) && !JS9.isNull(wcsinfo.crot) ){
theader.CROTA2 = wcsinfo.crot;
}
return theader;
};
// sanity checks
if( !JS9.reproject || !wcsim || this === wcsim ){ return; }
if( !this.raws || !this.raws[0] ){
JS9.error("no raw data for reprojection");
}
// go back to original data for reprojection
raw = this.raws[0];
if( !raw.header || !raw.wcsinfo ){
JS9.error("no WCS info available for reprojection");
}
// opts is optional
opts = opts || {};
// make copy of input header, removing wcs keywords
oheader = $.extend(true, {}, raw.header);
for( key of Object.keys(oheader) ){
if( wcsexp.test(key) ){
delete oheader[key];
}
}
if( typeof wcsim === "object" ){
// get wcs keywords from new header
if( wcsim.raw && wcsim.raw.header ){
nheader = wcsim.raw.header;
} else if( wcsim.BITPIX && wcsim.NAXIS1 && wcsim.NAXIS2 ){
// assume its a WCS header
nheader = wcsim;
} else {
JS9.error("invalid wcs object input to reproject()");
}
for( key of Object.keys(nheader) ){
if( wcsexp.test(key) ){
twcs[key] = nheader[key];
}
}
// combine new wcs keywords + old header keywords
wcsheader = $.extend(true, {}, twcs, oheader);
// sanity check on result
if( !wcsheader.NAXIS || !wcsheader.NAXIS1 || !wcsheader.NAXIS2 ){
// JS9.error("invalid FITS image header");
return;
}
// restrict size of reprojection
wcsheader.NAXIS1 = Math.min(wcsheader.NAXIS1,
JS9.globalOpts.image.xdim);
wcsheader.NAXIS2 = Math.min(wcsheader.NAXIS2,
JS9.globalOpts.image.ydim);
// convert reprojection header to a string
wcsstr = JS9.raw2FITS(wcsheader, {addcr: true});
// create vfile text file containing reprojection WCS
wvfile = `wcs\_${JS9.uniqueID()}.txt`;
JS9.vfile(wvfile, wcsstr);
// check limits on reprojection, if necessary
if( JS9.globalOpts.reprojectLimits ){
// reprojection limits
maxx = JS9.globalOpts.image.xdim;
maxy = JS9.globalOpts.image.ydim;
// check max image dimension
maxpix = JS9.globalOpts.image.xdim \* JS9.globalOpts.image.ydim;
// keep within the limits of current memory constraints, or die
if( (raw.header.NAXIS1 \* raw.header.NAXIS2) > maxpix ){
JS9.error(`the max reproject size is ${maxx} \* ${maxy}. You can use the Bin/Filter/Section plugin to extract a section, then save it as FITS and reproject the smaller image.`);
}
}
} else {
wvfile = wcsim;
}
// check input and reproj WCS to make sure we can run fast mProjectPP
// if not, try to make an alternate WCS header amenable to mProjectPP
try{
// try to change input WCS to a sys usable by mProjectPP
if( !ptypeexp.test(raw.wcsinfo.ptype) ){
theader = addwcsinfo(raw.header, raw.wcsinfo);
owvfile = `owcs\_${JS9.uniqueID()}.txt`;
JS9.vfile(owvfile, JS9.raw2FITS(theader, {addcr: true}));
awvfile = `awcs\_${JS9.uniqueID()}.txt`;
rstr = JS9.tanhdr(owvfile, awvfile, "");
if( JS9.DEBUG > 1 ){
JS9.log("tanhdr (input): %s %s -> %s",
owvfile, awvfile, rstr);
}
JS9.vunlink(owvfile);
if( rstr.search(/\[struct stat="OK"/) >= 0 ){
// add command switch to use this alternate wcs
opts.cmdswitches = opts.cmdswitches || "";
opts.cmdswitches += ` -i ${awvfile}`;
}
}
// try to change reproject WCS to a sys usable by mProjectPP
if( (wcsim.raw && !ptypeexp.test(wcsim.raw.wcsinfo.ptype)) ||
(wcsim.ptype && !ptypeexp.test(wcsim.ptype)) ){
theader = addwcsinfo(nheader, wcsim.raw.wcsinfo);
owvfile = `owcs\_${JS9.uniqueID()}.txt`;
JS9.vfile(owvfile, JS9.raw2FITS(theader, {addcr: true}));
awvfile2 = `awcs\_${JS9.uniqueID()}.txt`;
rstr = JS9.tanhdr(owvfile, awvfile2, "");
if( JS9.DEBUG > 1 ){
JS9.log("tanhdr (reproj): %s %s -> %s",
owvfile, awvfile2, rstr);
}
JS9.vunlink(owvfile);
if( rstr.search(/\[struct stat="OK"/) >= 0 ){
// delete old wcs file and use this alternate wcsfile
JS9.vunlink(wvfile);
wvfile = awvfile2;
}
}
}
catch(ignore){ /\* empty \*/ }
// get reference to existing raw data file (or create one)
if( raw.hdu && raw.hdu.fits.vfile ){
// input file name
ivfile = raw.hdu.fits.vfile;
// add extension name or number
if( raw.hdu.fits.extname ){
ivfile += `[${raw.hdu.fits.extname}]`;
} else if( raw.hdu.fits.extnum &&
(raw.hdu.fits.extnum > 0) ){
ivfile += `[${raw.hdu.fits.extnum}]`;
}
} else {
// input file name
arr = this.toArray();
ivfile = this.id.replace(/\.png$/, "\_png" + ".fits");
JS9.vfile(ivfile, arr);
}
// output file name
s = this.id
.replace(/\[.\*\]/, "")
.replace(/\.png$/i, ".fits")
.replace(/\.fz$/i, "")
.replace(/\.gz$/i, "");
ovfile = `reproj\_${JS9.uniqueID()}\_${s}`;
// remove previous vfile for this reprojection layer, if possible
tid = opts.rawid || "reproject";
for(i=0; i= 0 ){
avfile = `${ovfile.substring(0, n)}\_area${ovfile.substring(n)}`;
}
// optional command line args
cmdswitches = opts.cmdswitches || "";
// no area file, but add global switches for reproject processing
cmdswitches += ` -a 0 ${JS9.globalOpts.reprojSwitches}`;
// call reproject
rstr = JS9.reproject(ivfile, ovfile, wvfile, cmdswitches);
if( JS9.DEBUG > 1 ){
JS9.log("reproject: %s %s %s [%s] -> %s",
ivfile, ovfile, wvfile, cmdswitches, rstr);
}
// delete unneeded files ...
JS9.vunlink(avfile);
JS9.vunlink(wvfile);
if( awvfile ){
JS9.vunlink(awvfile);
}
if( arr ){
JS9.vunlink(ivfile);
}
// ... then error check
if( rstr.search(/\[struct stat="OK"/) < 0 ){
// signal this we completed the reproject attempt
rcomplete = true;
earr = rstr.match(/msg="(.\*)"/);
if( earr && earr[1] ){
JS9.error(`${earr[1]} (from mProjectPP)`);
} else {
JS9.error(rstr);
}
}
}
catch(e){
// avoid double error reporting
if( !rcomplete ){
// delete unneeded files ...
JS9.vunlink(avfile);
JS9.vunlink(wvfile);
// call error handler
if( rstr ){
JS9.error(rstr);
} else {
JS9.error("WCS reproject failed", e);
}
} else {
return;
}
}
// return output file name
return ovfile;
};
// high-level routine to reproject image using WCS info
// creates a new raw data layer ("reproject")
JS9.Image.prototype.reprojectData = function(...args){
let i, im, ovfile;
let [wcsim, opts] = args;
// sanity check
if( !wcsim || !JS9.reproject ){ return; }
// is this a string containing an image name or WCS values?
if( typeof wcsim === "string" ){
if( wcsim === "all" ){
for(i=0; i {
let topts, reprojHandler;
const defaultReprojHandler = (hdu) => {
// plugin callbacks
this.xeqPlugins("image", "onreprojectdata");
topts = topts || {};
topts.refreshRegions = true;
// reset section, unless specified otherwise
if( opts.resetSection !== false ){
topts.resetSection = true;
}
// pass on the lcs flag
if( opts.lcsUseRota2 ){
topts.lcsUseRota2 = true;
}
// refresh the image
this.refreshImage(hdu, topts);
// set status
this.setStatus("reprojectData", "complete");
// might have to re-execute calls in the stash
this.xeqStashCall(this.xeqstash, [opts.stash, "reprojectData"]);
// execute onreproject function
if( typeof opts.onreproject === "function" ){
try{ JS9.xeqByName(opts.onreproject, window, this); }
catch(e){ JS9.error("in onreproject callback", e, false); }
}
};
// opts is optional
opts = opts || {};
// handler
reprojHandler = opts.reprojHandler || defaultReprojHandler;
// call the low-level reproject routine, returning reprojected file
ovfile = this.reproject(wcsim, opts);
if( ovfile ){
// refresh image using the reprojected file ...
topts = $.extend(true, {}, JS9.fits.options, opts);
// ... in a new raw data layer
topts.rawid = topts.rawid || "reproject";
// save pointer to original wcs image
if( wcsim.raw && wcsim.raw.header ){
topts.wcsim = wcsim;
}
// process the FITS file
try{ JS9.handleFITSFile(ovfile, topts, reprojHandler); }
catch(e){ JS9.error("can't process reprojected FITS file", e); }
}
}, JS9.SPINOUT);
// allow chaining
return this;
};
// apply image processing filters to the current RGB image
JS9.Image.prototype.filterRGBImage = function(...args){
let [filter] = args;
// no arg: return list of filters
if( !filter ){
return Object.keys(JS9.ImageFilters);
}
// pre-processing and special processing
switch(filter){
case "reset":
// special case: reset to original RGB data, contrast/bias
this.setColormap("reset");
return this;
case "median":
// alias used in filters plugin
filter = "medianFilter";
break;
case "edge":
// alias used in filters plugin
filter = "edgeDetect";
break;
default:
break;
}
// sanity check
if( !JS9.ImageFilters[filter] ){
JS9.error(`JS9 image filter '${filter}' not available`);
}
// save this routine so it can be reconstituted in a restored session
this.xeqStashSave("filterRGBImage", args.slice());
// remove filter name arg
args.shift();
// add display context and RGB img arg
args.unshift(this.display.context, this.rgb.img);
// try to run the filter to generate a new RGB image
try{ JS9.ImageFilters[filter](...args); }
catch(e){ JS9.error(`JS9 image filter '${filter}' failed`, e); }
// display new RGB image
this.displayImage("display");
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
this.xeqPlugins("image", "onfilterrgbimage");
}
// allow chaining
return this;
};
// move image to a different display
// maybe this should be refactored using more useful routines ...
// ... and should (some of) this code be in the Fabric section??
JS9.Image.prototype.moveToDisplay = function(dname){
let i, im, key, layer, dlayer;
let got = 0;
const odisplay = this.display;
const ndisplay = JS9.lookupDisplay(dname);
// sanity check
if( !dname || !ndisplay ){
JS9.error(`could not find display: ${dname}`);
}
// clear old display first
this.display.clearMessage();
this.display.context.clear();
// plugin callbacks
this.xeqPlugins("image", "onimageclear");
// make sure the main layers in the old display are in the new display
for( key of Object.keys(odisplay.layers) ){
if( (odisplay.layers[key].dtype === "main") &&
!ndisplay.layers[key] ){
ndisplay.newShapeLayer(key, odisplay.layers[key].opts);
}
}
// turn off display of layers in new display
// don't want them showing on the new image ...
if( ndisplay.image ){
for( key of Object.keys(ndisplay.layers) ){
if( ndisplay.layers[key].dtype === "main" ){
ndisplay.image.showShapeLayer(key, false, {local: true});
}
}
}
// re-assign each "main" layer from old display to new by:
// saving the graphics, reassigning the canvas, restoring the graphics
for( key of Object.keys(this.layers) ){
layer = this.layers[key];
dlayer = ndisplay.layers[key];
if( dlayer ){
this.showShapeLayer(key, false, {local: true});
layer.dlayer = dlayer;
layer.divjq = dlayer.divjq;
layer.canvasjq = dlayer.canvasjq;
layer.canvas = dlayer.canvas;
} else {
delete this.layers[key];
}
}
// move "main" display from old to new
this.display = ndisplay;
// avoid erroneous save of previous layers
this.display.image = this;
// reset section to ensure proper display size
this.mkSection();
// and redisplay
this.displayImage("all");
// show shape layers in new display
for( key of Object.keys(this.layers) ){
this.showShapeLayer(key, true, {local: true});
}
// move rgb contribution, if necessary
if( odisplay.rgb.rim === this ){
odisplay.rgb.rim = null;
ndisplay.rgb.rim = this;
}
if( odisplay.rgb.gim === this ){
odisplay.rgb.gim = null;
ndisplay.rgb.gim = this;
}
if( odisplay.rgb.bim === this ){
odisplay.rgb.bim = null;
ndisplay.rgb.bim = this;
}
// old display has no image
odisplay.image = null;
// ensure proper positions for graphics
this.refreshLayers();
// display a different image in old display, if possible
for(i=0; i= 0 ){
JS9.displays.splice(i, 1);
}
odisplay.winid.close();
}
// allow chaining
return this;
};
// save session to a json file
// NB: save is an image method, load is a display method
JS9.Image.prototype.saveSession = function(file, opts){
let i, obj, str, blob, layer, dlayer, tobj, key, im, lpos, ipos;
const saveim = (im) => {
let regexp;
// object holding session keys
const obj = {};
// filename
if( window.electron ){
// remove current directory to make it relative
// this allows the session file (and data files) to be moved
// to a machine with a different directory structure, and
// also allows web and desktop sessions to be shared
regexp = new RegExp(`^${window.electron.currentDir}/`);
obj.file = im.file.replace(regexp, "");
} else {
obj.file = im.file;
}
// display size info
obj.dwidth = im.display.width;
obj.dheight = im.display.height;
// image params
obj.params = $.extend(true, {}, im.params);
// temp values: explicitly save some of them
obj.tmp = {};
if( im.tmp.gridStatus === "active" ){
obj.tmp.gridStatus = "active";
}
// get center of displayed image in physical coords
lpos = im.imageToLogicalPos({x:im.rgb.sect.xcen,
y:im.rgb.sect.ycen});
ipos = im.maybePhysicalToImage(lpos);
if( ipos ){
lpos = ipos;
}
// save section info
obj.sect = {};
obj.sect.xcen = lpos.x;
obj.sect.ycen = lpos.y;
obj.sect.xdim = im.raw.width;
obj.sect.ydim = im.raw.height;
obj.sect.zoom = im.rgb.sect.zoom;
// layers
obj.layers = [];
for( key of Object.keys(im.layers) ){
// save each main layer so it can be reconstituted
layer = im.layers[key];
dlayer = layer.dlayer;
// only save layers on main display
// don't save crosshair or grid
if( dlayer.dtype === "main" &&
key !== "crosshair" &&
key !== "grid" ){
tobj = {};
tobj.name = key;
tobj.json = dlayer.canvas.toJSON(dlayer.el);
tobj.dopts = $.extend(true, {}, dlayer.opts);
if( layer.catalog ){
tobj.catalog = layer.catalog;
}
if( layer.starbase ){
tobj.starbase = JSON.stringify(layer.starbase);
}
obj.layers.push(tobj);
}
dlayer.canvas.forEachObject((obj) => {
// look for winid's: they cause circular json errors
if( obj.params && obj.params.winid ){
if( $(obj.params.winid).is(":visible") ){
JS9.error("please close your region dialog box(es) to avoid a JSON circular reference error when saving this session");
} else {
obj.params.winid = null;
}
}
});
}
// save blend state
obj.blend = im.blend;
// save routines which must be executed when restoring session
obj.xeqstash = im.xeqstash;
// save wcsim reference, if necessary
if( im.wcsim && im.wcsim.id ){
obj.wcsim = im.wcsim.id;
}
// remove old display info
delete obj.params.display;
// remove rot90 and flip, as we will recreate them
obj.params.rot90 = 0;
obj.params.flip = "none";
// we didn't save the crosshair
obj.params.crosshair = false;
return obj;
};
if( !{}.hasOwnProperty.call(window, "saveAs") ){
JS9.error("no saveAs() available to save session");
}
// filename for saving
file = file || "js9.ses";
// make sure we have the right extension
if( !file.match(/\.ses$/) ){
file += ".ses";
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse session opts: ${opts}`, e); }
}
// change the cursor to show the waiting status
JS9.waiting(true, this.display);
// object we will save
obj = {};
// list of images to save
obj.images = [];
// which images to save?
if( opts.mode === "display" ){
// save all images in this display
for(i=0; i= 1 &&
this.xeqstash[len-1] &&
this.xeqstash[len-1].args[0] === -args[0] ){
this.xeqstash.pop();
return this;
}
break;
case "setFlip":
// two flips in the same direction cancel one another
len = this.xeqstash.length;
if( len >= 1 &&
this.xeqstash[len-1] &&
this.xeqstash[len-1].args[0] === args[0] ){
this.xeqstash.pop();
return this;
}
break;
default:
for(i=0; i {
let context = xeq.context || "image";
try{
switch(context){
case "image":
this[func](...xeq.args);
break;
case "display":
this.display[func](...xeq.args);
break;
default:
this[func](...xeq.args);
break;
}
}
catch(e){
JS9.error(`error executing stash: ${func}`, e, false);
}
};
xeqstash = xeqstash || this.xeqstash;
if( $.isArray(xeqstash) ){
for(i=0; i= 0 ){
continue;
}
doxeq(key, xeq);
}
} else {
// backward compatibility: pre 3.1 used an object, not an array
for( key of Object.keys(xeqstash) ){
if( $.inArray(key, exclArr) >= 0 ){
continue;
}
xeq = xeqstash[key];
doxeq(key, xeq);
}
}
};
// remove a stash routine
JS9.Image.prototype.xeqStashDiscard = function(xid){
let i, key;
// sanity check
if( !this.xeqstash ){ return; }
if( $.isArray(this.xeqstash) ){
for(i=this.xeqstash.length-1; i>=0; i--){
if( xid === this.xeqstash[i].func || xid === this.xeqstash[i].id ){
this.xeqstash.splice(i,1);
}
}
} else {
// pre 3.1 used an object
for( key of Object.keys(this.xeqstash) ){
if( xid === key || xid === this.xeqstash[key].id ){
delete this.xeqstash[key];
}
}
}
};
// execute plugins of various types (using type-specific values)
JS9.Image.prototype.xeqPlugins = function(xtype, xname, xval){
let pname, pinst, popts, parr, evt;
const xtrig = (name, obj) => {
const s = `JS9:${name}`;
$(document).trigger(s, obj);
};
// sanity check
if( !xtype || !xname || !JS9.globalOpts.xeqPlugins ){ return; }
// array of plugin instances
parr = this.display.pluginInstances || {};
// look for plugin callbacks to execute
for( pname of Object.keys(parr) ){
pinst = parr[pname];
popts = pinst.plugin.opts;
if( pinst.isActive(xname) && typeof popts[xname] === "function" ){
this.callingPlugin = xname;
switch(xtype){
case "image":
// used for: onimage[load,close,refresh,display]
try{
popts[xname].call(pinst, this);
xtrig(xname, {im: this});
}
catch(e){ pinst.errLog(xname, e); }
break;
case "region":
case "shape":
// used for: on[layer]change
// xval: pub
try{
popts[xname].call(pinst, this, xval);
xtrig(xname, {im: this, xreg: xval});
}
catch(e){ pinst.errLog(xname, e); }
break;
case "keydown":
case "keypress":
// used for: onkeydown, onkeypress (deprecated)
// xval: evt
evt = xval.originalEvent || xval;
try{
popts[xname].call(pinst, this, this.ipos, evt);
xtrig(xname, {im: this, ipos: this.ipos, evt: evt});
}
catch(e){ pinst.errLog(xname, e); }
break;
case "mouse":
// used for: onmouse[down,move,over,out]
// xval: evt
if( !this.clickInRegion || popts[`${xname}\_inRegion`] ){
evt = xval.originalEvent || xval;
try{
popts[xname].call(pinst, this, this.ipos, evt);
xtrig(xname, {im: this, ipos: this.ipos, evt: evt});
}
catch(e){ pinst.errLog(xname, e); }
}
break;
}
delete this.callingPlugin;
}
}
// allow chaining
return this;
};
// upload virtual file to proxy server
JS9.Image.prototype.uploadFITSFile = function(){
let vfile, vdata;
const upcb = (r) => {
delete JS9.worker.uploadActive;
window.setTimeout(() => { JS9.progress(false); }, 1000);
if( r.stderr ){
JS9.error(r.stderr);
} else if( r.stdout ){
// set FITS filename and proxy filename
this.fitsFile = r.stdout.trim();
this.proxyFile = this.fitsFile;
if( JS9.globalOpts.prependJS9Dir &&
!this.fitsFile.match(/^\${JS9\_DIR}/) &&
this.fitsFile.charAt(0) !== "/" ){
this.fitsFile = `\${JS9\_DIR}/${this.fitsFile}`;
}
// re-query for analysis
this.queryHelper("all");
}
};
// sanity check
if( !JS9.worker ){ return; }
// only supported when using socket.io ...
if( JS9.helper.type !== "nodejs" && JS9.helper.type !== "socket.io" ){
return;
}
// ... and only when we have a virtual file to upload
if( !this.raw.hdu || !this.raw.hdu.fits || !this.raw.hdu.fits.vfile ){
return;
}
// only one upload at a time
if( JS9.worker.uploadActive ){
JS9.error("only one upload allowed at a time");
}
// this is the file to upload
vfile = this.raw.hdu.fits.vfile;
// ask the remote server if we can upload
JS9.helper.send("quotacheck", null, (robj) => {
// check quota, only errors matter
if( robj.stderr || robj.errcode ){
JS9.error(robj.stderr || `from quotacheck: ${robj.errcode}`);
}
vdata = JS9.vread(vfile, "binary");
JS9.worker.socketio(() => {
JS9.worker.uploadActive = true;
JS9.progress(true, this.display);
JS9.worker.send("uploadFITS", [vfile, vdata], upcb, [vdata.buffer]);
});
});
return this;
};
// remove proxy file from a remote server
JS9.Image.prototype.removeProxyFile = function(s){
let t, reset, file, regexp;
const func = (r) => {
if( reset ){
if( r && r.stdout.trim() === "OK" ){
this.proxyFile = null;
this.proxyParent = null;
this.fitsFile = null;
this.analysisPackages = null;
this.queryHelper("all");
}
}
};
// arg can be a boolean, which means remove proxyFile and reset
if( typeof s === "boolean" ){
reset = s;
} else if( typeof s === "string" ){
// specify file to remove in the working directory
// check for attempt to break out of the working dir using abs path
if( s.match(/^\//) ){
return;
}
// remove possible install dir prefix and then ...
// check attempt to break out of the working dir using ".."
regexp = new RegExp(`^${JS9.INSTALLDIR}`);
t = s.replace(regexp, "");
if( t.match(/\.\./) ){
return;
}
file = s;
} else {
// default is to remove the proxy file
if( !this.proxyFile ){
return;
}
file = this.proxyFile;
// also remove the proxyParent file, if necessary
if( this.proxyParent ){
file = `${file} ${this.proxyParent}`;
}
}
// sanity check
if( !file ){ return; }
// ask to remove proxy file, and process result
JS9.Send('removeproxy', {'cmd': `js9Xeq removeproxy ${file}`}, func);
};
// convert table to a shape array for the given image
JS9.Image.prototype.starbaseToShapes = function(starbase, opts){
let i, j, k, shape, pos, siz, reg, data, header, delims, sizefunc;
let xcol, ycol, ra, dec, owcssys, wcssys, tcol, tregexp;
const global = JS9.globalOpts.catalogs;
const xcols = JS9.globalOpts.catalogs.ras;
const ycols = JS9.globalOpts.catalogs.decs;
const regs = [];
const getpos = (ra, dec) => {
let arr;
arr = JS9.wcs2pix(this.raw.wcs, ra, dec).trim().split(/ +/);
if( arr && arr.length ){
return {x: parseFloat(arr[0]), y: parseFloat(arr[1])};
}
return null;
};
const getcol = (starbase, header, cols, defcol) => {
let i, j, col;
if( defcol !== undefined ){
col = defcol;
} else {
// look for an exact match
col = -1;
for(j=0; j= 0 ){
break;
}
}
// no exact match, look for an approx match
if( col < 0 ){
tcol = cols[0];
tregexp = new RegExp(`^${tcol}`, "i");
for(i=0; i {
return { width: opts.width || global.width || 7,
height: opts.height || global.height || 7 };
};
break;
case "circle":
// eslint-disable-next-line no-unused-vars
sizefunc = () => {
return { radius: opts.radius || global.radius || 3.5};
};
break;
case "ellipse":
// eslint-disable-next-line no-unused-vars
sizefunc = () => {
return { r1: opts.r1 || global.r1 || 3.5,
r2: opts.r2 || global.r2 || 3.5 };
};
break;
default:
// eslint-disable-next-line no-unused-vars
sizefunc = () => {
return { width: opts.width || 7, height: opts.height || 7 };
};
break;
}
// save original wcs system
owcssys = this.getWCSSys();
// set wcs system for catalogs
if( opts.wcssys ){
wcssys = opts.wcssys;
} else if( global.wcssys ){
wcssys = global.wcssys;
} else {
// umm ...
wcssys = "ICRS";
}
// set wcssys for this catalog
this.setWCSSys(wcssys, false);
// convert each catalog object in the table into a JS9 shape
for(i=0, j=0; i {
const delims = " \t-.:hdmsr'\"";
const obj = {};
obj.val = JS9.saostrtod(s);
obj.delim = String.fromCharCode(JS9.saodtype());
if( (obj.delim !== "\0") && (delims.includes(obj.delim)) ){
// valid delim means we converted to a float
return obj;
} else if( JS9.isNumber(s) ){
// no delim, but its a number, so must be an int
return obj;
}
// everything else is a string
obj.val = s;
return obj;
};
// special case: 1 non-string arg is the catalog, not the layer
if( args.length === 1 && typeof layer !== "string" ){
catalog = layer;
layer = null;
}
// special case: 2 non-string args: file and obj, not the layer
if( args.length === 2 && typeof layer !== "string" ){
opts = catalog;
catalog = layer;
layer = null;
}
// sanity check
if( !catalog ){ return; }
if( global.tooltip ){
lopts.tooltip = global.tooltip;
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse catalog opts: ${opts}`, e); }
}
// default color, if none specified
opts.color = opts.color || global.color || "#00FF00";
// wcs system
opts.wcssys = opts.wcssys || global.wcssys;
// update the WCS strings when adding a catalog shape
opts.updateWCS = true;
// starbase opts
topts = {convFuncs: {def: defconv},
units: opts.units || global.units,
skip: opts.skip || global.skip};
// generate starbase table
try{ starbase = new JS9.Starbase(catalog, topts); }
catch(e){ JS9.error("could not parse catalog. Is it in tab-separated column format?"); }
// sanity check
if( !starbase || !starbase.data || !starbase.data.length ){
JS9.error("no objects found in catalog");
}
// generate new catalog shapes
shapes = this.starbaseToShapes(starbase, opts);
if( shapes.length ){
// layer name
layer = layer || `catalog\_${JS9.uniqueID()}` ;
// create a new layer, if necessary
this.display.newShapeLayer(layer, lopts);
// delete any old shapes
this.removeShapes(layer);
// save the original catalog before adding shapes
this.layers[layer].catalog = catalog;
this.layers[layer].starbase = starbase;
// add them to the catalog layer
this.addShapes(layer, shapes, opts);
} else {
JS9.error("no catalog objects found");
}
// allow chaining
return this;
};
// save catalog as a file
JS9.Image.prototype.saveCatalog = function(fname, which){
let layer, cat, blob;
layer = which || this.activeShapeLayer();
if( !this.layers[layer] || !this.layers[layer].catalog ){
if( layer && layer !== "undefined" ){
JS9.error(`no catalog available: ${layer}`);
} else {
JS9.error("no active catalog available");
}
}
cat = this.layers[layer].catalog;
blob = new Blob([cat], {type: "text/plain;charset=utf-8"});
fname = fname || `${layer}.cat`;
if( !fname.match(/\.cat$/) ){
fname += ".cat";
}
if( {}.hasOwnProperty.call(window, "saveAs") ){
JS9.saveAs(blob, fname);
} else {
JS9.error("no saveAs() available to save catalog");
}
return fname;
};
// convert ra, dec from one wcs to another
JS9.Image.prototype.wcs2wcs = function(from, to, ra, dec){
let owcssys, ounits, nwcs, arr, x, y, s, v0;
// save current wcs and units
owcssys = this.getWCSSys();
ounits = this.getWCSUnits();
// to, from default to current wcs
from = from || owcssys;
to = to || owcssys;
// convert ra, dec from string input to float degrees, if necessary
if( typeof ra === "string" ){
v0 = JS9.strtoscaled(ra);
if( JS9.isHMS(from, v0.dtype) ){
v0.dval \*= 15.0;
}
ra = v0.dval;
}
if( typeof dec === "string" ){
v0 = JS9.strtoscaled(dec);
dec = v0.dval;
}
// temporarily set the wcs to what we are converting from
nwcs = this.setWCSSys(from, false).getWCSSys();
// make sure change was successful
if( from !== "native" ){
if( nwcs !== from ){
JS9.error(`unknown or invalid wcs: ${from}`);
}
}
// convert input ra, dec into image pixels in this wcs
arr = JS9.wcs2pix(this.raw.wcs, ra, dec).trim().split(/ +/);
x = parseFloat(arr[0]);
y = parseFloat(arr[1]);
// set wcs back to the target wcs
this.setWCSSys(to, false);
// convert image pixels from input ra, dec into target wcs
this.setWCSUnits("degrees", false);
s = JS9.pix2wcs(this.raw.wcs, x, y).trim();
// reset wcs to original
this.setWCSUnits(ounits, false);
if( owcssys !== to ){
this.setWCSSys(owcssys, false);
}
// return result
return s;
};
// convert wcs, physical or image image length to image length,
// using current wcs and string delimiters to determine what input type
JS9.Image.prototype.wcs2imlen = function(s){
let v, wcsinfo, iscale;
let dpp = 1;
// sanity check
if( !s ){ return; }
v = JS9.strtoscaled(s);
wcsinfo = this.raw.wcsinfo || {cdelt1: 1, cdelt2: 1};
// oh dear, this is cheating ...
if( wcsinfo.cdelt1 !== undefined ){
dpp = wcsinfo.cdelt1;
} else if( wcsinfo.cdelt2 !== undefined ){
dpp = wcsinfo.cdelt2;
}
switch(this.params.wcssys){
case "image":
break;
case "physical":
// use LTM1\_1 or LTM1\_2 value stored for logical to image transforms
if( this.lcs && this.lcs.physical ){
iscale = Math.sqrt(Math.pow(this.lcs.physical.forward[0][0],2) +
Math.pow(this.lcs.physical.forward[0][1],2));
v.dval = Math.abs(v.dval \* iscale);
}
break;
default:
// cheap conversion of wcs len to image len
if( v.dtype && (v.dtype !== ".") && (v.dtype !== "\0") ){
v.dval = Math.abs(v.dval / dpp);
}
break;
}
return v.dval;
};
// ---------------------------------------------------------------------
// JS9 Colormap support
// ---------------------------------------------------------------------
JS9.Colormap = function(...args){
let [name, a1, a2, a3] = args;
let i, got;
// sanity check
if( !name ){ return; }
// type of colormap is based on number and type of args
this.name = name;
switch(args.length){
case 2:
if( $.isArray(a1[0]) && typeof a1[0][0] === "number" ){
// array of rgb values
// JS9.Colormap("sls", [[0, 0, 0], [0.043442, 0, 0.052883], ...]);
this.type = "lut";
this.colors = a1;
} else {
// array of static colors and min, max values
// JS9.Colormap("s1", [["red",1,1], ["cyan",2,3], ["blue",4,99]]);
this.type = "static";
this.colors = JS9.parseStaticColors(a1);
}
break;
case 4:
// three arrays of vertices
// JS9.Colormap("grey", [[0,0],[1,1]], [[0,0],[1,1]], [[0,0],[1,1]]));
this.type = "sao";
this.vertices = [a1, a2, a3];
break;
default:
JS9.error("colormap requires a colormap name and 1 or 3 array args");
break;
}
// flag whether this was a core or user-defined colormap
if( !JS9.inited ){
this.source = "core";
} else {
this.source = "user";
}
// replace or append
for(i=0; i 1 ){
JS9.log("JS9 colormap: %s", this.name);
}
};
JS9.Colormap.prototype.mkColorCell = function(ii){
let m, x, i, j, val, vertex, len, size, index;
const count = JS9.COLORSIZE;
const umax = 255;
const rgb = [0, 0, 0];
switch(this.type){
// from: tksao1.0/colormap/sao.C
case "sao":
x = ii / count;
// for each of red, green, blue ...
for(j=0; j<3; j++){
// look for the first vertex with x value larger than our x value
vertex = this.vertices[j];
len = vertex.length;
for(i=0; i x ){
break;
}
}
// if first vertex x value is greater than ours, use it
if( i === 0 ){
val = vertex[0][1];
// if last vertex xvalue is less than ours, use it
} else if( i === len ){
val = vertex[len-1][1];
// interpolate between two vertices
} else {
m = (vertex[i][1] - vertex[i-1][1]) /
(vertex[i][0] - vertex[i-1][0]);
if( m ){
// point slope form
val = m \* (x - vertex[i-1][0]) + vertex[i-1][1];
} else {
val = vertex[i][1];
}
}
// assign value to the correct color in the result array
rgb[j] = val \* umax;
}
break;
// from: tksao1.0/colormap/lut.C
case "lut":
size = this.colors.length;
// index into the evenly spaced RGB values
index = Math.floor(ii\*size/count);
if( index < 0 ){
rgb[0] = this.colors[0][0] \* umax;
rgb[1] = this.colors[0][1] \* umax;
rgb[2] = this.colors[0][2] \* umax;
} else if( index < size ){
rgb[0] = this.colors[index][0] \* umax;
rgb[1] = this.colors[index][1] \* umax;
rgb[2] = this.colors[index][2] \* umax;
} else {
rgb[0] = this.colors[size-1][0] \* umax;
rgb[1] = this.colors[size-1][1] \* umax;
rgb[2] = this.colors[size-1][2] \* umax;
}
break;
case "static":
break;
default:
JS9.error("unknown colormap type");
break;
}
// return the news
return rgb;
};
// ---------------------------------------------------------------------
// JS9 display object for the screen display
// ---------------------------------------------------------------------
JS9.Display = function(el){
// pass jQuery element, DOM element, or id
if( el instanceof jQuery ){
this.divjq = el;
} else if( typeof el === "object" ){
this.divjq = $(el);
} else {
this.divjq = $(`#${el}`);
}
// make sure div has some id
if( !this.divjq.attr("id") ){
this.divjq.attr("id", JS9.DEFID);
}
// save id
this.id = this.divjq.attr("id");
// display-specific scratch space
this.tmp = {};
// display RGB mode
this.rgb = {
active: false,
rim: null,
gim: null,
bim: null
};
// add class
this.divjq.addClass("JS9");
// set width and height on div
this.width = this.divjq.attr("data-width");
if( !this.width ){
this.width = JS9.WIDTH;
}
this.divjq.css("width", this.width);
this.width = parseInt(this.divjq.css("width"), 10);
this.height = this.divjq.attr("data-height");
if( !this.height ){
this.height = JS9.HEIGHT;
}
this.divjq.css("height", this.height);
this.height = parseInt(this.divjq.css("height"), 10);
// save original width and height
this.width0 = this.width;
this.height0 = this.height;
// set tabindex so we can sense keyboard events
// (this invocation senses keydown when no is image loaded)
this.divjq.attr("tabindex", 0);
// create DOM canvas element
this.canvas = document.createElement("canvas");
// jquery version for event handling and DOM manipulation
this.canvasjq = $(this.canvas)
.addClass("JS9Image")
.attr("id", `${this.id}Image`)
.attr("width", this.width)
.attr("height", this.height)
.css("z-index", JS9.ZINDEX);
// add container to the high-level div
this.displayConjq = $("

")
.addClass("JS9Container")
.attr("id", `${this.id}DisplayConjq`)
.css("z-index", JS9.ZINDEX)
// set tabindex so we can sense keyboard events
// (this invocation senses keydown after image is loaded)
.attr("tabindex", "0")
.append(this.canvasjq)
.appendTo(this.divjq);
if( !JS9.allinone ){
this.iconjq = $("

")
.addClass("JS9Logo")
.css("display", "none")
.css("z-index", JS9.ZINDEX+1)
.appendTo(this.divjq);
this.iconimgjs = $("![]()")
.addClass("JS9Logo")
.attr("src", JS9.InstallDir(JS9.globalOpts.logo))
.attr("alt", "js9")
.attr("title", "js9")
.appendTo(this.iconjq);
if( JS9.globalOpts.logoDisplay ){
this.iconjq.css("display", "block");
}
}
// add resize capability, if necessary
if( JS9.globalOpts.resizeHandle &&
{}.hasOwnProperty.call(window, "ResizeSensor") ){
this.divjq
.css("resize", "both")
.css("overflow", "hidden");
if( JS9.bugs.webkit\_resize ){
this.owidth = parseInt(this.divjq.css("width"), 10);
this.oheight = parseInt(this.divjq.css("height"), 10);
this.divjq
.css("width", this.width + JS9.RESIZEFUDGE)
.css("height", this.height + JS9.RESIZEFUDGE);
}
this.resizeSensor = new ResizeSensor(this.divjq, () => {
let nwidth = this.divjq.width();
let nheight = this.divjq.height();
if( JS9.bugs.webkit\_resize ){
nwidth -= JS9.RESIZEFUDGE;
nheight -= JS9.RESIZEFUDGE;
}
this.resize(nwidth, nheight);
});
}
// drawing context
this.context = this.canvas.getContext("2d");
// turn off anti-aliasing
if( !JS9.ANTIALIAS ){
this.context.imageSmoothingEnabled = false;
}
// add the display tooltip
this.tooltip = $("

")
.attr("id", `tooltip\_${this.id}`)
.addClass("JS9Tooltip")
.appendTo(this.divjq);
// no image loaded into this canvas
this.image = null;
// no plugin instances yet
this.pluginInstances = {};
// no layers yet
this.layers = {};
// init message layer
this.initMessages();
// blend mode is false to start
this.blendMode = false;
// display-based mouse/touch actions initially from global
this.mouseActions = JS9.globalOpts.mouseActions.slice(0);
this.touchActions = JS9.globalOpts.touchActions.slice(0);
// add event handlers
this.divjq.on("mouseenter", this, (evt) => {
return JS9.mouseEnterCB(evt);
});
this.divjq.on("mouseover", this, (evt) => {
return JS9.mouseOverCB(evt);
});
this.divjq.on("mousedown touchstart", this, (evt) => {
return JS9.mouseDownCB(evt);
});
this.divjq.on("mousemove touchmove", this, (evt) => {
return JS9.mouseMoveCB(evt);
});
this.divjq.on("mouseup touchend", this, (evt) => {
return JS9.mouseUpCB(evt);
});
this.divjq.on("mouseout", this, (evt) => {
return JS9.mouseOutCB(evt);
});
this.divjq.on("keypress", this, (evt) => {
return JS9.keyPressCB(evt);
});
this.divjq.on("keydown", this, (evt) => {
return JS9.keyDownCB(evt);
});
this.divjq.on("keyup", this, (evt) => {
return JS9.keyUpCB(evt);
});
this.divjq.on("wheel", this, (evt) => {
return JS9.wheelCB(evt);
});
// set up drag and drop, if available
this.divjq.on("dragenter", this, (evt) => {
return JS9.dragenterCB(this.id, evt);
});
this.divjq.on("dragover", this, (evt) => {
return JS9.dragoverCB(this.id, evt);
});
this.divjq.on("dragexit", this, (evt) => {
return JS9.dragexitCB(this.id, evt);
});
this.divjq.on("drop", this, (evt) => {
return JS9.dragdropCB(this.id, evt);
});
// no context menus on the display
this.divjq.on("contextmenu", this, () => {
return false;
});
// add local file open support
this.addFileDialog("Load", JS9.globalOpts.imageTemplates);
this.addFileDialog("RefreshImage", JS9.globalOpts.imageTemplates);
this.addFileDialog("LoadRegions", JS9.globalOpts.regTemplates);
this.addFileDialog("LoadSession", JS9.globalOpts.sessionTemplates);
this.addFileDialog("LoadColormap", JS9.globalOpts.colormapTemplates);
this.addFileDialog("LoadCatalog", JS9.globalOpts.catalogTemplates);
// add to list of displays
JS9.displays.push(this);
// set focus
this.displayConjq.focus();
// debugging
if( JS9.DEBUG ){
JS9.log("JS9 display: %s", this.id);
}
};
// add support for file dialog box which executes JS9 routine on file blobs
JS9.Display.prototype.addFileDialog = function(funcName, template){
let jdiv, jinput, id;
// sanity check
if( !funcName || !JS9.publics[funcName] ){ return; }
id = `openLocal${funcName}-${this.id}`;
// outer div
// https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file
// recommends opacity over visibility, but it breaks the menubar in ios
jdiv = $("

")
.addClass("JS9Hidden")
.appendTo(this.divjq);
// inner file input element
jinput = $("")
.attr("type", "file")
.attr("id", id)
.attr("multiple", true)
.appendTo(jdiv);
// add accept template, if possible
if( template ){
jinput.attr("accept", template);
}
// add callback for when input changes
jinput.on("change", (e) => {
let i, opts;
const el = e.currentTarget;
if( el.files.length ){
switch(funcName){
case "Load":
case "RefreshImage":
opts = {localAccess: true};
JS9.waiting(true, this);
break;
default:
break;
}
}
for(i=0; i")
.addClass("JS9Container")
.css("z-index", JS9.MESSZINDEX)
.appendTo(this.divjq);
this.infoArea = $("

")
.addClass("JS9Message")
.appendTo(this.messageContainer);
this.regionsArea = $("

")
.addClass("JS9Message")
.appendTo(this.messageContainer);
this.progressArea = $("

")
.addClass("JS9Progress")
.addClass("JS9Message")
.appendTo(this.messageContainer);
this.progressBar = $("")
.addClass("JS9ProgressBar")
.attr("value", 0)
.attr("max", 100)
.attr("name", "progress")
.appendTo(this.progressArea);
// make it draggable, if possible
try{
this.messageContainer.draggable({
// eslint-disable-next-line no-unused-vars
start(event, ui) {
this.oicb = JS9.globalOpts.internalContrastBias;
JS9.globalOpts.internalContrastBias = false;
},
// eslint-disable-next-line no-unused-vars
stop(event, ui) {
JS9.globalOpts.internalContrastBias = this.oicb;
}
});
}
catch(ignore){ /\* empty \*/ }
// allow chaining
return this;
};
// display a plugin in a light window or a new window
JS9.Display.prototype.displayPlugin = function(plugin){
let i, a, w, h, p, r, s, title, name, did, oid, iid, odiv, pdiv, pinst, win;
if( typeof plugin === "string" ){
for(i=0; i")
.attr("id", oid)
.css("display", "none")
.appendTo($(this.divjq));
$("

")
.addClass(plugin.name)
.attr("id", iid)
.attr("data-js9id", this.divjq.attr("id"))
.css("height", "100%")
.css("width", "100%")
.appendTo(odiv);
}
// window not created: create and show it
// create the window
w = plugin.opts.winDims[0] || JS9.WIDTH;
h = plugin.opts.winDims[1] || JS9.HEIGHT;
if( plugin.opts.winResize ){
r = "1";
} else {
r = "0";
}
// light window param string
s = sprintf(a.format, w, h, r);
// add the title, if explicitly called for and if not already added
if( plugin.opts.toolbarHTML &&
plugin.opts.toolbarHTML.search(/\$title/) >= 0 ){
title = "";
} else {
title = plugin.opts.winTitle || "";
}
// add display to title
title += sprintf(JS9.IDFMT, this.id);
// create the light window
win = JS9.lightWin(did, "div", oid, title, s);
// find inner div in the light window
pdiv = $(`#${did} #${iid}`);
// create the plugin inside the inner div
pinst = JS9.instantiatePlugin(pdiv, plugin, win);
pinst.winHandle.onclose = () => {
// just hide the window
pinst.winHandle.hide();
pinst.status = "inactive";
if( plugin.opts.onpluginclose ){
try{
plugin.opts.onpluginclose.call(pinst, this.image);
}
catch(e){
JS9.log("onplugincloseCB: %s [%s]\n%s",
plugin.name, e.message, JS9.strace(e));
}
}
return false;
};
pinst.status = "active";
if( plugin.opts.onplugindisplay ){
try{
plugin.opts.onplugindisplay.call(pinst, this.image);
}
catch(e){
JS9.log("onplugindisplayCB: %s [%s]\n%s",
plugin.name, e.message, JS9.strace(e));
}
}
} else if( pinst.status === "inactive" ){
// window created but hidden: show it
if( pinst.winHandle ){
pinst.winHandle.show();
pinst.status = "active";
if( plugin.opts.onplugindisplay ){
try{
plugin.opts.onplugindisplay.call(pinst, this.image);
}
catch(e){
JS9.log("onplugindisplayCB: %s [%s]\n%s",
plugin.name, e.message, JS9.strace(e));
}
}
}
} else if( pinst.status === "active" ){
// window created and showing: hide it
if( pinst.winHandle ){
pinst.winHandle.hide();
pinst.status = "inactive";
if( plugin.opts.onpluginclose ){
try{
plugin.opts.onpluginclose.call(pinst, this.image);
}
catch(e){
JS9.log("onplugincloseCB: %s [%s]\n%s",
plugin.name, e.message, JS9.strace(e));
}
}
}
}
break;
case "new":
JS9.error("external window support for plugins not yet implemented");
break;
}
};
// display the general file-loading form for this display
JS9.Display.prototype.displayLoadForm = function(opts){
let html, did, method;
const format = JS9.globalOpts.localLoadFormat;
if( JS9.globalOpts.remoteLoadMethod === "proxy" && !JS9.proxyAvailable() ){
JS9.globalOpts.remoteLoadMethod = "cgiproxy";
}
method = JS9.globalOpts.remoteLoadMethod;
// opts is optional, defaults to displaying local and remote
opts = opts || {local:true, remote:true};
// options for creating window
if( JS9.isNull(opts.title) ){
opts.title = "";
if( opts.local ){
opts.title = "Open ";
}
if( opts.remote ){
if( opts.title ){
opts.title += "or ";
}
opts.title += "Retrieve ";
}
opts.title += "an Image ";
if( opts.local ){
opts.title += "or Auxiliary File";
}
}
opts.winformat = opts.winformat ||
"width=640px,height=300px,resize=1,scrolling=1";
// from where do we get the html?
if( JS9.allinone ){
html = JS9.allinone.loadHTML;
} else {
html = JS9.InstallDir(JS9.globalOpts.loadURL);
}
// call this once window is loaded to init form values
$(JS9.lightOpts[JS9.LIGHTWIN].topid)
.arrive(".loadForm", {onceOnly: true}, (el) => {
const localfile = $(el).data("localfile") || this.tmp.localfile;
const remotefile = $(el).data("remotefile") || this.tmp.remotefile;
if( opts.local ){
$(did).find(".localfile").removeClass("nodisplay");
$(did).find(".localdoc").removeClass("nodisplay");
if( localfile ){
$(did).find(`input[name="localfile"]`).val(localfile);
}
$(did).find(`input[value=${format}]`).click();
}
if( opts.remote ){
$(did).find(".remotefile").removeClass("nodisplay");
$(did).find(".remotedoc").removeClass("nodisplay");
if( remotefile ){
$(did).find(`input[name="remotefile"]`).val(remotefile);
}
if( !JS9.proxyAvailable() ){
$(did).find(`input[value="proxy"]`).prop("disabled", true);
}
$(did).find(`input[value=${method}]`).click();
}
});
// create the window
did = JS9.Image.prototype.displayAnalysis.call(null, "params", html, opts);
// save display id
$(did).data("dispid", this.id);
};
// resize a display
JS9.Display.prototype.resize = function(width, height, opts){
let i, div, im, key, layer, nwidth, nheight, nleft, ntop, pinst, owidth;
const repos = (o) => {
o.left += nleft;
o.top += ntop;
o.setCoords();
};
// sanity check
if( !JS9.globalOpts.resize ){
JS9.error("display resize not enabled");
}
// no args => return current size
if( !width && !height ){
return {width: this.width, height: this.height};
}
// 'full' or 'reset' or 'image'
if( width === "full" ){
opts = height;
if( window.innerWidth ){
width = window.innerWidth;
}
if( window.innerHeight ){
// including menubar, if available
height = window.innerHeight;
// divs we take into account when centering
for(i=0; i= 0 &&
(JS9.isNull(opts.resizeMenubar) || opts.resizeMenubar) ){
pinst = this.pluginInstances.JS9Menubar;
if( pinst ){
$(`#${this.id}Menubar`).css("width", nwidth);
}
}
// change the toolbar width, unless explicitly told not to
if( $.inArray("JS9Toolbar", JS9.globalOpts.resizeDivs) >= 0 &&
(JS9.isNull(opts.resizeToolbar) || opts.resizeToolbar) ){
pinst = this.pluginInstances.JS9Toolbar;
if( pinst ){
// set new value for width
pinst.divjq.attr("data-width", `${String(nwidth)}px`);
// re-init toolbar for this size
JS9.Toolbar.init.call(pinst);
}
}
// change the colorbar width, unless explicitly told not to
if( $.inArray("JS9Colorbar", JS9.globalOpts.resizeDivs) >= 0 &&
(JS9.isNull(opts.resizeColorbar) || opts.resizeColorbar) ){
pinst = this.pluginInstances.JS9Colorbar;
if( pinst ){
// set new value for width
pinst.divjq.attr("data-width", `${String(nwidth)}px`);
// re-init colorbar for this size
JS9.Colorbar.init.call(pinst);
}
}
// change the statusbar width, unless explicitly told not to
if( $.inArray("JS9Statusbar", JS9.globalOpts.resizeDivs) >= 0 &&
(JS9.isNull(opts.resizeStatusbar) || opts.resizeStatusbar) ){
pinst = this.pluginInstances.JS9Statusbar;
if( pinst ){
$(`#${this.id}Statusbar`).css("width", nwidth);
// resize colorbar, if necessary
if( pinst.statusBar &&
pinst.statusBar.match(/\$colorbar/) &&
opts.resizeStatusbarColorbar !== false ){
pinst.colorwidth = Math.max(pinst.colorwidth + width - owidth,
JS9.Statusbar.COLORWIDTH);
JS9.Statusbar.display.call(pinst, this.image, {reinit: true});
}
}
}
// change size of shape canvases
for( key of Object.keys(this.layers) ){
layer = this.layers[key];
if( layer.dtype === "main" ){
layer.divjq.css("width", nwidth);
layer.divjq.css("height", nheight);
layer.canvasjq.attr("width", nwidth);
layer.canvasjq.attr("height", nheight);
layer.canvas.setWidth(nwidth);
layer.canvas.setHeight(nheight);
layer.canvas.calcOffset();
}
}
// change position of shapes on currently displayed layers
// save resize parameters for undisplayed layers
for(i=0; i= this.divjq.width()) &&
(pos.y + JS9.RESIZEDIST >= this.divjq.height()) ){
return true;
}
}
return false;
};
// scroll the display to the center of the viewport
// http://stackoverflow.com/questions/18150090/jquery-scroll-element-to-the-middle-of-the-screen-instead-of-to-the-top-with-a
JS9.Display.prototype.center = function(){
const el = this.divjq;
let i, div, tel, voffset, hoffset;
let elVOffset = el.offset().top;
let elHeight = el.height();
const windowHeight = $(window).height();
const elHOffset = el.offset().left;
const elWidth = el.width();
const windowWidth = $(window).width();
const speed = 250;
// divs we take into account when getting total height
for(i=0; i 0 ){
j = $.inArray(odisp, JS9.displays);
if( j >= 0 ){
JS9.displays.splice(j, 1);
}
el.remove();
}
}
}
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
if( this.image ){
this.image.xeqPlugins("image", "ongatherdisplay");
}
}
};
// separate images in this display into new displays
JS9.Display.prototype.separate = function(opts){
let arr, d0, d1, el;
let nsep = 0;
let row = 0;
let col = 0;
let myid = 1;
const sep = {};
const saveims = {};
const rexp = /\_sep[0-9][0-9]\*/;
const sepopts = JS9.globalOpts.separate;
const menuStr = "";
const toolStr = "";
const js9Str = "";
const colorStr = "";
const statusStr = "";
const winoptsStr = "width=%s,height=%s,top=%s,left=%s,resize=1,scolling=1";
const LIT\_FUDGE = 5;
const COLORBAR\_FUDGE = 7;
const DHTML\_HEIGHT = 30 + 13; // height of dhtml lightwin extras;
const initopts = (display, fromID, opts) => {
// sanity check
if( !fromID ){
JS9.error("can't init separation ops: no 'from' id");
}
sep.layout = opts.layout || JS9.globalOpts.separate.layout || "auto";
sep.leftMargin = opts.leftMargin || sepopts.leftMargin || 0;
sep.topMargin = opts.topMargin || sepopts.topMargin || 0;
// check if we want to do a grid ... and if we can
if( sep.layout === "auto" &&
display.divjq.closest(".JS9GridContainer").length > 0 ){
sep.layout = "grid";
}
if( sep.layout === "grid" ){
if( CSS.supports("display", "grid") ){
el = display.divjq.closest(".JS9GridContainer");
if( el.length > 0 ){
sep.container = el;
}
} else {
sep.layout = "auto";
}
}
switch(sep.layout){
case "auto":
col = 1;
row = 0;
break;
case "horizontal":
col = 1;
row = 0;
break;
case "vertical":
col = 0;
row = 1;
break;
default:
col = 1;
row = 0;
break;
}
sep.topExtra = DHTML\_HEIGHT;
sep.leftExtra = 0;
sep.js9 = $(`#${fromID}`);
sep.menubar = $(`#${fromID}Menubar`);
if( sep.menubar.length > 0 ){
sep.menubar.isactive = sep.menubar.closest(".JS9PluginContainer").css("visibility") === "visible";
}
sep.toolbar = $(`#${fromID}Toolbar`);
if( sep.toolbar.length > 0 ){
sep.toolbar.isactive = sep.toolbar.closest(".JS9PluginContainer").css("visibility") === "visible";
}
sep.statusbar = $(`#${fromID}Statusbar`);
if( sep.statusbar.length > 0 ){
sep.statusbar.isactive = sep.statusbar.closest(".JS9PluginContainer").css("visibility") === "visible";
}
sep.colorbar = $(`#${fromID}Colorbar`);
if( sep.colorbar.length > 0 && !sep.statusbar.length ){
sep.colorbar.isactive = sep.colorbar.closest(".JS9PluginContainer").css("visibility") === "visible";
}
if( sep.js9.length > 0 ){
// hack: height of the dhtml drag handle and status area
sep.width = sep.js9.width();
sep.height = sep.js9.height();
sep.top = sep.js9.offset().top - $(window).scrollTop() - LIT\_FUDGE;
sep.left = sep.js9.offset().left - $(document).scrollLeft();
if( sep.menubar.isactive ){
sep.height += sep.menubar.height();
sep.top -= sep.menubar.height();
}
if( sep.toolbar.isactive ){
sep.height += sep.toolbar.height();
sep.top -= sep.toolbar.height();
}
if( sep.statusbar.isactive ){
sep.height += sep.statusbar.height();
sep.top -= sep.statusbar.height();
} else if( sep.colorbar.isactive ){
sep.height += sep.colorbar.height();
sep.top -= sep.colorbar.height();
sep.top += COLORBAR\_FUDGE;
}
}
};
const getopts = (fromID, toID) => {
let html, winopts;
if( fromID ){
if( sep.js9.length > 0 ){
html = "";
if( sep.menubar.isactive ){
html += sprintf(menuStr, toID, sep.js9.width());
}
if( sep.toolbar.isactive ){
html += sprintf(toolStr, toID, sep.js9.width());
}
html += sprintf(js9Str, toID, sep.js9.width(),sep.js9.height());
if( sep.statusbar.isactive ){
html += sprintf(statusStr, toID, sep.js9.width());
} else if( sep.colorbar.isactive ){
html += sprintf(colorStr, toID, sep.js9.width());
}
}
if( sep.layout === "auto" ){
if( (sep.left + (sep.width \* (col+0.5))) > window.innerWidth ){
row++;
col = 0;
}
}
winopts = sprintf(winoptsStr,
sep.width,
sep.height,
sep.top + ((sep.height + sep.topMargin + sep.topExtra) \* row),
sep.left + ((sep.width + sep.leftMargin + sep.leftExtra) \* col));
// move to next column
if( sep.layout === "auto" || sep.layout === "horizontal" ){
col++;
} else if( sep.layout === "vertical" ){
row++;
}
}
// return info for this column;
return {id: toID, html: html, winopts: winopts};
};
const separateim = (arr) => {
let im, xopts, id;
const n = nsep++;
if( arr.length > n ){
if( typeof arr[n] === "number" ){
im = JS9.images[arr[n]];
} else {
im = arr[n];
}
// look for images in this display
if( im && im.display === this ){
// display this image so it's the current one we move
im.displayImage("all");
// init params
if( d0 === undefined ){
d0 = im.display.id;
initopts(im.display, d0, opts);
// if leave first image in place is false, decrement
// nsep so it gets separated on the next iteration
if( opts.firstinplace === false ){
nsep--;
}
separateim(arr);
} else {
// create a new window for this image
if( typeof opts.idbase === "string" ){
id = opts.idbase + myid++;
d1 = id;
} else {
d1 = `${d0.replace(rexp, "")}\_sep${JS9.uniqueID()}`;
}
saveims[d1] = im;
xopts = getopts(d0, d1);
// replace id, if idbase was supplied in opts
if( id ){
xopts.id = id;
}
if( sep.layout === "grid" ){
// a div hold the html for this separated display,
// and is appended to grid container
$("

")
.prop("id", xopts.id + "GridItem")
.addClass("JS9GridItem")
.append($(xopts.html))
.appendTo(sep.container);
// create the new JS9 display, with associated plugins
JS9.AddDivs(xopts.id);
// move this image
saveims[xopts.id].moveToDisplay(xopts.id);
// process next image
separateim(arr);
} else {
// create a light wndow
// code to run when new window exists
$(JS9.lightOpts[JS9.LIGHTWIN].topid)
.arrive(`#${d1}`, {onceOnly: true}, (el) => {
id = $(el).attr("id");
// FF (at least) needs this 0ms delay
window.setTimeout(() => {
// move this image
saveims[id].moveToDisplay(id);
// process next image
separateim(arr);
}, 0);
});
// load new window, code above gets run when window exists
JS9.LoadWindow(null, {id: xopts.id}, "light",
xopts.html, xopts.winopts);
}
}
} else {
// this image is in a different display, so process next image
separateim(arr);
}
} else {
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
if( this.image ){
this.image.xeqPlugins("image", "onseparatedisplay");
}
}
}
};
// opts are optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse separate opts: ${opts}`, e); }
}
// array of images to use
arr = opts.images || JS9.images;
// start separating the images
separateim(arr);
};
// display the next image from the JS9 images list which is in this display
JS9.Display.prototype.nextImage = function(inc){
let i, idx, nidx, im, dpos, npos;
let ims = [];
let masks = [];
inc = inc || 1;
if( !this.image ){
return this;
}
dpos = this.image.pos;
// make list of image masks for this display
if( !JS9.globalOpts.nextImageMask ){
for(i=0; i= 0 ){
continue;
}
// candidate image
ims.push(im);
}
// if there is only one image, we're done
if( ims.length <= 1 ){
return this;
}
// get index into images array for the currently displayed image
for(idx=0; idx= ims.length ){
nidx -= ims.length;
}
// wrap if necessary
while( nidx < 0 ){
nidx += ims.length;
}
// display if we are not back to where we started
if( idx !== nidx ){
// display image, 2D graphics, etc.
im = ims[nidx];
im.displayImage("all");
// already done in displayImage()
// im.refreshLayers();
im.display.clearMessage();
if( dpos ){
npos = im.displayToImagePos(dpos);
im.valpos = null;
im.valpos = im.updateValpos(npos, true);
}
}
// allow chaining
return this;
};
// load session from a json file
// NB: save is an image method, load is a display method
JS9.Display.prototype.loadSession = function(file, opts){
let obj, left;
const objs = {};
const finish = (im) => {
let i, dlayer, layer, lname, obj;
const dorender = () => {
// update layer's shape counter
const objs = dlayer.canvas.getObjects();
if( objs && typeof objs.length !== "undefined" ){
im.layers[dlayer.layerName].nshape = objs.length + 1;
}
// update objects for parents and children
JS9.Fabric.updateChildren(dlayer, null, "objects");
// change shape positions if the displays sizes differ
im.refreshLayers();
};
// see: http://fabricjs.com/v5-breaking-changes
const reviver = (data, instance) => {
// detect that version is less than 5
// change radians to degrees (for circles)
if (parseInt(data.version.slice(0, 1), 10) < 5) {
if( instance.startAngle ) instance.startAngle \*= 180 / Math.PI;
if( instance.endAngle ) instance.endAngle \*= 180 / Math.PI;
}
};
obj = objs[im.file] || {};
// reconstitute blend state
if( obj.blend ){
im.blend = $.extend(true, {}, obj.blend);
}
// reconstitute tmp values
if( obj.tmp ){
im.tmp = $.extend(true, {}, obj.tmp);
}
// reconstitute wcsim state
if( obj.wcsim ){
im.wcsim = JS9.lookupImage(obj.wcsim);
}
// reconstitute layers
if( obj.layers && obj.layers.length ){
for(i=0; i= 0 &&
lname === "regions" ){
continue;
}
// skip crosshair and grid
if( lname === "crosshair" || lname === "grid" ){
continue;
}
// make sure layer exists in the display
dlayer = this.newShapeLayer(lname, layer.dopts);
// add a layer instance to this image (no objects yet)
im.addShapes(lname, []);
// load the session objects into the layer and render
dlayer.canvas.loadFromJSON(layer.json, dorender, reviver);
// restore catalog and starbase, if necessary
if( layer.catalog ){
im.layers[lname].catalog = layer.catalog;
}
if( layer.starbase ){
try{im.layers[lname].starbase = JSON.parse(layer.starbase);}
catch(ignore){ /\* empty \*/ }
}
}
}
// if coordinate grid was active, display it
if( im.tmp && im.tmp.gridStatus === "active" ){
im.displayCoordGrid(true);
}
// if all images are loaded, sort them to the original load order
if( JS9.notNull(left) ){
left = left - 1;
if( left === 0 ){
JS9.images.sort((a, b) => {
let ai = 0, bi = 0;
if( objs[a.file] ){ ai = objs[a.file].i; }
if( objs[b.file] ){ bi = objs[b.file].i; }
return ai - bi;
});
}
}
// re-execute from the xeq stash
if( obj.xeqstash ){
im.xeqStashCall(obj.xeqstash);
}
// plugin callbacks
if( JS9.globalOpts.extendedPlugins ){
im.xeqPlugins("image", "onsessionload");
}
// execute onsessionload callback, if necessary
if( typeof opts.onsessionload === "function" ){
try{ JS9.xeqByName(opts.onsessionload, window, im); }
catch(e){ JS9.error("in onsessionload callback", e, false); }
}
};
const loadit = (imobj) => {
let pname;
// sanity check
if( !imobj.file ){
JS9.error("session does not contain a filename");
}
// save copy of object so we can edit it
obj = $.extend(true, {}, imobj);
// some param info needs to be deleted
delete obj.params.display;
// unset crosshair (we don't save it or load it)
obj.params.crosshair = false;
// include an onload callback to load the layers
obj.params.onload = finish;
// get pathname of image file
pname = obj.file;
// add section info
if( obj.sect ){
obj.params.xcen = obj.sect.xcen;
obj.params.ycen = obj.sect.ycen;
obj.params.xdim = obj.sect.xdim;
obj.params.ydim = obj.sect.ydim;
obj.params.zoom = obj.sect.zoom;
delete obj.sect;
}
// desktop only: are session file paths relative to the session path?
if( window.electron &&
JS9.desktopOpts.sessionPath &&
opts.sessionPath &&
obj.file.charAt(0) !== "/" &&
!obj.file.match(JS9.URLEXP) ){
pname = JS9.fixPath(opts.sessionPath + obj.file, opts);
}
// save for finish
objs[pname] = obj;
// load the image
JS9.Load(pname, obj.params, {display: this.id});
};
const loadem = (jobj) => {
let i, key, cmap, xobj;
// restore (and remove) globals
if( jobj.globalOpts ){
$.extend(true, JS9.globalOpts, jobj.globalOpts);
delete jobj.globalOpts;
}
// load colormaps
if( jobj.cmaps ){
for(i=0; i= 0 ){
xobj = {toplevel: true};
} else {
xobj = {toplevel: false};
}
JS9.AddColormap(cmap, xobj);
}
}
// load images
if( jobj.images ){
left = jobj.images.length;
for(i=0; i {
loadem(jobj);
},
error: (jqXHR, textStatus, errorThrown) => {
JS9.error(`could not load session: ${file}`, errorThrown);
}
});
}
// allow chaining
return this;
};
// dummy routines to display/clear message, overwritten in info plugin
// eslint-disable-next-line no-unused-vars
JS9.Display.prototype.displayMessage = function(type, message, target){
return;
};
// eslint-disable-next-line no-unused-vars
JS9.Display.prototype.clearMessage = function(which){
return;
};
// create a mosaic from a multi-extension FITS file or a number of images
JS9.Display.prototype.createMosaic = function(ims, opts){
let i, im, bin, carr;
const im0 = this.image;
const line1 = "| fname|";
const line2 = "| char|";
// remove temp files
const cleanup = () => {
let i;
for(i=0; i {
let earr;
// check for Montage error
if( rstr.search(/\[struct stat="OK"/) < 0 ){
// no longer waiting
JS9.waiting(false);
// first remove temp files
cleanup();
// signal this we completed the reproject attempt
earr = rstr.match(/msg="(.\*)"/);
if( earr && earr[1] ){
JS9.error(`${earr[1]} (from ${prog})`);
} else {
JS9.error(rstr || `unknown ${prog} failure`);
}
}
};
// display mosaic as a new image
const disp = (hdu, opts) => {
let topts, nim;
opts = opts || {};
topts = $.extend(true, {}, opts);
// start the waiting!
if( opts.waiting !== false ){
JS9.waiting(true, this);
}
// make sure we use the current display
topts.display = this.id;
// set up new and display new image
nim = new JS9.Image(hdu, topts);
// set status of both old and new image
im0.setStatus("createMosaic", "complete");
nim.setStatus("createMosaic", "complete");
// done waiting
JS9.waiting(false);
// everything else is done so call onmosaic func, if necessary
if( opts.onmosaic ){
try{ JS9.xeqByName(opts.onmosaic, window, nim); }
catch(e){ JS9.error("in create mosaic callback", e, false); }
}
};
// write comforting messages to the console while we wait and wait
const log = (...args) => {
let s;
if( opts.verbose || JS9.DEBUG > 1 ){
s = sprintf(...args);
// eslint-disable-next-line no-console
JS9.log(s);
}
};
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse createMosaic opts: ${opts}`, e); }
}
// reduce can be taken from the global value
opts.reduce = opts.reduce || JS9.globalOpts.reduceMosaic;
// same for reduction dims
opts.dim = opts.dim ||
Math.max(JS9.globalOpts.image.xdim, JS9.globalOpts.image.ydim);
// ims can be: array of ims or a single im or null (use displayed image)
// each im can itself be an im object or the image string id
if( !ims ){
// use currently display image, if possible
if( this.image ){
ims = [this.image];
} else {
ims = [];
}
} else if( typeof ims === "string" ){
if( ims === "current" ){
// use the currently loaded image
if( this.image ){
ims = [this.image];
} else {
ims = [];
}
} else if( ims === "all" ){
// use all images in this display
ims = [];
for(i=0; i {
let s, t, v, sw, naxis, rstr, inbuf, ext;
let vfile, ivfile, ovfile, bvfile, sect, topts;
let inlst, intbl, inhdr, inarr, binlst, bintbl;
let outlst, outtbl, outhdr, areafile, outfile;
const id = JS9.uniqueID();
const imsw = "-C"; // skip naxis[3,4]: they write garbage into the table
const mktmp = (suffix) => {
return `mosaic\_${id}\_${suffix}`;
};
// temps files get unique names
inlst = mktmp("in.lst");
intbl = mktmp("in.tbl");
inhdr = mktmp("in.hdr");
binlst = mktmp("bin.lst");
bintbl = mktmp("bin.tbl");
outlst = mktmp("out.lst");
outtbl = mktmp("out.tbl");
outhdr = mktmp("out.hdr");
// output file name comes from the first image name
outfile = ims[0].id
.replace(/\[.\*\]/, "")
.replace(/\.fz$/i, "")
.replace(/\.gz$/i, "")
.replace(/\.fits$/i, "\_mosaic.fits");
// Montage temp areafile comes from the output file name
areafile = outfile.replace(/\.fits$/, "\_area.fits");
// init cleanup array to make sure temp files get deleted
carr = [inlst, intbl, inhdr, binlst, bintbl,
outlst, outtbl, outhdr, areafile];
// generate input list from array of ims
s = `${line1}\n${line2}\n`;
for(i=0; i %s", vfile, ext, ovfile);
rstr = JS9.reproject(vfile, ovfile, outhdr, sw);
// check for errors
chkerr("mProjectPP", rstr);
}
}
// save output list in file
JS9.vfile(outlst, s);
// call the Mosaic/mImgtbl routine
rstr = JS9.imgtbl(outlst, ".", outtbl, "");
// check for errors
chkerr("mImgtbl", rstr);
// make sure input table has FITS files
if( !JS9.vsize(outtbl) ){
JS9.error("no FITS files were added to output table for mosaic");
}
// make the mosaic
log("create mosaic: %s", outfile);
rstr = JS9.madd(outtbl, outhdr, outfile, "");
// check for errors
chkerr("mAdd", rstr);
// cleanup temp files
cleanup();
// construct options
topts = $.extend(true, {}, JS9.fits.options, opts);
// we want the full image
topts.image = {xdim: 0, ydim: 0};
topts.file = outfile;
// process the newly retrieved data as FITS
JS9.fits.handleFITSFile(outfile, topts, disp);
}, JS9.SPINOUT);
// allow chaining
return this;
};
// swap images in the images stack for this display
// used by the sortable routine to switch images in a stack
// for moving an element of an array:
// https://stackoverflow.com/questions/5306680/move-an-array-element-from-one-array-position-to-another
JS9.Display.prototype.moveImageInStack = function(from, to){
let i, j, nfrom, nto;
for(i=0, j=0; i 1 ){
JS9.log("JS9 command: %s", this.name);
}
};
// get the display tied to this command (as well as the current image).
JS9.Command.prototype.getDisplayInfo = function(display){
if( display && display.id ){
this.display = display;
this.image = display.image;
}
// allow chaining
return this;
};
// return "get" or "set" to specify which command to run
JS9.Command.prototype.getWhich = function(args){
let which;
if( this.get && !this.set ){
which = "get";
} else if( this.set && !this.get ){
which = "set";
} else if( this.which ){
which = this.which(args);
} else if( args.length === 0 ){
which = "get";
} else {
which = "set";
}
return which;
};
// ---------------------------------------------------------------------
// JS9 helper to manage connection to back-end services
// ---------------------------------------------------------------------
JS9.Helper = function(){
// reset protocol for file:
if( JS9.globalOpts.helperProtocol === "file:" ){
JS9.globalOpts.helperProtocol = "http:";
}
// reset helper timeout for local access
if( !document.domain || document.domain === "localhost" ){
JS9.globalOpts.htimeout = JS9.globalOpts.lhtimeout;
}
// add suffix, if necessary
if( !JS9.globalOpts.helperProtocol.match(/\/\/$/) ){
JS9.globalOpts.helperProtocol += "//";
}
// assume the worst
this.connected = false;
this.helper = false;
// set up initial type of helper connection
if( JS9.allinone && !JS9.globalOpts.allinoneHelper ){
this.type = "none";
} else {
this.type = JS9.globalOpts.helperType || "sock.io";
}
// no page id yet
this.pageid = null;
// make the connection
this.connect();
};
// get back-end helper connection info
JS9.Helper.prototype.connectinfo = function(){
let s;
// no connection configured
if( JS9.helper.connected === null ){
return "notConfigured";
}
// connection configured and established
if( JS9.helper.connected ){
s = `connected ${JS9.helper.type} ${JS9.helper.url}`;
if( JS9.helper.pageid ){
s += `

${JS9.helper.pageid}`;
}
return s;
}
// connection configured but not established
return `notConnected ${JS9.helper.type}`;
};
// connect to back-end helper
JS9.Helper.prototype.connect = function(type){
let sockbase, sockfile;
const tries = JS9.globalOpts.ehretries;
const delay = JS9.globalOpts.ehtimeout;
const failedHelper = (textStatus, errorThrown) => {
this.connected = false;
this.helper = false;
this.ready = true;
$(document).trigger("JS9:helperReady",
{type: "socket.io", status: "error"});
textStatus = textStatus || "timeout";
if( !errorThrown || errorThrown === "timeout" ){
errorThrown = "or connection refused";
}
if( errorThrown === textStatus ){
textStatus = "";
}
if( errorThrown === "error" ){
errorThrown = "is the helper running?";
}
// throw error if needed
if( JS9.globalOpts.requireHelper ){
JS9.error(`helper connect error: ${textStatus} (${errorThrown})`);
} else if( JS9.DEBUG ){
JS9.log(`JS9 helper connect error: ${textStatus} (${errorThrown})`);
}
};
const connectHelper = (url) => {
// connect to helper
$.ajax({
url: url,
dataType: "script",
timeout: JS9.globalOpts.htimeout,
cache: true,
success: () => {
// if there is no io object, we didn't really succeed
// can happen, for example, in the Jupyter environment
if( typeof io === "undefined" ){
failedHelper("socket io object is undefined", null);
return;
}
// connect to the helper
this.socket = io.connect(this.url, JS9.socketioOpts);
// on-event processing
this.socket.on("connect", () => {
let ii, d, p;
this.connected = true;
this.helper = true;
d = [];
for(ii=0; ii {
this.pageid = obj.pageid;
this.js9helper = obj.js9helper;
JS9.globalOpts.dataPathModify = obj.dataPathModify;
this.ready = true;
$(document).trigger("JS9:helperReady",
{type: "socket.io", status: "OK"});
if( JS9.DEBUG ){
JS9.log(`JS9 helper: connect: ${this.type}`);
}
});
$(document).trigger("JS9:connected",
{type: "socket.io", status: "OK"});
});
this.socket.on("connect\_error", () => {
this.connected = false;
this.helper = false;
if( JS9.DEBUG > 1 ){
JS9.log("JS9 helper: connect error");
}
});
this.socket.on("connect\_timeout", () => {
this.connected = false;
this.helper = false;
if( JS9.DEBUG > 1 ){
JS9.log("JS9 helper: connect timeout");
}
});
this.socket.on("disconnect", (reason) => {
this.connected = false;
this.helper = false;
if( JS9.DEBUG > 1 ){
JS9.log(`JS9 helper: disconnect: ${reason}`);
}
// https://github.com/socketio/socket.io-client/blob/master/docs/API.md#event-disconnect
if( reason === "io server disconnect" ){
// the disconnection was initiated by the server,
// you need to reconnect manually
if( JS9.DEBUG > 1 ){
JS9.log("JS9 helper: manual reconnect");
}
this.socket.connect();
}
// else the socket will automatically try to reconnect
});
this.socket.on("reconnect", () => {
this.connected = true;
this.helper = true;
if( JS9.DEBUG > 1 ){
JS9.log("JS9 helper: reconnect");
}
});
this.socket.on("msg", JS9.msgHandler);
},
error: (jqXHR, textStatus, errorThrown) => {
failedHelper(textStatus, errorThrown);
}
});
};
// make an "alive" request of the helper (jsonp to avoid CORS rejection)
const waitForHelper = (eurl, hurl, tries) => {
$.ajax({
url: eurl,
dataType: "jsonp",
success: () => {
connectHelper(hurl);
},
error: () => {
if( --tries > 0 ){
window.setTimeout(() => {
waitForHelper(eurl, hurl, tries);
}, delay);
} else {
failedHelper();
}
}
});
};
// might be establishing a new type
if( type ){
this.type = type;
}
// close off previous socket connection, if necessary
if( this.socket ){
try{this.socket.disconnect();}
catch(e){JS9.log("warning: can't disconnect from socket");}
this.socket = null;
}
// base of helper url is either specified, same as current domain, or local
if( JS9.globalOpts.helperURL ){
if( JS9.globalOpts.helperURL.search(/:\/\//) >=0 ){
this.url = JS9.globalOpts.helperURL;
} else {
this.url = JS9.globalOpts.helperProtocol + JS9.globalOpts.helperURL;
}
} else if( document.domain ){
if( location.origin ){
this.url = location.origin;
} else {
this.url = JS9.globalOpts.helperProtocol + document.domain;
}
} else {
this.url = `${JS9.globalOpts.helperProtocol}localhost`;
}
// save base of url
this.baseurl = this.url;
// try to establish connection, based on connection type
switch(this.type){
case "none":
this.connected = null;
this.ready = true;
// signal JS9 helper is ready
$(document).trigger("JS9:helperReady", {type: "none", status: "OK"});
break;
case "get":
case "post":
// sanity check
if( !JS9.globalOpts.helperCGI ){
JS9.error("cgi script name missing for helper");
}
this.url += `/${JS9.globalOpts.helperCGI}`;
this.connected = true;
this.helper = true;
if( JS9.DEBUG ){
JS9.log(`JS9 helper: connect: ${this.type}`);
}
this.ready = true;
$(document).trigger("JS9:helperReady", {type: "get", status: "OK"});
break;
case "sock.io":
case "nodejs":
if( !JS9.globalOpts.helperPort ){
JS9.error("port missing for helper");
}
// ignore port on url, add our own
this.url = `${this.url.replace(/:[0-9][0-9]\*$/, "")}:${JS9.globalOpts.helperPort}`;
// which version of socket.io?
sockbase = "socket.io";
// use min version for production, as per migration docs
if( JS9.DEBUG <= 2 ){
sockfile = "socket.io.min.js";
} else {
sockfile = "socket.io.js";
}
// full url of the socket.io.js file
this.sockurl = `${this.url}/${sockbase}/${sockfile}`;
// make sure helper is running and then connect
if( window.electron ){
this.aliveurl = `${this.url}/alive`;
waitForHelper(this.aliveurl, this.sockurl, tries);
} else {
connectHelper(this.sockurl);
}
break;
default:
JS9.error(`unknown helper type: ${this.type}`);
break;
}
};
// send request to back-end helper
JS9.Helper.prototype.send = function(key, obj, cb){
// sanity check
if( !this.connected ){ return null; }
// add cookie value
// add dataPath, if available (but always look in the helper directory)
if( obj && (typeof obj === "object") ){
// wrap this in a try to catch CORS errors
try{ obj.cookie = document.cookie; }
catch(e){ delete obj.cookie; }
if( JS9.globalOpts.dataPath && !obj.dataPath ){
obj.dataPath = `${JS9.globalOpts.dataPath}:.`;
}
} else {
obj = {dataPath: "."};
}
// add path which gets us to the js9 root
if( JS9.TOROOT ){
obj.dataPath += `:${JS9.TOROOT}`;
}
// tell server how to get to root (for datapath)
// send message, based on connection type
switch(this.type){
case "get":
case "post":
obj.key = key;
if( JS9.helper.pageid ){
obj.pageid = JS9.helper.pageid;
}
if( JS9.DEBUG ){
JS9.log("JS9 cgi helper [%s, %s]: %s",
this.type, JSON.stringify(obj), this.url);
}
$.ajax({
url: this.url,
type: this.type.toUpperCase(),
data: obj,
dataType: "text",
success: (data) => {
if( typeof data === "string" &&
data.search(JS9.analOpts.epattern) >=0 ){
JS9.log(data);
}
if( cb ){
cb(data);
}
},
error: (jqXHR, textStatus, errorThrown) => {
if( JS9.DEBUG ){
JS9.log(`JS9 helper: ${this.type} failure: ${textStatus} ${errorThrown}`);
}
}
});
break;
case "sock.io":
case "nodejs":
JS9.helper.socket.emit(key, obj, cb);
break;
}
// allow chaining
return this;
};
// ---------------------------------------------------------------------
// JS9 web worker support to off-load CPU intensive tasks
// ---------------------------------------------------------------------
// create new web worker
JS9.WebWorker = function(url){
const finishup = () => {
this.worker.onmessage = JS9.WebWorker.prototype.msgHandler.bind(this);
this.handlers = [];
};
if( url.match(JS9.URLEXP) ){
// avoid cross-origin problems if the webworker is being retrieved
// from somewhere other than the local host
// this leaks a small bit of memory (no revokeObjectURL call)
JS9.fetchURL(null, url, null, (blob) => {
this.worker = new Worker(URL.createObjectURL(blob));
finishup();
});
} else {
// ordinary retrieval of a local file
this.worker = new Worker(url);
finishup();
}
};
// handle (known) messages from web worker
JS9.WebWorker.prototype.msgHandler = function(msg){
let i, handler;
const h = JS9.helper;
const obj = msg.data;
switch(obj.cmd){
case "progress":
JS9.progress(obj.result.value, obj.result.max);
break;
case "initsocketio":
if( obj.result === "OK" ){
this.sockinit = true;
for(i=0; i 1 ){
JS9.log(`JS9 worker socketio: ${obj.cmd}`);
}
break;
case "disconnect":
delete JS9.worker.uploadActive;
JS9.progress(false);
obj.result = obj.result || "JS9 worker socket was disconnected";
// need a slight delay here, not sure why
window.setTimeout(() => {
JS9.worker.send("initsocketio", [h.url, h.pageid],
() => {
if( obj.alert ){
alert(obj.result);
} else if( JS9.DEBUG > 1 ){
JS9.log(obj.result);
}
});
}, JS9.WORKEROUT);
break;
case "error":
delete JS9.worker.uploadActive;
JS9.progress(false);
JS9.error(obj.result||"in web worker");
break;
default:
break;
}
};
// send a message to a web worker
JS9.WebWorker.prototype.send = function(cmd, args, func, xfer){
const id = cmd + JS9.uniqueID();
const obj = {id, cmd, args};
// push context
if( func ){
args = args || [];
this.handlers.push({id, cmd, args, func});
}
// send message, possibly with transferred data
if( xfer ){
this.worker.postMessage(obj, xfer);
} else {
this.worker.postMessage(obj);
}
};
// initialize worker socketio connection, then call handler
JS9.WebWorker.prototype.socketio = function(handler){
const h = JS9.helper;
JS9.worker.send("initsocketio", [h.url, h.pageid], (s) => {
if( s === "OK" ){
if( handler ){ handler(); }
} else {
JS9.error(`can't init socket.io for JS9 worker: ${s}`);
}
});
};
// terminate a web worker
JS9.WebWorker.prototype.terminate = function(){
this.worker.terminate();
};
// ---------------------------------------------------------------------
// Graphics support using fabric.js
//
// Fabric object defines graphical primitives
// ---------------------------------------------------------------------
// quick way to separate fabric versions
fabric.major\_version = parseFloat(fabric.version.split(".")[0]);
fabric.minor\_version = parseFloat(fabric.version.split(".")[1]);
fabric.patch\_version = parseFloat(fabric.version.split(".")[2]);
// fabric sub-object to hold fabric routines
JS9.Fabric = {};
// extra fabric elements to save when switching between images
JS9.Fabric.elements = ["cornerSize", "cornerColor", "cornerStyle",
"borderColor",
"transparentCorners", "selectionLineWidth",
"centeredScaling", "hasControls", "hasRotatingPoint",
"lockMovementX", "lockMovementY", "lockRotation",
"lockScalingX", "lockScalingY", "lockUniScaling",
"selectable", "hasBorders", "params", "pub"];
// global options for all shapes
JS9.Fabric.opts = {
// default fabric.js options
originX: "center",
originY: "center",
strokeWidth: 2,
selectionLineWidth: 2,
borderColor: "#00EEFF",
cornerColor: "#00EEFF",
cornerSize: fabric.isTouchSupported ? 10 : 6,
cornerStyle: "circle",
hasControls: true,
hasRotatingPoint: true,
hasBorders: true,
transparentCorners: false,
centeredScaling: true,
strokeUniform: true,
selectable: true,
// minimizes the jump when first changing the region size
padding: 0,
canvas: {
selection: true
},
fill: "transparent",
objectCaching: false
};
// rescale the width of shapes in the shape layers
JS9.Fabric.rescaleStrokeWidth = function(scale, sw1){
const tscale = ((this.scaleX + this.scaleY) / 2);
// fabric 3.6.3+ supports strokeUniform, including for groups
if( fabric.major\_version >= 4 ||
(fabric.major\_version === 3 &&
fabric.minor\_version === 6 &&
fabric.patch\_version >= 3) ){
return;
}
// fabric 2+ supports strokeUniform, but not for groups
// still, it fixes the different strokeWidth problem for rectangular boxes
if( fabric.major\_version >= 2 && this.params &&
this.params.shape !== "annulus" && this.params.shape !== "cross" ){
return;
}
scale = scale || 1;
scale \*= tscale;
if( !sw1 && this.params ){
sw1 = this.params.sw1;
}
if( !sw1 ){
return;
}
if( this.type === "group" ){
this.forEachObject( (obj) => {
obj.rescaleBorder(scale, sw1);
});
} else {
this.set("strokeWidth", sw1 / scale);
}
};
// ensure the circle scales the same in X and Y
JS9.Fabric.rescaleEvenly = function(){
let lastscale;
if( !this.params || (this.scaleX === this.scaleY) ){
return;
}
switch(this.params.shape){
case "annulus":
case "circle":
lastscale = this.params.lastscale || 1;
if( this.scaleX !== lastscale ){
this.scaleY = this.scaleX;
} else if( this.scaleY !== lastscale ){
this.scaleX = this.scaleY;
}
this.params.lastscale = this.scaleX;
break;
}
};
// add to fabric object prototype
fabric.Object.prototype.rescaleBorder = JS9.Fabric.rescaleStrokeWidth;
fabric.Object.prototype.rescaleEvenly = JS9.Fabric.rescaleEvenly;
// ---------------------------------------------------------------------
// Shape prototype additions to JS9 Display class
// ---------------------------------------------------------------------
// create a new shape layer in the display
// call using display context
JS9.Fabric.newShapeLayer = function(layerName, layerOpts, divjq){
let id, dlayer;
const display = this;
const shupdate = (obj, s) => {
let i, o, objs;
let im = dlayer.display.image;
let ao = dlayer.canvas.getActiveObject();
let opts = {};
// sanity check
if( !im ){ return; }
if( obj.params ){
if( ao.type === "activeSelection" ){
opts.group = ao;
}
im.\_updateShape(layerName, obj, opts, s);
} else if( (obj.type === "activeSelection") ||
(obj.type === "group" && !obj.params) ){
objs = obj.getObjects();
for(i=0; i {
// sanity check
if( !display.image ){ return; }
// update multiselect dialog box for this image, if necessary
dlayer.display.image.\_updateMultiDialogs(setmode);
}
const seloff = (dlayer, obj) => {
// reset currently selected
dlayer.params.sel = null;
// reset currently selected layer
if( dlayer.display.image ){
dlayer.display.image.layer = null;
}
// selection cleared processing
// remove anchors from previously selected polygon
if( obj ){
switch(obj.type){
case "polyline":
case "polygon":
JS9.Fabric.removePolygonAnchors(dlayer, obj);
// renderAll() throws an error, might be related to:
// http://fabricjs.com/v2-breaking-changes-2
// dlayer.canvas.renderAll();
break;
}
// region updates
shupdate(obj, "unselect");
// update multi-select dialog
seldialog(-1);
}
};
// eslint-disable-next-line no-unused-vars
const selmultioff = (dlayer, opts) => {
let i, obj, aobjects;
aobjects = dlayer.canvas.getActiveObjects();
for(i=0; i {
// turn off previous selection, if necessary
if( dlayer.params.sel && obj.params && (dlayer.params.sel !== obj) ){
seloff(dlayer, dlayer.params.sel);
}
// set currently selected layer
if( dlayer.display.image ){
dlayer.display.image.layer = layerName;
}
// new selection processing
if( obj ){
// add anchors to selected polygon
switch(obj.type){
case "polyline":
case "polygon":
JS9.Fabric.addPolygonAnchors(dlayer, obj);
dlayer.canvas.renderAll();
break;
}
// set currently selected shape
if( obj.polyparams ){
dlayer.params.sel = obj.polyparams.polygon;
} else if( obj.params ){
dlayer.params.sel = obj;
}
// region updates
shupdate(obj, "select");
// update multi-select dialog
seldialog(1);
}
};
// eslint-disable-next-line no-unused-vars
const selmultion = (dlayer, opts, activeObject) => {
let i, j, obj, parent, child, objs;
// turn off previous selection, if necessary
if( dlayer.params.sel && (dlayer.params.sel !== activeObject) ){
seloff(dlayer, dlayer.params.sel);
}
// get current active object if necessary
activeObject = activeObject || dlayer.canvas.getActiveObject();
// and the associated objects
objs = dlayer.canvas.getActiveObjects();
for(i=0; i")
.addClass("JS9Container")
.css("z-index", 0)
.appendTo(divjq);
// create canvas element and append to container
dlayer.canvasjq = $("")
.addClass("JS9Layer")
.attr("id", id)
.attr("width", divjq.css("width"))
.attr("height", divjq.css("height"))
.appendTo(dlayer.divjq);
if( JS9.bugs.webkit\_resize && dlayer.dtype === "main" ){
dlayer.canvasjq
.attr("width", display.width)
.attr("height", display.height);
}
// new fabric canvas associated with this HTML canvas
dlayer.canvas = new fabric.Canvas(dlayer.canvasjq[0]);
// don't render on add or remove of objects (do it manually)
dlayer.canvas.renderOnAddRemove = false;
// preserve stacking (required in v1.6.6 to interact with polygon points)
dlayer.canvas.preserveObjectStacking = true;
// movable: short-hand for allowing objects to move (not resize)
if( dlayer.opts.movable ){
dlayer.opts.lockMovementX = false;
dlayer.opts.lockMovementY = false;
dlayer.opts.selectable = true;
dlayer.opts.evented = true;
} else if( dlayer.opts.movable === false ){
dlayer.opts.lockMovementX = true;
dlayer.opts.lockMovementY = true;
dlayer.opts.selectable = false;
dlayer.opts.evented = false;
}
// deprecated
if( (dlayer.opts.changeable === undefined) &&
(dlayer.opts.fixinplace !== undefined) ){
dlayer.opts.changeable = !dlayer.opts.fixinplace;
}
// locked: opposite alias of changeable
if( (dlayer.opts.changeable === undefined) &&
(dlayer.opts.locked !== undefined) ){
dlayer.opts.changeable = !dlayer.opts.locked;
}
// changeable: short-hand for allowing objects to move and resize
if( dlayer.opts.changeable ){
dlayer.opts.hasControls = true;
dlayer.opts.hasRotatingPoint = true;
dlayer.opts.hasBorders = true;
dlayer.opts.lockMovementX = false;
dlayer.opts.lockMovementY = false;
dlayer.opts.lockRotation = false;
dlayer.opts.lockScalingX = false;
dlayer.opts.lockScalingY = false;
dlayer.opts.lockUniScaling = false;
dlayer.opts.selectable = true;
dlayer.opts.evented = true;
dlayer.opts.usekeyboard = true;
} else if( dlayer.opts.changeable === false ){
dlayer.opts.hasControls = false;
dlayer.opts.hasRotatingPoint = false;
dlayer.opts.hasBorders = false;
dlayer.opts.lockMovementX = true;
dlayer.opts.lockMovementY = true;
dlayer.opts.lockRotation = true;
dlayer.opts.lockScalingX = true;
dlayer.opts.lockScalingY = true;
dlayer.opts.lockUniScaling = true;
dlayer.opts.selectable = false;
dlayer.opts.evented = false;
dlayer.opts.usekeyboard = false;
}
// short-hand for allowing group and individual selections
if( dlayer.opts.selectable ){
dlayer.opts.canvas.selection = true;
}
// are mouse callbacks defined in the opts object?
if( dlayer.opts.onmousedown || dlayer.opts.onmouseup ||
dlayer.opts.onmousemove || dlayer.opts.tooltip ||
dlayer.opts.onmouseover || dlayer.opts.onmouseout ){
dlayer.opts.evented = true;
if( dlayer.opts.onmousedown ){
dlayer.canvas.on("mouse:down", (opts) => {
if( dlayer.display.image && opts.target ){
let target = opts.target;
// nb: target might be a polygon anchor => no params
let params = target.params;
// set click state but ignore unchangeable regions
if( !params || (params && params.changeable !== false) ){
// on main window, set region click
if( dlayer.dtype === "main" ){
dlayer.display.image.clickInRegion = true;
dlayer.display.image.clickInLayer = layerName;
}
dlayer.opts.onmousedown.call(dlayer.canvas,
dlayer.display.image,
target.pub,
opts.e, target);
}
} else {
// only allow fabric selection if we have special key down
dlayer.canvas.\_selection = dlayer.canvas.selection;
if( dlayer.canvas.selection ){
dlayer.canvas.selection = JS9.specialKey(opts.e);
}
}
});
} else {
dlayer.canvas.on("mouse:down", (opts) => {
// only allow fabric selection if we have special key down
dlayer.canvas.\_selection = dlayer.canvas.selection;
if( dlayer.canvas.selection ){
dlayer.canvas.selection = JS9.specialKey(opts.e);
}
});
}
if( dlayer.opts.onmouseup ){
dlayer.canvas.on("mouse:up", (opts) => {
if( dlayer.display.image && opts.target ){
dlayer.opts.onmouseup.call(dlayer.canvas,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
// restore original selection state
dlayer.canvas.selection = dlayer.canvas.\_selection ||
dlayer.canvas.selection;
});
} else {
dlayer.canvas.on("mouse:up", () => {
// restore original selection state
dlayer.canvas.selection = dlayer.canvas.\_selection ||
dlayer.canvas.selection;
});
}
if( dlayer.opts.onmousemove ){
dlayer.canvas.on("mouse:move", (opts) => {
if( dlayer.display.image && opts.target ){
dlayer.opts.onmousemove.call(dlayer.canvas,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
});
}
if( dlayer.opts.onmouseover ){
dlayer.canvas.on("mouse:over", (opts) => {
if( dlayer.display.image && opts.target ){
dlayer.opts.onmouseover.call(dlayer.canvas,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
});
}
if( dlayer.opts.onmouseout ){
dlayer.canvas.on("mouse:out", (opts) => {
if( dlayer.display.image && opts.target ){
dlayer.opts.onmouseout.call(dlayer.canvas,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
});
}
if( dlayer.opts.onmousedblclick ){
dlayer.canvas.on("mouse:dblclick", (opts) => {
if( dlayer.display.image && opts.target ){
dlayer.opts.onmousedblclick.call(dlayer.canvas,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
});
}
if( dlayer.opts.tooltip ){
dlayer.canvas.on("mouse:over", (opts) => {
if( dlayer.display.image && opts.target ){
JS9.tooltip(opts.target.left+opts.target.width+2,
opts.target.top+opts.target.height+2,
dlayer.opts.tooltip,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
});
dlayer.canvas.on("mouse:out", (opts) => {
if( dlayer.display.image && opts.target ){
JS9.tooltip(opts.target.left, opts.target.top,
null,
dlayer.display.image,
opts.target.pub,
opts.e, opts.target);
}
});
}
} else {
dlayer.canvas.on("mouse:down", (opts) => {
// only allow fabric selection if we have special key down
dlayer.canvas.\_selection = dlayer.canvas.selection;
if( dlayer.canvas.selection ){
dlayer.canvas.selection = JS9.specialKey(opts.e);
}
});
dlayer.canvas.on("mouse:up", () => {
// restore original selection state
dlayer.canvas.selection = dlayer.canvas.\_selection ||
dlayer.canvas.selection;
});
}
// object modified
dlayer.canvas.on("object:modified", (opts) => {
let o, i, olen, myWidth, myHeight;
const objs = [];
// sanity check
if( !opts.target ){ return; }
o = opts.target;
// update deltas to connected parents
JS9.Fabric.updateChildren(dlayer, o, "deltas");
// might have to sort overlapping shapes by size
if( dlayer.opts.sortOverlapping ){
o.setCoords();
// find objects which intersect with this one
dlayer.canvas.forEachObject( (obj) => {
if( obj === o ){
return;
}
if( o.intersectsWithObject(obj) ){
myWidth = obj.getScaledWidth();
myHeight = obj.getScaledHeight();
objs.push({obj: obj, siz: myWidth \* myHeight});
}
});
// any intersecting shapes?
if( !objs.length ){
return;
}
myWidth = o.getScaledWidth();
myHeight = o.getScaledHeight();
// add current shape to array
objs.push({obj: o, siz: myWidth \* myHeight});
// sort in order of increasing size
objs.sort((a, b) => {
// using <= instead of < preserves order for =
if( a.siz <= b.siz ){
return -1;
} else {
return 1;
}
});
// re-order so smaller objects are in front
olen = objs.length;
for(i=0; i {
let o;
// sanity check
if( !opts.target ){ return; }
o = opts.target;
o.rescaleEvenly();
o.rescaleBorder();
JS9.Fabric.updateChildren(dlayer, o, "scaling");
if( (o.type === "activeSelection") || (o.type === "group") ){
shupdate(o, "scaling");
}
});
dlayer.canvas.on("object:moving", (opts) => {
let o;
// sanity check
if( !opts.target ){ return; }
o = opts.target;
JS9.Fabric.updateChildren(dlayer, o, "moving");
if( (o.type === "activeSelection") || (o.type === "group") ){
shupdate(o, "moving");
}
});
dlayer.canvas.on("object:rotating", (opts) => {
let o;
// sanity check
if( !opts.target ){ return; }
o = opts.target;
JS9.Fabric.updateChildren(dlayer, o, "rotating");
if( (o.type === "activeSelection") || (o.type === "group") ){
shupdate(o, "rotating");
}
});
// selection created: add anchors to polygon
dlayer.canvas.on("selection:created", (opts) => {
let obj;
if( JS9.globalOpts.skipSelectionProcessing ){ return; }
if( opts.target ){
// fabric v4
obj = opts.target;
if( obj.type === "activeSelection" ||
(obj.type === "group" && !obj.params) ){
selmultion(dlayer, opts, obj);
} else {
selon(dlayer, obj);
}
} else if( opts.selected && opts.selected.length ){
// fabric v5
if( opts.selected.length === 1 ){
obj = opts.selected[0];
selon(dlayer, obj);
} else {
selmultion(dlayer, opts);
}
}
});
// selection updated (adding a region to the current selection):
// add anchors to polygon
dlayer.canvas.on("selection:updated", (opts) => {
let obj;
if( JS9.globalOpts.skipSelectionProcessing ){ return; }
if( opts.target ){
// fabric v4
obj = opts.target;
if( obj.type === "activeSelection" ||
(obj.type === "group" && !obj.params) ){
selmultion(dlayer, opts, obj);
} else {
selon(dlayer, obj);
}
} else if( opts.selected && opts.selected.length ){
// fabric v5
if( opts.selected.length === 1 ){
obj = opts.selected[0];
selon(dlayer, obj);
} else {
selmultion(dlayer, opts);
}
}
});
// selection cleared
// v5: why does this work differently from the selection: events above???
// (i.e. still utilizes obj.target instead of obj.selected)
dlayer.canvas.on("before:selection:cleared", (opts) => {
let obj;
if( JS9.globalOpts.skipSelectionProcessing ){ return; }
// sanity check
if( !opts.target ){ return; }
obj = opts.target;
if( obj.type === "activeSelection" ||
(obj.type === "group" && !obj.params) ){
selmultioff(dlayer, opts);
} else {
seloff(dlayer, obj);
}
});
// if canvas moves (e.g. light window), calcOffset must be called ...
// there is no good cross-browser way to track an element changing,
// (advice is to set a timer!) so we just check when the mouse enters the
// div, because this is when the user will interact with some shape
// only do this if we are in a light window
if( dlayer.divjq.closest(JS9.lightOpts[JS9.LIGHTWIN].drag).length ){
if( fabric.isTouchSupported ){
dlayer.divjq.on("touchstart", () => {dlayer.canvas.calcOffset();});
} else {
dlayer.divjq.on("mouseenter", () => {dlayer.canvas.calcOffset();});
}
}
return dlayer;
};
// ---------------------------------------------------------------------------
// Shape prototype additions to JS9 Image class
// ---------------------------------------------------------------------------
// showShapeLayer: if mode is true, layer is displayed, otherwise hidden
// also an internal call which uses {local: true} to maybe hide/show layers
// call using image context
JS9.Fabric.showShapeLayer = function(layerName, mode, opts){
let jobj, xkey, layer, dlayer, canvas, objects, olen, obj;
let left = 0;
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer ){ return; }
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse showShapeLayer opts: ${opts}`, e); }
}
canvas = layer.canvas;
dlayer = this.display.layers[layerName];
// no args: return show mode
if( JS9.isNull(mode) ){
return layer.show;
}
if( mode === true || mode === "true" ){
// restore and show layer
if( !opts.local ){
layer.show = true;
// for non-internal show/hide, exit if we are not displaying image
if( this !== this.display.image ){
return;
}
}
// restore selection property
if( layer.show ){
canvas.selection = layer.opts.canvas.selection;
}
if( layer.json && layer.show ){
canvas.loadFromJSON(layer.json, () => {
let key, tdlayer, obj;
// update objects for parents and children
JS9.Fabric.updateChildren(layer.dlayer, null, "objects");
// translate these shapes if we resized while hidden
if( this.resize ){
canvas.getObjects().forEach( (o) => {
o.left += this.resize.left;
o.top += this.resize.top;
o.setCoords();
});
canvas.calcOffset();
}
layer.zindex = Math.abs(layer.zindex);
dlayer.divjq.css("z-index", layer.zindex);
// unselect selected objects in lower-zindex groups
for( key of Object.keys(this.layers) ){
if( (layerName !== key) && this.layers[key].show ){
tdlayer = this.display.layers[key];
if( tdlayer.divjq.css("z-index") < layer.zindex ){
obj = tdlayer.canvas.getActiveObject();
if( obj ){
JS9.Fabric.removePolygonAnchors(tdlayer,
obj);
if( tdlayer.canvas.getActiveObject() ){
tdlayer.canvas.discardActiveObject();
}
}
}
}
}
this.restoreSelection(layerName);
});
}
// remove resize object if we have no more hidden layers
for( xkey of Object.keys(this.layers) ){
if( this.layers[xkey].json ){
left++;
}
}
if( !left ){
this.resize = null;
}
// plugin callbacks
this.xeqPlugins("shape", "onshapelayershow", layerName);
} else {
// for non-internal show/hide, exit if we are not displaying image
if( !opts.local ){
if( this !== this.display.image ){
layer.show = false;
return;
}
}
// save and hide layer
if( layer.show ){
// can't use forEachObject, which loops in ascending order,
// because removing anchors changes the array destructively
objects = canvas.getObjects();
olen = objects.length;
while( olen-- ){
obj = objects[olen];
if( obj.params ){
if( obj.params.winid ){
obj.params.winid.close();
obj.params.winid = null;
}
if( obj.params.anchors ){
JS9.Fabric.removePolygonAnchors(layer.dlayer, obj);
}
}
}
jobj = canvas.toJSON(layer.dlayer.el);
layer.json = JSON.stringify(jobj);
this.saveSelection(layerName);
canvas.selection = false;
// push towards the bottom of the pile
if( dlayer ){
layer.zindex = -Math.abs(layer.zindex);
dlayer.divjq.css("z-index", layer.zindex);
}
canvas.clear();
}
if( !opts.local ){
layer.show = false;
}
// plugin callbacks
this.xeqPlugins("shape", "onshapelayerhide", layerName);
}
return this;
};
// display all layers for the current image (save previous)
// call using image context
JS9.Fabric.displayShapeLayers = function(){
let key;
// if prev and cur are the same, just exit
if( this === this.display.image ){
return;
}
// this.display.image still points to the previously loaded image
// save old layers
if( this.display.image && this.display.image.layers ){
for( key of Object.keys(this.display.image.layers) ){
this.display.image.showShapeLayer(key, false, {local: true});
}
}
// "this" points to the current image: display new layers
if( this.layers ){
for( key of Object.keys(this.layers) ){
this.showShapeLayer(key, true, {local: true});
}
}
};
// toggle display of active layers for the current image (save previous)
// call using image context
JS9.Fabric.toggleShapeLayers = function(){
let key, layer;
if( this.toggleLayers ){
// toggleLayers => we are currently hidden, so display them
for( key of Object.keys(this.layers) ){
layer = this.layers[key];
if( layer && this.toggleLayers[key] ){
this.showShapeLayer(key, true);
}
}
delete this.toggleLayers;
} else {
// no toggleLayers => we are currently displayed, so hide them
this.toggleLayers = {};
for( key of Object.keys(this.layers) ){
if( key === "crosshair" ){
continue;
}
layer = this.layers[key];
if( layer && layer.show && layer.dlayer.dtype === "main" ){
this.toggleLayers[key] = true;
this.showShapeLayer(key, false);
}
}
}
};
// retrieve (and initialize, if necessary) a shape layer
// call using image context
// eslint-disable-next-line no-unused-vars
JS9.Fabric.getShapeLayer = function(layerName, opts){
let dlayer, layer;
// sanity check
if( !layerName ){ return null; }
layer = this.layers[layerName];
// create new layer, if necessary
if( !layer ){
// check for display layer, which is required
dlayer = this.display.layers[layerName];
if( !dlayer ){
return null;
}
// make a new image display layer
this.layers[layerName] = {};
// create new layer for this image
layer = this.layers[layerName];
// assume we show this layer
layer.show = true;
// no shapes yet
layer.nshape = 0;
// backlink to display layer
layer.dlayer = dlayer;
// convenient link back to opts
layer.opts = layer.dlayer.opts;
// convenient link back to canvas
layer.canvas = layer.dlayer.canvas;
// recalculate offset -- why is this necessary??
layer.canvas.calcOffset();
}
// return layer
return layer;
};
// use zindex to make specified shape layer the active layer
// call using image context
JS9.Fabric.activeShapeLayer = function(s){
let i, j, a, key, layer, tlayer, ozindex, tzindex, rtn;
if( !s ){
// no args: return layer with highest zindex
for( key of Object.keys(this.layers) ){
tlayer = this.layers[key];
if( tlayer.dlayer.dtype === "main" ){
if( (tzindex === undefined) || (tlayer.zindex > tzindex) ){
tzindex = tlayer.zindex;
a = key;
}
}
}
// return highest zindex layer
rtn = a;
} else if( $.isArray(s) ){
// non-public internal call: array of layers was specified
// set zindex for layers in decreasing order
for(i=0, j=this.zlayer-1; i {
let tkey, ctags, color;
tagcolors = tagcolors || {};
// look through the color keys for exact match
for( tkey of Object.keys(tagcolors) ){
ctags = tkey.split("\_");
// see if all elements match
if( $(tags).not(ctags).length === 0 &&
$(ctags).not(tags).length === 0 ){
color = tagcolors[tkey];
break;
}
}
// look through color keys for subset match
if( !color ){
for( tkey of Object.keys(tagcolors) ){
ctags = tkey.split("\_");
if( $(tags).not(ctags).length === 0 ){
color = tagcolors[tkey];
break;
}
}
}
// look through color keys for superset match
if( !color ){
for( tkey of Object.keys(tagcolors) ){
ctags = tkey.split("\_");
if( $(ctags).not(tags).length === 0 ){
color = tagcolors[tkey];
break;
}
}
}
// final attempt: use existing object's color or a default color
color = color || (obj && obj.get("stroke")) ||
tagcolors.defcolor || JS9.globalOpts.defcolor || "#000000";
return color;
};
// opts is optional
opts = opts || {};
// remove means nothing else matters
if( opts.remove ){
return {remove: opts.remove};
}
// remove dangerous options (e.g., passed in JS9.GetRegions() object)
parent = opts.parent || (obj && obj.params && obj.params.parent);
delete opts.parent;
if( !opts.restoreid ){
delete opts.id;
}
delete opts.restoreid;
// initialize tags
nparams.tags = [];
// pre-processing special keys
if( opts.tags ){
if( typeof opts.tags === "string" ){
tags = opts.tags.toLowerCase().split(",");
// modes: source, background, include, exclude, etc
for(i=0; i= 3 ){
opts.wcssys = arr[2];
}
}
// ra and dec are in degrees, using the current wcs
if( this.validWCS() && JS9.notNull(opts.ra) && JS9.notNull(opts.dec) ){
// make sure we have the right wcssys
if( opts.wcssys ){
// from passed-in opts
owcssys = this.getWCSSys();
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
this.setWCSSys(opts.wcssys, false);
} else if( opts.\_wcssys ){
// local override from parseRegions
owcssys = this.getWCSSys();
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
this.setWCSSys(opts.\_wcssys, false);
// no longer needed or wanted
delete opts.\_wcssys;
}
// convert wcs supplied as strings
if( typeof opts.ra === "string" ){
opts.ra = JS9.saostrtod(opts.ra);
if( JS9.isHMS(this.params.wcssys) ){
opts.ra \*= 15.0;
}
}
if( typeof opts.dec === "string" ){
opts.dec = JS9.saostrtod(opts.dec);
}
// convert to image coords
arr = JS9.wcs2pix(this.raw.wcs, opts.ra, opts.dec).trim().split(/ +/);
// restore original wcssys
if( owcssys ){
this.setWCSSys(owcssys, false);
JS9.globalOpts.xeqPlugins = txeq;
}
// convert to display coords
pos = this.imageToDisplayPos({x: parseFloat(arr[0]),
y: parseFloat(arr[1])});
nopts.left = pos.x;
nopts.top = pos.y;
}
// look for primitives
if( (opts.left !== undefined) ){
nopts.left = opts.left;
}
if( (opts.top !== undefined) ){
nopts.top = opts.top;
}
// last gasp to get left and top (unless explicitly told not to)
if( nopts.left === undefined && opts.noLeftTop !== true ){
if( obj && (obj.left !== undefined) ){
nopts.left = obj.left;
} else {
nopts.left = this.display.canvasjq.attr("width") / 2 - 1;
}
}
if( nopts.top === undefined && opts.noLeftTop !== true ){
if( obj && (obj.top !== undefined) ){
nopts.top = obj.top;
} else {
// why is this fudge needed?
nopts.top = this.display.canvasjq.attr("height") / 2 - 1 + YFUDGE;
}
}
// relative movement requires opts left/top or an existing object
if( opts.deltax ){
nopts.left += opts.deltax;
}
if( opts.deltay ){
nopts.top -= opts.deltay;
}
// set scaling based on zoom factor
if( this.display.layers[layerName].dtype === "main" &&
!opts.preservedcoords ){
zoom = this.rgb.sect.zoom;
} else {
zoom = 1;
}
// look for reset directives (empty strings)
if( opts.strokeDashes === "" || opts.strokeDashArray === "" ){
opts.strokeDashArray = [];
}
if( opts.strokeWidth === "" ){
opts.strokeWidth = JS9.Fabric.opts.strokeWidth;
}
// shape-specific processing
switch(opts.shape){
case "annulus":
nparams.radii = [];
if( opts.radii !== undefined ){
if( typeof opts.radii === "string" ){
nparams.radii = opts.radii.replace(/ /g, "").split(",");
for(i=0, j=0; i {
switch(item){
case "top":
case "left":
case "width":
case "height":
case "radii":
case "radius":
case "rx":
case "ry":
case "angle":
case "panzoom":
case "iradius":
case "oradius":
case "nannuli":
case "aradius1":
case "aradius2":
case "configURL":
case "sortOverlapping":
case "tagcolors":
case "pts":
case "ptshape":
case "ptsize":
case "linepoints":
case "polypoints":
case "responseType":
case "display":
case "tags":
case "r1":
case "r2":
case "x":
case "y":
case "dx":
case "dy":
case "px":
case "py":
case "ra":
case "dec":
case "shape":
case "parent":
case "rtn":
case "\_wcssys":
case "file":
case "savefile":
case "savewhich":
case "saveformat":
case "saveselection":
case "savewcs":
case "sortids":
case "send":
case "listonchange":
case "multitext":
return false;
case "text":
if( opts.shape === "text" ){
return false;
}
return true;
case "editing":
return opts.editing;
default:
return true;
}
});
};
// if shape is not text but text is specified in the opts,
// make a text shape as a child of this shape
// call using image context
JS9.Fabric.\_handleChildText = function(layerName, s, opts){
let i, t, dpos, npos, topts, yoff, child;
const textht = 12;
// region layer only, for now
if( layerName !== "regions" ){
return;
}
// opts are optional
opts = opts || {};
if( (s.params.shape !== "text") && opts.text &&
(!s.params.children || !s.params.children.length) ){
yoff = (s.height \* s.scaleX / 2) - textht;
// default position for text (might be overridden by textOpts)
if( Math.abs(s.angle) < 0.000001 ){
dpos = {x: s.left, y: s.top - yoff};
} else {
dpos = JS9.rotatePoint({x: s.left, y: s.top - yoff},
s.angle, {x: s.left, y: s.top});
}
npos = this.displayToImagePos(dpos);
topts = {x: npos.x, y: npos.y, angle: -s.angle,
color: s.stroke, text: opts.text, tags: s.params.tags,
parent: "TBD", rtn: "object"};
if( opts.textOpts ){
topts = $.extend(true, {}, topts, opts.textOpts);
}
// create the child shape
t = this.addShapes(layerName, "text", topts);
// parent object keeps track of relationship between parent and child
t.params.parent = {id: s.params.id,
obj: s,
dleft: s.left - t.left,
dtop: s.top - t.top,
lastscalex: s.scaleX,
lastscaley: s.scaleY,
lastangle: s.angle,
textheight: textht};
// updateShape was skipped in addShapes because parent was TBD
// we can now updateShape with parent info ...
this.\_updateShape(layerName, t, null, "child", t.params);
// since strokeWidth changes with zoom, we need to save the opts
// and restore it on export
if( opts.strokeWidth !== undefined ){
t.params.parent.strokeWidth = opts.strokeWidth;
}
// text might be moved off default position already
if( (npos.x !== topts.x) || (npos.y !== topts.y) ){
t.params.parent.moved = true;
}
// flag if text RA and Dec were passed in textOpts
if( opts.textOpts &&
opts.textOpts.ra !== undefined &&
opts.textOpts.dec !== undefined ){
t.params.hasTextOpts = true;
}
// parent has another child
s.params.children.push({id: t.params.id, obj: t});
// update the parent
this.\_updateShape(layerName, s, null, "addchild", s.params);
} else if( s.params.children && s.params.children.length > 0 &&
(JS9.notNull(opts.text) ||
JS9.notNull(opts.textOpts) ||
JS9.notNull(opts.color)) ){
// process parameters passed to existing text children
for(i=0; i 0 ){
this.changeShapes(layerName, child.params.id, topts);
}
}
}
};
// add shapes to a layer
// call using image context
JS9.Fabric.addShapes = function(layerName, shape, myopts){
let i, sobj, sarr, carr, ns, s, bopts, opts, layer, canvas, dlayer;
let zoom, ttop, tleft, tangle, w2, h2, key;
let params = {};
let rarr = [], parr = [];
const objs = [];
const grp = {};
// is this core service disabled?
if( $.inArray("regions", this.params.disable) >= 0 &&
layerName === "regions" ){
return;
}
// optional myopts can be an object or a string
myopts = myopts || {};
// opts can be an object or json
if( typeof myopts === "string" ){
try{ myopts = JSON.parse(myopts); }
catch(e){ JS9.error(`can't parse shape opts: ${myopts}`, e); }
}
// delay adding the region, if this image is not the one being displayed
if( this.display.image !== this ){
this.delayedShapes = this.delayedShapes || [];
this.delayedShapes.push({layer: layerName, shape: shape,
mode: "add", opts: myopts});
return;
}
// remove old regions, if necessary (ie we are reloading the file)
if( myopts.file && JS9.globalOpts.reloadRefreshReg ){
try{ this.removeShapes("regions", myopts.file); }
catch(e){ /\* empty \*/ }
}
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer || !layer.show ){ return; }
canvas = layer.canvas;
// figure out the first arg
if( typeof shape === "string" ){
// look for a region string
s = this.parseRegions(shape, myopts);
if( typeof s === "string" ){
// nope, normal shape string
sarr = [{shape: s}];
} else {
// parsed array of shape objects from regions string
sarr = s;
}
} else if( $.isArray(shape) ){
sarr = shape;
} else if( typeof shape === "object" ){
sarr = [shape];
} else {
return;
}
// once a shape has been added, we can set the zindex to process events
if( JS9.isNull(layer.zindex) || Number.isNaN(layer.zindex) ){
if( this.display.layers[layerName].dtype === "main" ){
switch(layerName){
case JS9.Crosshair.LAYERNAME:
case JS9.Grid.LAYERNAME:
// these should never cover any other interactive layer
layer.zindex = 1;
break;
default:
// otherwise this layer goes to the top
layer.zindex = this.zlayer++;
break;
}
} else {
// layer is not in main display
layer.zindex = JS9.SHAPEZINDEX;
}
dlayer = this.display.layers[layerName];
dlayer.divjq.css("z-index", layer.zindex);
// we can now call the shape layer create plugin callbacks
this.xeqPlugins("shape", "onshapelayercreate", layerName);
}
// baseline opts
bopts = $.extend(true, {}, JS9.Fabric.opts, layer.opts, myopts);
// process each shape object
for(ns=0; ns= 0 ){
opts.centeredScaling = false;
}
// create the shape
switch(sobj.shape){
case "annulus":
// save shape
params.shape = "annulus";
// save group position
ttop = opts.top;
tleft = opts.left;
// individual radii in the group are at 0,0
opts.top = 0;
opts.left = 0;
rarr = [];
if( params.radii ){
for(i=0; i {
let groupid;
// ordinary shapes
if( o.params ){
// but not child shapes
if( !o.params.parent ){
JS9.tmp.regSelect.all.push(o.params.id);
}
} else if( o.type === "group" ){
// groups
groupid = this.lookupGroup(o);
if( groupid ){
JS9.tmp.regSelect.all.push(groupid);
}
}
});
try{
regSelect.parse(selection);
}
catch(e){
JS9.error(`parsing selection filter: ${selection}`, e);
}
if( opts.saveselection && selection ){
switch(selection.trim()){
case "all":
case "saved":
case "selected":
break;
default:
this.layers[layerName].selection = selection;
break;
}
}
selection = JS9.tmp.regSelect.ids;
delete JS9.tmp.regSelect;
return selection;
};
// select one of more shapes by id or tag and execute a callback
// call using image context
JS9.Fabric.\_selectShapes = function(layerName, selection, opts, cb){
let i, j, objects, olen, aobjects, alen, groups;
let id, ginfo, canvas, ocolor, tag, obj;
const used = [];
const xcb = (obj, ginfo) => {
if( $.inArray(obj, used) < 0 ){
cb.call(this, obj, ginfo);
used.push(obj);
}
}
const getshapes = (objects) => {
let got, obj, olen;
// sanity check
if( !objects ){ return []; }
// get objects, including objects inside groups, which themselves
// can be within groups ... (hence the do/while loop)
olen = objects.length;
do{
got = 0;
while( olen-- ){
obj = objects[olen];
// replace group with objects inside the group
if( obj.type === "group" && !obj.params ){
objects.splice(olen, 1, ...obj.getObjects());
got++;
}
}
olen = objects.length;
} while( got );
return objects;
};
const getgroups = (canvas, objects) => {
let i, j, obj, grp, olen, mlen, ao;
let mygroups = [];
let groups = [];
olen = objects.length;
// look for all possible groups
for(i=0; i {
let i, tobj;
for(i=0; i {
// but no text children
if( o.params && !o.params.parent ){
xcb(o, ginfo);
}
});
} else {
// dangerous case: pass the group object
// you'd better know what you are doing!
xcb(obj, ginfo);
}
} else {
// for some types of selections, we do need to
// look inside the group
obj.forEachObject((o) => {
if( o.params && id === o.params.file ){
xcb(o, ginfo);
}
});
}
// that's the entirety of processing we do on a group
continue;
}
// make sure its a valid region
if( !obj.params ){ continue; }
// convenience variables
ocolor = obj.stroke.toLowerCase();
// no text children unless explicity specified
if( obj.params.parent && id !== "child" && id !== "All" ){
continue;
}
// children should always have a parent
if( id === "child" && !obj.params.parent ){
continue;
}
// set group info
ginfo.group = groups[olen];
// try to match this id in various ways
if( id.toLowerCase() === "all" ){
// all
xcb(obj, ginfo);
} else if( (id.toLowerCase() === ocolor) ||
(JS9.colorToHex(id).toLowerCase() === ocolor) ){
// color
xcb(obj, ginfo);
} else if( id === obj.params.shape ){
// shape
xcb(obj, ginfo);
} else if( id === obj.params.file ){
// origin filename
xcb(obj, ginfo);
} else if( typeof obj.params.data === "object" &&
id === obj.params.data.syncid ){
// sync id (see sync plugin)
xcb(obj, ginfo);
} else if( id === "child" && obj.params.parent ){
// all
xcb(obj, ginfo);
} else if( id === "dcoords" && obj.params.preservedcoords ){
// all
xcb(obj, ginfo);
} else if( id === "nodcoords" && !obj.params.preservedcoords ){
// all
xcb(obj, ginfo);
} else if( id === "parent" &&
obj.params.children &&
obj.params.children.length ){
// all
xcb(obj, ginfo);
} else if( $.inArray(id, JS9.wcssyss) >= 0 &&
obj.params.wcsconfig &&
obj.params.wcsconfig.wcssys === id ){
// original wcs
xcb(obj, ginfo);
} else if( obj.params.tags ){
// tags
for(i=0; i remove selection for this layer
if( shape === "reset" ){
// remove last selection
delete layer.selection;
// change selection to none?
if( opts.activateselection !== false ){
// deselect current active object, if necessary
if( canvas.getActiveObject() ){
canvas.discardActiveObject();
}
// re-display so we don't see the old group
canvas.renderAll();
}
return this;
}
// collect the specified shapes
this.\_selectShapes(layerName, shape, opts, (obj) => {
// only select once, don't select shapes in groups
if( $.inArray(obj, arr) < 0 && (!obj.params || !obj.params.groupid) ){
arr.push(obj);
}
});
if( arr.length ){
// deselect current active object, if necessary
if( canvas.getActiveObject() ){
canvas.discardActiveObject();
}
if( arr.length === 1 ){
// select 1 shape
selection = arr[0];
} else {
// create a group selection of 2+ shapes
selection = new fabric.ActiveSelection(arr, {
canvas: canvas
});
}
// make this the active selection
canvas.setActiveObject(selection);
// display the new group
canvas.renderAll();
}
return this;
};
// remove shapes from a group selection
// call using image context
// eslint-disable-next-line no-unused-vars
JS9.Fabric.unselectShapes = function(layerName, shape, opts){
let layer, unshape, selection;
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer || !this.layers[layerName] ){ return; }
// default is to unselect everything
if( !shape || shape === "all" || shape === "selected" ){
return this.selectShapes(layerName, "reset");
}
selection = this.layers[layerName].selection || "selected";
unshape = `${selection} && !(${shape})`;
return this.selectShapes(layerName, unshape, opts);
};
// update public object in shapes
// call using image context
JS9.Fabric.updateShapes = function(layerName, shape, mode, opts){
// process the specified shapes
this.\_selectShapes(layerName, shape, null, (obj, ginfo) => {
this.\_updateShape(layerName, obj, ginfo, mode, opts);
});
return this;
};
// update multi-selection dialog boxes
// call using image context
JS9.Fabric.\_updateMultiDialogs = function(setmode){
// update multiselect dialog box for this image, if necessary
$("form[class\*='regionsConfigForm']").each((index, element) => {
const multi = $(element).data("multi");
const winid = $(element).data("winid");
const im = $(element).data("im");
if( multi && winid && im === this ){
if( im.tmp.updateMulti !== false ){
im.initRegionsForm(null, {winid, multi, setmode});
}
}
});
};
// primitive to update one shape
// call using image context
JS9.Fabric.\_updateShape = function(layerName, obj, ginfo, mode, opts){
let i, s, scalex, scaley, px, py, tval1, tval2, angstr;
let bin, zoom, tstr, dpos, gpos, ipos, npos, objs, olen, radius, oangle;
let opos, dist, txeq, owcssys, imforce, agroup, apos;
const pub = {};
const layer = this.layers[layerName];
const moderexp = /^(child||export|unexport|move|mouseout)$/;
const tr = (x) => { return x.toFixed(2); };
const tr4 = (x) => { return x.toFixed(4); };
const updatewcs = (wcs, layer, pub, regstr, angstr, opts, obj) => {
let i, s, v0, v1;
// get ra and dec of central position
s = JS9.pix2wcs(wcs, pub.x, pub.y).trim().split(/\s+/);
obj.rastr = s[0];
obj.decstr = s[1];
obj.wcssys = s[2];
v0 = JS9.strtoscaled(s[0]);
if( JS9.isHMS(s[2], v0.dtype) ){
v0.dval \*= 15.0;
}
v1 = JS9.strtoscaled(s[1]);
obj.ra = v0.dval;
obj.dec = v1.dval;
// generate WCS strings iff updateWCS is true
if( (opts.updateWCS !== false) &&
(opts.updateWCS || layer.opts.updateWCS) ){
obj.wcsstr = JS9.reg2wcs(wcs, regstr, JS9.REGSIZE)
.replace(/;$/, "");
// add angle to line, if possible
if( pub.shape === "line" && angstr ){
obj.wcsstr = obj.wcsstr.replace(/} \*$/, angstr + "}");
}
// wcs size args
s = obj.wcsstr.replace(/.\*\(/,"").replace(/\).\*/,"").split(",");
for(i=0; i {
let xname;
const xeq = (onchange) => {
try{
this.params.xeqonchange = false;
JS9.xeqByName(onchange, window, this, pub);
}
catch(e){
JS9.log("error in onchange: %s [%s]\n%s",
this.id, e.message, JS9.strace(e));
}
finally{
this.params.xeqonchange = true;
}
};
if( !obj.params.parent && !mode.match(moderexp) ){
// when xeqonchange is set on a layer
if( this.params.xeqonchange && layer.show ){
if( layer.opts.onchange ){
xeq(layer.opts.onchange);
} else if( layerName === "regions" &&
JS9.Regions.opts.onchange ){
// if onchange was set after region layer was set up
xeq(JS9.Regions.opts.onchange);
}
}
// plugin callbacks: these have the form on[layer]change,
// e.g. onregionschange
xname = `on${layerName}change`;
this.xeqPlugins("shape", xname, pub);
}
};
// sanity check
if( !obj || !obj.params ){ return; }
// convenience variables
ginfo = ginfo || {};
opts = opts || {};
mode = mode || "update";
// set scaling based on zoom factor
if( this.display.layers[layerName].dtype === "main" &&
!obj.params.preservedcoords ){
zoom = this.rgb.sect.zoom;
} else {
zoom = 1;
}
// fill in the blanks
pub.mode = mode;
pub.id = obj.params.id;
pub.groupid = obj.params.groupid;
pub.shape = obj.params.shape;
pub.layer = layerName;
pub.color = obj.color || obj.stroke;
pub.tags = obj.params.tags;
pub.sticky = obj.params.sticky;
pub.preservedcoords = obj.params.preservedcoords;
if( obj.params.ignore ){
pub.ignore = true;
}
if( obj.params.parent ){
pub.parent = obj.params.parent.obj.params.id;
} else {
pub.parent = null;
}
if( obj.params.children && obj.params.children.length ){
// for now, just output the first one (cf. listRegions)
pub.child = obj.params.children[0].id;
} else {
pub.child = null;
}
dpos = obj.getCenterPoint();
gpos = {x: 0, y: 0};
if( ginfo.group ){
// in a group, the display pos is relative to group pos,
// so we need to add them together
gpos = ginfo.group.getCenterPoint();
dpos = {x: gpos.x + (dpos.x \* ginfo.group.scaleX),
y: gpos.y + (dpos.y \* ginfo.group.scaleY)};
// also need to rotate the position by the group angle
if( ginfo.group.angle ){
dpos = JS9.rotatePoint(dpos, ginfo.group.angle, gpos);
}
// is the group contained in an active selection??
if( ginfo.group.type !== "activeSelection" ){
agroup = layer.canvas.getActiveObject();
if( agroup && agroup.type === "activeSelection" ){
objs = agroup.getObjects();
olen = objs.length;
for(i=0; i= 360 ){
pub.angle -= 360;
}
// the parts of the obj.scale[XY] values related to size (not zoom, binning)
scalex = obj.scaleX / zoom;
scaley = obj.scaleY / zoom;
if( ginfo.group ){
scalex \*= ginfo.group.scaleX;
scaley \*= ginfo.group.scaleY;
}
switch(pub.shape){
case "annulus":
pub.shape = "annulus";
pub.radii = [];
if( pub.imsys !== "image" ){
pub.lcs.radii = [];
}
pub.imstr = `annulus(${tr(px)},${tr(py)},`;
tstr = `annulus ${pub.x} ${pub.y} `;
objs = obj.getObjects();
olen = objs.length;
for(i=0; i 0 ){
pub.imstr += ",";
tstr += " ";
}
// get current point
npos = this.displayToImagePos(
{x: gpos.x + obj.left + obj.points[i].x \* obj.scaleX,
y: gpos.y + obj.top + obj.points[i].y \* obj.scaleY}
);
// add rotation
npos = JS9.rotatePoint(npos, oangle, {x: pub.x, y: pub.y});
if( pub.imsys === "image" ){
pub.imstr += `${tr(npos.x)},${tr(npos.y)}`;
} else {
const {x, y} = this.imageToLogicalPos(npos);
pub.imstr += `${tr(x)},${tr(y)}`;
pub.lcs.pts.push({x, y});
}
tstr += `${npos.x} ${npos.y}`;
pub.pts.push(npos);
if( pub.shape === "line" ){
if( i === 0 ){
dist = 0;
} else {
opos = pub.pts[i-1];
dist += Math.sqrt(((npos.x - opos.x) \* (npos.x - opos.x)) +
((npos.y - opos.y) \* (npos.y - opos.y)));
}
}
}
if( pub.shape === "line" && JS9.notNull(dist) ){
pub.imstr += `) {"size":${tr(dist)},"units":"pixels"`;
// if only two points, add angle between them
if( pub.pts.length === 2 ){
tval1 = Math.atan2(pub.pts[1].y - pub.pts[0].y,
pub.pts[1].x - pub.pts[0].x) \* 180 / Math.PI;
while( tval1 < 0 ){ tval1 += 360; }
angstr = `,"posang":${tr4(tval1)},"posunits":"degrees"`;
pub.imstr += angstr;
}
pub.imstr += "}";
} else {
pub.imstr += ")";
}
// points already have the angle incorporated into them
pub.angle = 0;
break;
case "text":
pub.imstr = `text(${tr(px)},${tr(py)},"${obj.text}",${tr4(pub.angle)})`;
tstr = `text ${pub.x} ${pub.y} "${obj.text}"` + ` ${pub.angle \* Math.PI / 180.0}`;
pub.text = obj.text;
break;
default:
break;
}
// wcs processing
if( this.validWCS() ){
updatewcs(this.raw.wcs, layer, pub, tstr, angstr, opts, pub);
if( mode !== "export" &&
obj.params.wcsconfig && obj.params.wcsconfig.wcssys ){
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
owcssys = this.getWCSSys();
if( JS9.notWCS(obj.params.wcsconfig.wcssys) ){
pub.wcsconfig = $.extend(true, {}, obj.params.wcsconfig);
} else {
this.setWCSSys(obj.params.wcsconfig.wcssys, false);
updatewcs(this.raw.wcs, layer, pub, tstr, angstr, opts,
obj.params.wcsconfig);
pub.wcsconfig = $.extend(true, {}, obj.params.wcsconfig);
}
this.setWCSSys(owcssys, false);
JS9.globalOpts.xeqPlugins = txeq;
}
}
// generic "data" property, optionally supplied when the shape is created
pub.data = obj.params.data;
// save the pub object
obj.set("pub", pub);
// update dialog box, if necessary
if( obj.params.winid ){
if( $(obj.params.winid).is(":visible") ){
this.initRegionsForm(obj);
} else {
obj.params.winid = null;
}
}
// stop here if no callbacks were requested
if( opts.nocb ){
return pub;
}
// callbacks for regions
xplugins();
// post processing:
// copy to clipboard, if necessary
if( layerName === "regions" && JS9.globalOpts.regToClipboard ){
switch(mode){
case "update":
i = pub.parent || pub.id;
break;
default:
i = null;
break;
}
if( JS9.notNull(i) ){
// ignore any problems
try{ s = this.listRegions(i, {mode: 1, includedcoords: true}); }
catch(e){ s = null; }
if( s ){ JS9.clipboard = s; }
}
}
// update multi dialog boxes, if necessary
if( layerName === "regions" && mode === "wcs" ){
this.\_updateMultiDialogs(true);
}
// and return it
return pub;
};
// lookup a group, either by name or by object
// groupObj = this.lookupGroup(groupID)
// groupID = this.lookupGroup(groupObj)
JS9.Fabric.lookupGroup = function(group, layerName){
let i, j, objs, obj, sobjs, sobj, layer, canvas;
layerName = layerName||"regions";
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer ){ return null; }
canvas = this.layers[layerName].canvas;
if( typeof group === "string" ){
objs = canvas.getObjects();
for(i=0; i 0 ){
this.display.displayMessage("regions", grpstr);
}
return grpstr.replace(/;\s\*/g, "\n").replace(/\n\n$/, "\n");
};
// create a quasi-permanent group from selected shapes
// call using image context
// eslint-disable-next-line no-unused-vars
JS9.Fabric.groupShapes = function(layerName, shape, opts){
let i, s, layer, dlayer, canvas, obj, id, skip, dupid;
const objs = [];
const pubs = [];
const getid = (opts) => {
let i = 1;
let id = opts.groupid || `group\_${i}`;
while( this.lookupGroup(id) ){
i = i+1;
id = id.replace(/\_[0-9][0-9]\*$/, "") + `\_${i}`;
}
return id;
};
// get layer
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer ){ return 0; }
// dlayer
dlayer = layer.dlayer;
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse groupShapes opts: ${opts}`, e); }
}
// convenience variable
canvas = layer.canvas;
// id for this group
id = getid(opts);
// collect the specified shapes
this.\_selectShapes(layerName, shape, opts, (obj) => {
if( $.inArray(obj, objs) < 0 ){
// so far, so goodx
skip = false;
// look for conflicts
if( obj.params.groupid ){
switch(JS9.globalOpts.regGroupConflict){
case "skip":
// save id of the conflicting group
dupid = obj.params.groupid;
// flag to skip adding to new group
skip = true;
break;
case "error":
default:
s = sprintf("%s can only be a member of one group [%s,%s]",
layerName === "regions" ? "regions" : "shapes",
obj.params.id, obj.params.groupid);
JS9.error(s);
break;
}
}
// save for group, if necessary
if( !skip ){
obj.params.groupid = id;
if( $.inArray("groupid", obj.params.exports) < 0 ){
obj.params.exports.push("groupid");
}
// save object
objs.push(obj);
pubs.push(obj.pub);
// save children (i.e., text)
// (but not pub, since don't call ongroupcreate on text)
if( obj.params && obj.params.children.length ){
for(i=0; i= 0 ){
shape.params.exports.splice(idx, 1);
}
}
}
}
}
// remove id from groups
if( this.groups[layerName] ){
idx = $.inArray(groupid, this.groups[layerName]);
if( idx >= 0 ){
this.groups[layerName].splice(idx, 1);
}
}
return this;
};
// remove the active shape
// eslint-disable-next-line no-unused-vars
JS9.Fabric.removeShapes = function(layerName, shape, opts){
let i, layer, canvas, ao;
let undoao = false;
const lopts = {mode: 1, includedcoords: true, sortids: false};
const arr = [];
const grp = [];
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer ){ return; }
canvas = layer.canvas;
// opts is optional
opts = opts || {};
// list active objects
if( canvas.getActiveObject() ){
ao = canvas.getActiveObjects();
}
// save regions for unremove?
if( layerName === "regions" && JS9.globalOpts.unremoveReg ){
this.regstack.push(this.listRegions(shape, lopts, layerName));
if( this.regstack.length > JS9.globalOpts.unremoveReg ){
this.regstack = this.regstack.slice(0,JS9.globalOpts.unremoveReg);
}
}
// process the specified shapes
this.\_selectShapes(layerName, shape, opts, (obj, ginfo) => {
let i, child, parent;
if( (obj.params.removable !== false || opts.overrideRemovable) &&
(!obj.params.sticky || opts.sticky !== false) ){
if( layer.dlayer.dtype === "main" ){
this.\_updateShape(layerName, obj, ginfo, "remove");
}
// clear any dialog box
if( obj.params.winid ){
obj.params.winid.close();
obj.params.winid = null;
}
// unlink parent
if( obj.params.parent ){
parent = obj.params.parent.obj;
for(i=parent.params.children.length-1; i>=0; i--){
if( obj === parent.params.children[i].obj ){
parent.params.children.splice(i,1);
break;
}
}
}
// mark children for removal
for(i=0; i= 0 ){
undoao = true;
}
// mark for removal
arr.push(obj);
}
});
// discard active object if we are deleting one of its shapes
// do before delete, as per: http://fabricjs.com/v2-breaking-changes-2
if( undoao ){
canvas.discardActiveObject();
}
// remove groups
for(i=0; i {
// public part of the shape
myshape = obj.pub || {};
// might need shape object itself
if( opts.includeObj ){
myshape.obj = obj;
}
shapes.push(myshape);
});
// sort shapes by id to maintain original order of creation
if( opts.sortids !== false ){
shapes.sort((a, b) => { return (a.id||0) - (b.id||0); });
}
return shapes;
};
// change the specified shape(s)
// call using image context
JS9.Fabric.changeShapes = function(layerName, shape, opts){
let i, s, sobj, bopts, layer, canvas, ao, aos, rlen, maxr, zoom, exports;
let topts, xopts;
const orad = [], cpts = [];
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer || !opts ){ return; }
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse shape opts: ${opts}`, e); }
}
// delay changing the region, if this image is not the one being displayed
if( this.display.image !== this ){
this.delayedShapes = this.delayedShapes || [];
this.delayedShapes.push({layer: layerName, shape: shape,
mode: "change", opts: opts});
return;
}
canvas = layer.canvas;
// active object
ao = canvas.getActiveObject();
if( ao && ao.type === "activeSelection" ){
// save and temporarily remove a selected group
// fabric.js doesn't deal with this very well
aos = canvas.getActiveObjects()
canvas.discardActiveObject();
canvas.renderAll();
ao = null;
}
// this selection is usually saved
if( JS9.isNull(opts.saveselection) ){ opts.saveselection = true; }
// process the specified shapes
this.\_selectShapes(layerName, shape, opts, (obj, ginfo) => {
// set scaling based on zoom factor
if( this.display.layers[layerName].dtype === "main" &&
!obj.params.preservedcoords ){
zoom = this.rgb.sect.zoom;
} else {
zoom = 1;
}
// combine the objects parameters with the new options
// clearing some of the old ones first to avoid conflicts
if( opts.radii ){
obj.params.radii = [];
}
if( opts.tags ){
obj.params.tags = [];
}
if( opts.locked !== undefined ){
delete obj.params.changeable;
}
// combine new opts with old opts
bopts = $.extend(true, {}, obj.params, opts);
// parse options and generate new obj and params
sobj = this.\_parseShapeOptions(layerName, bopts, obj);
// remove means remove specified shapes or all shapes
if( sobj.remove ){
if( sobj.remove === true || sobj.remove === "true" ){
sobj.remove = "all";
}
if( sobj.remove !== false && sobj.remove !== "false" ){
this.removeShapes(layerName, sobj.remove || "all");
return;
}
}
// get new option names to export when saving regions
exports = this.\_exportShapeOptions(opts).filter( (item) => {
return !{}.hasOwnProperty.call(obj.params.exports, item);
});
sobj.params.exports = obj.params.exports.concat(exports);
// if stroke (color) is defined, we probably need to convert it to hex
if( sobj.opts.stroke ){
sobj.opts.color = sobj.opts.stroke;
sobj.opts.stroke = JS9.colorToHex(sobj.opts.stroke);
}
// shape-specific pre-processing
switch(obj.params.shape){
case "text":
// can't use stroke, use fill instead
if( sobj.opts.stroke ){
sobj.opts.fill = sobj.opts.stroke;
}
sobj.opts.strokeWidth = 0;
break;
case "line":
case "polygon":
// if we are changing the points, reset the fabric angle
// otherwise, it's applied to points which know nothing about it
if( sobj.opts.points && sobj.opts.points.length ){
obj.angle = 0;
}
break;
}
// change the shape
obj.set(sobj.opts);
// reestablish params object
obj.params = $.extend(false, {}, obj.params, sobj.params);
// if strokeWidth is specified, we change params.sw1,
// which will be used by the rescaleBorder routine below
if( sobj.opts.strokeWidth ){
obj.params.sw1 = sobj.opts.strokeWidth;
}
// shape-specific post-processing
// mainly: change of size => remove size-based scaling factor
switch(obj.params.shape){
case "annulus":
if( opts.radii && opts.radii.length ){
// remove existing annuli
// can't remove inside the forEachObject loop
obj.forEachObject( (tobj) => { orad.push(tobj); });
// so do it outside the loop
rlen = orad.length;
for(i=0; i {
xopts = $.extend(true, {}, topts);
if( cpts[idx] ){ xopts.points = cpts[idx]; }
tobj.set(xopts);
});
break;
case "ellipse":
if( opts.r1 ){
obj.rx = obj.params.r1;
obj.scaleX = zoom;
// this sets the width of the control box
// why is it not done automatically???
obj.width = obj.rx \* 2;
}
if( opts.r2 ){
obj.ry = obj.params.r2;
obj.scaleY = zoom;
// this sets the height of the control box
// why is it not done automatically???
obj.height = obj.ry \* 2;
}
break;
case "line":
case "polygon":
if( (opts.points && opts.points.length) ||
(opts.pts && opts.pts.length) ){
obj.scaleX = zoom;
obj.scaleY = zoom;
}
if( ao === obj ){
JS9.Fabric.removePolygonAnchors(layer.dlayer, obj);
JS9.Fabric.addPolygonAnchors(layer.dlayer, obj);
}
// reset the center point
JS9.resetPolygonCenter(obj);
break;
case "text":
if( opts.text ){
obj.params.text = opts.text;
}
break;
}
// make sure border width is correct
obj.rescaleBorder();
// non-changeable shapes go to back
if( obj.params.changeable === false ){
canvas.sendToBack(obj);
}
// send region to front or back of set of overlapping regions
switch(sobj.opts.send){
case "front":
canvas.bringToFront(obj);
if( ao === obj ){
canvas.discardActiveObject();
}
break;
case "back":
canvas.sendToBack(obj);
if( ao === obj ){
canvas.discardActiveObject();
}
break;
default:
break;
}
// update children
JS9.Fabric.updateChildren(layer.dlayer, obj, "moving");
JS9.Fabric.updateChildren(layer.dlayer, obj, "scaling");
JS9.Fabric.updateChildren(layer.dlayer, obj, "rotating");
// update child's parent deltas
JS9.Fabric.updateChildren(layer.dlayer, obj, "deltas");
// and reset coords
obj.setCoords();
// might need to make a text shape as a child of this shape
this.\_handleChildText(layerName, obj, opts);
// update the shape info and make callbacks
this.\_updateShape(layerName, obj, ginfo, "update");
// callback if necessary
if( opts.onchangeshapes && obj.pub ){
try{ JS9.xeqByName(opts.onchangeshapes, this, this, obj.pub); }
catch(e){ JS9.error("in onchangeshapes callback", e, false); }
}
});
// reconstitute the selected group, if necessary
if( aos ){
this.selectShapes(layerName, aos);
}
// redraw (unless explicitly specified otherwise)
if( (opts.redraw === undefined) || opts.redraw ){
canvas.renderAll();
}
return this;
};
// update shape layer after a change in panning, zooming, binning
// uses ListRegions to recreate regions, very stable but slow for many shapes
// call using image context
JS9.Fabric.refreshShapes = function(layerName){
let regstr, owcssys, txeq, opts;
// sanity check
if( !layerName ){ return; }
// convenience variables
opts = {
mode:1,
sticky:false,
ignoreignore:true,
saveediting:true,
savewcsconfig:true,
sortids: false,
saveid:true
};
// temporarily turn off plugin execution to avoid firing regions callbacks
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
// temporarily change wcs system to be independent of image coords
// (in case we copied regions from one image to another)
owcssys = this.getWCSSys();
if( owcssys === "image" ){
// get a wcs sys independent of image coords
if( this.validWCS() ){
this.setWCSSys("native", false);
} else {
this.setWCSSys("physical", false);
}
}
// special optimization when panning an image with the mouse,
// to deal with slow panning a large number of regions
if( this.tmp.panzoomRefresh && this.tmp.panzoomRefresh[layerName] ){
if( !this.tmp.panzoomRefresh[layerName].regstr ){
// save current regions
regstr = this.listRegions("all", opts, layerName);
this.tmp.panzoomRefresh[layerName] = {regstr:regstr, refresh:false};
// remove current regions (including unremovable ones)
this.removeShapes(layerName, "all", {overrideRemovable: true,
sticky: false});
} else {
if( this.tmp.panzoomRefresh[layerName].refresh ){
regstr = this.tmp.panzoomRefresh[layerName].regstr;
// add back regions in current configuration
this.addShapes(layerName, regstr, {restoreid: true});
}
}
} else {
// get current regions (i.e., before update to current configuration)
regstr = this.listRegions("all", opts, layerName);
if( regstr ){
// save selection (remove shapes destroys it)
this.saveSelection(layerName);
// remove current regions (including unremovable ones)
this.removeShapes(layerName, "all", {overrideRemovable: true,
sticky: false});
// add back regions in current configuration
this.addShapes(layerName, regstr, {restoreid: true,
sortids: false});
// restore selection
this.restoreSelection(layerName);
}
}
// restore wcs system, if necessary
if( owcssys === "image" ){
this.setWCSSys(owcssys, false);
// update shapes to use the original coord system
this.updateShapes(layerName, "all", "refresh");
}
// restore plugin execution
JS9.globalOpts.xeqPlugins = txeq;
return this;
};
// copy one or more shapes to another image
// call using image context
JS9.Fabric.copyShapes = function(layerName, to, which){
let i, im, s, opts, layer;
const ims = [];
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer ){ return; }
if( typeof to === "object" ){
ims.push(to);
} else if( to === "all" ){
for(i=0; i (Math.PI \* 2) ){
angle -= Math.PI \* 2;
}
pos.x = Math.cos(angle) \* local.x - Math.sin(angle) \* local.y;
pos.y = Math.sin(angle) \* local.x + Math.cos(angle) \* local.y;
//Get the list of points from the polygon
points = obj.points;
//The algorithm is simple, iterate through the list of points
//and select a pair which forms a side of the polygon.
//For this side, pick a main point. Find the direction vector
//with respect to this main point, and find the position vector
//from this main point to the drag position.
//Dot product of position vector and direction vector give us
//the projection of the point on the current side.
//A simple bounds checking to ensure the projection is on
//the side, then a distance calculation.
//If the distance found is less than the current minimum difference
//update diff, newX and newY.
for(i=0; i p2.x ? p1.x : p2.x);
maxY = (p1.y > p2.y ? p1.y : p2.y);
//Select p2 as the main point.
//Find the direction vector and normalize it.
dir = {x: p1.x - p2.x, y: p1.y - p2.y};
m = Math.sqrt(dir.x\*dir.x + dir.y\*dir.y);
if( m !== 0 ){
dir.x = dir.x/m;
dir.y = dir.y/m;
}
//Find the position vector
pVec = {x: pos.x - p2.x, y: pos.y - p2.y};
//Dot product
dot = pVec.x \* dir.x + pVec.y \* dir.y;
//Find the projection along the current side
p = {x: p2.x + dir.x \* dot, y: p2.y + dir.y \* dot};
//Bounds checking to ensure projection remains
//between the point pair.
if( p.x < minX ){
p.x = minX;
} else if( p.x > maxX ){
p.x = maxX;
}
if( p.y < minY ){
p.y = minY;
} else if( p.y > maxY ){
p.y = maxY;
}
//Distance calculation.
d = (p.x-pos.x) \* (p.x-pos.x) + (p.y-pos.y) \* (p.y-pos.y);
//Minimum comparison.
if( d < diff ){
diff = d;
newpt.x = p.x;
newpt.y = p.y;
if( i === points.length ){
newpt.i = 0;
} else {
newpt.i = i;
}
}
}
// get canvas
layer = this.getShapeLayer(layerName);
// remove anchors
JS9.Fabric.removePolygonAnchors(layer.dlayer, obj);
// add the new point into the points array
points.splice(newpt.i+1, 0, {x: newpt.x, y: newpt.y});
// making this the active object will recreate the anchors
switch(obj.type){
case "polyline":
case "polygon":
JS9.Fabric.addPolygonAnchors(layer.dlayer, obj);
layer.dlayer.canvas.renderAll();
break;
}
// set currently selected shape
if( obj.polyparams ){
layer.dlayer.params.sel = obj.polyparams.polygon;
} else if( obj.params ){
layer.dlayer.params.sel = obj;
}
};
// remove the specified point
// call using image context
JS9.Fabric.\_removePolygonPoint = function(layerName, obj){
let layer, polygon, points, pt;
// sanity check
if( !obj || !obj.polyparams ){ return; }
// get info on this point
polygon = obj.polyparams.polygon;
points = polygon.points;
// maintain minimum number of points
if( (polygon.type === "polygon") && (points.length <= 3) ){
return;
} else if( (polygon.type === "polyline") && (points.length <= 2) ){
return;
}
pt = obj.polyparams.point;
// delete to stop an executing movePoint callback
delete obj.polyparams.point;
// get layer
layer = this.getShapeLayer(layerName);
// remove anchors
JS9.Fabric.removePolygonAnchors(layer.dlayer, polygon);
// add the new point into the points array
points.splice(pt, 1);
// reset the center point
JS9.resetPolygonCenter(polygon);
// making this the active object will recreate the anchors
layer.canvas.setActiveObject(polygon);
};
// add anchors to a polygon
// don't need to call using image context
JS9.Fabric.addPolygonAnchors = function(dlayer, obj){
let i, a;
let pos = {};
const canvas = dlayer.canvas;
const movePoint = (obj) => {
let anchor, poly, pt, points, im;
// anchor changed location to obj.transform.target in v4.5.1
if( obj.target && obj.target.polyparams ){
anchor = obj.target;
} else if( obj.transform &&
obj.transform.target && obj.transform.target.polyparams ){
anchor = obj.transform.target;
}
// sanity check
if( !anchor ){ return; }
// this is the polygon associated with this anchor
poly = anchor.polyparams.polygon;
// if the polygon is not changeable, just return
if( poly.params.changeable === false ){
return;
}
// these are the points in the polygon
points = poly.get("points");
// this is the point id associated with this anchor
pt = anchor.polyparams.point;
// if pt is not valid, just return
if( pt === undefined || points[pt] === undefined ){
return;
}
// new point for this anchor relative to center
// NB: anchor was rotated onto the vertex
if( poly.angle ){
pos = JS9.rotatePoint({x: anchor.left, y: anchor.top}, -poly.angle,
{x: poly.left, y: poly.top});
} else {
pos.x = anchor.left;
pos.y = anchor.top;
}
// move the polygon point to the anchor (in unscaled coords)
points[pt].x = (pos.x - poly.left) / poly.scaleX;
points[pt].y = (pos.y - poly.top) / poly.scaleY;
// reset the center point
JS9.resetPolygonCenter(poly);
// update the shape info
if( dlayer.display.image ){
im = dlayer.display.image;
im.\_updateShape(poly.params.layerName, poly, null, "update");
if( im.params.listonchange || poly.params.listonchange ){
im.listRegions(poly, {mode: 2});
}
}
// redraw
canvas.renderAll();
};
const moveAnchors = (obj) => {
let ii;
let tpos = {};
// change anchor positions
for(ii=0; ii {
moveAnchors(obj);
});
obj.on("rotating", () => {
moveAnchors(obj);
});
obj.on("scaling", () => {
moveAnchors(obj);
});
obj.setCoords();
};
// remove anchors from a polygon
// don't need to call using image context
JS9.Fabric.removePolygonAnchors = function(dlayer, shape){
let i;
const canvas = dlayer.canvas;
if( shape && shape.params && shape.params.anchors ){
// need to be able to remove anchors when locking a polygon
// if( shape.params.changeable === false ){
// return;
// }
// remove all anchors
for(i=0; i { return b.radius - a.radius; });
// add circle for edit
for(i=0; i {
if( o.params && o.params.shape === "circle" ){
circles.push(o);
}
});
// will hold new radii
opts.radii = [];
// ids of circles
ids = [...this.editAnnulus.ids];
// for each id, find the circle object and get its radius
// (what we're looking for is likely at the end of the stack)
for(j=circles.length-1; j>=0; j--){
cid = circles[j].params.id;
for(i=ids.length-1; i>=0; i--){
id = ids[i];
if( cid === id ){
// if pub.radius is epsilon, change back to 0
if( circles[j].pub.radius === epsilon ){
circles[j].pub.radius = 0;
}
opts.radii.push(circles[j].pub.radius);
ids.splice(i, 1);
break;
}
}
if( !ids.length ){
break;
}
}
opts.radii.sort((a, b) => { return a - b; });
}
// change the annulus
this.changeShapes(layerName, this.editAnnulus.annulus, opts);
// remove the edit circles
this.removeShapes(layerName, this.editAnnulus.ids);
// remove current edit parameters
delete this.editAnnulus;
};
// update child regions
// don't need to call using image context
JS9.Fabric.updateChildren = function(dlayer, shape, type){
let i, o, p, child, nangle, npos, pangle, objects, olen, got;
let tdleft, tdtop;
let x = {};
// region layer only, for now
if( dlayer.layerName !== "regions" ){
return;
}
// re-init objects within for parents and children
if( type === "objects" ){
// get list of top-level objects, replacing groups with their objects
objects = dlayer.canvas.getObjects().reverse();
olen = objects.length;
do{
got = 0;
while( olen-- ){
o = objects[olen];
// replace group with objects inside the group
if( o.type === "group" && !o.params ){
objects.splice(olen, 1, ...o.getObjects());
got++;
}
}
olen = objects.length;
} while( got );
// first get a list of parents and children
objects.forEach( (o) => {
if( o.params ){
if( o.params.parent || o.params.children.length ){
x[o.params.id] = o;
}
}
});
// then re-assign obj pointers to parents and children
objects.forEach( (o) => {
if( o.params ){
if( o.params.parent ){
o.params.parent.obj = x[o.params.parent.id];
}
for(i=0; i= 360 ){
pangle -= 360;
}
nangle = pangle - p.lastangle;
npos = JS9.rotatePoint({x: child.left,y: child.top},
nangle,
{x: shape.left, y: shape.top});
child.left = npos.x;
child.top = npos.y;
p.dleft = shape.left - child.left;
p.dtop = shape.top - child.top;
child.angle = child.angle + nangle;
while( child.angle < 0 ){
child.angle += 360;
}
while( child.angle >= 360 ){
child.angle -= 360;
}
p.lastangle = pangle;
break;
case "scaling":
p.dleft = p.dleft \* (shape.scaleX / p.lastscalex);
p.dtop = (p.dtop - p.textheight) \*
(shape.scaleY / p.lastscaley) + p.textheight;
p.lastscalex = shape.scaleX;
p.lastscaley = shape.scaleY;
p.moved = true;
child.left = shape.left - p.dleft;
child.top = shape.top - p.dtop;
break;
}
child.setCoords();
if( dlayer.display.image ){
dlayer.display.image.updateShapes(dlayer.layerName, child,
"updatechild");
}
}
};
// reset center of a polygon
// don't need to call using image context
JS9.resetPolygonCenter = function(poly){
let i, ndx, ndy, dobj, calcDim, dx, dy;
let tpos = {};
// deltas to center
dobj = poly.\_calcDimensions();
dx = (dobj.left + (dobj.width / 2)) \* poly.scaleX;
dy = (dobj.top + (dobj.height / 2)) \* poly.scaleY;
// new center
if( poly.angle ){
tpos = JS9.rotatePoint(
{x: poly.left + dx, y: poly.top + dy},
poly.angle,
{x: poly.left, y: poly.top}
);
} else {
tpos.x = poly.left + dx;
tpos.y = poly.top + dy;
}
// move points relative to new center
// required by polygon changes starting in fabric 1.5.x
ndx = dx / poly.scaleX;
ndy = dy / poly.scaleY;
for(i=0; i

`;
// add layers
for( key of Object.keys(this.layers) ){
layer = this.layers[key];
// output (showing) layers attached to the main display
if( layer.dlayer.dtype === "main" && layer.show ){
html += `${divstr}${layer.dlayer.canvas.toSVG()}

`;
}
}
// add colorbar, if necessary
if( (opts.colorbar === undefined) || opts.colorbar ){
pinst = this.display.pluginInstances.JS9Colorbar;
if( pinst && pinst.isActive() ){
// separate from main display
yoff += 2;
// colorbar canvas
dataURL = pinst.colorbarjq[0].toDataURL("image/png");
yoff += this.display.height;
divstr = sprintf(divtmpl, xoff, yoff);
html += `${divstr}![](${dataURL})

`;
if( pinst.textjq && pinst.textjq[0] ){
// colorbar text/tickmarks canvas
dataURL = pinst.textjq[0].toDataURL("image/png");
yoff += pinst.colorbarjq.height() + 1;
divstr = sprintf(divtmpl, xoff, yoff);
// need to rescale the text ... argh!!!
html += `${divstr}![](${dataURL})

`;
}
}
}
// finish up
html += "

";
// this is needed since v9 ... why???
if( window.electron ){
winurl = "data:text/html," + html;
}
// make a new window containing a blank URL
win = window.open(winurl, this.id, winopts);
if( !win ){
JS9.error("could not create print window (check your pop-up blockers)");
return;
}
// open DOM for writing
if( win.document ){
// open it (not strictly necessary but ...)
win.document.open();
// overwrite the doc with our html
win.document.write(html);
// must close!
win.document.close();
} else {
JS9.error("no method available for drawing image into print window");
}
};
// incorporate these graphics routines into JS9
JS9.Fabric.initGraphics = function(){
// display methods
JS9.Display.prototype.newShapeLayer = JS9.Fabric.newShapeLayer;
// image shape methods
JS9.Image.prototype.\_selectShapes = JS9.Fabric.\_selectShapes;
JS9.Image.prototype.\_updateShape = JS9.Fabric.\_updateShape;
JS9.Image.prototype.\_parseShapes = JS9.Fabric.\_parseShapes;
JS9.Image.prototype.\_parseShapeOptions = JS9.Fabric.\_parseShapeOptions;
JS9.Image.prototype.\_exportShapeOptions = JS9.Fabric.\_exportShapeOptions;
JS9.Image.prototype.\_handleChildText = JS9.Fabric.\_handleChildText;
JS9.Image.prototype.\_addPolygonPoint = JS9.Fabric.\_addPolygonPoint;
JS9.Image.prototype.\_removePolygonPoint = JS9.Fabric.\_removePolygonPoint;
JS9.Image.prototype.\_ungroupAnnulus = JS9.Fabric.\_ungroupAnnulus;
JS9.Image.prototype.\_regroupAnnulus = JS9.Fabric.\_regroupAnnulus;
JS9.Image.prototype.\_updateMultiDialogs = JS9.Fabric.\_updateMultiDialogs;
JS9.Image.prototype.addShapes = JS9.Fabric.addShapes;
JS9.Image.prototype.updateShapes = JS9.Fabric.updateShapes;
JS9.Image.prototype.getShapes = JS9.Fabric.getShapes;
JS9.Image.prototype.changeShapes = JS9.Fabric.changeShapes;
JS9.Image.prototype.removeShapes = JS9.Fabric.removeShapes;
JS9.Image.prototype.refreshShapes = JS9.Fabric.refreshShapes;
JS9.Image.prototype.copyShapes = JS9.Fabric.copyShapes;
JS9.Image.prototype.selectShapes = JS9.Fabric.selectShapes;
JS9.Image.prototype.unselectShapes = JS9.Fabric.unselectShapes;
JS9.Image.prototype.groupShapes = JS9.Fabric.groupShapes;
JS9.Image.prototype.ungroupShapes = JS9.Fabric.ungroupShapes;
JS9.Image.prototype.listGroups = JS9.Fabric.listGroups;
JS9.Image.prototype.lookupGroup = JS9.Fabric.lookupGroup;
JS9.Image.prototype.saveSelection = JS9.Fabric.saveSelection;
JS9.Image.prototype.restoreSelection = JS9.Fabric.restoreSelection;
// shape layer methods
JS9.Image.prototype.getShapeLayer = JS9.Fabric.getShapeLayer;
JS9.Image.prototype.showShapeLayer = JS9.Fabric.showShapeLayer;
JS9.Image.prototype.activeShapeLayer = JS9.Fabric.activeShapeLayer;
JS9.Image.prototype.displayShapeLayers = JS9.Fabric.displayShapeLayers;
JS9.Image.prototype.toggleShapeLayers = JS9.Fabric.toggleShapeLayers;
// print method which know about shapes
JS9.Image.prototype.print = JS9.Fabric.print;
};
// initialize graphics to use Fabric
JS9.Fabric.initGraphics();
/\*
\* mouse/touch module (May 19, 2016)
\*/
// create our namespace, and specify some meta-information and params
JS9.MouseTouch = {};
JS9.MouseTouch.CLASS = "JS9"; // class of plugin
JS9.MouseTouch.NAME = "MouseTouch"; // name of this plugin
JS9.MouseTouch.WIDTH = 512; // width of light window
JS9.MouseTouch.HEIGHT = 220; // height of light window
JS9.MouseTouch.BASE = JS9.MouseTouch.CLASS + JS9.MouseTouch.NAME;
JS9.MouseTouch.mouseText = [];
JS9.MouseTouch.mouseText[0] = "Move mouse, no buttons pressed:";
JS9.MouseTouch.mouseText[1] = "Move mouse, primary button pressed:";
JS9.MouseTouch.mouseText[2] = "Move mouse, secondary button pressed:";
JS9.MouseTouch.touchText = [];
JS9.MouseTouch.touchText[0] = "Touch move, with one finger:";
JS9.MouseTouch.touchText[1] = "Touch move, with two fingers:";
JS9.MouseTouch.touchText[2] = "Touch move, with three fingers:";
JS9.MouseTouch.textHTML="

%s

";
JS9.MouseTouch.actionHTML="

**%s**

";
// get an id based on the action
JS9.MouseTouch.actionid = function(cname, aname){
return (`${cname}\_${aname}`).replace(/[^A-Za-z0-9\_]/g, "\_");
};
// add to the text descriptions
JS9.MouseTouch.addText = function(container, text){
let s, divjq;
// create the html for this action
s = sprintf(JS9.MouseTouch.textHTML, text);
// add text html to the text container
divjq = $("

")
.addClass(`${JS9.MouseTouch.BASE}Text`)
.html(s)
.appendTo(container);
return divjq;
};
// add to the sortable action list
JS9.MouseTouch.addAction = function(container, cname, aname){
let s, id, divjq;
id = JS9.MouseTouch.actionid(cname, aname);
// create the html for this action
s = sprintf(JS9.MouseTouch.actionHTML, aname);
// add action html to the action container
divjq = $("

")
.addClass(`${JS9.MouseTouch.BASE}Action`)
.attr("id", id)
.html(s)
.appendTo(container);
return divjq;
};
// display value/position
// eslint-disable-next-line no-unused-vars
JS9.MouseTouch.isPinch = function(im, evt){
let i, display, dist, pinc, pdec;
const npinch = JS9.globalOpts.pinchWait;
const pthresh = JS9.globalOpts.pinchThresh;
// sanity check
if( !im ){ return -1; }
display = im.display;
if( !JS9.globalOpts.mousetouchZoom || (im.pos.touches.length !== 2) ){
return -1;
}
switch(display.ispinch ){
case -1:
case 1:
return display.ispinch;
}
dist = Math.sqrt(((im.pos.touches[0].x - im.pos.touches[1].x) \*
(im.pos.touches[0].x - im.pos.touches[1].x)) +
((im.pos.touches[0].y - im.pos.touches[1].y) \*
(im.pos.touches[0].y - im.pos.touches[1].y)));
if( !display.dist0 ){
display.dist0 = dist;
}
display.deltas.push(Math.floor(dist - display.dist0));
if( display.deltas.length >= npinch ){
for(i=1, pinc=0, pdec=0; i display.deltas[i-1] ){
pinc++;
} else if( display.deltas[i] < display.deltas[i-1] ){
pdec++;
}
}
if( (pinc >= pthresh) || (pdec >= pthresh) ){
display.ispinch = 1;
} else {
display.ispinch = -1;
}
display.lastzoom = 0;
return display.ispinch;
}
// not sure yet
return 0;
};
// ---------------------------------------------------------------------
//
// MouseTouch.Actions: callbacks when on mouse or touch movement
//
// for mouse: no click, primary click, secondary click
// for touch: 1, 2, or 3 fingers down
//
// the mouseActions and touchActions arrays in JS9.globalOpts determine
// the initial mapping of mouse/touch configuration to callback, e.g.:
//
// JS9.globalOpts.mouseActions = ["display value/position", "change contrast/bias", "pan the image"];
//
// You can add your own to the Actions object, with titles in mouseText ...
// They are transferred to the display object.
//
// ---------------------------------------------------------------------
JS9.MouseTouch.Actions = {};
// display value/position
// eslint-disable-next-line no-unused-vars
JS9.MouseTouch.Actions["display value/position"] = function(im, ipos, evt){
// special key: do nothing
if( JS9.specialKey(evt) ){
return;
}
// display pixel and wcs values
if( JS9.globalOpts.internalValPos && im && ipos ){
if( (ipos.x > 0) && (ipos.y > 0) &&
(ipos.x <= im.raw.width) && (ipos.y <= im.raw.height) ){
im.valpos = im.updateValpos(ipos, true);
}
}
};
// change contrast/bias
JS9.MouseTouch.Actions["change contrast/bias"] = function(im, ipos, evt){
let x, y, pos, display;
// skip contrast/bias change?
if( !JS9.globalOpts.internalContrastBias || !im || !ipos ){
return;
}
// skip if colormap is static
if( im.cmapObj.type === "static" ){
return;
}
// convenience variables
display = im.display;
// make sure we moved the mouse a bit
if( im.pos0 && im.pos ){
if( ((Math.abs(im.pos0.x-im.pos.x) < JS9.NOMOVE) &&
(Math.abs(im.pos0.y-im.pos.y) < JS9.NOMOVE)) ){
return;
}
}
// inside a region or with special key: no contrast/bias
if( im.clickInRegion || JS9.specialKey(evt) ){
return;
}
// if we have an RGB file or image overlay, no contrast/bias
if( im.useOffScreenCanvas() ){
return;
}
// get canvas position
pos = JS9.eventToDisplayPos(evt, im.posOffset);
// contrast/bias change
x = Math.floor(pos.x + 0.5);
y = Math.floor(pos.y + 0.5);
// values only from within display window?
if( JS9.globalOpts.containContrastBias ){
if( (x < 0) || (y < 0) ||
(x >= display.canvas.width) || (y >= display.canvas.height) ){
return;
}
}
im.params.bias = x / display.canvas.width;
im.params.contrast = y / display.canvas.height \* 10.0;
// work-around for FF bug, not fixed as of 8/8/2012
// https://bugzilla.mozilla.org/show\_bug.cgi?id=732621
if( JS9.bugs.firefox\_linux ){
window.setTimeout(() => {
im.displayImage("scaled", {blendMode: false});
}, 0);
} else {
im.displayImage("scaled", {blendMode: false});
}
// hack: delete filterRGBImage from stash to avoid restore during reproject
im.xeqStashDiscard("filterRGBImage");
// extended plugins
if( JS9.globalOpts.extendedPlugins ){
im.xeqPlugins("image", "onchangecontrastbias");
}
};
// stop action for contrast/bias: redisplay image
// eslint-disable-next-line no-unused-vars
JS9.MouseTouch.Actions["change contrast/bias"].stop = function(im, ipos, evt){
// if blendMode is on, we have to redisplay
if( im.display.blendMode ){
im.displayImage("rgb");
}
};
// zoom the image
JS9.MouseTouch.Actions["wheel zoom"] = function(im, evt){
let ozoom, nzoom, maxzoom, key;
let floor = JS9.globalOpts.panzoomRefreshLimit;
let got = 0;
const delta = evt.originalEvent.deltaY \* Math.sign(JS9.DIRZOOM);
// sanity check
if( !im ){ return; }
// is scroll to zoom turned on?
if( !JS9.globalOpts.mousetouchZoom ){
return;
}
// prevent pileup
im.tmp.wheelzooms = im.tmp.wheelzooms || 0;
if( im.tmp.wheelzooms++ % JS9.MODZOOM !== 0 ){
return;
}
// current zoom
ozoom = im.getZoom();
// scroll by the delta
if( delta < 0 ){
nzoom = Math.min(JS9.MAXZOOM, ozoom + JS9.ADDZOOM);
} else {
nzoom = Math.max(JS9.MINZOOM, ozoom - JS9.ADDZOOM);
}
// stop zooming once full image is in the screen?
if( JS9.globalOpts.mousetouchLimit ){
maxzoom = Math.min(im.display.width/im.raw.width,
im.display.height/im.raw.height);
if( maxzoom > nzoom && ozoom > nzoom ){
return;
}
}
// a little rounding makes the zoom nicer
nzoom = Math.round((nzoom + 0.00001) \* 100) / 100;
// see if any layers have many regions, thus requiring optimization
for( key of Object.keys(im.layers) ){
if( im.layers[key].show && im.layers[key].opts.panzoom ){
if( im.layers[key].canvas.size() > floor ){
im.tmp.panzoomRefresh = im.tmp.panzoomRefresh || {};
im.tmp.panzoomRefresh[key] = {};
got++;
}
}
}
// timeout to refresh layers
if( im.tmp.panzoomTimeout ){
clearTimeout(im.tmp.panzoomTimeout);
delete im.tmp.panzoomTimeout;
}
if( got || im.tmp.panzoomRefresh ){
im.tmp.panzoomTimeout = setTimeout(() => {
im.refreshLayers(im.tmp.panzoomRefresh);
delete im.tmp.panzoomRefresh;
}, JS9.TIMEOUT);
}
// zoom the image
im.setZoom(nzoom);
};
// pan the image
// eslint-disable-next-line no-unused-vars
JS9.MouseTouch.Actions["pan the image"] = function(im, ipos, evt){
let dx, dy, temp, sect, pos, key;
let thresh = JS9.globalOpts.panMouseThreshold;
let floor = JS9.globalOpts.panzoomRefreshLimit;
// sanity check
if( !im ){ return; }
sect = im.rgb.sect;
// how much would we pan by?
dx = ((im.pos0.x - im.pos.x) / sect.zoom);
dy = ((im.pos0.y - im.pos.y) / sect.zoom);
// pan the image (but avoid a redisplay, if we haven't moved much)
if( Math.abs(dx) >= thresh || Math.abs(dy) >= thresh ){
// flips will change the pan direction
if( im.params.flip === "x" ){
dx = -dx;
} else if( im.params.flip === "y" ){
dy = -dy;
} else if( im.params.flip === "xy" ){
dx = -dx;
dy = -dy;
}
// rotations will change the pan direction
if( im.params.rot90 === 90 ){
temp = dx;
dx = -dy;
dy = temp;
} else if( im.params.rot90 === 180 ){
dx = -dx;
dy = -dy;
} else if( im.params.rot90 === -90 ){
temp = dx;
dx = dy;
dy = -temp;
}
pos = {x: sect.xcen + dx, y: sect.ycen - dy};
// rotations will change the pan position
if( im.params.rotate ){
pos = JS9.rotatePoint(pos,
-im.params.rotate,
{x: sect.xcen, y: sect.ycen});
}
// see if any layers have many regions, thus requiring optimization
for( key of Object.keys(im.layers) ){
if( im.layers[key].show && im.layers[key].opts.panzoom ){
if( im.layers[key].canvas.size() > floor ){
im.tmp.panzoomRefresh = im.tmp.panzoomRefresh || {};
im.tmp.panzoomRefresh[key] = {};
}
}
}
im.setPan(pos);
// reset initial position
im.pos0 = im.pos;
}
};
// pinch zoom
// eslint-disable-next-line no-unused-vars
JS9.MouseTouch.Actions.pinch = function(im, ipos, evt){
let display, dist, nzoom;
// sanity check
if( !im ){ return; }
// is scroll to zoom turned on?
display = im.display;
// get current distance
dist = Math.sqrt(((im.pos.touches[0].x - im.pos.touches[1].x) \*
(im.pos.touches[0].x - im.pos.touches[1].x)) +
((im.pos.touches[0].y - im.pos.touches[1].y) \*
(im.pos.touches[0].y - im.pos.touches[1].y)));
nzoom = display.zoom0 \* dist / display.dist0;
// a little rounding makes the zoom nicer
nzoom = Math.max(JS9.MINZOOM, Math.min(JS9.MAXZOOM, Math.round((nzoom + 0.00001) \* 100) / 100));
// zoom the image
if( nzoom !== display.lastzoom ){
im.setZoom(nzoom);
}
display.lastzoom = nzoom;
};
// start of mouse/touch action processing
JS9.MouseTouch.Actions.start = function(im, ipos, evt){
let display, action;
if( im ){
display = im.display;
display.ispinch = 0;
display.dist0 = 0;
display.zoom0 = im.rgb.sect.zoom;
display.deltas = [];
}
action = JS9.MouseTouch.getAction(im, evt);
// call the start mouse/touch action, if necessary
if( JS9.MouseTouch.Actions[action] &&
JS9.MouseTouch.Actions[action].start ){
JS9.MouseTouch.Actions[action].start(im, im.ipos, evt);
}
};
// end of mouse/touch action processing
JS9.MouseTouch.Actions.stop = function(im, ipos, evt){
const action = JS9.MouseTouch.getAction(im, evt);
// call the stop mouse/touch action, if necessary
if( JS9.MouseTouch.Actions[action] &&
JS9.MouseTouch.Actions[action].stop ){
JS9.MouseTouch.Actions[action].stop(im, im.ipos, evt);
}
return;
};
// get action associated with the current clickState
JS9.MouseTouch.getAction = function(im, evt){
let action, display;
// sanity check
if( !im ){ return action; }
display = im.display;
switch(im.clickState){
// mouse move actions
case 0:
action = display.mouseActions[0];
break;
case 1:
action = display.mouseActions[1];
break;
case 2:
action = display.mouseActions[2];
break;
// touch event actions
case -1:
action = display.touchActions[0];
break;
case -2:
switch( JS9.MouseTouch.isPinch(im, evt) ){
case -1:
action = display.touchActions[1];
break;
case 0:
// do nothing, no idea if its a pinch yet
break;
case 1:
action = "pinch";
break;
}
break;
case -3:
action = display.touchActions[2];
break;
default:
break;
}
return action;
};
// execute the mouse/touch action routine
JS9.MouseTouch.action = function(im, evt, action){
action = action || JS9.MouseTouch.getAction(im, evt);
// call the mouse/touch action
if( action && JS9.MouseTouch.Actions[action] ){
JS9.MouseTouch.Actions[action](im, im.ipos, evt);
}
};
// change zoom mode for this display
JS9.MouseTouch.mousetouchzoom = function(id, target){
const display = JS9.lookupDisplay(id);
const mode = target.checked;
// change global blink mode
if( display ){
JS9.globalOpts.mousetouchZoom = mode;
}
};
// constructor: add HTML elements to the plugin
JS9.MouseTouch.init = function(){
let i, s;
// on entry, these elements have already been defined:
// this.div: the DOM element representing the div for this plugin
// this.divjq: the jquery object representing the div for this plugin
// this.id: the id of the div (or the plugin name as a default)
// this.display: the display object associated with this plugin
// this.dispMode: display mode (for internal use)
//
// create container to hold action container and header
// clean main container
this.divjq.html("");
// allow scrolling on the plugin
this.divjq.addClass("JS9PluginScrolling");
// main container
this.mousetouchContainer = $("

")
.addClass(`${JS9.MouseTouch.BASE}Container`)
.attr("id", `${this.id}MouseTouchContainer`)
.appendTo(this.divjq);
s = sprintf("

**Drag an action to reconfigure JS9 mouse/touch events:**

", `${JS9.MouseTouch.BASE}Header`);
this.mousetouchHeadContainer = $("")
.addClass(`${JS9.MouseTouch.BASE}Container`)
.attr("id", `${this.id}MouseTouchHeadContainer`)
.html(s)
.appendTo(this.mousetouchContainer);
this.mousetouchTextContainer = $("")
.addClass(`${JS9.MouseTouch.BASE}Container`)
.attr("id", `${this.id}MouseTouchTextContainer`)
.appendTo(this.mousetouchContainer);
this.mousetouchActionContainer = $("")
.addClass(`${JS9.MouseTouch.BASE}Container`)
.attr("id", `${this.id}MouseTouchActionContainer`)
.appendTo(this.mousetouchContainer);
if( JS9.TOUCHSUPPORTED ){
// container to hold text descriptions
this.mousetouchTouchTextContainer = $("

")
.addClass(`${JS9.MouseTouch.BASE}TextContainer`)
.attr("id", `${this.id}TouchTextContainer`)
.html("")
.appendTo(this.mousetouchTextContainer);
for(i=0; i")
.addClass(`${JS9.MouseTouch.BASE}ActionContainer`)
.attr("id", `${this.id}TouchContainer`)
.html("")
.appendTo(this.mousetouchActionContainer);
// add touch actions, if necessary
for(i=0; i {
this.oidx = ui.item.index();
},
stop: (event, ui) => {
const nidx = ui.item.index();
const oarr = this.display.touchActions.splice(this.oidx, 1)[0];
// JS9 action list reflects the sort
this.display.touchActions.splice(nidx, 0, oarr);
delete this.oidx;
}
});
}
if( !/iPad|iPhone|iPod/.test(navigator.platform) ){
// container to hold text descriptions
this.mousetouchMouseTextContainer = $("

")
.addClass(`${JS9.MouseTouch.BASE}TextContainer`)
.attr("id", `${this.id}MouseTextContainer`)
.appendTo(this.mousetouchTextContainer);
for(i=0; i< 3; i++){
JS9.MouseTouch.addText.call(this,
this.mousetouchMouseTextContainer,
JS9.MouseTouch.mouseText[i]);
}
for(i=3; i")
.addClass(`${JS9.MouseTouch.BASE}ActionContainer`)
.attr("id", `${this.id}MouseContainer`)
.html("")
.appendTo(this.mousetouchActionContainer);
// add mouse actions, if necessary
for(i=0; i {
this.oidx = ui.item.index();
},
stop: (event, ui) => {
const nidx = ui.item.index();
const oarr = this.display.mouseActions.splice(this.oidx, 1)[0];
// JS9 action list reflects the sort
this.display.mouseActions.splice(nidx, 0, oarr);
delete this.oidx;
}
});
}
// add the footer, containing buttons
s = sprintf("

Use mouse wheel or pinch to zoom:

", `${JS9.MouseTouch.BASE}Footer`, this.display.id);
this.mousetouchFootContainer = $("")
.addClass(`${JS9.MouseTouch.BASE}Container`)
.attr("id", `${this.id}MouseTouchFootContainer`)
.html(s)
.appendTo(this.mousetouchContainer);
// set initial value of scroll
if( JS9.globalOpts.mousetouchZoom ){
this.mousetouchContainer.find("input").attr("checked", true);
}
};
// ---------------------------------------------------------------------
// Regions object defines high level calls for Regions plugin
// ---------------------------------------------------------------------
JS9.Regions = {};
JS9.Regions.CLASS = "JS9";
JS9.Regions.NAME = "Regions";
// defaults for new regions
JS9.Regions.opts = {
// update WCS strings
updateWCS: true,
// pan and zoom enabled
panzoom: true,
tags: "source,include",
strokeWidth: 2,
ptStrokeWidth: 1,
// annuli: inner and outer radius, number of annuli
iradius: 15,
oradius: 30,
nannuli: 1,
// box
width: 60,
height: 60,
// circle
radius: 30,
// ellipse:
// use r1, r2 to avoid confusion with rad1, rad2 for rounding in boxes!
r1: 30,
r2: 20,
// point
ptshape: "box",
ptsize: 2,
// line
linepoints: [{x: -30, y: 30}, {x:30, y:-30}],
// polygon in display coords
// points: [{x: -30, y: 30}, {x:30, y:30}, {x:30, y:-30}, {x:-30, y: -30}],
polypoints: [{x: -30, y: 30}, {x:30, y:30}, {x:0, y:-30}],
// text
// fontFamily: "Helvetica, sans-serif",
fontFamily: "Helvetica",
fontSize: 14,
fontStyle: "normal",
fontWeight: 300,
textAlign: "left",
// angles (box, ellipse)
angle: 0,
// anchor radii
aradius1: 4,
aradius2: 8,
// region configuration url
configURL: "./params/regionsconfig.html",
// region save url
saveURL: "./params/regionssave.html",
// should overlapping shapes be sorted (smallest on top)?
sortOverlapping: true,
// title for region config dialog box
title: "Edit region",
// no centered scaling for these regions
noCenteredScaling: ["box", "line"],
// colors for tags
// these should be ordered from more specific to less specific
tagcolors: {
include\_source: "#00FF00",
exclude\_source: "#FF0000",
include\_background: "#FFD700",
exclude\_background: "#FF8C00",
source: "#00FF00",
background: "#FFD700",
defcolor: "#00FF00"
},
// mouse double-click processing
onmousedblclick(im, xreg, evt, target){
let params = target.params;
if( (params && !params.winid && !params.ignore ) ||
(!params && target.type === "activeSelection") ||
(!params && target.type === "group") ){
if( JS9.globalOpts.editRegions ){
im.displayRegionsForm(target);
}
}
return;
},
// mouse down processing
onmousedown(im, xreg, evt, target){
let poly;
// nb: target might be a polygon anchor => no params
let params = target.params;
if( JS9.specialKey(evt) ){
if( params ){
im.\_regroupAnnulus(params.layerName, evt);
}
if( target.type === "polygon" || target.type === "polyline" ){
// add polygon point
im.\_addPolygonPoint(params.layerName, target, evt);
im.\_updateShape(params.layerName, target, null, "update");
} else if( target.polyparams && target.polyparams.polygon ){
// remove polygon point
poly = target.polyparams.polygon;
im.\_removePolygonPoint(poly.params.layerName, target);
im.\_updateShape(poly.params.layerName, poly, null, "update");
} else if( params && params.shape === "annulus" ){
im.\_ungroupAnnulus(params.layerName, target);
}
}
},
// mouse up processing
onmouseup(){
let i;
let objs = [];
// one active object
if( this.getActiveObject() ){
objs.push(this.getActiveObject());
}
objs.push(this.getActiveObjects());
// re-select polygon which was just processed
for(i=0; i {
let i, tim;
let objs = [];
if( dlayer.display.image ){
tim = dlayer.display.image;
// one active object
// group of active objects
objs.push(dlayer.canvas.getActiveObjects());
// process all active objects
for(i=0; i {
const multi = $(element).data("multi");
const winid = $(element).data("winid");
const im = $(element).data("im");
if( multi && winid && im === this ){
opts.winid = winid;
im.initRegionsForm(null, opts);
got++;
}
});
// change title to reflect multi-select, if necessary
title = title.replace(/regions?/, "selected regions");
// all done if we reinit'ed an existing window
if( got ){ return; }
}
// call this once window is loaded
$(JS9.lightOpts[JS9.LIGHTWIN].topid)
.arrive(".regionsConfigForm", {onceOnly: true}, () => {
opts.firsttime = true;
if( shape && shape.params ){
this.updateShapes("regions", shape, "wcsconfig");
}
this.initRegionsForm(shape, opts);
});
// bring up display window
opts.winid = this.displayAnalysis("regions", s, {title, winformat});
// save winid, if possible
if( shape && shape.params ){
shape.params.winid = opts.winid;
}
};
// initialize the region config form
// call using image context
JS9.Regions.initConfigForm = function(obj, opts){
let i, key, val, el, el2, wcssys, twcssys, mover, mout, p1, p2, cmode;
let s, s2, s3, s4, winid, wid, form, otitle, fav, arr, ao, grp, o, objs;
let multi = false;
const wcsinfo = this.raw.wcsinfo || {cdelt1: 1, cdelt2: 1};
const defobj = {
type: "multi",
pub: {shape: "multi", wcsconfig: {}},
params: {}
};
const fmt= (val) => {
if( val === undefined ){
return undefined;
}
if( (typeof val === "number") && (val % 1 !== 0) ){
val = Math.round((val + 0.00001) \* 10000) / 10000;
}
return(String(val));
};
const replaceNewline = (s) => {
const nl = String.fromCharCode(13, 10);
if( typeof s === "string" ){
return s.replace(/\\n/g, nl);
}
return s;
};
// which wcssys do we use? edit version, if available
if( obj && obj.pub ){
if( obj.pub.wcsconfig && obj.pub.wcsconfig.wcssys ){
wcssys = obj.pub.wcsconfig.wcssys;
} else {
wcssys = this.params.wcssys;
}
} else {
wcssys = this.params.wcssys;
// fake obj: makes the checks easier, avoid if( obj ... ) everywhere
obj = defobj;
}
cmode = obj.params.changeable === false;
// opts is optional
opts = opts || {};
// where to we get winid?
if( obj.params.winid ){
winid = obj.params.winid;
} else if( opts.winid ){
winid = opts.winid;
}
// window id is required
if( !winid ){
return;
}
// find the form, based on winid
wid = $(winid).attr("id");
// leave trailing space!
form = `#${wid} .regionsConfigForm `;
// valid form is required
if( !$(form).length ){
return;
}
// if the form is already a multi-select form, keep it that way
if( $(form).data("multi") ){
multi = true;
} else {
multi = opts.multi;
}
// remove the nodisplay class from shape's div
$(`${form}.${obj.pub.shape}`).each((index, element) => {
$(element).removeClass("nodisplay");
});
// fill in form values based on current values in the shape object
$(`${form}.val`).each((index, element) => {
val = "";
key = $(element).attr("name");
// key-specific pre-processing
switch(key){
case "x":
case "y":
if( obj.pub.lcs && obj.pub.lcs[key] !== undefined ){
val = fmt(obj.pub.lcs[key]);
} else if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
case "radii":
if( obj.pub.radii ){
if( JS9.notWCS(wcssys) ||
!obj.pub.wcsconfig ||
!obj.pub.wcsconfig.wcsstr ){
val = obj.pub.imstr
.replace(/^annulus\(/,"").replace(/\)$/,"")
.split(",").slice(2).join(",");
} else {
val = obj.pub.wcsconfig.wcsstr
.replace(/^annulus\(/,"").replace(/\)$/,"")
.split(",").slice(2).join(",");
}
}
break;
case "pts":
if( obj.pub.pts ){
obj.pub.pts.forEach( (p) => {
if( val ){
val += ", ";
}
val += `${p.x.toFixed(2)}, ${p.y.toFixed(2)}`;
});
} else if( obj.pub.imstr ){
// use the flat points list instead of the pts object array
val = obj.pub.imstr.replace(/^.\*\(/, "").replace(/\)$/, "");
}
break;
case "linelength":
if( obj.pub.pts && obj.pub.pts.length === 2 ){
p1 = obj.pub.pts[0];
p2 = obj.pub.pts[1];
val = fmt(Math.sqrt((p2.x - p1.x) \* (p2.x - p1.x) +
(p2.y - p1.y) \* (p2.y - p1.y)));
switch(wcssys){
case "image":
case "physical":
break;
default:
val \*= Math.abs(wcsinfo.cdelt1);
val \*= Math.abs(wcsinfo.cdelt2);
break;
}
val = fmt(val);
this.tmp.linelength = val;
}
break;
case "lineangle":
if( obj.pub.pts && obj.pub.pts.length === 2 ){
p1 = obj.pub.pts[0];
p2 = obj.pub.pts[1];
val = Math.atan2(p2.y - p1.y, p2.x - p1.x) \* 180 / Math.PI;
while( val < 0 ){ val += 360; }
val = fmt(val);
this.tmp.lineangle = val;
}
break;
case "fontFamily":
if( obj.getFontFamily ){
val = obj.getFontFamily();
}
break;
case "fontSize":
if( obj.getFontSize ){
val = obj.getFontSize();
}
break;
case "fontStyle":
if( obj.getFontStyle ){
val = obj.getFontStyle();
}
break;
case "fontWeight":
if( obj.getFontWeight ){
val = obj.getFontWeight();
}
break;
case "colorPicker":
if( obj.pub.color !== undefined ){
val = JS9.colorToHex(obj.pub.color);
} else {
val = $(form).data("colorpicker") || JS9.globalOpts.defcolor;
}
break;
case "color":
// multi: don't set color to avoid applying it to new selections
if( !multi ){
if( obj.pub.color !== undefined ){
val = fmt(obj.pub.color);
} else if( $(form).data("colorpicker") ){
val = $(form).data("colorpicker");
}
}
break;
case "strokeWidth":
if( obj.params.sw1 ){
val = obj.params.sw1;
} else {
val = $(form).data("strokewidth") || "";
}
break;
case "strokeDashes":
if( obj.strokeDashArray ){
val = obj.strokeDashArray.join(" ");
if( val.match(/NaN/) ){
val = "";
}
} else {
val = $(form).data("strokedashes") || "";
}
break;
case "regstr":
if( JS9.notWCS(wcssys) ||
!obj.pub.wcsconfig ||
!obj.pub.wcsconfig.wcsstr ){
val = `${obj.pub.imsys};${obj.pub.imstr}`;
} else {
val = `${obj.pub.wcsconfig.wcssys};${obj.pub.wcsconfig.wcsstr}`;
}
break;
case "xpos":
switch(wcssys){
case "image":
if( obj.pub.preservedcoords && obj.pub.dx !== undefined ){
val = sprintf("d%.1f", obj.pub.dx);
} else if( obj.pub.x !== undefined ){
val = sprintf("%.1f", obj.pub.x);
}
break;
case "physical":
if( obj.pub.lcs ){
val = sprintf("%.1f", obj.pub.lcs.x);
} else if( obj.pub.x !== undefined ){
val = sprintf("%.1f", obj.pub.x);
}
break;
default:
if( obj.pub.wcsconfig && JS9.notNull(obj.pub.wcsconfig.ra) ){
val = sprintf("%.6f", obj.pub.wcsconfig.ra);
} else if( obj.pub.x !== undefined ){
val = sprintf("%.1f", obj.pub.x);
}
break;
}
$(`${form}[name='${key}']`).prop("readonly", cmode);
break;
case "ypos":
switch(wcssys){
case "image":
if( obj.pub.preservedcoords && obj.pub.dy !== undefined ){
val = sprintf("d%.1f", obj.pub.dy);
} else if( obj.pub.y !== undefined ){
val = sprintf("%.1f", obj.pub.y);
}
break;
case "physical":
if( obj.pub.lcs ){
val = sprintf("%.1f", obj.pub.lcs.y);
} else if( obj.pub.y !== undefined ){
val = sprintf("%.1f", obj.pub.y);
}
break;
default:
if( obj.pub.wcsconfig && JS9.notNull(obj.pub.wcsconfig.dec) ){
val = sprintf("%.6f", obj.pub.wcsconfig.dec);
} else if( obj.pub.y !== undefined ){
val = sprintf("%.1f", obj.pub.y);
}
break;
}
$(`${form}[name='${key}']`).prop("readonly", cmode);
break;
case "radius":
case "oradius":
case "length":
case "width":
case "r1":
switch(wcssys){
case "image":
if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
case "physical":
if( obj.pub.lcs && obj.pub.lcs[key] !== undefined ){
val = fmt(obj.pub.lcs[key]);
}
break;
default:
if( obj.pub.wcsconfig &&
JS9.notNull(obj.pub.wcsconfig.wcssizestr) ){
val = fmt(obj.pub.wcsconfig.wcssizestr[0]);
} else if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
}
$(`${form}[name='${key}']`).prop("readonly", cmode);
break;
case "height":
case "r2":
switch(wcssys){
case "image":
if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
case "physical":
if( obj.pub.lcs && obj.pub.lcs[key] !== undefined ){
val = fmt(obj.pub.lcs[key]);
}
break;
default:
if( obj.pub.wcsconfig &&
JS9.notNull(obj.pub.wcsconfig.wcssizestr) ){
val = fmt(obj.pub.wcsconfig.wcssizestr[1]);
} else if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
}
$(`${form}[name='${key}']`).prop("readonly", cmode);
break;
case "wcssys":
case "savewcs":
// add all wcs sys options
el = $(form).find(`[name='${key}']`);
if( !el.find("option").length ){
for(i=0; i${JS9.wcssyss[i]}`);
}
}
if( key === "savewcs" ){
twcssys = JS9.globalOpts.regSaveWCS || wcssys;
} else {
twcssys = wcssys;
}
el.find("option").each((index, element) => {
if( twcssys === element.value ){
val = element.value;
}
});
break;
case "wcsunits":
if( obj.pub.wcsunits ){
val = obj.pub.wcsunits;
}
break;
case "childtext":
if( obj.params.children && obj.params.children.length > 0 ){
val = replaceNewline(obj.params.children[0].obj.text);
}
break;
case "text":
if( obj.pub[key] !== undefined ){
val = replaceNewline(fmt(obj.pub[key]));
}
break;
case "id":
if( multi ){
val = "selected";
} else if( obj.pub.id !== undefined ){
val = String(obj.pub.id);
// set width of text input to be width of string
$(element).css("width", `${val.length}ch`);
}
break;
case "tags":
if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
case "savefile":
val = $(form).data("savefile") ||
this.tmp.saveregionsFile ||
"js9.reg";
if( window.electron && !val.match(/.\*\//) ){
val = `${window.electron.currentDir}/${val}`;
}
break;
case "selectfilter":
val = $(form).data("selectfilter");
break;
case "selectshape":
case "selectcolor":
case "selecttag":
case "selectwcs":
case "selectgroup":
JS9.Regions.regionsConfigSetSelectMenu(this, $(form), key);
break;
default:
if( obj.pub[key] !== undefined ){
val = fmt(obj.pub[key]);
}
break;
}
$(element).val(val);
});
// display or hide options
if( multi || !this.raw.wcs || this.raw.wcs < 0 ){
$(form).find("[name='wcssys']").hide();
}
// edit-able parameters
// child text display for shapes, editable if no existing children yet
if( obj.type !== "text" && obj.params.children ){
$(`${form}.childtext`).removeClass("nodisplay");
}
// init options, if necessary
if( opts.firsttime ){
// desktop: display file browser
if( window.electron ){
$(form).find(".rsavebrowse, .rconfigbrowse")
.removeClass("nodisplay");
}
// multi "cur" works off selected, not current, regions
if( multi ){
$(form).find("label[for='savecur']")
.text("sel");
$(form).find("input[id='savecur']")
.data("tooltip", "save selected regions");
$(form).find("[id='selectreg']")
.prop("checked", true);
} else {
$(form).find(".checkboxes").removeClass("nodisplay");
}
// add wcs button options
if( JS9.favorites.wcs && JS9.favorites.wcs.length ){
// display wcs buttons
el = $(form).find(".rwcsbuttons").removeClass("nodisplay");
// add buttons to button container, if necessary
el2 = el.find(".rwcsbuttoncontainer");
if( el2.length && !el2.find(".rwcsbutton").length ){
// add radio buttons for each favorite wcs
for(i=0; i${s2}
`);
}
// init the radio buttons
$(form).find('.rwcsbuttons').find(`[value='${wcssys}']`)
.prop('checked', true);
}
}
// alternate colorpicker
if( !JS9.globalOpts.internalColorPicker ||
!$.fn.spectrum.inputTypeColorSupport() ){
el = $(form).find(`input[name='colorPicker']`)
el.spectrum({showButtons: false,
showInput: false,
preferredFormat: "hex6"});
// when the color is changed via the colorpicker
el.on('move.spectrum', (evt, tinycolor) => {
let color = tinycolor.toHexString();
$(form).find("input[name='color']").val(color);
$(form).data("colorpicker", color);
});
}
}
// checkboxes
if( obj.params.listonchange === undefined ){
obj.params.listonchange = false;
}
if( obj.params.listonchange ){
$(`${form}[name='listonchange']`).prop("checked", true);
} else {
$(`${form}[name='listonchange']`).prop("checked", false);
}
if( obj.params.changeable !== false ){
$(`${form}[name='locked']`).prop("checked", false);
} else {
$(`${form}[name='locked']`).prop("checked", true);
}
if( obj.params.sticky ){
$(`${form}[name='sticky']`).prop("checked", true);
} else {
$(`${form}[name='sticky']`).prop("checked", false);
}
// save regions processing
$(`${form}[id='includejson']`)
.prop("checked", JS9.globalOpts.regIncludeJSON);
$(`${form}[id='includecomments']`)
.prop("checked", JS9.globalOpts.regIncludeComments);
$(`${form}[id='savedcoords']`)
.prop("checked", JS9.globalOpts.regSaveDCoords);
$(`${form}[id='includewcs']`)
.prop("checked", JS9.globalOpts.csvIncludeWCS);
// unset all save format radio buttons
$(form).find(`input[name='saveformat']`)
.prop("checked", false);
// set save format based on global value
$(form).find(`input[value='${JS9.globalOpts.regSaveFormat}']`)
.prop("checked", true);
// unset all save wcs radio buttons
$(form).find(`input[name='rwcsbutton']`)
.prop("checked", false);
// set save wcs based on global value
$(form).find(`input[value='${JS9.globalOpts.regSaveWCS||wcssys}']`)
.prop("checked", true);
// set which regions get saved
if( opts.type === "save" ){
s = `save${JS9.globalOpts.regSaveWhich1}`;
} else {
s = `save${JS9.globalOpts.regSaveWhich2}`;
}
$(`${form}[id='${s}']`).prop("checked", true);
// triggering the savefile will cause format to be updated
// and focus to be set
if( opts.type === "save" ){
$(form).find(`input[name='savefile']`).trigger("change");
}
// style menus
$(form).find(`input[name='strokeMenu']`).prop("selectedIndex", 0);
$(form).find(`input[name='dashesMenu']`).prop("selectedIndex", 0);
// shape specific processing
if( multi ){
$(form).find(".regid").hide();
$(form).find(".edit").hide();
$(form).find(".childtext").hide();
$(form).find(".multi").removeClass("nodisplay");
if( opts.setmode <= 0 ){
$(form).find(`[name='multitext']`).val("");
$(form).find(`input[name="color"]`).val("");
$(form).find(`input[name="strokeWidth"]`).val("");
$(form).find(`input[name="strokeDashes"]`).val("");
$(form).data("strokewidth", "");
$(form).data("strokedashes", "");
if( opts.setmode < 0 ){
$(form).find(`[name='selectfilter']`).val("");
$(form).data("selectfilter", "");
}
} else {
ao = this.layers.regions.canvas.getActiveObject();
if( ao && ao.type === "group" && !ao.params ){
objs = ao.getObjects();
if( objs && objs.length && objs[0] && objs[0].params ){
grp = objs[0].params.groupid;
}
if( grp ){
$(form).find(`[name='selectfilter']`).val(grp);
$(form).data('selectfilter', grp);
s = this.listGroups(grp);
s2 = s.substring(s.indexOf("\n")+1);
$(form).find(`[name='multitext']`).val(s2);
} else {
$(form).find(`[name='multitext']`).val("");
}
} else if( ao ){
ao = this.layers.regions.canvas.getActiveObjects();
for(i=0, s=[], s2=""; i {
$(form).find(`input[name='savefile']`).focus();
});
}
// add tooltip callbacks (not mobile: ios buttons stop working!)
if( !$(form).data("tooltipInit") ){
$(form).data("tooltipInit", true);
$(".rconfigcol\_R, .rsavecol\_R").on(mover, (e) => {
const target = e.currentTarget;
const tooltip = $(target)
.find("input, textarea, span")
.data("tooltip");
const el = $(target)
.closest(JS9.lightOpts[JS9.LIGHTWIN].top)
.find(JS9.lightOpts[JS9.LIGHTWIN].dragBar);
if( tooltip && el.length ){
// change title: see dhtmlwindow.js load() @line 130
otitle = $(el)[0].childNodes[0].nodeValue.replace(/:.\*/,"");
$(el)[0].childNodes[0].nodeValue = `${otitle}: ${tooltip}`;
}
});
$(".rconfigcol\_R, .rsavecol\_R").on(mout, (e) => {
const target = e.currentTarget;
const el = $(target)
.closest(JS9.lightOpts[JS9.LIGHTWIN].top)
.find(JS9.lightOpts[JS9.LIGHTWIN].dragBar);
if( el.length ){
otitle = $(el)[0].childNodes[0].nodeValue.replace(/:.\*/,"");
$(el)[0].childNodes[0].nodeValue = otitle;
}
});
}
};
// process the config form to change the specified shape
// call using image context
JS9.Regions.processConfigForm = function(form, obj, arr){
let i, key, nkey, val, nval, nopts, multi, layer, wcssys;
let cpos, p1, p2, d, x, y, ang, sel;
let bin = 1;
const defobj = {
type: "multi",
pub: {shape: "multi"},
params: {}
};
const alen = arr.length;
const opts = {};
const wcsinfo = this.raw.wcsinfo || {cdelt1: 1, cdelt2: 1};
const fmt= (val) => {
if( val === undefined ){
return undefined;
}
if( (typeof val === "number") && (val % 1 !== 0) ){
val = Math.round((val + 0.00001) \* 10000) / 10000;
}
return(String(val));
};
const fmtcheck = (val1, val2) => {
if( multi ){
return true;
}
if( val1 === undefined ){
return false;
}
return fmt(val1) !== fmt(val2);
};
const newval = (obj, key, val) => {
// let v1, v2;
// special keys having no public or param equivalents
if( key === "remove" ){
return val === "selected";
}
if( key === "childtext" ){
if( obj.params.children && obj.params.children.length > 0 ){
if( obj.params.children[0].obj &&
obj.params.children[0].obj.params ){
return val !== obj.params.children[0].obj.params.text;
}
return false;
}
return val !== obj.params.text;
}
if( key === "strokeWidth" ){
if( obj.params && obj.params.sw1 ){
return val !== obj.params.sw1;
} else {
return true;
}
}
if( key === "strokeDashes" ){
if( obj.strokeDashArray){
return JSON.stringify(obj.strokeDashArray) !==
JSON.stringify(val);
}
if( $.isArray(val) ){
switch(val.length){
case 0:
return false;
case 1:
return val[0] !== "";
case 2:
default:
return val[0] !== "" && val[1] !== "";
}
} else {
return val !== "";
}
}
if( key !== "tags" && val === "" ){
return false;
}
if( key === "misc" && val !== "" ){
return true;
}
if( key === "radii" && obj.params.radii ){
// https://stackoverflow.com/questions/1773069/using-jquery-to-compare-two-arrays-of-javascript-objects
// v1 = val.split(",").map((item) => {return parseFloat(item)});
// v2 = obj.params.radii;
// return $(v1).not(v2).length !== 0 || $(v2).not(v1).length !== 0;
// always return true or else annuli won't change other properties
return true;
}
if( key === "angle" ){
return obj.angle !== -parseFloat(val);
}
if( key === "ix" ){
if( obj.pub.preservedcoords &&
val.charAt(0).toLowerCase() === "d" ){
return fmtcheck(obj.pub.dx, JS9.saostrtod(val.substring(1)));
} else {
return fmtcheck(obj.pub.x, JS9.saostrtod(val));
}
}
if( key === "iy" ){
if( obj.pub.preservedcoords &&
val.charAt(0).toLowerCase() === "d" ){
return fmtcheck(obj.pub.dy, JS9.saostrtod(val.substring(1)));
} else {
return fmtcheck(obj.pub.y, JS9.saostrtod(val));
}
}
if( key === "px" && obj.pub.lcs ){
return fmtcheck(obj.pub.lcs.x.toFixed(1), val);
}
if( key === "py" && obj.pub.lcs ){
return fmtcheck(obj.pub.lcs.y.toFixed(1), val);
}
if( key === "ra" ){
if( obj.pub.wcsconfig && obj.pub.wcsconfig.wcsposstr ){
return fmtcheck(JS9.saostrtod(obj.pub.wcsconfig.wcsposstr[0]),
JS9.saostrtod(val));
} else if( obj.pub.wcsposstr ){
return fmtcheck(JS9.saostrtod(obj.pub.wcsposstr[0]),
JS9.saostrtod(val));
}
return false;
}
if( key === "dec" ){
if( obj.pub.wcsconfig && obj.pub.wcsconfig.wcsposstr ){
return fmtcheck(JS9.saostrtod(obj.pub.wcsconfig.wcsposstr[1]),
JS9.saostrtod(val));
} else if( obj.pub.wcsposstr ){
return fmtcheck(JS9.saostrtod(obj.pub.wcsposstr[1]),
JS9.saostrtod(val));
}
}
if( key === "sticky" ){
if( multi ){
return false;
} else {
return fmtcheck(obj.pub.sticky||false, val);
}
}
if( key === "locked" ){
if( multi ){
return false;
} else {
if( obj.params.changeable !== false ){
return val === false;
} else {
return val === true;
}
}
}
if( key === "listonchange" ){
if( multi ){
return false;
}
}
if( obj.pub.lcs && obj.pub.lcs[key] !== undefined ){
if( fmtcheck(obj.pub.lcs[key], val) ){
return true;
}
// don't look further or we end up checking image x, y
return false;
}
if( fmtcheck(obj.pub[key], val) ){
return true;
}
if( fmtcheck(obj.params[key], val) ){
return true;
}
if( fmtcheck(obj[key], val) ){
return true;
}
return false;
};
const getval = (s) => {
if( s === "true" ){
return true;
}
if( s === "false" ){
return false;
}
if( !JS9.isNumber(s) ){
return s;
}
return parseFloat(s);
};
const replaceNewline = (s) => {
const nl = String.fromCharCode(13, 10);
if( typeof s === "string" ){
return s.replace(/\\n/g, nl);
}
return s;
};
// set physical to image conversion, if possible
if( this.lcs && this.lcs.physical ){
bin = Math.sqrt(Math.pow(this.lcs.physical.forward[0][0],2) +
Math.pow(this.lcs.physical.forward[0][1],2));
}
// which wcssys do we use? edit version, if available
if( obj && obj.pub ){
if( obj.pub.wcsconfig && obj.pub.wcsconfig.wcssys ){
wcssys = obj.pub.wcsconfig.wcssys;
} else {
wcssys = this.params.wcssys;
}
} else {
wcssys = this.params.wcssys;
// fake obj: makes the checks easier, avoid if( obj ... ) everywhere
obj = defobj;
}
// multi selection or single region
multi = $(form).data("multi");
// layer or regions
layer = obj.pub.layer || "regions";
// process array of keyword/values
for(i=0; i parseInt(s, 10) );
}
}
}
break;
case "strokeWidth":
if( val === "" ){
opts[key] = "";
} else {
if( JS9.isNumber(val) ){
nval = parseInt(val, 10);
if( nval <= 0 ){
opts[key] = "";
} else if( (multi && val) ||
(!multi && newval(obj, key, nval)) ){
opts[key] = getval(nval);
}
}
}
break;
case "color":
if( val === "" ){
opts[key] = "";
} else if( newval(obj, key, val) ){
opts[key] = getval(val);
}
break;
case "tags":
if( multi ){
if( val ){
if( val === '""' || val === "''" ){
opts[key] = "";
} else {
opts[key] = getval(val);
}
}
} else if( newval(obj, key, val) ){
opts[key] = getval(val);
}
break;
case "childtext":
if( obj.type !== "text" ){
if( newval(obj, key, val) ){
opts.text = replaceNewline(val);
}
}
break;
case "ix":
if( newval(obj, key, val) ){
if( obj.pub.preservedcoords &&
val.charAt(0).toLowerCase() === "d" ){
opts.dx = getval(val.substring(1));
if( opts.dy === undefined && obj.pub.dy !== undefined ){
opts.dy = obj.pub.dy;
}
} else {
opts.x = getval(val);
if( opts.y === undefined && obj.pub.y !== undefined ){
opts.y = obj.pub.y;
}
}
}
break;
case "iy":
if( newval(obj, key, val) ){
if( obj.pub.preservedcoords &&
val.charAt(0).toLowerCase() === "d" ){
opts.dy = getval(val.substring(1));
if( opts.dx === undefined && obj.pub.dx !== undefined ){
opts.dx = obj.pub.dx;
}
} else {
opts.y = getval(val);
if( opts.x === undefined && obj.pub.x !== undefined ){
opts.x = obj.pub.x;
}
}
}
break;
case "px":
if( newval(obj, key, val) ){
opts.px = getval(val);
if( opts.py === undefined && obj.pub.lcs ){
opts.py = obj.pub.lcs.y;
}
}
break;
case "py":
if( newval(obj, key, val) ){
opts.py = getval(val);
if( opts.px === undefined && obj.pub.lcs ){
opts.px = obj.pub.lcs.x;
}
}
break;
case "ra":
if( newval(obj, key, val) ){
opts.ra = val;
if( opts.dec === undefined ){
if( obj.pub.wcsconfig && obj.pub.wcsconfig.wcsposstr ){
opts.dec = obj.pub.wcsconfig.wcsposstr[1];
} else if( obj.pub.wcsposstr ){
opts.dec = obj.pub.wcsposstr[1];
}
}
}
break;
case "dec":
if( newval(obj, key, val) ){
opts.dec = val;
if( opts.ra === undefined ){
if( obj.pub.wcsconfig && obj.pub.wcsconfig.wcsposstr ){
opts.ra = obj.pub.wcsconfig.wcsposstr[0];
} else if( obj.pub.wcsposstr ){
opts.ra = obj.pub.wcsposstr[0];
}
}
if( opts.wcssys === undefined ){
opts.wcssys = wcssys;
}
}
break;
case "wcssys":
break;
case "radius":
case "length":
case "width":
case "r1":
switch(wcssys){
case "image":
if( newval(obj, key, val) ){
opts[key] = getval(val);
}
break;
case "physical":
if( newval(obj, key, val) ){
opts[key] = getval(val) \* bin;
}
break;
default:
nval = JS9.strtoscaled(val);
val = Math.abs(nval.dval / wcsinfo.cdelt1);
nkey = key.replace("wcs", "");
if( newval(obj, nkey, val) ){
opts[nkey] = getval(val);
}
break;
}
break;
case "height":
case "r2":
switch(wcssys){
case "image":
if( newval(obj, key, val) ){
opts[key] = getval(val);
}
break;
case "physical":
if( newval(obj, key, val) ){
opts[key] = getval(val) \* bin;
}
break;
default:
nval = JS9.strtoscaled(val);
val = Math.abs(nval.dval / wcsinfo.cdelt2);
nkey = key.replace("wcs", "");
if( newval(obj, nkey, val) ){
opts[nkey] = getval(val);
}
break;
}
break;
case "radii":
if( newval(obj, key, val) ){
opts[key] = val;
}
break;
case "linelength":
if( obj.pub.pts && obj.pub.pts.length === 2 ){
if( JS9.isNumber(val) && val !== this.tmp.linelength ){
val = parseFloat(val);
switch(wcssys){
case "image":
case "physical":
break;
default:
if( wcsinfo.cdelt1 !== undefined ){
val /= Math.abs(wcsinfo.cdelt1);
} else if( wcsinfo.cdelt2 !== undefined ){
val /= Math.abs(wcsinfo.cdelt2);
}
break;
}
if( opts.pts ){
p1 = opts.pts[0];
p2 = opts.pts[1];
} else {
p1 = obj.pub.pts[0];
p2 = obj.pub.pts[1];
}
if( $.inArray("line",
JS9.Regions.opts.noCenteredScaling) >= 0 ){
// leave p1 fixed
// https://math.stackexchange.com/questions/175896/finding-a-point-along-a-line-a-certain-distance-away-from-another-point
d = Math.sqrt((p1.x - p2.x) \* (p1.x - p2.x) +
(p1.y - p2.y) \* (p1.y - p2.y) );
x = p1.x - (val \* (p1.x - p2.x))/d;
y = p1.y - (val \* (p1.y - p2.y))/d;
opts.pts = [p1, {x, y}];
} else {
// leave center fixed
cpos = {x: (p1.x + p2.x) / 2, y: (p1.y + p2.y) / 2 };
ang = parseFloat(this.tmp.lineangle)||0;
p1.x = cpos.x - val/2;
p1.y = cpos.y;
p2.x = cpos.x + val/2;
p2.y = cpos.y;
opts.pts = [JS9.rotatePoint(p1, ang, cpos),
JS9.rotatePoint(p2, ang, cpos)];
}
}
}
break;
case "lineangle":
if( obj.pub.pts && obj.pub.pts.length === 2 ){
if( JS9.isNumber(val) && val !== this.tmp.lineangle ){
ang = parseFloat(val) - parseFloat(this.tmp.lineangle)||0;
if( opts.pts ){
p1 = opts.pts[0];
p2 = opts.pts[1];
} else {
p1 = obj.pub.pts[0];
p2 = obj.pub.pts[1];
}
if( $.inArray("line",
JS9.Regions.opts.noCenteredScaling) >= 0 ){
// leave p1 fixed
opts.pts = [p1, JS9.rotatePoint(p2, ang, p1)];
} else {
// leave center fixed
cpos = {x: (p1.x + p2.x) / 2, y: (p1.y + p2.y) / 2 };
opts.pts = [JS9.rotatePoint(p1, ang, cpos),
JS9.rotatePoint(p2, ang, cpos)];
}
}
}
break;
case "remove":
if( newval(obj, key, val) ){
if( multi ){
opts[key] = "selected";
} else if( obj.pub.id !== undefined ){
opts[key] = obj.pub.id;
}
}
break;
case "locked":
if( newval(obj, key, !getval(val)) ){
opts.changeable = !getval(val);
}
break;
case "misc":
if( val.trim() ){
try{ nopts = JSON.parse(val); $.extend(opts, nopts); }
catch(e){ JS9.error(`invalid json: ${val}`);}
}
break;
default:
if( newval(obj, key, val) ){
opts[key] = getval(val);
}
break;
}
}
// change the shape(s), if necessary
if( Object.keys(opts).length > 0 ){
if( multi ){
sel = $(form).find(`[name='selectfilter']`).val() || "selected";
this.changeShapes(layer, sel, opts);
} else {
sel = $(form).find(`[name='id']`).val() || obj;
this.changeShapes(layer, sel, opts);
}
this.initRegionsForm(obj, {multi});
}
};
// convenience routine used in regionsConfig.html
JS9.Regions.regionsConfigSetSelectFilter = function(el, def) {
let i, s, curval, lastval, nval, nfilter;
let arr = [];
let defarr = [];
let grparr = [];
const form = el.closest('form');
const filter = form.find(`[name='selectfilter']`);
const im = form.data('im');
const withparens = (s) => {
let t;
if( !s ){ return ""; }
t = s.trim();
if( t.charAt(0) === "(" && t.charAt(t.length-1) === ")" ){
return t;
} else {
return `(${t})`;
}
};
// sanity check
if( !im ){ return; }
// groups
grparr = im.listGroups("all", {includeregions:false}).split("\n");
// new value from menu
nval = el.val().trim();
// cur value from filter select
curval = filter.val().trim();
// handle "saved" specially
if( def === "other" && nval === "saved" ){
// compose and set the new filter selection
s = im.layers.regions.selection || "";
if( s ){
if( curval ){
s = `${withparens(s)} && ${withparens(curval)}`;
}
}
filter.val(`${s}`);
// reset the menu
el.prop('selectedIndex', 0);
return;
}
if( curval ){
arr = curval.split(/\s+/);
}
if( arr.length ){
lastval = arr[arr.length-1];
if( !nval.match(/[&|]/) && !lastval.match(/[&|!]/) ){
// get array of possible values
switch(def){
case "regions":
defarr = JS9.regions;
break;
case "colors":
break;
case "tags":
break;
case "wcssys":
defarr = JS9.wcssyss;
break;
case "groups":
defarr = grparr;
break;
case "ops":
defarr = ["!", "&&", "||"];
break;
}
if( $.inArray(lastval, defarr) >= 0 ){
// if new and last val is of the same type, use || for union
// (intersection of same types, but non-identical, is null)
nval = `|| ${nval}`;
} else if( $.inArray(lastval, grparr) >= 0 ||
$.inArray(nval, grparr) >= 0 ){
// if either is a group, use || for union
// (intersection of non-identical groups is null)
nval = `|| ${nval}`;
} else {
// use && for intersection, e.g., color && shape
nval = `&& ${nval}`;
}
}
}
// this is the new filter
nfilter = `${curval} ${nval}`;
// futz w/parens: split by ||, add parens around segments containing &&
// if you used the menus to choose these:
// circle blue || box red
// then instead of this:
// circle && blue || box && red
// we should end up with this:
// (circle && blue) || (box && red)
if( JS9.globalOpts.regConfigAddParens ){
arr = nfilter.split("||");
if( arr.length >= 2 ){
for(i=0; i 0 ){
arr[i] = withparens(s);
} else {
arr[i] = s;
}
}
}
nfilter = arr.join(' || ').replace(/ \*/g, " ");
}
// compose and set the new filter selection
filter.val(nfilter);
// reset the menu
el.prop('selectedIndex', 0);
};
// convenience routine used in regionsConfig.html
JS9.Regions.regionsConfigSetSelectMenu = function(im, form, key) {
let i, j, s, el, objs, gots, arr;
const initmenu = (el) => {
let i;
// remove all but the header (0th option)
for(i=el.options.length-1; i>=1; i--) {
el.remove(i);
}
};
if( !key.match(/^select/) ){
key = `select${key}`;
}
el = form.find(`[name='${key}']`);
// reinit: clear menu
initmenu(el[0]);
// current objects
objs = im.getShapes("regions", "all");
// add items
switch(key){
case "selectshape":
for(i=0, gots=[]; i${s}`);
gots.push(s);
}
}
break;
case "selectcolor":
for(i=0, gots=[]; i${s}`);
gots.push(s);
}
}
break;
case "selecttag":
for(i=0, gots=[]; i${s[j]}`);
gots.push(s[j]);
}
}
}
break;
case "selectwcs":
for(i=0, gots=[]; i${s}`);
gots.push(s);
}
}
}
break;
case "selectgroup":
s = im.listGroups("all", {includeregions:false});
if( s ){
arr = s.split("\n");
for(i=0; i${arr[i]}`);
}
}
break;
}
};
// convenience routine used in regionsConfig.html
JS9.Regions.regionsConfigSetSelectOrGroup = function(im, form, key, update){
let obj, group, canvas;
let el1 = form.find(`[name="selectfilter"]`);
let el2 = form.find(`[name="multitext"]`);
let selection = el1.val().trim();
// sanity check
if( !im ){ return; }
// convenience variables
canvas = im.layers.regions.canvas;
// default is to allow update of multi-selection dialog
// sometimes we definitely don't want that to happen, so ...
if( update === false ){ im.tmp.updateMulti = false; }
// default is to select
if( !selection ){
el1.val("");
el2.val("");
form.data("selectfilter", "");
if( canvas.getActiveObject() ){
canvas.discardActiveObject();
}
canvas.renderAll()
key = "clear";
}
if( !key ){
key = im.lookupGroup(selection) ? "group" : "select";
}
switch(key){
case "select":
form.data("selectfilter", selection);
im.selectShapes("regions", selection, {transparentgroup: false});
break;
case "group":
form.data("selectfilter", selection);
group = im.groupShapes("regions", selection);
el1.val(group);
el2.val(im.listGroups(group))
obj = im.lookupGroup(group);
if( obj ){
canvas.setActiveObject(obj);
canvas.renderAll();
JS9.Regions.regionsConfigSetSelectMenu(im, form, "selectgroup");
}
break;
case "ungroup":
im.ungroupShapes("regions", selection);
el1.val("");
el2.val("");
form.data("selectfilter", "");
if( canvas.getActiveObject() ){
canvas.discardActiveObject();
}
JS9.Regions.regionsConfigSetSelectMenu(im, form, "selectgroup");
break;
case "clear":
form.find(`input[name="color"]`).val("");
form.find(`input[name="strokeWidth"]`).val("");
form.find(`input[name="strokeDashes"]`).val("");
form.data("strokewidth", "");
form.data("strokedashes", "");
break;
default:
break;
}
delete im.tmp.updateMulti;
};
// paste a region from clipboard
// call using image context
JS9.Regions.pasteFromClipboard = function(curpos){
let i, s, nobj, xpos, ypos, oval;
let objs = [];
let xcen = 0, ycen = 0;
const rregexp = /(annulus|box|circle|cross|ellipse|line|polygon|point|text) \*\(/;
// sanity check
if( !this ){ return; }
// get string from clipboard
s = JS9.CopyFromClipboard().trim();
// see if we have anything at all
if( !s ){
JS9.error(JS9.CLIPBOARDERROR);
}
// see if we have region(s)
if( s.match(rregexp) ){
// we don't update the clipboard for these operations
oval = JS9.globalOpts.regToClipboard;
JS9.globalOpts.regToClipboard = false;
// add regions (don't update clipboard)
objs = this.addShapes("regions", s, {rtn: "objs"});
// place regions in the position specified by the mouse, if necessary
if( curpos ){
// number of regions
nobj = objs.length;
// get centroid
for(i=0; i {
let i, s, key, child, ra, dec;
const nexports = {};
const params = obj.params;
const children = params.children;
const exports = params.exports;
for(i=0; i 0) && (children[0].obj.text) ){
child = children[0].obj;
// create a text child
nexports.text = child.text;
// get options for text child but ...
nexports.textOpts = getExports(child);
// try to minimize exported properties
if( obj.angle !== child.angle ){
// child has an explicit angle different from parent
nexports.textOpts.angle = -child.angle;
if( (obj.params.shape === "circle") ||
(obj.params.shape === "annulus") ){
child.params.hasTextOpts = true;
}
} else if( child.angle !== 0 ){
// parent is circle/annulus and child has an angle
if( (obj.params.shape === "circle") ||
(obj.params.shape === "annulus") ){
nexports.textOpts.angle = -child.angle;
child.params.hasTextOpts = true;
}
}
if( child.params.parent.moved || child.params.hasTextOpts ){
// wcs, then physical coords are preferred ...
if( child.pub.ra && child.pub.dec ){
// convert child ra, dec to target wcs, if necessary
if( owcssys && wcssys && owcssys !== wcssys ){
s = this.wcs2wcs(owcssys, wcssys,
child.pub.ra, child.pub.dec);
s = s.trim().split(/\s+/);
ra = JS9.saostrtod(s[0]);
if( JS9.isHMS(wcssys) ){
ra \*= 15.0;
}
dec = JS9.saostrtod(s[1]);
} else {
ra = child.pub.ra;
dec = child.pub.dec;
}
nexports.textOpts.ra = ra;
nexports.textOpts.dec = dec;
} else if( child.pub.lcs ){
nexports.textOpts.px = child.pub.lcs.x;
nexports.textOpts.py = child.pub.lcs.y;
} else {
// ... image coords will are only good for this image
nexports.textOpts.x = child.pub.x;
nexports.textOpts.y = child.pub.y;
}
}
if( nexports.textOpts.color === obj.stroke ){
delete nexports.textOpts.color;
}
if( nexports.textOpts.text ){
delete nexports.textOpts.text;
}
if( !Object.keys(nexports.textOpts).length ){
delete nexports.textOpts;
}
}
return nexports;
};
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "string" ){
try{ opts = JSON.parse(opts); }
catch(e){ JS9.error(`can't parse listRegions opts: ${opts}`, e); }
}
// pass sortids from opts to topts (used by getShapes)
if( JS9.notNull(opts.sortids) ) topts.sortids = opts.sortids;
// default is to display, including non-source tags
mode = opts.mode;
if( JS9.isNull(mode) ){
mode = 3;
}
// default is to list the regions layer
layerName = layerName || "regions";
layer = this.getShapeLayer(layerName);
// sanity check
if( !layer ){ return; }
// set user-specified wcs, if necessary
if( opts.wcssys || opts.wcsunits ){
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
if( opts.wcssys ){
owcssys = this.getWCSSys();
this.setWCSSys(opts.wcssys, false);
wcssys = this.getWCSSys();
}
if( opts.wcsunits ){
owcsunits = this.getWCSUnits();
this.setWCSUnits(opts.wcsunits, false);
}
// update wcs values
this.updateShapes(layerName, which, "export");
}
// include dcoord shapes?
if( JS9.isNull(opts.includedcoords) ){
opts.includedcoords = JS9.globalOpts.regListDCoords;
}
// get specified regions into an array
pubs = this.getShapes(layerName, which, topts);
// loop through shapes
rlen = pubs.length;
// display tags if at least one is not standard "source,include"
if( mode ){
for(i=0; i 0 ){ regstr += ","; }
regstr += `"${key}":`;
switch(typeof val){
case "string":
regstr += `"${val}"`;
break;
case "object":
try{ regstr += JSON.stringify(val); }
catch(e){ JS9.error(`can't parse: ${val}`, e); }
break;
default:
regstr += `${val}`;
break;
}
}
}
regstr += `})`;
lasttype = "image";
continue;
}
// init tags
tagjoin = region.tags.join(",");
if( tagjoin.includes("exclude") ){
iestr = "-";
} else {
iestr = "";
}
// add exported properties
exports = getExports(obj, region);
// add id, if necessary
if( opts.saveid ){
exports.id = region.id;
} else {
delete exports.id;
}
// save wcsconfig, if necessary
if( opts.savewcsconfig && region.wcsconfig &&
Object.keys(region.wcsconfig).length > 0 ){
exports.wcsconfig = $.extend(true, {}, region.wcsconfig);
} else {
delete exports.wcsconfig;
}
// add color, if necessary
if( region.color && !tagcolors.includes(region.color) ){
exports.color = region.color;
}
// display tags?
if( dotags ){
tagstr = ` # ${tagjoin}`;
}
// save editing?
if( !opts.saveediting ){
delete exports.editing;
}
// use wcs string, if available
if( region.wcsstr && JS9.isWCSSys(this.params.wcssys) ){
if( lasttype !== "wcs" ){
if( lasttype !== "none" ){
regstr += sepstr;
}
// use region wcs sys, if possible
// (current wcssys might be different!)
if( region.wcssys ){
regstr += region.wcssys;
} else {
regstr += this.params.wcssys;
}
lasttype = "wcs";
}
regstr += (sepstr + iestr + region.wcsstr);
} else if( region.imstr ){
// else use image string, if available
if( lasttype !== region.imsys ){
if( lasttype !== "none" ){
regstr += sepstr;
}
regstr += region.imsys;
lasttype = region.imsys;
}
regstr += (sepstr + iestr + region.imstr);
}
// odd modes output the exports
if( opts.includejson !== false &&
((mode % 2) === 1) &&
(Object.keys(exports).length > 0) ){
// line region: remove size/distance info
if( region.shape === "line" ){
regstr = regstr.replace(/ \*{[^{}]\*}$/,"");
}
regstr += ` ${JSON.stringify(exports)}`;
}
if( tagstr ){
regstr += tagstr;
}
}
// remove comments, if necessary
if( opts.includecomments === false ){
regstr = regstr.replace(/ \*#[^;]\*/g, "");
}
// restore original wcs, if necessary
if( owcssys || owcsunits ){
if( owcssys ){
this.setWCSSys(owcssys, false);
}
if( owcsunits ){
this.setWCSUnits(owcsunits, false);
}
// restore wcs values
this.updateShapes(layerName, which, "export");
JS9.globalOpts.xeqPlugins = txeq;
}
// display the region string, if necessary
if( mode > 1 ){
this.display.displayMessage("regions", regstr);
}
// always return the region string
return regstr;
};
// copy one or more regions to another image
// call using image context
JS9.Regions.copyRegions = function(to, which){
return this.copyShapes("regions", to, which);
};
// parse a string containing a subset of DS9/Funtools regions
// call using image context
JS9.Regions.parseRegions = function(s, opts){
let i, j, k, lines, obj, robj, txeq;
let owcssys, owcsunits, wcssys, iswcs, liswcs, pos, alen;
const regions = [];
const regrexp = /^-?(annulus|box|circle|cross|ellipse|line|polygon|point|text)$/;
const wcsrexp = /^(fk4|fk5|icrs|galactic|ecliptic|image|physical|linear)$/;
const imrexp = /^(image|physical)$/;
const unrexp = /[dr:]/;
const parrexp = /\(\s\*([^)]+?)\s\*\)/;
const seprexp = /\n|;/;
const optsrexp = /(\{.\*\})/;
const argsrexp = /\s\*,\s\*/;
const charrexp = /(\(|\{|#|;|\n)/;
const comrexp = /#(?![a-zA-Z0-9]{6}['"])/;
// convert "0" to false and "1" to true
const tf = (s) => {
if( s === "0" || s.toLowerCase() === "false" ){return false;}
return true;
};
// ds9 compatibility: get properties from comment string
const ds9properties = (s) => {
let xarr, key, key2, val, nobj;
const xobj = {};
const rexp = /([a-zA-Z][a-zA-Z0-9\_]\*)\s\*=\s\*(\d+(\s\*\d+)\*|[^ '"{]+|['"{][^'"}]\*['"}])/g;
const ds9opts = {
color(v) {return {color: v};},
dash(v) {if(v){return {strokeDashArray: [3,1]};}},
dashlist(v) {
let i, arr;
if( v ){
arr = v.split(" ");
for(i=0; i= 1 ){ obj.fontFamily = arr[0]; }
if( len >= 2 ){ obj.fontSize = parseFloat(arr[1]); }
if( len >= 3 ){ obj.fontStyle = arr[2]; }
if( len >= 4 ){ obj.fontWeight = arr[3]; }
return obj;
},
highlite(v) {return {hasControls: tf(v), hasBorders: tf(v), hasRotatingPoint: tf(v)};},
move(v) {return {movable: tf(v)};},
rotate(v) {return {rotatable: tf(v)};},
resize(v) {return {resizable: tf(v)};},
changeable(v) {return {changeable: tf(v)};},
select(v) {return {selectable: tf(v)};},
text(v) {return {text: v};},
tag(v) {return {tags: v};},
width(v) {return {strokeWidth: parseFloat(v)};}
};
// opts is optional
opts = opts || {};
// loop through DS9 region properties, converting to js9 props
while( (xarr = rexp.exec(s)) !== null ){
key = xarr[1].toLowerCase();
val = xarr[2].replace(/^['"{]|['"}]$/g, "");
if( {}.hasOwnProperty.call(ds9opts, key) &&
typeof ds9opts[key] === "function" ){
nobj = ds9opts[key](val) || {};
for( key2 of Object.keys(nobj) ){
if( key2 === "tags" && {}.hasOwnProperty.call(xobj, key2) ){
xobj[key2] += `,${nobj[key2]}`;
} else {
xobj[key2] = nobj[key2];
}
}
} else {
xobj[key] = val;
}
}
// save the remaining comment
s = s.replace(rexp, "");
if( s ){
xobj.\_comment = s.trim();
}
return xobj;
};
// parse region line into cmd (shape or wcs), args, opts, comment
const regparse1 = (s) => {
let t, tarr, ds9props;
const tobj = {};
// initialize the return object
tobj.opts = {};
tobj.args = [];
tobj.isregion = 0;
// look for a command
if( s.includes("(") ){
tobj.cmd = s.split("(")[0].trim().toLowerCase();
} else if( s.includes("{") ){
tobj.cmd = s.split("{")[0].trim().toLowerCase();
} else if( s.includes("#") ){
tobj.cmd = s.split("#")[0].trim().toLowerCase();
} else {
tobj.cmd = s.trim().toLowerCase();
}
// got regions?
if( tobj.cmd ){
tobj.isregion = (tobj.cmd.search(regrexp) >=0);
}
// split on comment (ignore color specifications starting with "#")
t = s.trim().split(comrexp);
// look for json opts after the arg list
tarr = optsrexp.exec(t[0]);
if( tarr && tarr[0] ){
// convert to object
try{ tobj.opts = JSON.parse(tarr[0].trim()); }
catch(e){ JS9.error(`can't parse opts: ${tarr[0]}`, e); }
}
// look for comments
tobj.comment = t[1];
if( tobj.comment ){
ds9props = ds9properties(tobj.comment.trim());
if( ds9props.\_comment !== undefined ){
tobj.comment = ds9props.\_comment;
delete ds9props.\_comment;
}
}
// merge with ds9 opts
if( ds9props ){
tobj.opts = $.extend({}, ds9props, tobj.opts);
}
// separate the region args into an array
tarr = parrexp.exec(s);
if( tarr && tarr[0].match(optsrexp) ){
// no region args, all properties passed in json
tobj.args = [];
} else if( tarr && tarr[1] ){
// region args, without json opts
tobj.args = tarr[1].split(argsrexp);
}
// look for - sign signifying an exclude region
if( tobj.isregion && tobj.cmd.startsWith("-") ){
tobj.cmd = tobj.cmd.slice(1);
if( tobj.comment ){
if( !tobj.comment.match(/exclude/) ){
tobj.comment += ",exclude";
}
} else {
tobj.comment = "exclude";
}
}
return tobj;
};
const getipos = (ix, iy) => {
let vt, sarr, v1, v2;
let obj = {};
// special handling for display coords
if( ix.charAt(0).toLowerCase() === "d" &&
iy.charAt(0).toLowerCase() === "d" ){
obj.dx = parseFloat(ix.substring(1));
obj.dy = parseFloat(iy.substring(1));
return obj;
}
// convert strings to numbers, along with unit delimiters
v1 = JS9.strtoscaled(ix);
v2 = JS9.strtoscaled(iy);
// local override of wcs if:
// a. we used sexagesimal units or appended d,r
// b. we are not currently using wcs
if( ((v1.dtype.match(unrexp)) || (v2.dtype.match(unrexp))) &&
!iswcs && !owcssys.match(imrexp) ){
liswcs = true;
wcssys = owcssys;
}
if( iswcs || liswcs ){
// arg1 coords are hms, but ecliptic, galactic are deg
if( JS9.isHMS(wcssys, v1.dtype) ){
v1.dval \*= 15.0;
}
// convert to degrees, if necessary
if( v1.dtype === "r" ){ v1.dval = v1.dval \* 180 / Math.PI; }
if( v2.dtype === "r" ){ v2.dval = v2.dval \* 180 / Math.PI; }
// get image coordinates
sarr = JS9.wcs2pix(this.raw.wcs, v1.dval, v2.dval).split(/ +/);
obj.x = parseFloat(sarr[0]);
obj.y = parseFloat(sarr[1]);
return obj;
} else if( wcssys === "physical" ){
vt = this.logicalToImagePos({x: v1.dval, y: v2.dval});
obj.x = vt.x;
obj.y = vt.y;
return obj;
}
// image coords
obj.x = v1.dval;
obj.y = v2.dval;
return obj;
};
// get image length
const getilen = (len, which) => {
let cstr, iscale;
const v = JS9.strtoscaled(len);
const wcsinfo = this.raw.wcsinfo || {cdelt1: 1, cdelt2: 1};
// local override of wcs if:
// a. we are not currently using wcs
// b. we used sexagesimal units or appended d,r
if( v.dtype.match(unrexp) && !iswcs && !owcssys.match(imrexp) ){
liswcs = true;
wcssys = owcssys;
}
if( iswcs || liswcs ){
// convert to degrees, if necessary
if( v.dtype === "r" ){ v.dval = v.dval \* 180 / Math.PI; }
// angular separation is not implemented
// region wcs size is always based on cdelt
if( JS9.REGSIZE !== 0 ){
JS9.error("region size based on ang sep is not implemented");
}
// wcs-based size
cstr = `cdelt${which}`;
v.dval = Math.abs(v.dval / wcsinfo[cstr]);
} else if( wcssys === "physical" ){
// use the LTM1\_1 value stored for logical to image transforms
if( this.lcs && this.lcs.physical ){
iscale = Math.sqrt(Math.pow(this.lcs.physical.forward[0][0],2)+
Math.pow(this.lcs.physical.forward[0][1],2));
v.dval = Math.abs(v.dval \* iscale);
}
}
return v.dval;
};
// get image angle
const getang = (a) => {
const v = JS9.strtoscaled(a);
return v.dval;
};
// get cleaned-up string
const getstr = (s) => {
const t = s.replace(/^['"]/, "").replace(/["']$/, "");
return t;
};
// sanity check
s = s.trim();
if( !s.match(charrexp) ){
return s;
}
// save original wcs
owcssys = this.getWCSSys();
owcsunits = this.getWCSUnits();
// this is the default wcs for regions
wcssys = "physical";
// do we have a real wcs?
iswcs = JS9.isWCSSys(wcssys);
// get individual "lines" (new-line or semi-colon separated)
lines = s.split(seprexp);
// for each region or cmd
for(i=0; i= 2 &&
obj.shape !== "line" &&
obj.shape !== "polygon" ){
// get image position
$.extend(obj, getipos(robj.args[0], robj.args[1]));
}
// if textOpts has ra, dec, save the wcssys, it may be
// different by the time textOpts gets processed
if( obj.textOpts &&
obj.textOpts.ra !== undefined &&
obj.textOpts.dec !== undefined ){
obj.textOpts.\_wcssys = wcssys;
}
// region args are optional
switch(robj.cmd){
case "annulus":
if( alen > 0 ){
obj.radii = [];
for(j=2; j= 3 ){
obj.width = getilen(robj.args[2], 1);
}
if( alen >= 4 ){
obj.height = getilen(robj.args[3], 2);
}
if( alen >= 5 ){
obj.angle = getang(robj.args[4]);
}
break;
case "circle":
if( alen >= 3 ){
obj.radius = getilen(robj.args[2], 1);
}
break;
case "ellipse":
if( alen >= 3 ){
obj.r1 = getilen(robj.args[2], 1);
}
if( alen >= 4 ){
obj.r2 = getilen(robj.args[3], 2);
}
if( alen >= 5 ){
obj.angle = getang(robj.args[4]);
}
break;
case "line":
case "polygon":
if( alen > 0 ){
obj.pts = [];
for(j=0, k=0; j= 3 ){
obj.text = getstr(robj.args[2]);
}
if( alen >= 4 ){
obj.angle = getang(robj.args[3]);
}
break;
default:
break;
}
// comment contains the tags
if( robj.comment ){
obj.tags = robj.comment;
}
// save this region
regions.push(obj);
} else {
// if its a wcs command
if( robj.cmd.match(wcsrexp) ){
// reset the wcs system
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
this.setWCSSys(robj.cmd, false);
JS9.globalOpts.xeqPlugins = txeq;
// get new wcssys
wcssys = this.getWCSSys();
// is this a real wcs?
iswcs = JS9.isWCSSys(wcssys);
} else if( robj.cmd === "remove" || robj.cmd === "delete" ){
regions.push({remove: true});
}
}
}
}
// restore original wcs
txeq = JS9.globalOpts.xeqPlugins;
JS9.globalOpts.xeqPlugins = false;
this.setWCSSys(owcssys, false);
this.setWCSUnits(owcsunits);
JS9.globalOpts.xeqPlugins = txeq;
// return the generated object
return regions;
};
// save regions to a file
JS9.Regions.saveRegions = function(fname, which, layer){
let i, s, t, header, regstr, format, blob, opts, arr, rid;
// see if default type is implicit in the output file
if( fname ){
arr = fname.match(/\.([^.]\*)$/);
if( arr && arr[1] && arr[1].match(/^(reg|svg|csv)$/) ){
format = arr[1];
}
}
// layer can be a layer name or an object describing layer, output type
if( typeof layer === "object" ){
opts = layer;
layer = null;
} else if( layer && typeof layer === "string" ){
try{ opts = JSON.parse(layer); }
catch(e){ opts = null; }
if( opts ){ layer = null; }
}
// see if parameters are in the opts object
if( opts ){
// layer name
if( JS9.notNull(opts.layer) ){
layer = opts.layer;
}
// old style 'type' property is now ...
if( JS9.notNull(opts.type) ){
format = opts.type ;
}
// ... format
if( JS9.notNull(opts.format) ){
format = opts.format ;
}
}
// make sure we have an opts
opts = opts || {};
// last chance ... use defaults
layer = layer || "regions";
format = format || "reg";
// and make a sanity check
if( !this.layers[layer] ){
JS9.error(`can't find layer for saveRegions: ${layer}`);
}
// construct final output file name, if necessary
if( !fname ){
if( layer !== "regions" ){
fname = `js9\_${layer}.${format}`;
} else {
fname = `js9.${format}`;
}
}
// generate the specified output
switch(format){
case "svg":
// convert layer to svg
try{
// add border box, if necessary
if( JS9.globalOpts.svgBorder ){
rid = this.addShapes(layer, "box",
{left: this.rgb.img.width/2,
top: this.rgb.img.height/2,
width: this.rgb.img.width,
height: this.rgb.img.height,
color: "black",
strokeWidth: 1,
tags: "SVGBorder"
});
}
// convert canvas to SVG
s = this.layers[layer].dlayer.canvas.toSVG();
// remove border box, if necessary
if( JS9.globalOpts.svgBorder ){
this.removeShapes(layer, rid);
}
}
catch(e){ JS9.error(`can't convert layer to SVG: ${layer}`);}
break;
case "csv":
// convert layer to region string
try{
opts.mode = 1;
opts.file = fname;
// when saving csv, we might want to include the wcs info
if( JS9.isNull(opts.includewcs) ){
opts.includewcs = JS9.globalOpts.csvIncludeWCS;
}
// when saving reg, we might want to exclude the dcoord shapes
if( JS9.isNull(opts.savedcoords) ){
opts.includedcoords = JS9.globalOpts.regSaveDCoords;
}
// list of regions
regstr = this.listRegions(which, opts, layer);
// convert to csv
arr = regstr.split(";");
for(i=0, s=""; ii.trim());
}
if( !$.isArray(remtags) ){
remtags = remtags.split(",").map(i=>i.trim());
}
s = this.getShapes("regions", which);
// for each shape ...
for(i=0; i background, include <-> exclude
// e.g. im.toggleRegionTags("selected", "source", "background");
// call using image context
JS9.Regions.toggleRegionTags = function(which, x1, x2){
let i, j, s, tags, xnew;
which = which || "all";
s = this.getShapes("regions", which);
for(i=0; i {
let i, x, y;
if( !ann.text ){
return null;
}
x = ann.x || 0;
if( ann.y.toUpperCase() === "%Y" ){
for(i=1; i x ){
y = Math.max(data[i-1][1], data[i][1], data[i+1][1]);
break;
}
}
} else {
y = ann.y;
}
return {x, y};
};
switch( JS9.globalOpts.plotLibrary ){
case "flot":
yTextOffset = -25;
divjq.find(".plotAnnotation").remove();
for(i=0; i divjq.width()) ){
continue;
}
ahtml = sprintf("

%s

",
ao.left, ao.top+yTextOffset,
ac, `↓${ann.text}`);
divjq.append(ahtml);
}
break;
case "plotly":
yTextOffset = -30;
for(i=0; i {
if( val === undefined ){
return undefined;
}
if( (typeof val === "number") && (val % 1 !== 0) ){
val = Math.round((val + 0.001) \* 100) / 100;
}
return(String(val));
};
// sanity check
if( !plot || !pobj ){ return; }
// convenience variables
winid = plot.winid;
wid = $(winid).attr("id");
form = `#${wid} #plotConfigForm `;
// flot support only for now ...
if( JS9.globalOpts.plotLibrary !== "flot" ){ return; }
// fill in the values from the plot
$(`${form}.val`).each((index, element) => {
val = "";
key = $(element).attr("name");
// key-specific pre-processing
switch(key){
case "xscale":
if( JS9.notNull(pobj.curscale.x) ){
val = fmt(pobj.curscale.x);
}
break;
case "xmin":
if( JS9.notNull(plot.getAxes().xaxis.options.min) ){
val = fmt(plot.getAxes().xaxis.options.min);
}
break;
case "xmax":
if( JS9.notNull(plot.getAxes().xaxis.options.max) ){
val = fmt(plot.getAxes().xaxis.options.max);
}
break;
case "yscale":
if( JS9.notNull(pobj.curscale.y) ){
val = fmt(pobj.curscale.y);
}
break;
case "ymin":
if( JS9.notNull(plot.getAxes().yaxis.options.min) ){
val = fmt(plot.getAxes().yaxis.options.min);
}
break;
case "ymax":
if( JS9.notNull(plot.getAxes().yaxis.options.max) ){
val = fmt(plot.getAxes().yaxis.options.max);
}
break;
default:
break;
}
$(element).val(val);
});
// save the image for later processing
$(form).data("im", this);
// save the plot object for later processing
$(form).data("plot", plot);
// save the plot opts object for later processing
$(form).data("pobj", pobj);
// save the window id for later processing
$(form).data("winid", winid);
// add tooltip callbacks (not mobile: ios buttons stop working!)
if( !$(form).data("tooltipInit") ){
$(form).data("tooltipInit", true);
if( JS9.BROWSER[3] ){
mover = "touchstart";
mout = "touchend";
} else {
mover = "mouseover";
mout = "mouseout";
}
$(".plotcol\_P").on(mover, (e) => {
let title;
const target = e.currentTarget;
const tooltip = $(target).find("input").data("tooltip");
const el = $(target)
.closest(JS9.lightOpts[JS9.LIGHTWIN].top)
.find(JS9.lightOpts[JS9.LIGHTWIN].dragBar);
if( tooltip && el.length ){
// change title: see dhtmlwindow.js load() @line 130
title = `${JS9.Plot.opts.title}: ${tooltip}`;
$(el)[0].childNodes[0].nodeValue = title;
}
});
$(".plotcol\_P").on(mout, (e) => {
const target = e.currentTarget;
const el = $(target)
.closest(JS9.lightOpts[JS9.LIGHTWIN].top)
.find(JS9.lightOpts[JS9.LIGHTWIN].dragBar);
if( el.length ){
$(el)[0].childNodes[0].nodeValue = JS9.Plot.opts.title;
}
});
}
};
// process the plot config form: called with the image context
// eslint-disable-next-line no-unused-vars
JS9.Plot.processConfigForm = function(form, plot, pobj, arr){
let i, key, val;
const alen = arr.length;
// sanity check
switch( JS9.globalOpts.plotLibrary ){
case "flot":
break;
case "plotly":
return;
}
// process array of keyword/values
for(i=0; i we were way off scale
try{ s = JS9.wcs2pix(cim.raw.wcs, ra, dec); }
catch(e){ s = null; }
if( s ){
arr = s.trim().split(/\s+/);
x = parseFloat(arr[0]);
y = parseFloat(arr[1]);
// if image pos is within the image boundaries ...
if( x > 0 && x < w && y > 0 && y < h ){
// draw the crosshair, centered on the image pos
hopts = {pts: [{x: 0, y: y}, {x: w, y: y}],
redraw:false};
cim.changeShapes(layername, cim.crosshair.h, hopts);
vopts = {pts: [{x: x, y: 0}, {x: x, y: h}],
redraw: true};
cim.changeShapes(layername, cim.crosshair.v, vopts);
cim.crosshair.visible = true;
}
}
}
}
}
};
// hide: move the crosshair out of the display
// eslint-disable-next-line no-unused-vars
JS9.Crosshair.hide = function(im, ipos, evt){
const layername = JS9.Crosshair.LAYERNAME;
const opts = JS9.Crosshair.opts.hiddenPts;
// sanity check
if( !im ){ return; }
// if the crosshair is visible ...
if( (im.crosshair && im.crosshair.visible) ||
im.tmp.arrowCrosshairVisible ){
// move it off the display
im.changeShapes(layername, im.crosshair.h, opts);
im.changeShapes(layername, im.crosshair.v, opts);
im.crosshair.visible = false;
delete im.tmp.arrowCrosshairVisible;
}
};
// image load: create the cross hair for this image
JS9.Crosshair.create = function(im){
const opts = JS9.Crosshair.opts.hiddenPts;
const layername = JS9.Crosshair.LAYERNAME;
// sanity check
if( !im ){ return; }
if( !im.crosshair ){
// create the crosshair object for this image
im.crosshair = {};
// create the crosshair, but don't display it yet
im.crosshair.h = im.addShapes(layername, "line", opts);
im.crosshair.v = im.addShapes(layername, "line", opts);
im.crosshair.visible = false;
}
};
// mark key actions which use the shift key
JS9.Crosshair.keyaction = function(im, ipos, evt){
if( im && evt && evt.shiftKey ){
im.tmp.shiftKey = true;
}
};
// unmark key action-based shift key use
JS9.Crosshair.keyup = function(im, ipos, evt){
// remove shiftKey marker, if necessary
if( im && im.tmp.shiftKey && evt && !evt.shiftKey ){
delete im.tmp.shiftKey;
}
};
// init: create the shape layer for this display
JS9.Crosshair.init = function(){
let i;
const layername = JS9.Crosshair.LAYERNAME;
// init the crosshair shape layer, but only once per display
for(i=0; i 1 ){
tscale = 10;
} else if( trange > 0.1 ){
tscale = 100;
} else if( trange > 0.01 ){
tscale = 1000;
} else if( trange > 0.001 ){
tscale = 10000;
} else if( trange > 0.0001 ){
tscale = 100000;
} else {
tscale = 1000000;
}
out0 = Math.floor(in0 \* tscale) / tscale;
out1 = Math.ceil(in1 \* tscale) / tscale;
outinc = Math.ceil(((out1 - out0) / n) \* tscale) / tscale;
return {lo: out0, hi: out1, inc: outinc};
};
// generate label value
JS9.Grid.getLabel = function(opts, v, which){
let i, t, idx, arr;
let doall = false;
switch(opts.wcsunits){
case "sexagesimal":
if( (which === "ra") &&
((opts.wcssys !== "galactic") && (opts.wcssys !== "ecliptic")) ){
v /= 15.0;
}
t = JS9.saodtostr(v, ":", opts.sexaPrec);
arr = t.split(":");
if( opts.last[which] ){
t = "";
for(i=0; i= -opts.margin && x <= raw.width + opts.margin &&
y >= -opts.margin && y <= raw.height + opts.margin ){
t += String(`${x + 1},${y}${1}, `);
n++;
if( lineloc === 0 ){
lineloc = 1;
if( dec < xdeclim ){
inc = xdecinc;
}
} else if( lineloc === 1 ){
if( dec > xdeclim ){
lineloc = 2;
inc = xdecinc0;
}
}
} else {
if( lineloc === 1 ){
lineloc = 2;
dec = dec - inc;
inc = xdecinc0;
}
}
}
}
if( n > 1 ){
s += t.replace(/,\s+$/, ") ");
s += ` {"color": "${opts.lineColor}"};`;
}
}
// lines of constant Dec
for(dec=dec0; dec<=dec1; dec=dec+decinc){
t = "line(";
inc = xrainc0;
lineloc = 0;
n = 0;
for(ra=ra0; ra<=ra1; ra=ra+inc){
arr = JS9.wcs2pix(raw.wcs, ra, dec).trim().split(/ +/);
if( arr && arr.length ){
x = parseFloat(arr[0]);
y = parseFloat(arr[1]);
if( x >= -opts.margin && x <= raw.width + opts.margin &&
y >= -opts.margin && y <= raw.height + opts.margin ){
t += String(`${x + 1},${y}${1}, `);
n++;
if( lineloc === 0 ){
lineloc = 1;
if( ra < xralim ){
inc = xrainc;
}
} else if( lineloc === 1 ){
if( ra > xralim ){
lineloc = 2;
inc = xrainc0;
}
}
} else {
if( lineloc === 1 ){
lineloc = 2;
ra = ra - inc;
inc = xrainc0;
}
}
}
}
if( n > 1 ){
s += t.replace(/,\s+$/, ") ");
s += ` {"color": "${opts.lineColor}"};`;
}
}
// dec labels along constant ra line
decoffx = opts.labelDecOffx / this.rgb.sect.zoom;
decoffy = opts.labelDecOffy / this.rgb.sect.zoom;
decskip = 0;
lastra = ra0;
for(ra=ra0, got=0; ra<=ra1; ra=ra+rainc){
for(dec=dec0; dec<=dec1; dec=dec+decinc){
arr = JS9.wcs2pix(raw.wcs, ra, dec).trim().split(/ +/);
if( arr && arr.length ){
x = parseFloat(arr[0]);
y = parseFloat(arr[1]);
dpos = this.imageToDisplayPos({x, y});
if( dpos.x > (this.ix+opts.labelMargin) && dpos.x < (this.rgb.img.width+this.ix-opts.labelMargin) &&
dpos.y > (this.iy+opts.labelMargin) && dpos.y < (this.rgb.img.height+this.iy-opts.labelMargin)){
if( decskip >= opts.decSkip ){
s += sprintf('text(%s,%s,%s,%s) {"color":"%s", "fontFamily":"%s", "fontSize":%s, "fontStyle":"%s", "fontWeight":"%s", "originX":"left", "originY":"top"};',
x + decoffx, y + decoffy,
JS9.Grid.getLabel.call(this, opts, dec, "dec"),
opts.decAngle,
opts.labelColor,
opts.labelFontFamily,
opts.labelFontSize,
opts.labelFontStyle,
opts.labelFontWeight);
got++;
} else {
if( ra !== lastra ){
decskip++;
}
lastra = ra;
}
}
}
}
if( got ){
break;
}
}
// ra labels along constant dec line
raoffx = opts.labelRAOffx / this.rgb.sect.zoom;
raoffy = opts.labelRAOffy / this.rgb.sect.zoom;
raskip = 0;
lastdec = dec0;
for(dec=dec0, got=0; dec<=dec1; dec=dec+decinc){
for(ra=ra0; ra<=ra1; ra=ra+rainc){
arr = JS9.wcs2pix(raw.wcs, ra, dec).trim().split(/ +/);
if( arr && arr.length ){
x = parseFloat(arr[0]);
y = parseFloat(arr[1]);
dpos = this.imageToDisplayPos({x, y});
if( dpos.x > (this.ix+opts.labelMargin) && dpos.x < (this.rgb.img.width+this.ix-opts.labelMargin) &&
dpos.y > (this.iy+opts.labelMargin) && dpos.y < (this.rgb.img.height+this.iy-opts.labelMargin)){
if( raskip >= opts.raSkip ){
s += sprintf('text(%s,%s,%s,%s) {"color":"%s", "fontFamily":"%s", "fontSize":%s, "fontStyle":"%s", "fontWeight":"%s", "originX":"left", "originY":"top"};',
x + raoffx, y + raoffy,
JS9.Grid.getLabel.call(this, opts, ra, "ra"),
opts.raAngle,
opts.labelColor,
opts.labelFontFamily,
opts.labelFontSize,
opts.labelFontStyle,
opts.labelFontWeight);
got++;
} else {
if( dec !== lastdec ){
raskip++;
}
lastdec = dec;
}
}
}
}
if( got ){
break;
}
}
// add the grid shapes
this.addShapes(JS9.Grid.LAYERNAME, s, opts);
// grid is complete and active
this.tmp.gridStatus = "active";
};
// toggle grid on/off
JS9.Grid.toggle = function(im){
// sanity check
if( !im ){ return; }
// toggle display
switch(im.tmp.gridStatus){
case undefined:
case null:
case "inactive":
// start afresh
im.displayCoordGrid(true);
break;
case "active":
// clear the grid
im.displayCoordGrid(false);
break;
case "processing":
default:
break;
}
};
// display grid, as needed
JS9.Grid.regrid = function(im){
if( im ){
// ignore if grid is not active or the image is not loaded
if( im.tmp.gridStatus !== "active" || im.status.load !== "complete" ){
return;
}
// redraw the grid
im.displayCoordGrid(true);
}
};
// plugin init: load our grid methods
// eslint-disable-next-line no-unused-vars
JS9.Grid.init = function(opts){
let dlayer;
opts = $.extend(true, {}, JS9.Catalogs.opts, JS9.Grid.opts, opts);
// init the display shape layer
dlayer = this.display.newShapeLayer(JS9.Grid.LAYERNAME, opts);
// mouse up: no-op
dlayer.canvas.on("mouse:up", () => {
return false;
});
};
// add to image prototypes
JS9.Image.prototype.displayCoordGrid = JS9.Grid.display;
// check if an object is an image handle
JS9.isImage = function(s){
if( typeof s === "object" &&
JS9.notNull(s.id) &&
JS9.notNull(s.raw) &&
JS9.notNull(s.rgb) &&
JS9.notNull(s.params) &&
JS9.notNull(s.display) ){
return true;
} if( typeof s === "string" && JS9.lookupImage(s) ){
return true;
}
return false;
};
// ---------------------------------------------------------------------
// Dysel: callbacks when a display is selected dynamically
// ---------------------------------------------------------------------
JS9.Dysel = {};
JS9.Dysel.CLASS = "JS9";
JS9.Dysel.NAME = "Dysel";
JS9.Dysel.display = null;
JS9.Dysel.plugins = [];
// plugin init: no op
// eslint-disable-next-line no-unused-vars
JS9.Dysel.init = function(opts){
return;
};
// unhighlight current selection
JS9.Dysel.unhighlightSelection = function(){
if( JS9.bugs.webkit\_resize ){
$(".JS9").find(".JS9Image").removeClass("JS9Highlight");
} else {
$(".JS9").removeClass("JS9Highlight");
}
};
// highlight display when dynamic selection is made
JS9.Dysel.highlightSelection = function(im){
let disp;
// sanity check
if( !im || !JS9.Dysel.retrievePlugins().length ){ return; }
// optimization: no processing if we only have one display
if( JS9.displays.length === 1 ){ return; }
// unhighlight all
JS9.Dysel.unhighlightSelection();
// the display to highlight
disp = im.display;
// highlight selected
if( JS9.bugs.webkit\_resize ){
$(disp.divjq).find(".JS9Image").addClass("JS9Highlight");
} else {
$(disp.divjq).addClass("JS9Highlight");
}
};
// add to dynamic selection array
JS9.Dysel.addPlugins = function(plugin){
JS9.Dysel.plugins.push(plugin);
};
// get dynamic selection array
JS9.Dysel.retrievePlugins = function(){
return JS9.Dysel.plugins;
};
// return current dynamically selected display
JS9.Dysel.getDisplay = function(which){
if( !JS9.Dysel.retrievePlugins().length ){
return null;
}
if( which === "previous" ){
return JS9.Dysel.odisplay;
}
return JS9.Dysel.display;
};
// return the display object associated with the current dynamic selection
// or else a default value
JS9.Dysel.getDisplayOr = function(def){
if( def === "previous" ){
return JS9.Dysel.getDisplay(def);
}
return JS9.Dysel.getDisplay() || def;
};
// set current dynamically selected display
JS9.Dysel.select = function(display){
// sanity check
if( !display || !JS9.Dysel.retrievePlugins().length ){ return; }
// save old display
JS9.Dysel.odisplay = JS9.Dysel.display;
// set new display
JS9.Dysel.display = display;
if( display.image ){
JS9.Dysel.highlightSelection(display.image);
// plugin callbacks for selected display
display.image.xeqPlugins("image", "ondynamicselect", null);
}
};
// imageload: select the display
JS9.Dysel.imageload = function(im){
if( im ){
JS9.Dysel.select(im.display);
}
};
// imageclose: select another display, if necessary
JS9.Dysel.imageclose = function(im){
let i, got, disp;
if( im ){
disp = JS9.Dysel.getDisplay();
if( !disp || disp.image !== im ){
return;
}
// if this the last image in this display?
for(i=0, got=0; i>> 0;
// 3. If len is 0, return false.
if (len === 0) {
return false;
}
// 4. Let n be ? ToInteger(fromIndex).
// (If fromIndex is undefined, this step produces the value 0.)
var n = fromIndex | 0;
// 5. If n ≥ 0, then
// a. Let k be n.
// 6. Else n < 0,
// a. Let k be len + n.
// b. If k < 0, let k be 0.
var k = Math.max(n >= 0 ? n : len - Math.abs(n), 0);
function sameValueZero(x, y) {
return x === y || (typeof x === "number" && typeof y === "number" && isNaN(x) && isNaN(y));
}
// 7. Repeat, while k < len
while (k < len) {
// a. Let elementK be the result of ? Get(O, ! ToString(k)).
// b. If SameValueZero(searchElement, elementK) is true, return true.
// c. Increase k by 1.
if (sameValueZero(o[k], searchElement)) {
return true;
}
k++;
}
// 8. Return false
return false;
}
});
}
// make a copy of the raw data
// used by setFlip and setRot90
JS9.getRawCopy = function(oraw, bitpix){
// make copy
let nraw = $.extend(true, {}, oraw);
nraw.bitpix = bitpix || oraw.bitpix;
switch(nraw.bitpix){
case 8:
nraw.data = new Uint8Array(oraw.data);
break;
case 16:
nraw.data = new Int16Array(oraw.data);
break;
case -16:
nraw.data = new Uint16Array(oraw.data);
break;
case 32:
nraw.data = new Int32Array(oraw.data);
break;
case -32:
nraw.data = new Float32Array(oraw.data);
break;
case -64:
nraw.data = new Float64Array(oraw.data);
break;
default:
JS9.error(`unsupported bitpix: ${nraw.bitpix}`);
break;
}
return nraw;
};
// extract line from raw data
// used by setFlip and setRot90
JS9.getRawLine = function(oraw, ooff, nraw, noff){
let obuf, nbuf;
switch(oraw.bitpix){
case 8:
obuf = new Uint8Array(oraw.data.buffer, ooff, oraw.width);
nbuf = new Uint8Array(nraw.data.buffer, noff, oraw.width);
break;
case 16:
case -16:
obuf = new Uint16Array(oraw.data.buffer, ooff, oraw.width);
nbuf = new Uint16Array(nraw.data.buffer, noff, oraw.width);
break;
case 32:
obuf = new Uint32Array(oraw.data.buffer, ooff, oraw.width);
nbuf = new Uint32Array(nraw.data.buffer, noff, oraw.width);
break;
case -32:
obuf = new Float32Array(oraw.data.buffer, ooff, oraw.width);
nbuf = new Float32Array(nraw.data.buffer, noff, oraw.width);
break;
case -64:
obuf = new Float64Array(oraw.data.buffer, ooff, oraw.width);
nbuf = new Float64Array(nraw.data.buffer, noff, oraw.width);
break;
default:
JS9.error(`unsupported bitpix: ${oraw.bitpix}`);
break;
}
return [obuf, nbuf];
};
// https://www.html5rocks.com/en/tutorials/webgl/typed\_arrays/
JS9.memcpy = function(dst, dstOffset, src, srcOffset, length){
var dstU8 = new Uint8Array(dst, dstOffset, length);
var srcU8 = new Uint8Array(src, srcOffset, length);
dstU8.set(srcU8);
};
// set explicit focus for IPython/Jupyter support
JS9.jupyterFocus = function(el, el2){
let eljq;
if( {}.hasOwnProperty.call(window, "Jupyter") ){
if( el instanceof jQuery ){
eljq = el;
} else {
eljq = $(el);
}
el2 = el2 || "input, textarea";
eljq.find(el2).each((index, element) => {
Jupyter.keyboard\_manager.register\_events($(element));
});
}
};
// return a unique value for a given image id by appending  to the id
JS9.getImageID = function(imid, dispid, myim){
let i, im, s;
let ids = 0;
let idmax = 1;
const imlen = JS9.images.length;
const rexp = /.\*<([0-9][0-9]\*)>$/;
const rexp2 = /<[0-9][0-9]\*>/;
imid = JS9.cleanPath(imid.replace(rexp2, ""), "id");
for(i=0; i= 0 ){
s = im.id.replace(rexp, "$1");
idmax = Math.max(idmax, parseInt(s, 10));
}
ids++;
}
}
}
if( ids ){
return `${imid}<${String(idmax+1)}>`;
}
return imid;
};
// return a unique value for ids
JS9.uniqueID = (function(){
let id = 1; // initial value
return function(){
return id++;
};
}());
// change cursor to waiting/not waiting
JS9.waiting = function(mode, display){
let el, opts, tdisp;
switch(mode){
case true:
if( {}.hasOwnProperty.call(window, "Spinner") &&
(JS9.globalOpts.waitType === "spinner") ){
if( display ){
if( typeof display === "object" ){
el = display.divjq[0];
} else if( typeof display === "string" ){
tdisp = JS9.lookupDisplay(display);
if( tdisp ){
el = tdisp.divjq[0];
}
}
}
if( !el ){
el = $("body").get(0);
}
if( !JS9.spinner ){
JS9.spinner = {};
opts = {color: JS9.globalOpts.spinColor,
opacity: JS9.globalOpts.spinOpacity};
JS9.spinner.spinner = new Spinner(opts);
}
JS9.spinner.spinner.spin(el);
} else {
$("body").addClass("waiting");
}
break;
case false:
if( {}.hasOwnProperty.call(window, "Spinner") &&
(JS9.globalOpts.waitType === "spinner") ){
if( JS9.spinner ){
JS9.spinner.spinner.stop();
}
} else {
$("body").removeClass("waiting");
}
break;
}
};
// display a progress bar
JS9.progress = function(arg1, arg2){
if( (typeof arg1 === "boolean") || (typeof arg1 === "string") ){
switch(arg1){
case true:
case "indeterminate":
if( arg2 ){
JS9.progress.display = arg2;
JS9.progress.display.displayMessage("progress", arg1);
}
break;
case false:
case "":
if( JS9.progress.display ){
JS9.progress.display.clearMessage("progress");
delete JS9.progress.display;
}
break;
}
} else if( typeof arg1 === "number" ){
if( JS9.progress.display ){
JS9.progress.display.displayMessage("progress", [arg1, arg2]);
}
}
};
// msg coming from socket.io or postMessage
JS9.msgHandler = function(msg, cb){
let i, s, obj, tdisp, res, dobj;
let args = [];
const cmd = msg.cmd;
const id = msg.id;
const oalerts = JS9.globalOpts.alerts;
const rstr = JS9.globalOpts.quietReturn ? "" : "OK";
const getDisplayObject = (id, args) => {
if( id ){
// bash sends a string, not an object
if( args.length > 0 ){
s = args[args.length-1];
if( typeof s === "string" ){
try{ obj = JSON.parse(s); }
catch(e){ obj = null; }
} else if( typeof s === "object" ){
obj = s;
}
// is this the display object? see JS9.parsePublicArgs
if( obj &&
(typeof obj === "object") &&
{}.hasOwnProperty.call(obj, "display") &&
(Object.keys(obj).length === 1) ){
// remove the current display object
args.pop();
// return the new one
return obj;
} else {
return {display: id};
}
} else {
return {display: id};
}
}
return null;
};
// turn off alerts
if( cb ){
JS9.globalOpts.alerts = false;
}
// look for a public API call
if( JS9.publics[cmd] ){
// check for non-array first arg
if( !$.isArray(msg.args) ){
msg.args = [msg.args];
}
// change empty quoted strings to empty strings
for(i=0; i {
rval.close();
})
.on("touchend", (e) => {
const curtime = (new Date()).getTime();
const lasttime = $(e.currentTarget).data("lasttime");
if( lasttime &&
(curtime - lasttime) > JS9.DBLCLICK0 &&
(curtime - lasttime) < JS9.DBLCLICK ){
rval.close();
}
$(e.currentTarget).data("lasttime", curtime);
});
// if ios user failed to close the window via the close button,
// give a hint (once per session only!)
$(`#${id} ${JS9.lightOpts[JS9.LIGHTWIN].dragBar}`)
.on("touchend", () => {
// skip check if we are dragging
if( !dhtmlwindow.distancex && !dhtmlwindow.distancey ){
if( JS9.lightOpts.nclick >= 2 ){
alert("trouble closing this window? double-tap the window handle");
JS9.lightOpts.nclick = -1;
} else {
if( JS9.lightOpts.nclick >= 0 ){
JS9.lightOpts.nclick++;
}
}
} else {
if( JS9.lightOpts.nclick > 0 ){
JS9.lightOpts.nclick = 0;
}
}
});
break;
default:
break;
}
return rval;
};
// wrapper for new func to avoid jslint errors
JS9.checkNew = function(obj){
if( !obj ){
JS9.error("internal failure in a JS9 constructor");
}
};
// desperate attempt to regularize the control/meta key
JS9.specialKey = function(e){
return (e.metaKey || e.ctrlKey);
};
// desperate attempt to regularize the stracktrace message
JS9.strace = function(e){
let s = "";
if( JS9.DEBUG > 1 ){
s = e.stack || e.stacktrace || "";
}
return s;
};
// try to make a nice string from a float
// ints remain ints, floats get truncated at 6 significant digits
JS9.floatToString = function(fval){
if( typeof fval === "number" ){
return sprintf("%g",
parseFloat(fval.toFixed(JS9.globalOpts.floatPrecision)));
} else if( typeof fval === "string" ){
return fval;
} else {
return String(fval);
}
};
// figure out precision from range of values (used by colorbar)
// from: /tksao1.0/colorbar/colorbarbase.C
JS9.floatPrecision = function(fval1, fval2){
let prec;
let aa = Math.floor(Math.log10(Math.abs(fval1)));
let bb = Math.floor(Math.log10(Math.abs(fval2)));
// not sure why prec is set to 1 in the else clause so ...
// if( aa !== bb ){
// prec = aa > bb ? aa : bb;
// } else {
// prec = 1;
// }
prec = Math.max(aa, bb);
return prec;
};
// convert float value to a string with decent precision
// from: /tksao1.0/colorbar/colorbarbase.C
JS9.floatFormattedString = function(fval, prec, jj){
let fmt;
let s = "";
if( fval === undefined ){
return s;
}
if( prec < -2 ){
fmt = `%.${String(2+jj)}e`;
s = sprintf(fmt, fval);
} else if( prec < 0 ){
s = fval.toFixed(Math.abs(prec)+3+jj);
} else if( prec < 2 ){
fmt = `%.${String(prec+jj)}f`;
s = sprintf(fmt, fval);
} else if( prec < 5 ){
s = fval.toFixed(0+jj);
} else {
fmt = `%.${String(2+jj)}e`;
s = sprintf(fmt, fval);
}
return s;
};
// get center of bounding box surrounding a polygon
JS9.centerPolygon = function(points){
let i, plen, minx, maxx, miny, maxy;
// sanity check
if( !points || !points.length ){ return; }
plen = points.length;
for(i=0; i maxx) ){
maxx = points[i].x;
}
if( (miny === undefined) || (points[i].y < miny) ){
miny = points[i].y;
}
if( (maxy === undefined) || (points[i].y > maxy) ){
maxy = points[i].y;
}
}
return {x: (minx + maxx) / 2.0, y: (miny + maxy) / 2.0};
};
// calculate centroid for a polygon
// wont work for self-intersecting polygons but it's all I do right now!
// adapted from: http://en.wikipedia.org/wiki/Centroid
JS9.centroidPolygon = function(points, doaverage){
let i, plen, factor, area, cx, cy;
let parta = 0;
let partx = 0;
let party = 0;
let totx = 0;
let toty = 0;
const pts = [];
// sanity check
if( !points || !points.length ){ return; }
// get points
plen = points.length;
// just average the points?
if( doaverage ){
for(i=0; i 0 ){
did = im.display.id;
if( !display ||
(typeof display === "string" && display === did) ||
(typeof display === "object" && display.id === did) ){
return im;
}
}
}
}
return null;
};
// return the display for the specified id
// id can be a display object or an id from a display object
JS9.lookupDisplay = function(id, mustExist){
let i;
const regexp = new RegExp(`[-\_]?(${JS9.PLUGINS})$`);
// default is the id must exist
if( mustExist === undefined ){
mustExist = true;
}
// lookup id
if( id && (id.toString().search(JS9.SUPERMENU) < 0) ){
// look for whole id
for(i=0; i {
let blob;
if( xhr.readyState === 4 ){
if( xhr.status === 200 || xhr.status === 0 ){
// delete fetch status so JS9.error() does not process it
delete JS9.fetchURL.status;
if( xhr.responseType === "blob" ){
blob = new Blob([xhr.response]);
// discard path (or scheme) up to slashes
// remove trailing ? params
if( name.match("://") ){
blob.name = name.split("/").reverse()[0]
.replace(/\?.\*$/, "");
} else {
blob.name = name;
}
// hack for Google Drive's lack of a filename
if( blob.name === "uc" ){
blob.name = `google\_${JS9.uniqueID()}.fits`;
}
if( handler ){
handler(blob, opts);
} else {
JS9.Load(blob, opts);
}
} else {
if( opts.display ){
handler(xhr.response, opts, {display: opts.display});
} else {
handler(xhr.response, opts);
}
}
} else if( xhr.status === 404 ){
JS9.error(`could not find ${url}`);
} else {
JS9.error(`can't load: ${url} ${xhr.statusText} ${xhr.status}`);
}
}
};
xhr.onerror = () => {
JS9.error(`cannot load: ${url} ... please check the url/pathname`);
};
xhr.ontimeout = () => {
JS9.error(`timeout awaiting response from server: ${url}`);
};
// hack: set fetch status for JS9.error() to sense and pass on
// this will be picked up by getStatus("load")
JS9.fetchURL.status = "processing";
// fetch the data!
try{ xhr.send(); }
catch(e){ JS9.error(`request to load ${url} failed`, e); }
};
// JS9 wrapper around saveAs:
// deal with pathnames in Electron desktop app
JS9.saveAs = function(blob, pathname){
let dirmatch, dirname, basename;
if( window.electron ){
dirmatch = pathname.match(/.\*\//);
// if a directory was specified ...
if( dirmatch && dirmatch[0] ){
// ... change save directory in Electron before save
dirname = dirmatch[0];
JS9.SaveDir(dirname, {onceOnly: true});
}
// get basename
basename = pathname.split('/').reverse()[0];
// wait a bit for ipc to finish, then save
window.setTimeout(() => {
// save basename in current save directory
try{ saveAs(blob, basename); }
catch(e){ JS9.error("could not saveAs", e); }
}, JS9.TIMEOUT);
} else {
// non-Electron (or no path): just save filename
try{ saveAs(blob, pathname); }
catch(e){ JS9.error("could not saveAs", e); }
}
}
// configure or return the fits library
JS9.fitsLibrary = function(s){
let t;
if( !s ){
return JS9.fits.name;
}
t = s.toLowerCase();
switch(t){
case "astroem":
case "cfitsio":
JS9.fits = Astroem;
// set up default options
JS9.fits.options = JS9.fits.options || {};
JS9.fits.options.handler = JS9.NewFitsImage;
JS9.fits.options.error = JS9.error;
if( JS9.userOpts.fits ){
JS9.fits.options.extlist = JS9.userOpts.fits.extlist;
JS9.fits.options.table = {
xdim: JS9.userOpts.fits.xdim,
ydim: JS9.userOpts.fits.ydim,
bin: JS9.userOpts.fits.bin || 1
};
JS9.fits.options.image = {
xdim: JS9.userOpts.fits.ixdim || JS9.userOpts.fits.xmax,
ydim: JS9.userOpts.fits.iydim || JS9.userOpts.fits.ymax,
bin: JS9.userOpts.fits.ibin || 1
};
} else {
JS9.fits.options.extlist = JS9.globalOpts.extlist;
JS9.fits.options.table = {bin: (JS9.globalOpts.table.bin || 1)};
// NB: dims are deprecated 11/27/16
if( JS9.notNull(JS9.globalOpts.table.xdim) ){
JS9.fits.options.table.xdim = JS9.globalOpts.table.xdim;
} else if( JS9.notNull(JS9.globalOpts.dims) ){
JS9.fits.options.table.xdim = JS9.globalOpts.dims[0];
}
if( JS9.notNull(JS9.globalOpts.table.ydim) ){
JS9.fits.options.table.ydim = JS9.globalOpts.table.ydim;
} else if( JS9.notNull(JS9.globalOpts.dims) ){
JS9.fits.options.table.ydim = JS9.globalOpts.dims[1];
}
JS9.fits.options.image = {bin: (JS9.globalOpts.image.bin || 1)};
if( JS9.notNull(JS9.globalOpts.image.xdim) ){
JS9.fits.options.image.xdim = JS9.globalOpts.image.xdim;
} else if( JS9.notNull(JS9.globalOpts.xmax) ){
JS9.fits.options.image.xdim = JS9.globalOpts.xmax;
}
if( JS9.notNull(JS9.globalOpts.image.ydim) ){
JS9.fits.options.image.ydim = JS9.globalOpts.image.ydim;
} else if( JS9.notNull(JS9.globalOpts.ymax) ){
JS9.fits.options.image.ydim = JS9.globalOpts.ymax;
}
}
if( JS9.fits.maxFITSMemory && JS9.globalOpts.maxMemory ){
JS9.fits.maxFITSMemory(JS9.globalOpts.maxMemory);
}
break;
default:
JS9.error(`unknown fits library: ${s}`);
break;
}
// common code
JS9.fits.ready = true;
JS9.fits.name = t;
JS9.fits.options.error = JS9.error;
JS9.fits.options.waiting = JS9.waiting;
return t;
};
// check for 'real' FITS handling routine and call it. This routine can:
// read a blob as a FITS file
// open an existing virtual FITS file (e.g. created by Montage reprojection)
JS9.handleFITSFile = function(file, opts, handler){
if( JS9.fits.handleFITSFile ){
JS9.fits.handleFITSFile(file, opts, handler);
} else {
JS9.error("no FITS module available to process FITS file");
}
};
// cleanup FITS file by deleting vfile, etc
JS9.cleanupFITSFile = function(raw, mode){
let rexp;
if( JS9.hostFS ){
rexp = new RegExp(`^${JS9.hostFS}`);
}
if( JS9.fits.cleanupFITSFile && raw && raw.hdu && raw.hdu.fits ){
// don't delete real local file
if( rexp && raw.hdu.fits.vfile && raw.hdu.fits.vfile.match(rexp) ){
mode = false;
}
JS9.fits.cleanupFITSFile(raw.hdu.fits, mode);
return true;
}
// just return if no available cleanup routine or no raw data file
return false;
};
// load an image (jpeg, png, etc)
JS9.handleImageFile = function(file, options, handler){
const reader = new FileReader();
options = $.extend(true, {}, JS9.fits.options, options);
handler = handler || JS9.Load;
reader.onload = (ev) => {
let data, grey, hdu;
const img = new Image();
img.onload = () => {
let x, y, v, header;
let i = 0;
const canvas = document.createElement("canvas");
const ctx = canvas.getContext("2d");
const h = img.height;
const w = img.width;
canvas.width = w;
canvas.height = h;
ctx.drawImage(img, 0, 0);
data = ctx.getImageData(0, 0, w, h).data;
grey = new Float32Array(h\*w);
for ( y = 0; y < h; y++ ) {
for ( x = 0; x < w; x++ ) {
// NTSC
v = 0.299 \* data[i] + 0.587 \* data[i+1] + 0.114 \* data[i+2];
grey[(h - y) \* w + x] = v;
i += 4;
}
}
header = {SIMPLE: true,
BITPIX: -32,
NAXIS: 2,
NAXIS1: w,
NAXIS2: h};
hdu = {filename: file.name,
naxis: 2, axis: [0, w, h], bitpix: -32, bin: 1,
head: header, data: grey, offscreen: img};
hdu.dmin = Number.MAX\_VALUE;
hdu.dmax = Number.MIN\_VALUE;
for(i=0; i< h\*w; i++){
if( !Number.isNaN(hdu.data[i]) &&
Number.isFinite(hdu.data[i]) ){
hdu.dmin = Math.min(hdu.dmin, hdu.data[i]);
hdu.dmax = Math.max(hdu.dmax, hdu.data[i]);
}
}
options.source = "img";
handler(hdu, options);
};
img.src = ev.target.result;
};
reader.readAsDataURL(file);
};
// check for 'real' FITS handling routine and call it
JS9.getFITSImage = function(fits, hdu, options, handler){
if( JS9.fits.getFITSImage ){
JS9.fits.getFITSImage(fits, hdu, options, handler);
} else {
JS9.error("no FITS module available to process FITS image");
}
};
// run fits2fits converter, if necessary
JS9.fits2fits = function(display, file, opts, func){
let i, s, xdim, ydim, bin, bmode, obj, xcond;
const xopts = {};
opts = opts || {};
if( JS9.notNull(opts.fits2fits) ){
xcond = opts.fits2fits;
} else {
xcond = JS9.globalOpts.fits2fits;
}
if( xcond === true ){
xcond = "always";
} else if( xcond === false ){
xcond = "never";
}
// if never, we are done
if( xcond.match(/never/i) ){
return false;
}
// make sure we are set up to run the converter
// requires a connected helper via a socket.io connection
if( !JS9.helper.connected ||
(JS9.helper.type !== "nodejs" && JS9.helper.type !== "socket.io") ){
if( xcond === "always" && JS9.globalOpts.requireFits2Fits ){
JS9.error("can't run fits2fits without connected JS9 helper");
}
return false;
}
// if the helper program does not exist, we might want to throw an error
if( !JS9.helper.js9helper ){
if( JS9.globalOpts.requireFits2Fits ){
JS9.error("js9helper not found for fits2fits processing");
} else {
return false;
}
}
// requires a tmp workdir
if( !JS9.globalOpts.workDir ){
if( JS9.globalOpts.requireFits2Fits ){
JS9.error("can't run fits2fits without a workdir");
}
return false;
}
xdim =
opts.xdim ||
JS9.fits.options.image.xdim ||
JS9.fits.options.table.xdim;
ydim =
opts.ydim ||
JS9.fits.options.image.ydim ||
JS9.fits.options.table.ydim;
bin =
opts.bin ||
JS9.fits.options.image.bin ||
JS9.fits.options.table.bin;
bmode = opts.binMode || JS9.globalOpts.binMode;
bmode = bmode === "a" ? "a" : "";
// handle string bin, possibly containing explicit binMode
if( typeof bin === "string" ){
if( bin.match(/[as]$/) ){
bmode = bin.slice(-1);
}
bin = parseInt(bin, 10);
}
bin = Math.max(1, bin || 1);
if( JS9.notNull(opts.xcen) && JS9.notNull(opts.ycen) ){
xopts.sect = `${xdim}@${opts.xcen},${ydim}@${opts.ycen},${bin}${bmode}`;
} else {
xopts.sect = `${xdim},${ydim},${bin}${bmode}`;
}
s = xcond.toLowerCase().split(/[>,]/);
for(i=0; i {
let robj, rarr, f, pf, nopts;
// return type can be string or object
if( typeof r === "object" ){
// object from node.js
robj = r;
} else {
// string from cgi
if( r.search(JS9.analOpts.epattern) >=0 ){
robj = {stderr: r};
} else {
robj = {stdout: r};
}
}
if( robj.stderr ){
JS9.error(robj.stderr, JS9.analOpts.epattern);
}
if( robj.stdout ){
// look for error condition, which we might throw or swallow
if( robj.stdout.match(/^ERROR:/) ){
if( JS9.globalOpts.requireFits2Fits ){
JS9.error(robj.stdout);
} else {
robj.stdout = xopts.fits;
}
}
// output is file and possibly parentFile
rarr = robj.stdout.split(/\n/);
// file
f = JS9.cleanPath(rarr[0]);
if( f === xopts.fits ){
// same file (imsection not run)
nopts = $.extend(true, {}, opts);
} else {
// new file using imsection
// relative path: add install dir prefix
if( f.charAt(0) !== "/" ){
f = JS9.InstallDir(f);
}
nopts = $.extend(true, {}, opts);
// but remove already-used section properties from opts
delete nopts.xcen;
delete nopts.ycen;
delete nopts.bin;
// but load entire image section
if( nopts.xdim !== undefined ){ nopts.xdim = 0; }
if( nopts.ydim !== undefined ){ nopts.ydim = 0; }
// save source
nopts.source = "fits2fits";
// it's a proxy file (i.e., delete it on close)
nopts.proxyFile = f;
// json fits info
if( rarr[1] ){
try{ obj = JSON.parse(rarr[1]); }
catch(ignore){ /\* empty \*/ }
if( obj ){
nopts.extname = obj.extname;
nopts.extnum = obj.extnum;
nopts.hdus = obj.hdus;
nopts.parent = obj;
}
}
// look for parentFile (relative to helper, not install)
if( rarr[2] ){
pf = JS9.cleanPath(rarr[2]);
nopts.parentFile = pf;
// now add extension info, if possible
if( nopts.extname ){
nopts.parentFile = nopts.parentFile
.replace(/\[.\*\]/, "");
nopts.parentFile += `[${nopts.extname}]`;
} else if( nopts.extnum && (nopts.extnum > 0) ){
nopts.parentFile = nopts.parentFile
.replace(/\[.\*\]/, "");
nopts.parentFile.file += `[${nopts.extnum}]`;
}
}
// add onload, if necessary
if( func ){
nopts.onload = func;
}
}
// no recursion!
nopts.fits2fits = false;
// load new file
JS9.Load(f, nopts, {display});
}
});
return true;
};
// return the specified colormap object (or default)
JS9.lookupColormap = function(name, mustExist){
let i;
// default is the id must exist
if( mustExist === undefined ){
mustExist = true;
}
if( !name ){
name = JS9.imageOpts.colormap;
}
if( name ){
for(i=0; i",
"47": "?"
};
// allow direct specification of keycode as a number
if( typeof evt === "number" ){
c = evt;
} else {
// otherwise its the event
c = evt.which || evt.keyCode;
}
s = String(c);
// normalize keyCode
if( {}.hasOwnProperty.call(\_to\_ascii, s) ){
c = \_to\_ascii[s];
}
if( !evt.shiftKey && (c >= 65 && c <= 90) ){
c = String.fromCharCode(c + 32);
} else if( !evt.shiftKey && {}.hasOwnProperty.call(\_specialKeys, c) ){
c = \_specialKeys[c];
} else if( evt.shiftKey && {}.hasOwnProperty.call(\_shiftUps, c) ){
//get shifted keyCode value
c = \_shiftUps[c];
} else {
c = String.fromCharCode(c);
}
// check for special key
if( JS9.specialKey(evt) ){
c = `M-${c}`;
}
return c;
};
// get position of mouse in a canvas
// http://stackoverflow.com/questions/1114465/getting-mouse-location-in-canvas
JS9.eventToDisplayPos = function(evt, offset){
// from http://www.quirksmode.org/js/events\_properties.html
let i, targ, pageX, pageY, leftOff, upOff, touches, pos;
const XFUDGE = 1;
const YFUDGE = 1;
if( !evt ){
evt = window.event;
}
if( evt.target ){
targ = evt.target;
} else if( evt.srcElement ){
targ = evt.srcElement;
}
if( targ.nodeType === 3 ){ // defeat Safari bug
targ = targ.parentNode;
}
// offset() returns the position of the element relative to the document
offset = offset || $(targ).offset();
// pageX, pageY: mouse positions relative to the document
// changed touch events: take position from first finger
if( evt.originalEvent ){
if( evt.originalEvent.touches &&
evt.originalEvent.touches.length ){
touches = evt.originalEvent.touches;
pageX = touches[0].pageX;
pageY = touches[0].pageY;
} else if( evt.originalEvent.changedTouches &&
evt.originalEvent.changedTouches.length ){
touches = evt.originalEvent.changedTouches;
pageX = touches[0].pageX;
pageY = touches[0].pageY;
} else {
pageX = evt.pageX;
pageY = evt.pageY;
}
} else {
// mouse events
pageX = evt.pageX;
pageY = evt.pageY;
}
// position is (evt pos relative to page - pos of element relative to page)
// FUDGE added after visual inspection of line512 at zoom 32
// I tried to place the mouse, and have the magnifier be in the right place
// Linux, FF & Chrome: x=1, y=1 (5/28/14)
leftOff = offset.left + XFUDGE;
upOff = offset.top + YFUDGE;
// display position
pos = {x: Math.floor(pageX - leftOff), y: Math.floor(pageY - upOff)};
// touch positions, if necessary
if( touches && touches.length ){
pos.touches = [{x: pos.x, y: pos.y}];
for(i=1; i {
let v = [];
let cosb = Math.cos ( b );
v[0] = Math.cos ( a ) \* cosb;
v[1] = Math.sin ( a ) \* cosb;
v[2] = Math.sin ( b );
return v;
};
// modified from P.T. Wallace (acquired via email 6/29/2020)
const slaDpav = (v1, v2) => {
let x0, y0, z0, w, x1, y1, z1, s, c;
/\* Unit vector to point 1. \*/
x0 = v1 [ 0 ];
y0 = v1 [ 1 ];
z0 = v1 [ 2 ];
w = Math.sqrt ( x0 \* x0 + y0 \* y0 + z0 \* z0 );
if( w != 0.0 ) { x0 /= w; y0 /= w; z0 /= w; }
/\* Vector to point 2. \*/
x1 = v2 [ 0 ];
y1 = v2 [ 1 ];
z1 = v2 [ 2 ];
/\* Position angle. \*/
s = y1 \* x0 - x1 \* y0;
c = z1 \* ( x0 \* x0 + y0 \* y0 ) - z0 \* ( x1 \* x0 + y1 \* y0 );
return ( s != 0.0 || c != 0.0 ) ? Math.atan2 ( s, c ) : 0.0;
};
const d2r = (x) => { return x \* Math.PI / 180; };
const r2d = (x) => { return x \* 180 / Math.PI; };
a = slaDcs2c(d2r(ra1), d2r(dec1));
b = slaDcs2c(d2r(ra2), d2r(dec2));
dist = slaDpav(a, b);
// negation required to be in line with our conventions
dist = -dist;
return r2d(dist);
};
// http://stackoverflow.com/questions/13695317/rotate-a-point-around-another-point
// angle is input in degrees
JS9.rotatePoint = function(point, angle, cen)
{
let cosA, sinA;
cen = cen || {x: 0.0, y: 0.0};
angle = Math.PI \* angle / 180.0;
cosA = Math.cos(angle);
sinA = Math.sin(angle);
return {
x: (cosA \* (point.x - cen.x) - sinA \* (point.y - cen.y) + cen.x),
y: (sinA \* (point.x - cen.x) + cosA \* (point.y - cen.y) + cen.y)
};
};
// multiply two matrices
// https://stackoverflow.com/questions/27205018/multiply-2-matrices-in-javascript
JS9.matrixMultiply = function(a, b){
let r, c, i, m;
const aNumRows = a.length, aNumCols = a[0].length;
// eslint-disable-next-line no-unused-vars
const bNumRows = b.length, bNumCols = b[0].length;
m = new Array(aNumRows); // initialize array of rows
for(r = 0; r < aNumRows; ++r){
m[r] = new Array(bNumCols); // initialize the current row
for(c = 0; c < bNumCols; ++c){
m[r][c] = 0; // initialize the current cell
for(i = 0; i < aNumCols; ++i){
m[r][c] += a[r][i] \* b[i][c];
}
}
}
return m;
};
// invert a 3x3 matrix
JS9.invertMatrix3 = function(xin){
let i, j, det\_1;
let pos = 0.0;
let neg = 0.0;
let temp = xin[0][0] \* xin[1][1];
const prec = 1.0e-15;
const xout = [[0,0,0], [0,0,0], [0,0,0]];
const accum = () => {
if( temp >= 0.0 ){
pos += temp;
} else {
neg += temp;
}
};
// sanity check for NaN
for(i=0; i<3; i++){
for(j=0; j<2; j++){
if( (xin[i][j] === undefined) || Number.isNaN(xin[i][j]) ){
return null;
}
}
}
accum();
temp = -xin[0][1] \* xin[1][0];
accum();
det\_1 = pos + neg;
// Is the submatrix A singular?
if( (det\_1 === 0.0) || (Math.abs(det\_1 / (pos - neg)) < prec) ){
// Matrix M has no inverse
return null;
}
// Calculate inverse(A) = adj(A) / det(A)
det\_1 = 1.0 / det\_1;
xout[0][0] = xin[1][1] \* det\_1;
xout[1][0] = - xin[1][0] \* det\_1;
xout[0][1] = - xin[0][1] \* det\_1;
xout[1][1] = xin[0][0] \* det\_1;
// Calculate -C \* inverse(A)
xout[2][0] = - (xin[2][0] \* xout[0][0] + xin[2][1] \* xout[1][0]);
xout[2][1] = - (xin[2][0] \* xout[0][1] + xin[2][1] \* xout[1][1]);
return xout;
};
// is this a string representation of a number?
// https://stackoverflow.com/questions/175739/built-in-way-in-javascript-to-check-if-a-string-is-a-valid-number
// NB: don't use Number.XXX routines, they don't work .. "2016-5" returns true
JS9.isNumber = function(s){
return !isNaN(parseFloat(s)) && isFinite(s);
};
// check if a variable is neither undefined nor null
JS9.notNull = function(s){
return s !== undefined && s !== null;
};
// check if a variable is either undefined or null
JS9.isNull = function(s){
return s === undefined || s === null;
};
// use a default if a variable is either undefined or null
JS9.defNull = function(s, def){
return JS9.notNull(s) ? s : def;
};
// check if a wcs system is a world coordinate system (fk5, etc)
JS9.isWCSSys = function(s){
return s !== "image" && s !== "physical";
};
// check if a wcs system is not a world coordinate system (fk5, etc)
JS9.notWCS = function(s){
return s === "image" || s === "physical";
};
// was last parsed string in units of hours/min/sec (using specified wcssys)?
JS9.isHMS = function(wcssys, dtype){
dtype = dtype || String.fromCharCode(JS9.saodtype());
return (dtype === ":" || dtype === "h") &&
wcssys !== "galactic" &&
wcssys !== "ecliptic";
};
// is this a HEALPix image?
JS9.ishealpix = function(im){
return im &&
im.imtab === "table" &&
im.raw && im.raw.header &&
im.raw.header.CTYPE1 && im.raw.header.CTYPE1.match(/--HPX/i);
};
// is the proxy server available for LoadProxy() call?
JS9.proxyAvailable = function(){
return JS9.globalOpts.loadProxy &&
!JS9.allinone &&
JS9.globalOpts.helperType !== "none" &&
JS9.globalOpts.workDir;
}
// parse a FITS card and return name and value
JS9.cardpars = function(card){
let value;
let name = card.slice(0, 8).trim();
if( name === "HISTORY" ){ return [name, card.slice(9).trim()]; }
if( name === "COMMENT" ){ return [name, card.slice(9).trim()]; }
if( card[8] !== "=" ){ return undefined; }
value = card.slice(10).replace(/'/g, " ").replace(/ \/.\*/, "").trim();
if( value === "T" ){
value = true;
} else if( value === "F" ){
value = false;
} else if( JS9.isNumber(value) ){
value = parseFloat(value);
}
return [name, value];
};
// convert obj to FITS-style string
JS9.raw2FITS = function(raw, opts){
let i, s, obj, key, val, card, ncard, header, left;
let hasend = false;
let t = "";
const gots = {};
const rexp = /^(NAXIS|CRPIX|CRVAL|CTYPE|CUNIT|CDELT)[34567]/;
const fixparam = (card, name, val, comm) => {
let s, oval, regexp;
let ncard = card;
if( name === "XTENSION" && !val ){
ncard = sprintf("%s = %20s / %-47s",
"SIMPLE",
"T",
"file does conform to FITS standard");
} else {
// eslint-disable-next-line no-useless-escape
regexp = new RegExp(`${name} \*= \*(-?[-+]?[0-9]\*\.?[0-9]\*([eE][-+]?[0-9]+)?) \*`);
if( card ){
s = card.replace(regexp, "$1");
oval = parseFloat(s);
} else {
oval = undefined;
}
if( oval !== val ){
ncard = sprintf("%-8s= %20s / %-47s", name, val, comm||"");
}
}
gots[name] = true;
return ncard;
};
// sanity check
if( !raw ){ return t; }
// opts is optional
opts = opts || {};
// backward compatibility: orig. version used boolean to specify addcr
if( typeof opts === "boolean" ){
opts = {addcr: opts};
}
// raw.card and raw.cardstr contain comments: use them if possible
if( raw.card || raw.cardstr ){
header = raw.header || {};
if( raw.card ){
ncard = raw.card.length;
} else {
ncard = raw.ncard;
}
for(i=0; i 0 ){
for(i=0; i#%d: **name**: %s **type**: %s",
obj.hdu, s, obj.type);
switch(obj.type){
case "image":
t += sprintf(" **bitpix**: %d **naxis**: %d", obj.bitpix, obj.naxis);
if( obj.naxes.length ){
t += " **axes**: [";
for(j=0; jrows: %d%s**cols**: [", obj.rows, s);
for(j=0; j {
let searchVal = value;
text.unmark({
done: () => {
text.mark(searchVal, {
caseSensitive: bar.opts.matchcase,
diacritics: bar.opts.diacritics,
accuracy: bar.opts.matchwords ? "exactly" : "partially",
wildcards: bar.opts.matchwildcards ? "enabled" : "disabled",
done: () => {
bar.results = text.find("mark");
bar.currentIndex = 0;
jumpTo();
}
});
}
});
};
const btnColor = (which) => {
const s = which.prop("data-btn");
if( bar.opts[s] ){
which.removeClass("JS9SearchButton-false");
which.addClass("JS9SearchButton-true");
} else {
which.removeClass("JS9SearchButton-true");
which.addClass("JS9SearchButton-false");
}
};
const jumpTo = () => {
let cur, pos;
if( bar.results.length ){
cur = bar.results.eq(bar.currentIndex);
bar.results.removeClass(currentClass);
if( cur.length ){
cur.addClass(currentClass);
pos = cur.position().top;
if( pos < 0 || pos > div.height() ){
pos = pos + div.scrollTop() - offsetTop;
div.scrollTop(pos);
}
}
}
};
textid = textid || ".JS9AnalysisText";
// make sure we have text
if( jel.is(textid) ){
text = jel;
} else {
text = jel.find(textid);
if( !text.length ){
return;
}
}
// light window or div?
div = jel.find(JS9.lightOpts[JS9.LIGHTWIN].drag);
if( !div.length ){
// just a div
div = jel;
}
// does the searchbar already exist?
bar = div.find(".JS9Searchbar");
if( bar.length ){
// make it visiable and return
bar.css("display", "block");
return;
}
// make a new searchbar
bar = $("

")
.addClass("JS9Searchbar")
.appendTo(div);
// add options
bar.opts = {
matchcase: false,
matchdiacritics: false,
matchwords: false,
matchwildcards: false,
};
// search text box
srch = $("")
.addClass("JS9SearchInput")
.appendTo(bar);
// event fires with each keystroke
srch.on("input", () => {
search(srch.val());
});
// placeholder hints
if( bar.opts.matchwildcards ){
srch.prop("placeholder", "sea\*rch template?");
} else {
srch.prop("placeholder", "search term(s)");
}
// find next occurence
next = $("")
.addClass("JS9SearchButton")
.prop("data-btn", "next")
.html("↓")
.appendTo(bar);
// find previous occurence
prev = $("")
.addClass("JS9SearchButton")
.prop("data-btn", "prev")
.html("↑")
.appendTo(bar);
// event callback for next and prev
next.add(prev).on("click", (e) => {
if( bar.results && bar.results.length) {
bar.currentIndex += $(e.currentTarget).is(prev) ? -1 : 1;
if( bar.currentIndex < 0 ){
bar.currentIndex = bar.results.length - 1;
}
if( bar.currentIndex > bar.results.length - 1 ){
bar.currentIndex = 0;
}
jumpTo();
}
});
matchcase = $("")
.addClass(`JS9SearchButton JS9SearchButton-${bar.opts.matchcase}`)
.prop("data-btn", "matchcase")
.html("Match Case")
.appendTo(bar);
matchcase.on("click", () => {
bar.opts.matchcase = !bar.opts.matchcase;
btnColor(matchcase);
search(srch.val());
});
btnColor(matchcase);
matchdiacritics = $("")
.addClass(`JS9SearchButton JS9SearchButton-${bar.opts.matchdiacritics}`)
.prop("data-btn", "matchdiacritics")
.html("Match Diacritics")
.appendTo(bar);
matchdiacritics.on("click", () => {
bar.opts.matchdiacritics = !bar.opts.matchdiacritics;
btnColor(matchdiacritics);
search(srch.val());
});
btnColor(matchdiacritics);
matchwords = $("")
.addClass(`JS9SearchButton JS9SearchButton-${bar.opts.matchwords}`)
.prop("data-btn", "matchwords")
.html("Whole Words")
.appendTo(bar);
matchwords.on("click", () => {
bar.opts.matchwords = !bar.opts.matchwords;
btnColor(matchwords);
search(srch.val());
});
btnColor(matchwords);
matchwildcards = $("")
.addClass(`JS9SearchButton JS9SearchButton-${bar.opts.matchwildcards}`)
.prop("data-btn", "matchwildcards")
.html("Wildcards")
.appendTo(bar);
matchwildcards.on("click", () => {
bar.opts.matchwildcards = !bar.opts.matchwildcards;
if( bar.opts.matchwildcards ){
srch.prop("placeholder", "sea\*rch template?");
} else {
srch.prop("placeholder", "search term(s)");
}
btnColor(matchwildcards);
search(srch.val());
});
btnColor(matchwildcards);
// close the searchbar
close = $("")
.addClass("JS9SearchButton")
.prop("data-btn", "close")
.html("Close")
.appendTo(bar);
close.on("click", () => {
text.unmark();
srch.val("");
bar.css("display", "none");
});
// no outline on focus
div.css("outline", "none");
// set tabindex so we can sense keyboard events
div.attr("tabindex", "0");
// meta-k will bring up the searchbar
div.on("keydown", (evt) => {
const code = evt.which || evt.keyCode;
const c = String.fromCharCode(code);
if( JS9.specialKey(evt) && c === "F" ){
if( bar.css("display") === "none" ){
bar.css("display", "block");
srch.focus();
} else {
text.unmark();
srch.val("");
bar.css("display", "none");
}
}
});
};
// create a tooltip, with the tip formatted from a string containing
// variables in the current context, e.g. "$im.id\n$xreg.imstr\n$xreg.data.tag"
JS9.tooltip = function(x, y, fmt, im, xreg, evt){
let tipstr, tx, ty, w, h;
const fmt2str = (str) => {
// eslint-disable-next-line no-unused-vars
const cmd = str.replace(/\$([a-zA-Z0-9\_./]+)/g, (m, t, o) => {
let i, v, val;
const arr = t.split(".");
switch(arr[0]){
case "im":
val = im;
break;
case "xreg":
val = xreg;
break;
case "evt":
val = evt;
break;
case "data":
val = xreg.data;
break;
default:
return m;
}
for(i=1; i {
JS9.mergePrefs(obj);
},
// eslint-disable-next-line no-unused-vars
error: (jqXHR, textStatus, errorThrown) => {
if( doerr ){
JS9.log("JS9 prefs file not available: %s", url);
}
}
});
};
// is this object a typed array?
JS9.isTypedArray = function(obj){
let type;
const types = {
"[object Int8Array]": true,
"[object Uint8Array]": true,
"[object Uint8ClampedArray]": true,
"[object Int16Array]": true,
"[object Uint16Array]": true,
"[object Int32Array]": true,
"[object Uint32Array]": true,
"[object Float32Array]": true,
"[object Float64Array]": true
};
type = Object.prototype.toString.call(obj);
return {}.hasOwnProperty.call(types, type);
};
// starbase table support
// tab-delimited ascii tables, # in first line is a comment
JS9.Starbase = function(s, opts){
let i, j, skips, dashes, data, cobj;
let line = 0;
const checkDashline = (dash) => {
let i;
for(i=0; i { return x; };
// init returned object
this.head = {};
this.convFuncs = [];
this.data = [];
this.delims = [];
// sanity check
if( !s ){ return; }
// opts is optional
opts = opts || {};
// get array of data lines
data = s.replace(/\s+$/,"").split("\n");
// skip comments
if( opts.skip ){
skips = opts.skip.split("");
if( skips && skips.length ){
for(; line < data.length; line++){
if( (skips[0] !== data[line][0]) &&
(skips[1] !== "\n" || data[line] !== "") ){
break;
}
}
}
}
// make sure we have a header to process
if( (data[line] === undefined) || (data[line+1] === undefined) ){
return;
}
// look for header and dashes, in various guises
this.headline = data[line++].trim().split(/ \*\t \*/);
if( opts.units ){
this.unitline = data[line++].trim().split(/ \*\t \*/);
}
this.dashline = data[line++].trim().split(/ \*\t \*/);
dashes = checkDashline(this.dashline);
// read lines until the dashline is found
while ( dashes === 0 || dashes !== this.headline.length ){
if( !opts.units ){
this.headline = this.dashline;
} else {
this.headline = this.unitline;
this.unitline = this.dashline;
}
this.dashline = data[line++].trim().split(/ \*\t \*/);
dashes = checkDashline(this.dashline);
}
// process header:
// replace "." with "\_" in header names
// create a vector of type converter funcs
for(i=0; i { return a.min - b.min; });
// return array of color objects
return staticColors;
};
// look up a static color
JS9.lookupStaticColor = (im, val, cache) => {
let i, color;
let nocolor = {red:0,green:0,blue:0,alpha:0};
const maxcache = 10000000;
const search = (array, val) => {
let middle, obj;
let start = 0;
let end = array.length - 1;
while( start <= end ){
middle = Math.floor((start + end) / 2);
obj = array[middle];
if( val >= obj.min && val <= obj.max ) {
// found the interval
return middle;
} else if( obj.max < val ){
// continue searching to the right
start = middle + 1;
} else {
// continue searching to the left
end = middle - 1;
}
}
// interval wasn't found
return -1;
};
if( im && im.staticObj ){
nocolor = im.params.nocolor || nocolor;
// colors are sorted, so we can skip values less than the first min
if( val < im.staticObj.colors[0].min ){ return nocolor; }
// return cached color, if possible
if( cache && cache[val] ){ return cache[val]; }
// look for the value within the static color intervals
i = search(im.staticObj.colors, val);
if( i < 0 ){
color = nocolor;
} else {
color = im.staticObj.colors[i];
if( !color.active ){
color = nocolor;
}
}
// save in cache, if possible
if( cache && val <= maxcache ){
cache[val] = color;
}
// this is the color
return color;
}
// nothing found
return nocolor;
};
// convert string to double, returning (possibly scaled) value and delim
JS9.strtoscaled = function(s){
let dval = JS9.saostrtod(s);
const dtype = String.fromCharCode(JS9.saodtype());
// scale for certain units
switch(dtype){
case '"':
dval /= 3600.0;
break;
case "'":
dval /= 60.0;
break;
case "r":
dval \*= (180.0 / Math.PI) ;
break;
default:
break;
}
return {dval, dtype};
};
// clean file path
JS9.cleanPath = function(s, what){
let t;
// vulnerability hints culled from https://html5sec.org/
const xssreg = /(<(animation|form|math|maction|svg|script|video)\s|<\?xml|javascript:|on.\*&equals;|alert\(|alert&lpar;)|window\./i;
if( !s ){ return ""; }
// check for xss vulnerabilities (but not within cfitsio brackets)
t = s.replace(/\[.\*\]/, "");
if( t.match(xssreg) ){
// we're under attack: turn on alerts no matter what
JS9.globalOpts.alerts = true;
// warn user they are under attack!
JS9.error(`${what||"filename"} is susceptible to XSS attack: ${t}`);
}
// remove unnecessary /./ etc
return s.trim().replace(/\/\.\//, "/").replace(/^\.\//, "");
};
// convert relative directory into absolute directory using currentDir
// desktop only, to make pathname relative to where js9 was started
JS9.fixPath = function(f, opts){
opts = opts || {};
if( window.electron &&
JS9.desktopOpts.currentPath &&
opts.fixpath !== false &&
!f.match(JS9.URLEXP) ){
if( f.match(/^\${JS9\_DIR}\//) ){
f = f.replace(/^\${JS9\_DIR}\//, JS9.INSTALLDIR);
} else if( f.match(/^\${JS9\_INSTALLDIR}\//) ){
f = f.replace(/^\${JS9\_INSTALLDIR}\//, JS9.INSTALLDIR);
} else if( f.match(/^\${JS9\_PAGEDIR}\//) ){
f = f.replace(/^\${JS9\_PAGEDIR}\//, "");
} else if( f.charAt(0) !== "/" ){
f = `${window.electron.currentDir}/${f}`;
}
}
return f;
};
// return virtual path of a local access file, if warranted
JS9.localAccess = function(file){
let tfile, text;
// only if local access is turned on and we have a local disk mounted
if( !file || !JS9.globalOpts.localAccess || !JS9.hostFS ){
return null;
}
// get file without bracket extension
tfile = file.replace(/\[.\*\]/, "");
// and file extension
text = `.${tfile.split(".").pop().toLowerCase()}`;
// this is the candidate virtual file
tfile = `${JS9.hostFS}/${tfile}`;
// check for existence
// note to myself: cfitsio uncompresses .gz files into memory, so
// there is no benefit to having ".gz" in the localTemplates list.
if( JS9.vsize(tfile) >= 0 &&
$.inArray(text, JS9.globalOpts.localTemplates.split(",")) >= 0){
if( JS9.DEBUG > 2 ){
JS9.log("local access file: %s", tfile);
}
return tfile;
}
// no local access file
return null;
};
// get directory name of a file, including trailing "/";
JS9.dirname = function(f){
if( !f || !f.includes("/") ){
return "";
}
return f.match(/.\*\//)[0];
};
// ---------------------------------------------------------------------
// end of Utilities
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
// global event handlers
// ---------------------------------------------------------------------
// mousedown: assumes display obj is passed in evt.data
JS9.mouseDownCB = function(evt){
const display = evt.data;
const im = display.image;
const x = $(document).scrollLeft(), y = $(document).scrollTop();
// sanity check
if( !im ){ return; }
// set focus, if necessary, but undo any scrolling
if( JS9.globalOpts.clickToFocus ){
im.display.displayConjq.focus();
window.scrollTo(x, y);
}
// get element offset
if( evt.target ){
im.posOffset = $(evt.target).offset();
}
// get canvas position
im.pos0 = JS9.eventToDisplayPos(evt, im.posOffset);
// this also is the current canvas position
im.pos = im.pos0;
// get image position
im.ipos0 = im.displayToImagePos(im.pos);
// this also is the current image position
im.ipos = im.ipos0;
// in the resize area?
display.resizing = display.inResize(im.pos);
// normal (non-resizing) processing
if( !display.resizing ){
evt.preventDefault();
// begin actions for mouse and touch events
if( {}.hasOwnProperty.call(JS9, "MouseTouch") ){
JS9.MouseTouch.action(im, evt, "start");
}
// inside a region, clear region display and return;
if( im.clickInRegion && (im.clickInLayer === "regions") ){
// clear the region layer
im.display.clearMessage("regions");
return;
}
// plugin callbacks
if( !JS9.specialKey(evt) ){
im.xeqPlugins("mouse", "onmousedown", evt);
}
}
// set click state to current mouse button
im.clickState = evt.which;
switch(evt.which){
case 1:
case 2:
break;
case 3:
// secondary mouse click
im.clickState = 2;
break;
}
// override click state with touch state, if possible
if( evt.originalEvent &&
evt.originalEvent.touches && evt.originalEvent.touches.length ){
im.clickState = -evt.originalEvent.touches.length;
}
// add this display's callbacks on the whole document
$(document).on(`mousemove.${display.id}`, display,
(evt) => { return JS9.mouseMoveCB(evt); });
$(document).on(`mouseup.${display.id}`, display,
(evt) => { return JS9.mouseUpCB(evt); });
};
// mouseup: assumes display obj is passed in evt.data
JS9.mouseUpCB = function(evt){
let i, dwidth, dheight, tdisp, isclick;
const display = evt.data;
const im = display.image;
// sanity check
if( !im ){
// handle supermenu clicks specially (even if no image is loaded)
if( {}.hasOwnProperty.call(JS9, "Menubar") ){
JS9.Menubar.onclick(evt.data);
}
return;
}
// get canvas position
im.pos = JS9.eventToDisplayPos(evt, im.posOffset);
// image position
im.ipos = im.displayToImagePos(im.pos);
isclick = ((Math.abs(im.pos0.x-im.pos.x) < JS9.NOMOVE) &&
(Math.abs(im.pos0.y-im.pos.y) < JS9.NOMOVE));
// prevent default unless we are close to the resize area
if( !display.inResize(im.pos) ){
evt.preventDefault();
}
// end actions for mouse and touch events
if( {}.hasOwnProperty.call(JS9, "MouseTouch") ){
JS9.MouseTouch.action(im, evt, "stop");
}
// in a region, update region string since we probably just modified it
if( im.clickInRegion && im.clickInLayer ){
if( !isclick ){
// tell plugins that this region has been updated (e.g. sync)
im.updateShapes(im.clickInLayer, "selected", "update");
}
}
// plugin callbacks
if( !JS9.specialKey(evt) ){
im.xeqPlugins("mouse", "onmouseup", evt);
if( isclick ){
im.xeqPlugins("mouse", "onclick", evt);
// handle supermenu clicks specially
if( {}.hasOwnProperty.call(JS9, "Menubar") ){
JS9.Menubar.onclick(im.display);
}
}
if( JS9.globalOpts.dynamicSelect === "click" ){
if( JS9.Dysel.getDisplayOr(display) !== display ){
// mark this as the current display
JS9.Dysel.select(display);
}
}
} else {
// shift-click: pan to mouse position, if necessary
if( isclick && !im.clickInRegion && JS9.globalOpts.metaClickPan ){
if( im.editAnnulus ){
im.\_regroupAnnulus("regions", evt);
} else {
im.setPan(im.ipos.x,im.ipos.y);
}
}
}
// safe to unset clickInRegion now
im.clickInRegion = false;
im.clickInLayer = null;
im.clickState = 0;
im.posOffset = null;
// finish refresh, if necessary
if( im.tmp.panzoomRefresh ){
im.refreshLayers(im.tmp.panzoomRefresh);
delete im.tmp.panzoomRefresh;
}
// finish resize, if necessary
if( display.resizing ){
display.resizing = false;
if( JS9.bugs.webkit\_resize ){
dwidth = parseInt(display.divjq.css("width"), 10);
dheight = parseInt(display.divjq.css("height"), 10);
if( dwidth < display.owidth ){
display.divjq.css("width", display.owidth + JS9.RESIZEFUDGE);
}
if( dheight < display.oheight ){
display.divjq.css("height", display.oheight + JS9.RESIZEFUDGE);
}
}
// if we were not displaying the image while resizing, do it now
if( !JS9.globalOpts.resizeRedisplay ){
im.displayImage("all");
im.refreshLayers();
}
}
// remove this display's callbacks on the whole document
$(document).off(`mouseup.${display.id}`);
$(document).off(`mousemove.${display.id}`);
// look for active mousedown from a different display and fire mouse up
for(i=0; i {
let file, fname;
// ... and load each file in turn
for(i=0; i=0 ){
visible = "hidden";
}
// wrap the target div in a container div
divjq.wrap(`

`);
// this is the original div
instance.odivjq = divjq;
// this is the div which the instance sees
instance.divjq = divjq;
// add classes for easier CSS specification
instance.divjq.addClass(`${plugin.xclass}Plugin`).addClass("JS9Plugin");
// add id
if( !instance.odivjq.attr("id") ){
instance.odivjq.attr("id", instance.id);
}
// the wrapper plugincontainer is the the outer div
instance.outerdivjq = instance.divjq.closest(".JS9PluginContainer");
// add the toolbar to the container, if necessary
if( divjq.data("toolbarseparate") !== false ){
if( plugin.opts.toolbarSeparate || divjq.data("toolbarseparate") ){
ndiv = `

`;
$(ndiv).insertBefore(instance.divjq);
}
}
}
// backlink this instance into the plugin
instance.plugin = plugin;
// save original el so we know we have done this one
instance.el = el;
// mark as valid for display and execution
// undefined => not created, or "active" or "inactive"
instance.status = "active";
// save this instance globally
plugin.instances.push(instance);
// for virtual plugins, instantiate and backlink into all displays
if( instance.winType === "virtual" ){
for(i=0; i`)
.css("z-index", JS9.BTNZINDEX)
.html(html)
.data("displayid", did)
.insertAfter(pdivjq);
}
instance.display.pluginInstances[plugin.name] = instance;
// call the init routine (usually a constructor)
// on entry: elements have already been defined in the context:
// this.div: the DOM element representing the div for this plugin
// this.divjq: jquery object representing the div for this plugin
// this.id: id of the div (or the plugin name as a default)
// this.plugin: plugin class object (user opts in opts subobject)
// this.winType: "div" (in-page div) or "light" (from view menu)
// this.winHandle: handle returned from light window create routine
// this.display: the display object associated with this plugin
// this.status: "active" or "inactive" or undefined
plugin.func.apply(instance, args);
// for a dynamic plugin, backlink this instance into all displays
if( did === "\*" ){
for(i=0; i {
let j, k, instance;
// instantiate any divs not yet done
$(`div.${plugin.name}`).each((index, element) => {
// new instance of this div-based plugin
JS9.instantiatePlugin($(element),
plugin, null, plugin.opts.divArgs);
});
// if we have a non-visible plugin (no menu and no window dims)
// which is not instantiated, instantiate it now (e.g. regions)
if( !plugin.opts.menuItem && plugin.opts.winDims &&
!plugin.opts.winDims[0] && !plugin.opts.winDims[1] ){
JS9.instantiatePlugin(null, plugin, null, plugin.opts.divArgs);
}
// backlink new instances of any dynamic plugins
for(j=0; j {
// tell Emscripten we already have wasm binary
// eslint-disable-next-line no-unused-vars
Module.wasmBinary = data;
JS9.globalOpts.astroemURL = JS9.InstallDir("astroemw.js");
// load astroem js (with wasm) file
try{
JS9.loadScript(JS9.globalOpts.astroemURL);
}
catch(e){
JS9.error(`can't load ${JS9.globalOpts.astroemURL}`);
}
});
} else {
JS9.globalOpts.astroemURL = JS9.InstallDir("astroem.js");
// load astroem js (only) file
try{
JS9.loadScript(JS9.globalOpts.astroemURL);
}
catch(e){
JS9.error(`can't load ${JS9.globalOpts.astroemURL}`);
}
}
};
// initialize FITS support
JS9.initFITS = function(){
// initialize astronomy emscripten routines (wcslib, etc), if possible
if( {}.hasOwnProperty.call(window, "Astroem") ){
JS9.vmalloc = Astroem.vmalloc;
JS9.vfree = Astroem.vfree;
JS9.vheap = Astroem.vheap;
JS9.vmemcpy = Astroem.vmemcpy;
JS9.vstrcpy = Astroem.vstrcpy;
JS9.vfile = Astroem.vfile;
JS9.vread = Astroem.vread;
JS9.vunlink = Astroem.vunlink;
JS9.vsize = Astroem.vsize;
JS9.vmount = Astroem.vmount;
JS9.arrfile = Astroem.arrfile;
JS9.listhdu = Astroem.listhdu;
JS9.initwcs = Astroem.initwcs;
JS9.freewcs = Astroem.freewcs;
JS9.wcsinfo = Astroem.wcsinfo;
JS9.wcssys = Astroem.wcssys;
JS9.wcsunits = Astroem.wcsunits;
JS9.pix2wcs = Astroem.pix2wcs;
JS9.wcs2pix = Astroem.wcs2pix;
JS9.reg2wcs = Astroem.reg2wcs;
JS9.saostrtod = Astroem.saostrtod;
JS9.saodtostr = Astroem.saodtostr;
JS9.saodtype = Astroem.saodtype;
JS9.zscale = Astroem.zscale;
JS9.tanhdr = Astroem.tanhdr;
JS9.reproject = Astroem.reproject;
JS9.madd = Astroem.madd;
JS9.imgtbl = Astroem.imgtbl;
JS9.makehdr = Astroem.makehdr;
JS9.shrinkhdr = Astroem.shrinkhdr;
JS9.imsection = Astroem.imsection;
JS9.regcnts = Astroem.regcnts;
JS9.fitsLibrary("cfitsio");
}
};
// init colormaps
JS9.initColormaps = function(){
// sanity check
if( !{}.hasOwnProperty.call(JS9, "Colormap") ){ return; }
// load colormaps
JS9.checkNew(new JS9.Colormap("grey",
[[0,0], [1,1]],
[[0,0], [1,1]],
[[0,0], [1,1]]));
JS9.checkNew(new JS9.Colormap("red",
[[0,0], [1,1]],
[[0,0], [0,0]],
[[0,0], [0,0]]));
JS9.checkNew(new JS9.Colormap("green",
[[0,0], [0,0]],
[[0,0], [1,1]],
[[0,0], [0,0]]));
JS9.checkNew(new JS9.Colormap("blue",
[[0,0], [0,0]],
[[0,0], [0,0]],
[[0,0], [1,1]]));
JS9.checkNew(new JS9.Colormap("heat",
[[0,0], [0.34,1], [1,1]],
[[0,0], [1,1]],
[[0,0], [0.65,0], [0.98,1], [1,1]]));
JS9.checkNew(new JS9.Colormap("cool",
[[0,0], [0.29,0], [0.76,0.1], [1,1]],
[[0,0], [0.22,0], [0.96,1], [1,1]],
[[0,0], [0.53,1], [1,1]]));
//https://ai.googleblog.com/2019/08/turbo-improved-rainbow-colormap-for.html
//https://gist.github.com/mikhailov-work/6a308c20e494d9e0ccc29036b28faa7a
JS9.checkNew(new JS9.Colormap("turbo",
[[0.18995,0.07176,0.23217],[0.19483,0.08339,0.26149],[0.19956,0.09498,0.29024],[0.20415,0.10652,0.31844],[0.20860,0.11802,0.34607],[0.21291,0.12947,0.37314],[0.21708,0.14087,0.39964],[0.22111,0.15223,0.42558],[0.22500,0.16354,0.45096],[0.22875,0.17481,0.47578],[0.23236,0.18603,0.50004],[0.23582,0.19720,0.52373],[0.23915,0.20833,0.54686],[0.24234,0.21941,0.56942],[0.24539,0.23044,0.59142],[0.24830,0.24143,0.61286],[0.25107,0.25237,0.63374],[0.25369,0.26327,0.65406],[0.25618,0.27412,0.67381],[0.25853,0.28492,0.69300],[0.26074,0.29568,0.71162],[0.26280,0.30639,0.72968],[0.26473,0.31706,0.74718],[0.26652,0.32768,0.76412],[0.26816,0.33825,0.78050],[0.26967,0.34878,0.79631],[0.27103,0.35926,0.81156],[0.27226,0.36970,0.82624],[0.27334,0.38008,0.84037],[0.27429,0.39043,0.85393],[0.27509,0.40072,0.86692],[0.27576,0.41097,0.87936],[0.27628,0.42118,0.89123],[0.27667,0.43134,0.90254],[0.27691,0.44145,0.91328],[0.27701,0.45152,0.92347],[0.27698,0.46153,0.93309],[0.27680,0.47151,0.94214],[0.27648,0.48144,0.95064],[0.27603,0.49132,0.95857],[0.27543,0.50115,0.96594],[0.27469,0.51094,0.97275],[0.27381,0.52069,0.97899],[0.27273,0.53040,0.98461],[0.27106,0.54015,0.98930],[0.26878,0.54995,0.99303],[0.26592,0.55979,0.99583],[0.26252,0.56967,0.99773],[0.25862,0.57958,0.99876],[0.25425,0.58950,0.99896],[0.24946,0.59943,0.99835],[0.24427,0.60937,0.99697],[0.23874,0.61931,0.99485],[0.23288,0.62923,0.99202],[0.22676,0.63913,0.98851],[0.22039,0.64901,0.98436],[0.21382,0.65886,0.97959],[0.20708,0.66866,0.97423],[0.20021,0.67842,0.96833],[0.19326,0.68812,0.96190],[0.18625,0.69775,0.95498],[0.17923,0.70732,0.94761],[0.17223,0.71680,0.93981],[0.16529,0.72620,0.93161],[0.15844,0.73551,0.92305],[0.15173,0.74472,0.91416],[0.14519,0.75381,0.90496],[0.13886,0.76279,0.89550],[0.13278,0.77165,0.88580],[0.12698,0.78037,0.87590],[0.12151,0.78896,0.86581],[0.11639,0.79740,0.85559],[0.11167,0.80569,0.84525],[0.10738,0.81381,0.83484],[0.10357,0.82177,0.82437],[0.10026,0.82955,0.81389],[0.09750,0.83714,0.80342],[0.09532,0.84455,0.79299],[0.09377,0.85175,0.78264],[0.09287,0.85875,0.77240],[0.09267,0.86554,0.76230],[0.09320,0.87211,0.75237],[0.09451,0.87844,0.74265],[0.09662,0.88454,0.73316],[0.09958,0.89040,0.72393],[0.10342,0.89600,0.71500],[0.10815,0.90142,0.70599],[0.11374,0.90673,0.69651],[0.12014,0.91193,0.68660],[0.12733,0.91701,0.67627],[0.13526,0.92197,0.66556],[0.14391,0.92680,0.65448],[0.15323,0.93151,0.64308],[0.16319,0.93609,0.63137],[0.17377,0.94053,0.61938],[0.18491,0.94484,0.60713],[0.19659,0.94901,0.59466],[0.20877,0.95304,0.58199],[0.22142,0.95692,0.56914],[0.23449,0.96065,0.55614],[0.24797,0.96423,0.54303],[0.26180,0.96765,0.52981],[0.27597,0.97092,0.51653],[0.29042,0.97403,0.50321],[0.30513,0.97697,0.48987],[0.32006,0.97974,0.47654],[0.33517,0.98234,0.46325],[0.35043,0.98477,0.45002],[0.36581,0.98702,0.43688],[0.38127,0.98909,0.42386],[0.39678,0.99098,0.41098],[0.41229,0.99268,0.39826],[0.42778,0.99419,0.38575],[0.44321,0.99551,0.37345],[0.45854,0.99663,0.36140],[0.47375,0.99755,0.34963],[0.48879,0.99828,0.33816],[0.50362,0.99879,0.32701],[0.51822,0.99910,0.31622],[0.53255,0.99919,0.30581],[0.54658,0.99907,0.29581],[0.56026,0.99873,0.28623],[0.57357,0.99817,0.27712],[0.58646,0.99739,0.26849],[0.59891,0.99638,0.26038],[0.61088,0.99514,0.25280],[0.62233,0.99366,0.24579],[0.63323,0.99195,0.23937],[0.64362,0.98999,0.23356],[0.65394,0.98775,0.22835],[0.66428,0.98524,0.22370],[0.67462,0.98246,0.21960],[0.68494,0.97941,0.21602],[0.69525,0.97610,0.21294],[0.70553,0.97255,0.21032],[0.71577,0.96875,0.20815],[0.72596,0.96470,0.20640],[0.73610,0.96043,0.20504],[0.74617,0.95593,0.20406],[0.75617,0.95121,0.20343],[0.76608,0.94627,0.20311],[0.77591,0.94113,0.20310],[0.78563,0.93579,0.20336],[0.79524,0.93025,0.20386],[0.80473,0.92452,0.20459],[0.81410,0.91861,0.20552],[0.82333,0.91253,0.20663],[0.83241,0.90627,0.20788],[0.84133,0.89986,0.20926],[0.85010,0.89328,0.21074],[0.85868,0.88655,0.21230],[0.86709,0.87968,0.21391],[0.87530,0.87267,0.21555],[0.88331,0.86553,0.21719],[0.89112,0.85826,0.21880],[0.89870,0.85087,0.22038],[0.90605,0.84337,0.22188],[0.91317,0.83576,0.22328],[0.92004,0.82806,0.22456],[0.92666,0.82025,0.22570],[0.93301,0.81236,0.22667],[0.93909,0.80439,0.22744],[0.94489,0.79634,0.22800],[0.95039,0.78823,0.22831],[0.95560,0.78005,0.22836],[0.96049,0.77181,0.22811],[0.96507,0.76352,0.22754],[0.96931,0.75519,0.22663],[0.97323,0.74682,0.22536],[0.97679,0.73842,0.22369],[0.98000,0.73000,0.22161],[0.98289,0.72140,0.21918],[0.98549,0.71250,0.21650],[0.98781,0.70330,0.21358],[0.98986,0.69382,0.21043],[0.99163,0.68408,0.20706],[0.99314,0.67408,0.20348],[0.99438,0.66386,0.19971],[0.99535,0.65341,0.19577],[0.99607,0.64277,0.19165],[0.99654,0.63193,0.18738],[0.99675,0.62093,0.18297],[0.99672,0.60977,0.17842],[0.99644,0.59846,0.17376],[0.99593,0.58703,0.16899],[0.99517,0.57549,0.16412],[0.99419,0.56386,0.15918],[0.99297,0.55214,0.15417],[0.99153,0.54036,0.14910],[0.98987,0.52854,0.14398],[0.98799,0.51667,0.13883],[0.98590,0.50479,0.13367],[0.98360,0.49291,0.12849],[0.98108,0.48104,0.12332],[0.97837,0.46920,0.11817],[0.97545,0.45740,0.11305],[0.97234,0.44565,0.10797],[0.96904,0.43399,0.10294],[0.96555,0.42241,0.09798],[0.96187,0.41093,0.09310],[0.95801,0.39958,0.08831],[0.95398,0.38836,0.08362],[0.94977,0.37729,0.07905],[0.94538,0.36638,0.07461],[0.94084,0.35566,0.07031],[0.93612,0.34513,0.06616],[0.93125,0.33482,0.06218],[0.92623,0.32473,0.05837],[0.92105,0.31489,0.05475],[0.91572,0.30530,0.05134],[0.91024,0.29599,0.04814],[0.90463,0.28696,0.04516],[0.89888,0.27824,0.04243],[0.89298,0.26981,0.03993],[0.88691,0.26152,0.03753],[0.88066,0.25334,0.03521],[0.87422,0.24526,0.03297],[0.86760,0.23730,0.03082],[0.86079,0.22945,0.02875],[0.85380,0.22170,0.02677],[0.84662,0.21407,0.02487],[0.83926,0.20654,0.02305],[0.83172,0.19912,0.02131],[0.82399,0.19182,0.01966],[0.81608,0.18462,0.01809],[0.80799,0.17753,0.01660],[0.79971,0.17055,0.01520],[0.79125,0.16368,0.01387],[0.78260,0.15693,0.01264],[0.77377,0.15028,0.01148],[0.76476,0.14374,0.01041],[0.75556,0.13731,0.00942],[0.74617,0.13098,0.00851],[0.73661,0.12477,0.00769],[0.72686,0.11867,0.00695],[0.71692,0.11268,0.00629],[0.70680,0.10680,0.00571],[0.69650,0.10102,0.00522],[0.68602,0.09536,0.00481],[0.67535,0.08980,0.00449],[0.66449,0.08436,0.00424],[0.65345,0.07902,0.00408],[0.64223,0.07380,0.00401],[0.63082,0.06868,0.00401],[0.61923,0.06367,0.00410],[0.60746,0.05878,0.00427],[0.59550,0.05399,0.00453],[0.58336,0.04931,0.00486],[0.57103,0.04474,0.00529],[0.55852,0.04028,0.00579],[0.54583,0.03593,0.00638],[0.53295,0.03169,0.00705],[0.51989,0.02756,0.00780],[0.50664,0.02354,0.00863],[0.49321,0.01963,0.00955],[0.47960,0.01583,0.01055]]));
// https://github.com/BIDS/colormap/blob/master/colormaps.py
JS9.checkNew(new JS9.Colormap("viridis", [[0.267004, 0.004874, 0.329415], [0.268510, 0.009605, 0.335427], [0.269944, 0.014625, 0.341379], [0.271305, 0.019942, 0.347269], [0.272594, 0.025563, 0.353093], [0.273809, 0.031497, 0.358853], [0.274952, 0.037752, 0.364543], [0.276022, 0.044167, 0.370164], [0.277018, 0.050344, 0.375715], [0.277941, 0.056324, 0.381191], [0.278791, 0.062145, 0.386592], [0.279566, 0.067836, 0.391917], [0.280267, 0.073417, 0.397163], [0.280894, 0.078907, 0.402329], [0.281446, 0.084320, 0.407414], [0.281924, 0.089666, 0.412415], [0.282327, 0.094955, 0.417331], [0.282656, 0.100196, 0.422160], [0.282910, 0.105393, 0.426902], [0.283091, 0.110553, 0.431554], [0.283197, 0.115680, 0.436115], [0.283229, 0.120777, 0.440584], [0.283187, 0.125848, 0.444960], [0.283072, 0.130895, 0.449241], [0.282884, 0.135920, 0.453427], [0.282623, 0.140926, 0.457517], [0.282290, 0.145912, 0.461510], [0.281887, 0.150881, 0.465405], [0.281412, 0.155834, 0.469201], [0.280868, 0.160771, 0.472899], [0.280255, 0.165693, 0.476498], [0.279574, 0.170599, 0.479997], [0.278826, 0.175490, 0.483397], [0.278012, 0.180367, 0.486697], [0.277134, 0.185228, 0.489898], [0.276194, 0.190074, 0.493001], [0.275191, 0.194905, 0.496005], [0.274128, 0.199721, 0.498911], [0.273006, 0.204520, 0.501721], [0.271828, 0.209303, 0.504434], [0.270595, 0.214069, 0.507052], [0.269308, 0.218818, 0.509577], [0.267968, 0.223549, 0.512008], [0.266580, 0.228262, 0.514349], [0.265145, 0.232956, 0.516599], [0.263663, 0.237631, 0.518762], [0.262138, 0.242286, 0.520837], [0.260571, 0.246922, 0.522828], [0.258965, 0.251537, 0.524736], [0.257322, 0.256130, 0.526563], [0.255645, 0.260703, 0.528312], [0.253935, 0.265254, 0.529983], [0.252194, 0.269783, 0.531579], [0.250425, 0.274290, 0.533103], [0.248629, 0.278775, 0.534556], [0.246811, 0.283237, 0.535941], [0.244972, 0.287675, 0.537260], [0.243113, 0.292092, 0.538516], [0.241237, 0.296485, 0.539709], [0.239346, 0.300855, 0.540844], [0.237441, 0.305202, 0.541921], [0.235526, 0.309527, 0.542944], [0.233603, 0.313828, 0.543914], [0.231674, 0.318106, 0.544834], [0.229739, 0.322361, 0.545706], [0.227802, 0.326594, 0.546532], [0.225863, 0.330805, 0.547314], [0.223925, 0.334994, 0.548053], [0.221989, 0.339161, 0.548752], [0.220057, 0.343307, 0.549413], [0.218130, 0.347432, 0.550038], [0.216210, 0.351535, 0.550627], [0.214298, 0.355619, 0.551184], [0.212395, 0.359683, 0.551710], [0.210503, 0.363727, 0.552206], [0.208623, 0.367752, 0.552675], [0.206756, 0.371758, 0.553117], [0.204903, 0.375746, 0.553533], [0.203063, 0.379716, 0.553925], [0.201239, 0.383670, 0.554294], [0.199430, 0.387607, 0.554642], [0.197636, 0.391528, 0.554969], [0.195860, 0.395433, 0.555276], [0.194100, 0.399323, 0.555565], [0.192357, 0.403199, 0.555836], [0.190631, 0.407061, 0.556089], [0.188923, 0.410910, 0.556326], [0.187231, 0.414746, 0.556547], [0.185556, 0.418570, 0.556753], [0.183898, 0.422383, 0.556944], [0.182256, 0.426184, 0.557120], [0.180629, 0.429975, 0.557282], [0.179019, 0.433756, 0.557430], [0.177423, 0.437527, 0.557565], [0.175841, 0.441290, 0.557685], [0.174274, 0.445044, 0.557792], [0.172719, 0.448791, 0.557885], [0.171176, 0.452530, 0.557965], [0.169646, 0.456262, 0.558030], [0.168126, 0.459988, 0.558082], [0.166617, 0.463708, 0.558119], [0.165117, 0.467423, 0.558141], [0.163625, 0.471133, 0.558148], [0.162142, 0.474838, 0.558140], [0.160665, 0.478540, 0.558115], [0.159194, 0.482237, 0.558073], [0.157729, 0.485932, 0.558013], [0.156270, 0.489624, 0.557936], [0.154815, 0.493313, 0.557840], [0.153364, 0.497000, 0.557724], [0.151918, 0.500685, 0.557587], [0.150476, 0.504369, 0.557430], [0.149039, 0.508051, 0.557250], [0.147607, 0.511733, 0.557049], [0.146180, 0.515413, 0.556823], [0.144759, 0.519093, 0.556572], [0.143343, 0.522773, 0.556295], [0.141935, 0.526453, 0.555991], [0.140536, 0.530132, 0.555659], [0.139147, 0.533812, 0.555298], [0.137770, 0.537492, 0.554906], [0.136408, 0.541173, 0.554483], [0.135066, 0.544853, 0.554029], [0.133743, 0.548535, 0.553541], [0.132444, 0.552216, 0.553018], [0.131172, 0.555899, 0.552459], [0.129933, 0.559582, 0.551864], [0.128729, 0.563265, 0.551229], [0.127568, 0.566949, 0.550556], [0.126453, 0.570633, 0.549841], [0.125394, 0.574318, 0.549086], [0.124395, 0.578002, 0.548287], [0.123463, 0.581687, 0.547445], [0.122606, 0.585371, 0.546557], [0.121831, 0.589055, 0.545623], [0.121148, 0.592739, 0.544641], [0.120565, 0.596422, 0.543611], [0.120092, 0.600104, 0.542530], [0.119738, 0.603785, 0.541400], [0.119512, 0.607464, 0.540218], [0.119423, 0.611141, 0.538982], [0.119483, 0.614817, 0.537692], [0.119699, 0.618490, 0.536347], [0.120081, 0.622161, 0.534946], [0.120638, 0.625828, 0.533488], [0.121380, 0.629492, 0.531973], [0.122312, 0.633153, 0.530398], [0.123444, 0.636809, 0.528763], [0.124780, 0.640461, 0.527068], [0.126326, 0.644107, 0.525311], [0.128087, 0.647749, 0.523491], [0.130067, 0.651384, 0.521608], [0.132268, 0.655014, 0.519661], [0.134692, 0.658636, 0.517649], [0.137339, 0.662252, 0.515571], [0.140210, 0.665859, 0.513427], [0.143303, 0.669459, 0.511215], [0.146616, 0.673050, 0.508936], [0.150148, 0.676631, 0.506589], [0.153894, 0.680203, 0.504172], [0.157851, 0.683765, 0.501686], [0.162016, 0.687316, 0.499129], [0.166383, 0.690856, 0.496502], [0.170948, 0.694384, 0.493803], [0.175707, 0.697900, 0.491033], [0.180653, 0.701402, 0.488189], [0.185783, 0.704891, 0.485273], [0.191090, 0.708366, 0.482284], [0.196571, 0.711827, 0.479221], [0.202219, 0.715272, 0.476084], [0.208030, 0.718701, 0.472873], [0.214000, 0.722114, 0.469588], [0.220124, 0.725509, 0.466226], [0.226397, 0.728888, 0.462789], [0.232815, 0.732247, 0.459277], [0.239374, 0.735588, 0.455688], [0.246070, 0.738910, 0.452024], [0.252899, 0.742211, 0.448284], [0.259857, 0.745492, 0.444467], [0.266941, 0.748751, 0.440573], [0.274149, 0.751988, 0.436601], [0.281477, 0.755203, 0.432552], [0.288921, 0.758394, 0.428426], [0.296479, 0.761561, 0.424223], [0.304148, 0.764704, 0.419943], [0.311925, 0.767822, 0.415586], [0.319809, 0.770914, 0.411152], [0.327796, 0.773980, 0.406640], [0.335885, 0.777018, 0.402049], [0.344074, 0.780029, 0.397381], [0.352360, 0.783011, 0.392636], [0.360741, 0.785964, 0.387814], [0.369214, 0.788888, 0.382914], [0.377779, 0.791781, 0.377939], [0.386433, 0.794644, 0.372886], [0.395174, 0.797475, 0.367757], [0.404001, 0.800275, 0.362552], [0.412913, 0.803041, 0.357269], [0.421908, 0.805774, 0.351910], [0.430983, 0.808473, 0.346476], [0.440137, 0.811138, 0.340967], [0.449368, 0.813768, 0.335384], [0.458674, 0.816363, 0.329727], [0.468053, 0.818921, 0.323998], [0.477504, 0.821444, 0.318195], [0.487026, 0.823929, 0.312321], [0.496615, 0.826376, 0.306377], [0.506271, 0.828786, 0.300362], [0.515992, 0.831158, 0.294279], [0.525776, 0.833491, 0.288127], [0.535621, 0.835785, 0.281908], [0.545524, 0.838039, 0.275626], [0.555484, 0.840254, 0.269281], [0.565498, 0.842430, 0.262877], [0.575563, 0.844566, 0.256415], [0.585678, 0.846661, 0.249897], [0.595839, 0.848717, 0.243329], [0.606045, 0.850733, 0.236712], [0.616293, 0.852709, 0.230052], [0.626579, 0.854645, 0.223353], [0.636902, 0.856542, 0.216620], [0.647257, 0.858400, 0.209861], [0.657642, 0.860219, 0.203082], [0.668054, 0.861999, 0.196293], [0.678489, 0.863742, 0.189503], [0.688944, 0.865448, 0.182725], [0.699415, 0.867117, 0.175971], [0.709898, 0.868751, 0.169257], [0.720391, 0.870350, 0.162603], [0.730889, 0.871916, 0.156029], [0.741388, 0.873449, 0.149561], [0.751884, 0.874951, 0.143228], [0.762373, 0.876424, 0.137064], [0.772852, 0.877868, 0.131109], [0.783315, 0.879285, 0.125405], [0.793760, 0.880678, 0.120005], [0.804182, 0.882046, 0.114965], [0.814576, 0.883393, 0.110347], [0.824940, 0.884720, 0.106217], [0.835270, 0.886029, 0.102646], [0.845561, 0.887322, 0.099702], [0.855810, 0.888601, 0.097452], [0.866013, 0.889868, 0.095953], [0.876168, 0.891125, 0.095250], [0.886271, 0.892374, 0.095374], [0.896320, 0.893616, 0.096335], [0.906311, 0.894855, 0.098125], [0.916242, 0.896091, 0.100717], [0.926106, 0.897330, 0.104071], [0.935904, 0.898570, 0.108131], [0.945636, 0.899815, 0.112838], [0.955300, 0.901065, 0.118128], [0.964894, 0.902323, 0.123941], [0.974417, 0.903590, 0.130215], [0.983868, 0.904867, 0.136897], [0.993248, 0.906157, 0.143936]]));
JS9.checkNew(new JS9.Colormap("magma",
[[0.001462, 0.000466, 0.013866], [0.002258, 0.001295, 0.018331], [0.003279, 0.002305, 0.023708], [0.004512, 0.003490, 0.029965], [0.005950, 0.004843, 0.037130], [0.007588, 0.006356, 0.044973], [0.009426, 0.008022, 0.052844], [0.011465, 0.009828, 0.060750], [0.013708, 0.011771, 0.068667], [0.016156, 0.013840, 0.076603], [0.018815, 0.016026, 0.084584], [0.021692, 0.018320, 0.092610], [0.024792, 0.020715, 0.100676], [0.028123, 0.023201, 0.108787], [0.031696, 0.025765, 0.116965], [0.035520, 0.028397, 0.125209], [0.039608, 0.031090, 0.133515], [0.043830, 0.033830, 0.141886], [0.048062, 0.036607, 0.150327], [0.052320, 0.039407, 0.158841], [0.056615, 0.042160, 0.167446], [0.060949, 0.044794, 0.176129], [0.065330, 0.047318, 0.184892], [0.069764, 0.049726, 0.193735], [0.074257, 0.052017, 0.202660], [0.078815, 0.054184, 0.211667], [0.083446, 0.056225, 0.220755], [0.088155, 0.058133, 0.229922], [0.092949, 0.059904, 0.239164], [0.097833, 0.061531, 0.248477], [0.102815, 0.063010, 0.257854], [0.107899, 0.064335, 0.267289], [0.113094, 0.065492, 0.276784], [0.118405, 0.066479, 0.286321], [0.123833, 0.067295, 0.295879], [0.129380, 0.067935, 0.305443], [0.135053, 0.068391, 0.315000], [0.140858, 0.068654, 0.324538], [0.146785, 0.068738, 0.334011], [0.152839, 0.068637, 0.343404], [0.159018, 0.068354, 0.352688], [0.165308, 0.067911, 0.361816], [0.171713, 0.067305, 0.370771], [0.178212, 0.066576, 0.379497], [0.184801, 0.065732, 0.387973], [0.191460, 0.064818, 0.396152], [0.198177, 0.063862, 0.404009], [0.204935, 0.062907, 0.411514], [0.211718, 0.061992, 0.418647], [0.218512, 0.061158, 0.425392], [0.225302, 0.060445, 0.431742], [0.232077, 0.059889, 0.437695], [0.238826, 0.059517, 0.443256], [0.245543, 0.059352, 0.448436], [0.252220, 0.059415, 0.453248], [0.258857, 0.059706, 0.457710], [0.265447, 0.060237, 0.461840], [0.271994, 0.060994, 0.465660], [0.278493, 0.061978, 0.469190], [0.284951, 0.063168, 0.472451], [0.291366, 0.064553, 0.475462], [0.297740, 0.066117, 0.478243], [0.304081, 0.067835, 0.480812], [0.310382, 0.069702, 0.483186], [0.316654, 0.071690, 0.485380], [0.322899, 0.073782, 0.487408], [0.329114, 0.075972, 0.489287], [0.335308, 0.078236, 0.491024], [0.341482, 0.080564, 0.492631], [0.347636, 0.082946, 0.494121], [0.353773, 0.085373, 0.495501], [0.359898, 0.087831, 0.496778], [0.366012, 0.090314, 0.497960], [0.372116, 0.092816, 0.499053], [0.378211, 0.095332, 0.500067], [0.384299, 0.097855, 0.501002], [0.390384, 0.100379, 0.501864], [0.396467, 0.102902, 0.502658], [0.402548, 0.105420, 0.503386], [0.408629, 0.107930, 0.504052], [0.414709, 0.110431, 0.504662], [0.420791, 0.112920, 0.505215], [0.426877, 0.115395, 0.505714], [0.432967, 0.117855, 0.506160], [0.439062, 0.120298, 0.506555], [0.445163, 0.122724, 0.506901], [0.451271, 0.125132, 0.507198], [0.457386, 0.127522, 0.507448], [0.463508, 0.129893, 0.507652], [0.469640, 0.132245, 0.507809], [0.475780, 0.134577, 0.507921], [0.481929, 0.136891, 0.507989], [0.488088, 0.139186, 0.508011], [0.494258, 0.141462, 0.507988], [0.500438, 0.143719, 0.507920], [0.506629, 0.145958, 0.507806], [0.512831, 0.148179, 0.507648], [0.519045, 0.150383, 0.507443], [0.525270, 0.152569, 0.507192], [0.531507, 0.154739, 0.506895], [0.537755, 0.156894, 0.506551], [0.544015, 0.159033, 0.506159], [0.550287, 0.161158, 0.505719], [0.556571, 0.163269, 0.505230], [0.562866, 0.165368, 0.504692], [0.569172, 0.167454, 0.504105], [0.575490, 0.169530, 0.503466], [0.581819, 0.171596, 0.502777], [0.588158, 0.173652, 0.502035], [0.594508, 0.175701, 0.501241], [0.600868, 0.177743, 0.500394], [0.607238, 0.179779, 0.499492], [0.613617, 0.181811, 0.498536], [0.620005, 0.183840, 0.497524], [0.626401, 0.185867, 0.496456], [0.632805, 0.187893, 0.495332], [0.639216, 0.189921, 0.494150], [0.645633, 0.191952, 0.492910], [0.652056, 0.193986, 0.491611], [0.658483, 0.196027, 0.490253], [0.664915, 0.198075, 0.488836], [0.671349, 0.200133, 0.487358], [0.677786, 0.202203, 0.485819], [0.684224, 0.204286, 0.484219], [0.690661, 0.206384, 0.482558], [0.697098, 0.208501, 0.480835], [0.703532, 0.210638, 0.479049], [0.709962, 0.212797, 0.477201], [0.716387, 0.214982, 0.475290], [0.722805, 0.217194, 0.473316], [0.729216, 0.219437, 0.471279], [0.735616, 0.221713, 0.469180], [0.742004, 0.224025, 0.467018], [0.748378, 0.226377, 0.464794], [0.754737, 0.228772, 0.462509], [0.761077, 0.231214, 0.460162], [0.767398, 0.233705, 0.457755], [0.773695, 0.236249, 0.455289], [0.779968, 0.238851, 0.452765], [0.786212, 0.241514, 0.450184], [0.792427, 0.244242, 0.447543], [0.798608, 0.247040, 0.444848], [0.804752, 0.249911, 0.442102], [0.810855, 0.252861, 0.439305], [0.816914, 0.255895, 0.436461], [0.822926, 0.259016, 0.433573], [0.828886, 0.262229, 0.430644], [0.834791, 0.265540, 0.427671], [0.840636, 0.268953, 0.424666], [0.846416, 0.272473, 0.421631], [0.852126, 0.276106, 0.418573], [0.857763, 0.279857, 0.415496], [0.863320, 0.283729, 0.412403], [0.868793, 0.287728, 0.409303], [0.874176, 0.291859, 0.406205], [0.879464, 0.296125, 0.403118], [0.884651, 0.300530, 0.400047], [0.889731, 0.305079, 0.397002], [0.894700, 0.309773, 0.393995], [0.899552, 0.314616, 0.391037], [0.904281, 0.319610, 0.388137], [0.908884, 0.324755, 0.385308], [0.913354, 0.330052, 0.382563], [0.917689, 0.335500, 0.379915], [0.921884, 0.341098, 0.377376], [0.925937, 0.346844, 0.374959], [0.929845, 0.352734, 0.372677], [0.933606, 0.358764, 0.370541], [0.937221, 0.364929, 0.368567], [0.940687, 0.371224, 0.366762], [0.944006, 0.377643, 0.365136], [0.947180, 0.384178, 0.363701], [0.950210, 0.390820, 0.362468], [0.953099, 0.397563, 0.361438], [0.955849, 0.404400, 0.360619], [0.958464, 0.411324, 0.360014], [0.960949, 0.418323, 0.359630], [0.963310, 0.425390, 0.359469], [0.965549, 0.432519, 0.359529], [0.967671, 0.439703, 0.359810], [0.969680, 0.446936, 0.360311], [0.971582, 0.454210, 0.361030], [0.973381, 0.461520, 0.361965], [0.975082, 0.468861, 0.363111], [0.976690, 0.476226, 0.364466], [0.978210, 0.483612, 0.366025], [0.979645, 0.491014, 0.367783], [0.981000, 0.498428, 0.369734], [0.982279, 0.505851, 0.371874], [0.983485, 0.513280, 0.374198], [0.984622, 0.520713, 0.376698], [0.985693, 0.528148, 0.379371], [0.986700, 0.535582, 0.382210], [0.987646, 0.543015, 0.385210], [0.988533, 0.550446, 0.388365], [0.989363, 0.557873, 0.391671], [0.990138, 0.565296, 0.395122], [0.990871, 0.572706, 0.398714], [0.991558, 0.580107, 0.402441], [0.992196, 0.587502, 0.406299], [0.992785, 0.594891, 0.410283], [0.993326, 0.602275, 0.414390], [0.993834, 0.609644, 0.418613], [0.994309, 0.616999, 0.422950], [0.994738, 0.624350, 0.427397], [0.995122, 0.631696, 0.431951], [0.995480, 0.639027, 0.436607], [0.995810, 0.646344, 0.441361], [0.996096, 0.653659, 0.446213], [0.996341, 0.660969, 0.451160], [0.996580, 0.668256, 0.456192], [0.996775, 0.675541, 0.461314], [0.996925, 0.682828, 0.466526], [0.997077, 0.690088, 0.471811], [0.997186, 0.697349, 0.477182], [0.997254, 0.704611, 0.482635], [0.997325, 0.711848, 0.488154], [0.997351, 0.719089, 0.493755], [0.997351, 0.726324, 0.499428], [0.997341, 0.733545, 0.505167], [0.997285, 0.740772, 0.510983], [0.997228, 0.747981, 0.516859], [0.997138, 0.755190, 0.522806], [0.997019, 0.762398, 0.528821], [0.996898, 0.769591, 0.534892], [0.996727, 0.776795, 0.541039], [0.996571, 0.783977, 0.547233], [0.996369, 0.791167, 0.553499], [0.996162, 0.798348, 0.559820], [0.995932, 0.805527, 0.566202], [0.995680, 0.812706, 0.572645], [0.995424, 0.819875, 0.579140], [0.995131, 0.827052, 0.585701], [0.994851, 0.834213, 0.592307], [0.994524, 0.841387, 0.598983], [0.994222, 0.848540, 0.605696], [0.993866, 0.855711, 0.612482], [0.993545, 0.862859, 0.619299], [0.993170, 0.870024, 0.626189], [0.992831, 0.877168, 0.633109], [0.992440, 0.884330, 0.640099], [0.992089, 0.891470, 0.647116], [0.991688, 0.898627, 0.654202], [0.991332, 0.905763, 0.661309], [0.990930, 0.912915, 0.668481], [0.990570, 0.920049, 0.675675], [0.990175, 0.927196, 0.682926], [0.989815, 0.934329, 0.690198], [0.989434, 0.941470, 0.697519], [0.989077, 0.948604, 0.704863], [0.988717, 0.955742, 0.712242], [0.988367, 0.962878, 0.719649], [0.988033, 0.970012, 0.727077], [0.987691, 0.977154, 0.734536], [0.987387, 0.984288, 0.742002], [0.987053, 0.991438, 0.749504]]));
JS9.checkNew(new JS9.Colormap("inferno", [[0.001462, 0.000466, 0.013866], [0.002267, 0.001270, 0.018570], [0.003299, 0.002249, 0.024239], [0.004547, 0.003392, 0.030909], [0.006006, 0.004692, 0.038558], [0.007676, 0.006136, 0.046836], [0.009561, 0.007713, 0.055143], [0.011663, 0.009417, 0.063460], [0.013995, 0.011225, 0.071862], [0.016561, 0.013136, 0.080282], [0.019373, 0.015133, 0.088767], [0.022447, 0.017199, 0.097327], [0.025793, 0.019331, 0.105930], [0.029432, 0.021503, 0.114621], [0.033385, 0.023702, 0.123397], [0.037668, 0.025921, 0.132232], [0.042253, 0.028139, 0.141141], [0.046915, 0.030324, 0.150164], [0.051644, 0.032474, 0.159254], [0.056449, 0.034569, 0.168414], [0.061340, 0.036590, 0.177642], [0.066331, 0.038504, 0.186962], [0.071429, 0.040294, 0.196354], [0.076637, 0.041905, 0.205799], [0.081962, 0.043328, 0.215289], [0.087411, 0.044556, 0.224813], [0.092990, 0.045583, 0.234358], [0.098702, 0.046402, 0.243904], [0.104551, 0.047008, 0.253430], [0.110536, 0.047399, 0.262912], [0.116656, 0.047574, 0.272321], [0.122908, 0.047536, 0.281624], [0.129285, 0.047293, 0.290788], [0.135778, 0.046856, 0.299776], [0.142378, 0.046242, 0.308553], [0.149073, 0.045468, 0.317085], [0.155850, 0.044559, 0.325338], [0.162689, 0.043554, 0.333277], [0.169575, 0.042489, 0.340874], [0.176493, 0.041402, 0.348111], [0.183429, 0.040329, 0.354971], [0.190367, 0.039309, 0.361447], [0.197297, 0.038400, 0.367535], [0.204209, 0.037632, 0.373238], [0.211095, 0.037030, 0.378563], [0.217949, 0.036615, 0.383522], [0.224763, 0.036405, 0.388129], [0.231538, 0.036405, 0.392400], [0.238273, 0.036621, 0.396353], [0.244967, 0.037055, 0.400007], [0.251620, 0.037705, 0.403378], [0.258234, 0.038571, 0.406485], [0.264810, 0.039647, 0.409345], [0.271347, 0.040922, 0.411976], [0.277850, 0.042353, 0.414392], [0.284321, 0.043933, 0.416608], [0.290763, 0.045644, 0.418637], [0.297178, 0.047470, 0.420491], [0.303568, 0.049396, 0.422182], [0.309935, 0.051407, 0.423721], [0.316282, 0.053490, 0.425116], [0.322610, 0.055634, 0.426377], [0.328921, 0.057827, 0.427511], [0.335217, 0.060060, 0.428524], [0.341500, 0.062325, 0.429425], [0.347771, 0.064616, 0.430217], [0.354032, 0.066925, 0.430906], [0.360284, 0.069247, 0.431497], [0.366529, 0.071579, 0.431994], [0.372768, 0.073915, 0.432400], [0.379001, 0.076253, 0.432719], [0.385228, 0.078591, 0.432955], [0.391453, 0.080927, 0.433109], [0.397674, 0.083257, 0.433183], [0.403894, 0.085580, 0.433179], [0.410113, 0.087896, 0.433098], [0.416331, 0.090203, 0.432943], [0.422549, 0.092501, 0.432714], [0.428768, 0.094790, 0.432412], [0.434987, 0.097069, 0.432039], [0.441207, 0.099338, 0.431594], [0.447428, 0.101597, 0.431080], [0.453651, 0.103848, 0.430498], [0.459875, 0.106089, 0.429846], [0.466100, 0.108322, 0.429125], [0.472328, 0.110547, 0.428334], [0.478558, 0.112764, 0.427475], [0.484789, 0.114974, 0.426548], [0.491022, 0.117179, 0.425552], [0.497257, 0.119379, 0.424488], [0.503493, 0.121575, 0.423356], [0.509730, 0.123769, 0.422156], [0.515967, 0.125960, 0.420887], [0.522206, 0.128150, 0.419549], [0.528444, 0.130341, 0.418142], [0.534683, 0.132534, 0.416667], [0.540920, 0.134729, 0.415123], [0.547157, 0.136929, 0.413511], [0.553392, 0.139134, 0.411829], [0.559624, 0.141346, 0.410078], [0.565854, 0.143567, 0.408258], [0.572081, 0.145797, 0.406369], [0.578304, 0.148039, 0.404411], [0.584521, 0.150294, 0.402385], [0.590734, 0.152563, 0.400290], [0.596940, 0.154848, 0.398125], [0.603139, 0.157151, 0.395891], [0.609330, 0.159474, 0.393589], [0.615513, 0.161817, 0.391219], [0.621685, 0.164184, 0.388781], [0.627847, 0.166575, 0.386276], [0.633998, 0.168992, 0.383704], [0.640135, 0.171438, 0.381065], [0.646260, 0.173914, 0.378359], [0.652369, 0.176421, 0.375586], [0.658463, 0.178962, 0.372748], [0.664540, 0.181539, 0.369846], [0.670599, 0.184153, 0.366879], [0.676638, 0.186807, 0.363849], [0.682656, 0.189501, 0.360757], [0.688653, 0.192239, 0.357603], [0.694627, 0.195021, 0.354388], [0.700576, 0.197851, 0.351113], [0.706500, 0.200728, 0.347777], [0.712396, 0.203656, 0.344383], [0.718264, 0.206636, 0.340931], [0.724103, 0.209670, 0.337424], [0.729909, 0.212759, 0.333861], [0.735683, 0.215906, 0.330245], [0.741423, 0.219112, 0.326576], [0.747127, 0.222378, 0.322856], [0.752794, 0.225706, 0.319085], [0.758422, 0.229097, 0.315266], [0.764010, 0.232554, 0.311399], [0.769556, 0.236077, 0.307485], [0.775059, 0.239667, 0.303526], [0.780517, 0.243327, 0.299523], [0.785929, 0.247056, 0.295477], [0.791293, 0.250856, 0.291390], [0.796607, 0.254728, 0.287264], [0.801871, 0.258674, 0.283099], [0.807082, 0.262692, 0.278898], [0.812239, 0.266786, 0.274661], [0.817341, 0.270954, 0.270390], [0.822386, 0.275197, 0.266085], [0.827372, 0.279517, 0.261750], [0.832299, 0.283913, 0.257383], [0.837165, 0.288385, 0.252988], [0.841969, 0.292933, 0.248564], [0.846709, 0.297559, 0.244113], [0.851384, 0.302260, 0.239636], [0.855992, 0.307038, 0.235133], [0.860533, 0.311892, 0.230606], [0.865006, 0.316822, 0.226055], [0.869409, 0.321827, 0.221482], [0.873741, 0.326906, 0.216886], [0.878001, 0.332060, 0.212268], [0.882188, 0.337287, 0.207628], [0.886302, 0.342586, 0.202968], [0.890341, 0.347957, 0.198286], [0.894305, 0.353399, 0.193584], [0.898192, 0.358911, 0.188860], [0.902003, 0.364492, 0.184116], [0.905735, 0.370140, 0.179350], [0.909390, 0.375856, 0.174563], [0.912966, 0.381636, 0.169755], [0.916462, 0.387481, 0.164924], [0.919879, 0.393389, 0.160070], [0.923215, 0.399359, 0.155193], [0.926470, 0.405389, 0.150292], [0.929644, 0.411479, 0.145367], [0.932737, 0.417627, 0.140417], [0.935747, 0.423831, 0.135440], [0.938675, 0.430091, 0.130438], [0.941521, 0.436405, 0.125409], [0.944285, 0.442772, 0.120354], [0.946965, 0.449191, 0.115272], [0.949562, 0.455660, 0.110164], [0.952075, 0.462178, 0.105031], [0.954506, 0.468744, 0.099874], [0.956852, 0.475356, 0.094695], [0.959114, 0.482014, 0.089499], [0.961293, 0.488716, 0.084289], [0.963387, 0.495462, 0.079073], [0.965397, 0.502249, 0.073859], [0.967322, 0.509078, 0.068659], [0.969163, 0.515946, 0.063488], [0.970919, 0.522853, 0.058367], [0.972590, 0.529798, 0.053324], [0.974176, 0.536780, 0.048392], [0.975677, 0.543798, 0.043618], [0.977092, 0.550850, 0.039050], [0.978422, 0.557937, 0.034931], [0.979666, 0.565057, 0.031409], [0.980824, 0.572209, 0.028508], [0.981895, 0.579392, 0.026250], [0.982881, 0.586606, 0.024661], [0.983779, 0.593849, 0.023770], [0.984591, 0.601122, 0.023606], [0.985315, 0.608422, 0.024202], [0.985952, 0.615750, 0.025592], [0.986502, 0.623105, 0.027814], [0.986964, 0.630485, 0.030908], [0.987337, 0.637890, 0.034916], [0.987622, 0.645320, 0.039886], [0.987819, 0.652773, 0.045581], [0.987926, 0.660250, 0.051750], [0.987945, 0.667748, 0.058329], [0.987874, 0.675267, 0.065257], [0.987714, 0.682807, 0.072489], [0.987464, 0.690366, 0.079990], [0.987124, 0.697944, 0.087731], [0.986694, 0.705540, 0.095694], [0.986175, 0.713153, 0.103863], [0.985566, 0.720782, 0.112229], [0.984865, 0.728427, 0.120785], [0.984075, 0.736087, 0.129527], [0.983196, 0.743758, 0.138453], [0.982228, 0.751442, 0.147565], [0.981173, 0.759135, 0.156863], [0.980032, 0.766837, 0.166353], [0.978806, 0.774545, 0.176037], [0.977497, 0.782258, 0.185923], [0.976108, 0.789974, 0.196018], [0.974638, 0.797692, 0.206332], [0.973088, 0.805409, 0.216877], [0.971468, 0.813122, 0.227658], [0.969783, 0.820825, 0.238686], [0.968041, 0.828515, 0.249972], [0.966243, 0.836191, 0.261534], [0.964394, 0.843848, 0.273391], [0.962517, 0.851476, 0.285546], [0.960626, 0.859069, 0.298010], [0.958720, 0.866624, 0.310820], [0.956834, 0.874129, 0.323974], [0.954997, 0.881569, 0.337475], [0.953215, 0.888942, 0.351369], [0.951546, 0.896226, 0.365627], [0.950018, 0.903409, 0.380271], [0.948683, 0.910473, 0.395289], [0.947594, 0.917399, 0.410665], [0.946809, 0.924168, 0.426373], [0.946392, 0.930761, 0.442367], [0.946403, 0.937159, 0.458592], [0.946903, 0.943348, 0.474970], [0.947937, 0.949318, 0.491426], [0.949545, 0.955063, 0.507860], [0.951740, 0.960587, 0.524203], [0.954529, 0.965896, 0.540361], [0.957896, 0.971003, 0.556275], [0.961812, 0.975924, 0.571925], [0.966249, 0.980678, 0.587206], [0.971162, 0.985282, 0.602154], [0.976511, 0.989753, 0.616760], [0.982257, 0.994109, 0.631017], [0.988362, 0.998364, 0.644924]]));
JS9.checkNew(new JS9.Colormap("plasma", [[0.050383, 0.029803, 0.527975], [0.063536, 0.028426, 0.533124], [0.075353, 0.027206, 0.538007], [0.086222, 0.026125, 0.542658], [0.096379, 0.025165, 0.547103], [0.105980, 0.024309, 0.551368], [0.115124, 0.023556, 0.555468], [0.123903, 0.022878, 0.559423], [0.132381, 0.022258, 0.563250], [0.140603, 0.021687, 0.566959], [0.148607, 0.021154, 0.570562], [0.156421, 0.020651, 0.574065], [0.164070, 0.020171, 0.577478], [0.171574, 0.019706, 0.580806], [0.178950, 0.019252, 0.584054], [0.186213, 0.018803, 0.587228], [0.193374, 0.018354, 0.590330], [0.200445, 0.017902, 0.593364], [0.207435, 0.017442, 0.596333], [0.214350, 0.016973, 0.599239], [0.221197, 0.016497, 0.602083], [0.227983, 0.016007, 0.604867], [0.234715, 0.015502, 0.607592], [0.241396, 0.014979, 0.610259], [0.248032, 0.014439, 0.612868], [0.254627, 0.013882, 0.615419], [0.261183, 0.013308, 0.617911], [0.267703, 0.012716, 0.620346], [0.274191, 0.012109, 0.622722], [0.280648, 0.011488, 0.625038], [0.287076, 0.010855, 0.627295], [0.293478, 0.010213, 0.629490], [0.299855, 0.009561, 0.631624], [0.306210, 0.008902, 0.633694], [0.312543, 0.008239, 0.635700], [0.318856, 0.007576, 0.637640], [0.325150, 0.006915, 0.639512], [0.331426, 0.006261, 0.641316], [0.337683, 0.005618, 0.643049], [0.343925, 0.004991, 0.644710], [0.350150, 0.004382, 0.646298], [0.356359, 0.003798, 0.647810], [0.362553, 0.003243, 0.649245], [0.368733, 0.002724, 0.650601], [0.374897, 0.002245, 0.651876], [0.381047, 0.001814, 0.653068], [0.387183, 0.001434, 0.654177], [0.393304, 0.001114, 0.655199], [0.399411, 0.000859, 0.656133], [0.405503, 0.000678, 0.656977], [0.411580, 0.000577, 0.657730], [0.417642, 0.000564, 0.658390], [0.423689, 0.000646, 0.658956], [0.429719, 0.000831, 0.659425], [0.435734, 0.001127, 0.659797], [0.441732, 0.001540, 0.660069], [0.447714, 0.002080, 0.660240], [0.453677, 0.002755, 0.660310], [0.459623, 0.003574, 0.660277], [0.465550, 0.004545, 0.660139], [0.471457, 0.005678, 0.659897], [0.477344, 0.006980, 0.659549], [0.483210, 0.008460, 0.659095], [0.489055, 0.010127, 0.658534], [0.494877, 0.011990, 0.657865], [0.500678, 0.014055, 0.657088], [0.506454, 0.016333, 0.656202], [0.512206, 0.018833, 0.655209], [0.517933, 0.021563, 0.654109], [0.523633, 0.024532, 0.652901], [0.529306, 0.027747, 0.651586], [0.534952, 0.031217, 0.650165], [0.540570, 0.034950, 0.648640], [0.546157, 0.038954, 0.647010], [0.551715, 0.043136, 0.645277], [0.557243, 0.047331, 0.643443], [0.562738, 0.051545, 0.641509], [0.568201, 0.055778, 0.639477], [0.573632, 0.060028, 0.637349], [0.579029, 0.064296, 0.635126], [0.584391, 0.068579, 0.632812], [0.589719, 0.072878, 0.630408], [0.595011, 0.077190, 0.627917], [0.600266, 0.081516, 0.625342], [0.605485, 0.085854, 0.622686], [0.610667, 0.090204, 0.619951], [0.615812, 0.094564, 0.617140], [0.620919, 0.098934, 0.614257], [0.625987, 0.103312, 0.611305], [0.631017, 0.107699, 0.608287], [0.636008, 0.112092, 0.605205], [0.640959, 0.116492, 0.602065], [0.645872, 0.120898, 0.598867], [0.650746, 0.125309, 0.595617], [0.655580, 0.129725, 0.592317], [0.660374, 0.134144, 0.588971], [0.665129, 0.138566, 0.585582], [0.669845, 0.142992, 0.582154], [0.674522, 0.147419, 0.578688], [0.679160, 0.151848, 0.575189], [0.683758, 0.156278, 0.571660], [0.688318, 0.160709, 0.568103], [0.692840, 0.165141, 0.564522], [0.697324, 0.169573, 0.560919], [0.701769, 0.174005, 0.557296], [0.706178, 0.178437, 0.553657], [0.710549, 0.182868, 0.550004], [0.714883, 0.187299, 0.546338], [0.719181, 0.191729, 0.542663], [0.723444, 0.196158, 0.538981], [0.727670, 0.200586, 0.535293], [0.731862, 0.205013, 0.531601], [0.736019, 0.209439, 0.527908], [0.740143, 0.213864, 0.524216], [0.744232, 0.218288, 0.520524], [0.748289, 0.222711, 0.516834], [0.752312, 0.227133, 0.513149], [0.756304, 0.231555, 0.509468], [0.760264, 0.235976, 0.505794], [0.764193, 0.240396, 0.502126], [0.768090, 0.244817, 0.498465], [0.771958, 0.249237, 0.494813], [0.775796, 0.253658, 0.491171], [0.779604, 0.258078, 0.487539], [0.783383, 0.262500, 0.483918], [0.787133, 0.266922, 0.480307], [0.790855, 0.271345, 0.476706], [0.794549, 0.275770, 0.473117], [0.798216, 0.280197, 0.469538], [0.801855, 0.284626, 0.465971], [0.805467, 0.289057, 0.462415], [0.809052, 0.293491, 0.458870], [0.812612, 0.297928, 0.455338], [0.816144, 0.302368, 0.451816], [0.819651, 0.306812, 0.448306], [0.823132, 0.311261, 0.444806], [0.826588, 0.315714, 0.441316], [0.830018, 0.320172, 0.437836], [0.833422, 0.324635, 0.434366], [0.836801, 0.329105, 0.430905], [0.840155, 0.333580, 0.427455], [0.843484, 0.338062, 0.424013], [0.846788, 0.342551, 0.420579], [0.850066, 0.347048, 0.417153], [0.853319, 0.351553, 0.413734], [0.856547, 0.356066, 0.410322], [0.859750, 0.360588, 0.406917], [0.862927, 0.365119, 0.403519], [0.866078, 0.369660, 0.400126], [0.869203, 0.374212, 0.396738], [0.872303, 0.378774, 0.393355], [0.875376, 0.383347, 0.389976], [0.878423, 0.387932, 0.386600], [0.881443, 0.392529, 0.383229], [0.884436, 0.397139, 0.379860], [0.887402, 0.401762, 0.376494], [0.890340, 0.406398, 0.373130], [0.893250, 0.411048, 0.369768], [0.896131, 0.415712, 0.366407], [0.898984, 0.420392, 0.363047], [0.901807, 0.425087, 0.359688], [0.904601, 0.429797, 0.356329], [0.907365, 0.434524, 0.352970], [0.910098, 0.439268, 0.349610], [0.912800, 0.444029, 0.346251], [0.915471, 0.448807, 0.342890], [0.918109, 0.453603, 0.339529], [0.920714, 0.458417, 0.336166], [0.923287, 0.463251, 0.332801], [0.925825, 0.468103, 0.329435], [0.928329, 0.472975, 0.326067], [0.930798, 0.477867, 0.322697], [0.933232, 0.482780, 0.319325], [0.935630, 0.487712, 0.315952], [0.937990, 0.492667, 0.312575], [0.940313, 0.497642, 0.309197], [0.942598, 0.502639, 0.305816], [0.944844, 0.507658, 0.302433], [0.947051, 0.512699, 0.299049], [0.949217, 0.517763, 0.295662], [0.951344, 0.522850, 0.292275], [0.953428, 0.527960, 0.288883], [0.955470, 0.533093, 0.285490], [0.957469, 0.538250, 0.282096], [0.959424, 0.543431, 0.278701], [0.961336, 0.548636, 0.275305], [0.963203, 0.553865, 0.271909], [0.965024, 0.559118, 0.268513], [0.966798, 0.564396, 0.265118], [0.968526, 0.569700, 0.261721], [0.970205, 0.575028, 0.258325], [0.971835, 0.580382, 0.254931], [0.973416, 0.585761, 0.251540], [0.974947, 0.591165, 0.248151], [0.976428, 0.596595, 0.244767], [0.977856, 0.602051, 0.241387], [0.979233, 0.607532, 0.238013], [0.980556, 0.613039, 0.234646], [0.981826, 0.618572, 0.231287], [0.983041, 0.624131, 0.227937], [0.984199, 0.629718, 0.224595], [0.985301, 0.635330, 0.221265], [0.986345, 0.640969, 0.217948], [0.987332, 0.646633, 0.214648], [0.988260, 0.652325, 0.211364], [0.989128, 0.658043, 0.208100], [0.989935, 0.663787, 0.204859], [0.990681, 0.669558, 0.201642], [0.991365, 0.675355, 0.198453], [0.991985, 0.681179, 0.195295], [0.992541, 0.687030, 0.192170], [0.993032, 0.692907, 0.189084], [0.993456, 0.698810, 0.186041], [0.993814, 0.704741, 0.183043], [0.994103, 0.710698, 0.180097], [0.994324, 0.716681, 0.177208], [0.994474, 0.722691, 0.174381], [0.994553, 0.728728, 0.171622], [0.994561, 0.734791, 0.168938], [0.994495, 0.740880, 0.166335], [0.994355, 0.746995, 0.163821], [0.994141, 0.753137, 0.161404], [0.993851, 0.759304, 0.159092], [0.993482, 0.765499, 0.156891], [0.993033, 0.771720, 0.154808], [0.992505, 0.777967, 0.152855], [0.991897, 0.784239, 0.151042], [0.991209, 0.790537, 0.149377], [0.990439, 0.796859, 0.147870], [0.989587, 0.803205, 0.146529], [0.988648, 0.809579, 0.145357], [0.987621, 0.815978, 0.144363], [0.986509, 0.822401, 0.143557], [0.985314, 0.828846, 0.142945], [0.984031, 0.835315, 0.142528], [0.982653, 0.841812, 0.142303], [0.981190, 0.848329, 0.142279], [0.979644, 0.854866, 0.142453], [0.977995, 0.861432, 0.142808], [0.976265, 0.868016, 0.143351], [0.974443, 0.874622, 0.144061], [0.972530, 0.881250, 0.144923], [0.970533, 0.887896, 0.145919], [0.968443, 0.894564, 0.147014], [0.966271, 0.901249, 0.148180], [0.964021, 0.907950, 0.149370], [0.961681, 0.914672, 0.150520], [0.959276, 0.921407, 0.151566], [0.956808, 0.928152, 0.152409], [0.954287, 0.934908, 0.152921], [0.951726, 0.941671, 0.152925], [0.949151, 0.948435, 0.152178], [0.946602, 0.955190, 0.150328], [0.944152, 0.961916, 0.146861], [0.941896, 0.968590, 0.140956], [0.940015, 0.975158, 0.131326]]));
// end of matlibplot colormaps
JS9.checkNew(new JS9.Colormap("i8",
[[0,0,0], [0,1,0], [0,0,1], [0,1,1],
[1,0,0], [1,1,0], [1,0,1], [1,1,1]]));
JS9.checkNew(new JS9.Colormap("aips0",
[[0.196,0.196,0.196], [0.475,0,0.608], [0,0,0.785], [0.373,0.655,0.925], [0,0.596,0], [0,0.965,0], [1,1,0], [1,0.694,0], [1,0,0]]));
JS9.checkNew(new JS9.Colormap("sls",
[[0, 0, 0], [0.043442, 0, 0.052883], [0.086883, 0, 0.105767], [0.130325, 0, 0.158650], [0.173767, 0, 0.211533], [0.217208, 0, 0.264417], [0.260650, 0, 0.317300], [0.304092, 0, 0.370183], [0.347533, 0, 0.423067], [0.390975, 0, 0.475950], [0.434417, 0, 0.528833], [0.477858, 0, 0.581717], [0.521300, 0, 0.634600], [0.506742, 0, 0.640217], [0.492183, 0, 0.645833], [0.477625, 0, 0.651450], [0.463067, 0, 0.657067], [0.448508, 0, 0.662683], [0.433950, 0, 0.668300], [0.419392, 0, 0.673917], [0.404833, 0, 0.679533], [0.390275, 0, 0.685150], [0.375717, 0, 0.690767], [0.361158, 0, 0.696383], [0.346600, 0, 0.7020], [0.317717, 0, 0.712192], [0.288833, 0, 0.722383], [0.259950, 0, 0.732575], [0.231067, 0, 0.742767], [0.202183, 0, 0.752958], [0.173300, 0, 0.763150], [0.144417, 0, 0.773342], [0.115533, 0, 0.783533], [0.086650, 0, 0.793725], [0.057767, 0, 0.803917], [0.028883, 0, 0.814108], [0, 0, 0.824300], [0, 0.019817, 0.838942], [0, 0.039633, 0.853583], [0, 0.059450, 0.868225], [0, 0.079267, 0.882867], [0, 0.099083, 0.897508], [0, 0.118900, 0.912150], [0, 0.138717, 0.926792], [0, 0.158533, 0.941433], [0, 0.178350, 0.956075], [0, 0.198167, 0.970717], [0, 0.217983, 0.985358], [0, 0.237800, 1], [0, 0.268533, 1], [0, 0.299267, 1], [0, 0.330, 1], [0, 0.360733, 1], [0, 0.391467, 1], [0, 0.422200, 1], [0, 0.452933, 1], [0, 0.483667, 1], [0, 0.514400, 1], [0, 0.545133, 1], [0, 0.575867, 1], [0, 0.606600, 1], [0, 0.631733, 0.975300], [0, 0.656867, 0.950600], [0, 0.682000, 0.925900], [0, 0.707133, 0.901200], [0, 0.732267, 0.876500], [0, 0.757400, 0.851800], [0, 0.782533, 0.827100], [0, 0.807667, 0.802400], [0, 0.832800, 0.777700], [0, 0.857933, 0.7530], [0, 0.883067, 0.728300], [0, 0.908200, 0.703600], [0, 0.901908, 0.676675], [0, 0.895617, 0.649750], [0, 0.889325, 0.622825], [0, 0.883033, 0.595900], [0, 0.876742, 0.568975], [0, 0.870450, 0.542050], [0, 0.864158, 0.515125], [0, 0.857867, 0.488200], [0, 0.851575, 0.461275], [0, 0.845283, 0.434350], [0, 0.838992, 0.407425], [0, 0.832700, 0.380500], [0, 0.832308, 0.354858], [0, 0.831917, 0.329217], [0, 0.831525, 0.303575], [0, 0.831133, 0.277933], [0, 0.830742, 0.252292], [0, 0.830350, 0.226650], [0, 0.829958, 0.201008], [0, 0.829567, 0.175367], [0, 0.829175, 0.149725], [0, 0.828783, 0.124083], [0, 0.828392, 0.098442], [0, 0.828000, 0.072800], [0.033167, 0.834167, 0.066733], [0.066333, 0.840333, 0.060667], [0.099500, 0.846500, 0.054600], [0.132667, 0.852667, 0.048533], [0.165833, 0.858833, 0.042467], [0.199000, 0.865000, 0.036400], [0.232167, 0.871167, 0.030333], [0.265333, 0.877333, 0.024267], [0.298500, 0.883500, 0.018200], [0.331667, 0.889667, 0.012133], [0.364833, 0.895833, 0.006067], [0.398000, 0.902000, 0], [0.430950, 0.902000, 0], [0.463900, 0.902000, 0], [0.496850, 0.902000, 0], [0.529800, 0.902000, 0], [0.562750, 0.902000, 0], [0.595700, 0.902000, 0], [0.628650, 0.902000, 0], [0.661600, 0.902000, 0], [0.694550, 0.902000, 0], [0.727500, 0.902000, 0], [0.760450, 0.902000, 0], [0.793400, 0.902000, 0], [0.810617, 0.897133, 0.003983], [0.827833, 0.892267, 0.007967], [0.845050, 0.887400, 0.011950], [0.862267, 0.882533, 0.015933], [0.879483, 0.877667, 0.019917], [0.896700, 0.872800, 0.023900], [0.913917, 0.867933, 0.027883], [0.931133, 0.863067, 0.031867], [0.948350, 0.858200, 0.035850], [0.965567, 0.853333, 0.039833], [0.982783, 0.848467, 0.043817], [1, 0.843600, 0.047800], [0.995725, 0.824892, 0.051600], [0.991450, 0.806183, 0.055400], [0.987175, 0.787475, 0.059200], [0.982900, 0.768767, 0.063000], [0.978625, 0.750058, 0.066800], [0.974350, 0.731350, 0.070600], [0.970075, 0.712642, 0.074400], [0.965800, 0.693933, 0.078200], [0.961525, 0.675225, 0.082000], [0.957250, 0.656517, 0.085800], [0.952975, 0.637808, 0.089600], [0.948700, 0.619100, 0.093400], [0.952975, 0.600408, 0.085617], [0.957250, 0.581717, 0.077833], [0.961525, 0.563025, 0.070050], [0.965800, 0.544333, 0.062267], [0.970075, 0.525642, 0.054483], [0.974350, 0.506950, 0.046700], [0.978625, 0.488258, 0.038917], [0.982900, 0.469567, 0.031133], [0.987175, 0.450875, 0.023350], [0.991450, 0.432183, 0.015567], [0.995725, 0.413492, 0.007783], [1, 0.394800, 0], [0.998342, 0.361900, 0], [0.996683, 0.329000, 0], [0.995025, 0.296100, 0], [0.993367, 0.263200, 0], [0.991708, 0.230300, 0], [0.990050, 0.197400, 0], [0.988392, 0.164500, 0], [0.986733, 0.131600, 0], [0.985075, 0.098700, 0], [0.983417, 0.065800, 0], [0.981758, 0.032900, 0], [0.980100, 0, 0], [0.955925, 0, 0], [0.931750, 0, 0], [0.907575, 0, 0], [0.883400, 0, 0], [0.859225, 0, 0], [0.835050, 0, 0], [0.810875, 0, 0], [0.786700, 0, 0], [0.762525, 0, 0], [0.738350, 0, 0], [0.714175, 0, 0], [0.690, 0, 0], [0.715833, 0.083333, 0.083333], [0.741667, 0.166667, 0.166667], [0.767500, 0.250, 0.250000], [0.793333, 0.333333, 0.333333], [0.819167, 0.416667, 0.416667], [0.845000, 0.500, 0.500000], [0.870833, 0.583333, 0.583333], [0.896667, 0.666667, 0.666667], [0.922500, 0.750, 0.750000], [0.948333, 0.833333, 0.833333], [0.974167, 0.916667, 0.916667], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]));
JS9.checkNew(new JS9.Colormap("a",
[[0,0], [0.25,0], [0.5,1], [1,1]],
[[0,0], [0.25,1], [0.5,0], [0.77,0], [1,1]],
[[0,0], [0.125,0], [0.5, 1], [0.64,0.5], [0.77, 0], [1,0]]));
JS9.checkNew(new JS9.Colormap("b",
[[0,0], [0.25,0], [0.5,1], [1,1]],
[[0,0], [0.5,0], [0.75,1], [1,1]],
[[0,0], [0.25,1], [0.5,0], [0.75,0], [1,1]]));
JS9.checkNew(new JS9.Colormap("bb",
[[0,0], [0.5,1], [1,1]],
[[0,0], [0.25,0], [0.75,1], [1,1]],
[[0,0], [0.5,0], [1,1]]));
JS9.checkNew(new JS9.Colormap("he",
[[0,0], [0.015,0.5], [0.25,0.5], [0.5,0.75], [1,1]],
[[0,0], [0.065,0], [0.125,0.5], [0.25,0.75], [0.5,0.81], [1,1]],
[[0,0], [0.015,0.125], [0.03,0.375], [0.065,0.625], [0.25,0.25], [1,1]]));
JS9.checkNew(new JS9.Colormap("hsv", (() => {
let i, frac, h, s, v, f, p, q, t, ii;
let cur = 0;
const size = 200;
const a = [];
for(i=0; i= 360.0 ){
h -= 360.0;
}
h /= 60.0;
ii = Math.floor(h);
f = h - ii;
p = v \* (1 - s);
q = v \* (1 - s\*f);
t = v \* (1 - s \* (1.0 - f));
a[cur] = [];
switch (ii){
case 0:
a[cur].push(v);
a[cur].push(t);
a[cur].push(p);
break;
case 1:
a[cur].push(q);
a[cur].push(v);
a[cur].push(p);
break;
case 2:
a[cur].push(p);
a[cur].push(v);
a[cur].push(t);
break;
case 3:
a[cur].push(p);
a[cur].push(q);
a[cur].push(v);
break;
case 4:
a[cur].push(t);
a[cur].push(p);
a[cur].push(v);
break;
case 5:
a[cur].push(v);
a[cur].push(p);
a[cur].push(q);
break;
default:
break;
}
}
return a;})()));
JS9.checkNew(new JS9.Colormap("rainbow",
[[0,1], [0.2,0], [0.6,0], [0.8,1], [1,1]],
[[0,0], [0.2,0], [0.4,1], [0.8,1], [1,0]],
[[0,1], [0.4,1], [0.6,0], [1,0]]));
JS9.checkNew(new JS9.Colormap("standard",
[[0,0], [0.333,0.3], [0.333,0], [0.666,0.3], [0.666,0.3], [1,1]],
[[0,0], [0.333,0.3], [0.333,0.3], [0.666,1], [0.666,0], [1,0.3]],
[[0,0], [0.333,1], [0.333,0], [0.666,0.3], [0.666,0], [1,0.3]]));
JS9.checkNew(new JS9.Colormap("staircase", (() => {
let ii, kk;
let cur = 0;
const a = [];
for(ii=1; ii<=5; ii++, cur++){
kk = ii/5.0;
a[cur] = [];
a[cur].push(kk \* 0.3);
a[cur].push(kk \* 0.3);
a[cur].push(kk);
}
for(ii=1; ii<=5; ii++, cur++){
kk = ii/5.0;
a[cur] = [];
a[cur].push(kk \* 0.3);
a[cur].push(kk);
a[cur].push(kk \* 0.3);
}
for(ii=1; ii<=5; ii++, cur++){
kk = ii/5.0;
a[cur] = [];
a[cur].push(kk);
a[cur].push(kk \* 0.3);
a[cur].push(kk \* 0.3);
}
return a;})()));
JS9.checkNew(new JS9.Colormap("color",
[[0,0,0], [0.18431, 0.18431, 0.18431], [0.37255, 0.37255, 0.37255], [0.56078, 0.56078, 0.56078], [0.74902, 0.74902, 0.74902], [0.93725, 0.93725, 0.93725], [0, 0.18431, 0.93725], [0, 0.37255, 0.74902], [0, 0.49804, 0.49804], [0, 0.74902, 0.30980], [0, 0.93725, 0], [0.30980, 0.62353, 0], [0.49804, 0.49804, 0], [0.62353, 0.30980, 0], [0.93725, 0, 0], [0.74902, 0, 0.30980]]));
};
// init console commands
JS9.initCommands = function(){
// sanity check
if( !{}.hasOwnProperty.call(JS9, "Command") ){ return; }
// load commands
JS9.checkNew(new JS9.Command({
name: "analysis",
alias: "run",
help: "list/run analysis for current image",
get() {
let i, j, n, t, tasks;
let result = "";
const im = this.image;
if( im && im.analysisPackages ){
for(j=0; j= 2 ){
key = args[0];
val = args[1];
if( typeof key === "string" && typeof val === "string" ){
switch( typeof JS9.globalOpts[key] ){
case "boolean":
JS9.globalOpts[key] = val.match(/true/i) ? true : false;
break;
case "number":
JS9.globalOpts[key] = parseFloat(val);
break;
case "string":
JS9.globalOpts[key] = val;
break;
case "object":
try{
val = JSON.parse(val);
}
catch(e){
JS9.error(`invalid JSON for global cmd: ${val}`);
}
JS9.globalOpts[key] = val;
break;
default:
break;
}
}
}
}
}));
JS9.checkNew(new JS9.Command({
name: "grid",
help: "set/get coordinate grid for current image",
get() {
let msg;
const im = this.image;
if( im ){
msg = im.displayCoordGrid();
}
return msg ? "true" : "false";
},
set(args) {
let mode;
const im = this.image;
if( im ){
if( args[0].match(/true/i) ){
mode = true;
} else {
mode = false;
}
im.displayCoordGrid(mode, args[1]);
}
}
}));
JS9.checkNew(new JS9.Command({
name: "help",
help: "get list of available commands",
get() {
let i, cmd;
let s1 = "Or execute JS9 public access routines (use spaceless args, please):";
let s2 = "SetColormap heat";
let s3 = "GetColormap";
let s4 = '{"colormap":"heat","contrast":3.75,"bias":0.736328125}';
let s5 = 'AddRegions circle(23:23:27.9,+58:48:42.8,3") {"color":"cyan"}';
let msg = "

";
for(i=0; i ${cmd.name} | ${cmd.help}`; if( cmd.alias ){ msg += ` (${cmd.alias}`; if( cmd.alias2 ){ msg += `, ${cmd.alias2}`; } msg += ")"; } msg += " |";
}
msg += `|  | |
`;
msg += `| ${s1} | |
`;
msg += `|  | |
`;
msg += `| ${s2} | |
`;
msg += `| ${s3} | |
`;
msg += `| ${s4} | |
`;
msg += `| ${s5} | |
`;
msg += "

";
return msg;
}
}));
JS9.checkNew(new JS9.Command({
name: "helper",
help: "set/get helper connection",
get() {
return JS9.helper.connectinfo();
},
set(args) {
JS9.helper.connect(args[0].trim());
}
}));
JS9.checkNew(new JS9.Command({
name: "image",
help: "get name of current image or display specified image",
get() {
const im = this.image;
if( im ){
return im.file;
}
},
set(args) {
let i, im;
for(i=0; i=0 ){
if( im.display === this.display ){
im.displayImage("display");
return;
}
}
}
}
}));
JS9.checkNew(new JS9.Command({
name: "images",
help: "get list of currently loaded images",
get() {
let i, im;
let msg = "";
for(i=0; i 1 ){
height = parseInt(args[1], 10);
} else {
height = width;
}
display.resize(width, height);
}
}
}));
JS9.checkNew(new JS9.Command({
name: "scale",
help: "set/get scaling for current image",
get() {
let res;
const im = this.image;
if( im ){
res = im.getScale();
return `${res.scale} ${res.scalemin} ${res.scalemax}`;
}
},
set(args) {
const im = this.image;
if( im ){
im.setScale(...args);
}
}
}));
JS9.checkNew(new JS9.Command({
name: "scales",
help: "get list of available scales",
get() {
return JS9.scales.join(", ");
}
}));
JS9.checkNew(new JS9.Command({
name: "section",
help: "display section of current image",
set(args) {
let s, obj;
const alen = args.length;
const im = this.image;
if( alen === 1 && args[0] === "full" ){
im.displaySection("full");
} else {
s = args.join(" ");
if( s ){
try{ obj = JSON.parse(s); }
catch(e){ JS9.error("invalid JSON section"); }
im.displaySection(obj);
}
}
}
}));
JS9.checkNew(new JS9.Command({
name: "status",
help: "get status for specified (or current) image",
get(args) {
let i, first, tim, im, cmd;
let result = "";
for(i=0; i=0 ){
im = tim;
break;
}
}
if( im ){
first = 1;
} else {
first = 0;
im = this.image;
}
if( im ){
// no args -> load
if( first > args.length ){
return im.status.load;
}
// process specific status
for(i=first; i {
const code = e.which || e.keyCode;
let id, el;
if( code === 13 ){
id = $(e.currentTarget).data("enterfunc");
if( id ){
e.preventDefault();
// look at children (key event in a form)
el = $(e.currentTarget).find(`[name='${id}']`);
if( el.length ){
el.click();
} else {
// look at siblings (key event on input not in a form)
el = $(e.currentTarget).siblings(`[name='${id}']`);
if( el.length ){
el.click();
}
}
return false;
}
}
});
};
// ---------------------------------------------------------------------
//
// JS9 Public API: public interface for use in Web pages
//
// obviously, you can use any JS9 call in a web page but we will
// keep this interface stable
//
// ---------------------------------------------------------------------
// parse func args, checking for object containing display property
// return new arg list and display id
// used in public api routines to retrieve optional {display: id} arg
JS9.parsePublicArgs = function(args){
let display = null;
const argv = Array.from(args);
const obj = argv[argv.length-1];
// look for object containing display property as last arg
if( obj && (typeof obj === "object") &&
{}.hasOwnProperty.call(obj, "display") &&
(Object.keys(obj).length === 1) ){
display = obj.display;
argv.pop();
}
// return results
return {argv, display};
};
// some public routines are just a wrapper around the underlying image call
// others require a new func
JS9.mkPublic = function(name, s){
if( typeof s === "string" ){
if( JS9.Image.prototype[s] ){
JS9[name] = function(...args){
let got;
const {display, argv} = JS9.parsePublicArgs(args);
const im = JS9.getImage(display);
if( im ){
// call the image method
got = im[s](...argv);
// don't return image handle, it can't be serialized
if( (got === im) || (got === im.display) ){
return JS9.globalOpts.quietReturn ? "" : "OK";
}
return got;
}
};
JS9.publics[name] = JS9[name];
} else {
JS9.error(`unknown image func for mkPublic: ${s}`);
}
} else if( typeof s === "function" ){
JS9[name] = s;
JS9.publics[name] = JS9[name];
} else {
JS9.error(`unsupported type for mkPublic: ${typeof s}`);
}
};
JS9.mkPublic("CloseImage", "closeImage");
JS9.mkPublic("DisplayImage", "displayImage");
JS9.mkPublic("DisplayExtension", "displayExtension");
JS9.mkPublic("DisplaySlice", "displaySlice");
JS9.mkPublic("DisplaySection", "displaySection");
JS9.mkPublic("BlendImage", "blendImage");
JS9.mkPublic("MaskImage", "maskImage");
JS9.mkPublic("GetColormap", "getColormap");
JS9.mkPublic("SetColormap", "setColormap");
JS9.mkPublic("GetZoom", "getZoom");
JS9.mkPublic("SetZoom", "setZoom");
JS9.mkPublic("GetPan", "getPan");
JS9.mkPublic("SetPan", "setPan");
JS9.mkPublic("AlignPanZoom", "alignPanZoom");
JS9.mkPublic("GetScale", "getScale");
JS9.mkPublic("SetScale", "setScale");
JS9.mkPublic("GetOpacity", "getOpacity");
JS9.mkPublic("SetOpacity", "setOpacity");
JS9.mkPublic("SetFlip", "setFlip");
JS9.mkPublic("GetFlip", "getFlip");
JS9.mkPublic("SetRotate", "setRotate");
JS9.mkPublic("GetRotate", "getRotate");
JS9.mkPublic("SetRot90", "setRot90");
JS9.mkPublic("GetRot90", "getRot90");
JS9.mkPublic("GetParam", "getParam");
JS9.mkPublic("SetParam", "setParam");
JS9.mkPublic("CopyParams", "copyParams");
JS9.mkPublic("GetValPos", "updateValpos");
JS9.mkPublic("ImageToDisplayPos", "imageToDisplayPos");
JS9.mkPublic("DisplayToImagePos", "displayToImagePos");
JS9.mkPublic("ImageToLogicalPos", "imageToLogicalPos");
JS9.mkPublic("LogicalToImagePos", "logicalToImagePos");
JS9.mkPublic("GetWCSUnits", "getWCSUnits");
JS9.mkPublic("SetWCSUnits", "setWCSUnits");
JS9.mkPublic("GetWCS", "getWCS");
JS9.mkPublic("SetWCS", "setWCS");
JS9.mkPublic("GetWCSSys", "getWCSSys");
JS9.mkPublic("SetWCSSys", "setWCSSys");
JS9.mkPublic("ShowShapeLayer", "showShapeLayer");
JS9.mkPublic("ActiveShapeLayer", "activeShapeLayer");
JS9.mkPublic("ToggleShapeLayers", "toggleShapeLayers");
JS9.mkPublic("AddShapes", "addShapes");
JS9.mkPublic("RemoveShapes", "removeShapes");
JS9.mkPublic("GetShapes", "getShapes");
JS9.mkPublic("ChangeShapes", "changeShapes");
JS9.mkPublic("CopyShapes", "copyShapes");
JS9.mkPublic("SelectShapes", "selectShapes");
JS9.mkPublic("UnselectShapes", "unselectShapes");
JS9.mkPublic("GroupShapes", "groupShapes");
JS9.mkPublic("UngroupShapes", "ungroupShapes");
JS9.mkPublic("DisplayCoordGrid", "displayCoordGrid");
JS9.mkPublic("Print", "print");
JS9.mkPublic("SavePNG", "savePNG");
JS9.mkPublic("SaveJPEG", "saveJPEG");
JS9.mkPublic("SaveFITS", "saveFITS");
JS9.mkPublic("UploadFITSFile", "uploadFITSFile");
JS9.mkPublic("CountsInRegions", "countsInRegions");
JS9.mkPublic("RadialProfile", "radialProfile");
JS9.mkPublic("Plot3D", "plot3d");
JS9.mkPublic("RunAnalysis", "runAnalysis");
JS9.mkPublic("GetAnalysis", "getAnalysis");
JS9.mkPublic("RawDataLayer", "rawDataLayer");
JS9.mkPublic("GaussBlurData", "gaussBlurData");
JS9.mkPublic("ImarithData", "imarithData");
JS9.mkPublic("RotateData", "rotateData");
JS9.mkPublic("ReprojectData", "reprojectData");
JS9.mkPublic("ShiftData", "shiftData");
JS9.mkPublic("FilterRGBImage", "filterRGBImage");
JS9.mkPublic("MoveToDisplay", "moveToDisplay");
// lookup an image
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("LookupImage", function(...args){
const obj = JS9.parsePublicArgs(args);
return JS9.lookupImage(obj.argv[0], obj.display);
});
// lookup a display
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("LookupDisplay", function(...args){
const obj = JS9.parsePublicArgs(args);
return JS9.lookupDisplay(obj.argv[0]||obj.display, obj.argv[1]);
});
// display next (or prev) image in a given display
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("DisplayNextImage", function(...args){
let n, display;
const obj = JS9.parsePublicArgs(args);
display = JS9.lookupDisplay(obj.display);
if( display ){
n = parseFloat(obj.argv[0]) || 1;
return display.nextImage(n);
}
});
// rename a display:
// RenameDisplay(nid) # change def. id (usually "JS9") to nid
// RenameDisplay(nid, {display: oid}) # change oid to nid
// RenameDisplay(oid, nid) # change oid to nid
JS9.mkPublic("RenameDisplay", function(...args){
let nid, oid, disp;
const obj = JS9.parsePublicArgs(args);
switch( obj.argv.length ){
case 0:
return;
case 1:
oid = obj.display;
nid = obj.argv[0];
break;
default:
oid = obj.argv[0];
nid = obj.argv[1];
break;
}
disp = JS9.lookupDisplay(oid);
if( disp && disp.id ){
oid = disp.id;
// save the orignal id, since existing plugins use it
if( !disp.oid ){
disp.oid = oid;
}
// set the new id
disp.id = nid;
// tell the helper to recognize the new instead of the old
JS9.helper.send("renameDisplay", {odisplay: oid, ndisplay: disp.id});
}
});
// close all displayed images
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("CloseDisplay", function(...args){
let i, s, im, disp, template, regexp;
const obj = JS9.parsePublicArgs(args);
disp = JS9.lookupDisplay(obj.argv[0], false);
if( !disp ){
disp = JS9.lookupDisplay(obj.display);
s = obj.argv[0];
}
template = obj.argv[1] || s;
if( template ){
try{ regexp = new RegExp(template); }
catch(e){ JS9.error(`invalid regexp for CloseDisplay: ${template}`); }
}
// reverse loop because we slice JS9.images
for(i=JS9.images.length-1; i>=0; i--){
im = JS9.images[i];
if( im.display === disp ){
if( regexp ){
if( im.id.match(regexp) ||
im.file.match(regexp) ||
im.fitsFile.match(regexp) ){
im.closeImage();
}
} else {
im.closeImage();
}
}
}
});
// add a colormap to JS9
JS9.mkPublic("AddColormap", function(...args){
let colormap, a1, a2, a3, a4, reader, cobj;
const obj = JS9.parsePublicArgs(args);
const obj2cmap = (xobj, opts) => {
let i, tobj;
if( typeof xobj !== "object" ){
JS9.error("invalid colormap object for JS9.AddColormap()");
}
if( !$.isArray(xobj) ){
xobj = [xobj];
}
for(i=0; i {
try{ cobj = JSON.parse(ev.target.result); }
catch(e){ JS9.error("can't parse JSON colormap", e); }
obj2cmap(cobj, a1);
};
reader.readAsText(colormap);
} else if( typeof colormap === "object" ){
// from LoadColormap
obj2cmap(colormap, a1);
} else {
switch(obj.argv.length){
case 1:
// json formatted string
try{ cobj = JSON.parse(colormap); }
catch(e){ JS9.error("can't parse JSON colormap", e); }
obj2cmap(cobj);
break;
case 2:
case 3:
if( typeof a1 === "string" ){
try{ a1 = JSON.parse(a1); }
catch(e){ JS9.error("can't parse JSON colormap", e); }
}
JS9.checkNew(new JS9.Colormap(colormap, a1));
if( obj.argv.length === 2 ){
JS9.globalOpts.topColormaps.push(colormap);
} else if( typeof a2 !== "object" || a2.toplevel !== false ){
JS9.globalOpts.topColormaps.push(colormap);
}
break;
case 4:
case 5:
if( typeof a1 === "string" ){
try{ a1 = JSON.parse(a1); }
catch(e){ JS9.error("can't parse JSON colormap", e); }
}
if( typeof a2 === "string" ){
try{ a2 = JSON.parse(a2); }
catch(e){ JS9.error("can't parse JSON colormap", e); }
}
if( typeof a3 === "string" ){
try{ a3 = JSON.parse(a3); }
catch(e){ JS9.error("can't parse JSON colormap", e); }
}
JS9.checkNew(new JS9.Colormap(colormap, a1, a2, a3));
if( obj.argv.length === 4 ){
JS9.globalOpts.topColormaps.push(colormap);
} else if( !a4 || typeof a4 !== "object" || a4.toplevel !== false ){
JS9.globalOpts.topColormaps.push(colormap);
}
break;
default:
JS9.error("AddColormap() requires a colormap name and 1 or 3 args");
break;
}
}
});
// load a colormap file
JS9.mkPublic("LoadColormap", function(...args){
let file, opts;
const obj = JS9.parsePublicArgs(args);
file = obj.argv[0];
opts = obj.argv[1];
// sanity check
if( !file ){
JS9.error("JS9.LoadColormap: no file specified for colormap load");
}
// convert blob to string
if( typeof file === "object" ){
JS9.AddColormap(file, opts);
} else if( typeof file === "string" ){
file = JS9.fixPath(file, opts);
JS9.fetchURL(null, file, null, (data) => {
JS9.AddColormap(data, opts);
});
} else {
// oops!
JS9.error(`unknown file type for LoadColormap: ${typeof file}`);
}
});
// set RGB mode (and maybe the images themselves)
JS9.mkPublic("SetRGBMode", function(...args){
let i, im, mode, imobj;
const obj = JS9.parsePublicArgs(args);
const disp = JS9.lookupDisplay(obj.display);
const colors = ["red", "green", "blue"];
const ids = ["rid", "gid", "bid"];
mode = obj.argv[0];
imobj = obj.argv[1];
if( mode === undefined ){
mode = !disp.rgb.active;
}
if( imobj ){
for(i=0; i<3; i++){
im = imobj[ids[i]];
if( typeof im === "string" ){
im = JS9.LookupImage(im);
}
if( !im ){
continue;
}
im.setColormap(colors[i]);
}
}
if( mode === "true" ){
mode = true;
} else if( mode === "false" ){
mode = false;
}
disp.rgb.active = !!mode;
JS9.DisplayImage({display: obj.display});
return disp.rgb.active;
});
// get RGB mode info
JS9.mkPublic("GetRGBMode", function(...args){
const obj = JS9.parsePublicArgs(args);
const disp = JS9.lookupDisplay(obj.display);
return {active: disp.rgb.active,
rid: disp.rgb.rim ? disp.rgb.rim.id: null,
gid: disp.rgb.gim ? disp.rgb.gim.id: null,
bid: disp.rgb.bim ? disp.rgb.bim.id: null};
});
// set/clear valpos flag
JS9.mkPublic("SetValPos", function(...args){
let mode;
let got = null;
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
mode = obj.argv[0];
if( im ){
got = im.params.valpos;
im.params.valpos = mode;
}
return got;
});
// set/clear image inherit flag
JS9.mkPublic("SetImageInherit", function(...args){
let mode;
let got = null;
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
mode = obj.argv[0];
if( im ){
got = im.params.inherit;
im.params.inherit = mode;
}
return got;
});
JS9.mkPublic("GetImageInherit", function(...args){
let got = null;
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
if( im ){
got = im.params.inherit;
}
return got;
});
// display in-page FITS images
JS9.mkPublic("Load", function(...args){
let i, s, im, disp, display, func, blob, bytes, topts, tfile, vfile;
let file, opts;
let ptype = "fits";
const obj = JS9.parsePublicArgs(args);
file = obj.argv[0];
opts = obj.argv[1];
// sanity check
if( !file ){
JS9.error("JS9.Load: no file specified for image load");
}
// check for display
if( obj.display ){
display = obj.display;
} else {
if( JS9.displays.length > 0 ){
display = JS9.displays[0].id;
} else {
display = JS9.DEFID;
}
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, opts);
} else if( typeof opts === "string" ){
// convert json to object
try{ opts = JSON.parse(opts); }
catch(e){ opts = { /\* empty \*/ }; }
}
// if display was implicit, add it to opts
opts.display = opts.display || display;
// check for onload func
if( opts.onload ){
func = opts.onload;
} else if( JS9.imageOpts.onload ){
func = JS9.imageOpts.onload;
opts.onload = func;
}
// unset previous fetch status before new load
delete JS9.fetchURL.status;
// handle blob containing FITS
if( file instanceof Blob ){
if( file.path || file.name ){
// new file (or, for Electron.js desktop, the path, which is better)
opts.file = JS9.cleanPath(file.path || file.name);
// does this image already exist?
if( typeof opts.refresh === "object" ){
im = opts.refresh;
} else {
im = JS9.lookupImage(opts.file, opts.display);
}
if( im ){
// do we refresh or redisplay?
if( JS9.isNull(opts.refresh) ){
opts.refresh = JS9.globalOpts.reloadRefresh;
}
if( opts.refresh ){
// save the handle of the image we will be refreshing
opts.refresh = im;
} else{
// if not refreshing, just re-display and exit
im.displayImage("display", opts);
im.refreshLayers();
im.display.clearMessage();
if( opts.onload ){
try{ JS9.xeqByName(opts.onload, window, im); }
catch(e){ JS9.error("in image onload callback", e,
false); }
}
JS9.waiting(false);
return;
}
} else {
// remove any extraneous refresh flag
delete opts.refresh;
}
} else {
// remove any extraneous refresh flag
delete opts.refresh;
}
if( !opts.file ){
opts.file = JS9.ANON + JS9.uniqueID();
}
// look for a mime type to tell us how to process this blob
if( file.type && file.type.includes("image/") ){
switch(file.type){
case "image/fits":
break;
default:
ptype = "img";
break;
}
} else if( opts.file.split(".").pop().match(/(png|jpg|jpeg)/i) ){
ptype = "img";
}
// processing type: img or fits
switch(ptype){
case "fits":
topts = $.extend(true, {}, JS9.fits.options, opts);
// for Electron.js desktop, see if we can access the path locally
// (for blobs coming from drag/drop and openLocal)
if( file.path && opts.localAccess ){
vfile = JS9.localAccess(file.path);
// if so, use the local file instead of storing a vfile
if( vfile ){
file = file.path;
topts.file = file;
topts.vfile = vfile;
}
}
try{ JS9.handleFITSFile(file, topts, JS9.NewFitsImage); }
catch(e){ JS9.error("can't process FITS file", e); }
break;
case "img":
try{ JS9.handleImageFile(file, opts, JS9.Load); }
catch(e){ JS9.error("can't process IMG file", e); }
break;
}
return;
}
// handle raw (fits) data objects
if( typeof file === "object" ){
JS9.checkNew(new JS9.Image(file, opts, func));
return;
}
// it's gotta be a string: in-memory FITS, url, or filename
if( typeof file !== "string" ){
JS9.error(`unknown file type for Load: ${typeof file}`);
}
// convert in-memory base64-encoded FITS to a binary string
if( file.slice(0,12) === "U0lNUExFICA9" ){
file = window.atob(file);
}
// handle in-memory FITS by converting to a blob
if( file.slice(0,9) === "SIMPLE =" ){
bytes = [];
for(i=0; i {
try{ JS9.handleFITSFile(file, topts, JS9.NewFitsImage); }
catch(e){ JS9.error("can't process FITS file", e); }
}, 0);
} else {
// fetch file
JS9.fetchURL(file, tfile, opts);
}
});
// create a new instance of JS9 in a window (light or new)
JS9.mkPublic("LoadWindow", function(...args){
let s, id, display, did, head, body, win, winid, initialURL, xobj;
let wid, wtype, wurl, idbase, title, warr, wwidth, wheight;
let file, opts, type, html, winopts;
const lopts = JS9.lightOpts[JS9.LIGHTWIN];
const obj = JS9.parsePublicArgs(args);
const removeDisplay = (display) => {
// remove from display list
const idx = $.inArray(display, JS9.displays);
if( idx >= 0 ){ JS9.displays.splice(idx, 1); }
};
const getHTML = (id, opts, winopts) => {
let html, display;
opts = opts || {};
if( opts.clone ){
display = JS9.lookupDisplay(opts.clone, false);
}
if( winopts ){
warr = winopts.match(/(.\*width=)([0-9]+)(px,height=)([0-9]+)(px.\*)/, "$1@@H@@$3");
wwidth = parseInt(warr[2], 10);
wheight = parseInt(warr[4], 10);
}
// make up the html with the unique id
html = "

---

";
// menubar
if( !display ||
($(`#${opts.clone}Menubar`).length > 0 &&
!display.pluginInstances.JS9Menubar.isDynamic) ){
html += ``;
} else if( winopts ){
wheight -= 40;
}
// display
html += ``;
// colorbar
if( !display ||
($(`#${opts.clone}Colorbar`).length > 0 &&
$(`#${opts.clone}Statusbar`).length ===0 &&
!display.pluginInstances.JS9Colorbar.isDynamic) ){
if( display && display.pluginInstances.JS9Colorbar ){
s = `data-showTicks='${display.pluginInstances.JS9Colorbar.showTicks}'`;
} else {
s = "";
}
html += ``;
if( display && display.pluginInstances.JS9Colorbar &&
!display.pluginInstances.JS9Colorbar.showTicks ){
wheight -= 15;
}
} else if( winopts ){
wheight -= 44;
}
if( !display ||
($(`#${opts.clone}Statusbar`).length > 0 &&
!display.pluginInstances.JS9Statusbar.isDynamic) ){
html += ``;
} else if( winopts ){
wheight -= 40;
}
if( winopts ){
if( JS9.Dysel.retrievePlugins().length ){
wwidth += 2;
wheight += 2;
}
return {html: html, winopts: warr[1] + String(wwidth) + warr[3] + String(wheight) + warr[5]};
}
return html;
};
// create display and load image into a light window
const lightLoad = (file, opts) => {
let display;
// create the new JS9 Display
display = new JS9.Display(id);
// save the light window id;
display.winid = winid;
// add to list of displays
JS9.helper.send("addDisplay", {"display": id});
// instantiate new plugins
JS9.instantiatePlugins();
// load the image into this display
opts.display = id;
// just becomes a standard load
if( file ){
JS9.Load(file, opts);
}
return display;
};
// close a light window, moving images if necessary
const lightClose = (display) => {
let i, im;
let got = 0;
const ims = [];
// make a list of images in his display
for(i=0; i {
let i, el;
// on arrival, add JS9 displays to 'move' part of form
el = $("#lightWinCloseForm").find("#lightWinCloseSel");
for(i=0; i", {
value: JS9.displays[i].id,
text: JS9.displays[i].id
}));
}
}
});
did = JS9.lightWin(wid, wtype, wurl, "Closing a light window",
lopts.lcloseWin);
$(did).data("dispid", id);
$(did).data("winid", winid);
return false;
}
};
// input args
file = obj.argv[0];
opts = obj.argv[1];
type = obj.argv[2];
html = obj.argv[3];
winopts = obj.argv[4];
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, opts);
} else if( typeof opts === "string" ){
// convert json to object
try{ opts = JSON.parse(opts); }
catch(e){ opts = {}; }
}
// default window type
type = type || "light";
// default base id
idbase = `${type}win`;
// create the specified type of window
switch(type){
case "light":
// use supplied id or make a reasonably unique id for the JS9 elements
if( opts.id ){
id = opts.id;
delete opts.id;
} else {
id = idbase + JS9.uniqueID();
}
// and a second one for controlling the light window
did = `d${id}`;
// inner html housing JS9 display, etc.
if( html ){
// html specified: def window opts is standard light image window
winopts = winopts || lopts.imageWin;
} else {
// no html specified: use originating display setup, if possible,
// otherwise use defaults, and always use default window opts
xobj = getHTML(id, opts, lopts.imageWin);
// always use returned html (there being no other option)
html = xobj.html;
// but only use the new winopts if no winopts was specified
winopts = winopts || xobj.winopts;
}
// nice title
title = sprintf(`JS9 Display${JS9.IDFMT}`, id);
// create the light window
winid = JS9.lightWin(did, "inline", html, title, winopts);
// set up display and load image
display = lightLoad(file, opts);
// on window close, we need to deal with the displayed images
winid.onclose = () => {
return lightClose(display);
};
// return the id
return id;
case "new":
// use supplied id or make a reasonably unique id for the JS9 elements
if( opts.id ){
id = opts.id;
delete opts.id;
} else {
id = idbase + JS9.uniqueID();
}
// window opts
winopts = winopts || `width=${JS9.globalOpts.newWindowWidth}, height=${ JS9.globalOpts.newWindowHeight}`;
// get our own file's header for css and js files
// if page is generated on the server side, hardwire ...
// if JS9 is not installed, hardwire ...
head = document.getElementsByTagName("head")[0].innerHTML;
// remove load of astroem[w].js, so it will be loaded during init
head = head.replace(/src=['"].\*astroemw?\.js['"]/, "");
// but why doesn't the returned header contain the js9 js file??
// umm... it seems to have it, at least FF does as of 8/25/15 ...
if( !head.match(/src=["'].\*js9\.js/) &&
!head.match(/src=["'].\*js9\.min\.js/) ){
head += '';
}
// make a body containing the JS9 elements and the preload call
body = html || getHTML(id, opts);
// combine head and body into a full html file
html = `${head}${body}

\n`;
// open the new window
if( window.electron ){
initialURL = "data:text/html,

";
}
win = window.open(initialURL, id, winopts);
if( !win ){
JS9.error("could not create window (check your pop-up blockers)");
return;
}
if( win.document ){
// open it (not strictly necessary but ...)
win.document.open();
// overwrite the doc with our html
win.document.write(html);
// must close!
win.document.close();
} else if( win.postMessage ){
JS9.error("LoadWindow('new') is disabled on the Desktop for security reasons");
} else {
JS9.error("no method available for drawing image into window");
}
// return the id
return id;
}
});
// load a link using back-end server as a proxy
JS9.mkPublic("LoadProxy", function(...args){
let f, disp, url, opts, oname;
const obj = JS9.parsePublicArgs(args);
url = obj.argv[0];
opts = obj.argv[1];
if( !JS9.globalOpts.loadProxy ){
JS9.error("proxy load not available for server");
}
if( !JS9.globalOpts.workDir ){
JS9.error("proxy load requires a temp workDir for server");
}
if( !url ){
JS9.error("no url specified for proxy load");
}
url = url.trim();
if( url.match(/dropbox\.com/) ){
// http://stackoverflow.com/questions/20757891/cross-origin-image-load-from-cross-enabled-site-is-denied
url = url.replace("www.dropbox.com", "dl.dropboxusercontent.com");
// https://blogs.dropbox.com/developers/2013/08/programmatically-download-content-from-share-links/
url = `${url.replace('?dl=0', '')}?raw=1`;
} else if( url.match(/drive\.google\.com/) ){
url=url.replace(/\/file\/d\/(\w+)\/\w+\?usp=sharing/,
"/uc?export=download&id=$1");
}
if( obj.display ){
disp = JS9.lookupDisplay(obj.display);
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, opts);
} else if( typeof opts === "string" ){
// convert json to object
try{ opts = JSON.parse(opts); }
catch(e){ opts = {}; }
}
// output filename specified?
if( opts.ofile ){
oname = opts.ofile;
delete opts.ofile;
} else {
oname = "";
}
JS9.waiting(true, disp);
JS9.Send("loadproxy", {"cmd": `js9Xeq loadproxy ${url} ${oname}`}, (r) => {
let robj, files, pf;
// return type can be string or object
if( typeof r === "object" ){
// object from node.js
robj = r;
} else {
// string from cgi
if( r.search(JS9.analOpts.epattern) >=0 ){
robj = {stderr: r};
} else {
robj = {stdout: r};
}
}
robj.errcode = robj.errcode || 0;
if( robj.stderr ){
JS9.error(robj.stderr);
} else if( robj.stdout ){
// output is file and possibly parentFile
files = robj.stdout.split(/\s+/);
if( files && files[0] ){
f = JS9.cleanPath(files[0]);
// proxy file
opts.proxyFile = f;
// relative path: add install dir prefix
if( f.charAt(0) !== "/" ){
f = JS9.InstallDir(f);
}
if( files[1] ){
pf = JS9.cleanPath(files[1]);
opts.parentFile = pf;
opts.proxyParent = pf;
}
// desktop app: don't make path relative to current directory
opts.fixpath = false;
// save original url
opts.proxyURL = url;
// load new file
JS9.Load(f, opts, {display: obj.display});
}
} else {
JS9.error("internal error: no return from load proxy command");
}
});
});
// save array of files to preload or preload immediately,
// depending on the state of processing
JS9.mkPublic("Preload", function(...args){
let i, j, mode, urlexp, func, arg1;
let emsg = "";
let pobj = null;
let dobj = null;
let alen = args.length;
const oalerts = JS9.globalOpts.alerts;
const obj = JS9.parsePublicArgs(args);
const baseexp = JS9.URLEXP;
const sesexp = /\.ses$/;
const cmapexp = /\.cmap$/;
arg1 = obj.argv[0];
// for socketio and loadProxy, support LoadProxy calls
if( JS9.globalOpts.loadProxy && JS9.helper.baseurl ){
urlexp = new RegExp(`^${JS9.helper.baseurl}`);
}
if( obj.display ){
dobj = {display: obj.display};
alen = alen - 1;
}
// check the state of processing
switch(alen){
case 0:
// if we are connected and have previously saved images, load now
// if connected is undefined, we have no back-end and we do our best
if( ((JS9.helper.connected === null) || JS9.helper.connected) &&
JS9.fits.name && (JS9.preloads.length > 0) ){
mode = 2;
} else {
// do nothing
mode = 3;
}
break;
case 1:
// boolean => we are ready to load
if( typeof arg1 === "boolean" ){
// if we have previously saved images, load now
if( arg1 && (JS9.preloads.length > 0) ){
mode = 2;
} else {
// do nothing
mode = 3;
}
} else {
// image args => if we are connected, we can load the images now
if( ((JS9.helper.connected === null) || JS9.helper.connected) &&
JS9.fits.name ){
mode = 1;
} else {
// save images and wait
mode = 0;
}
}
break;
default:
// image args => if we already are connected, we can load the images now
if( ((JS9.helper.connected === null) || JS9.helper.connected) &&
JS9.fits.name ){
mode = 1;
} else {
// save images and wait
mode = 0;
}
break;
}
switch(mode){
case 0:
// save preload image(s) for later
for(i=0; i {
im.refreshImage(hdu, opts);
};
fits = obj.argv[0];
opts = obj.argv[1] || {};
if( im ){
opts.id = im.id;
if( fits instanceof Blob ){
// cleanup previous FITS heap before handling the new FITS file,
// or we end up with a memory leak in the emscripten heap
if( !opts.rawid || opts.rawid === im.raw.id ){
JS9.cleanupFITSFile(im.raw, true);
}
try{ JS9.handleFITSFile(fits, JS9.fits.options, retry); }
catch(e){ JS9.error("can't refresh FITS file", e); }
} else {
im.refreshImage(fits, opts);
}
} else if( fits instanceof Blob ){
JS9.Load(...args);
}
});
// get specified status
JS9.mkPublic("GetStatus", function(...args){
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.argv[1] || obj.display);
const stat = obj.argv[0] || "load";
if( !obj.argv.length ){
return ["Load", "CreateMosaic", "DisplaySection", "LoadCatalog", "LoadRegions", "ReprojectData", "RotateData", "RunAnalysis"];
}
// if the fetch is still running or failed, return the status
if( JS9.fetchURL.status && stat.match(/^(pre)?load$/i) ){
return JS9.fetchURL.status;
}
// return status for specified image
if( im ){
return im.getStatus(stat);
}
return "none";
});
// get status of a Load ("complete" means ... complete)
JS9.mkPublic("GetLoadStatus", function(...args){
return JS9.GetStatus("load", ...args);
});
// http://stackoverflow.com/questions/400212/how-do-i-copy-to-the-clipboard-in-javascript
JS9.mkPublic("CopyToClipboard", function(text, im){
let msg, successful, textArea;
const x = $(document).scrollLeft(), y = $(document).scrollTop();
// save text for pseudo-pasting
JS9.clipboard = text;
// tmp textarea which from which the selection will be copied
textArea = document.createElement("textarea");
//
// \*\*\* styling is an extra step which is likely not required. \*\*\*
//
// Why is it here? To ensure:
// 1. the element is able to have focus and selection.
// 2. if element was to flash render it has minimal visual impact.
// 3. less flakyness with selection and copying which \*\*might\*\* occur if
// the textarea element is not visible.
//
// The likelihood is the element won't even render, not even a flash,
// so some of these are just precautions. However in IE the element
// is visible whilst the popup box asking the user for permission for
// the web page to copy to the clipboard.
//
// Place in top-left corner of screen regardless of scroll position.
textArea.style.position = "fixed";
textArea.style.top = 0;
textArea.style.left = 0;
// Ensure it has a small width and height. Setting to 1px / 1em
// doesn't work as it gives a negative w/h on some browsers.
textArea.style.width = "2em";
textArea.style.height = "2em";
// We don't need padding, reducing the size if it does flash render.
textArea.style.padding = 0;
// Clean up any borders.
textArea.style.border = "none";
textArea.style.outline = "none";
textArea.style.boxShadow = "none";
// Avoid flash of white box if rendered for any reason.
textArea.style.background = "transparent";
textArea.value = text;
document.body.appendChild(textArea);
textArea.select();
try {
successful = document.execCommand("copy");
if( successful ){
msg = "OK";
} else {
msg = "MANUAL";
if( JS9.BROWSER[2].match(/Mac/) ){
window.prompt("copy to clipboard: Cmd+C", text);
} else {
window.prompt("copy to clipboard: Ctrl+C", text);
}
}
} catch (err){
msg = "ERROR";
}
document.body.removeChild(textArea);
// refocus on display, but undo any scrolling
// (otherwise, the next keydown has no effect)
if( im && im.display ){
im.display.displayConjq.focus();
window.scrollTo(x, y);
}
return msg;
});
JS9.mkPublic("CopyFromClipboard", function(){
return JS9.clipboard || "";
});
// bring up the file dialog box and open selected FITS file(s)
JS9.mkPublic("OpenFileMenu", function(...args){
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
if( display ){
$(`#openLocalLoad-${display.id}`).click();
}
});
// bring up the file dialog box and open selected region files(s)
JS9.mkPublic("OpenRegionsMenu", function(...args){
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
if( display ){
$(`#openLocalLoadRegions-${display.id}`).click();
}
});
// bring up the file dialog box and load selected session files(s)
JS9.mkPublic("OpenSessionMenu", function(...args){
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
if( display ){
$(`#openLocalLoadSession-${display.id}`).click();
}
});
// bring up the file dialog box and open selected catalog file
JS9.mkPublic("OpenCatalogsMenu", function(...args){
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
if( display ){
$(`#openLocalLoadCatalog-${display.id}`).click();
}
});
// bring up the file dialog box and load selected colormap file(s)
JS9.mkPublic("OpenColormapMenu", function(...args){
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
if( display ){
$(`#openLocalLoadColormap-${display.id}`).click();
}
});
// save a colormap to disk
JS9.mkPublic("SaveColormap", function(...args){
let fname, im, cobj, s, blob, arg1, arg2;
const obj = JS9.parsePublicArgs(args);
const convertjson = (arg1) => {
let s = arg1;
if( typeof arg1 === "string" ){
try{ s = JSON.parse(arg1); }
catch(e){ /\* empty \*/ }
}
return s;
};
const getarr = (arr) => {
let i, c;
const cobj = [];
for(i=0; i background, include <-> exclude
// e.g. JS9.ToggleRegionTags("selected", "source", "background");
JS9.mkPublic("ToggleRegionTags", function(...args){
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
let which = obj.argv[0];
let x1 = obj.argv[1];
let x2 = obj.argv[2];
if( im ){
return im.toggleRegionTags(which, x1, x2);
}
return null;
});
// unremove previously removed regions
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("UnremoveRegions", function(...args){
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
if( im ){
return im.unremoveRegions();
}
return null;
});
// load a DS9/funtools regions file
JS9.mkPublic("LoadRegions", function(...args){
let s, reader, file, opts;
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
const addregions = (reg, ropts) => {
if( ropts && ropts.display !== undefined ){ delete ropts.display; }
// add the regions
im.addShapes("regions", reg, ropts);
// set status
im.setStatus("loadRegions", "complete");
// onload callback, if necessary
if( opts && opts.onload ){
try{ JS9.xeqByName(opts.onload, window, im); }
catch(e){ JS9.error("in regions onload callback", e, false); }
}
};
file = obj.argv[0];
opts = obj.argv[1];
// sanity check
if( !file ){
JS9.error("JS9.LoadRegions: no file specified for regions load");
}
// no action if no current image
if( !im ){
return;
}
// set status
im.setStatus("loadRegions", "processing");
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, opts);
} else if( typeof opts === "string" ){
// convert json to object
try{ opts = JSON.parse(opts); }
catch(e){ opts = {}; }
}
// convert blob to string
if( typeof file === "object" ){
s = file.path || file.name;
if( s ){
opts.file = s.split("/").reverse()[0];
}
// file reader object
reader = new FileReader();
reader.onload = (ev) => {
addregions(ev.target.result, opts);
};
reader.readAsText(file);
} else if( typeof file === "string" ){
opts.responseType = "text";
file = JS9.fixPath(file, opts);
opts.file = file.split("/").reverse()[0];
JS9.fetchURL(null, file, opts, addregions);
} else {
// oops!
JS9.error(`unknown file type for LoadRegions: ${typeof file}`);
}
});
// construct directory starting with where JS9 is installed
JS9.mkPublic("InstallDir", function(dir){
// sanity check
if( !dir ){ return ""; }
// add path to install directory, clean path a little bit
return JS9.cleanPath(JS9.INSTALLDIR + dir);
});
// add new display divs and/or new plugins
JS9.mkPublic("AddDivs", function(...args){
let i, j, div, dexist, id;
const obj = JS9.parsePublicArgs(args);
// process all divs
for(i=0; i< obj.argv.length; i++){
// get next id
id = obj.argv[i];
// sanity check
if( !id ){
continue;
}
// make sure div exists ...
if( $(`#${id}`).length === 0 ){
if( JS9.DEBUG ){
JS9.log("warning: can't find div, skipping AddDivs(): %s", id);
}
continue;
}
// ... but has not already been added
for(j=0; j= 0 ){
cel = display.divjq.closest(".JS9GridContainer");
el = display.divjq.closest(".JS9GridItem");
if( cel.length > 0 && el.length > 0 ){
if( cel.find(".JS9GridItem").length > 1 ){
// close all images
JS9.CloseDisplay(display.id);
// remove DOM element from grid
el.remove();
JS9.displays.splice(idx, 1);
} else {
JS9.error(`can't remove last display in grid: ${display.id}`);
}
} else if( display.winid && display.winid.close ){
// close all images
JS9.CloseDisplay(display.id);
// close light window
display.winid.close();
} else {
JS9.error("can only remove displays within a grid or lightwins");
}
} else {
JS9.error(`can't find display in display list: ${display.id}`);
}
});
// save a session (current image, images in current display, or all images)
JS9.mkPublic("SaveSession", function(...args){
let fname, display, disp, arg1, arg2;
let opts = {};
const obj = JS9.parsePublicArgs(args);
arg1 = obj.argv[0];
arg2 = obj.argv[1];
// opts can be an object or json or a filename
if( typeof arg1 === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, arg1);
} else if( typeof arg1 === "string" ){
// try to convert json to object, but default to a file name
try{ opts = JSON.parse(arg1); }
catch(e){
fname = arg1;
// but is there a second opts arg?
if( arg2 ){
if( typeof arg2 === "object" ){
opts = $.extend(true, {}, arg2);
} else {
try{ opts = JSON.parse(arg2); }
catch(e2){ opts = {}; }
}
}
}
}
// default save mode
if( !opts.mode ){
opts.mode = "display";
}
// check for display
if( obj.display ){
display = obj.display;
} else if( opts.display ){
display = opts.display;
} else {
if( JS9.displays.length > 0 ){
display = JS9.displays[0].id;
} else {
display = JS9.DEFID;
}
}
// display we are saving
disp = JS9.lookupDisplay(display);
// better have an image
if( !disp.image ){
return null;
}
// default filename, if none specified
if( !fname ){
if( opts.mode === "display" ){
// generic file name for saving multiple images
fname = `js9-${new Date().toISOString().slice(0,10)}.ses`;
} else {
// file name tied to image being saved
fname = `${disp.image.id}.ses`;
}
}
// save the session
return disp.image.saveSession(fname, opts);
});
// load a session file
JS9.mkPublic("LoadSession", function(...args){
let display, reader, disp, file, opts;
const obj = JS9.parsePublicArgs(args);
file = obj.argv[0];
opts = obj.argv[1];
// sanity check
if( !file ){
JS9.error("JS9.LoadSession: no file specified for load");
}
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, opts);
} else if( typeof opts === "string" ){
// convert json to object
try{ opts = JSON.parse(opts); }
catch(e){ opts = {}; }
}
// check for display
if( obj.display ){
display = obj.display;
} else if( opts.display ){
display = opts.display;
} else {
if( JS9.displays.length > 0 ){
display = JS9.displays[0].id;
} else {
display = JS9.DEFID;
}
}
disp = JS9.lookupDisplay(display);
opts.display = disp.id;
// convert blob to json object
if( typeof file === "object" ){
// file reader object
reader = new FileReader();
reader.onload = (ev) => {
const jobj = JSON.parse(ev.target.result);
opts.sessionPath = JS9.dirname(file.path || file.name || "");
disp.loadSession(jobj, opts);
};
reader.readAsText(file);
} else if( typeof file === "string" ){
opts.responseType = "text";
opts.display = disp.id;
file = JS9.fixPath(file, opts);
JS9.fetchURL(null, file, opts, (jstr, opts) => {
const jobj = JSON.parse(jstr);
opts.sessionPath = JS9.dirname(file);
disp.loadSession(jobj, opts);
});
} else {
// oops!
JS9.error(`unknown file type for LoadSession: ${typeof file}`);
}
});
// save regions to disk
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("SaveCatalog", function(...args){
const obj = JS9.parsePublicArgs(args);
const im = JS9.getImage(obj.display);
let fname = obj.argv[0];
let which = obj.argv[1];
if( im ){
return im.saveCatalog(fname, which);
}
return;
});
// load a starbase catalog file
JS9.mkPublic("LoadCatalog", function(...args){
let reader, im, layer, file, opts;
const obj = JS9.parsePublicArgs(args);
layer = obj.argv[0];
file = obj.argv[1];
opts = obj.argv[2];
// special case: 1 arg is the catalog, not the layer
// i.e., file reader object from openLocalLoadCotalog
if( layer instanceof Blob ){
opts = file;
file = layer;
layer = null;
}
// sanity check
if( !file ){
JS9.error("JS9.LoadCatalog: no file specified for catalog load");
}
// an image must loaded into the display
im = JS9.getImage(obj.display);
if( !im ){
return;
}
// set status
im.setStatus("loadCatalog", "processing");
// opts is optional
opts = opts || {};
// opts can be an object or json
if( typeof opts === "object" ){
// make a copy so we can modify it
opts = $.extend(true, {}, opts);
} else if( typeof opts === "string" ){
// convert json to object
try{ opts = JSON.parse(opts); }
catch(e){ opts = {}; }
}
// convert blob to string
if( file instanceof Blob ){
// file reader object
reader = new FileReader();
reader.onload = (ev) => {
// improve the filename, if possible
if( !layer && file.name ){
layer = file.name.replace(/\.[^.]\*$/, "");
}
// load the catalog
im.loadCatalog(layer, ev.target.result, opts);
// set status
im.setStatus("loadCatalog", "complete");
// onload callback
if( opts && opts.onload ){
try{ JS9.xeqByName(opts.onload, window, im); }
catch(e){ JS9.error("in catalog onload callback", e, false); }
}
};
reader.readAsText(file);
} else if( typeof file === "string" ){
if( file.match(/\t/) ){
// it's a table (contains a tab)
im.loadCatalog(layer, file, opts);
// set status
im.setStatus("loadCatalog", "complete");
// onload callback
if( opts && opts.onload ){
try{ JS9.xeqByName(opts.onload, window, im); }
catch(e){ JS9.error("in catalog onload callback", e, false); }
}
} else {
// its a file: retrieve and load the catalog
opts.responseType = "text";
file = JS9.fixPath(file, opts);
JS9.fetchURL(null, file, opts, (s) => {
// load the catalog
im.loadCatalog(layer, s, opts);
// set status
im.setStatus("loadCatalog", "complete");
// onload callback
if( opts && opts.onload ){
try{ JS9.xeqByName(opts.onload, window, im); }
catch(e){ JS9.error("in catalog onload callback", e, false); }
}
});
}
} else {
// oops!
JS9.error(`unknown file type for LoadCatalog: ${typeof file}`);
}
});
// create an image mosaic
JS9.mkPublic("CreateMosaic", function(...args){
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
let ims = obj.argv[0];
let opts = obj.argv[1];
if( display ){
return display.createMosaic(ims, opts);
}
});
// display the named plugin
JS9.mkPublic("DisplayPlugin", function(...args){
let i, plugin, pname, lcname, name;
const obj = JS9.parsePublicArgs(args);
const display = JS9.lookupDisplay(obj.display);
name = obj.argv[0];
if( display && obj.argv[0] ){
lcname = name.toLowerCase();
for(i=0; i {
try{ window.electron.sendMsg(opts); }
catch(e){ JS9.error("could not print window", e); }
}, JS9.TIMEOUT);
} else {
JS9.error("WindowPrint is only available for the JS9 desktop app");
}
});
// save PDF of window (Desktop JS9 only)
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("WindowToPDF", function(...args){
const obj = JS9.parsePublicArgs(args);
const opts = {cmd: "pdf"};
if( window.electron ){
opts.file = obj.argv[0] || "js9.pdf";
if( obj.argv[1] ){
opts.opts = obj.argv[1];
}
window.setTimeout(() => {
try{ window.electron.sendMsg(opts); }
catch(e){ JS9.error("could not create window pdf", e); }
}, JS9.TIMEOUT);
} else {
JS9.error("WindowToPDF is only available for the JS9 desktop app");
}
});
// save js9 messaging script (Desktop JS9 app only)
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("SaveScript", function(...args){
const obj = JS9.parsePublicArgs(args);
const opts = {cmd: "script"};
if( window.electron && window.electron.app ){
opts.file = obj.argv[0] || "";
window.setTimeout(() => {
try{ window.electron.sendMsg(opts); }
catch(e){ JS9.error("could not create messaging script", e); }
}, JS9.TIMEOUT);
} else {
JS9.error("SaveScript is only available for the JS9 desktop app");
}
});
// set save directory (Desktop JS9 only)
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("SaveDir", function(...args){
const obj = JS9.parsePublicArgs(args);
const opts = {cmd: "savedir"};
if( window.electron ){
if( obj.argv[0] !== undefined ){
opts.dirname = obj.argv[0];
if( obj.argv[1] ){ opts.opts = obj.argv[1]; }
} else {
JS9.error("SaveDir requires a directory name");
}
window.setTimeout(() => {
try{ window.electron.sendMsg(opts); }
catch(e){ JS9.error("could not set save directory", e); }
}, JS9.TIMEOUT);
} else {
JS9.error("SaveDir is only available for the JS9 desktop app");
}
});
// quit the app (Desktop JS9 only)
// eslint-disable-next-line no-unused-vars
JS9.mkPublic("Quit", function(...args){
const opts = {cmd: "quit"};
if( window.electron ){
window.setTimeout(() => {
try{ window.electron.sendMsg(opts); }
catch(e){ JS9.error("could not quit app", e); }
}, JS9.TIMEOUT);
} else {
JS9.error("Quit is only available for the JS9 desktop app");
}
});
// ---------------------------------------------------------------------
// end of JS9 Public Interface
// ---------------------------------------------------------------------
// ---------------------------------------------------------------------
// the init routine to start up JS9
// ---------------------------------------------------------------------
JS9.init = function(){
let uopts, url, ufile, dopts, key, arr;
// sanity check: need HTML5 canvas and JSON
if( !window.HTMLCanvasElement || !JSON ){
JS9.error("your browser does not support JS9 (no HTML5 canvas and/or JSON). Please try a modern version of Firefox, Chrome, Safari, Opera, or Edge.");
}
// get relative location of installed js9.css file
// which tells us where JS9 installed files (and the helper) are located
//
// allow specification of installdir in js9prefs.js
// check this manually: it's happening before processing the prefs
if( {}.hasOwnProperty.call(window, "JS9Prefs") &&
typeof JS9Prefs === "object" ){
if( JS9Prefs.globalOpts && JS9Prefs.globalOpts.installDir ){
JS9.INSTALLDIR = JS9Prefs.globalOpts.installDir;
}
}
if( !JS9.INSTALLDIR ){
try{
// process all links which end in 'js9.css'
$('link[href$="js9.css"]').each((index, element) => {
const h = $(element).attr("href");
if( h ){
// must really end in 'js9.css'
if( h.split("/").reverse()[0] === "js9.css" ){
// set install dir to its directory
JS9.INSTALLDIR = h.replace(/js9\.css$/, "");
}
}
});
} catch(e){
JS9.INSTALLDIR = "";
}
if( JS9.INSTALLDIR ){
JS9.INSTALLDIR = JS9.cleanPath(JS9.INSTALLDIR);
}
}
if( JS9.INSTALLDIR && JS9.INSTALLDIR.slice(-1) !== "/" ){
// make sure there is a trailing slash
JS9.INSTALLDIR += "/";
}
JS9.TOROOT = JS9.INSTALLDIR.replace(/([^/.])+/g, "..");
// if the js9 inline object exists, add it the JS9 object
if( {}.hasOwnProperty.call(window, "JS9Inline") &&
typeof JS9Inline === "object" ){
JS9.inline = $.extend(true, {}, JS9Inline);
}
// set up the dynamic drive html window
if( JS9.LIGHTWIN === "dhtml" ){
// Creation of dhtmlwindowholder was done by a document.write in
// dhtmlwindow.js. We removed it from dhtmlwindow.js file because it
// interfered with the jquery search for js9.css above. Oh boy ...
// But it has to be somewhere!
$("

")
.attr("id", "dhtmlwindowholder")
.appendTo($(document.body))
.append("");
// allow in-line specification of images for all-in-one configuration
if( JS9.inline ){
dhtmlwindow.imagefiles = [JS9.inline["images/min.gif"],
JS9.inline["images/close.gif"],
JS9.inline["images/restore.gif"],
JS9.inline["images/resize.gif"]];
} else if( JS9.allinone ){
dhtmlwindow.imagefiles = [JS9.allinone.min,
JS9.allinone.close,
JS9.allinone.restore,
JS9.allinone.resize];
} else {
dhtmlwindow.imagefiles=[JS9.InstallDir("images/min.gif"),
JS9.InstallDir("images/close.gif"),
JS9.InstallDir("images/restore.gif"),
JS9.InstallDir("images/resize.gif")];
}
// once a window is loaded, set jupyter focus, if necessary
if( {}.hasOwnProperty.call(window, "Jupyter") ){
$(JS9.lightOpts[JS9.LIGHTWIN].topid)
.arrive("input", (el) => {
JS9.jupyterFocus($(el).parent());
});
}
}
// use plotly if loaded separately, otherwise use internal flot
JS9.globalOpts.plotLibrary = JS9.globalOpts.plotLibrary || "flot";
if( (JS9.globalOpts.plotLibrary === "plotly") &&
!{}.hasOwnProperty.call(window, "Plotly") ){
JS9.globalOpts.plotLibrary = "flot";
}
// if js9 prefs were defined/loaded explicitly, merge properties
if( {}.hasOwnProperty.call(window, "JS9Prefs") &&
typeof JS9Prefs === "object" ){
JS9.mergePrefs(JS9Prefs);
} else {
// look for and load json pref files
// (set this to false in the page to avoid loading a prefs file)
if( JS9.PREFSFILE ){
// load site preferences, if possible
JS9.loadPrefs(JS9.InstallDir(JS9.PREFSFILE), 0);
// load page preferences, if possible
JS9.loadPrefs(JS9.PREFSFILE, 0);
}
}
// if JS9 prefs have regionOpts, transfer them to Regions.opts
if( {}.hasOwnProperty.call(JS9, "Regions") ){
$.extend(true, JS9.Regions.opts, JS9.regionOpts);
}
delete JS9.regionOpts;
// if JS9 prefs have catalogOpts, transfer them to Catalogs.opts
if( {}.hasOwnProperty.call(JS9, "Catalogs") ){
$.extend(true, JS9.Catalogs.opts, JS9.catalogOpts);
}
delete JS9.catalogOpts;
// if JS9 prefs have crosshairOpts, transfer them to Crosshair.opts
if( {}.hasOwnProperty.call(JS9, "Crosshair") ){
$.extend(true, JS9.Crosshair.opts, JS9.crosshairOpts);
}
delete JS9.crosshairOpts;
// if JS9 prefs have gridOpts, transfer them to Grid.opts
if( {}.hasOwnProperty.call(JS9, "Grid") ){
$.extend(true, JS9.Grid.opts, JS9.gridOpts);
}
delete JS9.gridOpts;
// if JS9 prefs have emscriptenOpts, transfer them to Module
if( {}.hasOwnProperty.call(JS9, "Module") ){
$.extend(true, Module, JS9.emscriptenOpts);
}
delete JS9.emscriptenOpts;
// if JS9 prefs have fabricOpts, transfer them to Fabric.opts
if( {}.hasOwnProperty.call(JS9, "Fabric") ){
$.extend(true, JS9.Fabric.opts, JS9.fabricOpts);
// incorporate our fabric defaults into fabric itself
for( key of Object.keys(JS9.Fabric.opts) ){
fabric.Object.prototype[key] = JS9.Fabric.opts[key];
}
}
delete JS9.fabricOpts;
// regularize resize params
if( !JS9.globalOpts.resize ){
JS9.globalOpts.resizeHandle = false;
}
// backward compatibility (we moved this property 7/2018)
if( JS9.analOpts.prependJS9Dir !== undefined ){
JS9.globalOpts.prependJS9Dir = JS9.analOpts.prependJS9Dir;
delete JS9.analOpts.prependJS9Dir;
}
// backward compatibility (we moved this property 7/2018)
if( JS9.analOpts.dataDir !== undefined ){
JS9.globalOpts.dataDir = JS9.analOpts.dataDir;
delete JS9.analOpts.dataDir;
}
// backward compatibility (we renamed this property 8/2020)
if( JS9.globalOpts.regionsToClipboard !== undefined &&
JS9.globalOpts.regToClipboard === undefined ){
JS9.globalOpts.regToClipboard = JS9.globalOpts.regionsToClipboard;
delete JS9.globalOpts.regionsToClipboard;
}
// backward compatibility (we renamed this property 8/2020)
if( JS9.globalOpts.regionDisplay !== undefined &&
JS9.globalOpts.regDisplay === undefined ){
JS9.globalOpts.regDisplay = JS9.globalOpts.regionDisplay;
delete JS9.globalOpts.regionDisplay;
}
// backward compatibility (we renamed this property 8/2020)
if( JS9.globalOpts.regionConfigSize !== undefined &&
JS9.globalOpts.regConfigSize === undefined ){
JS9.globalOpts.regConfigSize = JS9.globalOpts.regionConfigSize;
delete JS9.globalOpts.regionConfigSize;
}
// backward compatibility (we renamed this property 8/2020)
if( JS9.globalOpts.regionTemplates !== undefined &&
JS9.globalOpts.regTemplates === undefined ){
JS9.globalOpts.regTemplates = JS9.globalOpts.regionTemplates;
delete JS9.globalOpts.regionTemplates;
}
// turn off resize on mobile platforms
if( JS9.BROWSER[3] ){
JS9.globalOpts.resizeHandle = false;
}
// replace with global opts with user opts, if necessary
if( {}.hasOwnProperty.call(window, "localStorage") &&
JS9.globalOpts.localStorage ){
try{ uopts = localStorage.getItem("globals"); }
catch(e){ uopts = null; }
if( uopts ){
try{ JS9.userOpts.displays = JSON.parse(uopts); }
catch(ignore){ /\* empty \*/ }
if( JS9.userOpts.displays ){
$.extend(true, JS9.globalOpts, JS9.userOpts.displays);
}
}
try{ uopts = localStorage.getItem("images"); }
catch(e){ uopts = null; }
if( uopts ){
try{ JS9.userOpts.images = JSON.parse(uopts); }
catch(ignore){ /\* empty \*/ }
if( JS9.userOpts.images ){
$.extend(true, JS9.imageOpts, JS9.userOpts.images);
}
}
// this gets replaced below
try{ uopts = localStorage.getItem("fits"); }
catch(e){ uopts = null; }
if( uopts ){
try{ JS9.userOpts.fits = JSON.parse(uopts); }
catch(ignore){ /\* empty \*/ }
}
try{ uopts = localStorage.getItem("regions"); }
catch(e){ uopts = null; }
if( uopts ){
try{ JS9.userOpts.regions = JSON.parse(uopts); }
catch(ignore){ /\* empty \*/ }
if( JS9.userOpts.regions ){
$.extend(true, JS9.Regions.opts, JS9.userOpts.regions);
}
}
try{ uopts = localStorage.getItem("grid"); }
catch(e){ uopts = null; }
if( uopts ){
try{ JS9.userOpts.images = JSON.parse(uopts); }
catch(ignore){ /\* empty \*/ }
if( JS9.userOpts.images ){
$.extend(true, JS9.Grid.opts, JS9.userOpts.images);
}
}
try{ uopts = localStorage.getItem("catalog"); }
catch(e){ uopts = null; }
if( uopts ){
try{ JS9.userOpts.images = JSON.parse(uopts); }
catch(ignore){ /\* empty \*/ }
if( JS9.userOpts.images ){
$.extend(true, JS9.Catalogs.Opts, JS9.userOpts.images);
}
}
}
// set debug flag
JS9.DEBUG = JS9.DEBUG || JS9.globalOpts.debug || 0;
// init main display(s)
$("div.JS9").each((index, element) => {
JS9.checkNew(new JS9.Display($(element)));
});
// load web worker
if( window.Worker && !JS9.allinone){
try{ JS9.worker = new JS9.WebWorker(JS9.InstallDir(JS9.WORKERFILE)); }
catch(e){ /\* empty \*/ }
}
// for allinone files, emscripten is already loaded so init FITS now
if( JS9.allinone ){
JS9.initFITS();
} else {
// load emscripten, which will trigger init FITS later
JS9.initEmscripten();
}
// desktop js9 gets helper from command line via the environment
if( window.electron ){
JS9.globalOpts.helperType = "nodejs";
}
// initialize helper support
JS9.helper = new JS9.Helper();
// add handler for postMessage events
window.addEventListener("message", (ev) => {
let s, msg;
// For Chrome, origin property is in the ev.originalEvent object
let origin = ev.origin || ev.originalEvent.origin;
const data = ev.data;
if( origin === "null" ){
origin = "unknown";
}
// if postMessage handling is disabled, just (log and) return
if( !JS9.globalOpts.postMessage ){
if( JS9.DEBUG ){
s = `JS9 ignoring postMessage, origin: ${origin}`;
if( typeof data === "string" ){
s += ` data: ${data}`;
} else if( typeof data === "object" ){
s += ` obj: ${JSON.stringify(Object.keys(data))}`;
} else {
s += ` typeof: ${typeof data}`;
}
JS9.log(s);
}
return;
}
if( typeof data === "string" ){
// json string passed (we hope)
try{ msg = JSON.parse(data); }
catch(e){ JS9.error(`can't parse msg: ${data}`, e); }
} else if( typeof data === "object" ){
// object was passed directly
msg = data;
} else {
JS9.error("invalid msg from postMessage");
}
// call the msg handler for JS9 API calls
JS9.msgHandler(msg, (stdout, stderr, errcode, a) => {
let res;
a = a || {};
res = {name: a.name, rtype: a.rtype, rdata: stdout,
stdout: stdout, stderr: stderr, errcode: errcode};
parent.postMessage({cmd: msg.cmd, res: res}, "\*");
});
}, false);
// initialize image filters
if( {}.hasOwnProperty.call(window, "ImageFilters") ){
JS9.ImageFilters = ImageFilters;
}
// initialize colormaps
JS9.initColormaps();
// initialize console commands
JS9.initCommands();
// init analysis
JS9.initAnalysis();
// register essential plugins
JS9.RegisterPlugin(JS9.MouseTouch.CLASS, JS9.MouseTouch.NAME,
JS9.MouseTouch.init,
{menuItem: "Mouse/Touch",
onplugindisplay: JS9.MouseTouch.init,
help: "help/mousetouch.html",
winTitle: "Mouse/Touch Actions",
winResize: true,
winDims: [JS9.MouseTouch.WIDTH,JS9.MouseTouch.HEIGHT]});
JS9.RegisterPlugin(JS9.Regions.CLASS, JS9.Regions.NAME,
JS9.Regions.init,
{divArgs: ["regions"],
winDims: [0, 0]});
JS9.RegisterPlugin(JS9.Crosshair.CLASS, JS9.Crosshair.NAME,
JS9.Crosshair.init,
{onmousemove: JS9.Crosshair.display,
onkeyboardaction: JS9.Crosshair.keyaction,
onkeyup: JS9.Crosshair.keyup,
onimageload: JS9.Crosshair.create,
winDims: [0, 0]});
JS9.RegisterPlugin(JS9.Grid.CLASS, JS9.Grid.NAME,
JS9.Grid.init,
{onsetpan: JS9.Grid.regrid,
onsetzoom: JS9.Grid.regrid,
onsetwcssys: JS9.Grid.regrid,
onsetwcsunits: JS9.Grid.regrid,
onimageload: JS9.Grid.regrid,
onupdateprefs: JS9.Grid.regrid,
winDims: [0, 0]});
JS9.RegisterPlugin(JS9.Dysel.CLASS, JS9.Dysel.NAME,
JS9.Dysel.init,
{onimageload: JS9.Dysel.imageload,
onimageclose: JS9.Dysel.imageclose,
winDims: [0, 0]});
JS9.RegisterPlugin(JS9.Titlebar.CLASS, JS9.Titlebar.NAME,
JS9.Titlebar.init,
{ onimageload: JS9.Titlebar.imageload,
onimagedisplay: JS9.Titlebar.imagedisplay,
onimageclose: JS9.Titlebar.imageclose,
winDims: [0, 0]});
// find divs associated with each plugin and run the constructor
JS9.instantiatePlugins();
// sort plugins
JS9.plugins.sort((a,b) => {
const t1 = a.opts.menuItem;
const t2 = b.opts.menuItem;
if( !t1 ){
return 1;
}
if( !t2 ){
return -1;
}
if( t1 < t2 ){
return -1;
}
if( t1 > t2 ){
return 1;
}
return 0;
});
// check web page url for file to load, if necessary
// check for display rename
if( JS9.globalOpts.processQueryParams ){
url = new URL(window.location);
if( url.searchParams ){
uopts = {};
arr = null;
for (const [key, value] of url.searchParams){
switch(key){
case "url":
case "file":
ufile = value;
break;
case "display":
dopts = {display: value};
break;
case "renamedisplay":
arr=value.split(/[:,]/);
break;
default:
uopts[key] = value;
break;
}
}
// rename display when all is ready
if( arr ){
JS9.prerename = [...arr];
}
// preload file, if necessary
if( ufile ){
if( dopts ){
JS9.Preload(ufile, uopts, dopts);
} else {
JS9.Preload(ufile, uopts);
}
}
}
}
// scroll to top
$(document).scrollTop(0);
// signal JS9 init is complete
JS9.inited = true;
$(document).trigger("JS9:init");
};
// return namespace
return JS9;
}());
// INIT: after document is loaded, perform JS9 initialization
$(document).ready(() => {
// when all is ready, we can preload images
$(document).on("JS9:ready", () => {
if( !JS9.readied ){
JS9.readied = true;
if( JS9.notNull(JS9.prerename) && JS9.prerename.length ){
JS9.RenameDisplay(...JS9.prerename);
delete JS9.prerename;
}
JS9.Preload(true);
}
});
$(document).on("JS9:init", () => {
if( JS9.helper.ready && JS9.fits.ready ){
// ... signal we are completely ready
$(document).trigger("JS9:ready", {status: "OK"});
}
});
// ... might need to wait for astroem (via emscripten) to finish ...
$(document).on("astroem:ready", () => {
// astroem is loaded: we can now initialize FITS support
JS9.initFITS();
// if Node.js is available (i.e., if enabled in the Electron app),
// try to mount the local file system
if( window.electron && JS9.hostFS ){
try{
// mount local file system or clear mount point
if( !JS9.vmount("/", JS9.hostFS) ){
delete JS9.hostFS;
}
}
catch(e){
// no mount point for local file system
delete JS9.hostFS;
}
}
if( JS9.helper.ready && JS9.inited ){
// ... signal we are completely ready
$(document).trigger("JS9:ready", {status: "OK"});
}
});
// wait for helper
$(document).on("JS9:helperReady", () => {
if( JS9.fits.ready && JS9.inited && !JS9.readied ){
// ... signal we are completely ready (but only once)
$(document).trigger("JS9:ready", {status: "OK"});
}
});
// init JS9 (unless explicitly specified not to)
if( $('div[data-js9init="false"]').length === 0 ){
JS9.init();
}
});

## Links found on page


