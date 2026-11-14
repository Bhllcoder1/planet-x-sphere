---
source: https://raw.githubusercontent.com/Caltech-IPAC/firefly/dev/src/firefly/java/edu/caltech/ipac/visualize/plot/projection/GnomonicProjection.java
fetched: 2026-11-14
status: 200
---

/\*
\* License information at https://github.com/Caltech-IPAC/firefly/blob/master/License.txt
\*/
package edu.caltech.ipac.visualize.plot.projection;
import edu.caltech.ipac.visualize.plot.ImageHeader;
import edu.caltech.ipac.visualize.plot.ProjectionPt;
import edu.caltech.ipac.visualize.plot.Pt;
import edu.caltech.ipac.visualize.plot.ProjectionException;
public class GnomonicProjection {
static double dtr = Projection.dtr;
static double rtd = Projection.rtd;
static public ProjectionPt RevProject(double ra, double dec,
ProjectionParams hdr, boolean useProjException) throws ProjectionException {
int i, j;
double fsamp\_correction, fline\_correction;
double lat, lon;
double rpp1, rpp2, lat0, lon0;
double aa, ff1, ff2, rho;
double fline, fsamp, rtwist, temp;
double x, y;
double crpix1 = hdr.crpix1;
double crpix2 = hdr.crpix2;
double glong = hdr.crval1;
double glat = hdr.crval2;
double cdelt1 = hdr.cdelt1;
double cdelt2 = hdr.cdelt2;
double twist = hdr.crota2;
boolean using\_cd = hdr.using\_cd;
double dc1\_1 = hdr.dc1\_1;
double dc1\_2 = hdr.dc1\_2;
double dc2\_1 = hdr.dc2\_1;
double dc2\_2 = hdr.dc2\_2;
/\*
if (SUTDebug.isDebug())
System.out.println(
"RBH GnomonicProjection.RevProject input ra = " + ra +
" dec = " + dec);
\*/
lon = ra \* dtr;
lat = dec \* dtr;
/\*
if (SUTDebug.isDebug())
System.out.println(
"RBH GnomonicProjection.RevProject radians lon = " + lon +
" lat = " + lat + " dtr = " + dtr);
\*/
rpp1 = -cdelt1 \* dtr;
rpp2 = -cdelt2 \* dtr;
lon0 = glong \* dtr;
lat0 = glat \* dtr;
aa = Math.cos(lat) \* Math.cos(lon - lon0);
ff1 = 1. / (Math.sin(lat0) \* Math.sin(lat) + aa \* Math.cos(lat0));
ff2 = 1. / (Math.sin(lat0) \* Math.sin(lat) + aa \* Math.cos(lat0));
if (ff1 < 0) {
/\* we're more than 90 degrees from projection center \*/
if (useProjException) throw new ProjectionException("coordinates not on image");
else return null;
} else {
fline = -ff2 \* (Math.cos(lat0) \* Math.sin(lat) - aa \* Math.sin(lat0));
fsamp = -ff1 \* Math.cos(lat) \* Math.sin(lon - lon0);
if (using\_cd) {
temp = -(dc1\_1 \* fsamp + dc1\_2 \* fline) \* rtd;
fline = -(dc2\_1 \* fsamp + dc2\_2 \* fline) \* rtd;
fsamp = temp;
} else {
/\* do the twist \*/
rtwist = twist \* dtr; /\* convert to radians \*/
temp = fsamp \* Math.cos(rtwist) + fline \* Math.sin(rtwist);
fline = -fsamp \* Math.sin(rtwist) + fline \* Math.cos(rtwist);
fsamp = temp;
fsamp = (fsamp / rpp1); /\* now apply cdelt \*/
fline = (fline / rpp2);
}
if (hdr.map\_distortion) {
/\* apply SIRTF distortion corrections \*/
fsamp\_correction = 0.0;
int len = (int) Math.min(hdr.ap\_order + 1, ImageHeader.MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++) {
for (j = 0; j < len; j++) {
if (i + j <= hdr.ap\_order) {
fsamp\_correction +=
hdr.ap[i][j] \* Math.pow(fsamp, i) \* Math.pow(fline, j);
}
}
}
/\*
if (SUTDebug.isDebug())
System.out.println("deproject: fsamp correction = " + fsamp\_correction);
\*/
fline\_correction = 0.0;
len = (int) Math.min(hdr.bp\_order + 1, ImageHeader.MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++) {
for (j = 0; j < len; j++) {
if (i + j <= hdr.bp\_order) {
fline\_correction +=
hdr.bp[i][j] \* Math.pow(fsamp, i) \* Math.pow(fline, j);
}
}
}
fsamp += fsamp\_correction;
fline += fline\_correction;
/\*
if (SUTDebug.isDebug())
System.out.println("deproject: fline correction = " + fline\_correction);
\*/
}
}
/\*
if (SUTDebug.isDebug())
System.out.println(
"RBH GnomonicProjection.RevProject fsamp = " + fsamp +
" fline = " + fline);
\*/
x = fsamp + crpix1 - 1;
y = fline + crpix2 - 1;
ProjectionPt image\_pt = new ProjectionPt(x, y);
return (image\_pt);
}
static public Pt FwdProject(double x, double y, ProjectionParams hdr) {
int i, j;
double fsamp\_correction, fline\_correction;
double fsamp, fline;
double lat, lon;
double rpp1, rpp2, glongr, glatr;
double rtwist, temp;
double delta, beta;
double xxx, yyy, xx, yy;
double crpix1 = hdr.crpix1;
double crpix2 = hdr.crpix2;
double glong = hdr.crval1;
double glat = hdr.crval2;
double cdelt1 = hdr.cdelt1;
double cdelt2 = hdr.cdelt2;
double twist = hdr.crota2;
boolean using\_cd = hdr.using\_cd;
double cd1\_1 = hdr.cd1\_1;
double cd1\_2 = hdr.cd1\_2;
double cd2\_1 = hdr.cd2\_1;
double cd2\_2 = hdr.cd2\_2;
fsamp = x - crpix1 + 1;
fline = y - crpix2 + 1;
/\*
if (SUTDebug.isDebug())
{
System.out.println(
"RBH GnomonicProjection.FwdProject: projection name " + hdr.maptype);
System.out.println(
"RBH GnomonicProjection.FwdProject: input x = " + x + " y = " + y +
" fsamp = " + fsamp + " fline = " + fline);
//Thread.currentThread().dumpStack();
}
\*/
if (hdr.map\_distortion) {
/\* apply SIRTF distortion corrections \*/
fsamp\_correction = 0.0;
int len = (int) Math.min(hdr.a\_order + 1, ImageHeader.MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++) {
for (j = 0; j < len; j++) {
if (i + j <= hdr.a\_order) {
fsamp\_correction +=
hdr.a[i][j] \* Math.pow(fsamp, i) \* Math.pow(fline, j);
}
}
}
/\*
if (SUTDebug.isDebug())
System.out.println("dimage\_to\_sky: fsamp correction = " + fsamp\_correction);
\*/
fline\_correction = 0.0;
len = (int) Math.min(hdr.b\_order + 1, ImageHeader.MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++) {
for (j = 0; j < len; j++) {
if (i + j <= hdr.b\_order) {
fline\_correction +=
hdr.b[i][j] \* Math.pow(fsamp, i) \* Math.pow(fline, j);
}
}
}
fsamp += fsamp\_correction;
fline += fline\_correction;
/\*
if (SUTDebug.isDebug())
System.out.println("dimage\_to\_sky: fline correction = " + fline\_correction);
\*/
}
if (using\_cd) {
xx = -(cd1\_1 \* fsamp + cd1\_2 \* fline) \* dtr;
yy = -(cd2\_1 \* fsamp + cd2\_2 \* fline) \* dtr;
} else {
rpp1 = cdelt1 \* dtr; /\* radians per pixel \*/
rpp2 = cdelt2 \* dtr; /\* radians per pixel \*/
xx = -fsamp \* rpp1;
yy = -fline \* rpp2;
rtwist = twist \* dtr; /\* convert to radians \*/
temp = xx \* Math.cos(rtwist) - yy \* Math.sin(rtwist); /\* do twist \*/
yy = xx \* Math.sin(rtwist) + yy \* Math.cos(rtwist);
xx = temp;
}
delta = Math.atan(Math.sqrt(xx \* xx + yy \* yy));
if ((xx == 0.0) && (yy == 0.0))
yy = 1.0; /\* avoid domain error in atan2 \*/
beta = Math.atan2(-xx, yy);
glatr = glat \* dtr;
glongr = glong \* dtr;
lat = Math.asin(-Math.sin(delta) \* Math.cos(beta) \* Math.cos(glatr) +
Math.cos(delta) \* Math.sin(glatr));
xxx = Math.sin(glatr) \* Math.sin(delta) \* Math.cos(beta) +
Math.cos(glatr) \* Math.cos(delta);
yyy = Math.sin(delta) \* Math.sin(beta);
lon = glongr + Math.atan2(yyy, xxx);
lat = lat \* rtd;
lon = lon \* rtd;
/\*
if (SUTDebug.isDebug())
System.out.println(
"RBH GnomonicProjection.FwdProject: output lon = " + lon +
" lat = " + lat);
\*/
Pt \_pt = new Pt(lon, lat);
return (\_pt);
}
}

## Links found on page


