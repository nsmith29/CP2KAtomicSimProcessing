#!/usr/bin/env python3

#   Answers.py deals with recording the commandline arguments given by the user as well as the commandline inputs given
#   by the user to the questions asked within MAIN.py Start.Questions2Ask()
#   ----------------------------------------------------------
#   Author: Niamh Smith; E-mail: niamh.smith.17 [at] ucl.ac.uk
#   Date:
import os
import Core

class UArg:
    """
        Saving commandline arguments from user upon execution of MAIN.py as class definitions.

        Class Definitions:
            PerD(os.path)     : Saved full directory path to directory user named as the directory holding CP2K output
                                files for the perfect defect-free material structure.
            DefD(os.path)     : Saved full directory path to directory user named as the parent directory of particular
                                type of defect studied within material.
            CPtD(os.path)     : Saved full directory path to directory user named as the parent directory for
                                individual calculated reference chemical potentials for host and/or impurity elements
                                within material.
            Expt(boolean)     : True if user wants all defect subdirectories except ones stated after in commandline
                                arguments to be included in the data processing.
            Only(boolean)     : True if user wants only data processing of data within subdirectories stated after in
                                command line argument.
            SubDs(list)       : Saved list of subdirectory names given by user at the end of the commandline arguments
                                after keyword only or except.
            FdSD(dict)        : Empty dictionary which is only populated if the keyword 'only' has been used in the
                                command line arguments by the user. Each subdirectory name given in Input only (see
                                Inputs below) is put into this dictionary as an item key with an item value of 'False'.
                                The item value will be updated to 'True' when a subdirectory with a name that matches
                                one of the item keys is found within the tree directory of DefD.
        Inputs:
            perf_dir(str)     : Name of directory containing CP2K output files for the perfect defect-free material
                                structure given by user.

            def_dir(str)      : Name of parent directory of particular  type of defect studied within material given
                                by user.

            chem_pot_dir(str) : Name of parent directory holding subdirectories for individual calculated reference
                                chemical potentials for host and/or impurity elements within material given by user.

            expt(list)        : List of subdirectory names user wants to be excluded from data processing.

            only(list)        : List of subdirectory names user only wants to be data processed.
    """
    PerD = ''
    DefD = ''
    CPtD = ''
    Expt = False
    Only = False
    SubD = ''
    FdSD = dict()

    def __init__(self, perf_dir, def_dir, chem_pot_dir):
        UArg.ArgumentsSaved(perf_dir, def_dir, chem_pot_dir)

    @classmethod
    def ArgumentsSaved(cls, perf_dir, def_dir, chem_pot_dir):
        UArg.PerD= os.path.join(os.getcwd(),perf_dir)
        UArg.DefD= os.path.join(os.getcwd(),def_dir)
        UArg.CPtD= os.path.join(os.getcwd(),chem_pot_dir)

    @classmethod
    def ExceptionStated(cls, expt):
        UArg.Expt= True
        UArg.SubD= expt

    @classmethod
    def OnlyStated(cls, only):
        UArg.Only= True
        UArg.SubD= only
        for sub in only:
            UArg.FdSD[str(sub)]= False

class UserWants:
    """
        Saving commandline inputs given by user related to their analysis and display needs.

        Class definitions:
            AnalysisWants(None -> boolean) : True if user responds 'Y' to question 2 and wants results analysis.
            DisplayWants(None -> boolean)  : True if user responds 'Y' to Follow-up question 1 and wants to display
                                             results via GUI.
            BooleanConverter(dict)         : Dictionary used to convert.
        Inputs:
            analysis(str)                  : String of either 'Y' or 'N' corresponding to whether user wants analysis
                                             to be performed.

            display(str)                   : String of either 'Y' or 'N' corresponding to whether user wants results to
                                             be displayed in a GUI window.
    """
    AnalysisWants = None
    DisplayWants = None
    Append = None
    Overwrite = None

    BooleanConverter = {'Y':True,
                      'N':False}

    def __init__(self, f):
        self._f= f

    @classmethod
    def Save(cls, analysis, display):
        UserWants.AnalysisWants = UserWants.BooleanConverter[analysis]
        UserWants.DisplayWants = UserWants.BooleanConverter[display]

    @classmethod
    def appendVoverwrite(cls, append, overwrite):
        UserWants.Append = UserWants.BooleanConverter[append]
        UserWants.Overwrite = UserWants.BooleanConverter[overwrite]


class ProcessCntrls:
    """
        Saving the results processing options given by user in commandline input.

        Class definitions:
            ProcessWants(None -> list) : Saved list of result processing methods wanted by user.
            ProcessResults(dict)       : Empty dictionary to be populated with the same maj item keys of
                                         Core.Directories_Search.Address_book and then min item keys of each result
                                         processing method wanted by user with the item values of these min item keys
                                         being the fully calculated product of the result processing method.
                                         E.g. for the "charges and spins" result processing method, the item value
                                         will be the dataframe of Mulliken, Hirshfield, and bader charge and spin
                                         data.
            setup(list)                : List of placeholder item values for pairing and creation of inner nested
                                         dictionary of ProcessResults.

        Inputs:
            Processing(list)           : List of result processing options given by user in commandline input.
    """
    ProcessWants = None
    setup = None
    ProcessResults = {"perfect": dict(), "defect": dict()}

    def __init__(self, f):
        self._f= f

    @classmethod
    def SavingOtherWants(cls, processing):
        setup = []
        for process in processing:
            # When ProcessResults populated, are enough inner item values for inner result processing methods key strs.
            setup.append(str("results for {}".format(process)))

        ProcessCntrls.ProcessWants = processing
        ProcessCntrls.setup = setup

        if Core.UArg.Only is True:
            # ProcessResults not populated if 'only' used, now ProcessWants are known & saved, populate ProcessResults.
            Core.Directories_Search.PopulateResultsHolder()

    @classmethod
    def UpdateForResultsSaving(cls, dict_, name, rn_typ, chrg_stt, keywrd, result):
        """
            Update the inner item value for inner item key 'keywrd' to hold generated results item for defect.

            Inputs:
                dict_(str)          : Item key of list item [either "perfect" or "defect"] within the
                                      Directories_Search.Dir_Calc_Keys dictionary or dictionary d.

                name(str)           : Nested dict item key of project name of the particular defect geometry/placement/
                                      impurity inclusion.

                run(str)            : Nested dict item key of runtype of the calculation of the particular defect
                                      geometry/placement/impurity inclusion.

                chrg(int)           : Nested dict item key of charge state of the calculation of the particular defect
                                      geometry/placement/impurity inclusion.

                keywrd(str)         : Keyword which corresponds to the result processing method that the input 'result'
                                      is the processed outcome of.

                result(unspecifiec) : Processed outcome of results processing method of the input 'keywrd'.
        """
        Core.ProcessCntrls.ProcessResults[dict_][name][rn_typ][chrg_stt].update({keywrd: result})




