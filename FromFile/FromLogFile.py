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

    # line with a lattice vector and length of material cell used within calc.
    strg1 = line
    # self.lines[self.index] is fileline below line; holds b latt. vec. & length.
    strg2 = lines[index]
    # c latt. vec. & length.
    strg3 = lines[index + 1]
    collect1 = []
    for s, item, letter in zip([1, 2, 3], ['a', 'b', 'c'], ['A', 'B', 'C']):
        # extract txt of indices 4,5,6,9 in line split list. {letter} is lat cnst, {item}Latt is {item} line of lat vec.
        exec(f'*{letter}, {item}Latt= [float(var[1]) for var in enumerate(strg{s}.split()) if var[0] in '
             f'[4,5,6,9]]')
        exec(f'collect1.extend([{letter}, {item}Latt])')

    # place extracted values in corresponding position of proxy list.
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

    # make empty lists
    X, Y, Z, ELEMENT, MASS = [], [], [], [], []

    # find max number of atoms in calc for information to collected for.
    max = [int(var[1]) for var in enumerate(lines[index - 20].split()) if var[0] in [3]][0]

    # Some log files have an extra blank space between line where "locate" string is found & start of atom info.
    try:
        element = [var[1] for var in enumerate(lines[index + 2].split()) if var[0] in [2]]
        n = 2
    except ValueError:
        element = [var[1] for var in enumerate(lines[index + 3].split()) if var[0] in [2]]
        n = 3
    finally:
        for p in range(0, max):
            # extract index 2,4-6,8 in line split list. element - atom element, x/y/z - x/y/z-coord, mass - atomic mass.
            element, x, y, z, mass = [var[1] for var in enumerate(lines[index + n + p].split()) if
                                      var[0] in [2, 4, 5, 6, 8]]
            for f, F in zip([float(x), float(y), float(z), element, mass], [X, Y, Z, ELEMENT, MASS]):
                # saving extracted data within predefined lists.
                F.append(f)
    array = np.array([X, Y, Z])

    # place extracted values in corresponding position of proxy list.
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

    # extracted txt of index 2 in line split list, C is the charge state of calc.
    C = [int(var[1]) for var in enumerate(line.split()) if var[0] in [2]][0]

    # alter C so reported charge state is given with sign of charge state after number of charge ie -1 -> 1-
    if C < 0:
        # negative charge states.
        C = "".join(["".join([i for i in list(str(C)) if i != '-']),'-'])
    elif C == 0:
        pass
    else:
        # positive charge states.
        C = "".join([str(C),"+"])

    # place extracted value in corresponding position of proxy list.
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

    # extract of txt of index 8 in line split list. E is tot energy of calc converted from hartree units to eV.
    E = [(round(float(var[1]), 10) * 27.211) for var in enumerate(line.split()) if var[0] in [8]][0]

    # place extracted value in corresponding position of proxy list.
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

    # beta gap
    strg2 = line
    # alpha gap
    strg1 = lines[index - 2]
    collect2 = []
    for spin, s in zip(["alpha", "beta"], [1, 2]):
        # extract txt of index 6 in line split list. {spin}_HOMO_LUMOgap is {spin} band gap in eV.
        exec(f'{spin}_HOMO_LUMOgap = [float(var[1]) for var in enumerate(strg{s}.split()) if var[0] in[6]][0]')
        exec(f'collect2.append({spin}_HOMO_LUMOgap)')

    # place extracted values in corresponding position of proxy list.
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
        # extract indices 3,7 in line split list. kind_ele - name of kind, num_atoms - # of atoms of kind in calc.
        kind_ele, num_atoms = [var[1] for var in enumerate(line.split()) if var[0] in [3, 7]]
                                                     #
        collect3.extend([kind_ele, num_atoms])

    # place extracted values in corresponding position of proxy list.
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

    # extract txt of index 3 in line split list. N is the project name of calculation.
    N = [str(var[1]) for var in enumerate(line.split()) if var[0] in [3]][0]

    # place extracted value in corresponding position of proxy list.
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
    # A of specific atom indices or from 0 to total number of atoms in system.
    for A in rnge:
        # extract indices 3-6 in line split list. p1_a & p1_b - alpha & beta pops, p1_s & p1_c - Mulliken spin & charge.
        p1_a, p1_b, p1_c, p1_s = [round(float(var[1]),3) for var in enumerate(lines[int(index + 2 + A)].split())
                                  if var[0] in [3, 4, 5, 6]]
        collect.append([p1_a, p1_b, p1_c, p1_s])

    # place extracted values in corresponding position of proxy list.
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
    # A of specific atom indices or from 0 to total number of atoms in system.
    for A in rnge:
        # extract indices 4-7 in line split list. p2_a & p2_b - alpha & beta pops, p2_s & p2_c - Hirshfeld spin & charge.
        p2_a, p2_b, p2_s, p2_c = [round(float(var[1]),3) for var in enumerate(lines[int(index + 2 + A)].split())
                                  if var[0] in [4, 5, 6, 7]]
        collect.append([p2_a, p2_b, p2_c, p2_s])

    # place extracted values in corresponding position of proxy list.
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

    # extract txt of index 3 in line split list. R is the calculation run type.
    R = [str(var[1]) for var in enumerate(line.split()) if var[0] in [3]][0]

    # place extracted value in corresponding position of proxy list.
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

    # extract txt of index 5 in line split list. V is CP2K version calculation performed with.
    V = [float(var[1]) for var in enumerate(line.split()) if var[0] in [5]][0]

    # place extracted value in corresponding position of proxy list.
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

        # for every line in file from bottom of file,
        for ln in reversed(lines):
            index -= 1
            # for each result processing method keyword.
            for keywrd in keywrds:
                # info for each variable to be extracted for the specific method,
                for indx, item in enumerate(FromLog.want[keywrd]):
                    if FromLog.var_fo.get(item)["found"] is False:
                        if item.find("pop") == -1 and FromLog.var_fo.get(item)["locate"] in ln:

                            # Creating mp.Process() for associated functions requiring args of index & lines.
                            if item in ["a", "at_crd", "gap"]:
                                key = str(FromLog.var_fo.get(item)["via"])
                                # associated function w/ "at_crd" doesn't need ln being passed to it as an arg.
                                self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                                args=(index, lines, indx, self.v2rtn)) if item == \
                                                                                                        "at_crd" \
                                               else mp.Process(target=eval("{}".format(key)),
                                                                args=(ln, index, lines, indx, self.v2rtn))
                                # changing boolean to None to break out of if loop for var item
                                self.update_dict(item)

                            # 1st instance of "locate" string found in log for "knd_atms". Get total # of kinds in calc.
                            elif item == "knd_atms" and not FromLog.var_fo.get("knd_atms")["num"]:
                                self.kind_first_found(ln)

                            # total # of kinds known, new instance of "locate" string found in log file.
                            elif item == "knd_atms" and FromLog.var_fo.get("knd_atms")["num"]:
                                # list created at top of __init__. Append each new ln instance of "locate" found in.
                                all_kinds.append(ln)

                                # update number of kinds found to reflect another instance of "locate" has been found.
                                self.update_dict("knd_atms",["cnt", int(FromLog.var_fo.get("knd_atms")["cnt"]+1)])

                                # creating mp.Process() for associated functions which require all_kinds
                                if FromLog.var_fo.get("knd_atms")["cnt"] == int(FromLog.var_fo.get("knd_atms")["num"]):
                                    key = str(FromLog.var_fo.get(item)["via"])
                                    self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                                    args=(all_kinds, indx, self.v2rtn))
                                    # changing boolean to None to break out of if loop for "knd_atms" variable.
                                    self.update_dict("knd_atms")

                            # creating mp.Process() for associated functions which require ln.
                            else:
                                key = str(FromLog.var_fo.get(item)["via"])
                                self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                                args=(ln, indx, self.v2rtn))
                                # changing boolean to None to break out of if loop for var item.
                                self.update_dict(item)

                        # 1st "locate" string instance found for "pop1"/"pop2". atom "num" unknown, get tot atom #.
                        elif item.find("pop") != -1 and FromLog.var_fo.get(item)["locate"][0] in ln and not \
                                FromLog.var_fo.get(item)["num"]:
                            self.pop_first_found(item, index, lines)

                        # creating mp.Process() for associated functions which require atoms, index, lines.
                        elif item.find("pop") != -1 and FromLog.var_fo.get(item)["locate"][1] in ln:
                            atoms, key = int(FromLog.var_fo.get(item)["num"]), str(FromLog.var_fo.get(item)["via"])
                            self.process[indx] = mp.Process(target=eval("{}".format(key)),
                                                            args=(atoms, index, lines, indx, self.v2rtn))
                            # changing boolean to None to break out of if loop for var item.
                            self.update_dict(item)
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

        # extract txt of index 6 in line split list. number is number of different element kinds in calc.
        number = [float(var[1]) for var in enumerate(line.split()) if var[0] in [6]][0]
        # save total num of kinds in dict for later reference.
        self.update_dict("knd_atms", ["num", number, "cnt", 0])

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

        # extra blank line in file between lines containing "locate"[0] and last atom for "pop2"
        n = 2 if pop == "pop1" else 3
        # extract txt of index 0 in line split list. number is atom # of last atom listed in analysis = calc tot atoms.
        number = [var[1] for var in enumerate(lines[index - n].split())
                  if var[0] in [0]][0]
        # save total number of atoms in dict for later reference.
        self.update_dict(pop, ["num", number])

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

        # if optional argument extra given, then item value for item key "found" doesn't need updating yet.
        if extra:
            # List such as [k1, v1, k2, v2, k3, v3], 1/2 of list length = # of additional item pairs to be updated.
            for i in range(0, int(len(extra)/2)):
                # Pairing indices 2*i & 2*i+1 as key & value - i=0, 2*i=0{k1}, 2*i+1=1{v1}; i=2, 2*i=4{k3}, 2*i+1=5{v3}.
                FromLog.var_fo[key].update({extra[int(2*i)]: extra[int(2*i+1)]})
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
        # only when extra isn't None
        if extra:
            # List such as [k1, v1, k2, v2, k3, v3], 1/2 of list length = # of additional item pairs to be updated.
            for i in range(0, int(len(extra)/2)):

                # Pairing indices 2*i & 2*i+1 as key & value - i=0, 2*i=0{k1}, 2*i+1=1{v1}; i=2, 2*i=4{k3}, 2*i+1=5{v3}.
                FromLog.var_fo[key].update({extra[int(2 * i)]: extra[int(2 * i + 1)]})

    def Return(self):
        return self.v2rtn
