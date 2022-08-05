import FromFile
from Core import Extension
class SortingChargeStates:
    ProjectChargesStore = dict()
    def __init__(self, subdirs):
        self.subdirs = subdirs

        self.defneutral = []
        self.neutralsubdir = []
        self.namesneutral = []

        self.defneg1 = []
        self.namesneg1 = []
        self.defneg2 = []
        self.namesneg2 = []
        self.defneg3 = []
        self.namesneg3 = []

        self.defpos1 = []
        self.namespos1 = []
        self.defpos2 = []
        self.namespos2 = []
        self.defpos3 = []
        self.namespos3 = []

        self.CategorisingChargeStates()
        for i in range(len(self.namesneutral)):
            name = self.namesneutral[i]
            neutral_file = self.defneutral[i]
            charged_logfiles = self.Grouping4Projects(name, neutral_file)

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
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namesneutral.append(name)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == 1:
                self.defpos1.append(logfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namespos1.append(name)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == 2:
                self.defpos2.append(logfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namespos2.append(name)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == 3:
                self.defpos3.append(logfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namespos3.append(name)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == -1:
                self.defneg1.append(logfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namesneg1.append(name)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == -2:
                self.defneg2.append(logfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namesneg2.append(name)
            if FromFile.ChargeStateIdentification(inpfile).returnstate() == -3:
                self.defneg3.append(logfile)
                name = FromFile.NameOfProject(inpfile).ReturnName()
                self.namesneg3.append(name)

    def Grouping4Projects(self, name, file):
        ref = file.split('/')
        reference = ref[-2]
        logfiles = []

        if self.defneg1 != []:
            for j in range(len(self.namesneg1)):
                if name == self.namesneg1[j]:
                    logfiles.append(self.defneg1[j]) # need to do something here to make sure if there are multiple different calculation sets with same project name in inps that the correct charge state log.
                    if len(logfiles) >= 2:
                        for log in list(logfiles):
                            test = log.split('/')
                            Test = test[-2]
                            if Test != reference:
                                logfiles.remove(log)
        else:
            logfiles.append('-')

        if self.defneg2 != []:
            for j in range(len(self.namesneg2)):
                if name == self.namesneg2[j]:
                    logfiles.append(self.defneg2[j])
                    if len(logfiles) >= 3:
                        for log in list(logfiles):
                            if log != '-':
                                test = log.split('/')
                                Test = test[-2]
                                if Test != reference:
                                    logfiles.remove(log)
        else:
            logfiles.append('-')

        if self.defneg3 != []:
            for j in range(len(self.namesneg3)):
                if name == self.namesneg3[j]:
                    logfiles.append(self.defneg3[j])
                    if len(logfiles) >= 4:
                        for log in list(logfiles):
                            if log != '-':
                                test = log.split('/')
                                Test = test[-2]
                                if Test != reference:
                                    logfiles.remove(log)
        else:
            logfiles.append('-')

        if self.defpos1 != []:
            for j in range(len(self.namespos1)):
                if name == self.namespos1[j]:
                    logfiles.append(self.defpos1[j])
                    if len(logfiles) >= 5:
                        for log in list(logfiles):
                            if log != '-':
                                test = log.split('/')
                                Test = test[-2]
                                if Test != reference:
                                    logfiles.remove(log)
        else:
            logfiles.append('-')

        if self.defpos2 != []:
            for j in range(len(self.namespos2)):
                if name == self.namespos2[j]:
                    logfiles.append(self.defpos2[j])
                    if len(logfiles) >= 6:
                        for log in list(logfiles):
                            if log != '-':
                                test = log.split('/')
                                Test = test[-2]
                                if Test != reference:
                                    logfiles.remove(log)
        else:
            logfiles.append('-')

        if self.defpos3 != []:
            for j in range(len(self.namespos3)):
                if name == self.namespos3[j]:
                    logfiles.append(self.defpos3[j])
                    if len(logfiles) >= 7:
                        for log in list(logfiles):
                            if log != '-':
                                test = log.split('/')
                                Test = test[-2]
                                if Test != reference:
                                    logfiles.remove(log)
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