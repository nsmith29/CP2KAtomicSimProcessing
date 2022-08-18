import numpy as np
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core.structure import Structure
import Core
import FromFile
import Graphics
import DataProcessing

class Atoms3DplotData():
    def __init__(self, suffix, kind):
        self.suffix = suffix
        self.kind = kind
        self.x = []
        self.y = []
        self.z = []

        self.totatom, self.atoms, self.X, self.Y, self.Z = DataProcessing.FetchGeometryFromDictionary(
            self.suffix).Return()
        self.DataPoints4Kind()

    def DataPoints4Kind(self):
        for Atom, index in zip(list(self.atoms), range(0, int(self.totatom))):
            if Atom == self.kind:
                self.x.append(self.X[index])
                self.y.append(self.Y[index])
                self.z.append(self.Z[index])

        return self.x, self.y, self.z

class Bonds3DplotData():
    BondsAlreadyMadeStore = dict()
    def __init__(self, subdir, suffix):
        self.subdir = subdir
        self.suffix = suffix
        self.structure = None

        self.totatoms, self.atoms, self.X, self.Y, self.Z = DataProcessing.FetchGeometryFromDictionary(self.suffix).Return()

        for g in range(0, int(self.totatoms)):
            self.addAllAtoms(g)

        self.GeometryStructure()

        # for i in range(0, int(self.totatoms[0])):
        #     nn_dict = CrystalNN().get_nn_info(self.structure,i)
        #     for n in range(len(nn_dict)):
        #         possbond = str("{}".format(nn_dict[i]['site']))
        #         if possbond.find("-") != 1:
        #
        #             nn_dict[i]['site_index']
    @classmethod
    def addBondEntry(cls, atomindex, bondedindex):
        G = str("{}".format(atomindex))
        Bonds3DplotData.BondsAlreadyMadeStore[G] = bondedindex

    @classmethod
    def addAllAtoms(cls, g):
        G = str("{}".format(g))
        Bonds3DplotData.BondsAlreadyMadeStore[G] = dict()

    def GeometryStructure(self):
        A, B, C = FromFile.LatticeVectors(Core.Extension.files4defect(".inp",self.subdir)).search()
        sequence = []
        for x, y, z in zip(list(self.X), list(self.Y),list(self.Z)):
            sequence.append([x,y,z])

        charge = FromFile.ChargeStateIdentification(Core.Extension.files4defect(".inp",self.subdir)).returnstate()

        self.structure = Structure([A, B, C],self.atoms,sequence,charge, to_unit_cell=True, coords_are_cartesian=True)