import Core
import FromFile
import DataProcessing
import Presentation
import Graphics
import numpy as np

class SetUpGeometry:
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
        self.subs, self.suffixs = FromFile.OnlyNeutralWanted(subs, suffixs).ReturnPaths()


class DefectDictionary(SetUpGeometry):
    geometryDataStore = dict()
    def __init__(self):
        SetUpGeometry.__init__(self)
        for subdir, suffix in zip(list(self.subs), list(self.suffixs)):
            self.Create(subdir, suffix)

    @classmethod
    def Create(cls, subdir, suffix):
        entry = dict()
        string = str(suffix)
        geometry = []
        X, Y, Z = np.loadtxt(FromFile.LastXYZ(subdir).returnlastxyzname(), skiprows=2, usecols=(1, 2, 3), unpack=True)
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
        DefectDictionary.geometryDataStore[string] = entry

    # def GeometryAnalysisChosen(self, defect_type, atom_index):
    #     DataProcessing.perfectDirectory.Create()
    #     if defect_type == 'substitutional':
    #         DataProcessing.SubstitutionalGeometryDisplacement(atom_index, self.subs, self.suffixs)

class FetchGeometryFromDefectDictionary:
    def __init__(self, suffix):
        self.suffix = suffix
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

class perfectDirectory:
    perfectDataStore = dict()
    def __init__(self):
        self.CreatePerf()

    @classmethod
    def CreatePerf(cls):
        perfsubdir = Core.UserArguments.PerfectSubdir
        entry = dict()
        string = str(perfsubdir)
        geometry = []
        X, Y, Z = np.loadtxt(FromFile.perfLastXYZ(perfsubdir).returnlastxyzname(), skiprows=2, usecols=(1, 2, 3), unpack=True)
        atoms = FromFile.LastXYZ(perfsubdir).Name4Coordinate()
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

class FetchGeometryFromPerfectDictionary:
    def __init__(self):
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

class SubstitutionalGeometryDisplacement(DefectDictionary, perfectDirectory, FetchGeometryFromPerfectDictionary, FetchGeometryFromDefectDictionary):
    SubsGeoDisDataStore = dict()
    def __init__(self, atom_index):
        self.atom_index = int(atom_index)
        DefectDictionary.__init__(self)
        perfectDirectory.__init__(self)
        FetchGeometryFromPerfectDictionary.__init__(self)

        for suffix in list(self.suffixs):
            FetchGeometryFromDefectDictionary.__init__(self,suffix)
            self.defect_site_X = self.X[self.atom_index]
            self.defect_site_Y = self.Y[self.atom_index]
            self.defect_site_Z = self.Z[self.atom_index]
            self.StoringPositionDifferences(suffix, self.DifferenceInPosition()[0],self.DifferenceInPosition()[1],self.DifferenceInPosition()[2])

        print('works')
        print(SubstitutionalGeometryDisplacement.SubsGeoDisDataStore)

    def DifferenceInPosition(self):
        diff_X = self.perfX - self.X
        dist_X= self.defect_site_X - self.X
        diff_Y = self.perfY - self.Y
        dist_Y = self.defect_site_Y - self.Y
        diff_Z = self.perfZ - self.Z
        dist_Z = self.defect_site_Z - self.Z

        tot_displacement = np.sqrt(diff_X**2 + diff_Y**2 + diff_Z**2)
        tot_distance = np.sqrt(dist_X**2 + dist_Y**2 + dist_Z**2)
        tot_distance_sorted = np.sort(tot_distance)
        tot_displacement_sorted = [x for _, x in sorted(zip(tot_distance,tot_displacement))]
        tot_displacement_sorted2 = np.sort(tot_displacement)

        return tot_distance_sorted, tot_displacement_sorted, tot_displacement_sorted2

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