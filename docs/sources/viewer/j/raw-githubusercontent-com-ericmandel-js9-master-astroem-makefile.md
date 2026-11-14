---
source: https://raw.githubusercontent.com/ericmandel/js9/master/astroem/Makefile
fetched: 2026-11-14
status: 200
---

# astroem: astronomy/astrophysics C code compiled to javascript via emscripten
# see: http://kripken.github.io/emscripten-site/index.html
# astroem library containing our support code:
ASTROEMLIB = libastroem.a
# export files for wasm support:
ASTROEMWJS = astroemw.js
ASTROEMWASM = astroemw.wasm
# export files for non-wasm (javasript) support:
ASTROEMJS = astroem.js
# where is export files are installed
INSTALLDIR = ..
# use emscripten ports, rather than our own
# https://github.com/emscripten-ports
EMPORTS = -s USE\_ZLIB=1 -s USE\_BZIP2=1
# enable node file system for desktop use
EMFS = -lnodefs.js
# emcc compiler flags
# EMFLAGS = -g
# debugging
# EMFLAGS = -s ASSERTIONS=1
# debugging with symbols
# EMFLAGS = -O0 --memory-init-file 0 -s ASSERTIONS=1 -s SAFE\_HEAP=1
# production
# (no-deprecated switch to suppress scores of warnings in wcslib 5/5/2022)
EMFLAGS = -O3 -Wno-deprecated-non-prototype
# initial memory: support zscale up to 4096 \* 4096 \* 4-byte images
# EMOPTS = -s TOTAL\_MEMORY=67108864
# cfitsio requires memory growth
EMOPTS = -s TOTAL\_MEMORY=67108864 -s ALLOW\_MEMORY\_GROWTH=1 -sSTACK\_SIZE=5MB $(EMPORTS) $(EMFS)
# note to myself: in the event of a catastrophic drop in performance, see:
# https://github.com/emscripten-core/emscripten/issues/13899
# and try:
# -s BINARYEN\_EXTRA\_PASSES=--one-caller-inline-max-function-size=1
# can't use mem file: we don't know where the mem file will resides
# (moved out of compiler switches because this gives warning as of v2.0.32)
# NB: as of v3.1.59, emscripten no longer supports memory-init-file:
# MEMOPTS = --memory-init-file 0
MEMOPTS =
# javascript instead of wasm:
NOWASMOPTS = -s WASM=0 $(MEMOPTS)
# wasm support:
WASMOPTS = -s WASM=1 $(MEMOPTS)
# debugging
# WASMOPTS = -s WASM=1 -s SAFE\_HEAP=1 -s ASSERTIONS=1 $(MEMOPTS)
EMEXPORTS = -s EXPORTED\_FUNCTIONS="['\_malloc', '\_free', '\_initwcs', '\_freewcs', '\_wcsinfo', '\_pix2wcsstr', '\_wcs2pixstr', '\_reg2wcsstr', '\_wcssys', '\_wcsunits', '\_saostrtod', '\_saodtostr', '\_saodtype', '\_zscale', '\_gzopen', '\_gzread', '\_gzwrite', '\_gzclose', '\_gzseek', '\_BZ2\_bzopen', '\_BZ2\_bzread', '\_BZ2\_bzwrite', '\_BZ2\_bzclose', '\_openFITSFile', '\_openFITSMem', '\_getImageToArray', '\_filterTableToImage', '\_getHeaderToString', '\_closeFITSFile', '\_maxFITSMemory', '\_ffgerr', '\_ffgisz', '\_ffmahd', '\_ffghdn','\_ffmnhd', '\_ffghdt', '\_ffgky', '\_fffree', '\_listhdu', '\_tanhdr', '\_reproject', '\_madd', '\_imgtbl', '\_makehdr', '\_shrinkhdr', '\_imsection', '\_imannulusi', '\_imboxi', '\_imcirclei', '\_imellipsei', '\_imfieldi', '\_imlinei', '\_impiei', '\_imqtpiei', '\_impointi', '\_impandai', '\_imnannulusi', '\_imnboxi', '\_imnellipsei', '\_imnpiei', '\_impolygoni', '\_imvannulusi', '\_imvboxi', '\_imvellipsei', '\_imvpiei', '\_imvpointi', '\_imannulus', '\_imbox', '\_imcircle', '\_imellipse', '\_imfield', '\_imline', '\_impie', '\_imqtpie', '\_impoint', '\_impanda', '\_imnannulus', '\_imnbox', '\_imnellipse', '\_imnpie', '\_impolygon', '\_imvannulus', '\_imvbox', '\_imvellipse', '\_imvpie', '\_imvpoint', '\_regcnts', '\_vls', '\_vcat']" -s EXPORTED\_RUNTIME\_METHODS="['ccall', 'cwrap', 'writeArrayToMemory', 'stringToAscii']"
# JS9 C source code
JS9SRC = ../src
# include directories
EMINCS = -I./include
# extras to build emscripten runtime
EMEXTRAS = --pre-js pre.js --post-js post.js
# high-level wrapper code and support routines
WRAPPERS = ./wrappers
WSRCS = $(WRAPPERS)/wrappers.c \
$(WRAPPERS)/listhdu.c \
$(JS9SRC)/js9helper.c
WOBJS = $(WSRCS:%.c=%.o)
# routines built on top of cfitsio
JSFITSIO = ./jsfitsio
JSRCS = $(JSFITSIO)/jsfitsio.c \
$(JSFITSIO)/healpix.c
JOBJS = $(JSRCS:%.c=%.o)
# montage (re-project)
MONTAGE = ./montage
MSRCS = $(MONTAGE)/mGlobals.c \
$(MONTAGE)/mProjectPP.c \
$(MONTAGE)/mTANHdr.c \
$(MONTAGE)/mAdd.c \
$(MONTAGE)/mImgtbl.c \
$(MONTAGE)/mMakeHdr.c \
$(MONTAGE)/mShrinkHdr.c \
$(MONTAGE)/overlapAreaPP.c \
$(MONTAGE)/debugCheck.c \
$(MONTAGE)/checkHdr.c \
$(MONTAGE)/checkWCS.c \
$(MONTAGE)/two\_plane.c \
$(MONTAGE)/distort.c \
$(MONTAGE)/undistort.c \
$(MONTAGE)/initdistdata.c \
$(MONTAGE)/redefine\_pointing.c \
$(MONTAGE)/boundaries.c \
$(MONTAGE)/get\_files.c \
$(MONTAGE)/get\_hdr.c \
$(MONTAGE)/print\_rec.c \
$(MONTAGE)/convertCoordinates.c \
$(MONTAGE)/convertBesselianJulian.c \
$(MONTAGE)/convertEclEqu.c \
$(MONTAGE)/convertEquGal.c \
$(MONTAGE)/convertGalSgal.c \
$(MONTAGE)/computeFKCorrections.c \
$(MONTAGE)/precessBesselian.c \
$(MONTAGE)/precessJulian.c \
$(MONTAGE)/ccalc.c \
$(MONTAGE)/decimalDegreeToSex.c \
$(MONTAGE)/sexToDecimalDegree.c \
$(MONTAGE)/filePath.c \
$(MONTAGE)/mtbl.c
MOBJS = $(MSRCS:%.c=%.o)
# iraf zscale
ZSCALE = ./zscale
ZSSRCS = $(ZSCALE)/cdlzscale.c
ZSOBJS = $(ZSSRCS:%.c=%.o)
PKGOBJS = $(WOBJS) $(JOBJS) $(MOBJS) $(ZSOBJS)
PKGDIRS = $(WRAPPERS) $(JSFITSIO) $(MONTAGE) $(ZSCALE)
LIBS = lib/libcfitsio.a lib/libregions.a lib/libwcs.a lib/libutil.a \
lib/libem.a
# use Emscripten ports instead of our own
# lib/libz.a lib/libbz2.a
# emcc compiler and compiler flags:
CC = emcc
CFLAGS = $(EMFLAGS) $(EMINCS) -I$(JSFITSIO) -I$(ZSCALE) -I$(JS9SRC) -D'exit(n)=em\_exit(n)'
# emcc link command with common opts:
EMLINK = emcc $(EMFLAGS) $(EMOPTS) $(EMEXPORTS) $(EMEXTRAS)
all: $(ASTROEMLIB) $(ASTROEMJS) $(ASTROEMWJS)
# make a library using emar:
# https://github.com/emscripten-core/emscripten/issues/12382
$(ASTROEMLIB): $(PKGOBJS)
emar rcs $@ $?
$(ASTROEMJS): $(ASTROEMLIB) pre.js post.js shell-pre.js shell-post.js Makefile
@(echo "generating raw $(ASTROEMJS) ..."; \
$(EMLINK) $(NOWASMOPTS) $(ASTROEMLIB) $(LIBS) -o $(ASTROEMJS); \
echo "adding shell wrapper to generate $(ASTROEMJS) ..."; \
cat shell-pre.js > full\_$(ASTROEMJS); \
cat $(ASTROEMJS) >> full\_$(ASTROEMJS); \
cat shell-post.js >> full\_$(ASTROEMJS); \
mv full\_$(ASTROEMJS) $(ASTROEMJS);)
$(ASTROEMWJS): $(ASTROEMLIB) pre.js post.js shell-pre.js shell-post.js Makefile
@(echo "generating raw $(ASTROEMWJS) ..."; \
$(EMLINK) $(WASMOPTS) $(ASTROEMLIB) $(LIBS) -o $(ASTROEMWJS); \
echo "adding shell wrapper to generate $(ASTROEMWJS) ..."; \
cat shell-pre.js > full\_$(ASTROEMWJS); \
cat $(ASTROEMWJS) >> full\_$(ASTROEMWJS); \
cat shell-post.js >> full\_$(ASTROEMWJS); \
mv full\_$(ASTROEMWJS) $(ASTROEMWJS);)
install: FORCE
@(if [ -d $(INSTALLDIR) ]; then \
echo "installing $(ASTROEMJS) in: $(INSTALLDIR)"; \
cp -p $(ASTROEMJS) $(INSTALLDIR)/.; \
if [ x"$(ASTROEMWASM)" != x ]; then \
echo "also installing $(ASTROEMWJS): $(INSTALLDIR)"; \
cp -p $(ASTROEMWJS) $(INSTALLDIR)/.; \
cp -p $(ASTROEMWASM) $(INSTALLDIR)/.; \
fi; \
cd .. && $(MAKE) js9support; \
else \
echo "could not find JS9 directory: $(JS9)"; \
fi;)
clean: FORCE
@(rm -rf \*.o \*.a \*~ a.out\* foo\* \*.map \#\* \
astroem.\* astroemw.\*; \
for d in $(PKGDIRS); do \
cd $$d; \
if [ -f Makefile ]; then \
make clean; \
else \
rm -rf \*.o \*.a \*~ a.out\* foo\* \*.map \#\*; \
fi; \
cd ..; \
done;)
FORCE:

## Links found on page


