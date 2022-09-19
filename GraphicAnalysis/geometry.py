import numpy as np
import Core
import FromFile
import GraphicAnalysis
import DataProcessing

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

class Atoms3DplotData(FromFile.Kinds, GraphicAnalysis.atom_lookup, DataPoints4Kind):
    def __init__(self, suffix, subdir):
        input = Core.Extension().files4defect(".inp", subdir)
        FromFile.Kinds.__init__(self, input)
        self.num_kind = self.num_kinds + 1
        for elem in list(self.included_atoms):
            GraphicAnalysis.atom_lookup.__init__(self, elem)
            exec(f'self.color{elem} = self.atom_color')
            exec(f'self.size{elem} = self.size_normalised')
            DataPoints4Kind.__init__(self, suffix, elem)

class Bonds3DplotData(DataProcessing.SetupStructure4pymatgen, DataProcessing.NearestNeighbours, DataProcessing.CellBounds):
    def __init__(self, suffix, subdir):
        DataProcessing.SetupStructure4pymatgen.__init__(self, suffix, subdir)
        self.BondCounter = 0
        self.atomsbonded = []

        for i in range(0, int(self.totatom)):
            self.atomsbonded.append(i)
            DataProcessing.NearestNeighbours.__init__(self, self.structure, i)
            for j in range(len(self.nn_dict)):
                bondingindex = self.nn_dict[j]['site_index']
                if bondingindex not in self.atomsbonded:
                    exec(f'self.bond{self.BondCounter}_x = []')
                    exec(f'self.bond{self.BondCounter}_y = []')
                    exec(f'self.bond{self.BondCounter}_z = []')
                    coords = self.nn_dict[j]['site']
                    strcoords = str("{}".format(coords)).replace("[","").replace("]","").split()
                    x = float(strcoords[0])
                    y = float(strcoords[1])
                    z = float(strcoords[2])
                    bondlength = np.sqrt((self.X[i] - x)**2 + (self.Y[i] - y)**2 + (self.Z[i] - z)**2)
                    c = np.sqrt(self.C[0]**2 + self.C[1]**2 + self.C[2]**2)
                    if 0 < z < c:
                        DataProcessing.CellBounds.__init__(self, self.A, self.B, self.C, x, z)
                        if self.lowerXbound < x < self.upperXbound and self.lowerYbound < y < self.upperYbound:
                            if bondlength < c/2:
                                exec(f'self.bond{self.BondCounter}_x.append(self.X[i])')
                                exec(f'self.bond{self.BondCounter}_x.append(self.X[bondingindex])')
                                exec(f'self.bond{self.BondCounter}_y.append(self.Y[i])')
                                exec(f'self.bond{self.BondCounter}_y.append(self.Y[bondingindex])')
                                exec(f'self.bond{self.BondCounter}_z.append(self.Z[i])')
                                exec(f'self.bond{self.BondCounter}_z.append(self.Z[bondingindex])')
                                self.BondCounter += 1



