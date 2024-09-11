#!/usr/bin/env python3

import sys
import time
import queue
import json
import numpy as np
import pandas as pd
import threading as th
from Core.Messages import bcolors, ErrorMessages, SlowMessageLines
import Core
import FromFile



class CntrlChrgSpns:
    """
        Entry control point into charge and spin processing and analysis.

        Class mp.Process() is passed to via Core.Rooting when user gives "charges and spins" as a wanted results
        processing method.

        Class Definitions:
            NNandDef(boolean) : If False, charge and spin data to be processed for all atoms in calculation. If True,
                                charge and spin data only to be processed for certain atoms related to defect.

            questions(dict)   : Dictionary of questions to ask the user related to charge and spin processing.
    """

    NNandDef = None

    ContBdr =  None

    questions = {"Q1":f"\n{bcolors.QUESTION}Would you like to process charge and spin data for only atoms "
                      f"related to defect, i.e. nearest neighbouring atoms to defect site and defect atom, if present?"
                      f"({bcolors.OKCYAN}Y/N{bcolors.QUESTION})",
                 "Q2":f"\n{bcolors.QUESTION}Would you like to continue with Bader charge analysis for the "
                      f"found subdirectories which do contain the required files for this charge analysis method?("
                      f"{bcolors.OKCYAN}Y/N{bcolors.QUESTION})"}

    def __init__(self):
        #
        text = str("\n                                      {bcolors.OKGREEN}{bcolors.UNDERLINE}CHARGE AND SPIN DATA "
                   "PROCESSING{bcolors.ENDC}{bcolors.OKGREEN}...")
        SlowMessageLines(text)

        ## multithreading set up

        q = queue.Queue()
        lock = th.Lock()
        t1 = th.Thread(target=self.AskQuestion, args=(q, lock))
        t2 = th.Thread(target=self.BaderFiles, args=(q, lock))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

        # For perfect, get charges and spins for all atoms and save them as matrix.
        t3 = th.Thread(target=self.AllAtomsPerfect(), args=())
        t3.start()

        #
        if CntrlChrgSpns.NNandDef is True:
            t4 = th.Thread(target=self.NNandDefWanted, args=(lock,))
            t4.start()
        else:
            t4 = th.Thread(target=self.AllAtomsDefectSetup, args=())
            t4.start()
        t3.join()
        t4.join()

    def NNandDefWanted(self, lock):
        """

        """
        self.CreateDefinition()
        Core.InDirectory("charges and spins", lock, "only")

    def AllAtomsPerfect(self):
        """

        """
        # set up empty lists for panda dataframe
        TypeC, indexstrings, clmnstrngs = [], [], []

        # Collate charges and spins data
        name, run, chrg = Core.Directories_Search.Dir_Calc_Keys["perfect"]
        Mulliken, Hirshfeld =  FromFile.FromLog(
            Core.Directories_Search.Address_book["perfect"][name][run][chrg][".log"], ["charges and spins"]).Return()

        # Mulliken matrix [[alpha, beta, charge, spin],...]
        clmnstrngs.extend(["Mulliken, \u03B1 pop", "Mulliken, \u03B2 pop", "Mulliken, charges", "Mulliken, spins"])
        for indx, matline in enumerate(Mulliken):
            indexstrings.append(indx)
            TypeC.append(matline)

        #  Hirshfeld matrix [[alpha, beta, charge, spin],...]
        clmnstrngs.extend(["Hirshfeld, \u03B1 pop", "Hirshfeld, \u03B2 pop", "Hirshfeld, charges", "Hirshfeld, spins"])
        for indx, matline in enumerate(Hirshfeld):
            TypeC[indx].extend(matline)

        if Core.InDirectory.BaderBreak is not True:
            # Bader matrix [charge1, charge2, ......]
            Bader = np.loadtxt(Core.Directories_Search.Address_book["perfect"][name][run][chrg]["ACF.dat"],
                               skiprows=2, usecols=4, max_rows=448, unpack=True)
            clmnstrngs.append("Bader")
            for indx, matline in enumerate(Bader):
                TypeC[indx].append(round(int(matline),3))

        # Creation of panda dataframe of collated charges and spins
        df = pd.DataFrame(TypeC,
                          columns=clmnstrngs, index=indexstrings)
        n = df.columns.str.split(', ', expand=True).values
        df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in n])

        # Saving of dataframe to results
        Core.ProcessCntrls.UpdateForResultsSaving("perfect", name, run, chrg, "charges and spins", df)

        # Test saving of dataframe to results
        # print(Core.ProcessCntrls.ProcessResults["perfect"][name][run][chrg].get("charges and spins").to_string())

    def AllAtomsDefectSetup(self):
        """

        """
        for name, run, chrg in Core.Directories_Search.Dir_Calc_Keys["defect"]:
            self.AtomsDefect(name, run, chrg)

    def AtomsDefect(self, name, run, chrg):
        """

        """
        j = 0

    def Test4inputError(self, Q, A, lock):
        """
            Created to stop code repetition.
        """
        if str(A).upper() not in ['Y', 'N']:
            # if user has given an input which is not 'Y' or 'N', trigger ValueError.
            try:
                raise ValueError
            except ValueError:
                ErrorMessages.Main_ValueError2(lock)
                text = str(CntrlChrgSpns.questions[Q]+":")
                SlowMessageLines(text, lock)
                A = str(input( )).upper()
        Core.ProcessTakingPlace(lock, 0.05)

        return A

    def AskQuestion(self,q, lock):
        """
            OPTION: user want data for all atoms or only atoms related to defect (nearest neighbours and defect atom)?

            User required input question asked during multiprocessing process via use of sys.stdin() as one of two
            threads while the second thread finds files of bader charge analysis.

            Inputs:
                q

                lock

        """
        sys.stdin = open(0) # sys.stdin allows for command line input to be asked and waited for while within a
                            # multiprocessing process.
        while True:
            text = str(CntrlChrgSpns.questions["Q1"]+"{bcolors.OKBLUE}\nSelecting {bcolors.OKCYAN}'N'{bcolors.OKBLUE} "
                                                     "will result in charge and spins being processed for all atoms "
                                                     "within a calculation:")
            SlowMessageLines(text, lock)
            with lock:
                which_atoms = input()

            if Core.InDirectory.BaderBreak is not True:
                which_atoms = self.Test4inputError("Q1", which_atoms, lock)
            break  # must break out of while True loop otherwise question will be repeatedly asked once user has given
                   # their answer to input question.

        self.AnswertoOnly(Core.UserWants.BooleanConverter[str(which_atoms).upper()])
        q.put("pass")   # allow rest of self.BaderFile function to run now that user has supplied answer to asked
                        # question.

    def BaderFiles(self,q, lock):
        """


            Inputs:
                q

                lock
        """
        Core.InDirectory("charges and spins", lock, "bader")


        while q.empty() is True:  # If call of Core.InDirectory() two lines above completes before user has answered
                                  # question asked in self.AskQuestion function, stall running of remainder of function.
            time.sleep(0.2)

        while q.empty() is False:  # When queue q is given an item to show that user has given an answer and completed
                                   # self.AskQuestion function continue with rest of code for function.
            if Core.InDirectory.BaderBreak is True:
                sys.exit(0)
            if Core.InDirectory.BadersMissing is True:
                try:
                    raise FileNotFoundError
                except FileNotFoundError:
                    ErrorMessages.ProcessingChargesSpins_FileNotFoundError(Core.InDirectory.DirsMissingBader4error, lock)
                while True:
                    text = str(CntrlChrgSpns.questions["Q2"]+"{bcolors.OKBLUE}\nMulliken and Hirshfeld analysis will "
                                                             "still be performed for all found subdirectories. "
                                                             "Selecting {bcolors.OKCYAN}'Y'{bcolors.OKBLUE} will result"
                                                             " in extra datatable columns of Bader analysis data for "
                                                             "calculations which Bader analysis can be performed for:")
                    SlowMessageLines(text, lock)
                    Continue = input()

                    Continue = self.Test4inputError("Q2", Continue, lock)
                    break
                self.AnswertoBader(Core.UserWants.BooleanConverter[str(Continue).upper()])
            break

    @classmethod
    def AnswertoOnly(cls, bool):
        CntrlChrgSpns.NNandDef = bool

    @classmethod
    def AnswertoBader(cls, bool):
        CntrlChrgSpns.ContBdr = bool

    @classmethod
    def CreateDefinition(cls):
        """

        """
        Core.InDirectory.Execption2NNandDef = {"perfect": [], "defect": []}
        Core.InDirectory.ExeptionFound = False



