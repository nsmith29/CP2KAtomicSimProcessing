import Core
import FromFile
import DataProcessing
# import Presentation
# import GraphicAnalysis
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
            # FromFile.LastXYZ.__init__(self, subdir)
            FromFile.Name4Coordinate.__init__(self,subdir)
            X, Y, Z = np.loadtxt(self.new_xyz_file, skiprows=2, usecols=(1, 2, 3), unpack=True)
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

class FetchGeometryFromPerfectDictionary(SetUpGeometry, perfectDirectory):
    def __init__(self):
        SetUpGeometry.__init__(self)
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
    def __init__(self, numatoms, perfX, X, defectX, perfY, Y, defectY, perfZ, Z, defectZ):
        self.tot_displacement = []
        self.tot_distance = []
        for i in range(0, int(numatoms)):
            self.diff_X = perfX[i] - X[i]
            self.dist_X= defectX - X[i]
            self.diff_Y = perfY[i] - Y[i]
            self.dist_Y = defectY - Y[i]
            self.diff_Z = perfZ[i] - Z[i]
            self.dist_Z = defectZ - Z[i]

            tot_displacement = np.sqrt(self.diff_X**2 + self.diff_Y**2 + self.diff_Z**2)
            self.tot_displacement.append(tot_displacement)
            tot_distance = np.sqrt(self.dist_X**2 + self.dist_Y**2 + self.dist_Z**2)
            self.tot_distance.append(tot_distance)
        self.tot_distance_sorted = np.sort(self.tot_distance)
        self.tot_displacement_sorted = [x for _, x in sorted(zip(self.tot_distance,self.tot_displacement))]
        self.tot_displacement_sorted2 = np.sort(self.tot_displacement)

class SubstitutionalGeometryDisplacement(FetchGeometryFromPerfectDictionary, FetchGeometryFromDefectDictionary, DifferenceInPosition):
    SubsGeoDisDataStore = dict()
    def __init__(self, atom_index, suf):
        self.atom_index = int(atom_index) - 1
        FetchGeometryFromPerfectDictionary.__init__(self)

        FetchGeometryFromDefectDictionary.__init__(self,suf)
        self.defect_site_X = self.X[self.atom_index]
        self.defect_site_Y = self.Y[self.atom_index]
        self.defect_site_Z = self.Z[self.atom_index]

        self.defect_atom = self.atoms[self.atom_index]

        DifferenceInPosition.__init__(self, self.totatom, self.perfX, self.X, self.defect_site_X, self.perfY, self.Y, self.defect_site_Y, self.perfZ, self.Z, self.defect_site_Z)

class MaxDisplacement(SubstitutionalGeometryDisplacement):
    def __init__(self, atom_index, suf):
        SubstitutionalGeometryDisplacement.__init__(self, atom_index, suf)
        print(suf, self.tot_displacement_sorted2[-1])


class InterstitionalGeometryDisplacement:
    def __init__(self, atom_index):
        e = 11
        print(e)

class VacancyGeometryDisplacement:
    def __init__(self, atom_index):
        e = 17
        print(e)

class SubsVacancyGeometryDisplacement(FetchGeometryFromPerfectDictionary, FetchGeometryFromDefectDictionary):
    def __init__(self, indices, suffix):

        self.subs = int(indices[0]) - 1
        self.vac = int(indices[1]) - 1
        FetchGeometryFromPerfectDictionary.__init__(self)

        self.vacX = self.perfX[self.vac]
        self.vacY = self.perfY[self.vac]
        self.vacZ = self.perfZ[self.vac]
        FetchGeometryFromDefectDictionary.__init__(self, suffix)





class InterVacancyGeometryDisplacement:
    def __init__(self, atom_index):
        e = 9
        print(e)