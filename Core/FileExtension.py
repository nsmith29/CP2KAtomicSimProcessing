#!/usr/bin/env python3

import os
import Core
import sys
import subprocess
import time
import threading as th
import queue
from Core.Messages import ErrorMessages, bcolors
import FromFile
# import json


class Directories_Search:
    """
        Searching for individual defect subdirectories holding CP2K output files.

        Current working directory already included in os.path for perf, def, and chem pot directories.
        Need to find all subdirectories holding CP2K output files for defect calculations.
        Need to account for paths that go:
                                    DefectDir/charge_state/particular_defect/CP2K_output-files
                                    DefectDir/particular_defect/charge_state/..../CP2K_output_files

        Class definitions:
            Address_book(dict)           : Empty dictionary to be populated with os.path strs for needed perfect
                                           structure CP2K output files for results processing under "perfect" and
                                           os.path strs for each defect subdirectory and the needed defect CP2K output
                                           files they contain for results processing under "defect".
            Dir_Calc_Keys(dict)          : Empty dictionary to be populated with lists of nested dictionary keys
                                           specific to each specific nested dictionary entry within the Address_book
                                           dictionary.
            executables_address(os.path) : File path for the 'Executables' directory within the CP2KAtomicSimProcessor
                                           package. Important saved for execution of unix executable files needed for
                                           results processing method completion.
            Files4Results(dict)          : Dictionary of file extensions of files needed for completion of each result
                                           process method.
                                           The specific parent directories (perfect/defect/chem_pot) which these files
                                           need to be found in are given as keys to item lists of file extensions in the
                                           sub-dictionaries of either "cp2k_outputs" or "created_in_process".
                                           Why each file type is needed is given as comment next to their dictionary
                                           entry. If there is a final output file to be created for the specific result
                                           process method. e.g. a png image, the extension to be used for that file is
                                           also given.
    """

    Address_book = {"perfect": dict(), "defect": dict()}

    Dir_Calc_Keys = {"perfect": [], "defect": []}

    executables_address = None

    Files4Results ={"band structure":
                        {"cp2k_outputs":
                             {"defect":[".log"                               # To determine the version of CP2K
                                                                             # calculation was run with.

                                        ,".bs"]                              # File writen by CP2K containing band
                                                                             # structure information.
                             },
                         "intermediary":
                            {"defect":[".bs.set-1.csv"]                      # File of dataclasses created which can be
                                                                             # read to plot band structure.
                             },
                         "final_output":
                            {".bs.png"}},
                    "charges and spins":                                     # WARNING: continuation if files for bader
                                                                             # charge analysis aren't present.

                        {"only":                                             # If user selects "only" OPTION, additional
                                                                             # files needed.
                             {"cp2k_outputs":
                                  {"perfect":["-L.xyz"]                      # To compare final geometry of perfect with
                                                                             # initial geometry of defect.

                                   ,"defect":[".inp"                         # To extract project name and name of
                                                                             # initial starting geometry file of
                                                                             # calculation.
                                                                             # ERROR if .inp not found in directory.

                                              ,"''.xyz"]                     # Initial xyz file of defect calculation.
                                   }},
                         "bader":                                            # Bader charge analysis not intrinsic to
                                                                             # CP2K calculations, separate process to
                                                                             # standard charges and spins taken.
                            {"cp2k_outputs":
                                  {"perfect":["-ELECTRON_DENSITY-1_0.cube"]  # File writen by CP2K which is used
                                                                             # for gaining bader charges.

                                   ,"defect":["-ELECTRON_DENSITY-1_0.cube"]  # File writen by CP2K which is used
                                                                             # for gaining bader charges.
                                  },
                             "intermediary":
                                {"perfect":["ACF.dat"]                       # Bader analysis atomic coordinate file -
                                                                             # charges & locations of atoms.

                                            # ,"AVF.dat"                       # Bader analysis bader coordinate file.

                                            # ,"BCF.dat"]                      # Bader analysis atomic volume file.

                                 ,"defect":["ACF.dat"]                       # Bader analysis atomic coordinate file -
                                                                             # charges & locations of atoms.

                                            # ,"AVF.dat"                       # Bader analysis bader coordinate file.

                                            # ,"BCF.dat"]                      # Bader analysis atomic volume file.
                                 }},
                         "standard":                                         # Mulliken and Hirshfeld charge analysis
                                                                             # intrinsic to CP2K calculations.
                            {"cp2k_outputs":
                                {"perfect":[".log"]                          # Mulliken and Hirshfeld data printed in
                                                                             # log file.

                                 ,"defect":[".log"]                          # Mulliken and Hirshfeld data printed in
                                                                             # log file.
                                 }},
                         "final_output":
                             {"charges.txt"                                  # File to be created to hold dataframe of
                                                                             # charges & spins generated when user wants
                                                                             # to display results via GUI.
                              }},
                    "charge transition levels":                              # USER INPUT QUESTION: which charge
                                                                             # corrections? Material Dielectric matrix?
                        {"cp2k_outputs":
                             {"perfect":[".log"]                             # Atomic kinds, tot nums, total energies.

                              ,"defect":[".log"]                             # Atomic kinds, tot nums, charge state,
                                                                             # total energies.

                              ,"chem_pot":[".log"]                           # Total energy of chem_pot.
                                                                             # USER INPUT QUESTION: which found material
                                                                             # <list of material> should be used for
                                                                             # chemical potential of atomic kind <atomic
                                                                             # kind>.
                                   },
                         "final_output":
                             {".clt.png"}},
                    "geometry":
                        {"cp2k_outputs":
                             {"perfect":["-L.xyz"                            # Check if present in defect folder, check
                                                                             # if "-1.xyz" is present.

                                         ,".log"]                            # Lattice parameters.

                              ,"defect":["-1.xyz"                            # If not present, {??}WARNING error for
                                                                             # particular defect to be displayed at end
                                                                             # of processing and display{??}.

                                         ,".log"                             # Lattice parameters.

                                         ,"-L.xyz"]                          # Check if present in defect folder, check
                                                                             # if "-1.xyz" is present.
                              },
                         "intermediary":
                             {"perfect": ["-1.xyz"]

                              , "defect": ["-1.xyz"]
                              },
                         "final_output":
                             {".distVdisp.png"                               #

                              ,"BondsAngles.txt"                             # File to be created to hold dataframe of
                                                                             # bond lengths & angles generated when user
                                                                             # wants to display results via GUI.
                              }},
                    "IPR":"",
                    "PDOS":"",
                    "WFN":"",
                    "work function":""}

    def __init__(self,f):
        self._f = f

    @staticmethod
    def start_setup():
        """
            Setup up os.walk() directory transversing for perfect directory to find log file.
        """
        layer, w = 1, os.walk(Core.UArg.PerD)
        # traversing directory tree of defect parent directory in top-down approach
        for (path, dir, filenames) in w:
            Directories_Search._logs(path, filenames, "perfect")

    @staticmethod
    def finding_(q, lock):
        """
            Setup searching perfect and defect parent directories with os.walk() for log files.

            Going through the layers of files within the defect parent directory and passing the path, dir, and
            filenames found at each layer by os.walk() on to sub function _log for every subdirectory or when certain
            conditions are met if restrictions [only or except used in command line arguments] are given by user.

        """

        # first start to search for log file within perfect directory.
        Directories_Search.start_setup()

        layer, w= 1, os.walk(Core.UArg.DefD)
        # traversing directory tree of defect parent directory in top-down approach
        for (path, dir, filenames) in w:
            # enacting search in all except subdirs named
            if Core.UArg.Expt is True and not path.endswith(tuple(Core.UArg.SubD)):
                Directories_Search.found(path, dir, filenames)

            # enacting search in only subdirs named.
            elif Core.UArg.Only is True and path.endswith(tuple(Core.UArg.SubD)):
                Directories_Search.change_key(path)
                Directories_Search.found(path, dir, filenames)

            # enacting search in all subdirs
            elif Core.UArg.Expt is False and Core.UArg.Only is False:
                Directories_Search._logs(path, filenames, "defect")
            layer+= 1

        if Core.UArg.Only is True:
            # Testing the existence of all subdirectories named by user in command line arguments
            try:
                for key, value in Core.UArg.FdSD.items():
                    # if item value is False then subdirectory with item key name doesn't exist.
                    if value is not True:
                        raise FileNotFoundError
            except FileNotFoundError:
                # ERROR given if none of the subdirectories in Core.UArg.SubD are found
                if True not in Core.UArg.FdSD.values():
                    # send q an item to trigger program to stop & end.
                    q.put("sys.exit(1)")
                    # trigger error informing user that none of named directories user only wants to process exist.
                    ErrorMessages.FileExtension_FileNotFoundError1(key, lock)
                    sys.exit()

                # WARNING given if only one or two subdirectories in Core.UArg.SubD aren't found.
                else:
                    # send q an item to trigger start of execution of Start.Questions2Ask() in MAIN.py
                    q.put("pass")
                    # trigger error informing user some named directories user wants only to be processes don't exist.
                    ErrorMessages.FileExtension_FileNotFoundError2(key, lock)
                    sys.exit()
            else:
                q.put("pass")

        else:
            # trigger population of results holding dictionary.
            Directories_Search.PopulateResultsHolder()

    @staticmethod
    def found(path, dir, filenames):
        """
            Further searching directory tree when conditions of given commandline arguments 'only' and 'except' met.

            When user either wants to process data from only [Core.UArg.Only is True] or from all subdirectories except
            [Core.UArg.Expt is True] certain subdirectories [named in Core.UArg.SubD] and path found with os.walk()
            satisfies corresponding conditions in relation to the names of these certain files, the last subdirectory
            in the directory tree when conditions become satisfied may not be the final subdirectory in the directory
            tree. If the current last subdirectory of the path contains more subdirectories, then each of these
            subdirectories need to be searched by setting up a new os.walk() command.

            Inputs:
                path(os.path)          : os.path of current subdirectory being searched by os.walk() when condition
                                         related to processing data from only or from all subdirectories except is met.

                dir(list of str)       : list containing any subdirectories found within current subdirectory.

                filenames(list of str) : list containing any files found within current subdirectory.
        """

        # if dir is not an empty list.
        if dir:
            layer,w = 1,os.walk(path)
            # traversing directory tree of path in top-down approach
            for (path1, dir1, files1) in w:
                Directories_Search._logs(path1, files1, "defect")
                layer+= 1
        else:
            Directories_Search._logs(path, filenames, "defect")

    @staticmethod
    def _logs(path, filenames, dict_heading):
        """
            Searching filenames within the final subdirectory of the directory tree for .log file.

            Originally part of the finding_ function but was separated into a sub function to avoid code repetition.

            Inputs:
                path(os.path)          : os.path of current subdirectory being searched by os.walk().

                filenames(list of str) : list containing any files found within current subdirectory.

                dict_heading(str)      : item key of outermost dictionary with the Directories_Search.Address_book
                                         dictionary
        """

        for file in filenames:
            if file.endswith(".log") and not path.endswith(".ipynb_checkpoints"):
                # Get project name, run type and charge state from .log file.
                chrg_stt, name, rn_typ  = FromFile.FromLog(os.path.join(path, file), ["original"]).Return()

                # start sub-thread for populating Directories_Search.Dir_Calc_Keys with extracted variables
                t1_ = th.Thread(target=Directories_Search.add_to_Dir_Calc_Keys, args=(dict_heading, name[0],
                                                                                      rn_typ[0], chrg_stt[0],
                                                                                      Directories_Search.Dir_Calc_Keys))
                # start sub-thread for populating Directories_Search.Address_book with extracted variables and os.paths
                t2_ = th.Thread(target=Directories_Search.add_keys_nested_dict, args=([dict_heading, name[0],
                                                                                       rn_typ[0], chrg_stt[0]],
                                                                                      ["path", ".log"],
                                                                                      [path, os.path.join(path, file)],
                                                                                      Directories_Search.Address_book))
                [x.start() for x in [t1_, t2_]]
                [x.join() for x in [t1_, t2_]]

                break

    @staticmethod
    def PopulateResultsHolder():
        """
            Populating results dictionary, Core.ProcessCntrls.ProcessResults, with calc dirs & result processing methods

            Separated from Directories_Search._finding to avoid code repetition.
        """
        for dict_ in "perfect", "defect":
            for name, run, chrg in Directories_Search.Dir_Calc_Keys[dict_]:
                # start sub-thread for every found dictionary for populating Core.ProcessCntrls.ProcessResults
                t_ = th.Thread(target=Directories_Search.add_keys_nested_dict, args=([dict_, name, run, chrg],
                                                                                     Core.ProcessCntrls.ProcessWants,
                                                                                     Core.ProcessCntrls.setup,
                                                                                     Core.ProcessCntrls.ProcessResults))
                t_.start()
                t_.join()

    @classmethod
    def change_key(cls, path):
        """
            Update Core.UArg.FdSD dictionary to reflect subdirectory named by user has been found.

            When os.walk() finds a subdirectory with a name that matches one of the subdirectory name strings within
            Core.UArg.SubD, change the item value for the item key of the matching subdirectory name in Core.UArg.FdSD
            to True. Having an item value of True means that the subdirectory exists.

            Inputs:
                path(os.path)          : os.path of current subdirectory being searched by os.walk() when condition
                                         related to processing data from only is met.
        """

        for sub in Core.UArg.SubD:
            if path.endswith(sub):
                if sub in Core.UArg.FdSD:
                    Core.UArg.FdSD[sub]= True

    @classmethod
    def add_keys_nested_dict(cls, keys, subkeys, paths, d):
        """
            Adding nested dictionary data to pre-existing dictionary entries, instead of creating new entry of same key.

            This class method function adds nested dictionary data to pre-existing dictionary entries instead of
            creating completely new entries with repeated item keys.

            __ORIGINALLY CREATED FOR USE WHEN d = Directories_Search.Address_book:__
            A particular defect geometry/placement/impurity inclusion may have been calculated in multiple different
            charge states and under multiple different calculation run types. There will be multiple sets of results &
            cp2k_output files for each of these charge states and run types of the same defect. To keep track of all
            sets of results and output files for a defect, the project name must be saved as the outermost dictionary
            key with all subsequent information (run type, charge state, directory path, path of particular files)
            belonging to calculation runs of the same project name being nested in the dictionary of this project name
            outer key.

            Inputs:
                keys(list of maj key names)    : Keys which narrow down the particular calculation being specified. Maj
                                                 keys should be specified in a particular order - i.e. project name, run
                                                 type, charge state. Other keys can follow if needing to nest variable
                                                 data coming from a particular file.

                subkeys(list of min key names) : Keys of new data to be added as a new nested or within the innermost
                                                 nested dictionary.

                paths(list of os.paths/vars)   : Values for the subkeys.

                d(dict)                        : The dictionary name.
        """

        for key in keys:
            if key not in d:
                d[key]= {}
            d = d[key]
        try:
            for sub, path in zip(subkeys,paths):
                d.setdefault(sub, path)
        except TypeError:
            print(keys, d)

    @classmethod
    def add_to_Dir_Calc_Keys(cls, dict_, name, run, chrg, d = None):
        """
            Adding list of strs of dict nested keys - name, run, and chrg - for specific calc to separate dict.

            Created to make accessing nested item values within the Core.Directories_Search.Address_book and
            Core.ProcessingControls.Processing_Results dictionaries easier with iteration through the list items in [by
            default] dictionary Directories_Search.Dir_Calc_Keys [or whatever dictionary is given as optional input d]
            of nested list containing dict nested keys within Core.Directories_Search.Address_book and
            Core.ProcessingControls.Processing_Results.

            Inputs:
                dict_(str) : item key of list item [either "perfect" or "defect"] within the
                             Directories_Search.Dir_Calc_Keys dictionary or dictionary d.

                name(str)  : Nested dict item key of project name of the particular defect geometry/placement/impurity
                             inclusion.

                run(str)   : Nested dict item key of runtype of the calculation of the particular defect geometry/
                             placement/impurity inclusion.

                chrg(int)  : Nested dict item key of charge state of the calculation of the particular defect geometry/
                             placement/impurity inclusion.

                d(dict)    : Optional, gives dictionary name if wanted to be applied for dictionary which is not
                             Directories_Search.Dir_Calc_Keys.
        """

        if d:
            d[dict_].append([name, run, chrg])
        else:
            Directories_Search.Dir_Calc_Keys[dict_].append([name, run, chrg])


