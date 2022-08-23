import Core
import FromFile
import DataProcessing
# import Presentation
# import Graphics
import numpy as np

class SetUpGeometry(FromFile.OnlyNeutralWanted):
    def __init__(self):
        self.defectsub = Core.UserArguments.DefectSubdir
        subs = []
        suffixs = []
        if 'wfn' in Core.ProcessingControls.ProcessingWants:
            allsubs, allsuffixs = Core.Extension().All_defect_subdir("_1-1_l.cube", self.defectsub)
        else:
            allsubs, allsuffixs = Core.Extension().All_defect_subdir(".xyz",self.defectsub)
        [subs.append(x) for x in allsubs if x not in subs]
        [suffixs.append(y) for y in allsuffixs if y not in suffixs]
        FromFile.OnlyNeutralWanted.__init__(self, subs, suffixs)


class DefectDictionary(SetUpGeometry, FromFile.Name4Coordinate, FromFile.LastXYZ):
    geometryDataStore = dict()
    def __init__(self):
        SetUpGeometry.__init__(self)
        for subdir, suffix in zip(list(self.subdirs), list(self.suffixs)):
            FromFile.LastXYZ.__init__(self, subdir)
            X, Y, Z = np.loadtxt(self.new_xyz_file, skiprows=2, usecols=(1, 2, 3), unpack=True)
            FromFile.Name4Coordinate.__init__(self,subdir)
            self.Create(suffix, X, Y, Z, self.atoms)

    @classmethod
    def Create(cls, suffix, X, Y, Z, atoms):
        entry = dict()
        string = str(suffix)
        geometry = []
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
        DefectDictionary.geometryDataStore[string] = entry

class FetchGeometryFromDefectDictionary(DefectDictionary):
    def __init__(self, suffix):
        self.suffix = suffix
        DefectDictionary.__init__(self)
        self.atoms = []
        self.X = []
        self.Y = []
        self.Z = []

        self.totatom = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][-1][
                           'Index'] + 1

        for i in range(0, int(self.totatom)):
            atom = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Name']
            self.atoms.append(atom)
            x_ = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Xcoord']
            self.X.append(x_)
            y_ = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Ycoord']
            self.Y.append(y_)
            z_ = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Zcoord']
            self.Z.append(z_)
        self.X = np.asarray(self.X)
        self.Y = np.asarray(self.Y)
        self.Z = np.asarray(self.Z)

class perfectDirectory(FromFile.perfName4Coordinate, FromFile.perfLastXYZ):
    perfectDataStore = dict()
    def __init__(self):
        self.perfsubdir = Core.UserArguments.PerfectSubdir
        FromFile.perfLastXYZ.__init__(self, self.perfsubdir)
        X, Y, Z = np.loadtxt(self.new_xyz_file, skiprows=2, usecols=(1, 2, 3), unpack=True)
        FromFile.perfName4Coordinate.__init__(self, self.perfsubdir)
        self.CreatePerf(self.perfsubdir, X, Y, Z, self.atoms)

    @classmethod
    def CreatePerf(cls, perfsubdir, X, Y, Z, atoms):
        entry = dict()
        string = str(perfsubdir)
        geometry = []
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
        perfectDirectory.perfectDataStore[string] = entry

class FetchGeometryFromPerfectDictionary(perfectDirectory):
    def __init__(self):
        perfectDirectory.__init__(self)
        self.perfatoms = []
        self.perfX = []
        self.perfY = []
        self.perfZ = []

        totatom = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][-1]['Index'] + 1
        for i in range(0, int(totatom)):
            atom = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Name']
            self.perfatoms.append(atom)
            x_ = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Xcoord']
            self.perfX.append(x_)
            y_ = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Ycoord']
            self.perfY.append(y_)
            z_ = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Zcoord']
            self.perfZ.append(z_)
        self.perfX = np.asarray(self.perfX)
        self.perfY = np.asarray(self.perfY)
        self.perfZ = np.asarray(self.perfZ)

class DifferenceInPosition:
    def __init__(self, perfX, X, defectX, perfY, Y, defectY, perfZ, Z, defectZ):
        self.diff_X = perfX - X
        self.dist_X= defectX - X
        self.diff_Y = perfY - Y
        self.dist_Y = defectY - Y
        self.diff_Z = perfZ - Z
        self.dist_Z = defectZ - Z

        self.tot_displacement = np.sqrt(self.diff_X**2 + self.diff_Y**2 + self.diff_Z**2)
        self.tot_distance = np.sqrt(self.dist_X**2 + self.dist_Y**2 + self.dist_Z**2)
        self.tot_distance_sorted = np.sort(self.tot_distance)
        self.tot_displacement_sorted = [x for _, x in sorted(zip(self.tot_distance,self.tot_displacement))]
        self.tot_displacement_sorted2 = np.sort(self.tot_displacement)

class SubstitutionalGeometryDisplacement(FetchGeometryFromPerfectDictionary, FetchGeometryFromDefectDictionary, DifferenceInPosition):
    SubsGeoDisDataStore = dict()
    def __init__(self, atom_index):
        self.atom_index = int(atom_index)
        FetchGeometryFromPerfectDictionary.__init__(self)

        for suffix in list(self.suffixs):
            FetchGeometryFromDefectDictionary.__init__(self,suffix)
            self.defect_site_X = self.X[self.atom_index]
            self.defect_site_Y = self.Y[self.atom_index]
            self.defect_site_Z = self.Z[self.atom_index]
            DifferenceInPosition.__init__(self, self.perfX, self.X, self.defect_site_X, self.perfY, self.Y, self.defect_site_Y, self.perfZ, self.Z, self.defect_site_Z)
            self.StoringPositionDifferences(suffix, self.tot_distance, self.tot_displacement_sorted, self.tot_displacement_sorted2)

    @classmethod
    def StoringPositionDifferences(cls, suffix, tot_distance, tot_displacement1, tot_displacement2):
        entry = dict()
        string = str(suffix)
        entry["sorted distances"] = tot_distance
        entry["displacements sorted by distance"] = tot_displacement1
        entry["sorted displacements"] = tot_displacement2
        SubstitutionalGeometryDisplacement.SubsGeoDisDataStore[string] = entry

class InterstitionalGeometryDisplacement:
    def __init__(self, atom_index):
        e = 11
        print(e)

class VacancyGeometryDisplacement:
    def __init__(self, atom_index):
        e = 17
        print(e)

class SubsVacancyGeometryDisplacement:
    def __init__(self, atom_index):
        e = 8
        print(e)

class InterVacancyGeometryDisplacement:
    def __init__(self, atom_index):
        e = 9
        print(e)