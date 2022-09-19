import warnings
import numpy as np
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core.structure import Structure
import FromFile
import DataProcessing
import Core

class SetupStructure4pymatgen(DataProcessing.FetchGeometryFromPerfectDictionary, DataProcessing.FetchGeometryFromDefectDictionary, FromFile.LatticeVectors, FromFile.ChargeStateIdentification):
    def __init__(self, suffix, subdir):
        self.sequence = []
        if suffix == 'perf':
            DataProcessing.FetchGeometryFromPerfectDictionary.__init__(self)
        else:
            DataProcessing.FetchGeometryFromDefectDictionary.__init__(self, suffix)
        for x, y, z in zip(list(self.X), list(self.Y), list(self.Z)):
            self.sequence.append([x, y, z])
        input = Core.Extension().files4defect(".inp", subdir)
        FromFile.LatticeVectors.__init__(self, input)
        FromFile.ChargeStateIdentification.__init__(self, input)

        warnings.filterwarnings('ignore', '.*CrystalNN.*', )
        warnings.filterwarnings('ignore', '.*No oxidation.*', )

        self.structure = Structure([self.A, self.B, self.C], self.atoms, self.sequence, self.state, to_unit_cell=True,
                              coords_are_cartesian=True)

class NearestNeighbours:
    def __init__(self, structure, i):
        self.defind = i - 1
        self.nn_dict = CrystalNN(distance_cutoffs=(0.5, 1.5)).get_nn_info(structure, i)

    def returnlist(self):
        indices = []
        NN = []
        for j in range(len(self.nn_dict)):
            bondingindex = int(self.nn_dict[j]['site_index']) + 1
            NN.append(bondingindex)
        NN = np.sort(NN)
        for n in list(NN):
            if n < self.defind:
                indices.append(n)
            elif n > self.defind and self.defind not in indices:
                indices.append(self.defind)
                indices.append(n)
            else:
                indices.append(n)
        return indices