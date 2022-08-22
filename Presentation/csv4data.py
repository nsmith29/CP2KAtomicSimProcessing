import os
import Core
import datetime
import DataProcessing
import multiprocessing as mp

class csvfile:
    csvname = ''
    pdosWanted = None
    charges_and_spinsWanted = None

    pdosDataStore = dict()
    charges_and_spinsDataStore = []

    def __init__(self):
        stem = Core.Extension().current_work_directory()
        filename = "processed_data.csv"
        self.datacsv = os.path.join(stem, filename)
        csvfile.CSVsaved(self.datacsv)

    @classmethod
    def CSVsaved(cls, csv):
        csvfile.csvname = csv

    def Overwrite(self):
        datafile = open(self.datacsv, 'w')
        datafile.write('# test as of %s. \n' % (datetime.datetime.now()))
        datafile.close()

    def Append(self):
        datafile = open(self.datacsv, 'a')
        datafile.write('# test as of %s. \n' % (datetime.datetime.now()))
        datafile.close()

class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)

    def run(self):
        try:
            mp.Process.run(self)
        except TypeError:
                pass

class Data4perfect(DataProcessing.NoAnalysisPerfect, DataProcessing.PerfDataFrame):
    def __init__(self):
        self.analysisperf0 = None
        self.analysisperf1 = None
        for i in range(len(Core.ProcessingControls.ProcessingWants)):
            if Core.ProcessingControls.ProcessingWants[i] == 'pdos':
                DataProcessing.NoAnalysisPerfect.__init__(self)
                exec(f'self.analysisperf{i} = "          Alpha spin -" + str(self.perfHOMO_alpha) + "  " + '
                     f'str(self.perfLUMO_alpha) + "  " + str(self.perfalpha_diff) + """\n""" + "          Beta spin -" + '
                     f'str(self.perfHOMO_beta) + "  " + str(self.perfLUMO_beta) + "  " + str(self.perfalpha_diff) + """\n""" ')
            if Core.ProcessingControls.ProcessingWants[i] == 'charges and spins':
                answers = Core.ProcessingControls.Followups[i]
                DataProcessing.PerfDataFrame.__init__(self, answers)
                exec(f'self.analysisperf{i} = self.df.to_csv()')

class DefectSubDirsOrdering(DataProcessing.SetUpPdos, DataProcessing.SetupChargeSpins):
    def __init__(self):
        self.subdirs0 = []
        self.subdirs1 = []
        self.orderedprinting = []
        self.suffixs0 = []
        self.suffixs1 = []
        self.orderedsuffixs = []
        for i in range(len(Core.ProcessingControls.ProcessingWants)):
            if Core.ProcessingControls.ProcessingWants[i] == 'pdos':
                DataProcessing.SetUpPdos.__init__(self)
                exec(f'self.subdirs{i} = self.subdirs')
                exec(f'self.suffixs{i} = self.suffixs')
            if Core.ProcessingControls.ProcessingWants[i] == 'charges and spins':
                DataProcessing.SetupChargeSpins.__init__(self)
                exec(f'self.subdirs{i} = self.neutralsubdir')
                exec(f'self.suffixs{i} = self.defsuffixs')

        if self.subdirs1 != []:
            for dir, suffix in zip(list(self.subdirs0), list(self.suffixs0)):
                if dir in self.subdirs1:
                    self.orderedprinting.append(dir)
                    self.orderedsuffixs.append(suffix)
                    self.subdirs0.remove(dir)
                    self.suffixs0.remove(suffix)
                    self.subdirs1.remove(dir)
                    self.suffixs1.remove(suffix)
        else:
            self.orderedprinting = self.subdirs0
            self.orderedsuffixs = self.suffixs0
            self.subdirs0 = []
            self.suffixs0 = []

class CollectingDefectPdosData(DataProcessing.NoAnalysisDefects):
    def __init__(self, subdir, j):
        exec(f'self.analysisdef{j} = None')
        DataProcessing.SetUpPdos.__init__(self)
        subdirindex = self.subdirs.index(subdir)
        pdosfile = self.defpdos[subdirindex]
        DataProcessing.NoAnalysisDefects.__init__(self, pdosfile)
        exec(f'self.analysisdef{j} = "          Alpha spin -" + str(self.defHOMO_alpha) + "  " + '
             f'str(self.defLUMO_alpha) + "  " + str(self.defalpha_diff) + """\n""" + "          Beta spin -" + '
             f'str(self.defHOMO_beta) + "  " + str(self.defLUMO_beta) + "  " + str(self.defalpha_diff) + """\n""" ')

