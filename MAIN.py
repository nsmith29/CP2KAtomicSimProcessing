import os
import sys
from multiprocessing import Process
import Core
# import Presentation
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
                               "charges and spin", "charge transition levels"]):
            print(f"{bcolors.FAIL}Error! {bcolors.WARNING}Invalid results type stated, valid methods to choose from "
                  f"include:{bcolors.BOLD}band structure{bcolors.ENDC}, {bcolors.BOLD}charges and spins{bcolors.ENDC},"
            f"{bcolors.BOLD}charge transition levels{bcolors.ENDC}, {bcolors.BOLD}geometry{bcolors.ENDC}, {bcolors.BOLD}"
                  f"IPR{bcolors.ENDC}, "
            f" {bcolors.BOLD}pdos{bcolors.ENDC}, {bcolors.BOLD}wfn{bcolors.ENDC}, {bcolors.BOLD}work function"
                  f"{bcolors.ENDC}: ")
            processing = input(f"{bcolors.OKGREEN}Which results would you like to process?: {bcolors.ENDC}")

        followupQs = []
        if processing.find('band structure') != -1:
            followup3 = input(f"{bcolors.OKCYAN}What version of CP2K were calculations conducted with (i.e. CP2K "
                              f"v8.1)?: {bcolors.ENDC}")
            followupQs.append(followup3)
        if processing.find('charges and spin') != -1:
            followup1 = input(f"{bcolors.OKCYAN}Please state the indices of nearest atomic neighbours surrounding "
                              f"defect and the index of the defect:{bcolors.ENDC} ")
            followupQs.append(followup1)
        if processing.find('charge transition levels') != -1:
            followup4 = input(f"{bcolors.OKCYAN}Please state the charge states you have investigated ({bcolors.BOLD}e.g."
                              f" 0, -2, etc{bcolors.ENDC}{bcolors.OKCYAN}): {bcolors.ENDC} ")
            followupQs.append(followup4)
        if processing.find('geometry') != -1:
            print(f"{bcolors.OKCYAN}Please state the types of defect(s) being studied and the associated atomic index of"
                  f" this defect in format'{bcolors.BOLD}defect type, atom index'{bcolors.ENDC}{bcolors.OKCYAN}")
            followup5 = input(f"{bcolors.OKCYAN}Defects type options include: {bcolors.BOLD}substitutional{bcolors.ENDC}"
                              f"{bcolors.OKCYAN}, {bcolors.BOLD}interstitional{bcolors.ENDC}{bcolors.OKCYAN}, "
                              f"{bcolors.BOLD}vacancy{bcolors.ENDC}{bcolors.OKCYAN}, {bcolors.OKCYAN}subs-vacancy "
                              f"complex{bcolors.ENDC}{bcolors.OKCYAN}, {bcolors.BOLD}inter-vacancy complex{bcolors.ENDC}"
                              f"{bcolors.OKCYAN}: {bcolors.ENDC}")
            followupQs.append(followup5)
        if processing.find('IPR') != -1:
            followup2 = input(f"{bcolors.OKCYAN}Are your calculation spin polarised({bcolors.BOLD}y/n{bcolors.BOLD}"
                              f"{bcolors.OKCYAN})?: {bcolors.ENDC}")
            followupQs.append(followup2)
        if processing.find('pdos') != -1:
            followupQs.append(' ')
        if processing.find('wfn') != -1:
            followupQs.append(' ')
        if processing.find('work function') != -1:
            followupQs.append(' ')

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
        Core.ProcessingControls.SavingOtherWants(processing, followupQs)

if __name__ =='__main__':
    Start(*sys.argv)

    if Core.UserWants.DisplayWants == 'n':
        for i in range(len(Core.ProcessingControls.ProcessingWants)):
            if Core.ProcessingControls.ProcessingWants[i] == 'pdos':
                if Core.UserWants.AnalysisWants == 'n':
                    pro1a = Process(target=Core.ProcessingControls.PdosNo())
                    pro1a.start()
                elif Core.UserWants.AnalysisWants == 'y':
                    pro1b = Process(target=ResultsAnalysis.plotpdos) #DataProcessing.ControlPdos().YesAnalysis())
                    pro1b.start()
            if Core.ProcessingControls.ProcessingWants[i] == 'wfn':
                pro2 = Process(target=DataProcessing.ControlWfn)
                pro2.start()
            if Core.ProcessingControls.ProcessingWants[i] == 'charges and spins':
                followupAns = Core.ProcessingControls.Followups[i]
                followup_Ans = Core.ProcessingControls.Process_wants[i]
                if Core.UserWants.AnalysisWants == 'n':
                    pro3a = Process(target=Core.ProcessingControls.CharSpinNo(followupAns,followup_Ans))
                    pro3a.start()
                if Core.UserWants.AnalysisWants == 'y':
                    pro3b = Process(target=Core.ProcessingControls.CharSpinYes(followupAns))
                    pro3b.start()
            if Core.ProcessingControls.ProcessingWants[i] == 'geometry':
                followupAns = Core.ProcessingControls.Followups[i].split(',')
                pro4 = Process(target=Core.ProcessingControls.GeometryChosen(followupAns))
                pro4.start()

