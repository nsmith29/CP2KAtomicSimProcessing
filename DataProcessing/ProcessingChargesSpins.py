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

    def makingperfdata(self):
        SetupDataFrame.__init__(self)
        FromFile.GetChargesSpins.__init__(self, self.perffile)
        for index in self.indices:
            self.data4atomindex(index)
            for n in 1, 2:
                # exec(f'self.perf{index}_pop{n}_charge = self.pop{n}_charge')
                # exec(f'self.perf{index}_pop{n}_spin = self.pop{n}_spin')
                # exec(f'self.perf{index}_pop{n}_beta_pop = self.pop{n}_beta_pop')
                # exec(f'self.perf{index}_pop{n}_alpha_pop = self.pop{n}_alpha_pop')
                exec(f'self.chargesM{n}.append(self.pop{n}_charge)')#self.perf{index}_pop{n}_charge
                exec(f'self.spinsM{n}.append(self.pop{n}_spin)')#self.perf{index}_pop{n}_spin
                exec(f'self.popAM{n}.append(self.pop{n}_beta_pop)')#self.perf{index}_pop{n}_beta_pop
                exec(f'self.popBM{n}.append(self.pop{n}_alpha_pop)')#perf{index}_pop{n}_alpha_pop
        FromFile.GetChargesSpins.changingbackclassvars()

class PerfDataFrame(PerfChargeSpins):
    def __init__(self, answers):
        PerfChargeSpins.__init__(self, answers)
        self.makingperfdata()
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

# class DefectChargeSpins(FromFile.GetChargesSpins, LogfileChargeStateKey):
#     def __init__(self, name, i, file, indices):
#         LogfileChargeStateKey.__init__(self, i)
#         FromFile.GetChargesSpins.__init__(self, file)
#         for index in indices:
#             self.data4atomindex(index)
#             if Core.UserWants.AnalysisWants == 'n':
#                 self.string = str('{} {}, {}'.format(name, self.filestate, index))
#             else:
#                 self.string = str('{}, {}'.format(self.filestate, index))
#             for n in 1,2:
#                 exec(f'self.def_{self.filestatename}_{index}_pop{n}_charge = self.pop{n}_charge')
#                 exec(f'self.def_{self.filestatename}_{index}_pop{n}_spin = self.pop{n}_spin')
#                 exec(f'self.def_{self.filestatename}_{index}_pop{n}_beta_pop = self.pop{n}_beta_pop')
#                 exec(f'self.def_{self.filestatename}_{index}_pop{n}_alpha_pop = self.pop{n}_alpha_pop')


class DefectDataFrame(SortingChargeStatesOut, FromFile.GetChargesSpins, LogfileChargeStateKey, SetupDataFrame):#DefectChargeSpins
    def __init__(self, answers, neutralname, neutralinp, neutralfile):
        SetupDataFrame.__init__(self)
        # SortingChargeStatesOut.__init__(self, answers, neutralname, neutralinp)
        # DefectChargeSpins.__init__(self, neutralname, '-', neutralfile, self.indices)
        # for index in self.indices:
        LogfileChargeStateKey.__init__(self, '-')
        FromFile.GetChargesSpins.__init__(self, neutralfile)
        for index in self.indices:
            self.string = str('{}, {}'.format(self.filestate, index))
            self.columnstring.append(self.string)
            self.data4atomindex(index)
            for n in 1, 2:
                exec(f'self.chargesM{n}.append(self.pop{n}_charge)') #self.def_{self.filestatename}_{index}_pop{n}_charge
                exec(f'self.spinsM{n}.append(self.pop{n}_spin)') #self.def_{self.filestatename}_{index}_pop{n}_spin
                exec(f'self.popAM{n}.append(self.pop{n}_beta_pop)')#self.def_{self.filestatename}_{index}_pop{n}_beta_pop
                exec(f'self.popBM{n}.append(self.pop{n}_alpha_pop)')#self.def_{self.filestatename}_{index}_pop{n}_alpha_pop
        FromFile.GetChargesSpins.changingbackclassvars()
        SortingChargeStatesOut.__init__(self, answers, neutralname, neutralinp)
        for logfile, i in zip(list(self.logfiles), range(len(self.logfiles))):
            if logfile != "-":
                LogfileChargeStateKey.__init__(self, i)
                FromFile.GetChargesSpins.__init__(self, logfile)
                for index in self.indices:
                    #DefectChargeSpins.__init__(self, neutralname, i, logfile, index)
                    self.string = str('{}, {}'.format(self.filestate, index))
                    self.columnstring.append(self.string)
                    self.data4atomindex(index)
                    for n in 1, 2:
                        exec(f'self.chargesM{n}.append(self.pop{n}_charge)')#self.def_{self.filestatename}_{index}_pop{n}_charge
                        exec(f'self.spinsM{n}.append(self.pop{n}_spin)')#self.def_{self.filestatename}_{index}_pop{n}_spin
                        exec(f'self.popAM{n}.append(self.pop{n}_beta_pop)')#self.def_{self.filestatename}_{index}_pop{n}_beta_pop
                        exec(f'self.popBM{n}.append(self.pop{n}_alpha_pop)')#self.def_{self.filestatename}_{index}_pop{n}_alpha_pop
                FromFile.GetChargesSpins.changingbackclassvars()
        self.df = pd.DataFrame(
            [self.chargesM1, self.spinsM1, self.popAM1, self.popBM1, self.chargesM2, self.spinsM2, self.popAM2,
             self.popBM2],
            columns=self.columnstring, index=['Mulliken', '', '', '', 'Hirshfeld', '', '', ''])
        self.a = self.df.columns.str.split(', ', expand=True).values
        self.df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in self.a])


