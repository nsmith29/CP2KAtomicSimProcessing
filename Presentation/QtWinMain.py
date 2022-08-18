import matplotlib
matplotlib.use('QtAgg')
import Graphics
import DataProcessing
import PySide6
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *
import ResultsAnalysis
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
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wave-function analysis")
        self.setFixedSize(QSize(650,550))
        self.comboboxMain = QComboBox()
        self.comboboxMain.addItem(' ')
        for suffix in list(DataProcessing.SetupWfnVars.listofsufs):
            self.comboboxMain.addItem(str("{}".format(suffix)))
        self.comboboxMain.currentTextChanged.connect(self.MainChoice)

        dockWidgetCombo = QDockWidget(" ")
        dockWidgetCombo.setAllowedAreas(Qt.TopDockWidgetArea |
                                        Qt.LeftDockWidgetArea)
        dockWidgetCombo.setWidget(self.comboboxMain)
        self.addDockWidget(Qt.TopDockWidgetArea, dockWidgetCombo, Qt.Vertical)
        self.wfnFrame = Graphics.WfnStructurePlotFrame(self)

        self.setCentralWidget(self.wfnFrame)

    def MainChoice(self):
        selected = self.comboboxMain.currentText()
        # for suffix, subdir in zip(list(DataProcessing.SetupWfnVars.listofsufs), list(DataProcessing.SetupWfnVars.listofdirs)):
        if [selected == suffix for suffix in list(DataProcessing.SetupWfnVars.listofsufs)]:
            self.wfnFrame = Graphics.WfnStructurePlotFrame(self)
            self.wfnFrame.AddWfnContainer(selected)
            self.setCentralWidget(self.wfnFrame)
