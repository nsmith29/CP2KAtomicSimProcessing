import Core
import FromFile

class NameOfProject:
    def __init__(self, input_file):
        self.input_file = input_file

    # def ReturnName(self):
        with open(self.input_file) as inp:
            name = inp.readlines()[2].split()
            self.project_name = name[-1]

        # return project_name

class Kinds:
    kind = '     &KIND'
    def __init__(self, input_file):
        self.inpkindline = []
        self.included_atoms = []
        self.input_file = input_file

    # def searchingfile(self):
        inp = open(self.input_file, 'r')
        index = 0
        for line in inp:
            index += 1
            if FromFile.Kinds.kind in line:
                kindln = index - 1
                self.inpkindline.append(kindln)
        inp.close()

        self.num_kinds = len(self.inpkindline)  # len() returns the num elements in a list - = to num of kinds in structure

        inp = open(self.input_file, 'r')
        for position, line in enumerate(inp):
            if position in self.inpkindline:
                strg = line.split()
                atom = strg[-1]
                self.included_atoms.append(atom)
        inp.close()

        # return num_kinds, self.included_atoms

class chargecheck:
    def __init__(self, input_file):
        self.chargeline = ''
        self.check = False
        file = open(input_file, 'r')
        index = 0
        for line in file:
            index += 1
            if FromFile.ChargeStateIdentification.chargekw in line:
                self.check = True
                self.chargeline = index - 1
                break

class getchargestate:
    def __init__(self, input_file, chargeline):
        self.charge = None
        file = open(input_file, 'r')
        for position, line in enumerate(file):
            if position == chargeline:
                strg = line.split()
                self.charge = strg[-1]

class ChargeStateIdentification(chargecheck, getchargestate):
    chargekw = "     CHARGE"
    def __init__(self, input_file):
        self.input_file = input_file
        chargecheck.__init__(self, self.input_file)
        if self.check is True:
            getchargestate.__init__(self, self.input_file, self.chargeline)
            self.state = self.charge
        else:
            self.state = 0  # no charge keyword in inp, charge set to default neutral

class OnlyNeutralWanted(ChargeStateIdentification):
    def __init__(self, all_subdirs, all_suffixs):
        self.allsubdirs = all_subdirs
        self.allsuffixs = all_suffixs

        self.subdirs = []
        self.suffixs = []

        for subdir, suffix in zip(list(self.allsubdirs), list(self.allsuffixs)):
            ChargeStateIdentification.__init__(self, Core.Extension().files4defect(".inp", subdir))
            if self.state == 0:
                self.subdirs.append(subdir)
                self.suffixs.append(suffix)
        # return self.subdirs, self.suffixs

class CheckSameCalculationSettings:
    xc = 'XC'
    ADMM = 'AUXILIARY_DENSITY_MATRIX_METHOD'

    def __init__(self, ref_input_file, check_input_file):
        checklines1 = []
        checklines2 = []
        self.check = None
        with open(ref_input_file, 'r') as file1:
            lines = file1.read()
            globlines = lines[lines.find('&GLOBAL'):lines.find('&END GLOBAL')]
            checklines1.append(globlines)
            GEOOPT = lines[lines.find('&GEO_OPT'):lines.find('&END GEO_OPT')]
            checklines1.append(GEOOPT)
            CELLOPT = lines[lines.find('&CELL_OPT'):lines.find('&END CELL_OPT')]
            checklines1.append(CELLOPT)
            scflines = lines[lines.find('&SCF'):lines.find('&END SCF')]
            checklines1.append(scflines)
            qslines = lines[lines.find('&QS'):lines.find('&END QS')]
            checklines1.append(qslines)
            mgridlines = lines[lines.find('&MGRID'):lines.find('&END MGRID')]
            checklines1.append(mgridlines)
            xclines = lines[lines.find('&XC'):lines.find('&END XC')]
            checklines1.append(xclines)
            ADMMlines = lines[lines.find('&AUXILIARY_DENSITY_MATRIX_METHOD'):lines.find('&END AUXILIARY_DENSITY_MATRIX_METHOD')]
            checklines1.append(ADMMlines)
        found = []
        with open(check_input_file, 'r') as file2:
            lines = file2.read()
            globlines = lines[lines.find('&GLOBAL'):lines.find('&END GLOBAL')]
            checklines2.append(globlines)
            GEOOPT = lines[lines.find('&GEO_OPT'):lines.find('&END GEO_OPT')]
            checklines2.append(GEOOPT)
            CELLOPT = lines[lines.find('&CELL_OPT'):lines.find('&END CELL_OPT')]
            checklines2.append(CELLOPT)
            scflines = lines[lines.find('&SCF'):lines.find('&END SCF')]
            checklines2.append(scflines)
            qslines = lines[lines.find('&QS'):lines.find('&END QS')]
            checklines2.append(qslines)
            mgridlines = lines[lines.find('&MGRID'):lines.find('&END MGRID')]
            checklines2.append(mgridlines)
            xclines = lines[lines.find('&XC'):lines.find('&END XC')]
            checklines2.append(xclines)
            ADMMlines = lines[lines.find('&AUXILIARY_DENSITY_MATRIX_METHOD'):lines.find(
                '&END AUXILIARY_DENSITY_MATRIX_METHOD')]
            checklines2.append(ADMMlines)
            for check1, check2 in zip(list(checklines1), list(checklines2)):
                if check1 == check2:
                    found.append('+')
        if len(found) == len(checklines1):
            self.check = True
        else:
            self.check = False

class LatticeVectors:
    look4 = '     &CELL'
    def __init__(self, input_file):
        self.A_lat_Vec = None
        self.B_lat_Vec = None
        self.C_lat_Vec = None
        self.A = None
        self.B = None
        self.C = None
        self.input_file = input_file

    def search(self):
        inp = open(self.input_file, 'r')
        index = 0
        for line in inp:
            index += 1
            if LatticeVectors.look4 in line:
                CELL_line = index - 1
                self.A_lat_Vec = CELL_line + 1
                self.B_lat_Vec = CELL_line + 2
                self.C_lat_Vec = CELL_line + 3
                break
        inp.close()
        for l in 'A', 'B', 'C':
            lines_to_read = eval("self.{}_lat_Vec".format(l))
            inp = open(self.input_file, 'r')
            for position, line in enumerate(inp):
                if position == lines_to_read:
                    strg = line
                    exec(f'{l}_full_line_arr = strg.split()')
                    if l == 'A':
                        exec(f'{l}_full_line_arr.remove("A")')
                        exec(f'self.A = [float(x) for x in {l}_full_line_arr]')
                    elif l == 'B':
                        exec(f'{l}_full_line_arr.remove("B")')
                        exec(f'self.B = [float(x) for x in {l}_full_line_arr]')
                    elif l == 'C':
                        exec(f'{l}_full_line_arr.remove("C")')
                        exec(f'self.C = [float(x) for x in {l}_full_line_arr]')
            inp.close()

        return self.A, self.B, self.C