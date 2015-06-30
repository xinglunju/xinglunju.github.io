## Merge CSO and SMA SO data ##

## 1. Preparation of CSO data in miriad ##
miriad> 
fits in=c20kms_hnco.fits out=c20kms_hnco.cm op=xyin
regrid in=c20kms_hnco.cm out=c20kms_hnco.cm.regrid axes=1,2 project=sin options=noscale
puthd in=c20kms_hnco.cm.regrid/radesys value='FK5' type=ascii
puthd in=c20kms_hnco.cm.regrid/bunit value='K' type=ascii
puthd in=c20kms_hnco.cm.regrid/specsys value='LSRK' type=ascii
puthd in=c20kms_hnco.cm.regrid/velref value=257 type=integer
puthd in=c20kms_hnco.cm.regrid/telescop value='CSO' type=ascii
puthd in=c20kms_hnco.cm.regrid/observer value='xlu' type=ascii
puthd in=c20kms_hnco.cm.regrid/ctype4 value='STOKES' type=ascii
puthd in=c20kms_hnco.cm.regrid/cunit4 value='I' type=ascii
# Any other keywords?

fits in=c20kms_hnco.cm.regrid out=new.hnco.fits op=xyout

## 2. Import CSO fits image ##
CASA>
smaimage = '../../2012B-S097_2013A-S049/images/c20kms/MERGE/HNCO/c20kms.hnco.image'
smapb = '../../2012B-S097_2013A-S049/images/c20kms/MERGE/HNCO/c20kms.hnco.flux'

importfits(fitsimage="new.hnco.fits",imagename="cso.hnco.image")

# Swap stokes and velocity axes
imtrans(imagename="cso.hnco.image",outfile="cso.hnco.image.trans",order='0132')

# Smooth the velocity axis
ia.open('cso.hnco.image.trans')
im2 = ia.sepconvolve(outfile='cso.hnco.smooth.image',axes=[0,1,3],types=['gauss','gauss','gauss'],widths=['15arcsec','15arcsec','0.81MHz'])
im2.done()
ia.close()

# Regrid the velocity axis
imregrid(imagename='cso.hnco.smooth.image',template=smaimage,output='cso.hnco.regrid.image',asvelocity=True,axes=[0,1,3],interpolation='linear')

# From K to Jy/beam
frest =	219.79827
sdbeam = 34.0866
JyperK = 0.817 * (frest/100.)**2. * (sdbeam/10.)**2.
im1 = ia.imagecalc(outfile='cso.hnco.regrid.intensity.image',pixels=str(JyperK)+'*cso.hnco.regrid.image')
im1.done()
ia.close()
imhead('cso.hnco.regrid.intensity.image',mode='put',hdkey='bunit',hdvalue='Jy/beam')

## 3. Feather CSO and SMA data ##

# PB convolution of CSO data
impbcor(imagename='cso.hnco.regrid.intensity.image',outfile='cso.hnco.regrid.intensity.pb.image',pbimage=smapb,mode='multiply')

# Check the data with casafeather: effdishdiam is 10m, sdfactor is 1
feather(lowres='cso.hnco.regrid.intensity.pb.image',highres=smaimage,imagename='feathered.hnco.image',effdishdiam=10,lowpassfiltersd=True,sdfactor=1.0)

impbcor(imagename='feathered.hnco.image',pbimage=smapb,outfile='feathered.hnco.pbcor.image',mode='divide')

exportfits(imagename='feathered.hnco.image',fitsimage='feathered.hnco.image.fits',dropstokes=T,velocity=T)
exportfits(imagename='feathered.hnco.pbcor.image',fitsimage='feathered.hnco.pbcor.image.fits',dropstokes=T,velocity=T)

## 4. Final check

#imsmooth(imagename='feathered.hnco.pbcor.image',outfile='feathered.hnco.pbcor.image.smooth',kernel='gauss',major='34.51arcsec',minor='34.51arcsec',pa='0deg',targetres=True)

# Compare the above image with cso.hnco.regrid.intensity.imagev2?

## 5. Make moment maps

# Select channels between -20~40 km/s, rms=0.12 Jy/beam
rm -rf feathered.hnco.image.integrated*
rm -rf feathered.hnco.image.weighted_coord*
rm -rf feathered.hnco.image.weighted_dispersion_coord*

imsmooth(imagename='feathered.hnco.image',outfile='feathered.hnco.image.smooth',kernel='gauss',major='5.2arcsec',minor='3arcsec',pa='-176.035deg',targetres=T,overwrite=T)
ia.open('feathered.hnco.image.smooth')
im2 = ia.hanning(outfile='feathered.hnco.image.smooth.hann',drop=F)
im2.done()
ia.close()

# Smoothed image: rms~0.08 mJy/beam
immoments(imagename='feathered.hnco.image',moments=[0,1,2],chans='27~82',includepix=[0,9999.],mask='feathered.hnco.image.smooth.hann>0.4')

exportfits(imagename='feathered.hnco.image.integrated',fitsimage='feathered.hnco.image.integrated.fits',dropstokes=T)
exportfits(imagename='feathered.hnco.image.weighted_coord',fitsimage='feathered.hnco.image.weighted_coord.fits',dropstokes=T)
exportfits(imagename='feathered.hnco.image.weighted_dispersion_coord',fitsimage='feathered.hnco.image.weighted_dispersion_coord.fits',dropstokes=T)

