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
            s(str)         : String to be printed character by character.

            lock(th.Lock)  : Unowned lock synchronization primitive shared between threads which when called upon
                             blocks the ability of any other thread to print until the lock has finished the printing
                             commands within the current with statement it has acquired and is released.

            t(float)       : Optional. Input given if downtime between printing characters needs to be changed from
                             default of 0.024 seconds.

            q(queue.Queue) : Optional. Included if information from another thread needs to be passed to this function
                             in order to disrupt printing of str characters one by one while waiting for other threads
                             are being executed.
    """

    def __init__(self, s, lock, t = None, q = None):
        count = 0
        if q:
            while q.empty() is True:
                if count > 0:
                    # wait the time of printing 1/2 a line of characters before printing next line.
                    time.sleep(11)
                with lock:
                    self.printer(s, t)
                    # wait for update on queue.
                    time.sleep(0.3)
                    # increase number of count to indicate how many times this while loop has been enacted.
                    count += 1

            while q.empty() is False:
                # queue may not stay empty, need to trigger class end. sys.exit() won't work here...
                # sys.exit()
                # change value of count from int to str for str to be picked up by following if statement.
                count = "exit"

            if count == "exit":
                # change q so that it is no longer a queue.Queue()
                q = None
                # exit class and thread.
                sys.exit()
        else:
            with lock:
                self.printer(s, t)

    def printer(self, s, t = None):
        """
            code for actually printing each letter of the string one by one. Separated from __init__ to avoid repetition.
        """
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

            miss(None/True)     : Optional. Input given if the user message should not be printed along with '-----'
                                  when function is called.

            q(queue.Queue)      : Optional. Included if information from another thread needs to be passed to the
                                  Core.delay_print function in order to disrupt printing of str characters one by one
                                  while waiting for other threads are being executed.
    """

    def __init__(self, lock, t, miss = None, q = None):
        if not miss:
            # print user message.
            text = str("                                      {bcolors.OKBLUE}Thank you. Processing taking place.")
            SlowMessageLines(text, lock)
        text = str(
            f"{bcolors.OKBLUE}----------------------------------------------------------------------------------------"
            f"----------------------{bcolors.ENDC}\n")
        if q:
            t0 = th.Thread(target=Core.delay_print, args=(text, lock, t, q))
        elif t and not q:
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
        # Split string into list at "{" instances.
        trial, j = trial.split("{"), 0

        for item in trial:
            if "}" in item:
                # get index of item in list and split list items in two at the "}" instance.
                indx, new  = trial.index(item), [newitem for newitem in item.split("}")]
                # remove item from list so that it can be replaced by its two halves.
                trial.remove(item)
                # 1st half of item placed back at original index of item, 2nd half inserted at index + 1.
                [trial.insert(indx + idx, n) for idx, n in zip(range(len(new)), new)]

        for indx, item in enumerate(trial):
            # Don't want to count characters of bcolors calls.
            if "bcolors" not in item and len(item) != 0:
                # pre-inserted newline in string (ie linebreak for providing further context) found
                if "\n" in item:
                    # reset j to 0, add item characters length. '\n' stated after txt color change at start of str.
                    j = 0 + len(item)
                else:
                    # add length of character of item to j.
                    j += len(item)
                if j > 110:
                    j, trial = self.trimline(j, trial, item, indx)
                    if j == 110:
                        # reset j back to 0 if at 110.
                        j = j - 110

            # inactive bcolors (txt color) calls. Characters in these not to be counted as str characters.
            if "bcolors" in item:
                # remove inactive bcolors calls
                trial.remove(item)
                # replace with active bcolors calls.
                trial.insert(indx, str("{}".format(eval("{}".format(item)))))

        # add final reset of color & newline
        trial.extend([str("{}".format(eval("{}".format('bcolors.ENDC')))), "\n"])
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

        # k is num of characters j is over 110 by. o is  list of characters in item.
        k, o = 110 - j, [i for i in item]
        # if character which would be character 110 on the line is a blank space.
        if o[k] == ' ':
            # insert newline after blank space.
            o.insert(k + 1, "\n")
        else:
            try:
                while o[k] != ' ':
                    # move back characters from would be character 110 until character is a blank space.
                    k -= 1
                o.insert(k + 1, "\n")
            # index error if string is shorter than index stated to be character 110 of the line.
            except IndexError:
                # insert newline at beginning of string.
                o.insert(0, "\n")

        # put broken characters of item back together and replace item in main list
        new = "".join(o)
        trial.remove(item)
        trial.insert(indx, new)
        # return j value to account for removing 110 characters now on previous line, add characters now on current line.
        j_ = j + k - 110

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
        # text to be printed is within a multithreading environment.
        if lock:
            with lock:
                self.Print(lines)
        # test to be printed is not within a multithreading environment.
        else:
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
        # pass text to function to print each line of error slowly when lock is next unreleased & available.
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
        # pass text to function to print each line of error slowly when lock is next unreleased & available.
        SlowMessageLines(text)

    @staticmethod
    def Main_FileNotFoundError(err,i):
        """
            Inputs:
                err(error code) : Error code returned when one of the named directories in commandline arguments 1-3.

                i(int)          : Number of the argument which triggered the error code.
        """

        # Don't want to display full file path from / - only directories beyond the set sudo current working directory
        path, cwd = (str(err).split(' ')[-1]).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])

        text = str("\n{bcolors.FAIL}ERROR: {bcolors.UNDERLINE}"+f"{' '.join(str(err).split(' ')[:-1])}"
                   +"{bcolors.ENDC} {bcolors.HEADER}"+f"{dirpath}"+"{bcolors.FAIL}.{bcolors.WARNING} \nArgument "+f"{i}"
                   +" {bcolors.WARN2}should be "+f"{ErrorMessages.argv_dict[str(i)]}"+" {bcolors.ENDC}"
                                                                                      "{bcolors.WARN3}\n"
                   +"Spaces or dashes within a directories name are not permitted. Rename directory to remove "
                    "spaces/dashes if present in name before rerunning.")
        # pass text to function to print each line of error slowly when lock is next unreleased & available.
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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

        # Don't want to display full file path from / - only directories beyond the set sudo current working directory
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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

        # Don't want to display full file path from / - only directories beyond the set sudo current working directory
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
                    "spaces/dashes if present in name before rerunning with corrected name for {bcolors.BOLD}"
                    "{bcolors.HEADER}'"+f"{key}"+"'{bcolors.ENDC}{bcolors.WARN3} subdirectory.")
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
        SlowMessageLines(text, lock)

    @staticmethod
    def FileExtension_FileNotFoundError3(keywrd, name, run, charge, filetypes, lock):
        """
            Inputs:
                keywrd(str)   : Keyword which corresponds to the result processing method that FileNotFoundError has
                                been flagged for.

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

        # want message to be displayed for each of the files within the filetypes list.
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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

        # Don't want to display full file path from / - only directories beyond the set sudo current working directory
        path, cwd = str(path).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])

        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2]{bcolors.ENDC}{bcolors.FAIL} Needed "
                   "{bcolors.HEADER}'"+f"{extension}"+"'{bcolors.ENDC}{bcolors.FAIL} file for processing "
                                                      "{bcolors.OKGREEN}charges and spins data for only atoms related to "
                                                      "defect{bcolors.ENDC}{bcolors.FAIL} could not be found in directory"
                                                      " for:{bcolors.ENDC}{bcolors.HEADER} "+f"{dirpath}"+"{bcolors.FAIL}."
                                                      "{bcolors.WARN3} \n"
                                                      "Subsequently, {bcolors.OKGREEN}charges and spins{bcolors.ENDC}"
                                                      "{bcolors.WARN3} will be processed for all atoms within the "
                                                      "simulation held by directory{bcolors.HEADER}"+f"{dirpath}"+
                                                      "{bcolors.WARN3}")
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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

        # Don't want to display full file path from / - only directories beyond the set sudo current working directory
        path, cwd = str(path).split('/'), str(os.getcwd()).split('/')
        dirpath = '/'.join([directory for directory in path if directory not in cwd])

        text = str("\n{bcolors.FAIL}WARNING: {bcolors.UNDERLINE}[Errno 2]{bcolors.ENDC}{bcolors.FAIL} Needed "
                   "{bcolors.HEADER}'-ELECTRON_DENSITY-1_0.cube'{bcolors.ENDC}{bcolors.FAIL} file for {bcolors.OKGREEN}"
                   "analysis of Bader charges of atoms{bcolors.ENDC}{bcolors.FAIL} could not be found within the "
                   "given directory for perfect, defect-free material CP2K output files:{bcolors.HEADER} "+f"{dirpath}"
                   +"{bcolors.WARN3} \nSubsequently, {bcolors.OKGREEN}Bader charge analysis{bcolors.WARN3}"
                    " cannot be completed at all for results. {bcolors.OKGREEN}Mulliken and Hirshfeld analysis"
                    "{bcolors.WARN3} will, however, still be performed for all results found.")
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
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
        # pass text & lock to function to print each line of error slowly when lock is next unreleased & available.
        SlowMessageLines(text, lock)

        time.sleep(1)

        # want to print each of the strs held in list DirsMissingBader each on a separate line, one by one.
        for dir in DirsMissingBader:
            text = str("{bcolors.HEADER}- "+f"{dir}"+"{bcolors.ENDC}")
            # pass text & lock to function to print slowly when lock is next unreleased & available.
            SlowMessageLines(text, lock)


