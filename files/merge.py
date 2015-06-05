## Adapt from Jens Kauffmann's script
## at https://sites.google.com/site/jenskauffmann/research-notes/adding-zero-spa

## Merge CSO and SMA line data ##

## 1. Preparation of CSO data in miriad ##
miriad> 
fits in=target_line1_ffts1w.fits out=target_line1_ffts1w.cm op=xyin
regrid in=target_line1_ffts1w.cm out=target_line1_ffts1w.cm.regrid axes=1,2 project=sin options=noscale
puthd in=target_line1_ffts1w.cm.regrid/radesys value='FK5' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/bunit value='K' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/specsys value='LSRK' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/velref value=257 type=integer
puthd in=target_line1_ffts1w.cm.regrid/telescop value='CSO' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/observer value='xlu' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/cunit1 value='deg' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/cunit2 value='deg' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/cunit3 value='m/s' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/ctype4 value='STOKES' type=ascii
puthd in=target_line1_ffts1w.cm.regrid/cunit4 value='1' type=ascii
# Any other keywords?

fits in=target_line1_ffts1w.cm.regrid out=new.line1.fits op=xyout

## 2. Import CSO fits image ##

importfits(fitsimage="cso.line1.fits",imagename="cso.line1.image")

# Swap stokes and velocity axes
imtrans(imagename="cso.line1.image",outfile="cso.line1.image.trans",order='0132')

# Smooth the velocity axis
ia.open('cso.line1.image.trans')
im2 = ia.sepconvolve(outfile='cso.line1.smooth.image',axes=[0,1,3],types=['box','box','box'],widths=['15arcsec','15arcsec','0.8125MHz'])
im2.done()
ia.close()

# Regrid the velocity axis
imregrid(imagename='cso.line1.smooth.image',template='sma.line1.image',output='cso.line1.regrid.image',asvelocity=True,axes=[3],interpolation='cubic')

# From K to Jy/beam
# Diameter of CSO is 10.4 m, resolution is 34.51 arcsec.
JyperK = 0.817 * (217.105/100.)**2. * (34.51/10.)**2.
im1 = ia.imagecalc(outfile='cso.line1.regrid.intensity.image',pixels=str(JyperK)+'*cso.line1.regrid.image')
im1.done()
ia.close()

imhead('cso.line1.regrid.intensity.image',mode='put',hdkey='bunit',hdvalue='Jy/beam')

## 3. Feather CSO and SMA data ##

# PB correction of SMA data
impbcor(imagename='sma.line1.image',outfile='sma.line1.pbcor.image',pbimage='sma.line1.flux',mode='divide')

# Check the data with casafeather: effdishdiam is 10m, sdfactor is 1.2?
feather(lowres='cso.line1.regrid.intensity.image',highres='sma.line1.pbcor.image',imagename='feathered.line1.image',effdishdiam=10,lowpassfiltersd=True,sdfactor=1.2)

impbcor(imagename='feathered.line1.image',pbimage='sma.line1.flux',outfile='feathered.line1.uniform.image',mode='multiply')

## 4. Final check ##

imsmooth(imagename='feathered.line1.image',outfile='feathered.line1.smooth.image',kernel='gauss',major='34.51arcsec',minor='34.51arcsec',pa='0deg',targetres=True)

# Compare the above image to cso.line1.regrid.intensity.image, are their fluxes consistent?

