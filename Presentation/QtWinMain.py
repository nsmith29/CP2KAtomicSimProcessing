import matplotlib
matplotlib.use('QtAgg')
import PySide6
import Graphics
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *
from PySide6.QtCharts import QChart, QChartView, QLineSeries
from PySide6 import QtDataVisualization
from PySide6.QtDataVisualization import *
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindowGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculation Results GUI")

        self.setFixedSize(QSize(1440, 850))

class MainWindowWfn(QMainWindow):
    def __init__(self, subdir, suffix):
        super().__init__()
        self.setWindowTitle(str("Wfns for {}".format(suffix)))
        self.setFixedSize(QSize(650,550))

        self.setCentralWidget(Graphics.WfnStructurePlotFrame(self, subdir, suffix))