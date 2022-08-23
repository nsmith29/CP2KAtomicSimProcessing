import sys
import numpy as np
import os
import Core
from PySide6.QtWidgets import QApplication
import FromFile
import DataProcessing
# from Presentation import MainWindowWfn
# import Graphics


class ControlWfn:
    def __init__(self):
        DataProcessing.SetupWfnVars()


class SetupWfnVars(FromFile.OnlyNeutralWanted, DataProcessing.PdosMOprocessing):
    wfnDataStore = dict()
    def __init__(self):
        self.defectsub = Core.UserArguments.DefectSubdir
        wfnsubs = []
        wfnsuffixs = []
        wfncubes, suffixs = Core.Extension().All_defect_subdir("_1-1_l.cube", self.defectsub)
        [wfnsubs.append(x) for x in wfncubes if x not in wfnsubs]
        [wfnsuffixs.append(y) for y in suffixs if y not in wfnsuffixs]
        FromFile.OnlyNeutralWanted.__init__(self, wfnsubs, wfnsuffixs)

        for subdir, suffix in zip(list(self.subdirs), list(self.suffixs)):
            spins = ['ALPHA', 'BETA']
            spin_num = [1, 2]
            for s, n in zip(list(spins), list(spin_num)):
                pdos_file = Core.Extension().files4defect(str("{}_k{}-1.pdos".format(s, n)), subdir)
                DataProcessing.PdosMOprocessing.__init__(self, pdos_file)
                self.wfnfilesdict(subdir, suffix, self.defectsub, s, n, self.HOMO_MO)

    @classmethod
    def wfnfilesdict(cls, subdir, suffix, defectsub, s, n, HOMO_MO_num):
        global LUMOfile, HOMOfile
        entry = dict()
        string = str(suffix)
        a = dict()
        b = dict()
        spindic = [a, b]
        for d in list(spindic):
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

# class ReadingConvertingCube:
#     def __init__(self, suffix, subdir):
#         self.suffix = suffix
#         self.subdir= subdir
#         wfn = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["BETA"]['LUMO']
#         wfntest = open(str(wfn), 'r')
#
#         wfndir = asecube.read_cube(wfntest, read_data=True, program=None, verbose=False)
#
#         wfnarray = wfndir['data']
#         print(type(wfnarray))
#
#         filename = str(self.suffix + '.obj')
#         filepath = os.path.join(self.subdir, filename)
