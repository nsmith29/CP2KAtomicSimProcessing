import os
import sys
import multiprocessing as mp
import Core
import GUIwidgets
import Presentation
import DataProcessing
import ResultsAnalysis

os.chdir('/Users/appleair/Desktop/PhD/Jupyter_notebooks/Calculations/PBE0_impurities_analysis/Only_PBE0')

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Start:
    PerfectSubdir = ''
    DefectSubdir = ''
    ChemicalPotSubdir = ''
    def __init__(self, *argv):
        if len(sys.argv) == 5:
            perf_subdir = sys.argv[1]
            def_subdir = sys.argv[2]
            chempot_subdir = sys.argv[3]
            Core.UserArguments(perf_subdir, def_subdir,chempot_subdir)
            check = self.check_users_wants()

        elif len(sys.argv) >= 6:
            perf_subdir = sys.argv[1]
            def_subdir = sys.argv[2]
            chem_pot_subdir = sys.argv[3]

            if sys.argv[4] == 'only':
                self.keywrd = sys.argv[4]
                if len(sys.argv) == 6:
                    self.only = sys.argv[5]
                else:
                    self.only = []
                    for i in range(5, len(sys.argv)):
                        n = sys.argv[i]
                        self.only.append(n)
                Arguments = Core.UserArguments(perf_subdir, def_subdir, chem_pot_subdir)
                Arguments.OnlyStated(self.only)
            elif sys.argv[4] == 'except':
                self.keywrd = sys.argv[4]
                if len(sys.argv) == 6:
                    self.expt = sys.argv[5]
                else:
                    self.expt = []
                    for i in range(5, len(sys.argv)):
                        n = sys.argv[i]
                        self.expt.append(n)
                Arguments = Core.UserArguments(perf_subdir, def_subdir, chem_pot_subdir)
                Arguments.ExceptionStated(self.expt)
            check = self.check_users_wants()

        else:
            print(f"{bcolors.FAIL}Wrong number of or invalid arguments!")
            print(f"{bcolors.WARNING}Valid usage includes:")
            print(f"{bcolors.ENDC}{bcolors.BOLD}./MAIN.py perf_struc_subdir_name defect_struc_subdir_name chem_pot_"
                  f"subdir_name all")
            print(
                "./MAIN.py perf_struc_subdir_name defect_struc_subdir_name chem_pot_subdir_name only str_in_defect_"
                "subsubdir_name")
            print(
                f"./MAIN.py perf_struc_subdir_name defect_struc_subdir_name chem_pot_subdir_name except str_in_defect"
                f" subsubdir_name{bcolors.ENDC}")


    def check_users_wants(self):
        print(f"{bcolors.OKGREEN}Which results would you like to process?")
        processing = input(
            f"{bcolors.ENDC}Results options include: {bcolors.BOLD}band structure{bcolors.ENDC}, {bcolors.BOLD}charges "
            f"and spins{bcolors.ENDC}, {bcolors.BOLD}charge transition levels{bcolors.ENDC}, {bcolors.BOLD}geometry"
            f"{bcolors.ENDC}, {bcolors.BOLD}IPR{bcolors.ENDC}, {bcolors.BOLD}pdos{bcolors.ENDC}, {bcolors.BOLD}wfn"
            f"{bcolors.ENDC}, {bcolors.BOLD}work function{bcolors.ENDC} : ")
        while all(x not in processing for x in ["wfn", "geometry", "band structure", "work function", "IPR", "pdos",
                               "charges and spin", "charge transition levels", "test"]):
            print(f"{bcolors.FAIL}Error! {bcolors.WARNING}Invalid results type stated, valid methods to choose from "
                  f"include:{bcolors.ENDC}{bcolors.BOLD}band structure{bcolors.ENDC}, {bcolors.BOLD}charges and spins{bcolors.ENDC},"
            f"{bcolors.BOLD}charge transition levels{bcolors.ENDC}, {bcolors.BOLD}geometry{bcolors.ENDC}, {bcolors.BOLD}"
                  f"IPR{bcolors.ENDC}, "
            f" {bcolors.BOLD}pdos{bcolors.ENDC}, {bcolors.BOLD}wfn{bcolors.ENDC}, {bcolors.BOLD}work function"
                  f"{bcolors.ENDC}: ")
            processing = input(f"{bcolors.OKGREEN}Which results would you like to process?: {bcolors.ENDC}")

        self.followupQs = []
        processing = processing.split(', ')
        for i in range(len(processing)):
            if processing[i].find('band structure') != -1:
                followup3 = input(f"{bcolors.OKCYAN}What version of CP2K were calculations conducted with (i.e. CP2K "
                                  f"v8.1)?: {bcolors.ENDC}")
                self.followupQs.append(followup3)
            if processing[i].find('charges and spin') != -1:
                followup1 = input(f"{bcolors.OKCYAN}Please state the indices of nearest atomic neighbours surrounding "
                                  f"defect and the index of the defect:{bcolors.ENDC} ")
                self.followupQs.append(followup1)
            if processing[i].find('charge transition levels') != -1:
                followup4 = input(f"{bcolors.OKCYAN}Please state the charge states you have investigated ({bcolors.BOLD}e.g."
                                  f" 0, -2, etc{bcolors.ENDC}{bcolors.OKCYAN}): {bcolors.ENDC} ")
                self.followupQs.append(followup4)
            if processing[i].find('geometry') != -1:
                print(f"{bcolors.OKCYAN}Please state the types of defect(s) being studied and the associated atomic index of"
                      f" this defect in format'{bcolors.BOLD}defect type, atom index'{bcolors.ENDC}{bcolors.OKCYAN}")
                followup5 = input(f"{bcolors.OKCYAN}Defects type options include: {bcolors.BOLD}substitutional{bcolors.ENDC}"
                                  f"{bcolors.OKCYAN}, {bcolors.BOLD}interstitional{bcolors.ENDC}{bcolors.OKCYAN}, "
                                  f"{bcolors.BOLD}vacancy{bcolors.ENDC}{bcolors.OKCYAN}, {bcolors.OKCYAN}subs-vacancy "
                                  f"complex{bcolors.ENDC}{bcolors.OKCYAN}, {bcolors.BOLD}inter-vacancy complex{bcolors.ENDC}"
                                  f"{bcolors.OKCYAN}: {bcolors.ENDC}")
                self.followupQs.append(followup5)
            if processing[i].find('IPR') != -1:
                followup2 = input(f"{bcolors.OKCYAN}Are your calculation spin polarised({bcolors.BOLD}y/n{bcolors.BOLD}"
                                  f"{bcolors.OKCYAN})?: {bcolors.ENDC}")
                self.followupQs.append(followup2)
            if processing[i].find('pdos') != -1:
               self.followupQs.append('-')
            if processing[i].find('wfn') != -1:
               self.followupQs.append('-')
            if processing[i].find('work function') != -1:
                self.followupQs.append('-')

        print(f"{bcolors.OKGREEN}Would you like to perform data analysis({bcolors.BOLD}y/n{bcolors.ENDC}"
              f"{bcolors.OKGREEN})?")
        analysis = str(input(f"{bcolors.ENDC}Selecting {bcolors.BOLD}'n'{bcolors.ENDC} will generate processed_data.csv"
                             f" with containing data asked to be processed: "))
        while "wfn" in processing and 'y' not in analysis:
            print(f"{bcolors.FAIL}Error! {bcolors.WARNING}Results asked to be processed include {bcolors.BOLD}wfn"
                  f"{bcolors.ENDC}: {bcolors.WARNING}these results can not be displayed in a csv file and can "
                  f"only be analysed.")
            print(f"{bcolors.ENDC}If you do not wish for analysis to be performed on the other results you have asked "
                  f"to be processed, please press {bcolors.BOLD}Crt+C{bcolors.ENDC} now")
            analysis = str(input(f"Overwise press {bcolors.BOLD}y{bcolors.ENDC}: {bcolors.OKGREEN}Would you like to "
                                 f"perform data analysis({bcolors.BOLD}y/n{bcolors.ENDC}{bcolors.OKGREEN})"
                                 f"?{bcolors.ENDC}"))

        if analysis == 'y':
            print(f"{bcolors.OKGREEN}Would you like to create a GUI to display results({bcolors.BOLD}y/n{bcolors.ENDC}"
                  f"{bcolors.OKGREEN})?")
            display = input(f"{bcolors.ENDC}Selecting {bcolors.BOLD}'n'{bcolors.ENDC} will generate png files of "
                            f"analysed results: ")


        elif analysis == 'n':
            display = 'n'
            print(f"{bcolors.OKBLUE}If processed_data.csv already exists, data processed in this run will be appended "
                  f"to file")
            overwrite = input(f"If you would like to overwrite the file please type {bcolors.BOLD}'overwrite'"
                              f"{bcolors.ENDC}{bcolors.OKBLUE}, else type {bcolors.BOLD}'ok'{bcolors.ENDC}: ")
            if overwrite == 'overwrite':
                Presentation.csvfile().Overwrite()
            elif overwrite == 'ok':
                Presentation.csvfile().Append()


        Core.UserWants(analysis, display)
        Core.ProcessingControls.SavingOtherWants(processing, self.followupQs)

