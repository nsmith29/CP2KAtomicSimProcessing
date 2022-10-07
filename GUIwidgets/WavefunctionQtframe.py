import GUIwidgets
import DataProcessing
from PySide6.QtWidgets import *
from pyface.qt import QtGui
from PySide6.QtCore import Qt

class WfnStructurePlotFrame(QtGui.QWidget, DataProcessing.SetupWfnVars):
    selected = [None, None]
    spinstateselected = None
    Buffer = ''
    def __init__(self, parent):
        super().__init__()
        self.options = ['HOMO-1','HOMO','LUMO']
        self.layout = QGridLayout(self)
        for n in range(30):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(33):
            exec(f'self.layout.setRowMinimumHeight({m},33)')

        self.wfn_container = GUIwidgets.MayaviWidgetBlank(self)
        self.yescheckbox = QCheckBox("On")
        self.nocheckbox = QCheckBox("Off")

        self.wfnoptionsframe = QFrame()

        self.alphacheckbox = QCheckBox("Alpha")
        self.betacheckbox = QCheckBox("Beta")

        self.whichwfnList = QComboBox(self.wfnoptionsframe)

        self.neighbourbutton = QPushButton()

        self.checkboxes()
        self.Button4neighours()
        self.wfn_label = QLabel("Wavefunction")
        self.layout.addWidget(self.wfn_label,4,22,2,5)
        self.Tree4WfnSettings()
        self.setLayout(self.layout)

    def AddWfnContainer(self, suffix, subdir):
        self.layout.removeWidget(self.wfnoptionsframe)
        self.wfnoptionsframe.deleteLater()
        del self.wfnoptionsframe
        self.wfnoptionsframe = QFrame()
        self.SaveCurrentDropDownMenuSelection(suffix, subdir)
        self.Tree4WfnSettings()
        self.wfn_container = GUIwidgets.MayaviGEOQWidget(suffix, subdir, self)
        self.layout.addWidget(self.wfn_container, 1, 1, 16, 17)

    @classmethod
    def SaveDropdownBuffer(cls, buffer):
        WfnStructurePlotFrame.Buffer = buffer

    @classmethod
    def SaveCurrentDropDownMenuSelection(cls, suffix, subdir):
        WfnStructurePlotFrame.selected = [suffix, subdir]

    @classmethod
    def SaveCheckedSpinState(cls, state):
        WfnStructurePlotFrame.spinstateselected = state

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
            self.Tree4WfnSettings()
            self.layout.addWidget(self.wfnoptionsframe, 7, 19, 9, 9)

    def nocheckboxchanged(self, s):
        if s == Qt.Checked:
            self.yescheckbox.setChecked(Qt.Unchecked)
            self.layout.removeWidget(self.wfnoptionsframe)
            self.wfnoptionsframe.deleteLater()

    def Tree4WfnSettings(self):
        wfnframelayout = QVBoxLayout(self.wfnoptionsframe)
        wfnframelayout.addWidget(QLabel("Spin State"))
        self.alphacheckbox = QCheckBox("Alpha")
        self.betacheckbox = QCheckBox("Beta")
        spinstatelayout = QHBoxLayout()

        self.whichwfnList = QComboBox(self.wfnoptionsframe)
        self.alphacheckbox.setChecked(False)
        self.alphacheckbox.stateChanged.connect(self.alphacheckboxchanged)
        self.betacheckbox.setChecked(False)
        self.betacheckbox.stateChanged.connect(self.betacheckboxchanged)
        spinstatelayout.addWidget(self.alphacheckbox)
        spinstatelayout.addWidget(self.betacheckbox)
        wfnframelayout.addLayout(spinstatelayout)

        self.whichwfnList.addItem(" ")

        wfnframelayout.addWidget(self.whichwfnList)

        wfnframelayout.addWidget(QLabel("Isovalue:"))

        isovalueslider = QSlider(Qt.Horizontal, self.wfnoptionsframe)
        isovalueslider.setMinimum(0.05)
        isovalueslider.setTickInterval(0.05)
        isovalueslider.setEnabled(True)
        wfnframelayout.addWidget(isovalueslider)

    def Choice(self):
        selected = self.whichwfnList.currentText()
        # print(selected, WfnStructurePlotFrame.spinstateselected, WfnStructurePlotFrame.selected[0], WfnStructurePlotFrame.selected[1])
        if [selected == option for option in list(self.options)]:
            self.layout.removeWidget(self.wfn_container)
            self.wfn_container.deleteLater()
            self.inputsforvisualisation(WfnStructurePlotFrame.spinstateselected, selected)
            self.wfn_container = GUIwidgets.MayaviWfnQWidget(WfnStructurePlotFrame.selected[0], WfnStructurePlotFrame.selected[1], self)
            self.layout.addWidget(self.wfn_container, 1, 1, 16, 17)

    @classmethod
    def inputsforvisualisation(cls, spinstate, wavefunction):
        GUIwidgets.VisualizationWFN.spin = spinstate
        GUIwidgets.VisualizationWFN.wfn = wavefunction

    def alphacheckboxchanged(self, s):
        if s == Qt.Checked:
            self.SaveCheckedSpinState('ALPHA')
            self.betacheckbox.setChecked(Qt.Unchecked)
            self.whichwfnList.clear()
            self.whichwfnList.addItem(" ")
            if WfnStructurePlotFrame.selected[0] != None:
                if 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(WfnStructurePlotFrame.selected[0]))]['ALPHA']:
                    self.whichwfnList.addItem(self.options[0])
                self.whichwfnList.addItem(self.options[1])
                self.whichwfnList.addItem(self.options[2])
                self.whichwfnList.currentTextChanged.connect(self.Choice)


    def betacheckboxchanged(self, s):
        if s == Qt.Checked:
            self.SaveCheckedSpinState('BETA')
            self.alphacheckbox.setChecked(Qt.Unchecked)
            self.whichwfnList.clear()
            self.whichwfnList.addItem(" ")
            if WfnStructurePlotFrame.selected[0] != None:
                if 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(WfnStructurePlotFrame.selected[0]))]['BETA']:
                    self.whichwfnList.addItem(self.options[0])
                self.whichwfnList.addItem(self.options[1])
                self.whichwfnList.addItem(self.options[2])
                self.whichwfnList.currentTextChanged.connect(self.Choice)
