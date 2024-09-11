#!/usr/bin/env python3

from pymatgen.analysis.local_env import CrystalNN
from pymatgen.core.structure import Structure
import Core
import FromFile
import DataProcessing
# import Presentation
# import GraphicAnalysis
import numpy as np


class NearestNeighbours:
    """
        All bonds between nearest neighbours.

        Creates two dictionaries, one specifying all bonds between nearest neighbours and the other specifying the
        indices of each nearest neighbour atom to an atom within a system. Within both dictionaries, each nearest
        neighbour bond/pair in the system is only mentioned once corresponding to the atom with the lower index.

        Class definitions:
            Blank(boolean)                         : To determine if the dictionaries of a specific system need to be
                                                     reset to blank or not
            NN_dictionary(dictionary)              : Dictionary of the indices of each nearest neighbour of each atom.
            Bonds(dictionary)                      : Dictionary of bonds between nearest neighbours

        Inputs:
            system(str)                            : Name of defect being analysed

            structure(pymatgen periodic structure) :

            i(int)                                 : Index of atom finding near neighbours for

        Attributes:
            system(str)                            : Name of defect being analysed

            defind(int)                            : Index of atom finding near neighbours for

            nn_dict(pymatgen list of dictionaries) : Site, image and weights of near-neighbor site contributes to the
                                                     coordination number

        Outputs:
            NN_dictionary(dict)                     : Filled dictionary of the indices of each nearest neighbour of
                                                      each atom.
                                                      {'system':
                                                            {'a_i':
                                                                {'nn':
                                                                    {'0': nn_a1, '1': nn_a2, '2':nn_a3, '3':nn_a4}
                                                                }, ...
                                                            }, ...
                                                      }

            Bonds(dict)                             : Filled dictionary of bonds between nearest neighbours.
                                                      {'system':
                                                            {
                                                               ['i-nn_a', ...]
                                                            }, ...
                                                      }

    """

    Blank = True
    NN_dictionary = {"perfect": dict(), "defect": dict()}
    Bonds = {"perfect": dict(), "defect": dict()}

    def __init__(self, system, structure, i):
        self.system = system
        if NearestNeighbours.Blank is True:
            self.CreateBlankNNDict(self.system)
            self.CreateBlankBondsDict(self.system)

        self.defind = i
        self.nn_dict = CrystalNN(distance_cutoffs=(0.5, 1.5)).get_nn_info(structure, i)

        appending_entry, bonds = self.Workings(self.system, self.defind, self.nn_dict)
        self.FillNNDict(self.system, appending_entry)
        self.FillBondsDict(self.system, bonds)

    @classmethod
    def CreateBlankNNDict(cls, system):
        NearestNeighbours.NN_dictionary[system[0]][system[1]][system[2]][system[3]] = []

    @classmethod
    def CreateBlankBondsDict(cls, system):
        NearestNeighbours.Bonds[system[0]][system[1]][system[2]][system[3]] = []
        NearestNeighbours.Blank = False

    def Workings(self, system, i, nn_dict):
        appending_entry = dict()
        entry = dict()
        string = str("a_{}".format(i))
        neighbours = []
        bonds = []
        k = -1
        for j in range(len(nn_dict)):

            nn_a = nn_dict[j]['site_index']
            if str("{}-{}".format(nn_a, i)) not in NearestNeighbours.Bonds[system[0]][system[1]][system[2]][system[3]]:
                k += 1
                innerkeys = str("{}".format(k))
                element = str("{}".format(nn_a))
                sub = dict()
                sub[innerkeys] = element
                neighbours.append(sub)
                bonds.append(str("{}-{}".format(i, nn_a)))
        entry["nn"] = neighbours
        appending_entry[string] = entry

        return appending_entry, bonds

    @classmethod
    def FillNNDict(cls, system, appending_entry):
        NearestNeighbours.NN_dictionary[system[0]][system[1]][system[2]][system[3]].append(appending_entry)

    @classmethod
    def FillBondsDict(cls, system, bonds):
        for b in bonds:
            NearestNeighbours.Bonds[system[0]][system[1]][system[2]][system[3]].append(b)

    def returnlist(self):
        print(NearestNeighbours.NN_dictionary)
        print(NearestNeighbours.Bonds)


