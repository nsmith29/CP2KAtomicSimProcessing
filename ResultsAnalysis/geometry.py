import numpy as np
import warnings
from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core.structure import Structure
import Core
import FromFile
import Graphics
import DataProcessing
import ResultsAnalysis

class DataPoints4Kind(DataProcessing.FetchGeometryFromDefectDictionary):
    def __init__(self, suffix, elem):
        DataProcessing.FetchGeometryFromDefectDictionary.__init__(self, suffix)
        exec(f'self.k{elem}_x = []')
        exec(f'self.k{elem}_y = []')
        exec(f'self.k{elem}_z = []')
        for Atom, index in zip(list(self.atoms), range(0, int(self.totatom))):
            if Atom == elem:
                exec(f'self.k{elem}_x.append(self.X[index])')
                exec(f'self.k{elem}_y.append(self.Y[index])')
                exec(f'self.k{elem}_z.append(self.Z[index])')

class Atoms3DplotData(FromFile.Kinds, Graphics.atom_lookup, DataPoints4Kind):
    def __init__(self, suffix, subdir):
        input = Core.Extension().files4defect(".inp", subdir)
        FromFile.Kinds.__init__(self, input)
        self.num_kind = self.num_kinds + 1
        for elem in list(self.included_atoms):
            Graphics.atom_lookup.__init__(self, elem)
            exec(f'self.color{elem} = self.atom_color')
            exec(f'self.size{elem} = self.size_normalised')
            DataPoints4Kind.__init__(self, suffix, elem)

class Bonds3DplotData(DataProcessing.FetchGeometryFromDefectDictionary, FromFile.LatticeVectors, FromFile.ChargeStateIdentification, ResultsAnalysis.CellBounds):
    BondsAlreadyMadeStore = dict()
    def __init__(self, suffix, subdir):
        self.sequence = []
        self.BondCounter = 0
        self.atomsbonded = []
        self.structure = None
        DataProcessing.FetchGeometryFromDefectDictionary.__init__(self, suffix)
        for x, y, z in zip(list(self.X), list(self.Y), list(self.Z)):
            self.sequence.append([x, y, z])
        input = Core.Extension().files4defect(".inp", subdir)
        FromFile.LatticeVectors.__init__(self, input)
        FromFile.ChargeStateIdentification.__init__(self, input)

        warnings.filterwarnings('ignore', '.*CrystalNN.*', )
        warnings.filterwarnings('ignore', '.*No oxidation.*', )

        structure = Structure([self.A, self.B, self.C], self.atoms, self.sequence, self.state, to_unit_cell=True, coords_are_cartesian=True)

        for i in range(0, int(self.totatom)):
            self.atomsbonded.append(i)
            atom = i
            nn_dict = CrystalNN(distance_cutoffs=(0.5,1.5)).get_nn_info(structure, i)
            for j in range(len(nn_dict)):
                bondingindex = nn_dict[j]['site_index']
                if bondingindex not in self.atomsbonded:
                    exec(f'self.bond{self.BondCounter}_x = []')
                    exec(f'self.bond{self.BondCounter}_y = []')
                    exec(f'self.bond{self.BondCounter}_z = []')
                    test = nn_dict[j]['site']
                    strtest = str("{}".format(test)).replace("[","").replace("]","").split()
                    x = float(strtest[0])
                    y = float(strtest[1])
                    z = float(strtest[2])
                    if 0 < z < self.C[2]:
                        ResultsAnalysis.CellBounds.__init__(self, self.A, self.B, self.C, x, z)
                        if self.lowerXbound < x < self.upperXbound and self.lowerYbound < y < self.upperYbound:
                            exec(f'self.bond{self.BondCounter}_x.append(self.X[atom])')
                            exec(f'self.bond{self.BondCounter}_x.append(self.X[bondingindex])')
                            exec(f'self.bond{self.BondCounter}_y.append(self.Y[atom])')
                            exec(f'self.bond{self.BondCounter}_y.append(self.Y[bondingindex])')
                            exec(f'self.bond{self.BondCounter}_z.append(self.Z[atom])')
                            exec(f'self.bond{self.BondCounter}_z.append(self.Z[bondingindex])')
                            self.BondCounter += 1


