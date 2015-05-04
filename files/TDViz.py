from enthought.traits.api import HasTraits, Button, Instance, List, Str, Enum, Float, File
from enthought.traits.ui.api import View, Item, VGroup, HSplit, CheckListEditor, HGroup
from enthought.tvtk.pyface.scene_editor import SceneEditor
from enthought.mayavi.tools.mlab_scene_model import MlabSceneModel
from enthought.mayavi.core.ui.mayavi_scene import MayaviScene
from enthought.mayavi import mlab
import numpy as np
try:
	import astropy.io.fits as pyfits
except ImportError:
	import pyfits

class TDViz(HasTraits):
	fitsfile    = File(filter=[u"*.fits"])
	plotbutton1 = Button(u"Plot")
	plotbutton2 = Button(u"Plot")
	clearbutton = Button(u"Clear")
	scene = Instance(MlabSceneModel, ())
	rendering = Enum("Surface", "Volume")
	save_the_scene = Button(u"Save")
	add_cut = Button(u"Cutthrough")
	zscale = Float(1.0)
	xstart = Float(0.0)
	xend   = Float(1.0)
	ystart = Float(0.0)
	yend   = Float(1.0)
	zstart = Float(0.0)
	zend   = Float(1.0)
	datamin= Float(0.0) # rms = 600 mJy
	datamax= Float(1.0)
	opacity= Float(0.3)

	view = View(
      HSplit(
		VGroup(
			Item("fitsfile", label=u"Select a FITS datacube", show_label=True),
			Item("rendering", tooltip=u"Choose the rendering type you like", show_label=True),
			Item('plotbutton1', tooltip=u"Plot the 3D scene with volume rendering", visible_when="rendering=='Volume'"),
			Item('plotbutton2', tooltip=u"Plot the 3D scene with surface rendering", visible_when="rendering=='Surface'"),
			HGroup(Item('xstart', tooltip=u"starting pixel in X axis", show_label=True),
				   Item('xend', tooltip=u"ending pixel in X axis", show_label=True)),
			HGroup(Item('ystart', tooltip=u"starting pixel in Y axis", show_label=True),
				   Item('yend', tooltip=u"ending pixel in Y axis", show_label=True)),
			HGroup(Item('zstart', tooltip=u"starting pixel in Z axis", show_label=True),
				   Item('zend', tooltip=u"ending pixel in Z axis", show_label=True)),
			HGroup(Item('datamax', tooltip=u"Maximum datapoint shown", show_label=True),
				   Item('datamin', tooltip=u"Minimum datapoint shown", show_label=True)),
			Item('zscale', tooltip=u"Stretch the datacube in Z axis", show_label=True),
			Item('opacity', tooltip=u"Opacity of the scene", show_label=True),
			Item("save_the_scene", tooltip=u"Save current scene in a .obj file. There is no guarantee that everything you see are saved as what they are!", visible_when="rendering=='Surface'"),
			Item("add_cut", tooltip="Add a cutthrough view"),
			'clearbutton',
			show_labels=False
		),
		VGroup(
		    Item(name='scene',
                editor=SceneEditor(scene_class=MayaviScene),
                resizable=True,
                height=600,
                width=600
            ), show_labels=False
		)
      ),
	  resizable=True,
	  title=u"TDViz"
	)

	def _fitsfile_changed(self):
		img = pyfits.open(self.fitsfile)     # Read the fits data
		dat = img[0].data
		self.hdr  = img[0].header
		
		naxis = self.hdr['NAXIS']
		## The three axes loaded by pyfits are: velo, dec, ra
		## Swap the axes, RA<->velo
		if naxis == 4:
			self.data = np.swapaxes(dat[0],0,2)*1000.0
		elif naxis == 3:
			self.data = np.swapaxes(dat,0,2)*1000.0
		onevpix = self.hdr['CDELT3']
		## Flip the axis
		if onevpix > 0:
			self.data = self.data[:,:,::-1]
		self.data[np.isnan(self.data)] = 0.0
		self.data[np.isinf(self.data)] = 0.0

		self.datamax = np.asscalar(np.max(self.data))
		self.datamin = np.asscalar(np.min(self.data))
		self.xend    = self.data.shape[0]
		self.yend    = self.data.shape[1]
		self.zend    = self.data.shape[2]

	def loaddata(self):
		channel = self.data
		## Select a region, use mJy unit
		region=channel[self.xstart:self.xend,self.ystart:self.yend,self.zstart:self.zend]

		## Stretch the cube in V axis
		from scipy.interpolate import splrep
		from scipy.interpolate import splev
		vol=region.shape
		stretch=self.zscale
		## Stretch parameter: how many times longer the V axis will be
		sregion=np.empty((vol[0],vol[1],vol[2]*stretch))
		chanindex=np.linspace(0,vol[2]-1,vol[2])
		for j in range(0,vol[0]-1):
		    for k in range(0,vol[1]-1):
		        spec=region[j,k,:]
		        tck=splrep(chanindex,spec)
		        chanindex2=np.linspace(0,vol[2]-1,vol[2]*stretch)
		        sregion[j,k,:]=splev(chanindex2,tck)
		self.sregion = sregion

	def _plotbutton1_fired(self):
		mlab.clf()
		self.loaddata()
		field=mlab.pipeline.scalar_field(self.sregion)     # Generate a scalar field
		mlab.pipeline.volume(field,vmax=self.datamax,vmin=self.datamin) # Render the field with dots

		mlab.outline()
		mlab.xlabel('RA(J2000)')
		mlab.ylabel('DEC(J2000)')
		mlab.zlabel('Velocity')
		mlab.view(azimuth=0, elevation=0)
		mlab.show()
		
		self.field   = field

	def _plotbutton2_fired(self):
		mlab.clf()
		self.loaddata()
		field=mlab.contour3d(self.sregion,colormap='gist_ncar')     # Generate a scalar field
		field.contour.maximum_contour = self.datamax
		field.contour.minimum_contour = self.datamin
		field.actor.property.opacity = self.opacity

		mlab.outline()
		mlab.xlabel('RA(J2000)')
		mlab.ylabel('DEC(J2000)')
		mlab.zlabel('Velocity')
		mlab.view(azimuth=0, elevation=0)
		mlab.show()

		self.field   = field

#	def _datamax_changed(self):
#		if hasattr(self, "field"):
#			self.field.contour.maximum_contour = self.datamax

	def _add_cut_fired(self):
		cut=mlab.pipeline.scalar_cut_plane(self.field,plane_orientation="x_axes")
		cut.enable_contours=True
		cut.contour.number_of_contours=5

	def _save_the_scene_fired(self):
		mlab.savefig('3dscene.obj')

	def _clearbutton_fired(self):
		mlab.clf()

app = TDViz()
app.configure_traits()   