class CollectingDefectChargeSpinData(DataProcessing.DefectDataFrame):
    def __init__(self, subdir, j):
        exec(f'self.analysisdef{j} = None')
        answers = Core.ProcessingControls.Followups[j]
        DataProcessing.SetupChargeSpins.__init__(self)
        subdirindex = self.neutralsubdir.index(subdir)
        neutralname = self.namesneutral[subdirindex]
        neutralinp = self.inpneutral[subdirindex]
        neutralfile = self.defneutral[subdirindex]
        DataProcessing.DefectDataFrame.__init__(self, answers, neutralname, neutralinp, neutralfile)
        exec(f'self.analysisdef{j} = self.df.to_csv()')

class Data4Defect(CollectingDefectPdosData, CollectingDefectChargeSpinData):
    def __init__(self, subdir, i, which):
        self.analysisdef0 = None
        self.analysisdef1 = None
        if i == len(Core.ProcessingControls.ProcessingWants):
            for j in range(len(Core.ProcessingControls.ProcessingWants)):
                if Core.ProcessingControls.ProcessingWants[j] == 'pdos':
                    CollectingDefectPdosData.__init__(self, subdir, j)
                if Core.ProcessingControls.ProcessingWants[j] == 'charges and spins':
                    CollectingDefectChargeSpinData.__init__(self, subdir, j)
        elif i == 1:
            if Core.ProcessingControls.ProcessingWants[which] == 'pdos':
                CollectingDefectPdosData.__init__(self, subdir, which)
            if Core.ProcessingControls.ProcessingWants[which] == 'charges and spins':
                CollectingDefectChargeSpinData.__init__(self, subdir, which)
            print('hi')

class Printing2CSV(Data4perfect, Data4Defect, DefectSubDirsOrdering):
    def __init__(self):
        perfsubdir = Core.UserArguments.PerfectSubdir
        datacsv = open(csvfile.csvname, 'a')
        datacsv.write(str(perfsubdir) + '\n')
        Data4perfect.__init__(self)
        input = Core.ProcessingControls.ProcessingWants[0]
        datacsv.write(str("     {}:".format(input)) + '\n')
        datacsv.write(self.analysisperf0)
        if self.analysisperf1 != None:
            input = Core.ProcessingControls.ProcessingWants[1]
            datacsv.write(str("     {}:".format(input)) + '\n')
            datacsv.write(self.analysisperf1)
        DefectSubDirsOrdering.__init__(self)
        for subdir, suffix in zip(list(self.orderedprinting), list(self.orderedsuffixs)):
            datacsv.write(str(suffix) + '\n')
            i = len(Core.ProcessingControls.ProcessingWants)
            Data4Defect.__init__(self, subdir, i, '-')
            input = Core.ProcessingControls.ProcessingWants[0]
            datacsv.write(str("     {}:".format(input)) + '\n')
            datacsv.write(self.analysisdef0)
            if self.analysisdef1 != None:
                input = Core.ProcessingControls.ProcessingWants[1]
                datacsv.write(str("     {}:".format(input)) + '\n')
                datacsv.write(self.analysisperf1)
        if self.subdirs0 != []:
            for subdir in list(self.subdirs0):
                datacsv.write(str(subdir) + '\n')
                Data4Defect.__init__(self, subdir, 1, 0)
                input = Core.ProcessingControls.ProcessingWants[0]
                datacsv.write(str("     {}:".format(input)) + '\n')
                datacsv.write(self.analysisdef0)
        if self.subdirs1 != []:
            for subdir in list(self.subdirs1):
                datacsv.write(str(subdir) + '\n')
                Data4Defect.__init__(self, subdir, 1, 1)
                input = Core.ProcessingControls.ProcessingWants[1]
                datacsv.write(str("     {}:".format(input)) + '\n')
                datacsv.write(self.analysisdef1)
        datacsv.close()


