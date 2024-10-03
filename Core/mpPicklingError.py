#!/usr/bin/env python3

import multiprocessing as mp
import multiprocessing.pool
import Core
import json
import DataProcessing


class ProcessNoDaemonProcess(mp.Process):
    """
        Modified version of mp.Process specific for this package to make mp.Pool() non-daemonic child processes.

        Daemon attributes will always be turned as False.

        Inheritance:
            mp.Process(class) : Processes spawned by creating a Process
                                object. Process objects represent activity that is run in
                                a separate process. Equivalents of all the methods of
                                threading.Thread.
    """

    @property
    def daemon(self):
        """
            Overriding property of parent. Process’s daemon flag, a Boolean value. Return whether process is a daemon.

            Change initial value inherited from the creating process to False.
        """
        return False

    @daemon.setter
    def daemon(self, value):
        """
            Overriding property setter of parent. Set whether process is a daemon.

            Process’s daemon flag must be set before start() in mp.Process is called.

            Input:
                value(daemonic) : Sets self._config['daemon'] in mp.Process.
        """
        pass


class PoolNoDaemonProcess(mp.pool.Pool):
    """
        Modified version of mp.pool.Pool specific for this package for mp.Pool() non-daemonic workers.

        Inheritance:
            mp.pool.Pool(class) : Supports an async version of applying functions to arguments.
    """

    def Process(self, *args, **kwargs):
        """
            PoolNoDaemonProcess subclass method inheriting mp.pool.Pool superclass method of same name.

            Inputs:
                *arg:
                **kwargs:
        """

        # call to inherited mp.pool.Pool superclass method, staticmethod Process.
        proc = super().Process(*args,**kwargs) # PoolNoDaemonProcess, self
        # declaring call method of proc as class ProcessNoDaemonProcess.
        proc.__class__ = ProcessNoDaemonProcess

        return proc


class Rooting:
    """
        Rooting of mp.Pool() child process to specific code stem for wanted result processing method of child process.

        Wanted entry point function is determined via evaluation and execution of the item value str corresponding to
        the item key str within optdict which matches the input str value of the child worker process.

        Class definitions:
            optdict(dict) : Dictionary of specific entry point functions for each
                            implemented result processing method.

        Inputs:
            want(str)     : str assigned to specific mp.Pool() child process accessing
                            class which equates to the specific result processing
                            method assigned to the child worker process out of the
                            result processing methods chosen by user.
    """

    optdict= {"band structure": None,
              "charges and spins": "DataProcessing.CntrlChrgSpns",
              "charge transition levels": None, #DataProcessing.CTLsetup()
              "geometry": None, #"Presentation.geometryGUI",
              "IPR": None,
              "PDOS": None, # "GraphicAnalysis.plotpdos",
              "WFN": None, # "Presentation.WFNGUI",
              "work function": None,
              "test": None}

    def __init__(self, want):
        run = eval(str("{}()".format(Rooting.optdict.get(want))))


class resave_:
    """
        Ensuring established data collected from user inputs is accessible within the shared memory of the mp.Pool().

        Memory saved or created outside a mp.Pool() cannot be accessed within the mp.Pool() environment. Therefore, all
        class definition dictionaries which have been populated or updated since the user executed the commandline
        argument calling this script will be reset to their defaults upon starting to run the mp.Pool(). As this
        function is accessed from within the mp.Pool(), important class definition dictionaries can be re-saved back
        into their same class definitions within the mp.Pool().

        Inputs:
            Address_Book(dict)  : Outside mp.Pool() version of populated
                                  dictionary, Core.Directories_Search.Address_book, of
                                  os.path strs for needed perfect and defect structure CP2K
                                  output files and subdirectories for results processing.

            exectables(os.path) : Outside mp.Pool() version of saved file os.path,
                                  Core.Directories_Search.executables_address, for
                                  the 'Executables' directory within the
                                  CP2KAtomicSimProcessor package.

            CalcKeys(dict)      : Outside mp.Pool() version of populated dictionary,
                                  Core.Directories_Search.Dir_Calc_Keys, of list items of
                                  nested dictionary keys within the
                                  Core.Directories_Search.Address_book/
                                  Core.ProcessingControls.Processing_Results
                                  dictionaries for easier iterations through each specific calculation.

            Results(dict)       : Outside mp.Pool() version of half-populated
                                  dictionary, Core.ProcessingControls.Processing_Results,
                                  of specific calculations to be further populated with
                                  the fully calculated products of user wanted result processing
                                  methods.
    """

    def __init__(self, f):
        self._f = f

    @staticmethod
    def RsvAddrss4mp(Address_Book, exectables, CalcKeys, Results):

        print(json.dumps(Address_Book, indent=1))

        Core.Directories_Search.Address_book = Address_Book
        Core.Directories_Search.executables_address = exectables
        Core.Directories_Search.Dir_Calc_Keys = CalcKeys
        Core.ProcessCntrls.ProcessResults = Results
