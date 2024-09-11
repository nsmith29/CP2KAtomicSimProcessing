#!/usr/bin/env python3

class FromInp:
    """

    """

    want = {"charges and spins": ["FirstXYZ"]}

    var_fo = {"FirstXYZ":
                  {"locate": 'COORD_FILE_NAME', "via": 'find_xyz',
                   "check": "&TOPOLOGY", "swapped": False,
                   "alt": "&END COORD", "alt_via": "make_xyz",
                   "found": False}
              }

    def __init__(self, os_path, keywrds):
        self.results, self.os_path = [], os_path
        inp = open(os_path, 'r')
        self.lines, self.index = [inp.readlines(), len(inp.readlines()) + 1]

        for ln in reversed(self.lines):  # for every line in file from bottom of file,
            self.index -= 1
            for keywrd in keywrds:  # for each result processing method keyword,
                for indx, item in enumerate(FromInp.want[keywrd]):  # info for each variable to be extracted for the
                                                                    # specific method,
                    if FromInp.var_fo.get(item)["found"] is False:
                        if FromInp.var_fo.get(item)["locate"] in ln:
                            self.update_dict(item)  # changing boolean to None to break out of if loop for var item.
                            eval(str("self.{}(ln)".format(FromInp.var_fo.get(item)["via"])))

                        # When top of section where "locate" str usually placed is reached & "locate" str not found.
                        elif FromInp.var_fo.get(item)["check"] in ln:
                            self.switch(item)  # start looking for "alt" str in .inp file.

        inp.close()
        [self.reset_dict(item) for item in [FromInp.want.get(keywrd) for keywrd in keywrds][0]]

    def find_xyz(self, line):
        xyz_name = [str(var[1]) for var in enumerate(line.split()) if var[0] in [1]][0]
        if xyz_name.find('/'):
            xyz_name = xyz_name.split('/')[-1]
        self.results.append(xyz_name)

    def make_xyz(self, line):
        # index of line above in self.lines, derival of path of xyz file in same directory as .inp file of self.os_path.
        indx, readlines, filename = self.index - 2, [], '/'.join(self.os_path.split('/')[:-1] + ["geometry.xyz"])
        xyz_file, atoms = open(filename, 'w'), 0  # write new file and create counter for total number of atoms.
        while "&COORD" not in self.lines[indx]:  # if line contains "&COORD", xyz atom positions finished,
            atoms += 1
            readlines.insert(0, self.lines[indx])
            indx -= 1
        readlines.insert(0, f"     {atoms}\n\n")  # insert standard xyz file 1st line into lines for writing to new file.
        for string in readlines:
            xyz_file.write(str(string))
        xyz_file.close()

        self.results.append(filename.split('/')[-1])  # append just name of newly written xyz file

    @classmethod
    def switch(cls, key):
        """

        """
        locate, via, alt, alt_via = FromInp.var_fo[key].get("locate"), FromInp.var_fo[key].get("via"),\
                                    FromInp.var_fo[key].get("alt"), FromInp.var_fo[key].get("alt_via")
        FromInp.var_fo[key].update({"locate": alt})
        FromInp.var_fo[key].update({"alt": locate})
        FromInp.var_fo[key].update({"via": alt_via})
        FromInp.var_fo[key].update({"alt_via": via})
        FromInp.var_fo[key].update({"swapped": True})

    @classmethod
    def update_dict(cls, key):
        """
            Updating var_fo dictionary.

            As each "locate" string of each variable type needing to be found is located within a line of the log file
            being searched, the var_fo dictionary will need to be mainly updated to stop further iterations of the for
            loop in __init__. This is done by changing the item value of the "found" key of a variable from False to
            None.

            Inputs:
                key(str)         : Variable type name needed to have their nested dictionary reset.
        """
        FromInp.var_fo[key].update({"found": None})

    @classmethod
    def reset_dict(cls, key):
        """
            Resetting var_fo dictionary to defaults.

            For the class to be used effectively on the next log file it is given as an argument when it is next called,
            the dictionary (especially the item value of the item key "found") must be manually reset.

            Inputs:
                key(str)         : Variable type name needed to have their nested dictionary reset.
        """
        FromInp.var_fo[key].update({"found": False})
        if FromInp.var_fo[key].get("swapped") is True:
            locate, via, alt, alt_via = FromInp.var_fo[key].get("alt"), FromInp.var_fo[key].get("alt_via"), \
                                        FromInp.var_fo[key].get("locate"), FromInp.var_fo[key].get("via")
            FromInp.var_fo[key].update({"locate": locate})
            FromInp.var_fo[key].update({"alt": alt})
            FromInp.var_fo[key].update({"via": via})
            FromInp.var_fo[key].update({"alt_via": alt_via})
            FromInp.var_fo[key].update({"swapped": False})

    def Return(self):
        return self.results



