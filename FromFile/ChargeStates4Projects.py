import FromFile
from Core import Extension
class SortingChargeStates:
    ProjectChargesStore = dict()
    def __init__(self, subdirs):
        self.subdirs = subdirs

        self.defneutral = []
        self.neutralsubdir = []
        self.namesneutral = []
        self.inpneutral = []

        self.defneg1 = []
        self.namesneg1 = []
        self.inpneg1 = []
        self.defneg2 = []
        self.namesneg2 = []
        self.inpneg2 = []
        self.defneg3 = []
        self.namesneg3 = []
        self.inpneg3 = []

        self.defpos1 = []
        self.namespos1 = []
        self.inppos1 = []
        self.defpos2 = []
        self.namespos2 = []
        self.inppos2 = []
        self.defpos3 = []
        self.namespos3 = []
        self.inppos3 = []

        self.CategorisingChargeStates()
        for i in range(len(self.namesneutral)):
            name = self.namesneutral[i]
            neutral_file = self.defneutral[i]
            reference_inp = self.inpneutral[i]
            charged_logfiles = self.Grouping4Projects(name, reference_inp)

            subdir = self.neutralsubdir[i]
            self.ProjectDictionary(name, subdir, neutral_file, charged_logfiles)

        self.returnprojectnames()

    def CategorisingChargeStates(self):
        for subdir in list(self.subdirs):
            inpfile = Extension().files4defect(".inp", subdir)
            logfile = Extension().files4defect(".log", subdir)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == 0:
                self.defneutral.append(logfile)
                self.neutralsubdir.append(subdir)
                self.inpneutral.append(inpfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namesneutral.append(name)
            for num in 1, 2, 3:
                if FromFile.ChargeStateIdentification(inpfile).returnstate() == num:
                    exec(f'self.defpos{num}.append(logfile)')
                    exec(f'self.inppos{num}.append(inpfile)')
                    name = FromFile.NameOfProject(inpfile).ReturnName()
                    exec(f'self.namespos{num}.append(name)')
                if FromFile.ChargeStateIdentification(inpfile).returnstate() == -num:
                    exec(f'self.defneg{num}.append(logfile)')
                    exec(f'self.inpneg{num}.append(inpfile)')
                    name = FromFile.NameOfProject(inpfile).ReturnName()
                    exec(f'self.namesneg{num}.append(name)')

    def Grouping4Projects(self, name, reference):
        logfiles = []
        if self.defneg1 != []:
            logfiles.append(FromFile.ProjectSortingIt(name, self.namesneg1,self.defneg1,self.inpneg1,reference).Return())
        else:
            logfiles.append('-')
        if self.defneg2 != []:
            logfiles.append(FromFile.ProjectSortingIt(name, self.namesneg2, self.defneg2, self.inpneg2, reference).Return())
        else:
            logfiles.append('-')
        if self.defneg3 != []:
            logfiles.append(FromFile.ProjectSortingIt(name, self.namesneg3, self.defneg3, self.inpneg3, reference).Return())
        else:
            logfiles.append('-')
        if self.defpos1 != []:
            logfiles.append(FromFile.ProjectSortingIt(name, self.namespos1, self.defpos1, self.inppos1, reference).Return())
        else:
            logfiles.append('-')
        if self.defpos2 != []:
            logfiles.append(FromFile.ProjectSortingIt(name, self.namespos2, self.defpos2, self.inppos2, reference).Return())
        else:
            logfiles.append('-')
        if self.defpos3 != []:
            logfiles.append(FromFile.ProjectSortingIt(name, self.namespos3, self.defpos3, self.inppos3, reference).Return())
        else:
            logfiles.append('-')
        return logfiles

    @classmethod
    def ProjectDictionary(cls, name, subdir, neutralfile, projectfiles):
        project = dict()
        string = str(name)

        neutralinnerkeys = ["dirpath", "logfile"]
        neutrallist = [subdir, neutralfile]
        neutral = dict(zip(neutralinnerkeys,neutrallist))
        project['0'] = neutral
        project['-1'] = projectfiles[0]
        project['-2'] = projectfiles[1]
        project['-3'] = projectfiles[2]
        project['1'] = projectfiles[3]
        project['2'] = projectfiles[4]
        project['3'] = projectfiles[5]

        SortingChargeStates.ProjectChargesStore[string] = project

    def returnprojectnames(self):
        return self.namesneutral

class ProjectSortingIt:
    def __init__(self, name, statenames, statefiles, stateinputs, reference):
        self.file2return = []
        appendedJ = []
        for j in range(len(statenames)):
            if name == statenames[j]:
                self.file2return.append(statefiles[j])
                appendedJ.append(j)
                if len(self.file2return) >= 2:
                    for file, J in zip(list(self.file2return), list(appendedJ)):
                        if FromFile.CheckSameCalculationSettings(reference, stateinputs[J]) == False:
                            self.file2return.remove(file)
                            appendedJ.remove(J)
    def Return(self):
        return self.file2return