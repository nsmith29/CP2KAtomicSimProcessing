#!/usr/bin/env python3

#   Main python execution file of CP2KAtomicSimProcessor package
#   -----------------------------------------------------------
#   Usage:
#
#   -----------------------------------------------------------
#   Author: Niamh Smith; E-mail: niamh.smith.17 [at] ucl.ac.uk
#   Date: 05/08/2022; 11/08/2022 [multiprocessing implementation update]; 15/08/2022 [Debugging update]; 20/08/2022
#   [inheritance testing]; 23/08/2022 [update for PDOS, Charge+Spin, and Substitutional defect geometry]; 19/09/2022
#   [update for user inputs]; /08/2024 [upgrade of entire package]

import os
import sys
import time
import threading as th
import queue
# import json
# import multiprocessing as mp
# import multiprocessing.pool
import Core
from Core.Messages import bcolors, ErrorMessages, SlowMessageLines
from Core.mpPicklingError import ProcessNoDaemonProcess, resave_, Rooting, PoolNoDaemonProcess
# import DataProcessing


def save_executables_path(package_path):
    """
        Save file path of directory holding all unix executable files used by CP2KAtomicSimProcessor

        Inputs:
            package_path(os.path): File path to CP2KAtomicSimProcessor directory.
    """
    Core.Directories_Search.executables_address = os.path.join(package_path,"Executables")

package_path = os.getcwd()  # before os.chdir used, current working directory will be within CP2KAtomicSimProcessor
save_executables_path(package_path)

# sudo current working directory
os.chdir('/Users/appleair/Desktop/PhD/Jupyter_notebooks/Calculations/PBE0_impurities_analysis/Only_PBE0')
cwd = os.getcwd() # save os.path set by os.chdir command above as a variable