class Reset:
    """
        Reset the NearestNeighbours.Bonds & NearestNeighbours.NN_dictionary dictionaries for a particular system.

        Inputs:
            system(str): name of defect being analysed
    """

    def __init__(self, system):
        if system in NearestNeighbours.Bonds.keys():
            NearestNeighbours.Bonds[system[0]][system[1]][system[2]][system[3]] = []
            NearestNeighbours.NN_dictionary[system[0]][system[1]][system[2]][system[3]] = []
        else:
            NearestNeighbours.Blank = True

class Defining_Defect:
    """

    """

    def __init__(self, calckey, perfxyz, defxyz):
        switch = {'substitution': self.finding_substitutional_defects, 'vacancy': self.finding_vacancy_defects,
                  'interstitial': self.finding_interstitial_defects}

        self.name = calckey
        self.bulk, self.defect = open(perfxyz, 'r'), open(defxyz, 'r')
        self.bulk_lines, self.defect_lines = self.bulk.readlines(), self.defect.readlines()
        Type = self.type_definition()

        self.indices = switch.get(Type)()


    def type_definition(self):
        bulk1st, defect1st = self.bulk_lines.strip(), self.defect_lines.strip()
        if bulk1st == defect1st:
            Type = 'substitution'
        elif int(bulk1st) > int(defect1st):
            Type = 'vacancy'
        elif int(bulk1st) < int(defect1st):
            Type = 'interstitial'

        return Type

    def additional(self, dif_atoms):
        additional = []
        for atom in dif_atoms:
            for bond in NearestNeighbours.Bonds[self.name[0]][self.name[1]][self.name[2]][self.name[3]]:
                atoms = bond.replace('-', ' ').split()
                if atom == atoms[0] or atom == atoms[1]:
                    length1 = len(additional)
                    additional.append([atoms[i] for i in range(len(atoms)) if
                                       atoms[i] != atom and atoms[i] not in additional and atom[i] not in dif_atoms])
                    if length1 != len(additional) and len(additional[-1]) == 1:
                        additional.insert(-1, [additional[-1][0]][0])
                    additional.pop(-1)

        return additional

    def finding_substitutional_defects(self):
        print('finding substitutions')
        dif_atoms = []
        index = -2
        for i1, i2 in zip(range(len(self.bulk_lines)), range(len(self.defect_lines))):
            index += 1
            if '=' not in self.bulk_lines[i1]:
                a1, a2 = self.bulk_lines[i1].strip().split(), self.defect_lines[i2].strip().split()
                if a1[0] != a2[0] or round(float(a1[1]), 6) != round(float(a2[1]), 6) or round(float(a1[2]),
                                                                                               6) != round(float(a2[2]),
                                                                                                           6) or round(
                        float(a1[3]), 6) != round(float(a2[3]), 6):
                    dif_atoms.append(str(index))

        additional = self.additional(dif_atoms)
        # additional = []
        # for atom in dif_atoms:
        #     for bond in NearestNeighbours.Bonds[self.name[0]][self.name[1]][self.name[2]][self.name[3]]:
        #         atoms = bond.replace('-', ' ').split()
        #         if atom == atoms[0] or atom == atoms[1]:
        #             length1 = len(additional)
        #             additional.append([atoms[i] for i in range(len(atoms)) if
        #                                atoms[i] != atom and atoms[i] not in additional and atom[i] not in dif_atoms])
        #             if length1 != len(additional) and len(additional[-1]) == 1:
        #                 additional.insert(-1, [additional[-1][0]][0])
        #             additional.pop(-1)

        dif_atoms.extend(additional)

        return dif_atoms

    def finding_vacancy_defects(self):
        print('finding vacancy')
        dif_atoms = []
        diff = 0
        index = -2
        for i1, i2 in zip(range(len(self.bulk_lines)), range(len(self.defect_lines))):
            if diff:
                i1 = i2 - diff
                continue
            index += 1
            if '=' not in self.bulk_lines[i1]:
                a1, a2 = self.bulk_lines[i1].strip().split(), self.defect_lines[i2].strip().split()
                if a1[0] != a2[0] or round(float(a1[1]), 6) != round(float(a2[1]), 6) or round(float(a1[2]),
                                                                                               6) != round(float(a2[2]),
                                                                                                           6) or round(
                        float(a1[3]), 6) != round(float(a2[3]), 6):
                    dif_atoms.append(str(index))
                    diff = diff + 1 if diff else 1

        additional = self.additional(dif_atoms)
        # additional = []
        # for atom in dif_atoms:
        #     for bond in NearestNeighbours.Bonds[self.name[0]][self.name[1]][self.name[2]][self.name[3]]:
        #         atoms = bond.replace('-', ' ').split()
        #         if atom == atoms[0] or atom == atoms[1]:
        #             length1 = len(additional)
        #             additional.append([atoms[i] for i in range(len(atoms)) if
        #                                atoms[i] != atom and atoms[i] not in additional and atom[i] not in dif_atoms])
        #             if length1 != len(additional) and len(additional[-1]) == 1:
        #                 additional.insert(-1, [additional[-1][0]][0])
        #             additional.pop(-1)

        return additional

    def finding_interstitial_defects(self):
        print('finding interstitual')
        dif_atoms = []
        diff = 0
        index = -2
        for i1, i2 in zip(range(len(self.bulk_lines)), range(len(self.defect_lines))):
            if diff:
                i1 = i1 - diff
                continue
            index += 1
            if '=' not in self.bulk_lines[i1]:
                a1, a2 = self.bulk_lines[i1].strip().split(), self.defect_lines[i2].strip().split()
                if a1[0] != a2[0] or round(float(a1[1]), 6) != round(float(a2[1]), 6) or round(float(a1[2]),
                                                                                               6) != round(float(a2[2]),
                                                                                                           6) or round(
                        float(a1[3]), 6) != round(float(a2[3]), 6):
                    dif_atoms.append(str(index))
                    diff = diff + 1 if diff else 1

        additional = self.additional(dif_atoms)
        # additional = []
        # for atom in dif_atoms:
        #     for bond in NearestNeighbours.Bonds[self.name[0]][self.name[1]][self.name[2]][self.name[3]]:
        #         atoms = bond.replace('-', ' ').split()
        #         if atom == atoms[0] or atom == atoms[1]:
        #             length1 = len(additional)
        #             additional.append([atoms[i] for i in range(len(atoms)) if
        #                                atoms[i] != atom and atoms[i] not in additional and atom[i] not in dif_atoms])
        #             if length1 != len(additional) and len(additional[-1]) == 1:
        #                 additional.insert(-1, [additional[-1][0]][0])
        #             additional.pop(-1)
        dif_atoms.extend(additional)

        return dif_atoms

    def Retrn_indxs(self):
        return self.indices


