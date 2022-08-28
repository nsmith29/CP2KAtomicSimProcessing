import pandas as pd
import Core
import FromFile
# import Presentation


class SetupChargeSpins(FromFile.ReturnProjectNames,FromFile.CategorisingChargeStates):
    def __init__(self):
        self.perfsubdir = Core.UserArguments.PerfectSubdir
        self.perffile = Core.Extension().perfect_subdir(".log", self.perfsubdir)

        self.defectsub = Core.UserArguments.DefectSubdir
        self.defsubdirs, self.defsuffixs = Core.Extension().All_defect_subdir(".log", self.defectsub)
        FromFile.ReturnProjectNames.__init__(self, self.defsubdirs) #self.defneutral[logfiles], self.neutralsubdir[subdir], self.inpneutral[subdir], self.namesneutral[project_name]
        FromFile.CategorisingChargeStates.__init__(self, self.defsubdirs)

class SetupDataFrame:
    def __init__(self):
        self.columnstring = [' ']
        self.chargesM1 = ["charge"]
        self.spinsM1 = ["spin"]
        self.popAM1 = ["pop \u03B1"]
        self.popBM1 = ["pop \u03B2"]
        self.chargesM2 = ["charge"]
        self.spinsM2 = ["spin"]
        self.popAM2 = ["pop \u03B1"]
        self.popBM2 = ["pop \u03B2"]

class PerfChargeSpins(SetupChargeSpins, FromFile.GetChargesSpins, SetupDataFrame):
    def __init__(self, indices):
        self.indices = indices.replace(' ', '').split(',')
        SetupChargeSpins.__init__(self)
        SetupDataFrame.__init__(self)
        for index in self.indices:
            FromFile.GetChargesSpins.__init__(self,self.perffile,index)
            for n in 1, 2:
                exec(f'self.perf{index}_pop{n}_charge = self.pop{n}_charge')
                exec(f'self.perf{index}_pop{n}_spin = self.pop{n}_spin')
                exec(f'self.perf{index}_pop{n}_beta_pop = self.pop{n}_beta_pop')
                exec(f'self.perf{index}_pop{n}_alpha_pop = self.pop{n}_alpha_pop')
                exec(f'self.chargesM{n}.append(self.perf{index}_pop{n}_charge)')
                exec(f'self.spinsM{n}.append(self.perf{index}_pop{n}_spin)')
                exec(f'self.popAM{n}.append(self.perf{index}_pop{n}_beta_pop)')
                exec(f'self.popBM{n}.append(self.perf{index}_pop{n}_alpha_pop)')

class PerfDataFrame(PerfChargeSpins):
    def __init__(self, answers):
        PerfChargeSpins.__init__(self, answers)

        for index in self.indices:
            string = str('{}'.format(index))
            self.columnstring.append(string)


        self.df = pd.DataFrame([self.chargesM1, self.spinsM1, self.popAM1, self.popBM1, self.chargesM2, self.spinsM2, self.popAM2, self.popBM2],
                          columns=self.columnstring, index=['Mulliken', '', '', '', 'Hirshfeld', '', '', ''])
        # self.a = self.df.columns.str.split(', ', expand=True).values
        # self.df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in self.a])

class SortingChargeStatesOut(SetupChargeSpins, FromFile.ProjectSortingIt):
    def __init__(self, indices, neutralname, neutralinp):
        self.indices = indices.replace(' ', '').split(',')
        SetupChargeSpins.__init__(self)

        self.logfiles = []
        for sign in 'neg', 'pos':
            for num in 1, 2, 3:
                if eval("self.def{}{}".format(sign, num)) != []:
                    FromFile.ProjectSortingIt.__init__(self, neutralname, eval("self.names{}{}".format(sign, num)),
                                              eval("self.def{}{}".format(sign, num)),
                                              eval("self.inp{}{}".format(sign, num)), neutralinp)
                    self.logfiles.append(self.file2return[0])
                else:
                    self.logfiles.append("-")

class LogfileChargeStateKey:
    def __init__(self, i):
        if i == '-':
            self.filestate = 0
            self.filestatename = 0
        elif i == 0:
            self.filestate = -1
            self.filestatename = '_1'
        elif i == 1:
            self.filestate = -2
            self.filestatename = '_2'
        elif i == 2:
            self.filestate = -3
            self.filestatename = '_3'
        elif i == 3:
            self.filestate = 1
            self.filestatename = 1
        elif i == 4:
            self.filestate = 2
            self.filestatename = 2
        elif i == 5:
            self.filestate = 3
            self.filestatename = 3