class Process(mp.Process):
    def __init__(self, *args, **kwargs):
        mp.Process.__init__(self, *args, **kwargs)

    def run(self):
        try:
            mp.Process.run(self)
        except TypeError:
                pass

if __name__ =='__main__':
    Start(*sys.argv)
    if Core.UserWants.DisplayWants == 'n':
        if Core.UserWants.AnalysisWants == 'n':
            pro = Process(target=Presentation.Printing2CSV())
            pro.start()
        else:
            for i in range(len(Core.ProcessingControls.ProcessingWants)):
                if Core.ProcessingControls.ProcessingWants[i] == 'test':
                    pro0 = Process(target=GUIwidgets.TestingGeometry())
                    pro0.start()
                if Core.ProcessingControls.ProcessingWants[i] == 'pdos':
                    pro1 = Process(target=ResultsAnalysis.plotpdos()) #
                    pro1.start()
                if Core.ProcessingControls.ProcessingWants[i] == 'wfn':
                    pro2 = Process(target=Presentation.WFNGUI())
                    pro2.start()
                if Core.ProcessingControls.ProcessingWants[i] == 'charges and spins':
                    followupAns = Core.ProcessingControls.Followups[i]
                    followup_Ans = Core.ProcessingControls.Process_wants[i]
                    pro3 = Process(target=Core.ProcessingControls.CharSpinYes(followupAns))
                    pro3.start()
                if Core.ProcessingControls.ProcessingWants[i] == 'geometry':
                    pro4 = Process(target=Presentation.geometryGUI())
                    pro4.start()
                    # followupAns = Core.ProcessingControls.Followups[i].split(',')
                    # pro4 = Process(target=Core.ProcessingControls.GeometryChosen(followupAns))
                    # pro4.start()


