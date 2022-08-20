import pandas as pd

import Core
import FromFile
import Presentation
from Core import Extension

class SetupChargeSpins(FromFile.ReturnProjectNames):
    def __init__(self):
        self.perfsubdir = Core.UserArguments.PerfectSubdir
        self.perffile = Extension().perfect_subdir(".log", self.perfsubdir)

        self.defectsub = Core.UserArguments.DefectSubdir
        self.defsubdirs, self.defsuffixs = Extension().All_defect_subdir(".log", self.defectsub)
        FromFile.ReturnProjectNames.__init__(self, self.defsubdirs) #self.defneutral[logfiles], self.neutralsubdir[subdir], self.inpneutral[subdir], self.namesneutral[project_name]

class PerfChargeSpins(SetupChargeSpins, FromFile.GetChargesSpins):
    def __init__(self, indices):
        self.indices = indices.split(',')
        SetupChargeSpins.__init__(self)
        for index in self.indices:
            FromFile.GetChargesSpins.__init__(self,self.perffile,index)
            for n in 1, 2:
                exec(f'self.perf{index}_pop{n}_charge = self.pop{n}_charge')
                exec(f'self.perf{index}_pop{n}_spin = self.pop{n}_spin')
                exec(f'self.perf{index}_pop{n}_beta_pop = self.pop{n}_beta_pop')
                exec(f'self.perf{index}_pop{n}_alpha_pop = self.pop{n}_alpha_pop')

class ControlChargeSpins(PerfChargeSpins):
    charges_and_spinsData = dict()
    Indices = []
    def __init__(self, answers):
        PerfChargeSpins.__init__(self, answers)


        self.CreateDictionary(self.perfsubdir, self.perffile, self.indices)

        # self.defectsub = Core.UserArguments.DefectSubdir
        # self.defsubdirs, self.defsuffixs = Extension().All_defect_subdir(".log", self.defectsub)
        #
        # self.projectnames = FromFile.SortingChargeStates(self.defsubdirs).returnprojectnames()
        #
        # if Core.UserWants.AnalysisWants == 'n':
        #     Presentation.csvfile.ChargeDirectory()
        #     Presentation.csvfile.turnTrue("charges_and_spins")
        #
        # for name in list(self.projectnames):
        #     self.CreateDictionary(name, 'blank', self.indices)
        #
        # self.CreateDataFrame4Results()


    @classmethod
    def CreateDictionary(cls, projectname, filename, indices):
        entry = dict()
        projectstring = str(projectname)
        neutral = []
        for index in list(indices):
            atomindex = dict()
            if projectname == Core.UserArguments.PerfectSubdir:
                pop1charge, pop1spin, pop1popA, pop1popB, pop2charge, pop2spin, pop2popA, pop2popB = FromFile.GetChargesSpins(filename, index).returnchargespins()
            # else:
            #     pop1charge, pop1spin, pop1popA, pop1popB, pop2charge, pop2spin, pop2popA, pop2popB = FromFile.GetChargesSpins(FromFile.SortingChargeStates.ProjectChargesStore[projectstring]["0"]["logfile"],index).returnchargespins()
            atom = []
            innerkeys = ["Method", "spin", "charge", "pop a", "pop b"]
            method1 = ["Mulliken", pop1spin, pop1charge, pop1popA, pop1popB]
            method2 = ["Hirshfield", pop2spin, pop2charge, pop2popA, pop2popB]

            method1dict = dict(zip(innerkeys, method1))
            method2dict = dict(zip(innerkeys, method2))
            atom.append(method1dict)
            atom.append(method2dict)
            atomindex[index] = atom
            neutral.append(atomindex)
        entry["0"] = neutral
        # if projectname != Core.UserArguments.PerfectSubdir:
        #     Arrneg1 = []
        #     Arrneg2 = []
        #     Arrneg3 = []
        #     Arrpos1 = []
        #     Arrpos2 = []
        #     Arrpos3 = []
        #     for state, key in zip(('neg1', 'neg2', 'neg3', 'pos1', 'pos2', 'pos3'), ("-1","-2","-3","1","2","3")):
        #         if FromFile.SortingChargeStates.ProjectChargesStore[projectstring][str("{}".format(key))] != '-':
        #             for index in list(indices):
        #                 atomindex = dict()
        #                 atom = []
        #                 pop1charge, pop1spin, pop1popA, pop1popB, pop2charge, pop2spin, pop2popA, pop2popB = FromFile.GetChargesSpins(FromFile.SortingChargeStates.ProjectChargesStore[projectstring][str("{}".format(key))],index).returnchargespins()
        #                 innerkeys = ["Method", "spin", "charge", "pop a", "pop b"]
        #                 method1 = ["Mulliken", pop1spin, pop1charge, pop1popA, pop1popB]
        #                 method2 = ["Hirshfield", pop2spin, pop2charge, pop2popA, pop2popB]
        #
        #                 method1dict = dict(zip(innerkeys, method1))
        #                 method2dict = dict(zip(innerkeys, method2))
        #                 atom.append(method1dict)
        #                 atom.append(method2dict)
        #                 atomindex[index] = atom
        #                 exec(f'Arr{state}.append(atomindex)')
        #             entry[str("{}".format(key))] = eval("Arr{}".format(state))
        ControlChargeSpins.charges_and_spinsData[projectstring] = entry

    def CreateDataFrame4Results(self):
        for name in list(self.projectnames):
            columnstring = [' ']
            chargesM1 = ["charge"]
            spinsM1 = ["spin"]
            popAM1 = ["pop \u03B1"]
            popBM1 = ["pop \u03B2"]
            chargesM2 = ["charge"]
            spinsM2 = ["spin"]
            popAM2 = ["pop \u03B1"]
            popBM2 = ["pop \u03B2"]
            for index in self.indices:
                string = str('{}, {}'.format(self.perfsubdir,index))
                columnstring.append(string)
                for i in range(len(ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"])):
                    if index in ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i]:
                        chargetest = round(float(ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][0]['charge']),3)
                        chargesM1.append(chargetest)
                        spintest = round(float(ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][0]['spin']),3)
                        spinsM1.append(spintest)
                        popAtest = round(float(ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][0]['pop a']),3)
                        popAM1.append(popAtest)
                        popBtest = round(float(ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][0]['pop b']),3)
                        popBM1.append(popBtest)

                        chargetest2 = ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][1]['charge']
                        chargesM2.append(chargetest2)
                        spintest2 = ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][1]['spin']
                        spinsM2.append(spintest2)
                        popAtest2 = ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][1]['pop a']
                        popAM2.append(popAtest2)
                        popBtest2 = ControlChargeSpins.charges_and_spinsData[self.perfsubdir]["0"][i][index][1]['pop b']
                        popBM2.append(popBtest2)

            for state in list(ControlChargeSpins.charges_and_spinsData[name]):
                for index in self.indices:
                    string = str('{} {}, {}'.format(name, state, index))
                    columnstring.append(string)
                    for i in range(len(ControlChargeSpins.charges_and_spinsData[name][state])):
                        if index in ControlChargeSpins.charges_and_spinsData[name][state][i]:
                            chargetest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['charge']),3)
                            chargesM1.append(chargetest)
                            spintest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['spin']),3)
                            spinsM1.append(spintest)
                            popAtest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['pop a']),3)
                            popAM1.append(popAtest)
                            popBtest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['pop b']),3)
                            popBM1.append(popBtest)

                            chargetest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['charge']
                            chargesM2.append(chargetest2)
                            spintest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['spin']
                            spinsM2.append(spintest2)
                            popAtest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['pop a']
                            popAM2.append(popAtest2)
                            popBtest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['pop b']
                            popBM2.append(popBtest2)

            df = pd.DataFrame([chargesM1, spinsM1, popAM1, popBM1,chargesM2, spinsM2, popAM2, popBM2], columns=columnstring, index=['Mulliken', '', '', '','Hirshfeld', '', '', ''])
            a = df.columns.str.split(', ', expand=True).values
            df.columns = pd.MultiIndex.from_tuples([('',x[0]) if pd.isnull(x[1]) else x for x in a])
            print(df)