class InDirectory:
    """
        Definitions:
            BaderMissing(None->True)       : To be turned True if some defect subdirectories are found not to contain
                                             either the CP2K output file and intermediary file needed for bader charge
                                             analysis of the calculation.
            BaderBreak(None->True)         : To be turned True if CP2K output file and intermediary file needed for
                                             bader analysis could not be found within the defect-free structure's
                                             directory. Signals that bader charge analysis can't be done at all.
            ExeptionFound(bool)            : Only created [created in ProcessingChargesSpins.py] when user only wants
                                             charge analysis for atoms related to defect. When created is set as False,
                                             and is turned True if files needed for working out which atoms are related
                                             to defect aren't found in corresponding subdirectories for use.
            DirsMissingBader(dict)         : To be populated with a record of all subdirectories in which needed files
                                             for bader analysis could not be found as lists that matches a lists in
                                             Directories_Search.Dir_Calc_Keys.
            DirsMissingBader4error(list)   : To be populated with a record of sub-os.paths() for all subdirectories
                                             where needed files for bader analysis couldn't be found. Sub-os.paths()
                                             contain end of os.path() with only directories beyond the set sudo current
                                             working directory. Created for displaying directories within called error
                                             message for missing bader files.
            Execption2NNandDef(dict)       : Only created [created in ProcessingChargesSpins.py] when user only wants
                                             charge analysis for atoms related to defect. To be populated with a record
                                             of all subdirectories in which needed files couldn't be found as lists that
                                             matches a lists in Directories_Search.Dir_Calc_Keys.



        Inputs:
            keywrd(str)                    : Keyword corresponding to the result processing method currently being
                                             worked on which should also be one of the outer dictionary keys within the
                                             Directories_Search.Files4Results directory.

            lock(th.Lock)                  : Unowned lock synchronization primitive shared between threads which when
                                             called upon blocks the ability of any other thread to print until the lock
                                             has finished the printing commands within the current with statement it has
                                             acquired and is released.

            subkeywrd(None/str)            : Optional keyword corresponding to a sub-part of the keywrd result
                                             processing method. Will be a key str within first nested dictionary in the
                                             item value for item key keywrd within the Directories_Search.Files4Results
                                             directory.

    """

    BadersMissing = None

    BaderBreak = None

    DirsMissingBader = {"perfect": [], "defect": []}

    DirsMissingBader4error = []


    def __init__(self, keywrd, lock, subkeywrd = None):
        # only certain keywrds will have a subkeywrd included in their processing. Account for this.
        self.method = Directories_Search.Files4Results[keywrd][subkeywrd] if not subkeywrd == None else \
            Directories_Search.Files4Results[keywrd]

        self.keywrd, self.subkeywrd  = keywrd, subkeywrd

        if keywrd == "charges and spins" and subkeywrd == "only":
            # need special separate function for particular combination of keywrd and subkeywrd.
            self.OnlySpinsChargesOpt(lock)

        else:
            # 1st check intermediary files present, if intermediary files required, in each subdirectory
            nd, try4intr = [self.method.get("intermediary"), True] if "intermediary" in self.method.keys() \
                else [self.method.get("cp2k_outputs"), False]

            for dict_type, filetypes in nd.items():
                for name, run, chrg in Directories_Search.Dir_Calc_Keys[dict_type]:
                    self.Assessment(dict_type, name, run, chrg, filetypes, try4intr, lock)

    def Outcomes(self, dirpath, fltyps, test):
        """
            Sort out the variables returned from self.finding to give two list of bool answers and os_path/None strs.

            Created to stop code repetition.

            Inputs:
                dirpath(os.path)    : Path of subdirectory in which the file is being searched for

                fltyps(str)         : Name/extension of file being searched for

                test(bool)          : If True, testing the function by printing up certain steps to ensure function
                                      running as should. Input to be removed from final version.

            Outputs:
                found(list of bool) : Each item corresponds to the item of the same index within fltyps. True if file
                                      found within path, False if file not found within path

                newpath(os.paths)   : Each item corresponds to the item of the same index within fltyps. If
                                      corresponding item in found is True, the found file path which matches the
                                      name/extension of file.
        """

        # outcomes  either [bool1, path1] for 1 file or [[bool1, path1],[bool2, path2],...] for multiple
        outcomes = self.finding(dirpath, fltyps[0], test) if len(fltyps) == 1 else \
            [self.finding(dirpath, fltyp, test) for fltyp in fltyps]
        # convert multiple files case from [[bool1, path1],[bool2, path2],...] to [bool1, path1, bool2, path2,...]
        outcomes = [item for row in outcomes for item in row] if type(outcomes[0]) is not bool else outcomes
        # make to lists - found will be all bool variables [bool1, bool2,...], newpath is all paths [path1, path2,...]
        found, newpath = outcomes[::2], outcomes[1::2]

        return found, newpath

    def FileErrorOnlySpinsCharges(self, extension, dict_, name, run, chrg, lock):
        """
            Error handler for self.OnlySpinsChargesOpt function. Created to stop code repetition.

            Inputs:
                extension(str) : File extensions of file needed for completion of the result process method of charges
                                 and spins for only atoms related to the defect.

                dict_(str)     : item key of outermost dictionary with the Directories_Search.Address_book
                                 dictionary

                name(str)      : Project name of the particular defect geometry/placement/impurity inclusion
                                 of the subdirectory being searched for intermediary file/CP2K output file.

                run(str)       : Run type of the calculation of the particular defect geometry/placement/
                                 impurity inclusion of the subdirectory being searched for intermediary file/
                                 CP2K output file.

                chrg(int)      : Charge state of the calculation of the particular defect geometry/placement/
                                 impurity inclusion of the subdirectory being searched for intermediary file/
                                 CP2K output file.

                lock(th.Lock)  : Unowned lock synchronization primitive shared between threads which when called upon
                                 blocks the ability of any other thread to print until the lock has finished the
                                 printing commands within the current with statement it has acquired and is released.
        """

        try:
            raise FileNotFoundError
        except FileNotFoundError:
            # trigger error informing user ext_ wasn't found - analysis of only defect atoms can't be done 4 subdir.
            ErrorMessages.FileExtension_FileNotFoundError4ChargesAndSpinsOnly(extension,
                                                                              Directories_Search.Address_book
                                                                              [dict_][name][run]
                                                                              [chrg]["path"], lock)
            # update corresponding class definition to reflect analysis of only defect atoms can't be done 4 subdir.
            self.UpdateMissingDefinitions(self.subkeywrd, dict_, name, run, chrg)

    def OnlySpinsChargesOpt(self, lock):
        """
            Special function for finding files needed for processing of charges & spins for only atoms related to defect.

            Inputs:
                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
            -
        """

        # start with finding needed files within defect directories.
        for name, run, chrg in Directories_Search.Dir_Calc_Keys["defect"]:
            time.sleep(0.3)
            # search for file with ',inp' and get two lists, one purely of bools and one purely of os.path()s.
            found, newpath = self.Outcomes(
                Directories_Search.Address_book["defect"][name][run][chrg]["path"], [".inp"], False)
            if found[0] is False:
                # send information about directory in which .inp file couldn't be found in to error handling function.
                self.FileErrorOnlySpinsCharges(".inp", "defect", name, run, chrg, lock)
            else:
                # Get name of starting geometry xyz file from .inp file.
                xyzfilename = FromFile.FromInp(newpath[0], ["charges and spins"]).Return()
                # search for extracted initial xyz file within the directory path.
                found2, newpath2 = self.Outcomes(
                    Directories_Search.Address_book["defect"][name][run][chrg]["path"], xyzfilename, False)

                if found2[0] is False:
                    # send information about directory that initial xyz file isn't found in to error handling function.
                    self.FileErrorOnlySpinsCharges(xyzfilename[0], "defect", name, run, chrg, lock)
                else:
                    # initial xyz file has been found - append file path to Address_Book.
                    Directories_Search.add_keys_nested_dict(["defect", name, run, chrg], ["''.xyz"], [newpath2[0]],
                                                            Directories_Search.Address_book)

        # finding needed file within perfect directory.
        for name, run, chrg in Directories_Search.Dir_Calc_Keys["perfect"]:
            # search for the xyz file containing only the resultant geometry of perfect structure's last geo opt.
            found, newpath  = self.Outcomes(
                Directories_Search.Address_book["perfect"][name][run][chrg]["path"],
                self.method["cp2k_outputs"]["perfect"], False)

            if found[0] is False:
                # if last geometry optimization xyz file couldn't be found, search for file of all geometry steps.
                found2, newpath2 =  self.Outcomes(
                Directories_Search.Address_book["perfect"][name][run][chrg]["path"], "-1.xyz", False)

                # Assumed that -1.xyz file will always be in perfect structure directory and can be used to make -L.xyz
                newiterfiles = MakingIntermediaryFiles(
                    Core.Directories_Search.Address_book["perfect"][name][run][chrg]["path"],
                    newpath2, "geometry").Return()

                # append file paths of newly created intermediary files to Address_Book if relevant to processing method
                [Directories_Search.add_keys_nested_dict(["perfect"][name][run][chrg], [typ], [nwfl],
                                                         Directories_Search.Address_book)
                 for typ, nwfl in zip(Directories_Search.Files4Results["geometry"]["intermediary"]["perfect"],
                                      newiterfiles) if nwfl.endswith(typ)]
            else:
                Directories_Search.add_keys_nested_dict(["perfect", [name][run][chrg]],
                                                        self.method["cp2k_outputs"]["perfect"], [newpath[0]],
                                                        Directories_Search.Address_book)

    def Assessment(self, dict_, name, run, chrg, fltyps, inter, lock):
        """
            Assessment coordinator for finding result processing needed files in subdirectories

            Inputs:
                dict_(str)               : item key of outermost dictionary with the Directories_Search.Address_book
                                           dictionary

                name(str)                : Project name of the particular defect geometry/placement/impurity inclusion
                                           of the subdirectory being searched for intermediary file/CP2K output file.

                run(str)                 : Run type of the calculation of the particular defect geometry/placement/
                                           impurity inclusion of the subdirectory being searched for intermediary file/
                                           CP2K output file.

                chrg(int)                : Charge state of the calculation of the particular defect geometry/placement/
                                           impurity inclusion of the subdirectory being searched for intermediary file/
                                           CP2K output file.

                fltyps(str/list of strs) : list or name of file extensions of files needed for completion of results
                                           processing method.

                inter(boolean/None)      : if true, checking for intermediary files; if None, already checked for
                                           intermediary files, now checking for CP2K output files; if False, checking
                                           for CP2K output files.

                lock(th.Lock)            : Unowned lock synchronization primitive shared between threads which when
                                           called upon blocks the ability of any other thread to print until the lock
                                           has finished the printing commands within the current with statement it has
                                           acquired and is released.
        """

        KeyCheck, dirpath = Directories_Search.Address_book[dict_][name][run][chrg].keys(), \
                            Directories_Search.Address_book[dict_][name][run][chrg]["path"]
        # remove file extension(s) already found and in Directories_Search.Address_book from fltyps list.
        [fltyps.remove(fltyp) for fltyp in fltyps if fltyp in KeyCheck]
        # searching for file with file extensions and get two lists, one purely of bools and one purely of os.path()s.
        found, newpath = self.Outcomes(dirpath, fltyps, False)
        # send lists found and newpath to be evaluated on whether file extensions have been found.
        self.PostAssessmentTree("bool", dict_, name, run, chrg, inter, fltyps[0], found[0], newpath[0], lock) if \
            len(fltyps) == 1 \
            else self.PostAssessmentTree("list", dict_, name, run, chrg, inter, fltyps, found, newpath, lock)

    def finding(self, path, file, test):
        """
            Searching for file within the os.walk() directory tree of subdirectory path.

            Inputs:
                path(os.path)      : Path of subdirectory in which the file is being searched for

                file(str)          : Name/extension of file being searched for

                test(bool)         : If True, testing the function by printing up certain steps to ensure function
                                     running as should. Input to be removed from final version.

            Output:
                in_(bool)          : True if file found within path, False if file not found within path

                add2dict_(os.path) : If in_ is True, the found file path which matches the name/extension of file.
        """

        # function variable set up
        Lys, lyr, spltpth, w, in_, add2dict_, all_ = {"lyr":{} }, 1, str(path).split('/'), os.walk(path), None, 'N', 'N'
        if test is True:
            print(f"{bcolors.HEADER}{path}{bcolors.ENDC}, {bcolors.QUESTION}{file}{bcolors.ENDC}\n")  # #
            # hide

        # traversing directory tree of subdirectory given as path with path, dirs, & files in top-down approach.
        for (path_, dr, fls) in w:
            if in_ is True:
                # if variable in_ is True, break for loop through os.walk()
                break
            if test is True:
                print(f"{bcolors.QUESTION}path = {bcolors.OKBLUE}{path_}{bcolors.ENDC}, {bcolors.QUESTION}dir = "
                      f"{bcolors.OKCYAN}{dr}{bcolors.ENDC}, {bcolors.QUESTION}files = {bcolors.WARN4}{fls}{bcolors.ENDC}"
                      f", {bcolors.QUESTION}layer = {bcolors.OKGREEN}{lyr}{bcolors.ENDC}, {bcolors.QUESTION}in_ = "
                      f"{bcolors.FAIL}{in_}{bcolors.ENDC}")  # #
                # hide

            # if str of number of layer, lyr is not a nested key within dictionary Lyrs["lyr"]
            if str(lyr) not in Lys["lyr"]:
                # created nested dict for layer # with inner dict "fd" of list of dirs found by os.walk() and empty "tv"
                Lys["lyr"][str(lyr)] = {"fd":dr, "tv":[]}

            # if none of current path_ split list items are not in the split list of input path - in smaller subdir
            if len([d for d in str(path_).split('/') if d not in spltpth]) > 0:
                if test is True:
                    print(f"{bcolors.QUESTION}layer = {bcolors.OKGREEN}{lyr}{bcolors.ENDC}")  # #
                    # hide

                # reassign value of layer, lyr, to value of how many subdir layers deep current path_ is from input path
                lyr = len([d for d in str(path_).split('/') if d not in spltpth])
                if test is True:
                    print(f"{bcolors.QUESTION2}layer = {bcolors.OKGREEN}{lyr}{bcolors.ENDC}")  # #
                    # hide

                if str(path_).split('/')[-1] in Lys["lyr"][str(lyr)]["fd"]:
                    # append this last directory name of the path to the inner dict "tv" list
                    Lys["lyr"][str(lyr)]["tv"].append(str(path_).split('/')[-1])
            if test is True:
                print(Lys)  # #
                # hide

            # if directory of current path_ is completely empty, containing no files or subdirectories.
            if not dr and not fls and in_ is not True:
                # iterate through layers to current #, check all dirs transversed in upper layers- ie [#][fd] = [#][tv]
                for i in range(1, lyr + 1):
                    all_ = True if Lys["lyr"][str(i)]["tv"] == Lys["lyr"][str(i)]["fd"] and all_ is True or \
                                   Lys["lyr"][str(i)]["tv"] == Lys["lyr"][str(i)]["fd"] and all_ == "N" else False

                # if all upper layer directories have been transversed, then at end of directory tree & file not found.
                if all_ is True:
                    in_ = False
                    break
            else:
                for indx, file_ in enumerate(fls):
                    # file found in dir
                    if file_.endswith(str(file)) and not path_.endswith(".ipynb_checkpoints") and in_ is not True:
                        add2dict_ = os.path.join(path_, file_)
                        in_ = True
                        break
                    # if at the end of list of items in the directory and file has not been found.
                    elif indx == len(fls) - 1 and not in_ and in_ is not True:
                        # if already within final subdirectory of directory tree.
                        if not dir:
                            in_ = False
                        else:
                            lyr += 1

            if test is True:
                print(f"{bcolors.QUESTION2}path = {bcolors.OKBLUE}{path_}{bcolors.ENDC}, {bcolors.QUESTION2}new in_ =  "
                      f"{bcolors.FAIL}{in_}{bcolors.ENDC}, {bcolors.QUESTION2}layer = {bcolors.OKGREEN}{lyr}{bcolors.ENDC}")  # #
                # hide

        if not in_:
            if test is True:
                print(in_)
                # hide

            in_ = False
        if test is True:
            print(f"[{in_}, {add2dict_}]\n")  # #
            # hide

        return [in_, add2dict_]

    def PostAssessmentTree(self, Type, dict_, name, run, chrg, inter, fltyp, found, newpath, lock):
        """
            Deciding action taken branching function for outcome of whether needed file(s) was located in subdir.


            Inputs:
                Type(str)                : Whether fltyp, found, and newpath inputs are singular variables or lists of
                                           variables and acts as an indication of which version of if statement should
                                           be evaluated for each of the four options held within the option dictionary
                                           of the function.

                dict_(str)               : Item key of outermost dictionary with the Directories_Search.Address_book
                                           dictionary.

                name(str)                : Project name of the particular defect geometry/placement/impurity inclusion
                                           of the subdirectory being searched for intermediary file/CP2K output file.

                run(str)                 : Run type of the calculation of the particular defect geometry/placement/
                                           impurity inclusion of the subdirectory being searched for intermediary file/
                                           CP2K output file.

                chrg(int)                : Charge state of the calculation of the particular defect geometry/placement/
                                           impurity inclusion of the subdirectory being searched for intermediary file/
                                           CP2K output file.

                inter(boolean)           : If true, checking for intermediary files; if None, already checked for
                                           intermediary files, now checking for CP2K output files; if False, checking
                                           for CP2K output files.

                fltyp(list of str/str)   : List or name of file extensions of files needed for completion of results
                                           processing method.

                found(list of bool/bool) : If True, file with file extension fltyp has been found in subdirectory; if
                                           False, file type could not be found.

                newpath(None/os.path(s)) : File path, if found, of the file with file extension fltyp in subdirectory.

                lock(th.Lock)            : Unowned lock synchronization primitive shared between threads which when
                                           called upon blocks the ability of any other thread to print until the lock
                                           has finished the printing commands within the current with statement it has
                                           acquired and is released.
        """

        options = {"opt1":
                       {"bool": "inter is True and found is not True",
                        "list": "inter is True and True not in found or inter is True and True in found and False in "
                                "found"},
                   "opt2":
                       {"bool": "inter is True and found is True or inter is False and found is True",
                        "list": "inter is True and False not in found or inter is False and False not in found"},
                   "opt3":
                       {"bool": "inter is None and found is True", "list": "inter is None and False not in found"},
                   "opt4":
                       {"bool": "inter is None and found is not True or inter is False and found is not True",
                        "list": "inter is None and False in found or inter is False and False in found"}}


        # Checking for intermediary file & intermediary file not found/all or some intermediary files not found
        if eval(options["opt1"].get(Type)):
            # rerun assessment function to see if direct CP2K output files are in subdirectory
            self.Assessment(dict_, name, run, chrg, self.method.get("cp2k_outputs")[dict_], None, lock)

        # Checking for intermediary file & intermediate file found/No intermediary file needed, CP2K output file found.
        elif eval(options["opt2"].get(Type)):
            # intermediate/CP2K output file has been found so append their file path to Address_Book.
            [Directories_Search.add_keys_nested_dict([dict_, name, run, chrg], [fl], [pth],
                                                     Directories_Search.Address_book) for fl, pth in
             zip(fltyp, newpath)] if Type == "list" else \
                Directories_Search.add_keys_nested_dict([dict_, name, run, chrg], [fltyp], [newpath],
                                                        Directories_Search.Address_book)

        # Intermediary file(s) not found, checking for CP2K output file. CP2K output files found.
        elif eval(options["opt3"].get(Type)):
            ## multithreading set up
            # to pass information between threads.
            q = queue.Queue()
            # start thread to perform tasks to generate intermediate files.
            t0a = th.Thread(target=MakingIntermediaryFiles, args=(
                Core.Directories_Search.Address_book[dict_][name][run][chrg]["path"], newpath, self.keywrd, q))
            t0a.start()

            # start thread which starts printing '---' across the screen as Intermediary files are being created.
            t0b = th.Thread(target=Core.ProcessTakingPlace, args=(lock, 0.05, True))
            t0b.start()
            t0a.join()
            while q.empty() is False:
                # item which will be passed to queue will be file paths of the intermediary files generated
                newiterfiles = q.get()
                # append file paths of newly created intermediary files to Address_Book if relevant to processing method
                [Directories_Search.add_keys_nested_dict([dict_, name, run, chrg], [typ], [nwfl],
                                                         Directories_Search.Address_book)
                 for typ, nwfl in zip(self.method["intermediary"][dict_], newiterfiles) if nwfl.endswith(typ)]
            t0b.join()

        # Intermediary file & CP2K output file not found/No needed intermediary file, CP2K output file not found.
        elif eval(options["opt4"].get(Type)):
            # different errors & error codes need to be called based on different results processing methods performed.
            try:
                if self.keywrd == "charges and spins" and self.subkeywrd == "bader":
                    if dict_ == "perfect":
                        # raise when bader files for perfect structure not found as bader analysis can't be done at all.
                        raise ConnectionAbortedError
                    else:
                        # exception & error will be raised in ProcessingChargesSpins.py, setup for raising of error.
                        self.UpdateMissingDefinitions(self.subkeywrd, dict_, name, run, chrg)
                else:
                    # create list of all files which are missing within directory
                    missing = [file for file, fnd in zip(fltyp, found) if fnd is False] if Type == "list" else [fltyp]
                    raise FileNotFoundError

            except ConnectionAbortedError:
                # update corresponding class definition to reflect bader analysis can't be done.
                self.UpdateMissingDefinitions("perf bader")
                # trigger error message informing user that bader analysis can't be performed when lock next unreleased.
                ErrorMessages.FileExtension_ConnectionAbortedError(
                    Core.Directories_Search.Address_book[dict_][name][run][chrg]["path"], lock)
                # exist thread performing the InDirectory class.
                sys.exit(0)

            except FileNotFoundError:
                # trigger error message informing user files in missing not found in directory when lock next unreleased
                ErrorMessages.FileExtension_FileNotFoundError3(self.keywrd, name, run, chrg, missing, lock)

    @classmethod
    def UpdateMissingDefinitions(cls, subkeyword, dict_= None, name = None, run = None, chrg = None):
        """
            Update class definitions to reflect certain exceptions apply to result processing of particular calculations.

            Inputs:
               subkeyword(str)  : Trigger to indicate which class definitions need to be updated. May be one of the key
                                  strs of the first nested dictionary in the item value for the currently being
                                  performed results processing method item key, in the Directories_Search.Files4Results
                                  directory.

               dict_(str)       : (Optional) Item key of outermost dictionary with the Directories_Search.Address_book
                                  dictionary.

               name(str)        : (Optional) Project name of the particular defect geometry/placement/impurity inclusion
                                  of the subdirectory being searched for intermediary file/CP2K output file.

               run(str)         : (Optional) Run type of the calculation of the particular defect geometry/placement/
                                  impurity inclusion of the subdirectory being searched for intermediary file/CP2K
                                  output file.

               chrg(int)        : (Optional) Charge state of the calculation of the particular defect geometry/
                                  placement/impurity inclusion of the subdirectory being searched for intermediary file/
                                  CP2K output file.
        """

        if subkeyword == "perf bader":
            InDirectory.BaderBreak = True

        if subkeyword == "bader":
            InDirectory.BadersMissing = True

            # Add list that matches a list in Directories_Search.Dir_Calc_Keys to dict InDirectory.DirsMissingBader.
            Directories_Search.add_to_Dir_Calc_Keys(dict_, name, run, chrg, InDirectory.DirsMissingBader)

            # Don't want full file path from / - only directories beyond the set sudo current working directory
            path, cwd = str(Core.Directories_Search.Address_book[dict_][name][run][chrg]["path"]).split('/'), \
                        str(os.getcwd()).split('/')
            dirpath = '/'.join([directory for directory in path if directory not in cwd])

            # append file path of only directories beyond sudo cwd
            InDirectory.DirsMissingBader4error.append(str(dirpath))

        elif subkeyword == "only":
            # if this is the first exception where files missing for working out defect related atoms in a calc
            if Core.InDirectory.ExeptionFound is not True:
                # set dictionary definition to true.
                Core.InDirectory.ExeptionFound = True

            # Add list that matches a list in Directories_Search.Dir_Calc_Keys to dict InDirectory.Execption2NNandDef.
            Directories_Search.add_to_Dir_Calc_Keys(dict_, name, run, chrg, Core.InDirectory.Execption2NNandDef)


