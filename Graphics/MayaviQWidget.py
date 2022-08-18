import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor
from mayavi.mlab import move, pitch, yaw
import Core
import FromFile
import Graphics
import ResultsAnalysis

class Visualization(HasTraits):
    scene = Instance(MlabSceneModel, ())

    def __init__(self, suffix, subdir):
        HasTraits.__init__(self)
        self.suffix = suffix
        self.subdir = subdir
        self.num_kinds, self.included_atoms = FromFile.Kinds(
            Core.Extension().files4defect(".inp", self.subdir)).searchingfile()
        self.num_kind = self.num_kinds + 1

        for elem in list(self.included_atoms):
            exec(f'self.color{elem} = Graphics.atom_lookup(elem).identification()[0]')
            exec(f'self.size{elem} = Graphics.atom_lookup(elem).identification()[1]')
            exec(f'self.k{elem}_x, self.k{elem}_y, self.k{elem}_z = ResultsAnalysis.Atoms3DplotData(self.suffix,elem).DataPoints4Kind()')

    @on_trait_change('scene.activated')
    def update_plot(self):
        # This function is called when the view is opened. We don't
        # populate the scene when the view is not yet open, as some
        # VTK features require a GLContext.
        # We can do normal mlab calls on the embedded scene.
        for elem in list(self.included_atoms):
            self.scene.mlab.points3d(eval("self.k{}_x".format(elem)),eval("self.k{}_y".format(elem)),eval("self.k{}_z".format(elem)),color=eval("self.color{}".format(elem)),mode='sphere',scale_factor=eval("self.size{}".format(elem)))

        pitch(-3.75)
        yaw(-3.2)

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                      height=400, width=450, show_label=False, resizable=True, has_focus=True, springy=True, padding = 0),
                x = 50
                )

class MayaviWfnQWidget(QtGui.QWidget):
    def __init__(self, suffix, subdir, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = Visualization(suffix,subdir)
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)