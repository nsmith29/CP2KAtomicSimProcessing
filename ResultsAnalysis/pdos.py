import numpy as np
import matplotlib.pyplot as plt

import DataProcessing
import FromFile
import Graphics

class plotvariables:
    def __init__(self, dat):
        self.s = None
        self.energy = None
        self.density = None
        if dat.find("alpha") != -1:
            self.s = "alpha"
            self.energy, self.density = np.loadtxt(dat, unpack=True)
        elif dat.find("beta") != -1:
            self.s = "beta"
            self.energy, self.density = np.loadtxt(dat, unpack=True)
            self.density = - self.density

class plotpdos(DataProcessing.YesAnalysis, FromFile.Kinds, FromFile.NameOfProject, plotvariables, Graphics.Colors, FromFile.PdosScalingFactor):
    def __init__(self):
        DataProcessing.YesAnalysis.__init__(self)
        FromFile.Kinds.__init__(self, self.perfinpfile)
        perfnumkinds = self.num_kinds
        perfkindatoms = self.included_atoms

        for definpfile, subdir, suffix in zip(list(self.definp), list(self.subdirs), list(self.suffixs)):
            FromFile.NameOfProject.__init__(self,definpfile)
            exec(f'fig_{suffix} = plt.figure(figsize=(6, 4))')
            ax = plt.subplot()
            for i in range(len(self.perfdatfiles)):
                perfdat = self.perfdatfiles[i]
                for j in range(0, int(perfnumkinds)):
                    kind = perfkindatoms[j]
                    if perfdat.find(kind) != -1:
                        plotvariables.__init__(self, perfdat)
                        exec(f'self.perf_{kind}_{self.s}_energy = self.energy')
                        exec(f'self.perf_{kind}_{self.s}_density = self.density')
                        k = j + 1
                        Graphics.Colors.__init__(self, k)
                        if self.s == "alpha":
                            ax.plot(eval("self.perf_{}_{}_energy".format(kind, self.s)),
                                    eval("self.perf_{}_{}_density".format(kind,self.s)),
                                    ls='-', color=self.colour, label=str("perfect {}".format(kind)))
                        else:
                            ax.plot(eval("self.perf_{}_{}_energy".format(kind, self.s)),
                                    eval("self.perf_{}_{}_density".format(kind, self.s)),
                                    ls='-', color=self.colour)
            FromFile.Kinds.__init__(self, definpfile)
            defnumkinds = self.num_kinds
            defkindatoms = self.included_atoms
            for i in range(len(self.defdatfiles)):
                defdat = self.defdatfiles[i]
                for j in range(0, int(defnumkinds)):
                    check = str("/"+defkindatoms[j] + "_")
                    if defdat.find(check) != -1:
                        kind = defkindatoms[j]
                        k = perfnumkinds + j + 1
                        Graphics.Colors.__init__(self, k)
                        plotvariables.__init__(self, defdat)
                if kind in perfkindatoms:
                    exec(f'self.{suffix}_{kind}_{self.s}_energy = self.energy')
                    exec(f'self.{suffix}_{kind}_{self.s}_density = self.density')
                else:
                    FromFile.PdosScalingFactor.__init__(self, subdir, defkindatoms, defnumkinds, kind)
                    exec(f'self.{suffix}_{kind}_{self.s}_energy = self.energy')
                    self.density = self.density * self.scalingfactor
                    exec(f'self.{suffix}_{kind}_{self.s}_density = self.density')

                if self.s == "alpha":
                    ax.plot(eval("self.{}_{}_{}_energy".format(suffix,kind,self.s)),
                            eval("self.{}_{}_{}_density".format(suffix,kind,self.s)), ls='--', color=self.colour,
                            label=str("defect {}".format(kind)))
                else:
                    ax.plot(eval("self.{}_{}_{}_energy".format(suffix, kind, self.s)),
                            eval("self.{}_{}_{}_density".format(suffix, kind, self.s)), ls='--', color=self.colour)
            ax.set_xlim(-2, 5)
            ax.set_ylim(-200, 200)
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles, labels, ncol=2)
            plt.xlabel('Energy (eV)')
            plt.ylabel('Density of states')
            plt.savefig(str("{}/{}_pdos_plot.png".format(subdir, self.project_name)))
            plt.show()




