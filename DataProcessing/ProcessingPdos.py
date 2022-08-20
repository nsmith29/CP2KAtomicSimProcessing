"""Adapted from get-smeared-pdos.py file created by Juan Garcia in 2012"""
from math import pi, sqrt
import numpy as np
import os
# import DataProcessing
import FromFile
import Core
import Presentation
from Core import Extension

class SetUpPdos(FromFile.OnlyNeutralWanted):
    def __init__(self):
        self.perfsubdir = Core.UserArguments.PerfectSubdir
        self.perfinpfile = Extension().perfect_subdir(".inp", self.perfsubdir)
        self.perfpdosfiles = Extension().perfect_subdir(".pdos", self.perfsubdir)

        self.defectsub = Core.UserArguments.DefectSubdir
        defectsubdir = []
        defectsuffixs = []
        defpdossubdir, pdossuffixs = Extension().All_defect_subdir(".pdos", self.defectsub)
        [defectsubdir.append(x) for x in defpdossubdir if x not in defectsubdir]
        [defectsuffixs.append(y) for y in pdossuffixs if y not in defectsuffixs]
        FromFile.OnlyNeutralWanted.__init__(self,defectsubdir, defectsuffixs)
        self.defpdos = []
        self.definp = []
        for subdir, suffix in zip(list(self.subdirs), list(self.suffixs)):
            self.defpdos.append(Extension().files4defect(".pdos", subdir))
            self.definp.append(Extension().files4defect(".inp", subdir))

class ControlPdos(SetUpPdos):
    def __init__(self):
        SetUpPdos.__init__(self)

class Delta:
    def __init__(self, emin, emax, npts, energy, width):
        energies = np.linspace(emin, emax, npts)
        x = -((energies - energy) / width) ** 2
        self.delta = np.exp(x) / (sqrt(pi) * width)

class smearing(Delta):
    def __init__(self, npts, width, ):
        self.d = np.zeros(npts)
        emin = min(self.e)
        emax = max(self.e)
        for e, pd in zip(self.e, self.tpdos):
            Delta.__init__(self,emin, emax, npts, e, width)
            self.d += pd * self.delta


class pdos:
    def __init__(self, infilename):
        input_file = open(infilename, 'r')

        firstline = input_file.readline().strip().split()
        secondline = input_file.readline().strip().split()

        self.atom = firstline[6]
        self.iterstep = int(firstline[12][:-1])
        self.efermi = float(firstline[15])
        secondline[0:5] = []
        self.orbitals = secondline

        lines = input_file.readlines()

        eigenvalue = []
        self.occupation = []
        data = []
        self.pdos = []
        for index, line in enumerate(lines):
            data.append(line.split())
            data[index].pop(0)
            eigenvalue.append(float(data[index].pop(0)))
            self.occupation.append(int(float(data[index].pop(0))))
            self.pdos.append([float(i) for i in data[index]])

        self.e = [(x - self.efermi) * 27.211384523 for x in eigenvalue]

        self.tpdos = []
        for i in self.pdos:
            self.tpdos.append(sum(i))

    def __add__(self, other):
        sumtpdos = [i + j for i, j in zip(self.tpdos, other.tpdos)]
        return sumtpdos

class PdosSmearedDatPlot(FromFile.Kinds, pdos, smearing):
    def __init__(self, pdosfiles, subdir, inputfile):
        global pdos_dat_filename
        self.pdosfiles = pdosfiles
        self.subdir = subdir
        self.inputfile = inputfile
        FromFile.Kinds.__init__(self,self.inputfile)

        self.dat_files = []
        for k in range(0, int(self.num_kinds)):
            kr = k + 1
            Kstr = str('k{}-1'.format(kr))
            kind = self.included_atoms[k]
            file4kind = []
            for PDOS in list(self.pdosfiles):
                if PDOS.find(Kstr) != -1:
                    filename = PDOS
                    file4kind.append(filename)
            for filename in file4kind:
                pdos.__init__(self,filename)
                npts = len(self.e)
                smearing.__init__(self,npts, 0.1)
                eigenvalues = np.linspace(min(self.e), max(self.e), npts)
                if filename.find("ALPHA") != -1:
                    pdos_dat_filename = str("{}_alpha.dat".format(kind))
                elif filename.find("BETA") != -1:
                    pdos_dat_filename = str("{}_beta.dat".format(kind))
                pdos_dat_file = os.path.join(self.subdir, pdos_dat_filename)

                g = open(pdos_dat_file, 'w')
                for i, j in zip(eigenvalues, self.d):
                    t = str(i).ljust(15) + '     ' + str(j).ljust(15) + '\n'
                    g.write(t)
                g.close()

                self.dat_files.append(pdos_dat_file)

        # return dat_files

class YesAnalysis(SetUpPdos,PdosSmearedDatPlot):
    def __init__(self):
        SetUpPdos.__init__(self)
        PdosSmearedDatPlot.__init__(self, self.perfpdosfiles, self.perfsubdir, self.perfinpfile)
        self.perfdatfiles = self.dat_files
        for defpdosfile, definpfile, subdir, suffix in zip(list(self.defpdos), list(self.definp), list(self.subdirs), list(self.suffixs)):
            PdosSmearedDatPlot.__init__(self, defpdosfile, subdir, definpfile)
            self.defdatfiles = self.dat_files

