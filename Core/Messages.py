#!/usr/bin/env python3

#   Messages.py handles all settings for presentation/printing of text to the commandline terminal when
#   CP2KAtomicSimProcessor is run.
#   ----------------------------------------------------------
#   Author: Niamh Smith; E-mail: niamh.smith.17 [at] ucl.ac.uk
#   Date:

import os
import sys
import Core
import time
import threading as th

class bcolors:
    """
        Colours to be used for command line messages and for user inputs upon run of python file.

        Class definitions are each either a Select Graphic Rendition (SGR) or 8-bit Escape (ESC) color mode code.
    """

    HEADER = '\033[95m'
    QUESTION = '\x1b[38;5;135m'
    QUESTION2 = '\x1b[38;5;99m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARN2 = '\x1b[38;5;221m'
    WARN3 = '\033[93m'
    WARN4 = '\033[33m'
    WARNING = '\x1b[38;5;220m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    ITALIC = '\033[3m'
    UNDERLINE = '\033[4m'

class delay_print:
    """
        Delayed horizontal (on same line) printing of the characters within a string.

        Inputs:
            s(str)        : String to be printed character by character.

            lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                            blocks the ability of any other thread to print until the lock has finished the printing
                            commands within the current with statement it has acquired and is released.

            t(float)      : Optional input given if downtime between printing characters needs to be changed from
                            default of 0.024 seconds.
    """

    def __init__(self, s, lock, t = None):
        with lock:
            for c in s:
                sys.stdout.write(c)
                sys.stdout.flush()
                if t:
                    time.sleep(t)
                else:
                    time.sleep(0.024)

class ProcessTakingPlace:
    """
        Printing of buffer user statement and '----'.

        Printing in times of visual downtime (i.e no printing of questions/warnings/errors/results) to indicate that
        the programme is not ideal and processing is taking place.

        Inputs:
            lock(th.Lock)       : Unowned lock synchronization primitive shared between threads which when called upon
                                  blocks the ability of any other thread to print until the lock has finished the
                                  printing commands within the current with statement it has acquired and is released.

            t(float/empty list) : Optional input given if downtime between printing characters needs to be changed from
                                  default of 0.024 seconds.

            miss(None/True)     : Optional input given if the user message should not be printed along with '-----'
                                  when function is called.
    """

    def __init__(self, lock, t, miss = None):
        if not miss:
            text = str("                                      {bcolors.OKBLUE}Thank you. Processing taking place.")
            SlowMessageLines(text, lock)
        text = str(
            f"{bcolors.OKBLUE}----------------------------------------------------------------------------------------"
            f"----------------------{bcolors.ENDC}\n")
        if t:
            t0 = th.Thread(target=Core.delay_print, args=(text, lock, t))
        else:
            t0 = th.Thread(target=Core.delay_print, args=(text, lock))
        t0.start()
        t0.join()

class linewidth:
    """
        To ensure that all printed lines of text are 110 characters long or less.

        Inputs:
            trial(str) : String to be printed.

    """

    def __init__(self, trial):
        # String will contain "{" and "}" around inactive bcolors calls for changing text colour. Characters within
        # these bcolors calls can't be counted as string characters. Split the string into list at "{" instances first.
        trial, j = trial.split("{"), 0

        for item in trial:
            if "}" in item:
                # get index of item in list and split list items in two at the "}" instance.
                indx, new  = trial.index(item), [newitem for newitem in item.split("}")]
                trial.remove(item)  # remove item from list so that it can be replaced by its two halves.
                [trial.insert(indx + idx, n) for idx, n in zip(range(len(new)), new)]  # 1st half of item placed back at
                                                                                       # original index of item, 2nd
                                                                                       # half inserted at index + 1.

        for indx, item in enumerate(trial):
            if "bcolors" not in item and len(item) != 0:  # Don't want to count characters of bcolors calls.
                if "\n" in item:  # pre-inserted newline in string (ie linebreak for providing further context) found
                    j = 0 + len(item)  # reset value of j to zero then add length of characters of item. '\n' are stated
                                       # after changes in text colour so will be at start of the string.
                else:
                    j += len(item)  # add length of character of item to j.
                if j > 110:
                    j, trial = self.trimline(j, trial, item, indx)
                    if j == 110:
                        j = j - 110  #reset j back to 0 if at 110.

            if "bcolors" in item:  # for items which are inactive bcolors calls, replace with active bcolors calls.
                trial.remove(item)
                trial.insert(indx, str("{}".format(eval("{}".format(item)))))

        trial.extend([str("{}".format(eval("{}".format('bcolors.ENDC')))), "\n"])  # add final reset of color & newline
        trial = "".join(trial)
        self.trial = str(trial)

    def trimline(self, j, trial, item, indx):
        """
            trim line down to 110 characters or less.

            Inputs:
                j(int)      : Count of characters on current line after adding the characters of item.

                trial(list) : List of broken up string.

                item(str)   : Particular item of trial.

                indx(int)   : Index of item within the list of trial.
        """
        k, o = 110 - j, [i for i in item]  # k is num of characters j is over 110 by. o is  list of characters in item.
        if o[k] == ' ':  # if character which would be character 110 on the line is a blank space.
            o.insert(k + 1, "\n")  # insert newline after blank space.
        else:
            try:
                while o[k] != ' ':
                    k -= 1  # move back characters from would be character 110 until character is a blank space.
                o.insert(k + 1, "\n")
            except IndexError:  # index error if string is shorter than index stated to be character 110 of the line.
                o.insert(0, "\n")  # insert newline at beginning of string.

        new = "".join(o)  # put broken characters of item back together and replace item in main list
        trial.remove(item)
        trial.insert(indx, new)
        j_ = j + k - 110  # reset j value to be returned based on removing the 110 characters that are now on the
                          # previous line and then adding the characters which are now the length of line.

        return j_, trial

    def Return(self):
        return self.trial

class SlowMessageLines:
    """
        Delayed printing of whole lines of text to commandline terminal.

        Inputs:
            message(str)  : Message to be printed to the commandline terminal.

            lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                            blocks the ability of any other thread to print until the lock has finished the printing
                            commands within the current with statement it has acquired and is released.
    """

    def __init__(self, message, lock = None):
        message_ = linewidth(message).Return()
        lines = message_.splitlines()
        if lock:  # text to be printed is within a multithreading environment.
            with lock:
                self.Print(lines)
        else:  # test to be printed is not within a multithreading environment.
            self.Print(lines)

    def Print(self,lines):
        for line in lines:
            time.sleep(0.75)
            print(f"{line}")

class ErrorMessages:
    """
        All error messages that can be triggered in package.

        Each individual message is given as a staticmethod function,
                                                named as so: {py filename error occurred in}_{type of error occurred}.

        Class definitions
            argv_dict(dict) : Dictionary of partial error message strings related to each commandline argument.
    """
    argv_dict = {"1": f"{bcolors.ITALIC}the name of the {bcolors.WARNING}{bcolors.BOLD}directory{bcolors.ENDC}"
                      f"{bcolors.ITALIC}{bcolors.WARN2} of CP2K output files for the {bcolors.WARNING}{bcolors.BOLD}"
                      f"perfect, defect-free material{bcolors.ENDC}{bcolors.ITALIC}{bcolors.WARN2}.",
                 "2": f"{bcolors.ITALIC}the name of the {bcolors.WARNING}{bcolors.BOLD}parent directory{bcolors.ENDC}"
                      f"{bcolors.ITALIC}{bcolors.WARN2} which holds all subdirectories of each specific defect "
                      f"calculation run for a {bcolors.WARNING}{bcolors.BOLD}particular defect type{bcolors.ENDC}"
                      f"{bcolors.ITALIC}{bcolors.WARN2}",
                 "3": f"{bcolors.ITALIC}the name of the {bcolors.WARNING}{bcolors.BOLD}parent directory{bcolors.ENDC}"
                      f"{bcolors.ITALIC}{bcolors.WARN2} which holds all subdirectories of individual reference "
                      f"{bcolors.WARNING}{bcolors.BOLD}chemical potentials{bcolors.ENDC}{bcolors.ITALIC}{bcolors.WARN2}"
                      f" for host and impurity atoms "}

    def __init__(self, f):
        self._f= f

    @staticmethod
    def Main_IndexError():
        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}Wrong number of arguments!{bcolors.ENDC}"
                   "{bcolors.WARN3} \nValid usage includes:{bcolors.WARNING}{bcolors.ITALIC} \n./MAIN.py "
                   "perf_mat_dir_str defect_parent_dir_str chem_pot_dir_str all \n./MAIN.py perf_mat_dir_str "
                   "defect_parent_dir_str chem_pot_dir_str only str_of_defect_subdir \n./MAIN.py perf_mat_subdir_str "
                   "defect_parent_dir_str chem_pot_dir_str except str_of_defect_subdir")
        SlowMessageLines(text)

    @staticmethod
    def Main_KeyError(keywrd):
        """
            Inputs:
                keywrd(str) : user given commandline argument four
        """
        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}Invalid keyword {bcolors.BOLD}{bcolors.HEADER}'"
                   +f"{keywrd}"+"'{bcolors.ENDC}{bcolors.FAIL}{bcolors.UNDERLINE} given!{bcolors.ENDC}"
                                "{bcolors.WARN3} \nValid keywords for argument four are:  '{bcolors.WARNING}"
                                "{bcolors.ITALIC}all{bcolors.WARN3}' / '{bcolors.WARNING}except{bcolors.WARN3}' / "
                                "'{bcolors.WARNING}only{bcolors.WARN3}'.")
        SlowMessageLines(text)

    @staticmethod
    def Main_FileNotFoundError(err,i):
        """
            Inputs:
                err(error code) : Error code returned when one of the named directories in commandline arguments 1-3.

                i(int)          : Number of the argument which triggered the error code.
        """
        path, cwd = (str(err).split(' ')[-1]).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])
        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}"+f"{' '.join(str(err).split(' ')[:-1])}"
                   +"{bcolors.ENDC} {bcolors.HEADER}"+f"{dirpath}"+"{bcolors.FAIL}.{bcolors.WARNING} \nArgument "+f"{i}"
                   +" {bcolors.WARN2}should be "+f"{ErrorMessages.argv_dict[str(i)]}"+" {bcolors.ENDC}"
                                                                                      "{bcolors.WARN3}\n"
                   +"Spaces or dashes within a directories name are not permitted. Rename directory to remove "
                    "spaces/dashes if present in name before rerunning.")
        SlowMessageLines(text)

    @staticmethod
    def Main_ValueError1(options, lock):
        """
            Inputs:
                options(list) : List of the methods of data processing the user can choose from.

                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}Invalid results type given!{bcolors.ENDC}"
                   "{bcolors.WARNING} \nValid methods implemented are:{bcolors.OKCYAN}{bcolors.ITALIC} \n"
                   +f"{', '.join(options)}"+"{bcolors.ENDC}{bcolors.WARN3} \nPlease use commas to separate the names of"
                                            " each method within your answer.")
        SlowMessageLines(text, lock)

    @staticmethod
    def Main_ValueError2(lock):
        """
            Inputs:
                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        text = str("\n{bcolors.FAIL}WARNING:{bcolors.UNDERLINE}Invalid answer given!{bcolors.ENDC}{bcolors.WARN3} "
                   "\nTry again. Only valid answers are {bcolors.OKCYAN}Y {bcolors.WARN3}and {bcolors.OKCYAN}N"
                   "{bcolors.WARN3}. ")
        SlowMessageLines(text, lock)

    @staticmethod
    def Main_NotImplementedError(lock):
        """
            Inputs:
                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}Results asked to be processed include 'WFN'. "
                   "{bcolors.ENDC}{bcolors.WARN3} \nWFN results can not be displayed in a csv file. \nIf you do not "
                   "wish for analysis to be performed on the other results asked for please press {bcolors.OKCYAN}"
                   "{bcolors.ITALIC}Crt+C{bcolors.ENDC}{bcolors.WARN3} now. Otherwise press {bcolors.OKCYAN}Y"
                   "{bcolors.WARN3}.")
        SlowMessageLines(text, lock)

    @staticmethod
    def Main_TypeError(err, lock):
        """
            Inputs:
                err(error code) : Error code of TypeError which has been triggered.

                lock(th.Lock)   : Unowned lock synchronization primitive shared between threads which when called upon
                                  blocks the ability of any other thread to print until the lock has finished the
                                  printing commands within the current with statement it has acquired and is released.
        """
        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}"+f"{err}"+"{bcolors.ENDC}")
        SlowMessageLines(text, lock)

    @staticmethod
    def FileExtension_FileNotFoundError1(key, lock):
        """
            Inputs:
                key(str)      : Name of subdirectory listed after 'only' by user in commandline arguments which cannot
                                be found within parent directory.

                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        path, cwd = str(Core.UArg.DefD).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])
        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}[Errno 2] No subdirectory {bcolors.BOLD}{bcolors.HEADER}"
                   "'"+f"{key}"+"'{bcolors.ENDC}{bcolors.FAIL}{bcolors.UNDERLINE} found in parent directory:"
                                "{bcolors.ENDC} {bcolors.HEADER}'"+f"{dirpath}"+"'{bcolors.FAIL}.{bcolors.WARN2}\n"
                   +"Use of key word '{bcolors.WARNING}{bcolors.ITALIC}{bcolors.BOLD}only{bcolors.ENDC}"
                    "{bcolors.WARN2}' requires all arguments given after '{bcolors.WARNING}{bcolors.ITALIC}"
                    "{bcolors.BOLD}only{bcolors.ENDC}{bcolors.WARN2}' to be names of subdirectories within the "
                    "{bcolors.HEADER}{bcolors.ITALIC}"+f"{Core.UArg.DefD.split('/')[-1]}"+"{bcolors.ENDC}"
                      "{bcolors.WARN2} parent directory. {bcolors.ENDC}{bcolors.WARN3} \nSpaces or dashes within a "
                   "directories name are not permitted. Rename directory to remove spaces/dashes if present in name(s) "
                   "before rerunning.")
        SlowMessageLines(text, lock)

    @staticmethod
    def FileExtension_FileNotFoundError2(key, lock):
        """
            Inputs:
                key(str)      : Name of subdirectory listed after 'only' by user in commandline arguments which cannot
                                be found within parent directory.

                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        path, cwd = str(Core.UArg.DefD).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])
        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2] No subdirectory {bcolors.BOLD}{bcolors.HEADER}"
                   "'"+f"{key}"+"'{bcolors.ENDC}{bcolors.FAIL}{bcolors.UNDERLINE} found in parent directory:"
                                "{bcolors.ENDC} {bcolors.HEADER}'"+f"{dirpath}"+"'{bcolors.FAIL}.{bcolors.WARN2}\n"
                   +"Use of key word '{bcolors.WARNING}{bcolors.ITALIC}{bcolors.BOLD}only{bcolors.ENDC}{bcolors.WARN2}"
                    "' requires all arguments given after '{bcolors.WARNING}{bcolors.ITALIC}{bcolors.BOLD}only"
                    "{bcolors.ENDC}{bcolors.WARN2}' to be names of subdirectories within the {bcolors.HEADER}"
                    "{bcolors.ITALIC}"+f"{Core.UArg.DefD.split('/')[-1]}"+"{bcolors.ENDC}{bcolors.WARN2} parent "
                                                                          "directory. {bcolors.ENDC}{bcolors.WARN3}\n"
                   +"Spaces or dashes within a directories name are not permitted. Rename directory to remove "
                    "spaces/dashes if present in name before rerunning with corrected name for{bcolors.BOLD}"
                    "{bcolors.HEADER}'"+f"{key}"+"{bcolors.ENDC}{bcolors.WARN3} subdirectory.")
        SlowMessageLines(text, lock)

    @staticmethod
    def FileExtension_FileNotFoundError3(keywrd, name, run, charge, filetypes, lock):
        """
            Inputs:
                keywrd(str)   : Keyword which corresponds to the result processing method that the input 'result'
                                is the processed outcome of.

                name(str)     : Nested dict item key of project name of the particular defect geometry/placement/
                                impurity inclusion.

                run(str)      : Nested dict item key of runtype of the calculation of the particular defect geometry/
                                placement/impurity inclusion.

                chrg(int)     : Nested dict item key of charge state of the calculation of the particular defect
                                geometry/placement/impurity inclusion.

                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        print("\n")
        for fltyp in filetypes:
            text = str("{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2]{bcolors.ENDC}{bcolors.FAIL} CP2K output "
                       "file type {bcolors.BOLD}{bcolors.HEADER}'"+f"{fltyp}"+"'{bcolors.ENDC}{bcolors.FAIL} needed for"
                                                                              " the {bcolors.OKGREEN}"+f"{keywrd}"+
                       " processing{bcolors.ENDC}{bcolors.FAIL} method could not be found in the {bcolors.HEADER}"
                       +f"{run}"+"{bcolors.ENDC}{bcolors.FAIL} directory for the {bcolors.HEADER}"+f"{charge}"+
                       "{bcolors.ENDC}{bcolors.FAIL} charge state of {bcolors.HEADER}"+f"{name}"+
                       "{bcolors.ENDC}{bcolors.FAIL}.")
            SlowMessageLines(text, lock)

        text = str("{bcolors.WARN3}Processing for the {bcolors.OKGREEN}"+f"{keywrd}"+"{bcolors.ENDC}{bcolors.WARN3} "
                                                                                     "method will continue for found "
                                                                                     "subdirectories which contain all "
                                                                                     "required filetypes for the "
                                                                                     "method.")
        SlowMessageLines(text, lock)

    @staticmethod
    def FileExtension_FileNotFoundError4ChargesAndSpinsOnly(extension, path, lock):
        """
            Inputs:
                extension(str) : File extensions of file needed for completion of the result process method of charges
                                 and spins for only atoms related to the defect.

                path(os.path)  : File path of the directory in which file with extension was being searched for.

                lock(th.Lock)  : Unowned lock synchronization primitive shared between threads which when called upon
                                 blocks the ability of any other thread to print until the lock has finished the printing
                                 commands within the current with statement it has acquired and is released.
        """
        path, cwd = str(path).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])

        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2]{bcolors.ENDC}{bcolors.FAIL} Needed "
                   "{bcolors.HEADER}'"+f"{extension}"+"'{bcolors.ENDC}{bcolors.FAIL} file for processing "
                                                      "{bcolors.OKGREEN}charges and spins data for only atoms related to "
                                                      "{bcolors.ENDC}{bcolors.FAIL}defect{bcolors.ENDC}{bcolors.HEADER}"
                                                      " could not be found in directory for:"+f"{dirpath}"+"{bcolors.FAIL}."
                                                      "{bcolors.WARN3} \n"
                                                      "Subsequently, {bcolors.OKGREEN}charges and spins{bcolors.ENDC}"
                                                      "{bcolors.WARN3} will be processed for all atoms within the "
                                                      "simulation held by directory{bcolors.HEADER}"+f"{dirpath}"+
                                                      "{bcolors.WARN3}")
        SlowMessageLines(text, lock)

    @staticmethod
    def FileExtension_ConnectionAbortedError(path, lock):
        """
            Inputs:
                path(os.path) : File path of the directory in which file was being searched for.

                lock(th.Lock) : Unowned lock synchronization primitive shared between threads which when called upon
                                blocks the ability of any other thread to print until the lock has finished the printing
                                commands within the current with statement it has acquired and is released.
        """
        path, cwd = str(path).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])
        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2]{bcolors.ENDC}{bcolors.FAIL} Needed "
                   "{bcolors.HEADER}'-ELECTRON_DENSITY-1_0.cube'{bcolors.ENDC}{bcolors.FAIL} file for {bcolors.OKGREEN}"
                   "analysis of Bader charges of atoms{bcolors.ENDC}{bcolors.FAIL} could not be found within the "
                   "given directory for perfect, defect-free material CP2K output files:{bcolors.HEADER} "+f"{dirpath}"
                   +"{bcolors.WARN3} \nSubsequently, {bcolors.OKGREEN}Bader charge analysis{bcolors.WARN3}"
                    " cannot be completed at all for results. {bcolors.OKGREEN}Mulliken and Hirshfeld analysis"
                    "{bcolors.WARN3} will, however, still be performed for all results found.")
        SlowMessageLines(text, lock)

    @staticmethod
    def ProcessingChargesSpins_FileNotFoundError(DirsMissingBader, lock):
        """
            Inputs:
                DirsMissingBader(list) : List of file paths of the directory in which file was being searched for.

                lock(th.Lock)          : Unowned lock synchronization primitive shared between threads which when called
                                         upon blocks the ability of any other thread to print until the lock has
                                         finished the printing commands within the current with statement it has
                                         acquired and is released.
        """
        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2]{bcolors.ENDC}{bcolors.FAIL} Needed "
                   "{bcolors.HEADER}'-ELECTRON_DENSITY-1_0.cube'{bcolors.ENDC}{bcolors.FAIL} file for {bcolors.OKGREEN}"
                   "analysis of Bader charges of atoms{bcolors.ENDC}{bcolors.FAIL} could not be found within the "
                   "following directories for:")
        SlowMessageLines(text, lock)

        time.sleep(1)
        for dir in DirsMissingBader:
            text = str("{bcolors.HEADER}- "+f"{dir}"+"{bcolors.ENDC}")
            SlowMessageLines(text, lock)


