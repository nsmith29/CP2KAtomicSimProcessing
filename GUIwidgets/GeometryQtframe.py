import matplotlib
matplotlib.use('QtAgg')
import GUIwidgets
import Core
import DataProcessing
from PySide6.QtWidgets import *
from pyface.qt import QtGui
from PySide6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class WorkingOutGeometryData2Plot(DataProcessing.SubstitutionalGeometryDisplacement):
    def __init__(self, suffix):
        self.Xdata = None
        self.Ydata = None
        for i in range(len(Core.ProcessingControls.ProcessingWants)):
            if Core.ProcessingControls.ProcessingWants[i] == 'geometry':
                followupAns = Core.ProcessingControls.Followups[i].split(',')
                if followupAns[0] == 'substitutional':
                    DataProcessing.SubstitutionalGeometryDisplacement.__init__(self, followupAns[1], suffix)
                    self.Xdata = self.tot_distance_sorted
                    self.Ydata = self.tot_displacement_sorted

            if Core.ProcessingControls.ProcessingWants[i] == 'test':
                DataProcessing.SubstitutionalGeometryDisplacement.__init__(self, 305, suffix)
                self.Xdata = self.tot_distance_sorted
                self.Ydata = self.tot_displacement_sorted

class TestingGeometry(WorkingOutGeometryData2Plot, DataProcessing.SetUpGeometry):
    def __init__(self):
        DataProcessing.SetUpGeometry.__init__(self)
        WorkingOutGeometryData2Plot.__init__(self, self.suffixs[0])
        print(self.Xdata)
        # print(" ")
        print(self.Ydata)

class DisplacementsPlotting(GUIwidgets.MplCanvas, WorkingOutGeometryData2Plot):
    def __init__(self, suffix, parent=None):
        GUIwidgets.MplCanvas.__init__(self, 4.0, 2.5, 70)
        WorkingOutGeometryData2Plot.__init__(self, suffix)
        self.axes.plot(self.Xdata, self.Ydata, ls='-', color='#76EEC6', label=str("displacement in {}".format(suffix)))
        handles, labels = self.axes.get_legend_handles_labels()
        self.axes.legend(handles, labels)
        self.axes.set(xlabel='Distance from defect atom ($\AA$)', ylabel='Displacement from bulk pos.($\AA$)')

class StructurePlotFrame(QtGui.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QGridLayout(self)
        for n in range(41):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(33):
            exec(f'self.layout.setRowMinimumHeight({m},33)')
        self.container = QWidget()
        self.layout.addWidget(self.container, 1, 1, 16, 17)
        self.displacements_fig = GUIwidgets.MplCanvas(4.0, 2.5, 75)
        ax = self.displacements_fig.axes
        ax.set(xlabel='Distance from defect atom ($\AA$)', ylabel='Displacement from bulk pos.($\AA$)')
        self.layout.addWidget(self.displacements_fig, 1, 19, 16, 19)
        self.setLayout(self.layout)

    def AddContainer(self, suffix, subdir):
        self.layout.removeWidget(self.container)
        self.container.deleteLater()
        del self.container

        self.container = GUIwidgets.MayaviWfnQWidget(suffix, subdir, self)
        self.layout.addWidget(self.container, 1, 1, 16, 17)

    def displacements_plot(self, subdir):
        self.layout.removeWidget(self.displacements_fig)
        self.displacements_fig.deleteLater()
        del self.displacements_fig

        self.displacements_fig = DisplacementsPlotting(subdir, self)
        self.layout.addWidget(self.displacements_fig,1,19,16,19)
