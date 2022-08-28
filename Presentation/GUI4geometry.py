import sys
import Presentation
import GUIwidgets
import DataProcessing

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

class MainWindowGeometry(QMainWindow, DataProcessing.SetUpGeometry):
    def __init__(self):
        super().__init__()
        print('reached 2nd')
        self.setWindowTitle("Geometry analysis")
        self.setFixedSize(QSize(800,550))
        self.comboboxMain = QComboBox()
        self.comboboxMain.addItem(' ')
        DataProcessing.SetUpGeometry.__init__(self)
        for suffix in self.suffixs:
            self.comboboxMain.addItem(str("{}".format(suffix)))
        self.comboboxMain.currentTextChanged.connect(self.MainChoice)

        dockWidgetCombo = QDockWidget(" ")
        dockWidgetCombo.setAllowedAreas(Qt.TopDockWidgetArea |
                                        Qt.LeftDockWidgetArea)
        dockWidgetCombo.setWidget(self.comboboxMain)
        self.addDockWidget(Qt.TopDockWidgetArea, dockWidgetCombo, Qt.Vertical)
        self.Frame = GUIwidgets.StructurePlotFrame(self)

        self.setCentralWidget(self.Frame)

    def MainChoice(self):
        selected = self.comboboxMain.currentText()
        if [selected == suffix for suffix in list(self.suffixs)]:
            suffixindex = self.suffixs.index(selected)
            subdir = self.subdirs[suffixindex]
            self.Frame = GUIwidgets.StructurePlotFrame(self)
            self.Frame.AddContainer(selected, subdir)
            self.Frame.displacements_plot(selected)
            self.setCentralWidget(self.Frame)

class geometryGUI:
    def __init__(self):
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()

        window = Presentation.MainWindowGeometry()

        window.show()
        sys.exit(app.exec())