class MakingIntermediaryFiles:
    """
        Creating intermediary files needed for results processing method from given CP2K output files.

        Definitions:
            functions(dict)                : Dictionary of associated functions within class which should be used to
                                             create the needed intermediary files for each particular result processing
                                             method.

        Inputs:
            dirpath(os.path)               : Directory path to directory of calculation where intermediate file needs
                                             to be created in.

            filepaths(str/list of os.path) : File path(s) of CP2K output file(s) to be used for creating the
                                             intermediary file(s).

            keywrd(str)                    : Keyword corresponding to the result processing method wanting to be
                                             performed by user.

            q(queue.Queue)                 : Optional. When given shared between this class and function
                                             Core.InDirectory.PostAssessmentTree to allow the returning of New file
                                             os.path()(s) for the newly created intermediary file(s) back to
                                             Core.InDirectory.PostAssessmentTree.
zxz
        Outputs:
            flns4rtrn(str/list of os.path) : New file os.path()(s) for the newly created intermediary file(s).
    """

    functions = {"charges and spins": "BaderFileCreation",
                 "Geometry": "GeometryLastCreation"
                 }

    def __init__(self, dirpath, filepaths, keywrd, q = None):
        self.dirpath, self.filepaths = dirpath, filepaths
        # get list of names of all items within directory of self.dirpath at entry to class.
        before = os.listdir(self.dirpath)

        # call associated function for
        eval("self.{}()".format(MakingIntermediaryFiles.functions.get(keywrd)))

        after = os.listdir(self.dirpath)
        self.flns4rtrn = [os.path.join(self.dirpath, file) for file in after if file not in before]
        if q:
            q.put(self.flns4rtrn)

    def BaderFileCreation(self):
        """
            Creation of "ACF.dat" (atom coords), "AVF.dat"(bader coords), "BCF.dat"(atomic vol) files for bader analysis.

            self.filepaths should consist of one os.path() for file with file extension '-ELECTRON_DENSITY-1_0.cube.'

        """

        # filename at end of self.filepaths os.path(), cwd when entering function, & os.path() to bader executable.
        baderfile, cwd, BdrExec = self.filepaths.split("/")[-1], os.getcwd(), \
                                  os.path.join(Core.Directories_Search.executables_address,"bader")

        # change sudo current working directory (cwd) to directory of calculation.
        os.chdir(self.dirpath)
        # acts as: !{bader executable} {filepath}; output created by BdrExec program is suppressed.
        p = subprocess.call([BdrExec, baderfile],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.STDOUT)
        # change sudo current working directory back to originally set directory in MAIN.py.
        os.chdir(cwd)

    def GeometryLastCreation(self):
        """
            Creation of new xyz file which contains the coordinates of the final geometry optimization step of the calc.

            self.filepaths should consist of one os.path() for file with the file extension of '1.xyz'.
        """

        # derive new file name from previous 1.xyz name with the new extension of L.xyz.
        new_xyz_file = "".join([i for i in self.filepaths][:-5] + ["L.xyz"])
        old_xyz, new_xyz1 = open(self.filepaths, 'r'), open(new_xyz_file, 'w')
        # tot # of atoms will not change between 1st & last optimization step - 1st 1.xyz line gives # of atoms in calc.
        tot_atoms, lines, j, index = [str('     ' + "".join(old_xyz.readline().split())), old_xyz.readlines(),
                                      len(old_xyz.readlines()), len(old_xyz.readlines()) + 1]

        last_itr = False
        # for last geometry step, need to start at bottom of 1.xyz file.
        for line in reversed(lines):
            # moving up the lines from the bottom of 1.xyz file.
            index -= 1

            # last line in 1.xyz file which will be written as first line in new L.xyz file.
            if tot_atoms not in line and index == j and last_itr is False:
                string = line
                new_xyz1.write(string)
                new_xyz1.close()

            # rest of the coordinates of the last geometry step and final line with total atoms.
            elif last_itr is False:
                # 1st line of each geometry optimization step has only tot # of atoms - Last line to write.
                if tot_atoms in line and last_itr is False:
                    # Last_itr needs to be set to True to stop the writing of further lines to L.xyz after final line.
                    last_itr = True

                # opening L.xyz file in read+ mode so that file can be read and written to.
                with open(new_xyz_file, 'r+') as new_xyz2:
                    # create list of all lines within the newly created L.xyz file.
                    lines2 = new_xyz2.readlines()
                    # add next line up from the bottom of 1.xyz to the front of the list of lines in L.xyz.
                    lines2.insert(0, line)
                    new_xyz2.seek(0)
                    # write amended list of L.xyz lines with next line from 1.xyz at the top from top of file down.
                    new_xyz2.writelines(lines2)

    def Return(self):
        return self.flns4rtrn