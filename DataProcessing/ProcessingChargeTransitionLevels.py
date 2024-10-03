import Core
import FromFile

class CTLsetup:
    def __init__(self):
        for system in 'C', 'SiCl4', 'Si', 'CF4', 'GaCl2', 'B4C', 'InCl', 'Sc3C4', 'Tl2Cl3', 'Mg2Si', 'Ca2Si', 'ZnCl2', 'CuCl', 'BaCl2', 'BeCl2':
            print('help me!')

# class GainChemPots(FromFile.Kinds):
#     def __init__(self, input):
#         self.perfsubdir = Core.UserArguments.PerfectSubdir
#         self.chempotdir = Core.UserArguments.ChemicalPotSubdir
#         self.perfinput = Core.Extension().perfect_subdir(".inp", self.perfsubdir)
#         FromFile.Kinds.__init__(self, self.perfinput)
#         self.PerfKinds = self.included_atoms
#         FromFile.Kinds.__init__(self, input)
#         self.defectKinds = self.included_atoms
#         for kind in list(self.defectKinds):
#             if kind in self.PerfKinds:
#                 exec(f'{kind}_dir = Core.Extension().returnperfkindsubdir(kind, self.chempotdir)')
#                 print('perf kinds',eval("{}_dir".format(kind)))
#             elif kind == 'Al':
#
#             else:
#                 exec(f'{kind}_dir = Core.Extension().defectkindsubdir(kind, self.chempotdir)')
#                 directory = eval("{}_dir".format(kind))
#                 chempot_inp = Core.Extension().checkadditionalkindsubdir(directory)
#                 FromFile.Kinds.__init__(self, chempot_inp)
#                 for addkind in list(self.included_atoms):
#                     if addkind not in self.PerfKinds or self.defectKinds:
#                         exec(f'{addkind}_dir = Core.Extension().defectkindsubdir(addkind, self.chempotdir)')

# class CTLsetup(FromFile.ReturnProjectNames, GainChemPots):
#     def __init__(self):
#         self.defectsub = Core.UserArguments.DefectSubdir
#         self.defsubdirs, self.defsuffixs = Core.Extension().All_defect_subdir(".log", self.defectsub)
#         FromFile.ReturnProjectNames.__init__(self, self.defsubdirs)
#         for subdir, input in zip(list(self.neutralsubdir), list(self.inpneutral)):
#             GainChemPots.__init__(self, input)
        #sort into charge states
        #work out corresponding chemical potential directory for defect
        #Get total energy values of chem pot, defect, defect-free structures
        #charge correction