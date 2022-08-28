import sys
import Presentation
import GUIwidgets
import DataProcessing
import matplotlib
matplotlib.use('QtAgg')
import PySide6
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import *

class MainWindowWfn(QMainWindow, DataProcessing.SetupWfnVars):
    def __init__(self):
        super().__init__()
        DataProcessing.SetupWfnVars.__init__(self)
        self.setWindowTitle("Wave-function analysis")
        self.setFixedSize(QSize(650,550))
        self.comboboxMain = QComboBox()
        self.comboboxMain.addItem(' ')
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
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()

        window = Presentation.MainWindowWfn()

        window.show()
        sys.exit(app.exec())