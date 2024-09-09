#!/usr/bin/env python3

import numpy as np
import multiprocessing as mp

def find_a(line, index, lines, i, result):
    """
        Extracting lattice parameters of calculation cell.

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            index(int)                         : Number which signifies line number from bottom
                                                 of log file that "locate" str has been found to
                                                 be contained in.

            lines(list of str)                 : All lines found within the log file via
                                                 log.readlines() in __init__ of FromFile.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    strg1 = line  # line with a lattice vector and length of material cell used within calc.
    strg2 = lines[index]  # self.lines[self.index] is fileline below line; holds b latt. vec. & length.
    strg3 = lines[index + 1]  # c latt. vec. & length.
    collect1 = []
    for s, item, letter in zip([1, 2, 3], ['a', 'b', 'c'], ['A', 'B', 'C']):
        exec(f'*{letter}, {item}Latt= [float(var[1]) for var in enumerate(strg{s}.split()) if var[0] in '
             f'[4,5,6,9]]')  # data extraction of text indexed from list when line(s) is split via delimiter
                             # white space. {letter} is lattice constant length, {item}Latt is lattice vector.
        exec(f'collect1.extend([{letter}, {item}Latt])')
    result[i] = collect1

def find_at(index, lines, i, result):
    """
        Extracting details of atomic coordinates and identities.

        Inputs:
            index(int)                         : Number which signifies line number from bottom
                                                 of log file that "locate" str has been found to
                                                 be contained in.

            lines(list of str)                 : All lines found within the log file via
                                                 log.readlines() in __init__ of FromFile.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    X, Y, Z, ELEMENT, MASS = [], [], [], [], []
    max = [int(var[1]) for var in enumerate(lines[index - 20].split()) if var[0] in [3]][0]
    try:
        element = [var[1] for var in enumerate(lines[index + 2].split()) if var[0] in [2]]
        n = 2
    except ValueError:
        element = [var[1] for var in enumerate(lines[index + 3].split()) if var[0] in [2]]
        n = 3
    finally:
        for p in range(0, max):
            element, x, y, z, mass = [var[1] for var in enumerate(lines[index + n + p].split()) if
                                      var[0] in [2, 4, 5, 6, 8]]  # extraction of text in indices 2,4-6,8 in list of
                                                                  # line(s) split by delimiter white space. For atom
                                                                  # p, element is the element type of the atom, x/y/
                                                                  # z is the atom's x-/y-/z-coordinate, mass is the
                                                                  # atom's atomic mass.
            for f, F in zip([float(x), float(y), float(z), element, mass], [X, Y, Z, ELEMENT, MASS]):
                F.append(f)  # saving extracted data within predefined lists.
    array = np.array([X, Y, Z])
    result[i] = [array]

def find_charge(line, i, result):
    """
        Extracting charge state of calculation

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    C = [int(var[1]) for var in enumerate(line.split()) if var[0] in [2]][0]
    if C < 0:
        C = "".join(["".join([i for i in list(str(C)) if i != '-']),'-'])
    elif C == 0:
        pass
    else:
        C = "".join([str(C),"+"])
    result[i] = [C]

def find_energy(line, i, result):
    """
        Extracting total energy of calculation.

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    E = [(round(float(var[1]), 10) * 27.211) for var in enumerate(line.split()) if var[0] in [8]][0]  # total energy
                                                                                                      # converted from
                                                                                                      # hartree units
                                                                                                      # to eV.
    result[i] = [E]

def find_gap(line, index, lines, i, result):
    """
        Extraction of details about band gap of calculation.

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            index(int)                         : Number which signifies line number from bottom
                                                 of log file that "locate" str has been found to
                                                 be contained in.

            lines(list of str)                 : All lines found within the log file via
                                                 log.readlines() in __init__ of FromFile.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    strg2 = line  # beta gap
    strg1 = lines[index - 2]  # alpha gap
    collect2 = []
    for spin, s in zip(["alpha", "beta"], [1, 2]):
        exec(f'{spin}_HOMO_LUMOgap = [float(var[1]) for var in enumerate(strg{s}.split()) if var[0] in[6]][0]')  # in eV.
        exec(f'collect2.append({spin}_HOMO_LUMOgap)')
    result[i] = collect2

def find_kind(lines, i, result):
    """
        Extracting details about each atomic kind in calculation.

        Inputs:
            line(list of str)                  : lines of log file that "locate" str for variable
                                                 has been found to be contained in.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    collect3 = []
    for line in lines:
        kind_ele, num_atoms = [var[1] for var in enumerate(line.split())
                               if var[0] in [3, 7]]  # extraction of txt in indices 3, 7 in list of line split
                                                     # via delimiter white space. kind_ele is name of particular
                                                     # kind, num_atoms is the number of atoms of kind in
                                                     # calculation.
        collect3.extend([kind_ele, num_atoms])
    result[i] = collect3

