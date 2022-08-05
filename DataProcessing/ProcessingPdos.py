"""Adapted from get-smeared-pdos.py file created by Juan Garcia in 2012"""
from math import pi, sqrt
import numpy as np
import os
import DataProcessing
import FromFile
import Core
import Presentation
from Core import Extension
from ResultsAnalysis import plotpdos


class ControlPdos:
    def __init__(self):
        # perfect structure
        self.perfsubdir = Core.UserArguments.PerfectSubdir
        self.perfinpfile = Extension().perfect_subdir(".inp", self.perfsubdir)
        self.perfpdosfiles = Extension().perfect_subdir(".pdos", self.perfsubdir)

        # Defect structure
        self.defectsub = Core.UserArguments.DefectSubdir
        defectsubdir = []
        defectsuffixs = []
        defpdossubdir, pdossuffixs = Extension().All_defect_subdir(".pdos", self.defectsub)
        [defectsubdir.append(x) for x in defpdossubdir if x not in defectsubdir]
        [defectsuffixs.append(y) for y in pdossuffixs if y not in defectsuffixs]
        self.defsubdir = []
        self.suffixs = []
        self.defpdos = []
        self.definp = []
        for subdir, suffix in zip(list(defectsubdir), list(defectsuffixs)):
            inpfile = Extension().files4defect(".inp", subdir)
            pdosfile = Extension().files4defect(".pdos", subdir)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == 0:
                self.definp.append(inpfile)
                self.defpdos.append(pdosfile)
                self.defsubdir.append(subdir)
                self.suffixs.append(suffix)

    def YesAnalysis(self):
        perfdatfiles = DataProcessing.PdosSmearedDatPlot(self.perfpdosfiles, self.perfsubdir, self.perfinpfile).CreateDatFile()
        for defpdosfile, definpfile, subdir, suffix in zip(list(self.defpdos), list(self.definp), list(self.defsubdir), list(self.suffixs)):
            defdatfiles = DataProcessing.PdosSmearedDatPlot(defpdosfile, subdir, definpfile).CreateDatFile()
            plotpdos(perfdatfiles, self.perfinpfile, defdatfiles, definpfile, subdir, suffix)

    def NoAnalysis(self):
        # perfect structure
        exec(
            f'{self.perfsubdir}_HOMO_alpha, {self.perfsubdir}_LUMO_alpha, {self.perfsubdir}_HOMO_beta, {self.perfsubdir}'
            f'_LUMO_beta = PdosMOprocessing({self.perfpdosfiles}).ReturningMO()')

        exec(f'{self.perfsubdir}_alpha_diff = round(({self.perfsubdir}_LUMO_alpha - {self.perfsubdir}_HOMO_alpha),4)')
        exec(f'{self.perfsubdir}_beta_diff = round(({self.perfsubdir}_LUMO_beta - {self.perfsubdir}_HOMO_beta),4)')
        for s in 'alpha', 'beta':
            exec(f'{self.perfsubdir}_HOMO_{s} = round({self.perfsubdir}_HOMO_{s},4)')
            exec(f'{self.perfsubdir}_LUMO_{s} = round({self.perfsubdir}_LUMO_{s},4)')

        # print(Presentation.csvfile.pdosDataStore)
        Presentation.csvfile.PdosDirectory(self.perfsubdir, eval("{}_HOMO_alpha".format(self.perfsubdir)),
                                           eval("{}_LUMO_alpha".format(self.perfsubdir)), eval("{}_alpha_diff".format(self.perfsubdir)),
                                           eval("{}_HOMO_beta".format(self.perfsubdir)), eval("{}_LUMO_beta".format(self.perfsubdir)),
                                           eval("{}_beta_diff".format(self.perfsubdir)))
        # print(Presentation.csvfile.pdosDataStore)
        for defpdosfile, suffix in zip(list(self.defpdos), list(self.suffixs)):
            exec(
                f'{suffix}_HOMO_alpha, {suffix}_LUMO_alpha, {suffix}_HOMO_beta, {suffix}'
                f'_LUMO_beta = PdosMOprocessing(defpdosfile).ReturningMO()')
            exec(f'{suffix}_alpha_diff = round(({suffix}_LUMO_alpha - {suffix}_HOMO_alpha),4)')
            exec(f'{suffix}_beta_diff = round(({suffix}_LUMO_beta - {suffix}_HOMO_beta),4)')
            for s in 'alpha', 'beta':
                exec(f'{suffix}_HOMO_{s} = round({suffix}_HOMO_{s},4)')
                exec(f'{suffix}_LUMO_{s} = round({suffix}_LUMO_{s},4)')
            Presentation.csvfile.PdosDirectory(suffix, eval("{}_HOMO_alpha".format(suffix)), eval("{}_LUMO_alpha".format(suffix)),
                                               eval("{}_alpha_diff".format(suffix)), eval("{}_HOMO_beta".format(suffix)),
                                               eval("{}_LUMO_beta".format(suffix)), eval("{}_beta_diff".format(suffix)))
            # print(Presentation.csvfile.pdosDataStore)
        Presentation.csvfile.turnTrue('pdos')

