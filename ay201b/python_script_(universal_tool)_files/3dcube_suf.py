import numpy as np
import pyfits

img=pyfits.open('L1551.co.selfcal.fits')     # Read the fits data
dat=img[0].data
channel=dat[0]
#region=channel[55:110,0:95,0:95]*1000   # Select a region. Use mJy unit
region=channel[55:110,:,:]*1000   # Select a region. Use mJy unit
## In pyfits, 1st dimension is velocity, and 2nd/3rd dimensions are DEC/RA

## Stretch the cube in V axis
from scipy.interpolate import splrep
from scipy.interpolate import splev
vol=region.shape
stretch=1.0
## Stretch parameter: how many times longer the V axis will be
sregion=np.empty((vol[0]*stretch,vol[1],vol[2]))
chanindex=np.linspace(0,vol[0]-1,vol[0])
for j in range(0,vol[1]-1):
	for k in range(0,vol[2]-1):
		spec=region[:,j,k]
		tck=splrep(chanindex,spec)
		chanindex2=np.linspace(0,vol[0]-1,vol[0]*stretch)
		sregion[:,j,k]=splev(chanindex2,tck)

## Swap the axes, RA<->velo
sregion_temp=np.swapaxes(sregion,0,2)
## Flip the axis
sregion=sregion_temp[::-1,::-1,:]

#minflux=sregion.min()
#maxflux=sregion.max()

## Convert the pixels to RA/DEC coordinates
from pywcs import WCS
hdr = img[0].header
corr = WCS(hdr)
nx = hdr['NAXIS1']
ny = hdr['NAXIS2']
px = np.linspace(0,nx-1,nx)
py = np.linspace(0,ny-1,ny)
#print nx
#print py
## This header has 4 dimensions, so the pixel location needs 4 components.
## [RA, DEC, VEL, POL?]
#radec = corr.wcs_pix2sky([10,10,55,0], 1)
#wx, wy = corr.wcs_pix2sky([px,py], 0)
#wy = corr.wcs_pix2world(10, 0)
#wy = corr.wcs_pix2world([0,py], 0)
#print radec


from enthought.mayavi import mlab

## For volume rendering (problems in saving as a obj file)
#field=mlab.pipeline.scalar_field(sregion)     # Generate a scalar field
#mlab.pipeline.volume(field,vmin=2000,vmax=10000) # Render the field with dots

## For surface rendering
field=mlab.contour3d(sregion,colormap='gist_ncar')     # Generate a scalar field
#field.contour.maximum_contour = 13000
field.contour.minimum_contour = 2000
field.actor.property.opacity = 0.3

mlab.outline()
mlab.xlabel('RA(J2000)')
mlab.ylabel('DEC(J2000)')
mlab.zlabel('Velocity')
#mlab.axes()
#mlab.colorbar()

## Add 3-d text in the cube
mlab.text3d(30,80,23,'Outflows in L1551 IRS5',scale=2.)
#mlab.text(45,45,"outflows!",width=0.2,z=20)

## Draw arrows to show outflows etc.
vector1=mlab.quiver3d(55,55,30,1,1,0.2,mode='arrow',scale_factor=10.0,color=(0.0,0.0,1.0))
vector2=mlab.quiver3d(55,40,30,1,-1.2,0.2,mode='arrow',scale_factor=10.0,color=(0.0,0.0,1.0))
vector3=mlab.quiver3d(45,50,30,-0.8,1,0.2,mode='2dthick_arrow',scale_factor=10.0,color=(0.0,0.0,1.0))
vector4=mlab.quiver3d(49,48,30,0.2,0,1,mode='2darrow',scale_factor=8.0,color=(0.0,0.0,1.0))

vector5=mlab.quiver3d(47,58,20,-1,1.8,-0.2,mode='arrow',scale_factor=10.0,color=(1.0,0.0,0.0))
vector6=mlab.quiver3d(45,45,20,-1.2,-1,-0.2,mode='arrow',scale_factor=10.0,color=(1.0,0.0,0.0))
vector7=mlab.quiver3d(55,45,20,1,-1.4,-0.2,mode='2dthick_arrow',scale_factor=10.0,color=(1.0,0.0,0.0))
vector8=mlab.quiver3d(48,48,20,-0.2,0,-1,mode='2darrow',scale_factor=8.0,color=(1.0,0.0,0.0))

# Insert the continuum image as a background
img=pyfits.open('L1551.cont.fits')     # Read the fits data
dat=img[0].data
dat0=dat[0]
channel=dat0[0]
region=channel[0:95,0:95]*1000   # Select a region. Use mJy unit

## Swap the axes, RA<->velo
region_temp=np.swapaxes(region,0,1)
## Flip the axis
region=region_temp[::-1,::-1]

#field=mlab.pipeline.scalar_field(region)     # Generate a scalar field
#mlab.pipeline.volume(field,vmin=200) # Render the field with dots
field=mlab.contour3d(region,colormap='gist_ncar')     # Generate a scalar field
#field.contour.maximum_contour = 13000
field.contour.minimum_contour = 200
field.actor.property.opacity = 0.3

mlab.show()

## Save a .obj file. Can use programs like DAZ3D to convert it to .u3d file,
## and insert into a pdf doc.
#mlab.savefig('surface.obj')

## Make a section view of the 3d cube
#cut=mlab.pipeline.scalar_cut_plane(field.children[0],plane_orientation="x_axes")
#cut.enable_contours=True
#cut.contour.number_of_contours=5
## The axis could rotate, thus creating a PV diagram or a 2d image in one channel
