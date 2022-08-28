import GUIwidgets
import DataProcessing
from PySide6.QtWidgets import *
from pyface.qt import QtGui
from PySide6.QtCore import Qt

class WfnStructurePlotFrame(QtGui.QWidget, DataProcessing.SetupWfnVars):
    selected = None
    def __init__(self, parent):
        super().__init__()
        self.layout = QGridLayout(self)
        for n in range(30):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(33):
            exec(f'self.layout.setRowMinimumHeight({m},33)')
        self.yescheckbox = QCheckBox("On")
        self.nocheckbox = QCheckBox("Off")

        self.wfnoptionsframe = QFrame()

        self.neighbourbutton = QPushButton()

        self.checkboxes()
        self.Button4neighours()
        self.wfn_label = QLabel("Wavefunction")
        self.layout.addWidget(self.wfn_label,4,22,2,5)
        self.Tree4WfnSettings(WfnStructurePlotFrame.selected)
        self.setLayout(self.layout)

    def AddWfnContainer(self, suffix, subdir):
        self.layout.removeWidget(self.wfnoptionsframe)
        self.wfnoptionsframe.deleteLater()
        del self.wfnoptionsframe
        self.wfnoptionsframe = QFrame()
        self.SaveCurrentDropDownMenuSelection(suffix)
        self.Tree4WfnSettings(suffix)
        wfn_container = GUIwidgets.MayaviWfnQWidget(suffix, subdir, self)
        self.layout.addWidget(wfn_container, 1, 1, 16, 17)

    @classmethod
    def SaveCurrentDropDownMenuSelection(cls, suffix):
        WfnStructurePlotFrame.selected = suffix

    def Button4neighours(self):
        self.neighbourbutton.setText("defect nearest neighbours")
        self.layout.addWidget(self.neighbourbutton,2,19,2,9)

    def checkboxes(self):
        checkframe1 = QFrame()
        checklayout1 = QGridLayout(checkframe1)
        for n in range(4):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(4):
            exec(f'self.layout.setRowMinimumHeight({m},33)')
        self.yescheckbox.setCheckState(Qt.Unchecked)
        self.yescheckbox.stateChanged.connect(self.yescheckboxchanged)
        checklayout1.addWidget(self.yescheckbox, 1, 2, 1, 3)
        self.layout.addWidget(checkframe1, 5, 20, 2, 5)

        checkframe2 = QFrame()
        checklayout2 = QGridLayout(checkframe2)
        for n in range(4):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(4):
            exec(f'self.layout.setRowMinimumHeight({m},33)')
        self.nocheckbox.setChecked(Qt.Checked)
        self.nocheckbox.stateChanged.connect(self.nocheckboxchanged)
        checklayout2.addWidget(self.nocheckbox, 1, 2, 1, 3)
        self.layout.addWidget(checkframe2, 5, 24, 2, 4)

    def yescheckboxchanged(self, s):
        if s == Qt.Checked:
            self.nocheckbox.setChecked(Qt.Unchecked)
            self.wfnoptionsframe = QFrame()
            self.Tree4WfnSettings(WfnStructurePlotFrame.selected)
            self.layout.addWidget(self.wfnoptionsframe, 7, 19, 9, 9)

    def nocheckboxchanged(self, s):
        if s == Qt.Checked:
            self.yescheckbox.setChecked(Qt.Unchecked)
            self.layout.removeWidget(self.wfnoptionsframe)
            self.wfnoptionsframe.deleteLater()

    def Tree4WfnSettings(self, suffix):
        wfnframelayout = QVBoxLayout(self.wfnoptionsframe)
        wfnframelayout.addWidget(QLabel("Spin State"))

        spinstatelayout = QHBoxLayout()
        alphacheckbox = QCheckBox("Alpha")
        alphacheckbox.setChecked(False)
        betacheckbox = QCheckBox("Beta")
        betacheckbox.setChecked(True)
        spinstatelayout.addWidget(alphacheckbox)
        spinstatelayout.addWidget(betacheckbox)
        wfnframelayout.addLayout(spinstatelayout)

        whichwfnList = QComboBox(self.wfnoptionsframe)
        if suffix != None:
            if 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(suffix))]['ALPHA']:
                whichwfnList.addItem("HOMO-1")
            elif 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(suffix))]['BETA']:
                whichwfnList.addItem("HOMO-1")
        whichwfnList.addItem("HOMO")
        whichwfnList.addItem("LUMO")
        wfnframelayout.addWidget(whichwfnList)

        wfnframelayout.addWidget(QLabel("Isovalue:"))

        isovalueslider = QSlider(Qt.Horizontal, self.wfnoptionsframe)
        isovalueslider.setMinimum(0.05)
        isovalueslider.setTickInterval(0.05)
        isovalueslider.setEnabled(True)
        wfnframelayout.addWidget(isovalueslider)