class ControlChargeSpins(PerfChargeSpins, SortingChargeStatesOut, FromFile.GetChargesSpins, LogfileChargeStateKey):
    def __init__(self, answers):
        PerfChargeSpins.__init__(self, answers)
        for neutralname, file, subdir, neutralinp in zip(list(self.namesneutral),list(self.defneutral), list(self.neutralsubdir),
                                                   list(self.inpneutral)):
            self.makingperfdata()
            for index in self.indices:
                string = str('{}, {}'.format(self.perfsubdir, index))
                self.columnstring.append(string)
            print(subdir)
            # columnstring = self.columnstring
            # chargesM1 = self.chargesM1
            # spinsM1 = self.spinsM1
            # popAM1 = self.popAM1
            # popBM1 = self.popBM1
            # chargesM2 = self.chargesM2
            # spinsM2 = self.spinsM2
            # popAM2 = self.popAM2
            # popBM2 = self.popBM2
            SortingChargeStatesOut.__init__(self, answers, neutralname, neutralinp)

            LogfileChargeStateKey.__init__(self, '-')
            FromFile.GetChargesSpins.__init__(self, file)
            for index in self.indices:
                # DefectChargeSpins.__init__(self, neutralname,'-', file, index)
                self.string = str('{} {}, {}'.format(neutralname, self.filestate, index))
                self.columnstring.append(self.string)
                self.data4atomindex(index)
                for n in 1,2:
                    exec(f'self.chargesM{n}.append(self.pop{n}_charge)')  # self.def_{self.filestatename}_{index}_pop{n}_charge
                    exec(f'self.spinsM{n}.append(self.pop{n}_spin)')  # self.def_{self.filestatename}_{index}_pop{n}_spin
                    exec(f'self.popAM{n}.append(self.pop{n}_beta_pop)')  # self.def_{self.filestatename}_{index}_pop{n}_beta_pop
                    exec(f'self.popBM{n}.append(self.pop{n}_alpha_pop)')  # self.def_{self.filestatename}_{index}_pop{n}_alpha_pop
            FromFile.GetChargesSpins.changingbackclassvars()
            for logfile, i in zip(list(self.logfiles), range(len(self.logfiles))):
                if logfile != "-":
                    LogfileChargeStateKey.__init__(self, i)
                    FromFile.GetChargesSpins.__init__(self, logfile)
                    for index in self.indices:
                        # DefectChargeSpins.__init__(self, neutralname, i, logfile, index)
                        self.string = str('{} {}, {}'.format(neutralname, self.filestate, index))
                        self.columnstring.append(self.string)
                        self.data4atomindex(index)
                        for n in 1, 2:
                            exec(f'self.chargesM{n}.append(self.pop{n}_charge)')  # self.def_{self.filestatename}_{index}_pop{n}_charge
                            exec(f'self.spinsM{n}.append(self.pop{n}_spin)')  # self.def_{self.filestatename}_{index}_pop{n}_spin
                            exec(f'self.popAM{n}.append(self.pop{n}_beta_pop)')  # self.def_{self.filestatename}_{index}_pop{n}_beta_pop
                            exec(f'self.popBM{n}.append(self.pop{n}_alpha_pop)')  # self.def_{self.filestatename}_{index}_pop{n}_alpha_pop
                    FromFile.GetChargesSpins.changingbackclassvars()
            # print(columnstring, '\n', chargesM1, '\n', spinsM1, '\n', popAM1, '\n', popBM1, '\n',  chargesM2, '\n', spinsM2, '\n', popAM2, '\n', popBM2)
            df = pd.DataFrame([self.chargesM1, self.spinsM1, self.popAM1, self.popBM1, self.chargesM2, self.spinsM2, self.popAM2, self.popBM2],
                              columns=self.columnstring, index=['Mulliken', '', '', '', 'Hirshfeld', '', '', ''])
            a = df.columns.str.split(', ', expand=True).values
            df.columns = pd.MultiIndex.from_tuples([('', x[0]) if pd.isnull(x[1]) else x for x in a])
            print(df)