def find_name(line, i, result):
    """
        Extracting project name of calculation.

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    N = [str(var[1]) for var in enumerate(line.split()) if var[0] in [3]][0]  # extraction of txt in index 3 in list of
                                                                              # line split via delimiter white space. N
                                                                              # is the project name of calculation.
    result[i] = [N]

def find_pop1(atoms, index, lines, i, result):
    """
        Extraction of details related to Mulliken Population Analysis of all or only certain atoms within calculation.

        Inputs:
            atoms(list/int)                    : If int, tot number of atoms in calculation. If
                                                 list, list of specific atom indices to only get
                                                 details for.

            index(int)                         : Number which signifies line number from bottom
                                                 of log file that "locate" str has been found to
                                                 be contained in.

            lines(list of str)                 : All lines found within the log file via
                                                 log.readlines() in __init__ of FromFile.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    collect = []
    rnge = atoms if type(atoms) == list else range(0,atoms)
    for A in rnge:  # A of specific atomm indices or from 0 to total number of atoms in system.
        p1_a, p1_b, p1_c, p1_s = [round(float(var[1]),3) for var in enumerate(lines[int(index + 2 + A)].split())
                                  if var[0] in [3, 4, 5, 6]]  # extraction of txt in indices 3-6 in list of line
                                                              # split by delimiter white space. p1_a & p1_b are
                                                              # alpha & beta spin populations, p1_s & p1_c are
                                                              # atom spin & charge for Mulliken analysis.
        collect.append([p1_a, p1_b, p1_c, p1_s])
    result[i] = collect

def find_pop2(atoms, index, lines, i, result):
    """
        Extraction of details related to Hirshfeld Population Analysis of all or only certain atoms within calculation.

        Inputs:
            atoms(list/int)                    : If int, tot number of atoms in calculation. If
                                                 list, list of specific atom indices to only get
                                                 details for.

            index(int)                         : Number which signifies line number from bottom
                                                 of log file that "locate" str has been found to
                                                 be contained in.

            lines(list of str)                 : All lines found within the log file via
                                                 log.readlines() in __init__ of FromFile.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    collect = []
    rnge = atoms if type(atoms) == list else range(0, atoms)
    for A in rnge:  # A of specific atomm indices or from 0 to total number of atoms in system.
        p2_a, p2_b, p2_s, p2_c = [round(float(var[1]),3) for var in enumerate(lines[int(index + 2 + A)].split())
                                  if var[0] in [4, 5, 6, 7]]  # extraction of txt in indices 4-7 in list of line
                                                              # split by delimiter white space. p2_a & p2_b are
                                                              # alpha & beta spin populations, p2_s & p2_c are
                                                              # atom spin & charge for Hirshfeld analysis.
        collect.append([p2_a, p2_b, p2_c, p2_s])
    result[i] = collect

def find_run(line, i, result):
    """
        Extracting run type of calculation.

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    R = [str(var[1]) for var in enumerate(line.split()) if var[0] in [3]][0]  # extraction of txt in index 3 in list of
                                                                              # line split via delimiter white space. R
                                                                              # is the calculation run type.
    result[i] = [R]

def find_version(line, i, result):
    """
        Extracting CP2K version calculation was run with.

        Inputs:
            line(str)                          : line of log file that "locate" str for variable
                                                 has been found to be contained in.

            i(int)                             : Index of list proxy within result (see below)
                                                 to be replaced by list of variable details
                                                 extracted within this function.

            result(list proxy of list proxies) : Collector of result details extracted for each
                                                 variable type.
    """

    V = [float(var[1]) for var in enumerate(line.split()) if var[0] in [5]][0]  # extraction of txt in index 5 in list
                                                                                # of line split via delimiter white
                                                                                # space. V is CP2K version calculation
                                                                                # performed with.
    result[i] = [V]

