---
source: https://raw.githubusercontent.com/Caltech-IPAC/firefly/dev/src/firefly/java/edu/caltech/ipac/visualize/plot/ImageHeader.java
fetched: 2026-11-14
status: 200
---

/\*
\* License information at https://github.com/Caltech-IPAC/firefly/blob/master/License.txt
\*/
package edu.caltech.ipac.visualize.plot;
import edu.caltech.ipac.astro.conv.CoordConv;
import edu.caltech.ipac.firefly.visualize.VisUtil;
import edu.caltech.ipac.util.SUTDebug;
import edu.caltech.ipac.visualize.plot.plotdata.FitsReadUtil;
import edu.caltech.ipac.visualize.plot.projection.Projection;
import edu.caltech.ipac.visualize.plot.projection.ProjectionParams;
import nom.tam.fits.Header;
import java.io.Serializable;
public class ImageHeader implements Serializable
{
// IF you modify this class please make sure you modify ProjectionParams if necessary
public static final String ORIGIN= "ORIGIN";
public static final String EXPTIME= "EXPTIME";
public static final String IMAGEZPT= "IMAGEZPT";
public static final String AIRMASS= "AIRMASS";
public static final String EXTINCT= "EXTINCT";
public static final String PALOMAR\_ID= "Palomar Transient Factory";
public static final int MAX\_SIP\_LENGTH = 10;
public final int EQ = 0;
public final int EC = 1;
public final int GA = 2;
public final int SGAL = 3;
public int bitpix, naxis, naxis1, naxis2, naxis3;
public double crpix1, crpix2, crval1, crval2, cdelt1, cdelt2, crota2;
public double crota1;
public double file\_equinox;
public String ctype1;
public String ctype2;
public String radecsys;
public double datamax, datamin;
public double bscale, bzero;
public String bunit;
public String origin;
public double airmass;
public double extinct;
public double imagezpt;
public double exptime;
public double blank\_value;
public int maptype;
public double cd1\_1, cd1\_2, cd2\_1, cd2\_2;
public double dc1\_1, dc1\_2, dc2\_1, dc2\_2;
public boolean using\_cd = false;
public long data\_offset;
public int plane\_number;
/\* the following are for PLATE projection \*/
public double plate\_ra, plate\_dec;
public double x\_pixel\_offset, y\_pixel\_offset;
public double x\_pixel\_size, y\_pixel\_size;
public double plt\_scale;
public double[] ppo\_coeff, amd\_x\_coeff, amd\_y\_coeff;
/\* the following are for SIRTF distortion corrections to the \*/
/\* GNOMONIC projection (ctype1 ending in -SIP)\*/
public double a\_order, ap\_order, b\_order, bp\_order;
public double[][] a = new double[MAX\_SIP\_LENGTH][MAX\_SIP\_LENGTH];
public double[][] ap = new double[MAX\_SIP\_LENGTH][MAX\_SIP\_LENGTH];
public double[][] b = new double[MAX\_SIP\_LENGTH][MAX\_SIP\_LENGTH];
public double[][] bp = new double[MAX\_SIP\_LENGTH][MAX\_SIP\_LENGTH];
public boolean map\_distortion = false;
public double[] pv1 = null;
public double[] pv2 = null;
public boolean using\_tpv= false;
public String keyword;
public ImageHeader()
{
}
public ImageHeader(Header header)
{
this(header, 0L, 0);
}
public ImageHeader(Header header, long HDU\_offset, int \_plane\_number)
{
int i, j;
boolean got\_cd1\_1, got\_cd1\_2, got\_cd2\_1, got\_cd2\_2;
boolean got\_pc1\_1, got\_pc1\_2, got\_pc2\_1, got\_pc2\_2;
double pc1\_1 = Double.NaN;
double pc1\_2 = Double.NaN;
double pc2\_1 = Double.NaN;
double pc2\_2 = Double.NaN;
boolean axes\_reversed = false;
double twist;
double rah,ram,ras, dsign,decd,decm,decs;
double dec\_deg,ra\_hours;
String ctype1\_trim = null;
long header\_size = FitsReadUtil.getHeaderSize(header);
data\_offset = HDU\_offset + header\_size;
plane\_number = \_plane\_number;
bitpix = header.getIntValue("BITPIX");
naxis = header.getIntValue("NAXIS");
naxis1 = header.getIntValue("NAXIS1");
naxis2 = header.getIntValue("NAXIS2");
if (naxis > 2)
naxis3 = header.getIntValue("NAXIS3");
else
naxis3 = 1;
crpix1 = header.getDoubleValue("CRPIX1", Double.NaN);
crpix2 = header.getDoubleValue("CRPIX2", Double.NaN);
crval1 = header.getDoubleValue("CRVAL1", Double.NaN);
crval2 = header.getDoubleValue("CRVAL2", Double.NaN);
cdelt1 = header.getDoubleValue("CDELT1");
cdelt2 = header.getDoubleValue("CDELT2");
crota1 = header.getDoubleValue("CROTA1");
crota2 = header.getDoubleValue("CROTA2");
/\*
\* CTYPEi indicates the coordinate type and projection. According to the standard specified by the paper: Representations of world coordinates in FITS
\* E. W. Greisen1 and M. R. Calabretta2 (paper I). The CTYPEn has linear and non-linear. Non-linear coordinate systems will be signaled by CTYPEi
\* in “4–3” form: the first four characters specify the coordinate type, the fifth character is a ’-’, and the remaining three characters
\* specify an algorithm code for computing the world coordinate value, for example ’ABCD-XYZ’. We explicitly allow the
\* possibility that the coordinate type may augment the algorithm code, for example ’FREQ-F2W’ and ’VRAD-F2W’ may denote
\* somewhat different algorithms (see Paper III). Coordinate types with names of less than four characters are padded on the right
\* with ’-’, and algorithm codes with less than three characters are padded on the right with blanks, for example ’RA---UV ’.
\* However, we encourage the use of three-letter algorithm codes. Particular coordinate types and algorithm codes must be established by convention.
\* CTYPEi values that are not in “4–3” form should be interpreted as linear axes. It is possible that there may be old FITS files with a linear axis for
\* which CTYPEi is, by chance, in 4–3 form. However, it is very unlikely that it will match a recognized algorithm code (use of
\* three-letter codes will reduce the chances). In such a case the axis should be treated as linear.
\*
\*/
if (header.containsKey("CTYPE1"))
{
ctype1 = header.getStringValue("CTYPE1") + " ";
ctype2 = header.getStringValue("CTYPE2") + " ";
ctype1\_trim = ctype1.trim();
String ctype1\_tail = ctype1.substring(4, 8);
// Either CTYPEi = 'LINEAR' or ctypei is defined but the value is not specified, default to linear
if (ctype1\_trim.isEmpty() || ctype1\_trim.equalsIgnoreCase("LINEAR")){
maptype = Projection.LINEAR;
}
else if (ctype1\_trim.contains("-TAN"))
maptype = Projection.GNOMONIC;
else if (ctype1\_trim.contains("-TPV")) {
maptype = Projection.TPV;
using\_tpv= true;
}
else if (ctype1\_trim.contains("-SIN"))
maptype = Projection.ORTHOGRAPHIC;
else if (ctype1\_trim.endsWith("-NCP"))
maptype = Projection.NCP;
else if (ctype1\_trim.endsWith("-ARC"))
maptype = Projection.ARC;
else if (ctype1\_trim.endsWith("-AIT"))
maptype = Projection.AITOFF;
else if (ctype1\_trim.endsWith("-ATF"))
maptype = Projection.AITOFF;
else if (ctype1\_trim.endsWith("-CAR"))
maptype = Projection.CAR;
else if (ctype1\_trim.endsWith("-CEA"))
maptype = Projection.CEA;
else if (ctype1\_trim.endsWith("-SFL"))
maptype = Projection.SFL;
else if (ctype1\_trim.endsWith("-GLS"))
maptype = Projection.SFL;
else if (ctype1\_trim.endsWith("-STG"))
maptype = Projection.STG;
else if (ctype1\_trim.endsWith("-HPX"))
maptype = Projection.HPX;
else if (ctype1\_trim.endsWith("----"))
maptype = Projection.LINEAR;
else if (ctype1\_tail.equals(" "))
maptype = Projection.LINEAR;
else
maptype = Projection.UNRECOGNIZED;
if ((ctype1\_trim.startsWith("DEC")) ||
(ctype1\_trim.startsWith("MM")) ||
(ctype1\_trim.startsWith("GLAT")) ||
(ctype1\_trim.startsWith("LAT")) ||
(ctype1\_trim.startsWith("ELAT")))
{
/\* flag that axes are reversed \*/
axes\_reversed = true;
}
}
else
maptype = Projection.UNSPECIFIED;
if (header.containsKey("DSKYGRID"))
maptype = Projection.ORTHOGRAPHIC;
if (maptype == Projection.CAR)
{
/\* wcs projection routines require crpix1 in -180 to 180 hemisphere \*/
double halfway = Math.abs(180.0 / cdelt1);
if (crpix1 > halfway)
crpix1 -= 2 \* halfway;
if (crpix1 < -halfway)
crpix1 += 2 \* halfway;
}
got\_cd1\_1 = header.containsKey("CD1\_1");
if (got\_cd1\_1)
{
cd1\_1 = header.getDoubleValue("CD1\_1");
}
else
{
got\_cd1\_1 = header.containsKey("CD001001");
if (got\_cd1\_1)
{
cd1\_1 = header.getDoubleValue("CD001001");
}
}
got\_pc1\_1 = header.containsKey("PC1\_1");
if (got\_pc1\_1)
{
pc1\_1 = header.getDoubleValue("PC1\_1");
}
else
{
got\_pc1\_1 = header.containsKey("PC001001");
if (got\_pc1\_1)
{
pc1\_1 = header.getDoubleValue("PC001001");
}
}
got\_cd1\_2 = header.containsKey("CD1\_2");
if (got\_cd1\_2)
{
cd1\_2 = header.getDoubleValue("CD1\_2");
}
else
{
got\_cd1\_2 = header.containsKey("CD001002");
if (got\_cd1\_2)
{
cd1\_2 = header.getDoubleValue("CD001002");
}
}
got\_pc1\_2 = header.containsKey("PC1\_2");
if (got\_pc1\_2)
{
pc1\_2 = header.getDoubleValue("PC1\_2");
}
else
{
got\_pc1\_2 = header.containsKey("PC001002");
if (got\_pc1\_2)
{
pc1\_2 = header.getDoubleValue("PC001002");
}
}
got\_cd2\_1 = header.containsKey("CD2\_1");
if (got\_cd2\_1)
{
cd2\_1 = header.getDoubleValue("CD2\_1");
}
else
{
got\_cd2\_1 = header.containsKey("CD002001");
if (got\_cd2\_1)
{
cd2\_1 = header.getDoubleValue("CD002001");
}
}
got\_pc2\_1 = header.containsKey("PC2\_1");
if (got\_pc2\_1)
{
pc2\_1 = header.getDoubleValue("PC2\_1");
}
else
{
got\_pc2\_1 = header.containsKey("PC002001");
if (got\_pc2\_1)
{
pc2\_1 = header.getDoubleValue("PC002001");
}
}
got\_cd2\_2 = header.containsKey("CD2\_2");
if (got\_cd2\_2)
{
cd2\_2 = header.getDoubleValue("CD2\_2");
}
else
{
got\_cd2\_2 = header.containsKey("CD002002");
if (got\_cd2\_2)
{
cd2\_2 = header.getDoubleValue("CD002002");
}
}
got\_pc2\_2 = header.containsKey("PC2\_2");
if (got\_pc2\_2)
{
pc2\_2 = header.getDoubleValue("PC2\_2");
}
else
{
got\_pc2\_2 = header.containsKey("PC002002");
if (got\_pc2\_2)
{
pc2\_2 = header.getDoubleValue("PC002002");
}
}
if ((!got\_cd1\_1 ) &&
(!got\_cd1\_2 ) &&
(!got\_cd2\_1 ) &&
(!got\_cd2\_2 ))
{
/\* no CD matrix values in header - look for PC matrix values \*/
if (got\_pc1\_1 )
{
cd1\_1 = cdelt1 \* pc1\_1;
got\_cd1\_1 = true;
}
if (got\_pc1\_2 )
{
cd1\_2 = cdelt1 \* pc1\_2;
got\_cd1\_2 = true;
}
if (got\_pc2\_1 )
{
cd2\_1 = cdelt2 \* pc2\_1;
got\_cd2\_1 = true;
}
if (got\_pc2\_2 )
{
cd2\_2 = cdelt2 \* pc2\_2;
got\_cd2\_2 = true;
}
}
if (using\_tpv) {
pv1= getPVArray(header,"1");
pv2= getPVArray(header,"2");
} else if (maptype == Projection.HPX) {
pv2= getPVArrayHPX(header);
}
datamax = header.getDoubleValue("DATAMAX", Double.NaN);
datamin = header.getDoubleValue("DATAMIN", Double.NaN);
bscale = header.getDoubleValue("BSCALE", 1.0);
bzero = header.getDoubleValue("BZERO", 0.0);
bunit = header.getStringValue("BUNIT");
if (bunit == null)
bunit = "DN";
origin = header.getStringValue(ORIGIN);
if (origin == null)
{
origin = "";
}
if (origin.startsWith(PALOMAR\_ID))
{
exptime = header.getDoubleValue(EXPTIME, 0.0);
imagezpt = header.getDoubleValue(IMAGEZPT, 0.0);
airmass = header.getDoubleValue(AIRMASS, 0.0);
extinct = header.getDoubleValue(EXTINCT, 0.0);
}
file\_equinox = header.getDoubleValue("EQUINOX", 0.0);
if (file\_equinox == 0.0)
file\_equinox = header.getDoubleValue("EPOCH", 2000.0);
radecsys = header.getStringValue("RADECSYS");
if (radecsys == null)
{
radecsys = header.getStringValue("RADESYS");
}
blank\_value = bitpix > 0 ? header.getDoubleValue("BLANK", Double.NaN) : Double.NaN;
if (SUTDebug.isDebug())
System.out.println("blank\_value = " + blank\_value);
String telescope = header.getStringValue("TELESCOP");
if ((telescope != null) && (telescope.startsWith("ISO")))
{
/\* ISO images have bad CD matrix - try not to use it \*/
if ((cdelt1 != 0) &&
(cdelt2 != 0))
{
//System.out.println("ISO image - using CDELTn");
got\_cd1\_1 = false; // prevent use of CD matrix
}
}
if ((!Double.isNaN(crval2)) &&
(!Double.isNaN(crval1)) &&
(!Double.isNaN(crpix1)) &&
(!Double.isNaN(crpix2)) &&
(maptype != Projection.UNRECOGNIZED) &&
((got\_cd1\_1 ) ||
(got\_cd1\_2 ) ||
(got\_cd2\_1 ) ||
(got\_cd2\_2 )) )
{
if (axes\_reversed)
{
double temp;
temp = crval1;
crval1 = crval2;
crval2 = temp;
temp = cd2\_2;
cd2\_2 = cd1\_2;
cd1\_2 = cd1\_1;
cd1\_1 = cd2\_1;
cd2\_1 = temp;
}
/\* save values for Greisen's formulas \*/
using\_cd = true;
/\* invert matrix \*/
double determinant = cd1\_1 \* cd2\_2 - cd1\_2 \* cd2\_1;
dc1\_1 = cd2\_2 / determinant;
dc1\_2 = - cd1\_2 / determinant;
dc2\_1 = - cd2\_1 / determinant;
dc2\_2 = cd1\_1 / determinant;
twist = Math.atan2(-cd1\_2, cd2\_2);
crota2 = twist \* Projection.rtd;
if (false) /\* patch out, now that CD matrix is handled \*/
{
/\* average the two methods to lessen the effect of skew \*/
twist = (Math.atan2(-cd2\_1, -cd1\_1) + twist) / 2.0;
if (Math.abs(cd1\_1) > Math.abs(cd1\_2))
{
cdelt1 = cd1\_1 / Math.cos(twist);
cdelt2 = cd2\_2 / Math.cos(twist);
}
else
{
cdelt1 = cd2\_1 / Math.sin(twist);
cdelt2 = - cd1\_2 / Math.sin(twist);
}
}
}
else
{
if (axes\_reversed)
{
double temp;
temp = crval1;
crval1 = crval2;
crval2 = temp;
temp = cdelt1;
cdelt1 = cdelt2;
cdelt2 = temp;
/\* dont know what to do with twist \*/
/\* will have to wait until I have a sample image \*/
}
}
/\* now do SIRTF distortion corrections \*/
if ((ctype1\_trim != null) && (ctype1\_trim.endsWith("-SIP")))
{
map\_distortion = true;
a\_order = header.getIntValue("A\_ORDER");
if (a\_order>= 0)
{
int len= (int)Math.min(a\_order+1, MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++)
{
for (j = 0; j < len; j++)
{
a[i][j] = 0.0;
if (i + j <= a\_order)
{
keyword = "A\_" + i + "\_" + j;
a[i][j] = header.getDoubleValue(keyword, 0.0);
/\*
System.out.println("a[" + i + "][" + j + "] = " + a[i][j]);
\*/
}
}
}
}
b\_order = header.getIntValue("B\_ORDER");
if (b\_order>= 0)
{
int len= (int)Math.min(b\_order+1, MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++)
{
for (j = 0; j < len; j++)
{
b[i][j] = 0.0;
if (i + j <= b\_order)
{
keyword = "B\_" + i + "\_" + j;
b[i][j] = header.getDoubleValue(keyword, 0.0);
/\*
System.out.println("b[" + i + "][" + j + "] = " + b[i][j]);
\*/
}
}
}
}
ap\_order = header.getIntValue("AP\_ORDER");
if (ap\_order>= 0)
{
int len= (int)Math.min(ap\_order+1, MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++)
{
for (j = 0; j < len; j++)
{
ap[i][j] = 0.0;
if (i + j <= ap\_order)
{
keyword = "AP\_" + i + "\_" + j;
ap[i][j] = header.getDoubleValue(keyword, 0.0);
/\*
System.out.println("ap[" + i + "][" + j + "] = " + ap[i][j]);
\*/
}
}
}
}
bp\_order = header.getIntValue("BP\_ORDER");
if (bp\_order>= 0)
{
int len= (int)Math.min(bp\_order+1, MAX\_SIP\_LENGTH);
for (i = 0; i < len; i++)
{
for (j = 0; j < len; j++)
{
bp[i][j] = 0.0;
if (i + j <= bp\_order)
{
keyword = "BP\_" + i + "\_" + j;
bp[i][j] = header.getDoubleValue(keyword, 0.0);
/\*
System.out.println("bp[" + i + "][" + j + "] = " + bp[i][j]);
\*/
}
}
}
}
}
if (using\_cd)
{
/\* need an approximation of cdelt1 and cdelt2 \*/
CoordinateSys in\_coordinate\_sys = CoordinateSys.makeCoordinateSys(
this.getJsys(), this.file\_equinox);
Projection proj = createProjection(in\_coordinate\_sys);
try
{
WorldPt proj\_center = proj.getWorldCoords(crpix1 - 1, crpix2 - 1);
WorldPt one\_to\_right = proj.getWorldCoords(crpix1, crpix2 - 1);
WorldPt one\_up = proj.getWorldCoords(crpix1 - 1, crpix2);
cdelt1 = - VisUtil.computeDistance( proj\_center, one\_to\_right);
cdelt2 = VisUtil.computeDistance( proj\_center, one\_up);
if (SUTDebug.isDebug())
{
System.out.println("CENTER lon = " + proj\_center.getLon() +
" lat = " + proj\_center.getLat() +
" one\_right lon = " + one\_to\_right.getLon() +
" lat = " + one\_to\_right.getLat() +
" cdelt1 = " + cdelt1 +
" one\_up lon = " + one\_up.getLon() +
" lat = " + one\_up.getLat() +
" cdelt2 = " + cdelt2);
}
}
catch (ProjectionException pe)
{
cdelt1 = 0;
cdelt2 = 0;
}
}
/\* now do Digital Sky Survey plate solution coefficients \*/
if (header.containsKey("PLTRAH") && !header.containsKey("CTYPE1"))
{
if (SUTDebug.isDebug())
System.out.println("ITS a PLATE projection");
maptype = Projection.PLATE;
rah = header.getDoubleValue("PLTRAH");
ram = header.getDoubleValue("PLTRAM");
ras = header.getDoubleValue("PLTRAS");
ra\_hours = rah + (ram / 60.0) + (ras / 3600.0);
plate\_ra = ra\_hours \* 15.0 \* Projection.dtr;
String decsign = header.getStringValue("PLTDECSN");
if (decsign.charAt(0) == '-')
dsign = -1.;
else
dsign = 1.;
decd = header.getDoubleValue("PLTDECD");
decm = header.getDoubleValue("PLTDECM");
decs = header.getDoubleValue("PLTDECS");
dec\_deg = dsign \* (decd+(decm/60.0)+(decs/3600.0));
plate\_dec = dec\_deg \* Projection.dtr;
/\*
fprintf(debug\_file,
"WCSINIT Plate center RA=%2.0f:%2.0f:%5.3f, Dec=%3.0f:%2.0f:%5.3f\n",
rah,ram,ras,dsign\*decd,decm,decs);
\*/
if (SUTDebug.isDebug())
System.out.println(" WCSINIT Plate center RA= " + rah + " " +
ram + " " + ras + " DEC = " + dsign\*decd + " " + decm + " " +
decs);
x\_pixel\_offset = header.getDoubleValue( "CNPIX1");
y\_pixel\_offset = header.getDoubleValue( "CNPIX2");
plt\_scale = header.getDoubleValue( "PLTSCALE");
x\_pixel\_size = header.getDoubleValue( "XPIXELSZ");
y\_pixel\_size = header.getDoubleValue( "YPIXELSZ");
ppo\_coeff = new double[6];
ppo\_coeff[0] = header.getDoubleValue( "PPO1");
ppo\_coeff[1] = header.getDoubleValue( "PPO2");
ppo\_coeff[2] = header.getDoubleValue( "PPO3");
ppo\_coeff[3] = header.getDoubleValue( "PPO4");
ppo\_coeff[4] = header.getDoubleValue( "PPO5");
ppo\_coeff[5] = header.getDoubleValue( "PPO6");
amd\_x\_coeff = new double[20];
amd\_x\_coeff[0] = header.getDoubleValue( "AMDX1");
amd\_x\_coeff[1] = header.getDoubleValue( "AMDX2");
amd\_x\_coeff[2] = header.getDoubleValue( "AMDX3");
amd\_x\_coeff[3] = header.getDoubleValue( "AMDX4");
amd\_x\_coeff[4] = header.getDoubleValue( "AMDX5");
amd\_x\_coeff[5] = header.getDoubleValue( "AMDX6");
amd\_x\_coeff[6] = header.getDoubleValue( "AMDX7");
amd\_x\_coeff[7] = header.getDoubleValue( "AMDX8");
amd\_x\_coeff[8] = header.getDoubleValue( "AMDX9");
amd\_x\_coeff[9] = header.getDoubleValue( "AMDX10");
amd\_x\_coeff[10] = header.getDoubleValue( "AMDX11");
amd\_x\_coeff[11] = header.getDoubleValue( "AMDX12");
amd\_x\_coeff[12] = header.getDoubleValue( "AMDX13");
amd\_x\_coeff[13] = header.getDoubleValue( "AMDX14");
amd\_x\_coeff[14] = header.getDoubleValue( "AMDX15");
amd\_x\_coeff[15] = header.getDoubleValue( "AMDX16");
amd\_x\_coeff[16] = header.getDoubleValue( "AMDX17");
amd\_x\_coeff[17] = header.getDoubleValue( "AMDX18");
amd\_x\_coeff[18] = header.getDoubleValue( "AMDX19");
amd\_x\_coeff[19] = header.getDoubleValue( "AMDX20");
amd\_y\_coeff = new double[20];
amd\_y\_coeff[0] = header.getDoubleValue( "AMDY1");
amd\_y\_coeff[1] = header.getDoubleValue( "AMDY2");
amd\_y\_coeff[2] = header.getDoubleValue( "AMDY3");
amd\_y\_coeff[3] = header.getDoubleValue( "AMDY4");
amd\_y\_coeff[4] = header.getDoubleValue( "AMDY5");
amd\_y\_coeff[5] = header.getDoubleValue( "AMDY6");
amd\_y\_coeff[6] = header.getDoubleValue( "AMDY7");
amd\_y\_coeff[7] = header.getDoubleValue( "AMDY8");
amd\_y\_coeff[8] = header.getDoubleValue( "AMDY9");
amd\_y\_coeff[9] = header.getDoubleValue( "AMDY10");
amd\_y\_coeff[10] = header.getDoubleValue( "AMDY11");
amd\_y\_coeff[11] = header.getDoubleValue( "AMDY12");
amd\_y\_coeff[12] = header.getDoubleValue( "AMDY13");
amd\_y\_coeff[13] = header.getDoubleValue( "AMDY14");
amd\_y\_coeff[14] = header.getDoubleValue( "AMDY15");
amd\_y\_coeff[15] = header.getDoubleValue( "AMDY16");
amd\_y\_coeff[16] = header.getDoubleValue( "AMDY17");
amd\_y\_coeff[17] = header.getDoubleValue( "AMDY18");
amd\_y\_coeff[18] = header.getDoubleValue( "AMDY19");
amd\_y\_coeff[19] = header.getDoubleValue( "AMDY20");
crpix1 = 0.5 - x\_pixel\_offset;
crpix2 = 0.5 - y\_pixel\_offset;
if (cdelt1 == 0.0)
{
cdelt1 = - plt\_scale \* x\_pixel\_size / 1000 / 3600;
cdelt2 = plt\_scale \* y\_pixel\_size / 1000 / 3600;
}
}
if (cdelt2<0) { //todo - this assumed the pixels were flipped, determine if we want to keep doing this
cdelt2 = -cdelt2;
crpix2 = naxis2 - crpix2+ 1;
}
}
public String getProjectionName()
{
return Projection.getProjectionName(maptype);
}
public int getCoordSys()
{
int retval = -1;
if (maptype == Projection.PLATE || maptype == Projection.LINEAR )
retval = EQ;
//non-linear case
//CTYPEi the first four characters are: RA-- and DEC-, GLON and GLAT, or ELON and ELAT, for equatorial, galactic, and ecliptic coordinates, respectively.
if (ctype1 != null)
{
String s = ctype1.substring(0, 2);
if (s.equals("RA"))
retval = EQ;
else if (s.equals("DE"))
retval = EQ;
else if (s.equals("LL"))
retval = EQ;
else if (s.equals("GL"))
retval = GA;
else if (s.equals("LO"))
retval = GA;
else if (s.equals("EL"))
retval = EC;
}
return retval;
}
public double getEquinox()
{
return file\_equinox;
}
public int getJsys()
{
int jsys;
switch (getCoordSys())
{
case EQ:
if ((radecsys != null) &&
(radecsys.startsWith("FK4")))
jsys = CoordConv.EQUATORIAL\_B;
else if ((radecsys != null) &&
((radecsys.startsWith("FK5")) ||
(radecsys.startsWith("ICRS"))))
jsys = CoordConv.EQUATORIAL\_J;
else if (file\_equinox < 2000.0)
jsys = CoordConv.EQUATORIAL\_B;
else
jsys = CoordConv.EQUATORIAL\_J;
break;
case EC:
if ((radecsys != null) &&
(radecsys.startsWith("FK4")))
jsys = CoordConv.ECLIPTIC\_B;
else if ((radecsys != null) &&
(radecsys.startsWith("FK5")))
jsys = CoordConv.ECLIPTIC\_J;
else if (file\_equinox < 2000.0)
jsys = CoordConv.ECLIPTIC\_B;
else
jsys = CoordConv.ECLIPTIC\_J;
break;
case GA:
jsys = CoordConv.GALACTIC;
break;
case SGAL:
jsys = CoordConv.SUPERGALACTIC;
break;
default:
jsys = -1;
}
return jsys;
}
public double[] getPVArray(Header header, String idxStr) {
double[] retval = new double[40];
for(int i=0; i<40; i++) {
retval[i]= header.getDoubleValue("PV"+idxStr+"\_"+i, i==1?1D:0D);
}
return retval;
}
public double[] getPVArrayHPX(Header header) {
double[] retval = new double[2];
retval[0] = header.getDoubleValue("PV2\_1", 4.0);
retval[1] = header.getDoubleValue("PV2\_2", 3.0);
return retval;
}
public Projection createProjection(CoordinateSys csys) {
return new Projection(createProjectionParams(this),csys);
}
public Projection createProjection() {
return createProjection(determineCoordSys());
}
public CoordinateSys determineCoordSys() {
int sys= getJsys();
CoordinateSys imageCoordSys= CoordinateSys.makeCoordinateSys( sys, getEquinox() );
// tmp
if ((getEquinox() == 2000.0) && (sys == -1) ) { // tmp
imageCoordSys= CoordinateSys.EQ\_J2000; // tmp
} // tmp
// tmp
return imageCoordSys;
}
public static ProjectionParams createProjectionParams(ImageHeader hdr) {
ProjectionParams params= new ProjectionParams();
params.bitpix= hdr.bitpix;
params.naxis = hdr.naxis;
params.naxis1= hdr.naxis1;
params.naxis2= hdr.naxis2;
params.naxis3= hdr.naxis3;
params.crpix1= hdr.crpix1;
params.crpix2= hdr.crpix2;
params.crval1= hdr.crval1;
params.crval2= hdr.crval2;
params.cdelt1= hdr.cdelt1;
params.cdelt2= hdr.cdelt2;
params.crota2= hdr.crota2;
params.crota1= hdr.crota1;
params.file\_equinox= hdr.file\_equinox;
params.ctype1= hdr.ctype1;
params.ctype2= hdr.ctype2;
params.radecsys= hdr.radecsys;
params.datamax= hdr.datamax;
params.datamin= hdr.datamin;
//params.bscale= hdr.bscale;
//params.bzero= hdr.bzero;
//params.bunit= hdr.bunit;
//params.blank\_value= hdr.blank\_value;
params.maptype= hdr.maptype;
params.cd1\_1= hdr.cd1\_1;
params.cd1\_2= hdr.cd1\_2;
params.cd2\_1= hdr.cd2\_1;
params.cd2\_2= hdr.cd2\_2;
params.dc1\_1= hdr.dc1\_1;
params.dc1\_2= hdr.dc1\_2;
params.dc2\_1= hdr.dc2\_1;
params.dc2\_2= hdr.dc2\_2;
params.using\_cd= hdr.using\_cd;
params.using\_tpv= hdr.using\_tpv;
params.pv1= hdr.pv1;
params.pv2= hdr.pv2;
params.plate\_ra= hdr.plate\_ra;
params.plate\_dec= hdr.plate\_dec;
params.x\_pixel\_offset= hdr.x\_pixel\_offset;
params.y\_pixel\_offset= hdr.y\_pixel\_offset;
params.x\_pixel\_size= hdr.x\_pixel\_size;
params.y\_pixel\_size= hdr.y\_pixel\_size;
params.plt\_scale= hdr.plt\_scale;
params.ppo\_coeff= hdr.ppo\_coeff;
params.amd\_x\_coeff= hdr.amd\_x\_coeff;
params.amd\_y\_coeff= hdr.amd\_y\_coeff;
params.a\_order= hdr.a\_order;
params.ap\_order= hdr.ap\_order;
params.b\_order= hdr.b\_order;
params.bp\_order= hdr.bp\_order;
params.a= hdr.a;
params.ap= hdr.ap;
params.b= hdr.b;
params.bp= hdr.bp;
params.map\_distortion= hdr.map\_distortion;
params.keyword= hdr.keyword;
return params;
}
public String toString()
{
StringBuffer sb = new StringBuffer();
sb.append(
"\n bitpix = " + bitpix + " naxis = " + naxis +
" naxis1 = " + naxis1 + " naxis2 = " + naxis2 +
" naxis3 = " + naxis3);
sb.append(
"\n crpix1 = " + crpix1 + " crpix2 = " + crpix2 +
"\n crval1 = " + crval1 + " crval2 = " + crval2 +
"\n cdelt1 = " + cdelt1 + " cdelt2 = " + cdelt2 +
" crota2 = " + crota2);
if (using\_cd)
{
sb.append(
"\n cd1\_1 = " + cd1\_1 + " cd1\_2 = " + cd1\_2 + " cd2\_1 = " +
cd2\_1 + " cd2\_2 = " + cd2\_2);
sb.append(
"\n dc1\_1 = " + dc1\_1 + " dc1\_2 = " + dc1\_2 + " dc2\_1 = " +
dc2\_1 + " dc2\_2 = " + dc2\_2);
}
sb.append(
"\n file\_equinox = " + file\_equinox + " ctype1 = " + ctype1 +
" ctype2 = " + ctype2);
sb.append("\n maptype = " + Projection.getProjectionName(maptype));
return sb.toString();
}
}

## Links found on page


