import numpy as np
import matplotlib.pyplot as plt

import DataProcessing
import FromFile
import GraphicAnalysis

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

class retry:
    def __init__(self, perfkinds, defkinds, defkindatoms):
        self.defkind = None
        self.defk = None
        self.defkinds = defkinds
        self.defatoms = defkindatoms
        self.perfkinds = perfkinds

    def tryAgain(self, defdat, check, j):
        if j > self.defkinds: return
        if defdat.find(check) != -1:
            self.defkind = self.defatoms[j]
            self.defk = self.perfkinds + j + 1
        else:
            j += 1
            check = str("/" + self.defatoms[j] + "_")
            self.tryAgain(defdat, check, j)


class plotpdos(DataProcessing.YesAnalysis, FromFile.Kinds, FromFile.NameOfProject, plotvariables, GraphicAnalysis.Colors, FromFile.LastXYZ, retry, FromFile.PdosScalingFactor):
    def __init__(self):
        DataProcessing.YesAnalysis.__init__(self)
        FromFile.Kinds.__init__(self, self.perfinpfile)
        self.perfnumkinds = self.num_kinds
        self.perfkindatoms = self.included_atoms

        for subdir, suffix, definpfile in zip(list(self.subdirs), list(self.suffixs), list(self.definp)):
            FromFile.NameOfProject.__init__(self,definpfile)
            exec(f'fig_{suffix} = plt.figure(figsize=(6, 4))')
            self.ax = plt.subplot()
            for i in range(len(self.perfdatfiles)):
                perfdat = self.perfdatfiles[i]
                for j in range(0, int(self.perfnumkinds)):
                    kind = self.perfkindatoms[j]
                    if perfdat.find(kind) != -1:
                        plotvariables.__init__(self, perfdat)
                        exec(f'self.perf_{kind}_{self.s}_energy = self.energy')
                        exec(f'self.perf_{kind}_{self.s}_density = self.density')
                        k = j + 1
                        GraphicAnalysis.Colors.__init__(self, k)
                        if self.s == "alpha":
                            self.ax.plot(eval("self.perf_{}_{}_energy".format(kind, self.s)),
                                     eval("self.perf_{}_{}_density".format(kind,self.s)),
                                     ls='-', color=self.colour, label=str("perfect {}".format(kind)))
                        else:
                            self.ax.plot(eval("self.perf_{}_{}_energy".format(kind, self.s)),
                                    eval("self.perf_{}_{}_density".format(kind, self.s)),
                                    ls='-', color=self.colour)
            FromFile.LastXYZ.__init__(self, subdir)
            FromFile.Kinds.__init__(self, definpfile)
            defnumkinds = self.num_kinds
            defkindatoms = self.included_atoms
            j = 0
            for i in range(len(self.defdatfiles)):
                defdat = self.defdatfiles[i]
                retry.__init__(self, self.perfnumkinds, defnumkinds, defkindatoms)

                j = 0
                check = str("/" + self.defatoms[j] + "_")
                self.tryAgain(defdat, check, j)

                GraphicAnalysis.Colors.__init__(self, self.defk)
                plotvariables.__init__(self, defdat)
                if self.defkind in self.perfkindatoms:
                    exec(f'self.{suffix}_{self.defkind}_{self.s}_energy = self.energy')
                    exec(f'self.{suffix}_{self.defkind}_{self.s}_density = self.density')
                else:
                    FromFile.PdosScalingFactor.__init__(self, self.new_xyz_file, defkindatoms, defnumkinds, self.defkind)
                    exec(f'self.{suffix}_{self.defkind}_{self.s}_energy = self.energy')
                    self.density = self.density * self.scalingfactor
                    exec(f'self.{suffix}_{self.defkind}_{self.s}_density = self.density')

                if self.s == "alpha":
                    self.ax.plot(eval("self.{}_{}_{}_energy".format(suffix,self.defkind,self.s)),
                                 eval("self.{}_{}_{}_density".format(suffix,self.defkind,self.s)),
                                 ls='--', color=self.colour, label=str("defect {}".format(self.defkind)))
                else:
                    self.ax.plot(eval("self.{}_{}_{}_energy".format(suffix, self.defkind, self.s)),
                            eval("self.{}_{}_{}_density".format(suffix, self.defkind, self.s)), ls='--', color=self.colour)
            self.ax.set_xlim(-2, 5)
            self.ax.set_ylim(-200, 200)
            handles, labels = self.ax.get_legend_handles_labels()
            self.ax.legend(handles, labels, ncol=2)
            plt.xlabel('Energy (eV)')
            plt.ylabel('Density of states')
            plt.savefig(str("{}/{}_pdos_plot.png".format(subdir, self.project_name)))
            plt.show()


