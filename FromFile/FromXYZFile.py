import FromFile
from Core import Extension

# class to identify the number of atoms of each kind
class LastXYZ:
    def __init__(self,subdir):
        self.subdir = subdir
        lastxyz = Extension().files4defect("-L.xyz", self.subdir)
        if lastxyz == " ":
            xyz_file = Extension().files4defect(".xyz", self.subdir)
            name_list = []
            for i in range(len(xyz_file)):
                letter = xyz_file[i]
                name_list.append(letter)

            with open(xyz_file) as f:
                firstline = f.readline().rstrip()
                self.tot_atoms = firstline.split()

            self.total_atoms_in_calc = float(self.tot_atoms[0]) + 2
            itr_start = []
            L_itr_lines = []
            file = open(xyz_file, 'r')
            index = 0
            for line in file:
                index += 1
                if firstline in line:
                    j = index
                    itr_start.append(j)
            l = (itr_start[-1] - 1)
            for n in range(0, int(self.total_atoms_in_calc)):
                Lns = l + n
                L_itr_lines.append(Lns)
            file.close()

            name_list[-5] = "L"
            self.new_xyz_file = "".join(name_list)

            file = open(xyz_file, 'r')
            output_file = open(self.new_xyz_file, 'w')
            for position, line in enumerate(file):
                if position in L_itr_lines:
                    string = line
                    output_file.write(string)
            output_file.close()
            file.close()
        else:
            self.new_xyz_file = lastxyz

            with open(self.new_xyz_file) as f:
                firstline = f.readline().rstrip()
                self.tot_atoms = firstline.split()

            self.total_atoms_in_calc = float(self.tot_atoms[0]) + 2

    def returnlastxyzname(self):
        return self.new_xyz_file

    def returntotalatoms(self):
        return self.tot_atoms

    def Name4Coordinate(self):
        atoms = []
        i_lines = []

        file = open(self.new_xyz_file, 'r')
        for i in range(2, int(self.total_atoms_in_calc)):
            i_lines.append(i)
        for position, line in enumerate(file):
            if position in i_lines:
                strg = line.split()
                name = strg[0]
                atoms.append(name)

        return atoms


class NumTotAtomsOfKind:
    def __init__(self, subdir, kinds, num):
        self.subdir = subdir
        self.kinds = kinds
        self.num = num

        self.atoms4kind = self.GetNumOfEachKind()

    def GetNumOfEachKind(self):
        xyzfile = FromFile.LastXYZ(self.subdir).returnlastxyzname()
        atoms4kind = []
        for i in range(0, int(self.num)):
            find = self.kinds[i]
            file = open(xyzfile, 'r')
            index = 0
            count = 0
            for line in file:
                index += 1
                if find in line:
                    count += 1
            file.close()
            atoms4kind.append(count)

        return atoms4kind

    def PdosScalingFactor(self, specifickind):
        kindAnum = 0
        for i in range(0, int(self.num)):
            if self.kinds[i] != specifickind:
                if kindAnum == 0:
                    kindAnum = self.atoms4kind[i]
                else:
                    kindBnum = self.atoms4kind[i]
                    if kindAnum < kindBnum:
                        kindAnum = kindBnum
            else:
                index = i
        specific_number = self.atoms4kind[index]

        scalingfactor = 50 * round((kindAnum - specific_number)/50)

        return scalingfactor

