import FromFile
from Core import Extension

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
            inpfile = Extension().files4defect(".inp", subdir)
            logfile = Extension().files4defect(".log", subdir)
            FromFile.ChargeStateIdentification.__init__(self,inpfile)
            if self.state == 0:
                self.defneutral.append(logfile)
                self.neutralsubdir.append(subdir)
                self.inpneutral.append(inpfile)
                FromFile.NameOfProject.__init__(self, inpfile)
                self.namesneutral.append(self.project_name)

class CategorisingChargeStates(SetupSortingCharged, FromFile.ChargeStateIdentification, FromFile.NameOfProject):
    def __init__(self, subdirs):
        self.subdirs = subdirs
        SetupSortingCharged.__init__(self)
        for subdir in list(self.subdirs):
            inpfile = Extension().files4defect(".inp", subdir)
            logfile = Extension().files4defect(".log", subdir)
            for num in 1, 2, 3:
                if self.state == num:
                    exec(f'self.defpos{num}.append(logfile)')
                    exec(f'self.inppos{num}.append(inpfile)')
                    FromFile.NameOfProject.__init__(self, inpfile)
                    exec(f'self.namespos{num}.append(self.project_name)')
                if self.state == -num:
                    exec(f'self.defneg{num}.append(logfile)')
                    exec(f'self.inpneg{num}.append(inpfile)')
                    FromFile.NameOfProject.__init__(self,inpfile)
                    exec(f'self.namesneg{num}.append(self.project_name)')


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
    # def Return(self):
    #     return self.file2return


class SortingChargeStates(CategorisingChargeStates, ProjectSortingIt):
    # ProjectChargesStore = dict()
    def __init__(self, subdirs):
        CategorisingChargeStates.__init__(self, subdirs)
        for i in range(len(self.namesneutral)):
            exec(f'self.logfiles_{self.namesneutral} = []')
        for i in range(len(self.namesneutral)):
            name = self.namesneutral[i]
            neutral_file = self.defneutral[i]
            reference_inp = self.inpneutral[i]
            for sign in 'neg', 'pos':
                for num in 1, 2, 3:
                    if eval("self.def{}{}".format(sign,num)) != []:
                        ProjectSortingIt.__init__(self,name,eval("self.names{}{}".format(sign,num)),eval("self.def{}{}".format(sign,num)),eval("self.inp{}{}".format(sign,num)),reference_inp)
                        exec(f'self.logfiles_{self.namesneutral}.append(self.file2return)')
                    else:
                        exec(f'self.logfiles_{self.namesneutral}.append("-")')
        #
        #     subdir = self.neutralsubdir[i]
        #     self.ProjectDictionary(name, subdir, neutral_file, charged_logfiles)
        #
        # self.returnprojectnames()


        # return logfiles

    # @classmethod
    # def ProjectDictionary(cls, name, subdir, neutralfile, projectfiles):
    #     project = dict()
    #     string = str(name)
    #
    #     neutralinnerkeys = ["dirpath", "logfile"]
    #     neutrallist = [subdir, neutralfile]
    #     neutral = dict(zip(neutralinnerkeys,neutrallist))
    #     project['0'] = neutral
    #     project['-1'] = projectfiles[0]
    #     project['-2'] = projectfiles[1]
    #     project['-3'] = projectfiles[2]
    #     project['1'] = projectfiles[3]
    #     project['2'] = projectfiles[4]
    #     project['3'] = projectfiles[5]
    #
    #     SortingChargeStates.ProjectChargesStore[string] = project
    #