class Start:
    """
        Processing command line arguments upon running of MAIN.py. Decides code path to take, given # of arguments given.

        Class definitions
            test(dict)      : Dictionary of valid keywords for argument four to test whether
                              the 4th commandline argument given by user is a valid keyword.
            questions(dict) : Dictionary of questions to ask the user within
                              self.check_users_wants().
            options(list)   : List of the methods of data processing the user can choose
                              from.

        Compulsory arguments given by user should represent the following info
            argv[1](str)   : name of directory containing CP2K output files for the perfect
                             defect-free material structure.
            argv[2](str)   : name of parent directory of particular type of defect studied
                             within material which contains the subdirectories of CP2K
                             output files for each specific defect calculation run.
            argv[3](str)   : name of parent directory holding subdirectories containing
                             CP2K output files for individual calculated reference
                             chemical potentials for host and/or impurity elements
                             within material being studied.
            argv[4](str)   : keyword of either 'all', 'except', or 'only'.

        Optional argument to be included by user, if argv[4] is except or only, should represent the following info
            argv[5:](str)  : each argument from the 6th argument onwards should be
                             the name of a specific subdirectory within the parent
                             directory named in argv[2].

    """

    test = {"all":True,
            "except":True,
            "only":True}

    questions = {"Q1":f"\n{bcolors.QUESTION}Which results types would you like to process?{bcolors.ENDC}",
                 "Q2":f"\n{bcolors.QUESTION}Would you like to perform data analysis?({bcolors.OKCYAN}Y/N{bcolors.QUESTION})" 
                      f"{bcolors.ENDC}",  # 45
                 "Q2fup1":f"\n{bcolors.QUESTION}Would you like to create a GUI to display results?({bcolors.OKCYAN}Y/N"
                          f"{bcolors.QUESTION}){bcolors.ENDC}",
                 "Q2fup2":f"\n{bcolors.QUESTION}Would you like to overwrite this file?({bcolors.OKCYAN}Y/N"
                          f"{bcolors.QUESTION}){bcolors.ENDC}"}

    options = ("band structure", "charges and spins", "charge transition levels", "geometry", "IPR", "PDOS", "WFN",
               "work function", "test")

    def __init__(self):

        # testing whether commandline arguments 1-4 given by user trigger any error codes.
        try:
            # test whether correct number of arguments has been given,
            keywrd = str(sys.argv[4])
            # test whether fourth argument is a valid keyword.
            testkeywrd = Start.test[keywrd]
            # test whether strs given in argvs 1, 2, and 3 correspond to actual directories.
            for i in 1,2,3:
                # test the existence of directory names given as strings  in command arguments`by changing sudo cwd.
                os.chdir(os.path.join(cwd,str(sys.argv[i])))
            # reset current working directory back to directory set on line 22.
            os.chdir(cwd)

        # execution of error exceptions.
        except IndexError:
            # trigger error message informing user that 4th commandline argument given was not a valid keyword option.
            ErrorMessages.Main_IndexError()
            # end programme
            sys.exit(1)
        except KeyError:
            # trigger error message informing user that they have not given enough commandline arguments
            ErrorMessages.Main_KeyError(keywrd)
            sys.exit(1)
        except FileNotFoundError as err:
            # trigger error message informing user that
            ErrorMessages.Main_FileNotFoundError(err,i)
            sys.exit(1)

        else:
            # saving directory str given by user for 1st 3 arguments.
            Arguments = Core.UArg(sys.argv[1], sys.argv[2],sys.argv[3])
            if keywrd != 'all':
                # single specific defect subdirectory given as final argument.
                if len(sys.argv) == 6:
                    defect = [sys.argv[5]]
                # multiple specific defect subdirectories given after 5th argument.
                else:
                    defect = []
                    for i in range(5, len(sys.argv)):
                        # creation of list of specific defect subdirectories given by user.
                        defect.append(sys.argv[i])
                if keywrd == 'only':
                    # saving defect subdirectory name(s) & enacting setting for data processing of only subdirs named.
                    Arguments.OnlyStated(defect)
                elif keywrd == 'except':
                    # saving defect subdir name(s) & enacting settings for data processing of all subdirs except named.
                    Arguments.ExceptionStated(defect)
        self.stop = None

        ## multithreading set up

        # to pass information between threads.
        q = queue.Queue()
        # to block simultaneous printing of text from multiple threads.
        lock = th.Lock()

        # printing '-----' across screen while downtime buffer happening in check_users_wants
        # t0 = th.Thread(target=Core.ProcessTakingPlace, args=(lock, 0.25, True, q))

        Core.Directories_Search.finding_(q, lock)
        # finding all os.paths() for directories/subdirectories with CP2K results to be included in programme execution.
        # t1 = th.Thread(target=Core.Directories_Search.finding_, args=(q, lock))
        # t2 = th.Thread(target=self.check_users_wants, args=(q, lock))
        # [x.start() for x in [t0, t1, t2]]

        # if Core.UArg.Only is False:
        #     # self.check_user_wants goes straight through to self.Questions2Ask; '-----' stops printing across screen.
        #     [x.join() for x in [t0, t2]]
        #     # printing message for user and '-----' across screen while thread t1 finishes.
        #     t_ = th.Thread(target=Core.ProcessTakingPlace, args=(lock, 0.05))
        #     t_.start()
        #     # t1 still executing Directories_Search.PopulateResultsHolder() at end of Core.Directories_Search.finding_
        #     [x.join() for x in [t_, t1]]
        # else:
        #     # t1 ended without running Directories_Search.PopulateResultsHolder(); run by sub-thread t3 of t2 instead.
        #     [x.join() for x in [t0, t1, t2]]
        #
        # # when 'only' used & a named directory doesn't exist - q sent item to trigger program to stop & end.
        # if self.stop is True:
        #      sys.exit(1)

        # print("done in",time.time()-t)

    def check_users_wants(self, q, lock):
        """
            Checking conditions are upheld and no error codes are triggered before continuing to ask the user questions.

            Inputs:
                q(queue.Queue) : Shared between this method and method
                                 Core.Directories_Search.finding_ and method
                                 Core.Messages.delay_print (via Core.ProcessTakingPlace)
                                 to allow the passing of information:

                                 1. when Core.UArg.Only is True from
                                    Core.Directories_Search.finding_ to this method and
                                    Core.Messages.delay_print to trigger the printing of '----'
                                    to be stopped, and a FileNotFoundError if certain subdirectories
                                    singled out by user don't exist/calling of self.Questions2Ask.
                                 2. when Core.UArg.Only is False from this method to
                                    Core.Messages.delay_print to trigger the printing of '----' to be
                                    stopped so self.Questions2Ask can be run.

                lock(th.Lock)  : Unowned lock synchronization primitive shared
                                 between threads which when called upon blocks the ability
                                 of any other thread to print until the lock has finished the
                                 printing commands within the current with statement it has
                                 acquired and is released.
        """

        if Core.UArg.Only is True:
            while q.empty() is True:
            # provide buffer downtime for thread in case a given subdirectory for 'only' isn't found & error is flagged.
                time.sleep(0.05)
            while q.empty() is False:
                # when 'only' used & a named directory doesn't exist - q sent item to trigger program to stop & end.
                if q.get() == "sys.exit(1)":
                    self.stop = True
                    return
                else:
                    self.Questions2Ask(lock)
        else:
            # To stop '------' continuing to be printed across screen.
            q.put("pass")
            self.Questions2Ask(lock)

    def Questions2Ask(self, lock):
        """
            Asking the user base questions to gain understanding of how user would like the programme to do.

            Originally a part of check_users_wants, but split off to avoid code repetition while still completing the
            execution of asking the user questions about what they'd like the programme to do, if no errors are
            triggered by the commandline arguments.

            Inputs:
                lock(th.Lock) : Unowned lock synchronization primitive shared
                                between threads which when called upon blocks the ability
                                of any other thread to print until the lock has finished the
                                printing commands within the current with statement it has
                                acquired and is released.
        """

        # Question one
        text = str(Start.questions["Q1"]+"{bcolors.OKBLUE}\nResults options include: {bcolors.OKCYAN}"+
                           ', '.join(Start.options[0:6])+"                              "+
                          ', '.join(Start.options[6:9]))

        # pass text & lock to function to print each line of question slowly when lock is next unreleased & available.
        SlowMessageLines(text, lock)
        # request user input.
        processing = input()

        # test for error in user's input response.
        try:
            for entry in processing.split(', '):
                # if user input string doesn't match an implemented option for processing method, ValueError triggered.
                Start.options.index(entry)
        except ValueError:
            # trigger error informing user that they have given an input which isn't valid once lock is next unreleased.
            ErrorMessages.Main_ValueError1(Start.options, lock)
            # restate question printed slowly when lock is next unreleased.
            SlowMessageLines(Start.questions["Q1"], lock)
            processing = input()

        # turn processing input str into a list.
        if processing.find(','):
            processing = processing.split(', ')
        else:
            processing = [processing]

        # saving users answer for what results they'd like processing.
        t3 = th.Thread(target=Core.ProcessCntrls.SavingOtherWants, args=(processing,))
        t3.start()
        t3.join()

        # Question two
        text = str(Start.questions["Q2"] + "{bcolors.OKBLUE}\nSelecting {bcolors.OKCYAN}'N'{bcolors.OKBLUE} "
                                           "will generate processed_data.txt which will contain data asked to be "
                                           "processed:")
        SlowMessageLines(text, lock)
        analysis = str(input()).upper()

        try:
            # if user has given an input which is not 'Y' or 'N', trigger ValueError.
            if analysis not in ['Y', 'N']:
                raise ValueError
            # if user wants the WFN result processing method, but says 'N' to this question, trigger NotImplementedError
            while "WFN" in processing and 'Y' not in analysis:
                raise NotImplementedError

        except ValueError:
            # trigger error informing user that they have given an input which is invalid once lock is next unreleased.
            ErrorMessages.Main_ValueError2(lock)
            SlowMessageLines(Start.questions["Q2"], lock)
            analysis = str(input()).upper()

        except NotImplementedError:
            # trigger error informing user their answers to Q1 & Q2 are incompatible when lock is next unreleased.
            ErrorMessages.Main_NotImplementedError(lock)
            SlowMessageLines(Start.questions["Q2"], lock)
            analysis = str(input()).upper()

        # Follow-up Questions to Question 2
        if analysis == 'Y':
            text = str(Start.questions["Q2fup1"] + "{bcolors.OKBLUE}\nSelecting {bcolors.OKCYAN}'N'"
                                                   "{bcolors.OKBLUE} will generate png files of analysed "
                                                   "results: ")
            SlowMessageLines(text, lock)
            display = str(input()).upper()

            try:
                if analysis not in ['Y', 'N']:
                    raise ValueError

            except ValueError:
                ErrorMessages.Main_ValueError2(lock)
                SlowMessageLines(Start.questions["Q2fup1"], lock)
                display = str(input()).upper()

            Core.UserWants.appendVoverwrite('N','N')

        elif analysis == 'N':
            text = str("{bcolors.OKBLUE}If processed_data.txt already exists, data processed in this run will"
                       f" be appended to file\n" + Start.questions["Q2fup2"])
            SlowMessageLines(text)
            overwrite = str(input()).upper()

            try:
                if analysis not in ['Y', 'N']:
                    raise ValueError

            except ValueError:
                ErrorMessages.Main_ValueError2(lock)
                SlowMessageLines(Start.questions["Q2fup2"], lock)
                overwrite = str(input()).upper()

            if overwrite == 'Y':
                Core.UserWants.appendVoverwrite('N', 'Y')
            else:
                Core.UserWants.appendVoverwrite('Y', 'N')

            display = 'N'

        # saving users wants for analysing and displaying the data.
        Core.UserWants.Save(analysis, display)


# Entry point of code for multiprocessing.
if __name__ =='__main__':
    # t = time.time()
    Start()
    # print("done in", time.time() - t)

    # limit CPUs available to pool child processes to 2/3 of local machine CPUs - CPUs left for grandchild processes.
    # CPUs2use = int(os.cpu_count() * 2/3)
    # p = PoolNoDaemonProcess(CPUs2use)
    #
    # # conducting a single worker processes while blocking other workers to allow access to important data by the pool.
    # setup = p.apply(resave_.RsvAddrss4mp, [Core.Directories_Search.Address_book,
    #                                        Core.Directories_Search.executables_address,
    #                                        Core.Directories_Search.Dir_Calc_Keys,
    #                                        Core.ProcessCntrls.ProcessResults])
    #
    # # Give each available CPU a process for each selected result processing method - feed ProcessingWants to Rooting.
    # run = p.map(Rooting, Core.ProcessCntrls.ProcessWants)
    # p.close()
    # p.join()

