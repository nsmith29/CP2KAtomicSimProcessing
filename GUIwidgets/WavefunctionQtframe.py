import GUIwidgets
from PySide6.QtWidgets import *
from pyface.qt import QtGui
from PySide6.QtCore import Qt
# from PySide6.QtDataVisualization import *


class WfnStructurePlotFrame(QtGui.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.layout = QGridLayout(self)
        for n in range(30):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(33):
            exec(f'self.layout.setRowMinimumHeight({m},33)')

        self.Button4neighours()
        self.wfn_label = QLabel("Wavefunction")
        self.layout.addWidget(self.wfn_label,4,19,2,5)
        self.Checkbox()
        self.Tree4WfnSettings()
        self.setLayout(self.layout)

    def AddWfnContainer(self, suffix, subdir):
        wfn_container = GUIwidgets.MayaviWfnQWidget(suffix, subdir, self)
        self.layout.addWidget(wfn_container, 1, 1, 16, 17)

    def Button4neighours(self):
        self.neighbourbutton = QPushButton()
        self.neighbourbutton.setText("defect nearest neighbours")
        self.layout.addWidget(self.neighbourbutton,2,19,2,9)

    def Checkbox(self):
        self.yescheckbox = QCheckBox()
        self.yescheckbox.setText("On")
        self.yescheckbox.setChecked(False)
        self.layout.addWidget(self.yescheckbox,5,19,2,3)
        self.nocheckbox = QCheckBox()
        self.nocheckbox.setText("off")
        self.nocheckbox.setChecked(True)
        self.layout.addWidget(self.nocheckbox,5,24,2,3)

    def Tree4WfnSettings(self):
        self.wfntree = QTreeWidget()
        self.wfntree.setHeaderHidden(True)

        wfnoptionsframe = QFrame(self.wfntree)
        wfnframelayout = QVBoxLayout(wfnoptionsframe)

        whichwfnList = QComboBox(wfnoptionsframe)
        # if 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["ALPHA"]:
        #     exec(f'whichwfnList{self.suffix}.addItem("HOMO-1")')
        # elif 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["BETA"]:
        #     exec(f'whichwfnList{self.suffix}.addItem("HOMO-1")')
        whichwfnList.addItem("HOMO")
        whichwfnList.addItem("LUMO")
        wfnframelayout.addWidget(whichwfnList)

        wfnframelayout.addWidget(QLabel("Spin State"))

        spinstatelayout= QHBoxLayout()
        alphacheckbox = QCheckBox()
        alphacheckbox.setText("Alpha")
        alphacheckbox.setChecked(False)
        betacheckbox = QCheckBox()
        betacheckbox.setText("Beta")
        betacheckbox.setChecked(True)
        spinstatelayout.addWidget(alphacheckbox)
        spinstatelayout.addWidget(betacheckbox)
        wfnframelayout.addLayout(spinstatelayout)

        wfnframelayout.addWidget(QLabel("Isovalue:"))

        isovalueslider = QSlider(Qt.Horizontal, wfnoptionsframe)
        isovalueslider.setMinimum(0.05)
        isovalueslider.setTickInterval(0.05)
        isovalueslider.setEnabled(True)
        wfnframelayout.addWidget(isovalueslider)

        self.layout.addWidget(self.wfntree,7,19,9,9)

