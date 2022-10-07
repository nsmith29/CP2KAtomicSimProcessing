import os
os.environ['ETS_TOOLKIT'] = 'qt4'
os.environ['QT_API'] = 'pyside6'
from pyface.qt import QtGui, QtCore
from traits.api import HasTraits, Instance, on_trait_change
from traitsui.api import View, Item
from mayavi.core.ui.api import MayaviScene, MlabSceneModel, \
        SceneEditor
from mayavi.mlab import move, pitch, yaw
import numpy as np
import GraphicAnalysis

class VisualizationGEO(HasTraits, GraphicAnalysis.Atoms3DplotData, GraphicAnalysis.Bonds3DplotData):
    scene = Instance(MlabSceneModel, ())

    def __init__(self, suffix, subdir):
        HasTraits.__init__(self)
        GraphicAnalysis.Atoms3DplotData.__init__(self, suffix, subdir)
        GraphicAnalysis.Bonds3DplotData.__init__(self, suffix, subdir)

    @on_trait_change('scene.activated')
    def update_plot(self):
        for elem in list(self.included_atoms):
            self.scene.mlab.points3d(eval("self.k{}_x".format(elem)),eval("self.k{}_y".format(elem)),eval("self.k{}_z".format(elem)),color=eval("self.color{}".format(elem)),mode='sphere',scale_factor=eval("self.size{}".format(elem)))
        for num in range(0, int(self.BondCounter)):
            self.scene.mlab.plot3d(eval("self.bond{}_x".format(num)),eval("self.bond{}_y".format(num)),eval("self.bond{}_z".format(num)),color=(0,0,0),tube_radius=0.05)

        pitch(-3.75)
        yaw(-3.2)

    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                      height=400, width=450, show_label=False, resizable=True, has_focus=True, springy=True, padding = 0),
                x = 50
                )

class MayaviWidgetBlank(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

class MayaviGEOQWidget(QtGui.QWidget):
    def __init__(self, suffix, subdir, parent=None):
        QtGui.QWidget.__init__(self, parent)
        layout = QtGui.QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        self.visualization = VisualizationGEO(suffix,subdir)
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

class VisualizationWFN(VisualizationGEO, HasTraits, GraphicAnalysis.ReadingConvertingCube):
    scene = Instance(MlabSceneModel, ())
    spin = None
    wfn = None

    def __init__(self, suffix, subdir):
        HasTraits.__init__(self)
        VisualizationGEO.__init__(self, suffix, subdir)
        print(VisualizationWFN.spin, VisualizationWFN.wfn)
        GraphicAnalysis.ReadingConvertingCube.__init__(self, suffix, VisualizationWFN.spin,
                                                       VisualizationWFN.wfn)

    @on_trait_change('scene.activated')
    def update_plot(self):
        for elem in list(self.included_atoms):
            self.scene.mlab.points3d(eval("self.k{}_x".format(elem)),eval("self.k{}_y".format(elem)),eval("self.k{}_z".format(elem)),color=eval("self.color{}".format(elem)),mode='sphere',scale_factor=eval("self.size{}".format(elem)))
        for num in range(0, int(self.BondCounter)):
            self.scene.mlab.plot3d(eval("self.bond{}_x".format(num)),eval("self.bond{}_y".format(num)),eval("self.bond{}_z".format(num)),color=(0,0,0),tube_radius=0.05)


        cp = self.scene.mlab.contour3d(self.data, contours=self.contours, transparent=True,
                                  opacity=0.5, colormap='blue-red')
        polydata = cp.actor.actors[0].mapper.input
        pts = np.array(polydata.points) - 1
        polydata.points = np.dot(pts, self.A / np.array(self.data.shape)[:, np.newaxis])

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

        self.visualization = VisualizationWFN(suffix,subdir)
        self.ui = self.visualization.edit_traits(parent=self,
                                                 kind='subpanel').control
        layout.addWidget(self.ui)
        self.ui.setParent(self)

