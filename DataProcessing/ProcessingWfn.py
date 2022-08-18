import sys
import numpy as np
import os
import Core
from PySide6.QtWidgets import QApplication
import ase.io.cube as asecube
import FromFile
import DataProcessing
import Presentation
import Graphics


class ControlWfn:
    def __init__(self):
        DataProcessing.SetupWfnVars()
        DataProcessing.GeometryControl()
        if not QApplication.instance():
            app = QApplication(sys.argv)
        else:
            app = QApplication.instance()
        window = Presentation.MainWindowWfn()
        window.show()
        sys.exit(app.exec())


class SetupWfnVars:
    wfnDataStore = dict()
    listofdirs = []
    listofsufs = []

    def __init__(self):
        self.defectsub = Core.UserArguments.DefectSubdir
        wfnsubs = []
        wfnsuffixs = []
        wfncubes, suffixs = Core.Extension().All_defect_subdir("_1-1_l.cube", self.defectsub)
        [wfnsubs.append(x) for x in wfncubes if x not in wfnsubs]
        [wfnsuffixs.append(y) for y in suffixs if y not in wfnsuffixs]
        self.wfnsubs, self.wfnsuffixs = FromFile.OnlyNeutralWanted(wfnsubs, wfnsuffixs).ReturnPaths()
        for subdir, suffix in zip(list(self.wfnsubs), list(self.wfnsuffixs)):
            self.wfnfilesdict(subdir, suffix, self.defectsub)
        self.Save(self.wfnsubs, self.wfnsuffixs)

    @classmethod
    def Save(cls, subdir, suffix):
        SetupWfnVars.listofdirs = subdir
        SetupWfnVars.listofsufs = suffix

    @classmethod
    def wfnfilesdict(cls, subdir, suffix, defectsub):
        global LUMOfile, HOMOfile
        entry = dict()
        string = str(suffix)
        spins = ['ALPHA', 'BETA']
        spin_num = [1, 2]
        a = dict()
        b = dict()
        spindic = [a, b]
        for s, n, d in zip(list(spins), list(spin_num), list(spindic)):
            HOMO_MO_num = DataProcessing.PdosMOprocessing(Core.Extension().files4defect(str("{}_k{}-1.pdos".format(s,n)), subdir)).ReturnMONum()
            LUMO_MO_num = HOMO_MO_num + 1
            testchar_MO_num = HOMO_MO_num - 1
            LUMO_MO_ = []
            HOMO_MO_ = []
            testchar_MO_ = []
            for wfn in 'HOMO', 'LUMO', 'testchar':
                MO_num = str(eval("{}_MO_num".format(wfn)))
                for i in range(len(MO_num)):
                    exec(f'{wfn}_MO_.append(MO_num[i])')
                filename = str("{}{}{}_{}-1_l.cube".format(eval("{}_MO_[0]".format(wfn)), eval("{}_MO_[1]".format(wfn)), eval("{}_MO_[2]".format(wfn)), n))
                if wfn == "HOMO":
                    HOMOfile = Core.Extension().files4defect(filename, subdir)
                    d["HOMO"] = HOMOfile
                elif wfn == "LUMO":
                    LUMOfile = Core.Extension().files4defect(filename, subdir)
                    d["LUMO"] = LUMOfile
                elif wfn == "testchar":
                    check4HOMO_1 = Core.Extension().All_defect_subdir(filename, defectsub)[0]
                    if check4HOMO_1 != []:
                        for dir_ in list(check4HOMO_1):
                            if dir_ == subdir:
                                HOMO_1file = Core.Extension().files4defect(str("{}{}{}_{}-1_l.cube".format(testchar_MO_[0],testchar_MO_[1],testchar_MO_[2],n)), subdir)
                                d["HOMO-1"] = HOMO_1file
            entry[str("{}".format(s))] = d

class ReadingConvertingCube:
    def __init__(self, suffix, subdir):
        self.suffix = suffix
        self.subdir= subdir
        wfn = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["BETA"]['LUMO']
        wfntest = open(str(wfn), 'r')

        wfndir = asecube.read_cube(wfntest, read_data=True, program=None, verbose=False)

        wfnarray = wfndir['data']
        print(type(wfnarray))

        filename = str(self.suffix + '.obj')
        filepath = os.path.join(self.subdir, filename)

        # pymesh.meshio.form_mesh(wfnarray,)

        # WavefrontWriter.write(filepath, wfnarray, name='testwfn')