class PdosSmearedDatPlot:
    def __init__(self, pdosfiles, subdir, inputfile):
        self.pdosfiles = pdosfiles
        self.subdir = subdir
        self.inputfile = inputfile

    def get_kinds(self):
        self.num_kinds, self.included_atoms = FromFile.Kinds(self.inputfile).searchingfile()
        return self.num_kinds, self.included_atoms

    def CreateDatFile(self):
        global pdos_dat_filename
        self.num_kinds, self.include_atoms = self.get_kinds()
        dat_files = []
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
                Pdos = pdos(filename)
                npts = len(Pdos.e)
                pdos_smeared = Pdos.smearing(npts, 0.1)
                eigenvalues = np.linspace(min(Pdos.e), max(Pdos.e), npts)
                if filename.find("ALPHA") != -1:
                    pdos_dat_filename = str("{}_alpha.dat".format(kind))
                elif filename.find("BETA") != -1:
                    pdos_dat_filename = str("{}_beta.dat".format(kind))
                pdos_dat_file = os.path.join(self.subdir, pdos_dat_filename)

                g = open(pdos_dat_file, 'w')
                for i, j in zip(eigenvalues, pdos_smeared):
                    t = str(i).ljust(15) + '     ' + str(j).ljust(15) + '\n'
                    g.write(t)
                g.close()

                dat_files.append(pdos_dat_file)

        return dat_files


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

    def ReturningMO(self):
        return self.HOMO_alpha, self.LUMO_alpha, self.HOMO_beta, self.LUMO_beta

    def ReturnMONum(self):
        return self.HOMO_MO


class pdos:
    """ Projected electronic density of states from CP2K output files
        Attributes -
        atom {str}:  the name of the atom where the DoS is projected
        iterstep {int}: the iteration step from the CP2K job
        efermi {float}: the energy of the Fermi level [a.u]
        e {float}: (eigenvalue - efermi) in eV
        occupation {int}: 1 for occupied state or 0 for unoccupied
        pdos {nested list of float}:
            projected density of states on each orbital for each eigenvalue
            [[s1, p1, d1,....], [s2, p2, d2,...],...]
            s: pdos in s orbitals
            p: pdos in p orbitals
            d: pdos in d orbitals
        tpdos {list of float}: sum of all the orbitals PDOS
        Methods - smearing(self,npts, width): return the smeared tpdos
    """

    def __init__(self, infilename):
        """Read a CP2K .pdos file and build a pdos instance
        Parameters - infilename {str}: pdos output from CP2K.
        """
        input_file = open(infilename, 'r')

        firstline = input_file.readline().strip().split()
        secondline = input_file.readline().strip().split()

        # Kind of atom
        self.atom = firstline[6]
        # iterationstep
        self.iterstep = int(firstline[12][:-1])  # [:-1] delete ","
        # Energy of the Fermi level
        self.efermi = float(firstline[15])

        # it keeps just the orbital names
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
        """Return the sum of two PDOS objects"""
        sumtpdos = [i + j for i, j in zip(self.tpdos, other.tpdos)]
        return sumtpdos

    def delta(self, emin, emax, npts, energy, width):
        """Return a delta-function centered at energy
        Parameters -
        emin {float}: minimun eigenvalue
        emax {float}: maximun eigenvalue
        npts {int}: Number of points in the smeared pdos
        energy {float}: energy where the gaussian is centered
        width {float}: dispersion parameter
        Return - delta {numpy array}: array of delta function values
        """
        energies = np.linspace(emin, emax, npts)
        x = -((energies - energy) / width) ** 2
        return np.exp(x) / (sqrt(pi) * width)

    def smearing(self, npts, width, ):
        """Return a gaussian smeared DOS"""
        d = np.zeros(npts)
        emin = min(self.e)
        emax = max(self.e)
        for e, pd in zip(self.e, self.tpdos):
            d += pd * self.delta(emin, emax, npts, e, width)
        return d


def sum_tpdos(tpdos1, tpdos2):
    """Return the sum of two PDOS"""
    return [i + j for i, j in zip(tpdos1, tpdos2)]