class PdosMOprocessing:
    def __init__(self, pdosfiles):
        if type(pdosfiles) == list:
            self.pdosfiles = pdosfiles
            for s in 'alpha', 'beta':
                if s == 'alpha':
                    for PDOS in list(self.pdosfiles):
                        if PDOS.find("ALPHA_k1-1") != -1:
                            pdos = PDOS
                    exec(f'{s}_MO, {s}_Eigenvalue, {s}_Occupation = np.loadtxt(pdos, usecols=(0,1,2), unpack=True)')

                elif s == 'beta':
                    for PDOS in list(self.pdosfiles):
                        if PDOS.find("BETA_k1-1") != -1:
                            pdos = PDOS
                exec(f'{s}_MO, {s}_Eigenvalue, {s}_Occupation = np.loadtxt(pdos, usecols=(0,1,2), unpack=True)')

                exec(f'{s}_Eigenvalue = {s}_Eigenvalue * 27.211')
                exec(f'indices_{s}_occ = []')
                exec(f'indices_{s}_unocc = []')
                Occupation = eval("{}_Occupation".format(s))
                for j in range(len(Occupation)):
                    if Occupation[j] == 1.00000:
                        exec(f'indices_{s}_occ.append(j)')
                for i in range(len(Occupation)):
                    if Occupation[i] == 0.00000:
                        exec(f'indices_{s}_unocc.append(i)')
                exec(f'occupied_{s} = {s}_Eigenvalue[indices_{s}_occ]')
                exec(f'HOMO_{s} = occupied_{s}[-1]')
                exec(f'unoccupied_{s} = {s}_Eigenvalue[indices_{s}_unocc]')
                exec(f'LUMO_{s} = unoccupied_{s}[0]')
                if s == 'alpha':
                    self.HOMO_alpha = eval("HOMO_{}".format(s))
                    self.LUMO_alpha = eval("LUMO_{}".format(s))
                elif s == 'beta':
                    self.HOMO_beta = eval("HOMO_{}".format(s))
                    self.LUMO_beta = eval("LUMO_{}".format(s))
        else:
            pdos = pdosfiles
            MO, Eigenvalue, Occupation = np.loadtxt(pdos, usecols=(0,1,2), unpack=True)
            indices_occ = []
            for j in range(len(Occupation)):
                if Occupation[j] == 1.00000:
                    indices_occ.append(j)
            occupied_MOs = MO[indices_occ]
            self.HOMO_MO = occupied_MOs[-1]

    # def ReturningMO(self):
    #     return self.HOMO_alpha, self.LUMO_alpha, self.HOMO_beta, self.LUMO_beta
    #
    # def ReturnMONum(self):
    #     return self.HOMO_MO

class NoAnalysisPerfect(SetUpPdos, PdosMOprocessing):
    def __init__(self):
        SetUpPdos.__init__(self)
        PdosMOprocessing.__init__(self,self.perfpdosfiles)
        self.perfHOMO_alpha = self.HOMO_alpha
        self.perfLUMO_alpha = self.LUMO_alpha
        self.perfHOMO_beta = self.HOMO_beta
        self.perfLUMO_beta = self.LUMO_beta

        self.perfalpha_diff = round((self.perfLUMO_alpha - self.perfHOMO_alpha),4)
        self.perfbeta_diff = round((self.perfLUMO_beta - self.perfHOMO_beta),4)
        for s in 'alpha', 'beta':
            exec(f'self.perfHOMO_{s} = round(self.perfHOMO_{s},4)')
            exec(f'self.perfLUMO_{s} = round(self.perfLUMO_{s},4)')


class NoAnalysisDefects(SetUpPdos, PdosMOprocessing):# <<<<---------------
    def __init__(self,): #self.defpdos
        SetUpPdos.__init__(self)
        PdosMOprocessing.__init__(self, )
        for defpdosfile, suffix in zip(list(self.defpdos), list(self.suffixs)):
            exec(
                f'{suffix}_HOMO_alpha, {suffix}_LUMO_alpha, {suffix}_HOMO_beta, {suffix}'
                f'_LUMO_beta = PdosMOprocessing(defpdosfile).ReturningMO()')
            exec(f'{suffix}_alpha_diff = round(({suffix}_LUMO_alpha - {suffix}_HOMO_alpha),4)')
            exec(f'{suffix}_beta_diff = round(({suffix}_LUMO_beta - {suffix}_HOMO_beta),4)')
            for s in 'alpha', 'beta':
                exec(f'{suffix}_HOMO_{s} = round({suffix}_HOMO_{s},4)')
                exec(f'{suffix}_LUMO_{s} = round({suffix}_LUMO_{s},4)')
            # Presentation.csvfile.PdosDirectory(suffix, eval("{}_HOMO_alpha".format(suffix)), eval("{}_LUMO_alpha".format(suffix)),
            #                                    eval("{}_alpha_diff".format(suffix)), eval("{}_HOMO_beta".format(suffix)),
            #                                    eval("{}_LUMO_beta".format(suffix)), eval("{}_beta_diff".format(suffix)))
            # print(Presentation.csvfile.pdosDataStore)
        # Presentation.csvfile.turnTrue('pdos')

def sum_tpdos(tpdos1, tpdos2):
    return [i + j for i, j in zip(tpdos1, tpdos2)]