# class SetUpGeometry(FromFile.OnlyNeutralWanted):
#     def __init__(self):
#         self.defectsub = Core.UserArguments.DefectSubdir
#         subs = []
#         suffixs = []
#         if 'wfn' in Core.ProcessingControls.ProcessingWants:
#             allsubs, allsuffixs = Core.Extension().All_defect_subdir("_1-1_l.cube", self.defectsub)
#         else:
#             allsubs, allsuffixs = Core.Extension().All_defect_subdir(".xyz",self.defectsub)
#         [subs.append(x) for x in allsubs if x not in subs]
#         [suffixs.append(y) for y in allsuffixs if y not in suffixs]
#         FromFile.OnlyNeutralWanted.__init__(self, subs, suffixs)
#
# class DefectDictionary(SetUpGeometry, FromFile.Name4Coordinate, FromFile.LastXYZ):
#     geometryDataStore = dict()
#     def __init__(self):
#         SetUpGeometry.__init__(self)
#         for subdir, suffix in zip(list(self.subdirs), list(self.suffixs)):
#             # FromFile.LastXYZ.__init__(self, subdir)
#             FromFile.Name4Coordinate.__init__(self,subdir)
#             X, Y, Z = np.loadtxt(self.new_xyz_file, skiprows=2, usecols=(1, 2, 3), unpack=True)
#             self.Create(suffix, X, Y, Z, self.atoms)
#
#     @classmethod
#     def Create(cls, suffix, X, Y, Z, atoms):
#         entry = dict()
#         string = str(suffix)
#         geometry = []
#         for i in range(len(atoms)):
#             index = i
#             atom = atoms[i]
#             x = X[i]
#             y = Y[i]
#             z = Z[i]
#             innerkeys = ["Index", "Name", "Xcoord", "Ycoord", "Zcoord"]
#             element = [index, atom, x, y, z]
#             sub = dict(zip(innerkeys, element))
#             geometry.append(sub)
#         entry["Geometry"] = geometry
#         DefectDictionary.geometryDataStore[string] = entry
#
# class FetchGeometryFromDefectDictionary(DefectDictionary):
#     def __init__(self, suffix):
#         self.suffix = suffix
#         DefectDictionary.__init__(self)
#         self.atoms = []
#         self.X = []
#         self.Y = []
#         self.Z = []
#
#         self.totatom = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][-1][
#                            'Index'] + 1
#
#         for i in range(0, int(self.totatom)):
#             atom = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Name']
#             self.atoms.append(atom)
#             x_ = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Xcoord']
#             self.X.append(x_)
#             y_ = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Ycoord']
#             self.Y.append(y_)
#             z_ = DataProcessing.DefectDictionary.geometryDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Zcoord']
#             self.Z.append(z_)
#         self.X = np.asarray(self.X)
#         self.Y = np.asarray(self.Y)
#         self.Z = np.asarray(self.Z)
#
# class perfectDirectory(FromFile.perfName4Coordinate, FromFile.perfLastXYZ):
#     perfectDataStore = dict()
#     def __init__(self):
#         self.perfsubdir = Core.UserArguments.PerfectSubdir
#         FromFile.perfLastXYZ.__init__(self, self.perfsubdir)
#         X, Y, Z = np.loadtxt(self.new_xyz_file, skiprows=2, usecols=(1, 2, 3), unpack=True)
#         FromFile.perfName4Coordinate.__init__(self, self.perfsubdir)
#         self.CreatePerf(self.perfsubdir, X, Y, Z, self.atoms)
#
#     @classmethod
#     def CreatePerf(cls, perfsubdir, X, Y, Z, atoms):
#         entry = dict()
#         string = str(perfsubdir)
#         geometry = []
#         for i in range(len(atoms)):
#             index = i
#             atom = atoms[i]
#             x = X[i]
#             y = Y[i]
#             z = Z[i]
#             innerkeys = ["Index", "Name", "Xcoord", "Ycoord", "Zcoord"]
#             element = [index, atom, x, y, z]
#             sub = dict(zip(innerkeys, element))
#             geometry.append(sub)
#         entry["Geometry"] = geometry
#         perfectDirectory.perfectDataStore[string] = entry
#
# class FetchGeometryFromPerfectDictionary(SetUpGeometry, perfectDirectory):
#     def __init__(self):
#         SetUpGeometry.__init__(self)
#         perfectDirectory.__init__(self)
#         self.perfatoms = []
#         self.perfX = []
#         self.perfY = []
#         self.perfZ = []
#
#         totatom = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][-1]['Index'] + 1
#         for i in range(0, int(totatom)):
#             atom = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Name']
#             self.perfatoms.append(atom)
#             x_ = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Xcoord']
#             self.perfX.append(x_)
#             y_ = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Ycoord']
#             self.perfY.append(y_)
#             z_ = DataProcessing.perfectDirectory.perfectDataStore[str("{}".format(Core.UserArguments.PerfectSubdir))]["Geometry"][i]['Zcoord']
#             self.perfZ.append(z_)
#         self.perfX = np.asarray(self.perfX)
#         self.perfY = np.asarray(self.perfY)
#         self.perfZ = np.asarray(self.perfZ)
#
# class DifferenceInPosition:
#     def __init__(self, numatoms, perfX, X, defectX, perfY, Y, defectY, perfZ, Z, defectZ):
#         self.tot_displacement = []
#         self.tot_distance = []
#         for i in range(0, int(numatoms)):
#             self.diff_X = perfX[i] - X[i]
#             self.dist_X= defectX - X[i]
#             self.diff_Y = perfY[i] - Y[i]
#             self.dist_Y = defectY - Y[i]
#             self.diff_Z = perfZ[i] - Z[i]
#             self.dist_Z = defectZ - Z[i]
#
#             tot_displacement = np.sqrt(self.diff_X**2 + self.diff_Y**2 + self.diff_Z**2)
#             self.tot_displacement.append(tot_displacement)
#             tot_distance = np.sqrt(self.dist_X**2 + self.dist_Y**2 + self.dist_Z**2)
#             self.tot_distance.append(tot_distance)
#         self.tot_distance_sorted = np.sort(self.tot_distance)
#         self.tot_displacement_sorted = [x for _, x in sorted(zip(self.tot_distance,self.tot_displacement))]
#         self.tot_displacement_sorted2 = np.sort(self.tot_displacement)
#
# class SubstitutionalGeometryDisplacement(FetchGeometryFromPerfectDictionary, FetchGeometryFromDefectDictionary, DifferenceInPosition):
#     SubsGeoDisDataStore = dict()
#     def __init__(self, atom_index, suf):
#         self.atom_index = int(atom_index) - 1
#         FetchGeometryFromPerfectDictionary.__init__(self)
#
#         FetchGeometryFromDefectDictionary.__init__(self,suf)
#         self.defect_site_X = self.X[self.atom_index]
#         self.defect_site_Y = self.Y[self.atom_index]
#         self.defect_site_Z = self.Z[self.atom_index]
#
#         self.defect_atom = self.atoms[self.atom_index]
#
#         DifferenceInPosition.__init__(self, self.totatom, self.perfX, self.X, self.defect_site_X, self.perfY, self.Y, self.defect_site_Y, self.perfZ, self.Z, self.defect_site_Z)
#
# class MaxDisplacement(SubstitutionalGeometryDisplacement):
#     def __init__(self, atom_index, suf):
#         SubstitutionalGeometryDisplacement.__init__(self, atom_index, suf)
#         print(suf, self.tot_displacement_sorted2[-1])
#
# class InterstitionalGeometryDisplacement:
#     def __init__(self, atom_index):
#         e = 11
#         print(e)
#
# class VacancyGeometryDisplacement:
#     def __init__(self, atom_index):
#         e = 17
#         print(e)
#
# class SubsVacancyGeometryDisplacement(FetchGeometryFromPerfectDictionary, FetchGeometryFromDefectDictionary):
#     def __init__(self, indices, suffix):
#
#         self.subs = int(indices[0]) - 1
#         self.vac = int(indices[1]) - 1
#         FetchGeometryFromPerfectDictionary.__init__(self)
#
#         self.vacX = self.perfX[self.vac]
#         self.vacY = self.perfY[self.vac]
#         self.vacZ = self.perfZ[self.vac]
#         FetchGeometryFromDefectDictionary.__init__(self, suffix)
#
# class InterVacancyGeometryDisplacement:
#     def __init__(self, atom_index):
#         e = 9
#         print(e)