class DefectChargeSpins(FromFile.GetChargesSpins, LogfileChargeStateKey):
    def __init__(self, name, i, file, index):
        LogfileChargeStateKey.__init__(self, i)
        self.string = str('{} {}, {}'.format(name, self.filestate, index))
        FromFile.GetChargesSpins.__init__(self, file, index)
        for n in 1,2:
            exec(f'self.def_{self.filestatename}_{index}_pop{n}_charge = self.pop{n}_charge')
            exec(f'self.def_{self.filestatename}_{index}_pop{n}_spin = self.pop{n}_spin')
            exec(f'self.def_{self.filestatename}_{index}_pop{n}_beta_pop = self.pop{n}_beta_pop')
            exec(f'self.def_{self.filestatename}_{index}_pop{n}_alpha_pop = self.pop{n}_alpha_pop')

class DefectDataFrame(SortingChargeStatesOut, DefectChargeSpins, SetupDataFrame):
    def __init__(self, answers, neutralname, neutralinp, neutralfile):
        SetupDataFrame.__init__(self)
        SortingChargeStatesOut.__init__(self, answers, neutralname, neutralinp)
        for index in self.indices:
            DefectChargeSpins.__init__(self, neutralname, '-', neutralfile, index)
            string = str('{}, {}'.format(self.filestate, index))
            self.columnstring.append(string)
            for n in 1, 2:
                exec(f'self.chargesM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_charge)')
                exec(f'self.spinsM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_spin)')
                exec(f'self.popAM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_beta_pop)')
                exec(f'self.popBM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_alpha_pop)')
        for logfile, i in zip(list(self.logfiles), range(len(self.logfiles))):
            if logfile != "-":
                for index in self.indices:
                    DefectChargeSpins.__init__(self, neutralname, i, logfile, index)
                    string = str('{}, {}'.format(self.filestate, index))
                    self.columnstring.append(string)
                    for n in 1, 2:
                        exec(f'self.chargesM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_charge)')
                        exec(f'self.spinsM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_spin)')
                        exec(f'self.popAM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_beta_pop)')
                        exec(f'self.popBM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_alpha_pop)')
        self.df = pd.DataFrame(
            [self.chargesM1, self.spinsM1, self.popAM1, self.popBM1, self.chargesM2, self.spinsM2, self.popAM2,
             self.popBM2],
            columns=self.columnstring, index=['Mulliken', '', '', '', 'Hirshfeld', '', '', ''])
        self.a = self.df.columns.str.split(', ', expand=True).values
        self.df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in self.a])


class ControlChargeSpins(PerfChargeSpins, SortingChargeStatesOut, DefectChargeSpins):
    def __init__(self, answers):
        PerfChargeSpins.__init__(self, answers)
        for index in self.indices:
            string = str('{}, {}'.format(self.perfsubdir, index))
            self.columnstring.append(string)
        for neutralname, file, subdir, neutralinp in zip(list(self.namesneutral),list(self.defneutral), list(self.neutralsubdir),
                                                   list(self.inpneutral)):
            print(subdir)
            columnstring = self.columnstring
            chargesM1 = self.chargesM1
            spinsM1 = self.spinsM1
            popAM1 = self.popAM1
            popBM1 = self.popBM1
            chargesM2 = self.chargesM2
            spinsM2 = self.spinsM2
            popAM2 = self.popAM2
            popBM2 = self.popBM2
            SortingChargeStatesOut.__init__(self, answers, neutralname, neutralinp)

            for index in self.indices:
                DefectChargeSpins.__init__(self, neutralname,'-', file, index)
                columnstring.append(self.string)
                for n in 1,2:
                    exec(f'chargesM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_charge)')
                    exec(f'spinsM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_spin)')
                    exec(f'popAM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_beta_pop)')
                    exec(f'popBM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_alpha_pop)')
            for logfile, i in zip(list(self.logfiles), range(len(self.logfiles))):
                if logfile != "-":
                    for index in self.indices:
                        DefectChargeSpins.__init__(self, neutralname, i, logfile, index)
                        columnstring.append(self.string)
                        for n in 1, 2:
                            exec(f'chargesM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_charge)')
                            exec(f'spinsM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_spin)')
                            exec(f'popAM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_beta_pop)')
                            exec(f'popBM{n}.append(self.def_{self.filestatename}_{index}_pop{n}_alpha_pop)')

            # print(columnstring, '\n', chargesM1, '\n', spinsM1, '\n', popAM1, '\n', popBM1, '\n',  chargesM2, '\n', spinsM2, '\n', popAM2, '\n', popBM2)
            df = pd.DataFrame([chargesM1, spinsM1, popAM1, popBM1, chargesM2, spinsM2, popAM2, popBM2],
                              columns=columnstring, index=['Mulliken', '', '', '', 'Hirshfeld', '', '', ''])
            a = df.columns.str.split(', ', expand=True).values
            df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in a])
            print(df)


