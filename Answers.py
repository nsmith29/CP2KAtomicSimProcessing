import DataProcessing
import Presentation

class UserArguments:
    PerfectSubdir = ''
    DefectSubdir = ''
    ChemicalPotSubdir = ''
    Exception = False
    Only = False
    NotDir = ''
    OnlyDir = ''

    def __init__(self, perf_subdir, def_subdir, chempot_subdir):
        self.perf_subdir = perf_subdir
        self.def_subdir = def_subdir
        self.chempot_subdir = chempot_subdir
        UserArguments.ArgumentsSaved(self.perf_subdir, self.def_subdir, self.chempot_subdir)

    @classmethod
    def ArgumentsSaved(cls, perf_subdir, def_subdir, chempot_subdir):
        UserArguments.PerfectSubdir = perf_subdir
        UserArguments.DefectSubdir = def_subdir
        UserArguments.ChemicalPotSubdir = chempot_subdir

    @classmethod
    def ExceptionStated(cls, expt):
        UserArguments.Exception = True
        UserArguments.NotDir = expt

    @classmethod
    def OnlyStated(cls, only):
        UserArguments.Only = True
        UserArguments.OnlyDir = only

class UserWants:
    AnalysisWants = ''
    DisplayWants = ''

    def __init__(self, analysis, display):
        self.analysis = analysis
        self.display = display
        UserWants.Save(self.analysis, self.display)

    @classmethod
    def Save(cls, analysis, display):
        UserWants.AnalysisWants = analysis
        UserWants.DisplayWants = display

class ProcessingControls:
    ProcessingWants = ''
    Followups = ''
    def __init__(self, processing, followupQs):
        self.processing = processing.split(',')
        self.followupQs = followupQs
        if UserWants.DisplayWants == 'n':
            for i in range(len(self.processing)):
                if self.processing[i] == 'pdos':
                    if UserWants.AnalysisWants == 'n':
                        Presentation.csvfile.turnFalse('pdos')
                        action = DataProcessing.ControlPdos().NoAnalysis()
                    elif UserWants.AnalysisWants == 'y':
                        action = DataProcessing.ControlPdos().YesAnalysis()
                if self.processing[i] == 'wfn':
                    action = DataProcessing.ControlWfn()
                if self.processing[i] == 'charges and spins':
                    followupAns = followupQs[i]
                    if UserWants.AnalysisWants == 'n':
                        Presentation.csvfile.turnFalse('charges_and_spins')
                    action = DataProcessing.ControlChargeSpins(followupAns)

    
                # if self.processing[i] == 'geometry':
                #     followupAns = followupQs[i].split(',')
                #     defect_type = followupAns[0]
                #     atomic_index = followupAns[1]
                #     if defect_type == 'substitutional':
                #         action = DataProcessing.SubstitutionalGeometry(atomic_index)
                #     if defect_type == 'interstitional':
                #         action = DataProcessing.InterstitionalGeometry(atomic_index)
                #     if defect_type == 'vacancy':
                #         action = DataProcessing.VacancyGeometry(atomic_index)
                #     if defect_type == 'subs-vacancy complex':
                #         action = DataProcessing.SubsVacancyGeometry(atomic_index)
                #     if defect_type == 'inter-vacancy complex':
                #         action = DataProcessing.InterVacancyGeometry(atomic_index)
                # if self.processing[i] == 'band structure':
                #     followupAns = int(followupQs[i])
                #     if followupAns >= 8:
                #         action = DataProcessing.bandstructureCP2K8()
                #     elif followupAns < 8:
                #         action = DataProcessing.bandstructureCP2K()
                # if self.processing[i] == "work function":
                #     e = 10 # processing .py file needs to be sorted out
                # if self.processing[i] == 'IPR':
                #     followupAns = followupQs[i]
                #     if followupAns == 'y':
                #         b = 8
                #     elif followupAns == 'n':
                #         b = 10
    
            if UserWants.AnalysisWants == 'n':
                process_wants = []
                for want in list(self.processing):
                    change = want.replace(' ', '_')
                    process_wants.append(change)


                Presentation.Printing2CSV(self.processing, process_wants)

        elif UserWants.DisplayWants == 'y':
            ProcessingControls.SavingOtherWants(self.processing, self.followupQs)
            action = exec(open("../Presentation/GUI4data.py",'r'))

    @classmethod
    def SavingOtherWants(cls, processing, followupQs):
        ProcessingControls.ProcessingWants = processing
        ProcessingControls.Followups = followupQs