class CreateDataFrame4ResultsCSV:
    def __init__(self, name):
        self.indices = ControlChargeSpins.Indices
        self.perfsubdir = Core.UserArguments.PerfectSubdir
        columnstring = [' ']
        chargesM1 = ["charge"]
        spinsM1 = ["spin"]
        popAM1 = ["pop \u03B1"]
        popBM1 = ["pop \u03B2"]
        chargesM2 = ["charge"]
        spinsM2 = ["spin"]
        popAM2 = ["pop \u03B1"]
        popBM2 = ["pop \u03B2"]
        if name == Core.UserArguments.PerfectSubdir:
            for index in self.indices:
                string = str('{}, {}'.format(self.perfsubdir,index))
                columnstring.append(string)
                for i in range(len(ControlChargeSpins.charges_and_spinsData[name]["0"])):
                    if index in ControlChargeSpins.charges_and_spinsData[name]["0"][i]:
                        chargetest = round(float(ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][0]['charge']),3)
                        chargesM1.append(chargetest)
                        spintest = round(float(ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][0]['spin']),3)
                        spinsM1.append(spintest)
                        popAtest = round(float(ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][0]['pop a']),3)
                        popAM1.append(popAtest)
                        popBtest = round(float(ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][0]['pop b']),3)
                        popBM1.append(popBtest)

                        chargetest2 = ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][1]['charge']
                        chargesM2.append(chargetest2)
                        spintest2 = ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][1]['spin']
                        spinsM2.append(spintest2)
                        popAtest2 = ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][1]['pop a']
                        popAM2.append(popAtest2)
                        popBtest2 = ControlChargeSpins.charges_and_spinsData[name]["0"][i][index][1]['pop b']
                        popBM2.append(popBtest2)
        else:
            for state in list(ControlChargeSpins.charges_and_spinsData[name]):
                for index in self.indices:
                    string = str('{} {}, {}'.format(name, state, index))
                    columnstring.append(string)
                    for i in range(len(ControlChargeSpins.charges_and_spinsData[name][state])):
                        if index in ControlChargeSpins.charges_and_spinsData[name][state][i]:
                            chargetest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['charge']),3)
                            chargesM1.append(chargetest)
                            spintest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['spin']),3)
                            spinsM1.append(spintest)
                            popAtest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['pop a']),3)
                            popAM1.append(popAtest)
                            popBtest = round(float(ControlChargeSpins.charges_and_spinsData[name][state][i][index][0]['pop b']),3)
                            popBM1.append(popBtest)

                            chargetest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['charge']
                            chargesM2.append(chargetest2)
                            spintest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['spin']
                            spinsM2.append(spintest2)
                            popAtest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['pop a']
                            popAM2.append(popAtest2)
                            popBtest2 = ControlChargeSpins.charges_and_spinsData[name][state][i][index][1]['pop b']
                            popBM2.append(popBtest2)

            df = pd.DataFrame([chargesM1, spinsM1, popAM1, popBM1,chargesM2, spinsM2, popAM2, popBM2], columns=columnstring, index=['Mulliken', '', '', '','Hirshfeld', '', '', ''])
            a = df.columns.str.split(', ', expand=True).values
            df.columns = pd.MultiIndex.from_tuples([('',x[0]) if pd.isnull(x[1]) else x for x in a])
