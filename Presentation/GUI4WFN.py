import sys
import Presentation
import GUIwidgets
import DataProcessing
import matplotlib
matplotlib.use('QtAgg')
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

class MainWindowWfn(QMainWindow, DataProcessing.SetupWfnVars):
    def __init__(self):
        super().__init__()
        print('reached 2nd')
        self.setWindowTitle("Wave-function analysis")
        self.setFixedSize(QSize(650,550))
        self.comboboxMain = QComboBox()
        self.comboboxMain.addItem(' ')
        DataProcessing.SetupWfnVars.__init__(self)
        for suffix in self.suffixs:
            self.comboboxMain.addItem(str("{}".format(suffix)))
        self.comboboxMain.currentTextChanged.connect(self.MainChoice)

        dockWidgetCombo = QDockWidget(" ")
        dockWidgetCombo.setAllowedAreas(Qt.TopDockWidgetArea |
                                        Qt.LeftDockWidgetArea)
        dockWidgetCombo.setWidget(self.comboboxMain)
        self.addDockWidget(Qt.TopDockWidgetArea, dockWidgetCombo, Qt.Vertical)
        self.wfnFrame = GUIwidgets.WfnStructurePlotFrame(self)

        self.setCentralWidget(self.wfnFrame)

    def MainChoice(self):
        selected = self.comboboxMain.currentText()
        if [selected == suffix for suffix in list(self.suffixs)]:
            suffixindex = self.suffixs.index(selected)
            subdir = self.subdirs[suffixindex]
            self.wfnFrame = GUIwidgets.WfnStructurePlotFrame(self)
            self.wfnFrame.AddWfnContainer(selected, subdir)
            self.setCentralWidget(self.wfnFrame)

class WFNGUI:
    def __init__(self):
        print('reached')
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()

        window = Presentation.MainWindowWfn()

        window.show()
        sys.exit(app.exec())