import sys
import numpy as np
import os
import Core
from PySide6.QtWidgets import QApplication
import ase.io.cube as asecube
from visvis.vvio.wavefront import WavefrontWriter
import FromFile
import DataProcessing
import Presentation
import Graphics


class ControlWfn:
    def __init__(self):
        DataProcessing.SetupWfnVars()

        subdirs = DataProcessing.SetupWfnVars.listofdirs
        suffixs = DataProcessing.SetupWfnVars.listofsufs
        for subdir, suffix in zip(list(subdirs), suffixs):
            app = QApplication(sys.argv)
            window = Presentation.MainWindowWfn(subdir, suffix)
            window.show()
            sys.exit(app.exec())
            # DataProcessing.ReadingConvertingCube(suffix, subdir)
            # break

class SetupWfnVars:
    wfnDataStore = dict()
    listofdirs = []
    listofsufs = []

    def __init__(self):
        self.defectsub = Core.UserArguments.DefectSubdir
        self.wfnsubs = []
        self.wfnsuffixs = []
        wfnsubs = []
        wfnsuffixs = []
        wfncubes, suffixs = Core.Extension().All_defect_subdir("_1-1_l.cube", self.defectsub)
        [wfnsubs.append(x) for x in wfncubes if x not in wfnsubs]
        [wfnsuffixs.append(y) for y in suffixs if y not in wfnsuffixs]
        for subdir, suffix in zip(list(wfnsubs), list(wfnsuffixs)):
            returndir, suf = self.OnlyNeutral(subdir, suffix)
            self.wfnfilesdict(returndir, suf, self.defectsub)
        self.Save(self.wfnsubs, self.wfnsuffixs)


    def OnlyNeutral(self, subdir, suffix):
        if FromFile.ChargeStateIdentification(Core.Extension().files4defect(".inp", subdir)).returnstate() == 0:
            self.wfnsubs.append(subdir)
            self.wfnsuffixs.append(suffix)
            return subdir, suffix

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

        geometry = []
        X, Y, Z = np.loadtxt(FromFile.LastXYZ(subdir).returnlastxyzname(),skiprows=2,  usecols=(1,2,3), unpack=True)
        atoms = FromFile.LastXYZ(subdir).Name4Coordinate()
        for i in range(len(atoms)):
            index = i
            atom = atoms[i]
            x = X[i]
            y = Y[i]
            z = Z[i]
            innerkeys = ["Index", "Name", "Xcoord", "Ycoord", "Zcoord"]
            element = [index, atom, x, y, z]
            sub = dict(zip(innerkeys, element))
            geometry.append(sub)
        entry["Geometry"] = geometry
        SetupWfnVars.wfnDataStore[string] = entry

class ReadingConvertingCube:
    def __init__(self, suffix, subdir):
        self.suffix = suffix
        self.subdir= subdir
        wfn = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["BETA"]['LUMO']
        wfntest = open(str(wfn), 'r')

        wfndir = asecube.read_cube(wfntest, read_data=True, program=None, verbose=False)

        wfnarray = wfndir['data']

        filename = str(self.suffix + '.obj')
        filepath = os.path.join(self.subdir, filename)

        WavefrontWriter.write(filepath, wfnarray, name='testwfn')