class FromLog:
    """
        Extracting data from log files

        Definitions:
            want(dict)             : Dictionary of specific variables that need to be extracted from
                                     the log file [Input os.path (see below)] for each particular
                                     result processing method the user may choose to perform.
            var_fo(dict)           : Dictionary of variable information [var_fo] for each variable
                                     type which can be extracted from a log file. Each variable has a
                                     nested dictionary containing keys:
                                        "locate"(str)        : String pattern associated with variable which can be
                                                               searched for within the log file to extract details about
                                                               the variable.
                                        "via"(str)           : Name of associated function in class [without ()]
                                                               which holds code for detailing how exactly to extract the
                                                               correct information from the log file for the variable.
                                        "found"(False/None)  : Indication of whether, or not, the string
                                                               item value for "locate" has been found within the log
                                                               file. Value will be None if string has been found.
                                        "reset"(None/List)   : Record of additional keys and their values
                                                               which need to be reset back to their default values
                                                               at the end of the execution of the class, alongside
                                                               resetting "found" back to False, so that class is ready
                                                               to be executed again for extracting variables from
                                                               another, different .log file.
                                     Additional keys for some variables include:
                                        "num"(None -> int)   : For "kind_atoms", "num" will be
                                                               populated with the number of different
                                                               element species that are present within the
                                                               material being simulated. For "pop1" and
                                                               "pop2", "num" will be populated with the total
                                                               number of atoms that are present within the material.
                                        "cnt"(None -> int)   : For "kind_atoms", "count" will keep
                                                               track of how many of the different elemental
                                                               species have had their corresponding data
                                                               extracted from the .log file.


        Inputs:
            os.path(os.path)       : File path of log file being searched.

            keywrds(list)          : Potentially a list of multiple keywords which
                                     correspond to the different result processing method
                                     the user may choose to perform.

        Variables:
            process(dict)          : Dictionary where all mp.Process()'s created in __init__ for
                                     running associated functions of each needed variable are
                                     inputted as item values with items keys detailing the stated order
                                     of variable types within the want dictionary entry for a particular
                                     result processing method
            v2rtn(mp.manager list) : Multiprocessing.Manager.list() containing i
                                     number of inner mp.Manager.list()'s [equal to the total number of
                                     variable types needing to be found] to be used for collecting the
                                     result details extracted for each variable type via the associated
                                     functions within each mp.Process() created. mp.Manager.list()
                                     can then be returned containing all extracted data.
    """

    want = {"band structure": ["version"],
            "charges and spins": ["pop1", "pop2"],
            "charge transition levels": [ "charge", "energy", "knd_atms"],
            "geometry": ["a"],
            "original": ["charge", "name", "run"],
            "all":["a","at_crd","charge","energy","gap","knd_atms","name","pop1","pop2","run","version"]}

    var_fo = {"a":
                  {"locate": '|a|', "via": "find_a", "found": False, "reset": None},
              "at_crd":
                  {"locate": "MODULE QUICKSTEP:  ATOMIC COORDINATES IN angstrom", "via": "find_at", "found": False,
                   "reset": None},
              "charge":
                  {"locate": "DFT| Charge", "via": "find_charge", "found": False, "reset": None},
              "energy":
                  {"locate": "ENERGY| Total FORCE_EVAL", "via": "find_energy", "found": False, "reset": None},
              "gap":
                  {"locate": "HOMO - LUMO gap", "via": "find_gap", "found": False, "reset": None},
              "knd_atms":
                  {"locate": "Atomic kind", "via": "find_kind", "found": False, "num": None, "cnt": None,
                   "reset": ["num", None, "count", None]},
              "name":
                  {"locate": "Project name", "via": "find_name", "found": False, "reset": None},
              "pop1":
                  {"locate": ["Total charge and spin", "Mulliken Population Analysis"], "via": "find_pop1",
                   "found": False, "num": None, "reset": ["num", None]},
              "pop2":
                  {"locate": ["Total Charge", 'Hirshfeld Charges'], "via": "find_pop2", "found": False,
                   "num": None, "reset": ["num", None]},
              "run":
                  {"locate": "Run type", "via": "find_run", "found": False, "reset": None},
              "version":
                  {"locate": " CP2K| version string:", "via": "find_version", "found": False, "reset": None}}

    def __init__(self, os_path, keywrds):
        manager = mp.Manager()
        self.process, all_kinds = dict(), []

        self.v2rtn = manager.list([ manager.list() for i in range(sum([len(FromLog.want[key]) for key in keywrds])) ])
        log = open(os_path, 'r')
        lines, index = [log.readlines(), len(log.readlines()) + 1]

        for ln in reversed(lines):  # for every line in file from bottom of file,
            index -= 1
            for keywrd in keywrds:  # for each result processing method keyword,
                for indx, item in enumerate(FromLog.want[keywrd]):  # info for each variable to be extracted for the
                                                                    # specific method,
                    if FromLog.var_fo.get(item)["found"] is False:
                        if item.find("pop") == -1 and FromLog.var_fo.get(item)["locate"] in ln:

                            # Creating mp.Process() for associated functions which require index and lines to be passes
                            # as args.
                            if item in ["a", "at_crd", "gap"]:
                                key = str(FromLog.var_fo.get(item)["via"])
                                # associated function w/ "at_crd" doesn't need ln being passed to it as an arg.
                                self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                                args=(index, lines, indx, self.v2rtn)) if item == \
                                                                                                        "at_crd" \
                                               else mp.Process(target=eval("{}".format(key)),
                                                                args=(ln, index, lines, indx, self.v2rtn))
                                self.update_dict(item)  # changing boolean to None to break out of if loop for var item

                            # 1st instance of "locate" string found in log for "knd_atms". Get total # of kinds in calc.
                            elif item == "knd_atms" and not FromLog.var_fo.get("knd_atms")["num"]:
                                self.kind_first_found(ln)

                            # total # of kinds known, new instance of "locate" string found in log file.
                            elif item == "knd_atms" and FromLog.var_fo.get("knd_atms")["num"]:
                                all_kinds.append(ln)  # all_kinds(list) was created alongside self.process at beginning
                                                      # of __init__. Each new ln with new instance of "locate" found is
                                                      # appended to list.

                                # update number of kinds found to reflect another instance of "locate" has been found.
                                self.update_dict("knd_atms",["cnt", int(FromLog.var_fo.get("knd_atms")["cnt"]+1)])

                                # creating mp.Process() for associated functions which require all_kinds
                                if FromLog.var_fo.get("knd_atms")["cnt"] == int(FromLog.var_fo.get("knd_atms")["num"]):
                                    key = str(FromLog.var_fo.get(item)["via"])
                                    self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                                    args=(all_kinds, indx, self.v2rtn))
                                    self.update_dict("knd_atms")  # changing boolean to None to break out of if loop
                                                                  # for "knd_atms" variable.

                            # creating mp.Process() for associated functions which require ln.
                            else:
                                key = str(FromLog.var_fo.get(item)["via"])
                                self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                                args=(ln, indx, self.v2rtn))
                                self.update_dict(item)  # changing boolean to None to break out of if loop for var item.

                        # 1st instance of "locate" string found in log for "pop1" or "pop2". atom numbers ("num")
                        # unknown, get total number of atoms in calc.
                        elif item.find("pop") != -1 and FromLog.var_fo.get(item)["locate"][0] in ln and not \
                                FromLog.var_fo.get(item)["num"]:
                            self.pop_first_found(item, index, lines)

                        # creating mp.Process() for associated functions which require atoms, index, lines.
                        elif item.find("pop") != -1 and FromLog.var_fo.get(item)["locate"][1] in ln:
                            atoms, key = int(FromLog.var_fo.get(item)["num"]), str(FromLog.var_fo.get(item)["via"])
                            self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                            args=(atoms, index, lines, indx, self.v2rtn))
                            self.update_dict(item)  # changing boolean to None to break out of if loop for var item.
        self.compute()
        log.close()
        [self.reset_dict(item, FromLog.var_fo.get(item)["reset"]) for item in [FromLog.want.get(keywrd) for keywrd in
                                                                              keywrds][0]]

    def compute(self):
        """
            Running mp.Process()'s created in __init__

            Converting the dictionary of mp.Process()'s in to a list of mp.Process()'s to be all start()'ed one after
            the other before they are all join()'ed one after the other.
        """

        processes = []
        for indx in self.process:
            processes.append(self.process[indx])
        [x.start() for x in processes]
        [x.join() for x in processes]

    def kind_first_found(self, line):
        """
            Obtaining total number of atomic kinds in calculation system.

            Inputs:
                line(str) : line of log file that "locate" str for variable
                            "knd_atms" has been found to be contained in.
        """

        number = [float(var[1]) for var in enumerate(line.split())
                  if var[0] in [6]][0]  # extraction of txt in indices 6 in list of line split via delimiter
                                        # white space. number is number of different element kinds in calc.
        self.update_dict("knd_atms", ["num", number, "cnt", 0])  # save total num of kinds in dict for later reference.

    def pop_first_found(self, pop, index, lines):
        """
            Obtaining total number of atoms in calculation system.

            Inputs:
                pop(str)           : The particular 'pop' variable type name - either
                                     "pop1" or "pop2"

                index(int)         : Number which signifies line number from bottom
                                     of log file that "locate"[0] str has been found to
                                     be contained in.

                lines(list of str) : All lines found within the log file via
                                     log.readlines() in __init__.
        """

        n = 2 if pop == "pop1" else 3  # extra blank line in file between lines containing "locate"[0] and last atom #
                                       # for "pop2"
        number = [var[1] for var in enumerate(lines[index - n].split())
                  if var[0] in [0]][0]  # extraction of txt in index 0 in list of line split by white space. number
                                        # is atom # of last atom listed in pop anlysis, = system tot atoms.
        self.update_dict(pop, ["num", number])  # save total number of atoms in dict for later reference.

    @classmethod
    def update_dict(cls, key, extra=None):
        """
            Updating var_fo dictionary.

            As each "locate" string of each variable type needing to be found is located within a line of the log file
            being searched, the var_fo dictionary will need to be mainly updated to stop more mp.Process()'s being
            created then are needed and to make sure the details extracted for each variable type is the most
            up-to-date details from the last job run of the calculation.
            This is done by changing the item value of the "found" key of a variable from False to None.

            Inputs:
                key(str)         : Variable type name needed to have their nested dictionary reset.

                extra(list/None) : Optional argument of list type which will only be given if
                                   another item key and value pair within the nested dictionary of a
                                   variable type need to be updated with intermediate data
                                   collected during searching the log file. Like for variable types:
                                   "knd_atms", "pop1", and "pop2".
        """

        if extra:  # if optional argument extra given, then item value for item key "found" doesn't need updating yet.
            for i in range(0, int(len(extra)/2)):  # if list, will consist of elements such as [k1, v1, k2, v2, k3, v3],
                                                   # Half of list length = # of additional item pairs to be updated.

                # Ensuring subsequent elements [i*(i*1) and i*(i*1)*1] of list used as item key and value pairs
                # i.e. if i = 0: i*(i*1) = 0 {k1}, i*(i*1)*1 = 1{v1}; if i = 2, i*(i*1) = 4 {k3}, i*(i*1)*1 = 5 (v3).
                FromLog.var_fo[key].update({extra[int(i+(i*1))]: extra[int(i+(i*1)+1)]})
        else:
            FromLog.var_fo[key].update({"found": None})

    @classmethod
    def reset_dict(cls, key, extra):
        """
            Resetting var_fo dictionary to defaults.

            Although the var_fo dictionary is reset to the original state it is in before the FromLog class is called
            within each mp.Process() created, outside of those mp.Process()'s the dictionary is still populated by the
            item values changed within its current run. For the class to be used effectively on the next log file it is
            given as an argument when it is next called, the dictionary (especially the item value of the item key
            "found") must be manually reset.

            Inputs:
                key(str)         : Variable type name needed to have their nested dictionary reset.

                extra(list/None) : Additional item values and their item keys which need to
                                   be reset back to their defaults alongside the item value for the
                                   "found" item key. Only certain variable types require additional
                                   items to be reset - for those who don't extra will be None; for
                                   those that do extra will be a list. This list corresponds to the
                                   defaults stated within the FromLog.var_fo[key]["reset"] item
                                   values of each variable type.
        """

        FromLog.var_fo[key].update({"found": False})
        if extra:  # only when extra isn't None
            for i in range(0, int(len(extra)/2)):  # if list, will consist of elements such as [k1, v1, k2, v2, k3, v3],
                                                   # Half of list length = # of additional item pairs to be updated.

                # Ensuring subsequent elements [i*(i*1) and i*(i*1)*1] of list used as item key and value pairs
                # i.e. if i = 0: i*(i*1) = 0 {k1}, i*(i*1)*1 = 1{v1}; if i = 2, i*(i*1) = 4 {k3}, i*(i*1)*1 = 5 (v3).
                FromLog.var_fo[key].update({extra[int(i+(i*1))]: extra[int(i+(i*1)+1)]})

    def Return(self):
        return self.v2rtn
