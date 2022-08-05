import os
import Core
import datetime

import DataProcessing
import FromFile


class csvfile:
    csvname = ''
    pdosWanted = None
    charges_and_spinsWanted = None

    pdosDataStore = dict()
    charges_and_spinsDataStore = []

    def __init__(self):
        stem = Core.Extension().current_work_directory()  # ''.join(path_stem)
        filename = "processed_data.csv"
        self.datacsv = os.path.join(stem, filename)
        csvfile.CSVsaved(self.datacsv)

    @classmethod
    def CSVsaved(cls, csv):
        csvfile.csvname = csv

    def Overwrite(self):
        datafile = open(self.datacsv, 'w')  # "w" for overwrite file; "a" for append to file end
        datafile.write('# test as of %s. \n' % (datetime.datetime.now()))
        datafile.close()

    def Append(self):
        datafile = open(self.datacsv, 'a')
        datafile.write('# test as of %s. \n' % (datetime.datetime.now()))
        datafile.close()

    @classmethod
    def turnFalse(cls, variable):
        exec(f'csvfile.{variable}Wanted = False')

    @classmethod
    def turnTrue(cls, variable):
        exec(f'csvfile.{variable}Wanted = True')

    @classmethod
    def ChargeDirectory(cls):
        csvfile.charges_and_spinsDataStore = FromFile.SortingChargeStates.ProjectChargesStore

    @classmethod
    def PdosDirectory(cls, suffix, alphaHOMO, alphaLUMO, alphabandgap, betaHOMO, betaLUMO, betabandgap):
        results = dict()
        string = str(suffix)
        innerkeys = ["HOMO", "LUMO", "bandgap"]
        alphalist = [alphaHOMO, alphaLUMO, alphabandgap]
        betalist = [betaHOMO, betaLUMO, betabandgap]
        a = dict(zip(innerkeys, alphalist))
        b = dict(zip(innerkeys, betalist))
        results["alpha"] = a
        results["beta"] = b
        csvfile.pdosDataStore[string] = results

class Printing2CSV:
    def __init__(self, ProcesssingWants, rawinputs):
        self.ProcessingWants = ProcesssingWants
        self.rawinputs = rawinputs
        classvaribles4wants = []
        for input in list(self.rawinputs):
            classvaribles4wants.append(eval("csvfile.{}Wanted".format(input)))
        if all(x == True for x in classvaribles4wants):
            perfsubdir = Core.UserArguments.PerfectSubdir
            datacsv = open(csvfile.csvname, 'a')
            datacsv.write(str(perfsubdir) + '\n')
            for want, input in zip(list(self.ProcessingWants), list(self.rawinputs)):
                datacsv.write(str("     {}:".format(input)) + '\n')
                if want == 'charges and spins':
                    DataFrame = DataProcessing.CreateDataFrame4ResultsCSV(perfsubdir)
                    DataFrame.to_csv(path_or_buf=None, sep=',', na_rep='', float_format=None,
                                 columns=None, header=True, index=True, index_label=None, mode='w', encoding=None,
                                 compression='infer', quoting=None, quotechar='"', line_terminator=None,
                                 chunksize=None, date_format=None, doublequote=True, escapechar=None,
                                 decimal='.', errors='strict', storage_options=None)
                if want == 'pdos':
                    alpha = str(eval("csvfile.{}DataStore[perfsubdir]['alpha']".format(input))).replace('{', " ")
                    alpha = alpha.replace("}", "")
                    alpha = alpha.replace("'", "")
                    alpha = alpha.replace(":", "=")
                    beta = str(eval("csvfile.{}DataStore[perfsubdir]['beta']".format(input))).replace('{', " ")
                    beta = beta.replace("}", "")
                    beta = beta.replace("'", "")
                    beta = beta.replace(":", "=")
                    datacsv.write('          Alpha spin -' + alpha + '\n')
                    datacsv.write('          Beta spin -' + beta + '\n')
            self.defectsub = Core.UserArguments.DefectSubdir
            suffixs = Core.Extension().All_defect_subdir(".log", self.defectsub)[-1]
            for suffix in list(suffixs):
                datacsv.write(str(suffix) + '\n')
                for want, input in zip(list(self.ProcessingWants), list(self.rawinputs)):
                    if suffix in eval("csvfile.{}DataStore".format(input)):
                        datacsv.write(str("     {}:".format(want)) + '\n')
                        if want == 'pdos':
                            alpha = str(eval("csvfile.{}DataStore[suffix]['alpha']".format(input))).replace('{', " ")
                            alpha = alpha.replace("}", "")
                            alpha = alpha.replace("'", "")
                            alpha = alpha.replace(":", "=")
                            beta = str(eval("csvfile.{}DataStore[suffix]['beta']".format(input))).replace('{', " ")
                            beta = beta.replace("}", "")
                            beta = beta.replace("'", "")
                            beta = beta.replace(":", "=")
                            datacsv.write('          Alpha spin -' + alpha + '\n')
                            datacsv.write('          Beta spin -' + beta + '\n')

            datacsv.close()


