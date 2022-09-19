import FromFile
import Core

class SetupSortingNeutral:
    def __init__(self):
        self.defneutral = []
        self.neutralsubdir = []
        self.namesneutral = []
        self.inpneutral = []

class SetupSortingCharged:
    def __init__(self):
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

class ReturnProjectNames(SetupSortingNeutral, FromFile.ChargeStateIdentification, FromFile.NameOfProject):
    def __init__(self, subdirs):
        self.subdirs = subdirs
        SetupSortingNeutral.__init__(self)
        for subdir in list(self.subdirs):
            inpfile = Core.Extension().files4defect(".inp", subdir)
            logfile = Core.Extension().files4defect(".log", subdir)
            FromFile.ChargeStateIdentification.__init__(self,inpfile)
            if self.state == 0:
                self.defneutral.append(logfile)
                self.neutralsubdir.append(subdir)
                self.inpneutral.append(inpfile)
                FromFile.NameOfProject.__init__(self, inpfile)
                self.namesneutral.append(self.project_name)

class CategorisingChargeStates(SetupSortingCharged, FromFile.ChargeStateIdentification, FromFile.NameOfProject):
    def __init__(self, subdirs):
        SetupSortingCharged.__init__(self)
        for subdir in list(subdirs):
            inpfile = Core.Extension().files4defect(".inp", subdir)
            logfile = Core.Extension().files4defect(".log", subdir)
            FromFile.ChargeStateIdentification.__init__(self, inpfile)
            for num in 1, 2, 3:
                if int(self.state) == num:
                    exec(f'self.defpos{num}.append(logfile)')
                    exec(f'self.inppos{num}.append(inpfile)')
                    FromFile.NameOfProject.__init__(self, inpfile)
                    exec(f'self.namespos{num}.append(self.project_name)')
                if int(self.state) == -num:
                    exec(f'self.defneg{num}.append(logfile)')
                    exec(f'self.inpneg{num}.append(inpfile)')
                    FromFile.NameOfProject.__init__(self,inpfile)
                    exec(f'self.namesneg{num}.append(self.project_name)')

class ProjectSortingIt(FromFile.CheckSameCalculationSettings):
    def __init__(self, name, statenames, statefiles, stateinputs, reference):
        self.file2return = []
        self.inputs4return = []
        appendedJ = []
        for j in range(len(statenames)):
            if name == statenames[j]:
                self.file2return.append(statefiles[j])
                appendedJ.append(j)
                self.inputs4return.append(stateinputs[j])
            if len(self.file2return) >= 2:
                for file, input, J in zip(list(self.file2return), list(self.inputs4return), list(appendedJ)):
                    FromFile.CheckSameCalculationSettings.__init__(self, reference, input)
                    if self.check == False:
                        self.file2return.remove(file)
                        self.inputs4return.remove(input)
                        appendedJ.remove(J)




