import numpy as np
import matplotlib.pyplot as plt
import FromFile
import Graphics

class plotpdos:
    def __init__(self, perfectfiles, perfectinput, defectfiles, defectinput, defectsubdir, suffix):
        self.perfectfiles = perfectfiles
        self.perfectinput = perfectinput
        self.defectfiles = defectfiles
        self.defectinput = defectinput
        self.defectsubdir = defectsubdir
        self.suffix = suffix

        project_name = FromFile.NameOfProject(self.defectinput).ReturnName()
        exec(f'fig_{self.suffix} = plt.figure(figsize=(6, 4))')
        ax = plt.subplot()
        perfnumkinds, perfkindatoms = FromFile.Kinds(self.perfectinput).searchingfile()
        for i in range(len(self.perfectfiles)):
            perfdat = self.perfectfiles[i]
            for j in range(0, int(perfnumkinds)):
                kind = perfkindatoms[j]
                if perfdat.find(kind) != -1:
                    s, energy, density = self.plotvariables(perfdat)
                    exec(f'self.perf_{kind}_{s}_energy = energy')
                    exec(f'self.perf_{kind}_{s}_density = density')
                    k = j + 1
                    Color = Graphics.Colors(k).getcolor()
                    if s == "alpha":
                        ax.plot(eval("self.perf_{}_{}_energy".format(kind, s)),
                                eval("self.perf_{}_{}_density".format(kind,s)),
                                ls='-', color=Color, label=str("perfect {}".format(kind)))
                    else:
                        ax.plot(eval("self.perf_{}_{}_energy".format(kind, s)),
                                eval("self.perf_{}_{}_density".format(kind, s)),
                                ls='-', color=Color)
        defnumkinds, defkindatoms = FromFile.Kinds(self.defectinput).searchingfile()
        for i in range(len(self.defectfiles)):
            defdat = self.defectfiles[i]
            for j in range(0, int(defnumkinds)):
                check = str("/"+defkindatoms[j] + "_")
                if defdat.find(check) != -1:
                    kind = defkindatoms[j]
                    k = perfnumkinds + j + 1
                    Color = Graphics.Colors(k).getcolor()
                    s, energy, density = self.plotvariables(defdat)
            if kind in perfkindatoms:
                exec(f'self.{suffix}_{kind}_{s}_energy = energy')
                exec(f'self.{suffix}_{kind}_{s}_density = density')
            else:
                scalefactor = FromFile.NumTotAtomsOfKind(self.defectsubdir, defkindatoms,
                                                               defnumkinds).PdosScalingFactor(kind)
                exec(f'self.{suffix}_{kind}_{s}_energy = energy')
                density = density * scalefactor
                exec(f'self.{suffix}_{kind}_{s}_density = density')

            if s == "alpha":
                ax.plot(eval("self.{}_{}_{}_energy".format(suffix,kind,s)),
                        eval("self.{}_{}_{}_density".format(suffix,kind,s)), ls='--', color=Color,
                        label=str("defect {}".format(kind)))
            else:
                ax.plot(eval("self.{}_{}_{}_energy".format(suffix, kind, s)),
                        eval("self.{}_{}_{}_density".format(suffix, kind, s)), ls='--', color=Color)
        ax.set_xlim(-2, 5)
        ax.set_ylim(-200, 200)
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles, labels, ncol=2)
        plt.xlabel('Energy (eV)')
        plt.ylabel('Density of states')
        plt.savefig(str("{}/{}_pdos_plot.png".format(self.defectsubdir,project_name)))
        plt.show()


    def plotvariables(self, dat):
        if dat.find("alpha") != -1:
            s = "alpha"
            energy, density = np.loadtxt(dat, unpack=True)
        elif dat.find("beta") != -1:
            s = "beta"
            energy, density = np.loadtxt(dat, unpack=True)
            density = - density
        return s, energy, density

