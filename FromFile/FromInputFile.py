import FromFile

class NameOfProject:
    def __init__(self, input_file):
        self.input_file = input_file

    def ReturnName(self):
        with open(self.input_file) as inp:
            name = inp.readlines()[2].split()
            project_name = name[-1]

        return project_name


class Kinds:
    kind = '     &KIND'
    def __init__(self, input_file):
        self.inpkindline = []
        self.included_atoms = []
        self.input_file = input_file

    def searchingfile(self):
        inp = open(self.input_file, 'r')
        index = 0
        for line in inp:
            index += 1
            if FromFile.Kinds.kind in line:
                kindln = index - 1
                self.inpkindline.append(kindln)
        inp.close()

        num_kinds = len(self.inpkindline)  # len() returns the num elements in a list - = to num of kinds in structure

        inp = open(self.input_file, 'r')
        for position, line in enumerate(inp):
            if position in self.inpkindline:
                strg = line.split()
                atom = strg[-1]
                self.included_atoms.append(atom)
        inp.close()

        return num_kinds, self.included_atoms

class ChargeStateIdentification:
    chargekw = "     CHARGE"
    def __init__(self, input_file):
        self.input_file = input_file
        self.chargeline = ''
        self.check = False

        if self.chargecheck():
            self.state = self.getchargestate()
        else:
            self.state = 0  # no charge keyword in inp, charge set to default neutral

        self.returnstate()

    def chargecheck(self):
        file = open(self.input_file, 'r')
        index = 0
        for line in file:
            index += 1
            if FromFile.ChargeStateIdentification.chargekw in line:
                self.check = True
                self.chargeline = index - 1
                break

        return self.check

    def getchargestate(self):
        file = open(self.input_file, 'r')
        for position, line in enumerate(file):
            if position == self.chargeline:
                strg = line.split()
                charge = strg[-1]
                return charge

    def returnstate(self):
        return int(self.state)

