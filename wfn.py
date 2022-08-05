import sys
import numpy as np
import math
import PySide6
import Core
import FromFile
import Graphics
import DataProcessing
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMatrix4x4, QQuaternion, QVector3D, QColor
from PySide6.QtWidgets import *
from PySide6.Qt3DCore import Qt3DCore
from PySide6.Qt3DExtras import Qt3DExtras
from PySide6.Qt3DInput import Qt3DInput
from PySide6.QtDataVisualization import *

#mayavi
class WfnStructurePlotFrame(QWidget):
    BondsAlreadyMadeStore = dict()
    def __init__(self, parent, subdir, suffix):
        super().__init__()
        # definitions
        self.subdir = subdir
        self.suffix = suffix
        self.num_kinds, self.included_atoms = FromFile.Kinds(
            Core.Extension().files4defect(".inp", self.subdir)).searchingfile()
        self.num_kind = self.num_kinds + 1
        self.index = 0
        for t in range(0, 2000):
            exec(f'self.addBond_{t} = "None"')
        for s in range(1,11):
            exec(f'self.series{s}{self.suffix} = "None"')
        self.atoms = []
        self.X = []
        self.Y = []
        self.Z = []
        self.totatom = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["Geometry"][-1][
                           'Index'] + 1
        for g in range(0, int(self.totatom)):
            self.addAllAtoms(g)
        for i in range(0, int(self.totatom)):
            atom = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Name']
            self.atoms.append(atom)
            x_ = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Xcoord']
            self.X.append(x_)
            y_ = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Ycoord']
            self.Y.append(y_)
            z_ = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["Geometry"][i]['Zcoord']
            self.Z.append(z_)

        # wfn gui
        self.layout = QGridLayout()
        for n in range(30):
            exec(f'self.layout.setColumnMinimumWidth({n},18)')
        for m in range(33):
            exec(f'self.layout.setRowMinimumHeight({m},33)')

        exec(f'self.scatter{self.suffix} = Q3DScatter()')
        exec(f'self.container{self.suffix} = QWidget.createWindowContainer(self.scatter{self.suffix})')
        frame = QWidget()
        exec(f'self.layout.addWidget(self.container{self.suffix}, 1, 1, 16, 17)')

        # set up for atoms
        for i in range(1, int(self.num_kind)):
            exec(f'self.series{i}{self.suffix} =  QScatter3DSeries()')
            exec(f'self.data{i}{self.suffix} = QScatterDataItem()')
        for elem in list(self.included_atoms):
            exec(f'self.color{elem}{self.suffix} = Graphics.atom_lookup(elem).identification()[0]')
            exec(f'self.size{elem}{self.suffix} = Graphics.atom_lookup(elem).identification()[1]')

        # set up for bonds
        for h in range(0, int(self.totatom)):
            bonds_formed = Graphics.atom_lookup(self.atoms[h]).identification()[-1]

            exec(f'self.distance_from_atom{h} = []')
            exec(f'self.from_atom{h}_to_atom = []')
            exec(f'atom{h}_bonded_to = []')
            for f in range(0, int(self.totatom)):
                if h != f:
                    dis = np.sqrt(
                        (self.X[h] - self.X[f]) ** 2 + (self.Y[h] - self.Y[f]) ** 2 + (self.Z[h] - self.Z[f]) ** 2)
                    exec(f'self.distance_from_atom{h}.append(dis)')
                    exec(f'self.from_atom{h}_to_atom.append(f)')

            closeness_to_atom = [x for _, x in sorted(
                zip(eval("self.distance_from_atom{}".format(h)), eval("self.from_atom{}_to_atom".format(h))))]
            for m in range(0, int(bonds_formed)):
                Atom = self.atoms[int(closeness_to_atom[m])]
                if Graphics.atom_lookup(Atom).identification()[-1] >= bonds_formed:
                    if self.atoms[h] != Atom:
                        F = eval("closeness_to_atom[{}]".format(m))
                        if str("{}".format(h)) in WfnStructurePlotFrame.BondsAlreadyMadeStore[str("{}".format(F))]:
                            break
                        else:
                            self.Bonds(h, F)

        self.ScatterDataPoints()

        self.Button4neighours()
        exec(f'self.wfn_label = QLabel("Wavefunction")')
        exec(f'self.layout.addWidget(self.wfn_label,4,19,2,5)')
        self.Checkbox()
        self.Tree4WfnSettings()
        self.setLayout(self.layout)

    @classmethod
    def addAllAtoms(cls, g):
        G = str("{}".format(g))
        WfnStructurePlotFrame.BondsAlreadyMadeStore[G] = dict()

    @classmethod
    def addBondEntry(cls, h, f, length):
        H = str("{}".format(h))
        F = str("{}".format(f))
        WfnStructurePlotFrame.BondsAlreadyMadeStore[H][F] = length

    def Bonds(self, h, F):
        xdiff = self.X[h] - self.X[F]
        ydiff = self.Y[h] - self.Y[F]
        zdiff = self.Z[h] - self.Z[F]

        length = np.sqrt(xdiff ** 2 + ydiff ** 2 + zdiff ** 2)

        self.addBondEntry(h, F, length)
        xlength = xdiff / 25
        ylength = ydiff / 25
        zlength = zdiff / 25

        vector = [xdiff, ydiff, zdiff]
        angle = math.atan(ydiff / (np.sqrt((xdiff) ** 2 + (ydiff) ** 2)))
        exec(f'series{self.index} = QScatter3DSeries()')
        data = QScatterDataItem()

        for w in range(0, 25):
            new_x = self.X[F] + (w * xlength)
            new_y = self.Y[F] + (w * ylength)
            new_z = self.Z[F] + (w * zlength)
            data.setPosition(QVector3D(new_x, new_y, new_z))
            exec(f'series{self.index}.dataProxy().addItem(data)')
        exec(f'series{self.index}.setMesh(QAbstract3DSeries.MeshCube)')
        exec(f'series{self.index}.setMeshAxisAndAngle(QVector3D(vector[0], vector[1], vector[2]), angle)')
        exec(f'series{self.index}.setItemSize(float(0.015))')
        exec(f'series{self.index}.setBaseColor(QColor(Qt.white))')

        exec(f'self.addBond_{self.index} = series{self.index}')
        self.index = self.index + 1

    def ScatterDataPoints(self):
        for Atom, index in zip(list(self.atoms), range(0, int(self.totatom))):
            for elem, i in zip(list(self.included_atoms), range(1, int(self.num_kind))):
                if Atom == elem:
                    x = float(self.X[index])
                    y = float(self.Y[index])
                    z = float(self.Z[index])
                    exec(f'self.data{i}{self.suffix}.setPosition(QVector3D(x, y, z))')
                    exec(f'self.series{i}{self.suffix}.dataProxy().addItem(self.data{i}{self.suffix})')
                    exec(f'self.series{i}{self.suffix}.setBaseColor(self.color{elem}{self.suffix})')
                    exec(f'self.series{i}{self.suffix}.setItemSize(float(self.size{elem}{self.suffix}))')

        exec(f'modifier = Graphics.ScatterDataModifier(self.subdir, self.suffix, self.scatter{self.suffix}, self.series1{self.suffix}, '
             f'self.series2{self.suffix}, self.series3{self.suffix}, self.series4{self.suffix}, '
             f'self.series5{self.suffix}, self.series6{self.suffix}, self.series7{self.suffix}, '
             f'self.series8{self.suffix}, self.series9{self.suffix}, self.series10{self.suffix}).plotBonds(self.addBond_0,'
             f' self.addBond_1, self.addBond_2, self.addBond_3, self.addBond_4, self.addBond_5, self.addBond_6,'
             f' self.addBond_7, self.addBond_8, self.addBond_9, self.addBond_10, self.addBond_11, self.addBond_12,'
             f' self.addBond_13, self.addBond_14, self.addBond_15, self.addBond_16, self.addBond_17, self.addBond_18,'
             f' self.addBond_19, self.addBond_20, self.addBond_21, self.addBond_22, self.addBond_23, self.addBond_24,'
             f' self.addBond_25, self.addBond_26, self.addBond_27, self.addBond_28, self.addBond_29, self.addBond_30,'
             f' self.addBond_31, self.addBond_32, self.addBond_33, self.addBond_34, self.addBond_35, self.addBond_36,'
             f' self.addBond_37, self.addBond_38, self.addBond_39, self.addBond_40, self.addBond_41, self.addBond_42,'
             f' self.addBond_43, self.addBond_44, self.addBond_45, self.addBond_46, self.addBond_47, self.addBond_48,'
             f' self.addBond_49, self.addBond_50, self.addBond_51, self.addBond_52, self.addBond_53, self.addBond_54,'
             f' self.addBond_55, self.addBond_56, self.addBond_57, self.addBond_58, self.addBond_59, self.addBond_60,'
             f' self.addBond_61, self.addBond_62, self.addBond_63, self.addBond_64, self.addBond_65, self.addBond_66,'
             f' self.addBond_67, self.addBond_68, self.addBond_69, self.addBond_70, self.addBond_71, self.addBond_72,'
             f' self.addBond_73, self.addBond_74, self.addBond_75, self.addBond_76, self.addBond_77, self.addBond_78,'
             f' self.addBond_79, self.addBond_80, self.addBond_81, self.addBond_82, self.addBond_83, self.addBond_84,'
             f' self.addBond_85, self.addBond_86, self.addBond_87, self.addBond_88, self.addBond_89, self.addBond_90,'
             f' self.addBond_91, self.addBond_92, self.addBond_93, self.addBond_94, self.addBond_95, self.addBond_96,'
             f' self.addBond_97, self.addBond_98, self.addBond_99, self.addBond_100, self.addBond_101, self.addBond_102,'
             f' self.addBond_103, self.addBond_104, self.addBond_105, self.addBond_106, self.addBond_107, self.addBond_108,'
             f' self.addBond_109, self.addBond_110, self.addBond_111, self.addBond_112, self.addBond_113, self.addBond_114,'
             f' self.addBond_115, self.addBond_116, self.addBond_117, self.addBond_118, self.addBond_119, self.addBond_120,'
             f' self.addBond_121, self.addBond_122, self.addBond_123, self.addBond_124, self.addBond_125, self.addBond_126,'
             f' self.addBond_127, self.addBond_128, self.addBond_129, self.addBond_130, self.addBond_131, self.addBond_132,'
             f' self.addBond_133, self.addBond_134, self.addBond_135, self.addBond_136, self.addBond_137, self.addBond_138,'
             f' self.addBond_139, self.addBond_140, self.addBond_141, self.addBond_142, self.addBond_143, self.addBond_144,'
             f' self.addBond_145, self.addBond_146, self.addBond_147, self.addBond_148, self.addBond_149, self.addBond_150,'
             f' self.addBond_151, self.addBond_152, self.addBond_153, self.addBond_154, self.addBond_155, self.addBond_156,'
             f' self.addBond_157, self.addBond_158, self.addBond_159, self.addBond_160, self.addBond_161, self.addBond_162,'
             f' self.addBond_163, self.addBond_164, self.addBond_165, self.addBond_166, self.addBond_167, self.addBond_168,'
             f' self.addBond_169, self.addBond_170, self.addBond_171, self.addBond_172, self.addBond_173, self.addBond_174,'
             f' self.addBond_175, self.addBond_176, self.addBond_177, self.addBond_178, self.addBond_179, self.addBond_180,'
             f'self.addBond_181, self.addBond_182, self.addBond_183, self.addBond_184, self.addBond_185, self.addBond_186,'
             f' self.addBond_187, self.addBond_188, self.addBond_189, self.addBond_190, self.addBond_191, self.addBond_192,'
             f' self.addBond_193, self.addBond_194, self.addBond_195, self.addBond_196, self.addBond_197, self.addBond_198,'
             f' self.addBond_199, self.addBond_200, self.addBond_201, self.addBond_202, self.addBond_203, self.addBond_204,'
             f' self.addBond_205, self.addBond_206, self.addBond_207, self.addBond_208, self.addBond_209, self.addBond_210,'
             f' self.addBond_211, self.addBond_212, self.addBond_213, self.addBond_214, self.addBond_215, self.addBond_216,'
             f' self.addBond_217, self.addBond_218, self.addBond_219, self.addBond_220, self.addBond_221, self.addBond_222,'
             f' self.addBond_223, self.addBond_224, self.addBond_225, self.addBond_226, self.addBond_227, self.addBond_228,'
             f' self.addBond_229, self.addBond_230, self.addBond_231, self.addBond_232, self.addBond_233, self.addBond_234,'
             f' self.addBond_235, self.addBond_236, self.addBond_237, self.addBond_238, self.addBond_239, self.addBond_240,'
             f' self.addBond_241, self.addBond_242, self.addBond_243, self.addBond_244, self.addBond_245, self.addBond_246,'
             f' self.addBond_247, self.addBond_248, self.addBond_249, self.addBond_250, self.addBond_251, self.addBond_252,'
             f' self.addBond_253, self.addBond_254, self.addBond_255, self.addBond_256, self.addBond_257, self.addBond_258,'
             f' self.addBond_259, self.addBond_260, self.addBond_261, self.addBond_262, self.addBond_263, self.addBond_264,'
             f' self.addBond_265, self.addBond_266, self.addBond_267, self.addBond_268, self.addBond_269, self.addBond_270,'
             f' self.addBond_271, self.addBond_272, self.addBond_273, self.addBond_274, self.addBond_275, self.addBond_276,'
             f' self.addBond_277, self.addBond_278, self.addBond_279, self.addBond_280, self.addBond_281, self.addBond_282,'
             f' self.addBond_283, self.addBond_284, self.addBond_285, self.addBond_286, self.addBond_287, self.addBond_288,'
             f' self.addBond_289, self.addBond_290, self.addBond_291, self.addBond_292, self.addBond_293, self.addBond_294,'
             f' self.addBond_295, self.addBond_296, self.addBond_297, self.addBond_298, self.addBond_299, self.addBond_300,'
             f' self.addBond_301, self.addBond_302, self.addBond_303, self.addBond_304, self.addBond_305, self.addBond_306,'
             f' self.addBond_307, self.addBond_308, self.addBond_309, self.addBond_310, self.addBond_311, self.addBond_312,'
             f' self.addBond_313, self.addBond_314, self.addBond_315, self.addBond_316, self.addBond_317, self.addBond_318,'
             f' self.addBond_319, self.addBond_320, self.addBond_321, self.addBond_322, self.addBond_323, self.addBond_324,'
             f' self.addBond_325, self.addBond_326, self.addBond_327, self.addBond_328, self.addBond_329, self.addBond_330,'
             f' self.addBond_331, self.addBond_332, self.addBond_333, self.addBond_334, self.addBond_335, self.addBond_336,'
             f' self.addBond_337, self.addBond_338, self.addBond_339, self.addBond_340, self.addBond_341, self.addBond_342,'
             f' self.addBond_343, self.addBond_344, self.addBond_345, self.addBond_346, self.addBond_347, self.addBond_348,'
             f' self.addBond_349, self.addBond_350, self.addBond_351, self.addBond_352, self.addBond_353, self.addBond_354,'
             f' self.addBond_355, self.addBond_356, self.addBond_357, self.addBond_358, self.addBond_359, self.addBond_360,'
             f' self.addBond_361, self.addBond_362, self.addBond_363, self.addBond_364, self.addBond_365, self.addBond_366,'
             f' self.addBond_367, self.addBond_368, self.addBond_369, self.addBond_370, self.addBond_371, self.addBond_372,'
             f' self.addBond_373, self.addBond_374, self.addBond_375, self.addBond_376, self.addBond_377, self.addBond_378,'
             f' self.addBond_379, self.addBond_380, self.addBond_381, self.addBond_382, self.addBond_383, self.addBond_384,'
             f' self.addBond_385, self.addBond_386, self.addBond_387, self.addBond_388, self.addBond_389, self.addBond_390,'
             f' self.addBond_391, self.addBond_392, self.addBond_393, self.addBond_394, self.addBond_395, self.addBond_396,'
             f' self.addBond_397, self.addBond_398, self.addBond_399, self.addBond_400, self.addBond_401, self.addBond_402,'
             f' self.addBond_403, self.addBond_404, self.addBond_405, self.addBond_406, self.addBond_407, self.addBond_408,'
             f' self.addBond_409, self.addBond_410, self.addBond_411, self.addBond_412, self.addBond_413, self.addBond_414,'
             f' self.addBond_415, self.addBond_416, self.addBond_417, self.addBond_418, self.addBond_419, self.addBond_420,'
             f' self.addBond_421, self.addBond_422, self.addBond_423, self.addBond_424, self.addBond_425, self.addBond_426,'
             f' self.addBond_427, self.addBond_428, self.addBond_429, self.addBond_430, self.addBond_431, self.addBond_432,'
             f' self.addBond_433, self.addBond_434, self.addBond_435, self.addBond_436, self.addBond_437, self.addBond_438,'
             f' self.addBond_439, self.addBond_440, self.addBond_441, self.addBond_442, self.addBond_443, self.addBond_444,'
             f' self.addBond_445, self.addBond_446, self.addBond_447, self.addBond_448, self.addBond_449, self.addBond_450,'
             f' self.addBond_451, self.addBond_452, self.addBond_453, self.addBond_454, self.addBond_455, self.addBond_456,'
             f' self.addBond_457, self.addBond_458, self.addBond_459, self.addBond_460, self.addBond_461, self.addBond_462,'
             f' self.addBond_463, self.addBond_464, self.addBond_465, self.addBond_466, self.addBond_467, self.addBond_468,'
             f' self.addBond_469, self.addBond_470, self.addBond_471, self.addBond_472, self.addBond_473, self.addBond_474,'
             f' self.addBond_475, self.addBond_476, self.addBond_477, self.addBond_478, self.addBond_479, self.addBond_480,'
             f' self.addBond_481, self.addBond_482, self.addBond_483, self.addBond_484, self.addBond_485, self.addBond_486,'
             f' self.addBond_487, self.addBond_488, self.addBond_489, self.addBond_490, self.addBond_491, self.addBond_492,'
             f' self.addBond_493, self.addBond_494, self.addBond_495, self.addBond_496, self.addBond_497, self.addBond_498,'
             f' self.addBond_499, self.addBond_500, self.addBond_501, self.addBond_502, self.addBond_503, self.addBond_504,'
             f' self.addBond_505, self.addBond_506, self.addBond_507, self.addBond_508, self.addBond_509, self.addBond_510,'
             f' self.addBond_511, self.addBond_512, self.addBond_513, self.addBond_514, self.addBond_515, self.addBond_516,'
             f' self.addBond_517, self.addBond_518, self.addBond_519, self.addBond_520, self.addBond_521, self.addBond_522,'
             f' self.addBond_523, self.addBond_524, self.addBond_525, self.addBond_526, self.addBond_527, self.addBond_528,'
             f' self.addBond_529, self.addBond_530, self.addBond_531, self.addBond_532, self.addBond_533, self.addBond_534,'
             f' self.addBond_535, self.addBond_536, self.addBond_537, self.addBond_538, self.addBond_539, self.addBond_540,'
             f' self.addBond_541, self.addBond_542, self.addBond_543, self.addBond_544, self.addBond_545, self.addBond_546,'
             f' self.addBond_547, self.addBond_548, self.addBond_549, self.addBond_550, self.addBond_551, self.addBond_552,'
             f' self.addBond_553, self.addBond_554, self.addBond_555, self.addBond_556, self.addBond_557, self.addBond_558,'
             f' self.addBond_559, self.addBond_560, self.addBond_561, self.addBond_562, self.addBond_563, self.addBond_564,'
             f' self.addBond_565, self.addBond_566, self.addBond_567, self.addBond_568, self.addBond_569, self.addBond_570,'
             f' self.addBond_571, self.addBond_572, self.addBond_573, self.addBond_574, self.addBond_575, self.addBond_576,'
             f' self.addBond_577, self.addBond_578, self.addBond_579, self.addBond_580, self.addBond_581, self.addBond_582,'
             f' self.addBond_583, self.addBond_584, self.addBond_585, self.addBond_586, self.addBond_587, self.addBond_588,'
             f' self.addBond_589, self.addBond_590, self.addBond_591, self.addBond_592, self.addBond_593, self.addBond_594,'
             f' self.addBond_595, self.addBond_596, self.addBond_597, self.addBond_598, self.addBond_599, self.addBond_600,'
             f' self.addBond_601, self.addBond_602, self.addBond_603, self.addBond_604, self.addBond_605, self.addBond_606,'
             f' self.addBond_607, self.addBond_608, self.addBond_609, self.addBond_610, self.addBond_611, self.addBond_612,'
             f' self.addBond_613, self.addBond_614, self.addBond_615, self.addBond_616, self.addBond_617, self.addBond_618,'
             f' self.addBond_619, self.addBond_620, self.addBond_621, self.addBond_622, self.addBond_623, self.addBond_624,'
             f' self.addBond_625, self.addBond_626, self.addBond_627, self.addBond_628, self.addBond_629, self.addBond_630,'
             f' self.addBond_631, self.addBond_632, self.addBond_633, self.addBond_634, self.addBond_635, self.addBond_636,'
             f' self.addBond_637, self.addBond_638, self.addBond_639, self.addBond_640, self.addBond_641, self.addBond_642,'
             f' self.addBond_643, self.addBond_644, self.addBond_645, self.addBond_646, self.addBond_647, self.addBond_648,'
             f' self.addBond_649, self.addBond_650, self.addBond_651, self.addBond_652, self.addBond_653, self.addBond_654,'
             f' self.addBond_655, self.addBond_656, self.addBond_657, self.addBond_658, self.addBond_659, self.addBond_660,'
             f' self.addBond_661, self.addBond_662, self.addBond_663, self.addBond_664, self.addBond_665, self.addBond_666,'
             f' self.addBond_667, self.addBond_668, self.addBond_669, self.addBond_670, self.addBond_671, self.addBond_672,'
             f' self.addBond_673, self.addBond_674, self.addBond_675, self.addBond_676, self.addBond_677, self.addBond_678,'
             f' self.addBond_679, self.addBond_680, self.addBond_681, self.addBond_682, self.addBond_683, self.addBond_684,'
             f' self.addBond_685, self.addBond_686, self.addBond_687, self.addBond_688, self.addBond_689, self.addBond_690,'
             f' self.addBond_691, self.addBond_692, self.addBond_693, self.addBond_694, self.addBond_695, self.addBond_696,'
             f' self.addBond_697, self.addBond_698, self.addBond_699, self.addBond_700, self.addBond_701, self.addBond_702,'
             f' self.addBond_703, self.addBond_704, self.addBond_705, self.addBond_706, self.addBond_707, self.addBond_708,'
             f' self.addBond_709, self.addBond_710, self.addBond_711, self.addBond_712, self.addBond_713, self.addBond_714,'
             f' self.addBond_715, self.addBond_716, self.addBond_717, self.addBond_718, self.addBond_719, self.addBond_720,'
             f' self.addBond_721, self.addBond_722, self.addBond_723, self.addBond_724, self.addBond_725, self.addBond_726,'
             f' self.addBond_727, self.addBond_728, self.addBond_729, self.addBond_730, self.addBond_731, self.addBond_732,'
             f' self.addBond_733, self.addBond_734, self.addBond_735, self.addBond_736, self.addBond_737, self.addBond_738,'
             f' self.addBond_739, self.addBond_740, self.addBond_741, self.addBond_742, self.addBond_743, self.addBond_744,'
             f' self.addBond_745, self.addBond_746, self.addBond_747, self.addBond_748, self.addBond_749, self.addBond_750,'
             f' self.addBond_751, self.addBond_752, self.addBond_753, self.addBond_754, self.addBond_755, self.addBond_756,'
             f' self.addBond_757, self.addBond_758, self.addBond_759, self.addBond_760, self.addBond_761, self.addBond_762,'
             f' self.addBond_763, self.addBond_764, self.addBond_765, self.addBond_766, self.addBond_767, self.addBond_768,'
             f' self.addBond_769, self.addBond_770, self.addBond_771, self.addBond_772, self.addBond_773, self.addBond_774,'
             f' self.addBond_775, self.addBond_776, self.addBond_777, self.addBond_778, self.addBond_779, self.addBond_780,'
             f' self.addBond_781, self.addBond_782, self.addBond_783, self.addBond_784, self.addBond_785, self.addBond_786,'
             f' self.addBond_787, self.addBond_788, self.addBond_789, self.addBond_790, self.addBond_791, self.addBond_792,'
             f' self.addBond_793, self.addBond_794, self.addBond_795, self.addBond_796, self.addBond_797, self.addBond_798,'
             f' self.addBond_799, self.addBond_800, self.addBond_801, self.addBond_802, self.addBond_803, self.addBond_804,'
             f' self.addBond_805, self.addBond_806, self.addBond_807, self.addBond_808, self.addBond_809, self.addBond_810,'
             f' self.addBond_811, self.addBond_812, self.addBond_813, self.addBond_814, self.addBond_815, self.addBond_816,'
             f' self.addBond_817, self.addBond_818, self.addBond_819, self.addBond_820, self.addBond_821, self.addBond_822,'
             f' self.addBond_823, self.addBond_824, self.addBond_825, self.addBond_826, self.addBond_827, self.addBond_828,'
             f' self.addBond_829, self.addBond_830, self.addBond_831, self.addBond_832, self.addBond_833, self.addBond_834,'
             f' self.addBond_835, self.addBond_836, self.addBond_837, self.addBond_838, self.addBond_839, self.addBond_840,'
             f' self.addBond_841, self.addBond_842, self.addBond_843, self.addBond_844, self.addBond_845, self.addBond_846,'
             f' self.addBond_847, self.addBond_848, self.addBond_849, self.addBond_850, self.addBond_851, self.addBond_852,'
             f' self.addBond_853, self.addBond_854, self.addBond_855, self.addBond_856, self.addBond_857, self.addBond_858,'
             f' self.addBond_859, self.addBond_860, self.addBond_861, self.addBond_862, self.addBond_863, self.addBond_864,'
             f' self.addBond_865, self.addBond_866, self.addBond_867, self.addBond_868, self.addBond_869, self.addBond_870,'
             f' self.addBond_871, self.addBond_872, self.addBond_873, self.addBond_874, self.addBond_875, self.addBond_876,'
             f' self.addBond_877, self.addBond_878, self.addBond_879, self.addBond_880, self.addBond_881, self.addBond_882,'
             f' self.addBond_883, self.addBond_884, self.addBond_885, self.addBond_886, self.addBond_887, self.addBond_888,'
             f' self.addBond_889, self.addBond_890, self.addBond_891, self.addBond_892, self.addBond_893, self.addBond_894,'
             f' self.addBond_895, self.addBond_896, self.addBond_897, self.addBond_898, self.addBond_899, self.addBond_900,'
             f' self.addBond_901, self.addBond_902, self.addBond_903, self.addBond_904, self.addBond_905, self.addBond_906,'
             f' self.addBond_907, self.addBond_908, self.addBond_909, self.addBond_910, self.addBond_911, self.addBond_912,'
             f' self.addBond_913, self.addBond_914, self.addBond_915, self.addBond_916, self.addBond_917, self.addBond_918,'
             f' self.addBond_919, self.addBond_920, self.addBond_921, self.addBond_922, self.addBond_923, self.addBond_924,'
             f' self.addBond_925, self.addBond_926, self.addBond_927, self.addBond_928, self.addBond_929, self.addBond_930,'
             f' self.addBond_931, self.addBond_932, self.addBond_933, self.addBond_934, self.addBond_935, self.addBond_936,'
             f' self.addBond_937, self.addBond_938, self.addBond_939, self.addBond_940, self.addBond_941, self.addBond_942,'
             f' self.addBond_943, self.addBond_944, self.addBond_945, self.addBond_946, self.addBond_947, self.addBond_948,'
             f' self.addBond_949, self.addBond_950, self.addBond_951, self.addBond_952, self.addBond_953, self.addBond_954,'
             f' self.addBond_955, self.addBond_956, self.addBond_957, self.addBond_958, self.addBond_959, self.addBond_960,'
             f' self.addBond_961, self.addBond_962, self.addBond_963, self.addBond_964, self.addBond_965, self.addBond_966,'
             f' self.addBond_967, self.addBond_968, self.addBond_969, self.addBond_970, self.addBond_971, self.addBond_972,'
             f' self.addBond_973, self.addBond_974, self.addBond_975, self.addBond_976, self.addBond_977, self.addBond_978,'
             f' self.addBond_979, self.addBond_980, self.addBond_981, self.addBond_982, self.addBond_983, self.addBond_984,'
             f' self.addBond_985, self.addBond_986, self.addBond_987, self.addBond_988, self.addBond_989, self.addBond_990,'
             f' self.addBond_991, self.addBond_992, self.addBond_993, self.addBond_994, self.addBond_995, self.addBond_996,'
             f' self.addBond_997, self.addBond_998, self.addBond_999, self.addBond_1000, self.addBond_1001,'
             f' self.addBond_1002, self.addBond_1003, self.addBond_1004, self.addBond_1005, self.addBond_1006,'
             f' self.addBond_1007, self.addBond_1008, self.addBond_1009, self.addBond_1010, self.addBond_1011,'
             f' self.addBond_1012, self.addBond_1013, self.addBond_1014, self.addBond_1015, self.addBond_1016,'
             f' self.addBond_1017, self.addBond_1018, self.addBond_1019, self.addBond_1020, self.addBond_1021,'
             f' self.addBond_1022, self.addBond_1023, self.addBond_1024, self.addBond_1025, self.addBond_1026,'
             f' self.addBond_1027, self.addBond_1028, self.addBond_1029, self.addBond_1030, self.addBond_1031,'
             f' self.addBond_1032, self.addBond_1033, self.addBond_1034, self.addBond_1035, self.addBond_1036,'
             f' self.addBond_1037, self.addBond_1038, self.addBond_1039, self.addBond_1040, self.addBond_1041,'
             f' self.addBond_1042, self.addBond_1043, self.addBond_1044, self.addBond_1045, self.addBond_1046,'
             f' self.addBond_1047, self.addBond_1048, self.addBond_1049, self.addBond_1050, self.addBond_1051,'
             f' self.addBond_1052, self.addBond_1053, self.addBond_1054, self.addBond_1055, self.addBond_1056,'
             f' self.addBond_1057, self.addBond_1058, self.addBond_1059, self.addBond_1060, self.addBond_1061,'
             f' self.addBond_1062, self.addBond_1063, self.addBond_1064, self.addBond_1065, self.addBond_1066,'
             f' self.addBond_1067, self.addBond_1068, self.addBond_1069, self.addBond_1070, self.addBond_1071,'
             f' self.addBond_1072, self.addBond_1073, self.addBond_1074, self.addBond_1075, self.addBond_1076,'
             f' self.addBond_1077, self.addBond_1078, self.addBond_1079, self.addBond_1080, self.addBond_1081,'
             f' self.addBond_1082, self.addBond_1083, self.addBond_1084, self.addBond_1085, self.addBond_1086,'
             f' self.addBond_1087, self.addBond_1088, self.addBond_1089, self.addBond_1090, self.addBond_1091,'
             f' self.addBond_1092, self.addBond_1093, self.addBond_1094, self.addBond_1095, self.addBond_1096,'
             f' self.addBond_1097, self.addBond_1098, self.addBond_1099, self.addBond_1100, self.addBond_1101,'
             f' self.addBond_1102, self.addBond_1103, self.addBond_1104, self.addBond_1105, self.addBond_1106,'
             f' self.addBond_1107, self.addBond_1108, self.addBond_1109, self.addBond_1110, self.addBond_1111,'
             f' self.addBond_1112, self.addBond_1113, self.addBond_1114, self.addBond_1115, self.addBond_1116,'
             f' self.addBond_1117, self.addBond_1118, self.addBond_1119, self.addBond_1120, self.addBond_1121,'
             f' self.addBond_1122, self.addBond_1123, self.addBond_1124, self.addBond_1125, self.addBond_1126,'
             f' self.addBond_1127, self.addBond_1128, self.addBond_1129, self.addBond_1130, self.addBond_1131,'
             f' self.addBond_1132, self.addBond_1133, self.addBond_1134, self.addBond_1135, self.addBond_1136,'
             f' self.addBond_1137, self.addBond_1138, self.addBond_1139, self.addBond_1140, self.addBond_1141,'
             f' self.addBond_1142, self.addBond_1143, self.addBond_1144, self.addBond_1145, self.addBond_1146,'
             f' self.addBond_1147, self.addBond_1148, self.addBond_1149, self.addBond_1150, self.addBond_1151,'
             f' self.addBond_1152, self.addBond_1153, self.addBond_1154, self.addBond_1155, self.addBond_1156,'
             f' self.addBond_1157, self.addBond_1158, self.addBond_1159, self.addBond_1160, self.addBond_1161,'
             f' self.addBond_1162, self.addBond_1163, self.addBond_1164, self.addBond_1165, self.addBond_1166,'
             f' self.addBond_1167, self.addBond_1168, self.addBond_1169, self.addBond_1170, self.addBond_1171,'
             f' self.addBond_1172, self.addBond_1173, self.addBond_1174, self.addBond_1175, self.addBond_1176,'
             f' self.addBond_1177, self.addBond_1178, self.addBond_1179, self.addBond_1180, self.addBond_1181,'
             f' self.addBond_1182, self.addBond_1183, self.addBond_1184, self.addBond_1185, self.addBond_1186,'
             f' self.addBond_1187, self.addBond_1188, self.addBond_1189, self.addBond_1190, self.addBond_1191,'
             f' self.addBond_1192, self.addBond_1193, self.addBond_1194, self.addBond_1195, self.addBond_1196,'
             f' self.addBond_1197, self.addBond_1198, self.addBond_1199, self.addBond_1200, self.addBond_1201,'
             f' self.addBond_1202, self.addBond_1203, self.addBond_1204, self.addBond_1205, self.addBond_1206,'
             f' self.addBond_1207, self.addBond_1208, self.addBond_1209, self.addBond_1210, self.addBond_1211,'
             f' self.addBond_1212, self.addBond_1213, self.addBond_1214, self.addBond_1215, self.addBond_1216,'
             f' self.addBond_1217, self.addBond_1218, self.addBond_1219, self.addBond_1220, self.addBond_1221,'
             f' self.addBond_1222, self.addBond_1223, self.addBond_1224, self.addBond_1225, self.addBond_1226,'
             f' self.addBond_1227, self.addBond_1228, self.addBond_1229, self.addBond_1230, self.addBond_1231,'
             f' self.addBond_1232, self.addBond_1233, self.addBond_1234, self.addBond_1235, self.addBond_1236,'
             f' self.addBond_1237, self.addBond_1238, self.addBond_1239, self.addBond_1240, self.addBond_1241,'
             f' self.addBond_1242, self.addBond_1243, self.addBond_1244, self.addBond_1245, self.addBond_1246,'
             f' self.addBond_1247, self.addBond_1248, self.addBond_1249, self.addBond_1250, self.addBond_1251,'
             f' self.addBond_1252, self.addBond_1253, self.addBond_1254, self.addBond_1255, self.addBond_1256,'
             f' self.addBond_1257, self.addBond_1258, self.addBond_1259, self.addBond_1260, self.addBond_1261,'
             f' self.addBond_1262, self.addBond_1263, self.addBond_1264, self.addBond_1265, self.addBond_1266,'
             f' self.addBond_1267, self.addBond_1268, self.addBond_1269, self.addBond_1270, self.addBond_1271,'
             f' self.addBond_1272, self.addBond_1273, self.addBond_1274, self.addBond_1275, self.addBond_1276,'
             f' self.addBond_1277, self.addBond_1278, self.addBond_1279, self.addBond_1280, self.addBond_1281,'
             f' self.addBond_1282, self.addBond_1283, self.addBond_1284, self.addBond_1285, self.addBond_1286,'
             f' self.addBond_1287, self.addBond_1288, self.addBond_1289, self.addBond_1290, self.addBond_1291,'
             f' self.addBond_1292, self.addBond_1293, self.addBond_1294, self.addBond_1295, self.addBond_1296,'
             f' self.addBond_1297, self.addBond_1298, self.addBond_1299, self.addBond_1300, self.addBond_1301,'
             f' self.addBond_1302, self.addBond_1303, self.addBond_1304, self.addBond_1305, self.addBond_1306,'
             f' self.addBond_1307, self.addBond_1308, self.addBond_1309, self.addBond_1310, self.addBond_1311,'
             f' self.addBond_1312, self.addBond_1313, self.addBond_1314, self.addBond_1315, self.addBond_1316,'
             f' self.addBond_1317, self.addBond_1318, self.addBond_1319, self.addBond_1320, self.addBond_1321,'
             f' self.addBond_1322, self.addBond_1323, self.addBond_1324, self.addBond_1325, self.addBond_1326,'
             f' self.addBond_1327, self.addBond_1328, self.addBond_1329, self.addBond_1330, self.addBond_1331,'
             f' self.addBond_1332, self.addBond_1333, self.addBond_1334, self.addBond_1335, self.addBond_1336,'
             f' self.addBond_1337, self.addBond_1338, self.addBond_1339, self.addBond_1340, self.addBond_1341,'
             f' self.addBond_1342, self.addBond_1343, self.addBond_1344, self.addBond_1345, self.addBond_1346,'
             f' self.addBond_1347, self.addBond_1348, self.addBond_1349, self.addBond_1350, self.addBond_1351,'
             f' self.addBond_1352, self.addBond_1353, self.addBond_1354, self.addBond_1355, self.addBond_1356,'
             f' self.addBond_1357, self.addBond_1358, self.addBond_1359, self.addBond_1360, self.addBond_1361,'
             f' self.addBond_1362, self.addBond_1363, self.addBond_1364, self.addBond_1365, self.addBond_1366,'
             f' self.addBond_1367, self.addBond_1368, self.addBond_1369, self.addBond_1370, self.addBond_1371,'
             f' self.addBond_1372, self.addBond_1373, self.addBond_1374, self.addBond_1375, self.addBond_1376,'
             f' self.addBond_1377, self.addBond_1378, self.addBond_1379, self.addBond_1380, self.addBond_1381,'
             f' self.addBond_1382, self.addBond_1383, self.addBond_1384, self.addBond_1385, self.addBond_1386,'
             f' self.addBond_1387, self.addBond_1388, self.addBond_1389, self.addBond_1390, self.addBond_1391,'
             f' self.addBond_1392, self.addBond_1393, self.addBond_1394, self.addBond_1395, self.addBond_1396,'
             f' self.addBond_1397, self.addBond_1398, self.addBond_1399, self.addBond_1400, self.addBond_1401,'
             f' self.addBond_1402, self.addBond_1403, self.addBond_1404, self.addBond_1405, self.addBond_1406,'
             f' self.addBond_1407, self.addBond_1408, self.addBond_1409, self.addBond_1410, self.addBond_1411,'
             f' self.addBond_1412, self.addBond_1413, self.addBond_1414, self.addBond_1415, self.addBond_1416,'
             f' self.addBond_1417, self.addBond_1418, self.addBond_1419, self.addBond_1420, self.addBond_1421,'
             f' self.addBond_1422, self.addBond_1423, self.addBond_1424, self.addBond_1425, self.addBond_1426,'
             f' self.addBond_1427, self.addBond_1428, self.addBond_1429, self.addBond_1430, self.addBond_1431,'
             f' self.addBond_1432, self.addBond_1433, self.addBond_1434, self.addBond_1435, self.addBond_1436,'
             f' self.addBond_1437, self.addBond_1438, self.addBond_1439, self.addBond_1440, self.addBond_1441,'
             f' self.addBond_1442, self.addBond_1443, self.addBond_1444, self.addBond_1445, self.addBond_1446,'
             f' self.addBond_1447, self.addBond_1448, self.addBond_1449, self.addBond_1450, self.addBond_1451,'
             f' self.addBond_1452, self.addBond_1453, self.addBond_1454, self.addBond_1455, self.addBond_1456,'
             f' self.addBond_1457, self.addBond_1458, self.addBond_1459, self.addBond_1460, self.addBond_1461,'
             f' self.addBond_1462, self.addBond_1463, self.addBond_1464, self.addBond_1465, self.addBond_1466,'
             f' self.addBond_1467, self.addBond_1468, self.addBond_1469, self.addBond_1470, self.addBond_1471,'
             f' self.addBond_1472, self.addBond_1473, self.addBond_1474, self.addBond_1475, self.addBond_1476,'
             f' self.addBond_1477, self.addBond_1478, self.addBond_1479, self.addBond_1480, self.addBond_1481,'
             f' self.addBond_1482, self.addBond_1483, self.addBond_1484, self.addBond_1485, self.addBond_1486,'
             f' self.addBond_1487, self.addBond_1488, self.addBond_1489, self.addBond_1490, self.addBond_1491,'
             f' self.addBond_1492, self.addBond_1493, self.addBond_1494, self.addBond_1495, self.addBond_1496,'
             f' self.addBond_1497, self.addBond_1498, self.addBond_1499, self.addBond_1500, self.addBond_1501,'
             f' self.addBond_1502, self.addBond_1503, self.addBond_1504, self.addBond_1505, self.addBond_1506,'
             f' self.addBond_1507, self.addBond_1508, self.addBond_1509, self.addBond_1510, self.addBond_1511,'
             f' self.addBond_1512, self.addBond_1513, self.addBond_1514, self.addBond_1515, self.addBond_1516,'
             f' self.addBond_1517, self.addBond_1518, self.addBond_1519, self.addBond_1520, self.addBond_1521,'
             f' self.addBond_1522, self.addBond_1523, self.addBond_1524, self.addBond_1525, self.addBond_1526,'
             f' self.addBond_1527, self.addBond_1528, self.addBond_1529, self.addBond_1530, self.addBond_1531,'
             f' self.addBond_1532, self.addBond_1533, self.addBond_1534, self.addBond_1535, self.addBond_1536,'
             f' self.addBond_1537, self.addBond_1538, self.addBond_1539, self.addBond_1540, self.addBond_1541,'
             f' self.addBond_1542, self.addBond_1543, self.addBond_1544, self.addBond_1545, self.addBond_1546,'
             f' self.addBond_1547, self.addBond_1548, self.addBond_1549, self.addBond_1550, self.addBond_1551,'
             f' self.addBond_1552, self.addBond_1553, self.addBond_1554, self.addBond_1555, self.addBond_1556,'
             f' self.addBond_1557, self.addBond_1558, self.addBond_1559, self.addBond_1560, self.addBond_1561,'
             f' self.addBond_1562, self.addBond_1563, self.addBond_1564, self.addBond_1565, self.addBond_1566,'
             f' self.addBond_1567, self.addBond_1568, self.addBond_1569, self.addBond_1570, self.addBond_1571,'
             f' self.addBond_1572, self.addBond_1573, self.addBond_1574, self.addBond_1575, self.addBond_1576,'
             f' self.addBond_1577, self.addBond_1578, self.addBond_1579, self.addBond_1580, self.addBond_1581,'
             f' self.addBond_1582, self.addBond_1583, self.addBond_1584, self.addBond_1585, self.addBond_1586,'
             f' self.addBond_1587, self.addBond_1588, self.addBond_1589, self.addBond_1590, self.addBond_1591,'
             f' self.addBond_1592, self.addBond_1593, self.addBond_1594, self.addBond_1595, self.addBond_1596,'
             f' self.addBond_1597, self.addBond_1598, self.addBond_1599, self.addBond_1600, self.addBond_1601,'
             f' self.addBond_1602, self.addBond_1603, self.addBond_1604, self.addBond_1605, self.addBond_1606,'
             f' self.addBond_1607, self.addBond_1608, self.addBond_1609, self.addBond_1610, self.addBond_1611,'
             f' self.addBond_1612, self.addBond_1613, self.addBond_1614, self.addBond_1615, self.addBond_1616,'
             f' self.addBond_1617, self.addBond_1618, self.addBond_1619, self.addBond_1620, self.addBond_1621,'
             f' self.addBond_1622, self.addBond_1623, self.addBond_1624, self.addBond_1625, self.addBond_1626,'
             f' self.addBond_1627, self.addBond_1628, self.addBond_1629, self.addBond_1630, self.addBond_1631,'
             f' self.addBond_1632, self.addBond_1633, self.addBond_1634, self.addBond_1635, self.addBond_1636,'
             f' self.addBond_1637, self.addBond_1638, self.addBond_1639, self.addBond_1640, self.addBond_1641,'
             f' self.addBond_1642, self.addBond_1643, self.addBond_1644, self.addBond_1645, self.addBond_1646,'
             f' self.addBond_1647, self.addBond_1648, self.addBond_1649, self.addBond_1650, self.addBond_1651,'
             f' self.addBond_1652, self.addBond_1653, self.addBond_1654, self.addBond_1655, self.addBond_1656,'
             f' self.addBond_1657, self.addBond_1658, self.addBond_1659, self.addBond_1660, self.addBond_1661,'
             f' self.addBond_1662, self.addBond_1663, self.addBond_1664, self.addBond_1665, self.addBond_1666,'
             f' self.addBond_1667, self.addBond_1668, self.addBond_1669, self.addBond_1670, self.addBond_1671,'
             f' self.addBond_1672, self.addBond_1673, self.addBond_1674, self.addBond_1675, self.addBond_1676,'
             f' self.addBond_1677, self.addBond_1678, self.addBond_1679, self.addBond_1680, self.addBond_1681,'
             f' self.addBond_1682, self.addBond_1683, self.addBond_1684, self.addBond_1685, self.addBond_1686,'
             f' self.addBond_1687, self.addBond_1688, self.addBond_1689, self.addBond_1690, self.addBond_1691,'
             f' self.addBond_1692, self.addBond_1693, self.addBond_1694, self.addBond_1695, self.addBond_1696,'
             f' self.addBond_1697, self.addBond_1698, self.addBond_1699, self.addBond_1700, self.addBond_1701,'
             f' self.addBond_1702, self.addBond_1703, self.addBond_1704, self.addBond_1705, self.addBond_1706,'
             f' self.addBond_1707, self.addBond_1708, self.addBond_1709, self.addBond_1710, self.addBond_1711,'
             f' self.addBond_1712, self.addBond_1713, self.addBond_1714, self.addBond_1715, self.addBond_1716,'
             f' self.addBond_1717, self.addBond_1718, self.addBond_1719, self.addBond_1720, self.addBond_1721,'
             f' self.addBond_1722, self.addBond_1723, self.addBond_1724, self.addBond_1725, self.addBond_1726,'
             f' self.addBond_1727, self.addBond_1728, self.addBond_1729, self.addBond_1730, self.addBond_1731,'
             f' self.addBond_1732, self.addBond_1733, self.addBond_1734, self.addBond_1735, self.addBond_1736,'
             f' self.addBond_1737, self.addBond_1738, self.addBond_1739, self.addBond_1740, self.addBond_1741,'
             f' self.addBond_1742, self.addBond_1743, self.addBond_1744, self.addBond_1745, self.addBond_1746,'
             f' self.addBond_1747, self.addBond_1748, self.addBond_1749, self.addBond_1750, self.addBond_1751,'
             f' self.addBond_1752, self.addBond_1753, self.addBond_1754, self.addBond_1755, self.addBond_1756,'
             f' self.addBond_1757, self.addBond_1758, self.addBond_1759, self.addBond_1760, self.addBond_1761,'
             f' self.addBond_1762, self.addBond_1763, self.addBond_1764, self.addBond_1765, self.addBond_1766,'
             f' self.addBond_1767, self.addBond_1768, self.addBond_1769, self.addBond_1770, self.addBond_1771,'
             f' self.addBond_1772, self.addBond_1773, self.addBond_1774, self.addBond_1775, self.addBond_1776,'
             f' self.addBond_1777, self.addBond_1778, self.addBond_1779, self.addBond_1780, self.addBond_1781,'
             f' self.addBond_1782, self.addBond_1783, self.addBond_1784, self.addBond_1785, self.addBond_1786,'
             f' self.addBond_1787, self.addBond_1788, self.addBond_1789, self.addBond_1790, self.addBond_1791,'
             f' self.addBond_1792, self.addBond_1793, self.addBond_1794, self.addBond_1795, self.addBond_1796,'
             f' self.addBond_1797, self.addBond_1798, self.addBond_1799, self.addBond_1800, self.addBond_1801,'
             f' self.addBond_1802, self.addBond_1803, self.addBond_1804, self.addBond_1805, self.addBond_1806,'
             f' self.addBond_1807, self.addBond_1808, self.addBond_1809, self.addBond_1810, self.addBond_1811,'
             f' self.addBond_1812, self.addBond_1813, self.addBond_1814, self.addBond_1815, self.addBond_1816,'
             f' self.addBond_1817, self.addBond_1818, self.addBond_1819, self.addBond_1820, self.addBond_1821,'
             f' self.addBond_1822, self.addBond_1823, self.addBond_1824, self.addBond_1825, self.addBond_1826,'
             f' self.addBond_1827, self.addBond_1828, self.addBond_1829, self.addBond_1830, self.addBond_1831,'
             f' self.addBond_1832, self.addBond_1833, self.addBond_1834, self.addBond_1835, self.addBond_1836,'
             f' self.addBond_1837, self.addBond_1838, self.addBond_1839, self.addBond_1840, self.addBond_1841,'
             f' self.addBond_1842, self.addBond_1843, self.addBond_1844, self.addBond_1845, self.addBond_1846,'
             f' self.addBond_1847, self.addBond_1848, self.addBond_1849, self.addBond_1850, self.addBond_1851,'
             f' self.addBond_1852, self.addBond_1853, self.addBond_1854, self.addBond_1855, self.addBond_1856,'
             f' self.addBond_1857, self.addBond_1858, self.addBond_1859, self.addBond_1860, self.addBond_1861,'
             f' self.addBond_1862, self.addBond_1863, self.addBond_1864, self.addBond_1865, self.addBond_1866,'
             f' self.addBond_1867, self.addBond_1868, self.addBond_1869, self.addBond_1870, self.addBond_1871,'
             f' self.addBond_1872, self.addBond_1873, self.addBond_1874, self.addBond_1875, self.addBond_1876,'
             f' self.addBond_1877, self.addBond_1878, self.addBond_1879, self.addBond_1880, self.addBond_1881,'
             f' self.addBond_1882, self.addBond_1883, self.addBond_1884, self.addBond_1885, self.addBond_1886,'
             f' self.addBond_1887, self.addBond_1888, self.addBond_1889, self.addBond_1890, self.addBond_1891,'
             f' self.addBond_1892, self.addBond_1893, self.addBond_1894, self.addBond_1895, self.addBond_1896,'
             f' self.addBond_1897, self.addBond_1898, self.addBond_1899, self.addBond_1900, self.addBond_1901,'
             f' self.addBond_1902, self.addBond_1903, self.addBond_1904, self.addBond_1905, self.addBond_1906,'
             f' self.addBond_1907, self.addBond_1908, self.addBond_1909, self.addBond_1910, self.addBond_1911,'
             f' self.addBond_1912, self.addBond_1913, self.addBond_1914, self.addBond_1915, self.addBond_1916,'
             f' self.addBond_1917, self.addBond_1918, self.addBond_1919, self.addBond_1920, self.addBond_1921,'
             f' self.addBond_1922, self.addBond_1923, self.addBond_1924, self.addBond_1925, self.addBond_1926,'
             f' self.addBond_1927, self.addBond_1928, self.addBond_1929, self.addBond_1930, self.addBond_1931,'
             f' self.addBond_1932, self.addBond_1933, self.addBond_1934, self.addBond_1935, self.addBond_1936,'
             f' self.addBond_1937, self.addBond_1938, self.addBond_1939, self.addBond_1940, self.addBond_1941,'
             f' self.addBond_1942, self.addBond_1943, self.addBond_1944, self.addBond_1945, self.addBond_1946,'
             f' self.addBond_1947, self.addBond_1948, self.addBond_1949, self.addBond_1950, self.addBond_1951,'
             f' self.addBond_1952, self.addBond_1953, self.addBond_1954, self.addBond_1955, self.addBond_1956,'
             f' self.addBond_1957, self.addBond_1958, self.addBond_1959, self.addBond_1960, self.addBond_1961,'
             f' self.addBond_1962, self.addBond_1963, self.addBond_1964, self.addBond_1965, self.addBond_1966,'
             f' self.addBond_1967, self.addBond_1968, self.addBond_1969, self.addBond_1970, self.addBond_1971,'
             f' self.addBond_1972, self.addBond_1973, self.addBond_1974, self.addBond_1975, self.addBond_1976,'
             f' self.addBond_1977, self.addBond_1978, self.addBond_1979, self.addBond_1980, self.addBond_1981,'
             f' self.addBond_1982, self.addBond_1983, self.addBond_1984, self.addBond_1985, self.addBond_1986,'
             f' self.addBond_1987, self.addBond_1988, self.addBond_1989, self.addBond_1990, self.addBond_1991,'
             f' self.addBond_1992, self.addBond_1993, self.addBond_1994, self.addBond_1995, self.addBond_1996,'
             f' self.addBond_1997, self.addBond_1998, self.addBond_1999)')

    def Button4neighours(self):
        exec(f'self.neighbourbutton{self.suffix} = QPushButton()')
        exec(f'self.neighbourbutton{self.suffix}.setText("defect nearest neighbours")')
        exec(f'self.layout.addWidget(self.neighbourbutton{self.suffix},2,19,2,9)')

    def Checkbox(self):
        exec(f'self.yescheckbox{self.suffix} = QCheckBox()')
        exec(f'self.yescheckbox{self.suffix}.setText("On")')
        exec(f'self.yescheckbox{self.suffix}.setChecked(False)')
        exec(f'self.layout.addWidget(self.yescheckbox{self.suffix},5,19,2,3)')
        exec(f'self.nocheckbox{self.suffix} = QCheckBox()')
        exec(f'self.nocheckbox{self.suffix}.setText("off")')
        exec(f'self.nocheckbox{self.suffix}.setChecked(True)')
        exec(f'self.layout.addWidget(self.nocheckbox{self.suffix},5,24,2,3)')

    def Tree4WfnSettings(self):
        exec(f'self.wfntree{self.suffix} = QTreeWidget()')
        exec(f'self.wfntree{self.suffix}.setHeaderHidden(True)')

        exec(f'wfnoptionsframe{self.suffix} = QFrame(self.wfntree{self.suffix})')
        exec(f'wfnframelayout{self.suffix} = QVBoxLayout(wfnoptionsframe{self.suffix})')

        exec(f'whichwfnList{self.suffix} = QComboBox(wfnoptionsframe{self.suffix})')
        if 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["ALPHA"]:
            exec(f'whichwfnList{self.suffix}.addItem("HOMO-1")')
        elif 'HOMO-1' in DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["BETA"]:
            exec(f'whichwfnList{self.suffix}.addItem("HOMO-1")')
        exec(f'whichwfnList{self.suffix}.addItem("HOMO")')
        exec(f'whichwfnList{self.suffix}.addItem("LUMO")')
        exec(f'wfnframelayout{self.suffix}.addWidget(whichwfnList{self.suffix})')

        exec(f'wfnframelayout{self.suffix}.addWidget(QLabel("Spin State"))')

        exec(f'spinstatelayout{self.suffix} = QHBoxLayout()')
        exec(f'alphacheckbox{self.suffix} = QCheckBox()')
        exec(f'alphacheckbox{self.suffix}.setText("Alpha")')
        exec(f'alphacheckbox{self.suffix}.setChecked(False)')
        exec(f'betacheckbox{self.suffix} = QCheckBox()')
        exec(f'betacheckbox{self.suffix}.setText("Beta")')
        exec(f'betacheckbox{self.suffix}.setChecked(True)')
        exec(f'spinstatelayout{self.suffix}.addWidget(alphacheckbox{self.suffix})')
        exec(f'spinstatelayout{self.suffix}.addWidget(betacheckbox{self.suffix})')
        exec(f'wfnframelayout{self.suffix}.addLayout(spinstatelayout{self.suffix})')

        exec(f'wfnframelayout{self.suffix}.addWidget(QLabel("Isovalue:"))')

        exec(f'isovalueslider{self.suffix} = QSlider(Qt.Horizontal, wfnoptionsframe{self.suffix})')
        exec(f'isovalueslider{self.suffix}.setMinimum(0.05)')
        exec(f'isovalueslider{self.suffix}.setTickInterval(0.05)')
        exec(f'isovalueslider{self.suffix}.setEnabled(True)')
        exec(f'wfnframelayout{self.suffix}.addWidget(isovalueslider{self.suffix})')

        exec(f'self.layout.addWidget(self.wfntree{self.suffix},7,19,9,9)')

class ScatterDataModifier:

    def __init__(self, subdir, suffix, m_graph, series1, series2, series3, series4, series5, series6, series7, series8, series9, series10):
        self.subdir = subdir
        self.suffix = suffix
        self.m_graph = m_graph
        self.X = []
        self.Y = []
        self.Z = []
        self.atoms = []
        self.num_kinds, self.included_atoms = FromFile.Kinds(
            Core.Extension().files4defect(".inp", self.subdir)).searchingfile()
        self.num_kind = self.num_kinds + 1
        self.totatom = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(self.suffix))]["Geometry"][-1][
                           'Index'] + 1

        self.m_graph.activeTheme().setType(Q3DTheme.ThemeEbony)
        self.m_graph.activeTheme().setBackgroundColor(QColor(Qt.black))
        font = self.m_graph.activeTheme().font()
        m_fontSize = 12
        font.setPointSize(m_fontSize)
        self.m_graph.activeTheme().setFont(font)
        self.m_graph.setShadowQuality(QAbstract3DGraph.ShadowQualitySoftLow)
        self.m_graph.scene().activeCamera().setCameraPreset(Q3DCamera.CameraPresetFront)
        self.m_graph.scene().activeCamera().setMinZoomLevel(float(200.0))
        self.m_graph_handler = Q3DInputHandler()
        self.m_graph_handler.setRotationEnabled(True)
        self.m_graph_handler.setZoomEnabled(True)
        self.m_graph_handler.setSelectionEnabled(True)

        proxy = QScatterDataProxy()
        self.series = QScatter3DSeries(proxy)
        self.series.setItemLabelFormat("@xTitle: @xLable @yTitle: @yLabel @zTitle: @zLabel")
        self.m_smooth = True
        self.series.setMeshSmooth(self.m_smooth)
        self.m_graph.addSeries(self.series)

        self.series1 = series1
        self.series2 = series2
        self.series3 = series3
        self.series4 = series4
        self.series5 = series5
        self.series6 = series6
        self.series7 = series7
        self.series8 = series8
        self.series9 = series9
        self.series10 = series10

        self.AddDataPoint()

    def AddDataPoint(self):
        self.m_graph.axisX().setTitle("X")
        self.m_graph.axisY().setTitle("Y")
        self.m_graph.axisZ().setTitle("Z")
        self.m_graph.setAspectRatio(1.0)

        self.m_graph.removeSeries(self.series)

        self.series1.setItemLabelFormat("@xTitle: @xLabel @yTitle: @yLabel @zTitle: @zLabel")
        self.m_graph.addSeries(self.series1)
        if self.series2 != "None":
            self.m_graph.addSeries(self.series2)
        if self.series3 != "None":
            self.m_graph.addSeries(self.series3)
        if self.series4 != "None":
            self.m_graph.addSeries(self.series4)
        if self.series5 != "None":
            self.m_graph.addSeries(self.series5)
        if self.series6 != 'None':
            self.m_graph.addSeries(self.series6)
        if self.series7 != 'None':
            self.m_graph.addSeries(self.series7)
        if self.series8 != 'None':
            self.m_graph.addSeries(self.series8)
        if self.series9 != 'None':
            self.m_graph.addSeries(self.series9)
        if self.series10 != 'None':
            self.m_graph.addSeries(self.series10)

    def plotBonds(self, rpv, odi, baz, nsz, pzz, ahd, jun, lwc, kcx, xdd, utq, gnd, qsl, oyn, ybt, lxc, gpn, smc, ymd,
                  emt, xhn, vtc, scw, zpp, mab, baa, rpm, qxh, ofw, svl, vrf, ilw, tgc, vnc, djd, hcd, gzx, pkp, bbm,
                  nyn, vha, lpa, fsh, dce, voi, tpm, sqb, hsz, qjs, ngy, jte, aep, hmq, omd, rhd, lqd, apj, rft, txx, ytx,
                  wve, dqy, rzg, tow, xla, hho, kmg, kxe, lii, yjc, jgq, ygj, jdk, ucq, fyt, zia, cxa, nnb, yde, fdm, rpc,
                  rrl, sef, kbv, xag, wzx, run, vze, pcw, lki, szt, uko, qcz, cpz, skj, oeu, jst, zmj, wmg, psu, nvw, crg,
                  zwy, nab, owy, guv, yyz, ohi, mse, lwm, syn, xkm, zih, gct, iap, vnb, oua, ebq, wjj, xkf, xri, ehm, irq,
                  der, bhq, vwt, blc, ahr, prl, nhj, idd, yry, ciy, ypl, zth, avy, jky, wtq, bpi, ioe, jeo, gtu, epv, plw,
                  guu, wks, wsp, zbo, exf, cyf, haj, zvx, ovq, bwr, zxd, llj, bjo, vva, fwu, xuz, cgh, gzs, rxw, ami, zib,
                  ukm, xce, mgt, vfs, noo, kac, uul, eat, lvt, fsj, qur, hju, mcr, eze, cbr, jvl, foz, veg, pqg, qig, eut,
                  fif, qoi, kti, vcn, mib, ivv, eob, eel, nma, ljp, kel, kfh, tqw, uoi, tza, eyg, kyi, dlt, ffp, knu, wtf,
                  qtc, xnn, uzm, dvz, ifn, skf, ghc, lif, rdt, qwg, pbs, igo, ksi, sde, irk, ccs, adf, api, thi, rlm, rql,
                  itk, eyo, tjt, bdc, ksy, qke, ulo, xyf, zxp, wqi, yav, ixt, rwe, hdp, bfh, wom, ozc, bkp, qhf, sib, vmj,
                  exv, hom, zlf, lpw, sil, sko, scr, vba, krh, oxk, zek, atx, fss, trt, pee, vkr, ajn, woc, kiu, yyd, gga,
                  lgl, jty, mjn, zxq, qzy, uxa, qir, lkn, aaq, ssg, wbl, ofe, yev, zin, toq, pwh, dad, ogz, mdl, zxe, ces,
                  efs, pxy, odd, rdd, yjb, zsw, icn, qzw, epc, lck, wfi, xlo, ymo, eql, baf, qlf, yaf, rji, ahc, xiy, qzv,
                  qif, xoh, rvb, vrz, fbs, shx, pea, ggr, ccm, tpi, thk, wfn, tup, qgj, pxo, zrs, sxb, gki, efk, giz, isl,
                  qjk, pkv, rao, pxj, hxz, fxr, hdy, jqs, ewv, qcw, fdz, nad, qtd, vsg, tfw, zfe, jip, vwk, rty, vre, osl,
                  aki, eja, eop, eea, nbx, uxz, qck, evw, lnv, llc, gnb, voa, cdb, cqv, kkp, ecx, ren, iri, kmf, pep, bpd,
                  thu, yem, nac, ipi, jbx, owh, kwx, asc, sfj, mct, drb, tch, eko, tzq, iqj, tcn, cns, slk, cje, hsj, elp,
                  xfs, sba, ocb, cnq, rnz, tcl, hxt, tmi, tiz, olz, qba, lgr, xhs, ear, ddp, sjq, gnr, omc, ldv, ecr, zmf,
                  emi, tlj, ekt, enh, fkm, lmo, dqc, ovo, pqy, fqv, nmi, dcx, ypf, toa, ilc, ixo, kpn, nms, mhh, tpw, cpg,
                  qmw, irz, fxv, nwr, inx, ojg, ojq, rcy, pwi, rcj, cfj, wkx, npk, ssj, inj, ika, mfe, sgv, hce, jso, kxi,
                  coo, dxa, euy, lkk, jkd, kvo, dqz, hmy, pac, vhf, ohw, amv, sfo, wqc, mpf, rtg, fqo, qav, jqa, sdm, vyv,
                  gba, qhb, dyd, pzq, wxz, jxy, cpw, rfj, kqo, lkb, pol, nyg, wau, ogo, lzw, jza, hqj, ivb, zlv, jgc, vda,
                  gtk, aio, unl, nwe, xza, rjl, gue, xvo, eyc, blk, lzs, ibr, ndj, tld, fow, vun, voh, wns, otj, ahn, lhk,
                  wpe, myq, ovs, yrt, ifx, dsc, jdw, wge, gnv, kfx, lgd, snv, iva, wkf, cjn, aay, rzt, aek, jtw, oye, vvz,
                  qay, cjj, sxw, iyd, kio, tud, dmi, yqz, hyw, dex, oju, usw, hxh, mvc, pis, pnx, geu, xau, noc, oyd, lod,
                  xyl, zmi, sob, axq, hbb, uaj, zln, pnj, ylk, ghr, nag, wnl, kxh, roc, ynv, pdk, bnc, cub, rbd, cgl, rtl,
                  tln, xfu, aed, bwk, bmm, eqf, eoa, ahm, ayv, gbm, qkq, qkz, cyb, jmp, mcg, kkz, abg, sqz, ttz, voz, nis,
                  vsw, aye, aya, vlz, pur, lnl, mpa, bee, xrx, gwq, bpb, kyp, mbb, fdr, ixh, xey, jhu, hvq, hgo, sjm, vyh,
                  mbh, etr, vhy, ewc, lsx, uwb, cig, yyy, nwq, ixp, yqm, qaj, kyv, rln, lrd, tfe, kna, puq, vve, esf, tnf,
                  kef, yqv, gtt, pou, fvc, eug, xqv, edk, yrg, emx, zkz, xgl, ssq, eoc, thw, ksf, bir, dcp, xll, axv, eqt,
                  sbp, lmr, idn, vyt, ecw, iuo, nho, gdi, llp, mqd, fzv, xmf, iok, exr, upw, ita, bgl, mxb, ayf, xqz, tqv,
                  fgd, dvg, dcj, dph, fak, zsy, syt, rgm, bmw, kia, zdx, jvq, lbs, uqh, bco, hoq, byh, myn, shk, khq, ttf,
                  scm, qht, xae, mlb, xtq, cxq, agb, hvo, iec, xmy, qbl, xtg, kaz, bzx, zsl, gtn, afp, hvd, uen, ute, njv,
                  lvx, zzj, exc, krr, hpd, tee, utf, rgz, ebc, rjh, rof, lum, uli, huk, rum, sog, mln, uok, mif, hwb, lfn,
                  imc, vqj, mgm, hbi, pmb, aqr, myd, dcm, xgj, hvz, tyi, yhp, pfl, qpt, lvv, hyj, vlf, uzy, son, nze, tmn,
                  zfw, sid, yov, unq, fqq, woy, fik, xbw, fwa, rqs, ehd, rza, ngj, pxi, moo, jrt, hni, fth, jyn, vef, hak,
                  wlj, otv, nwk, jfq, pbw, ffd, trl, eje, chj, nen, pjs, uds, gaf, bsn, yhs, zvz, kqe, smb, ulc, hrc, rdb,
                  ytf, fwy, jvu, tfy, sci, oxq, edj, eyd, wik, avc, che, qin, iwu, adb, ymt, hxl, yot, dud, omv, jus, qau,
                  qwi, etw, con, kzn, bxc, kid, far, wpl, pgl, oaz, fgj, lqk, dct, brl, yxr, tcj, wrc, tof, lbz, sha, ghv,
                  ljk, jxs, xfh, vrd, vej, nkm, jnr, qwj, dbp, orl, ypw, xxd, agt, sdr, oen, snx, mpp, ath, hyi, znb, otb,
                  nfu, nyt, aen, tme, icb, gck, vpk, yub, vio, zfk, dte, mrs, xxt, fxo, lrk, qri, hoc, qvn, ibl, biu, zym,
                  dyk, cmu, fix, nvo, dlm, zzm, iko, rmq, jmc, lsq, eyq, suf, kqb, swg, ium, voq, yzv, jbu, jcr, hym, cmg,
                  evz, znn, fre, klv, ian, lsw, jod, kxk, swi, kgb, eis, qnc, usy, cmi, mjq, uie, inp, iuy, rnj, zzv, ulv,
                  zqt, suo, zeq, huv, ldq, abm, ojp, myb, uyj, sbv, yif, fvi, rer, mem, dig, zew, sgk, erv, bxu, pns, ioo,
                  jdo, aev, fxh, wxv, cnd, upg, vux, ken, wkw, ivm, oqm, qvx, ncx, pax, gkx, vrh, vsi, wnn, irs, igd, gwf,
                  ldo, rfx, unv, heg, xtk, axk, rbz, gjd, xfj, opk, pwp, czh, nhq, wxf, wrw, nnz, riw, aui, lgx, tue, yly,
                  uwj, cbv, aea, fav, hku, pvc, wei, gkz, pgv, yuc, iwh, xqo, ota, qew, dqg, bfg, ynz, exw, sud, vhj, ges,
                  amw, iqt, kol, hfa, fvu, qsi, qix, tcr, ctk, qqg, wze, hod, hzr, nlh, qso, pja, oqe, rst, fzh, awz, atn,
                  fwb, txd, ybg, tpe, how, nuu, wam, oiw, mrc, wjo, yfw, nxm, rqn, aju, eyh, xsj, zyp, hee, coj, xzj, uzf,
                  sbb, wah, ldz, emu, umg, fpi, zpz, mzh, hqu, eoz, zxg, ncc, kbs, usi, hzi, rbh, kun, aoi, qwm, uyc, duh,
                  eyn, gdh, lca, ubu, zsz, dns, xxn, zyg, cec, bla, unp, rjg, gti, qfc, nrj, hxf, ayh, hkg, akd, nfw, ouc,
                  sul, isf, biq, zun, khc, xpj, grn, hut, bzo, zzl, wpu, ihi, syo, rsw, ivn, jcy, ivi, biy, jhc, izz, vlx,
                  lyr, kmy, dsl, ptb, evn, ciw, kht, lmb, rpp, uln, yha, dhq, tkk, ayp, ija, rnd, ztc, fxl, sly, rig, xdh,
                  xnz, ufa, ehv, zkv, jpm, jyb, jyu, ukn, qeh, yal, mlg, yup, puk, cof, bvl, gjv, stg, gjk, ofr, utn, sis,
                  yjo, ewj, pdb, lac, ajp, esr, ovc, bcv, nqx, znq, utk, jmz, xwg, yfp, wkn, prm, elr, ile, xpy, tss, gei,
                  jfy, qzl, siv, kyb, gil, kqv, gjq, vbj, gtl, cbk, ehw, eyf, fce, xsu, wzs, wbn, awa, tze, zvc, fnc, rda,
                  tqe, hft, ctt, ufz, hjd, gsn, sgd, dji, wmx, qds, oiv, row, mhr, jql, noe, ohk, mdd, ocr, ltf, qrm, hou,
                  tli, kuh, bnn, qzm, nvz, nug, klc, hwq, xmt, ozi, fog, dcq, abq, dio, pxv, ani, qwr, uyu, alv, sce, onu,
                  zkd, hfc, mcc, dne, oak, uuz, deb, rod, mzf, jzb, zvh, nzu, nzs, aza, gch, zuh, whs, ugu, kuv, lqv, let,
                  hvw, bov, yna, xzn, pvm, jdv, sls, sbr, nnd, vtb, fbk, csj, hqc, mrg, ozk, ctx, nvj, lrj, edx, lyd, bqe,
                  laj, qlo, xfd, mkb, buw, bgd, lmc, gll, ywr, uei, bvk, iyb, urk, pmh, nzw, bmz, cmf, hzl, dr, tvq, csd,
                  xns, inq, xzc, nmo, pql, ufl, nja, bya, cuj, ikp, zzh, tbc, jqz, hlu, mhc, bgv, xcc, sft, hlm, gxj, sqx,
                  veq, bos, ddq, cuu, jbg, fkl, jhh, dov, koq, yze, xmi, cuf, yfy, lwb, pte, rks, omz, rws, bjg, uwl, zdm,
                  xtm, asn, rzf, mzo, rqq, nbr, qxm, kdj, hrk, uhu, yge, ovy, mlr, jjx, qol, pgy, nej, hbq, odw, baw, gzw,
                  yaj, xja, qni, dbl, clr, tyh, bah, elg, kda, ync, mzd, iku, tau, pzx, fsy, qmq, ugi, ods, fjk, zfv, ecp,
                  ukb, rhn, wgg, vbo, zws, hpc, qdb, oaw, lcq, grc, vkb, oyz, bzk, lyh, dfp, wru, frg, izu, tqq, xlh, mes,
                  svf, ipe, vyz, hgm, wyc, iwe, gow, cem, euv, pmu, qfk, qmp, zpm, ily, pbc, bhc, gwa, gbq, anq, msq, nkw,
                  xfc, tmu, nqu, fkg, muv, uja, fjy, ppe, fpm, qob, acw, vyc, vzt, div, pcv, kmx, brn, qgf, wzu, dkm, srf,
                  sdo, sby, rjw, eln, gxz, guq, gsw, fsb, vtp, cxp, nea, iaa, pez, mdm, slf, zfm, eak, cdm, ymi, eax, pfu,
                  xui, jrr, jiy, prv, nml, mxy, wto, qoh, hvb, iqw, scj, qhs, moj, vtl, yxy, yak, nta, csv, yrl, vxi, fuf,
                  krz, jvn, pnv, ezl, iau, aaj, xir, qdj, zel, jej, vds, jxq, ras, flw, lfw, uoj, ohu, lxy, vyf, znr, sox,
                  ukw, meh, qmm, yef, zkn, het, zai, tmq, qyn, mws, rwb, aok, efp, qqi, qit, tfx, wxp, fjo, gtf, juo, bsh,
                  gvt, cln, rzk, jsk, zyv, phn, pco, gsi, jri, tqs, mfh, yfm, cdi, zay, ecs, txv, ant, ay, aul, kwr, zqb,
                  wqv, jtz, cds, luj, gal, hyf, jmi, npr, dwy, ehs, hfq, zcw, qnu, aer, pej, fru, mub, lkc, hjf, aab, eqx,
                  rtd, byn, aoy, kat, kru, dkv, djw, ezm, syb, gbz, rhx, rge, ise, rev, xwi, xti, wxd, sli, dek, lgs, xkz,
                  vpa, clv, haf, usu, mmo, ntc, kay, edr, iiv, duj, wtk, xdl, lwn, zrt, eol, kgc, zks, bad, cyd, ach, lox,
                  dsw, yuh, zgp, iib, jkx, uwe, knh, chk, zgj, gka, asa, ioj, qak, jov, ynm, wdb, owe, uod, zjw, paj, txi,
                  sab, mhu, oyc, rtc, akf, tzs, yba, grp, cdw, syx, mnv, xeh, hxo, kkk, dwr, zpn, pnl, bgb, ivs, rcg, orn,
                  nwx, zrp, rmd, jnl, fvv, gyl, wgv, sqq, qzj, yve, kos, ece, igk, ybw, epa, lsb, nvl, lem, idi, fzm, agm,
                  rja, vfc, emy, djk, pw, efq, zpl, iks, ypm, lme, jba, blt, aod, dkx, mey, rdm, tlz, ivw, rpa, dgz, zpa,
                  kto, ltz, pfk, ema, tjo, jje, hzd, fxt, azp, zmc, gxl, qiw, plt, zhk, wpr, zrf, dwk, cwm, kyf, kfa, jnt,
                  jjn, fii, mjl, vdt, uga, lff, omm, gyf, qhn, fpx, ksm, jyq, ilo, qbe, pxs, xup, srs, nzx, gda, yxq, cuc,
                  rrv, kem, xbx, aug, sjg, rjb, ipt, qhh, bpm, sma, rex, aql, evp, lxm, zop, asm, twg, uak, bwh, uke, cpf,
                  xcp, quv, tnq, awu, qud, lvw, kuf, eph, hxs, ifi, yag, tbj, gah, ybf, vnl, rgf, ezw, xul, vqb, xlt, edi,
                  twn, krk, jcq, iez, ady, via, yiv, xyi, pif, ket, zzq, epi, mxq, vby, jpx, lru, rae, oiy, gam, ljf, gha,
                  alb, duq, wyj, dck, rwc, qlk, niy, oxx, raz, bjm, hmw, uae, dnk, btz, wgt, eoh, sgh, gri, fgh, pvl, vhb,
                  cfx, rkw, ezo, juu, erc, cyx, ewy, ylh, xwq, eri, jsa, llk, bec, uhc, xhh, phf, lvn, dca, vfz, nvc, nsw,
                  waj, dqj, wnq, byw, ypi, ygg, njn, vxj, gvq, giv, wpt, bog, gzu, kcl, uco, guz, hby, axj, qve, vov, yfj,
                  bph, wad, fpa, tnz, dbu, hyg, tav, vyl, ovr, juj, neb, zwi, mio, bhh, hqe, xga, tnp, fmx, ewo, mlh, bqk,
                  kcb, htt, usp, oil, ttx, ajx, zac, jll, qrl, tkg, vrk, puu, kpw, qop, tkn, whe, juh, spn, tcf, xxj, ogu,
                  ywz, mwx, lvm, vzx, due, cxr, sug, hhs, gbx, teu, tur, uju, hhf, dma, nsb, kdo, akr, gqd, kkg, uit, ibg,
                  klu, vbx, get, jqr, zuz, zkh, ppp, vtd, kzd, vhn, nuj, paq, kwm, hyu, wae, zom, uth, mnb, gfl, uck, cwn,
                  gjm, btk, tlr, exb, szr, odt, dwl, tez, qgs, etb, gqt, eqb, iyc, cux, nlt, tcs, qdl, zea, ufi, ugr, png,
                  lbn, fye, gpb, atk, psz, reg, rzn, kiz):
        if rpv !=  "None":
           self.m_graph.addSeries(rpv)
        if odi !=  "None":
           self.m_graph.addSeries(odi)
        if baz !=  "None":
           self.m_graph.addSeries(baz)
        if nsz !=  "None":
           self.m_graph.addSeries(nsz)
        if pzz !=  "None":
           self.m_graph.addSeries(pzz)
        if ahd !=  "None":
           self.m_graph.addSeries(ahd)
        if jun !=  "None":
           self.m_graph.addSeries(jun)
        if lwc !=  "None":
           self.m_graph.addSeries(lwc)
        if kcx !=  "None":
           self.m_graph.addSeries(kcx)
        if xdd !=  "None":
           self.m_graph.addSeries(xdd)
        if utq !=  "None":
           self.m_graph.addSeries(utq)
        if gnd !=  "None":
           self.m_graph.addSeries(gnd)
        if qsl !=  "None":
           self.m_graph.addSeries(qsl)
        if oyn !=  "None":
           self.m_graph.addSeries(oyn)
        if ybt !=  "None":
           self.m_graph.addSeries(ybt)
        if lxc !=  "None":
           self.m_graph.addSeries(lxc)
        if gpn !=  "None":
           self.m_graph.addSeries(gpn)
        if smc !=  "None":
           self.m_graph.addSeries(smc)
        if ymd !=  "None":
           self.m_graph.addSeries(ymd)
        if emt !=  "None":
           self.m_graph.addSeries(emt)
        if xhn !=  "None":
           self.m_graph.addSeries(xhn)
        if vtc !=  "None":
           self.m_graph.addSeries(vtc)
        if scw !=  "None":
           self.m_graph.addSeries(scw)
        if zpp !=  "None":
           self.m_graph.addSeries(zpp)
        if mab !=  "None":
           self.m_graph.addSeries(mab)
        if baa !=  "None":
           self.m_graph.addSeries(baa)
        if rpm !=  "None":
           self.m_graph.addSeries(rpm)
        if qxh !=  "None":
           self.m_graph.addSeries(qxh)
        if ofw !=  "None":
           self.m_graph.addSeries(ofw)
        if svl !=  "None":
           self.m_graph.addSeries(svl)
        if vrf !=  "None":
           self.m_graph.addSeries(vrf)
        if ilw !=  "None":
           self.m_graph.addSeries(ilw)
        if tgc !=  "None":
           self.m_graph.addSeries(tgc)
        if vnc !=  "None":
           self.m_graph.addSeries(vnc)
        if djd !=  "None":
           self.m_graph.addSeries(djd)
        if hcd !=  "None":
           self.m_graph.addSeries(hcd)
        if gzx !=  "None":
           self.m_graph.addSeries(gzx)
        if pkp !=  "None":
           self.m_graph.addSeries(pkp)
        if bbm !=  "None":
           self.m_graph.addSeries(bbm)
        if nyn !=  "None":
           self.m_graph.addSeries(nyn)
        if vha !=  "None":
           self.m_graph.addSeries(vha)
        if lpa !=  "None":
           self.m_graph.addSeries(lpa)
        if fsh !=  "None":
           self.m_graph.addSeries(fsh)
        if dce !=  "None":
           self.m_graph.addSeries(dce)
        if voi !=  "None":
           self.m_graph.addSeries(voi)
        if tpm !=  "None":
           self.m_graph.addSeries(tpm)
        if sqb !=  "None":
           self.m_graph.addSeries(sqb)
        if hsz !=  "None":
           self.m_graph.addSeries(hsz)
        if qjs !=  "None":
           self.m_graph.addSeries(qjs)
        if ngy !=  "None":
           self.m_graph.addSeries(ngy)
        if jte !=  "None":
           self.m_graph.addSeries(jte)
        if aep !=  "None":
           self.m_graph.addSeries(aep)
        if hmq !=  "None":
           self.m_graph.addSeries(hmq)
        if omd !=  "None":
           self.m_graph.addSeries(omd)
        if rhd !=  "None":
           self.m_graph.addSeries(rhd)
        if lqd !=  "None":
           self.m_graph.addSeries(lqd)
        if apj !=  "None":
           self.m_graph.addSeries(apj)
        if rft !=  "None":
           self.m_graph.addSeries(rft)
        if txx !=  "None":
           self.m_graph.addSeries(txx)
        if ytx !=  "None":
           self.m_graph.addSeries(ytx)
        if wve !=  "None":
           self.m_graph.addSeries(wve)
        if dqy !=  "None":
           self.m_graph.addSeries(dqy)
        if rzg !=  "None":
           self.m_graph.addSeries(rzg)
        if tow !=  "None":
           self.m_graph.addSeries(tow)
        if xla !=  "None":
           self.m_graph.addSeries(xla)
        if hho !=  "None":
           self.m_graph.addSeries(hho)
        if kmg !=  "None":
           self.m_graph.addSeries(kmg)
        if kxe !=  "None":
           self.m_graph.addSeries(kxe)
        if lii !=  "None":
           self.m_graph.addSeries(lii)
        if yjc !=  "None":
           self.m_graph.addSeries(yjc)
        if jgq !=  "None":
           self.m_graph.addSeries(jgq)
        if ygj !=  "None":
           self.m_graph.addSeries(ygj)
        if jdk !=  "None":
           self.m_graph.addSeries(jdk)
        if ucq !=  "None":
           self.m_graph.addSeries(ucq)
        if fyt !=  "None":
           self.m_graph.addSeries(fyt)
        if zia !=  "None":
           self.m_graph.addSeries(zia)
        if cxa !=  "None":
           self.m_graph.addSeries(cxa)
        if nnb !=  "None":
           self.m_graph.addSeries(nnb)
        if yde !=  "None":
           self.m_graph.addSeries(yde)
        if fdm !=  "None":
           self.m_graph.addSeries(fdm)
        if rpc !=  "None":
           self.m_graph.addSeries(rpc)
        if rrl !=  "None":
           self.m_graph.addSeries(rrl)
        if sef !=  "None":
           self.m_graph.addSeries(sef)
        if kbv !=  "None":
           self.m_graph.addSeries(kbv)
        if xag !=  "None":
           self.m_graph.addSeries(xag)
        if wzx !=  "None":
           self.m_graph.addSeries(wzx)
        if run !=  "None":
           self.m_graph.addSeries(run)
        if vze !=  "None":
           self.m_graph.addSeries(vze)
        if pcw !=  "None":
           self.m_graph.addSeries(pcw)
        if lki !=  "None":
           self.m_graph.addSeries(lki)
        if szt !=  "None":
           self.m_graph.addSeries(szt)
        if uko !=  "None":
           self.m_graph.addSeries(uko)
        if qcz !=  "None":
           self.m_graph.addSeries(qcz)
        if cpz !=  "None":
           self.m_graph.addSeries(cpz)
        if skj !=  "None":
           self.m_graph.addSeries(skj)
        if oeu !=  "None":
           self.m_graph.addSeries(oeu)
        if jst !=  "None":
           self.m_graph.addSeries(jst)
        if zmj !=  "None":
           self.m_graph.addSeries(zmj)
        if wmg !=  "None":
           self.m_graph.addSeries(wmg)
        if psu !=  "None":
           self.m_graph.addSeries(psu)
        if nvw !=  "None":
           self.m_graph.addSeries(nvw)
        if crg !=  "None":
           self.m_graph.addSeries(crg)
        if zwy !=  "None":
           self.m_graph.addSeries(zwy)
        if nab !=  "None":
           self.m_graph.addSeries(nab)
        if owy !=  "None":
           self.m_graph.addSeries(owy)
        if guv !=  "None":
           self.m_graph.addSeries(guv)
        if yyz !=  "None":
           self.m_graph.addSeries(yyz)
        if ohi !=  "None":
           self.m_graph.addSeries(ohi)
        if mse !=  "None":
           self.m_graph.addSeries(mse)
        if lwm !=  "None":
           self.m_graph.addSeries(lwm)
        if syn !=  "None":
           self.m_graph.addSeries(syn)
        if xkm !=  "None":
           self.m_graph.addSeries(xkm)
        if zih !=  "None":
           self.m_graph.addSeries(zih)
        if gct !=  "None":
           self.m_graph.addSeries(gct)
        if iap !=  "None":
           self.m_graph.addSeries(iap)
        if vnb !=  "None":
           self.m_graph.addSeries(vnb)
        if oua !=  "None":
           self.m_graph.addSeries(oua)
        if ebq !=  "None":
           self.m_graph.addSeries(ebq)
        if wjj !=  "None":
           self.m_graph.addSeries(wjj)
        if xkf !=  "None":
           self.m_graph.addSeries(xkf)
        if xri !=  "None":
           self.m_graph.addSeries(xri)
        if ehm !=  "None":
           self.m_graph.addSeries(ehm)
        if irq !=  "None":
           self.m_graph.addSeries(irq)
        if der !=  "None":
           self.m_graph.addSeries(der)
        if bhq !=  "None":
           self.m_graph.addSeries(bhq)
        if vwt !=  "None":
           self.m_graph.addSeries(vwt)
        if blc !=  "None":
           self.m_graph.addSeries(blc)
        if ahr !=  "None":
           self.m_graph.addSeries(ahr)
        if prl !=  "None":
           self.m_graph.addSeries(prl)
        if nhj !=  "None":
           self.m_graph.addSeries(nhj)
        if idd !=  "None":
           self.m_graph.addSeries(idd)
        if yry !=  "None":
           self.m_graph.addSeries(yry)
        if ciy !=  "None":
           self.m_graph.addSeries(ciy)
        if ypl !=  "None":
           self.m_graph.addSeries(ypl)
        if zth !=  "None":
           self.m_graph.addSeries(zth)
        if avy !=  "None":
           self.m_graph.addSeries(avy)
        if jky !=  "None":
           self.m_graph.addSeries(jky)
        if wtq !=  "None":
           self.m_graph.addSeries(wtq)
        if bpi !=  "None":
           self.m_graph.addSeries(bpi)
        if ioe !=  "None":
           self.m_graph.addSeries(ioe)
        if jeo !=  "None":
           self.m_graph.addSeries(jeo)
        if gtu !=  "None":
           self.m_graph.addSeries(gtu)
        if epv !=  "None":
           self.m_graph.addSeries(epv)
        if plw !=  "None":
           self.m_graph.addSeries(plw)
        if guu !=  "None":
           self.m_graph.addSeries(guu)
        if wks !=  "None":
           self.m_graph.addSeries(wks)
        if wsp !=  "None":
           self.m_graph.addSeries(wsp)
        if zbo !=  "None":
           self.m_graph.addSeries(zbo)
        if exf !=  "None":
           self.m_graph.addSeries(exf)
        if cyf !=  "None":
           self.m_graph.addSeries(cyf)
        if haj !=  "None":
           self.m_graph.addSeries(haj)
        if zvx !=  "None":
           self.m_graph.addSeries(zvx)
        if ovq !=  "None":
           self.m_graph.addSeries(ovq)
        if bwr !=  "None":
           self.m_graph.addSeries(bwr)
        if zxd !=  "None":
           self.m_graph.addSeries(zxd)
        if llj !=  "None":
           self.m_graph.addSeries(llj)
        if bjo !=  "None":
           self.m_graph.addSeries(bjo)
        if vva !=  "None":
           self.m_graph.addSeries(vva)
        if fwu !=  "None":
           self.m_graph.addSeries(fwu)
        if xuz !=  "None":
           self.m_graph.addSeries(xuz)
        if cgh !=  "None":
           self.m_graph.addSeries(cgh)
        if gzs !=  "None":
           self.m_graph.addSeries(gzs)
        if rxw !=  "None":
           self.m_graph.addSeries(rxw)
        if ami !=  "None":
           self.m_graph.addSeries(ami)
        if zib !=  "None":
           self.m_graph.addSeries(zib)
        if ukm !=  "None":
           self.m_graph.addSeries(ukm)
        if xce !=  "None":
           self.m_graph.addSeries(xce)
        if mgt !=  "None":
           self.m_graph.addSeries(mgt)
        if vfs !=  "None":
           self.m_graph.addSeries(vfs)
        if noo !=  "None":
           self.m_graph.addSeries(noo)
        if kac !=  "None":
           self.m_graph.addSeries(kac)
        if uul !=  "None":
           self.m_graph.addSeries(uul)
        if eat !=  "None":
           self.m_graph.addSeries(eat)
        if lvt !=  "None":
           self.m_graph.addSeries(lvt)
        if fsj !=  "None":
           self.m_graph.addSeries(fsj)
        if qur !=  "None":
           self.m_graph.addSeries(qur)
        if hju !=  "None":
           self.m_graph.addSeries(hju)
        if mcr !=  "None":
           self.m_graph.addSeries(mcr)
        if eze !=  "None":
           self.m_graph.addSeries(eze)
        if cbr !=  "None":
           self.m_graph.addSeries(cbr)
        if jvl !=  "None":
           self.m_graph.addSeries(jvl)
        if foz !=  "None":
           self.m_graph.addSeries(foz)
        if veg !=  "None":
           self.m_graph.addSeries(veg)
        if pqg !=  "None":
           self.m_graph.addSeries(pqg)
        if qig !=  "None":
           self.m_graph.addSeries(qig)
        if eut !=  "None":
           self.m_graph.addSeries(eut)
        if fif !=  "None":
           self.m_graph.addSeries(fif)
        if qoi !=  "None":
           self.m_graph.addSeries(qoi)
        if kti !=  "None":
           self.m_graph.addSeries(kti)
        if vcn !=  "None":
           self.m_graph.addSeries(vcn)
        if mib !=  "None":
           self.m_graph.addSeries(mib)
        if ivv !=  "None":
           self.m_graph.addSeries(ivv)
        if eob !=  "None":
           self.m_graph.addSeries(eob)
        if eel !=  "None":
           self.m_graph.addSeries(eel)
        if nma !=  "None":
           self.m_graph.addSeries(nma)
        if ljp !=  "None":
           self.m_graph.addSeries(ljp)
        if kel !=  "None":
           self.m_graph.addSeries(kel)
        if kfh !=  "None":
           self.m_graph.addSeries(kfh)
        if tqw !=  "None":
           self.m_graph.addSeries(tqw)
        if uoi !=  "None":
           self.m_graph.addSeries(uoi)
        if tza !=  "None":
           self.m_graph.addSeries(tza)
        if eyg !=  "None":
           self.m_graph.addSeries(eyg)
        if kyi !=  "None":
           self.m_graph.addSeries(kyi)
        if dlt !=  "None":
           self.m_graph.addSeries(dlt)
        if ffp !=  "None":
           self.m_graph.addSeries(ffp)
        if knu !=  "None":
           self.m_graph.addSeries(knu)
        if wtf !=  "None":
           self.m_graph.addSeries(wtf)
        if qtc !=  "None":
           self.m_graph.addSeries(qtc)
        if xnn !=  "None":
           self.m_graph.addSeries(xnn)
        if uzm !=  "None":
           self.m_graph.addSeries(uzm)
        if dvz !=  "None":
           self.m_graph.addSeries(dvz)
        if ifn !=  "None":
           self.m_graph.addSeries(ifn)
        if skf !=  "None":
           self.m_graph.addSeries(skf)
        if ghc !=  "None":
           self.m_graph.addSeries(ghc)
        if lif !=  "None":
           self.m_graph.addSeries(lif)
        if rdt !=  "None":
           self.m_graph.addSeries(rdt)
        if qwg !=  "None":
           self.m_graph.addSeries(qwg)
        if pbs !=  "None":
           self.m_graph.addSeries(pbs)
        if igo !=  "None":
           self.m_graph.addSeries(igo)
        if ksi !=  "None":
           self.m_graph.addSeries(ksi)
        if sde !=  "None":
           self.m_graph.addSeries(sde)
        if irk !=  "None":
           self.m_graph.addSeries(irk)
        if ccs !=  "None":
           self.m_graph.addSeries(ccs)
        if adf !=  "None":
           self.m_graph.addSeries(adf)
        if api !=  "None":
           self.m_graph.addSeries(api)
        if thi !=  "None":
           self.m_graph.addSeries(thi)
        if rlm !=  "None":
           self.m_graph.addSeries(rlm)
        if rql !=  "None":
           self.m_graph.addSeries(rql)
        if itk !=  "None":
           self.m_graph.addSeries(itk)
        if eyo !=  "None":
           self.m_graph.addSeries(eyo)
        if tjt !=  "None":
           self.m_graph.addSeries(tjt)
        if bdc !=  "None":
           self.m_graph.addSeries(bdc)
        if ksy !=  "None":
           self.m_graph.addSeries(ksy)
        if qke !=  "None":
           self.m_graph.addSeries(qke)
        if ulo !=  "None":
           self.m_graph.addSeries(ulo)
        if xyf !=  "None":
           self.m_graph.addSeries(xyf)
        if zxp !=  "None":
           self.m_graph.addSeries(zxp)
        if wqi !=  "None":
           self.m_graph.addSeries(wqi)
        if yav !=  "None":
           self.m_graph.addSeries(yav)
        if ixt !=  "None":
           self.m_graph.addSeries(ixt)
        if rwe !=  "None":
           self.m_graph.addSeries(rwe)
        if hdp !=  "None":
           self.m_graph.addSeries(hdp)
        if bfh !=  "None":
           self.m_graph.addSeries(bfh)
        if wom !=  "None":
           self.m_graph.addSeries(wom)
        if ozc !=  "None":
           self.m_graph.addSeries(ozc)
        if bkp !=  "None":
           self.m_graph.addSeries(bkp)
        if qhf !=  "None":
           self.m_graph.addSeries(qhf)
        if sib !=  "None":
           self.m_graph.addSeries(sib)
        if vmj !=  "None":
           self.m_graph.addSeries(vmj)
        if exv !=  "None":
           self.m_graph.addSeries(exv)
        if hom !=  "None":
           self.m_graph.addSeries(hom)
        if zlf !=  "None":
           self.m_graph.addSeries(zlf)
        if lpw !=  "None":
           self.m_graph.addSeries(lpw)
        if sil !=  "None":
           self.m_graph.addSeries(sil)
        if sko !=  "None":
           self.m_graph.addSeries(sko)
        if scr !=  "None":
           self.m_graph.addSeries(scr)
        if vba !=  "None":
           self.m_graph.addSeries(vba)
        if krh !=  "None":
           self.m_graph.addSeries(krh)
        if oxk !=  "None":
           self.m_graph.addSeries(oxk)
        if zek !=  "None":
           self.m_graph.addSeries(zek)
        if atx !=  "None":
           self.m_graph.addSeries(atx)
        if fss !=  "None":
           self.m_graph.addSeries(fss)
        if trt !=  "None":
           self.m_graph.addSeries(trt)
        if pee !=  "None":
           self.m_graph.addSeries(pee)
        if vkr !=  "None":
           self.m_graph.addSeries(vkr)
        if ajn !=  "None":
           self.m_graph.addSeries(ajn)
        if woc !=  "None":
           self.m_graph.addSeries(woc)
        if kiu !=  "None":
           self.m_graph.addSeries(kiu)
        if yyd !=  "None":
           self.m_graph.addSeries(yyd)
        if gga !=  "None":
           self.m_graph.addSeries(gga)
        if lgl !=  "None":
           self.m_graph.addSeries(lgl)
        if jty !=  "None":
           self.m_graph.addSeries(jty)
        if mjn !=  "None":
           self.m_graph.addSeries(mjn)
        if zxq !=  "None":
           self.m_graph.addSeries(zxq)
        if qzy !=  "None":
           self.m_graph.addSeries(qzy)
        if uxa !=  "None":
           self.m_graph.addSeries(uxa)
        if qir !=  "None":
           self.m_graph.addSeries(qir)
        if lkn !=  "None":
           self.m_graph.addSeries(lkn)
        if aaq !=  "None":
           self.m_graph.addSeries(aaq)
        if ssg !=  "None":
           self.m_graph.addSeries(ssg)
        if wbl !=  "None":
           self.m_graph.addSeries(wbl)
        if ofe !=  "None":
           self.m_graph.addSeries(ofe)
        if yev !=  "None":
           self.m_graph.addSeries(yev)
        if zin !=  "None":
           self.m_graph.addSeries(zin)
        if toq !=  "None":
           self.m_graph.addSeries(toq)
        if pwh !=  "None":
           self.m_graph.addSeries(pwh)
        if dad !=  "None":
           self.m_graph.addSeries(dad)
        if ogz !=  "None":
           self.m_graph.addSeries(ogz)
        if mdl !=  "None":
           self.m_graph.addSeries(mdl)
        if zxe !=  "None":
           self.m_graph.addSeries(zxe)
        if ces !=  "None":
           self.m_graph.addSeries(ces)
        if efs !=  "None":
           self.m_graph.addSeries(efs)
        if pxy !=  "None":
           self.m_graph.addSeries(pxy)
        if odd !=  "None":
           self.m_graph.addSeries(odd)
        if rdd !=  "None":
           self.m_graph.addSeries(rdd)
        if yjb !=  "None":
           self.m_graph.addSeries(yjb)
        if zsw !=  "None":
           self.m_graph.addSeries(zsw)
        if icn !=  "None":
           self.m_graph.addSeries(icn)
        if qzw !=  "None":
           self.m_graph.addSeries(qzw)
        if epc !=  "None":
           self.m_graph.addSeries(epc)
        if lck !=  "None":
           self.m_graph.addSeries(lck)
        if wfi !=  "None":
           self.m_graph.addSeries(wfi)
        if xlo !=  "None":
           self.m_graph.addSeries(xlo)
        if ymo !=  "None":
           self.m_graph.addSeries(ymo)
        if eql !=  "None":
           self.m_graph.addSeries(eql)
        if baf !=  "None":
           self.m_graph.addSeries(baf)
        if qlf !=  "None":
           self.m_graph.addSeries(qlf)
        if yaf !=  "None":
           self.m_graph.addSeries(yaf)
        if rji !=  "None":
           self.m_graph.addSeries(rji)
        if ahc !=  "None":
           self.m_graph.addSeries(ahc)
        if xiy !=  "None":
           self.m_graph.addSeries(xiy)
        if qzv !=  "None":
           self.m_graph.addSeries(qzv)
        if qif !=  "None":
           self.m_graph.addSeries(qif)
        if xoh !=  "None":
           self.m_graph.addSeries(xoh)
        if rvb !=  "None":
           self.m_graph.addSeries(rvb)
        if vrz !=  "None":
           self.m_graph.addSeries(vrz)
        if fbs !=  "None":
           self.m_graph.addSeries(fbs)
        if shx !=  "None":
           self.m_graph.addSeries(shx)
        if pea !=  "None":
           self.m_graph.addSeries(pea)
        if ggr !=  "None":
           self.m_graph.addSeries(ggr)
        if ccm !=  "None":
           self.m_graph.addSeries(ccm)
        if tpi !=  "None":
           self.m_graph.addSeries(tpi)
        if thk !=  "None":
           self.m_graph.addSeries(thk)
        if wfn !=  "None":
           self.m_graph.addSeries(wfn)
        if tup !=  "None":
           self.m_graph.addSeries(tup)
        if qgj !=  "None":
           self.m_graph.addSeries(qgj)
        if pxo !=  "None":
           self.m_graph.addSeries(pxo)
        if zrs !=  "None":
           self.m_graph.addSeries(zrs)
        if sxb !=  "None":
           self.m_graph.addSeries(sxb)
        if gki !=  "None":
           self.m_graph.addSeries(gki)
        if efk !=  "None":
           self.m_graph.addSeries(efk)
        if giz !=  "None":
           self.m_graph.addSeries(giz)
        if isl !=  "None":
           self.m_graph.addSeries(isl)
        if qjk !=  "None":
           self.m_graph.addSeries(qjk)
        if pkv !=  "None":
           self.m_graph.addSeries(pkv)
        if rao !=  "None":
           self.m_graph.addSeries(rao)
        if pxj !=  "None":
           self.m_graph.addSeries(pxj)
        if hxz !=  "None":
           self.m_graph.addSeries(hxz)
        if fxr !=  "None":
           self.m_graph.addSeries(fxr)
        if hdy !=  "None":
           self.m_graph.addSeries(hdy)
        if jqs !=  "None":
           self.m_graph.addSeries(jqs)
        if ewv !=  "None":
           self.m_graph.addSeries(ewv)
        if qcw !=  "None":
           self.m_graph.addSeries(qcw)
        if fdz !=  "None":
           self.m_graph.addSeries(fdz)
        if nad !=  "None":
           self.m_graph.addSeries(nad)
        if qtd !=  "None":
           self.m_graph.addSeries(qtd)
        if vsg !=  "None":
           self.m_graph.addSeries(vsg)
        if tfw !=  "None":
           self.m_graph.addSeries(tfw)
        if zfe !=  "None":
           self.m_graph.addSeries(zfe)
        if jip !=  "None":
           self.m_graph.addSeries(jip)
        if vwk !=  "None":
           self.m_graph.addSeries(vwk)
        if rty !=  "None":
           self.m_graph.addSeries(rty)
        if vre !=  "None":
           self.m_graph.addSeries(vre)
        if osl !=  "None":
           self.m_graph.addSeries(osl)
        if aki !=  "None":
           self.m_graph.addSeries(aki)
        if eja !=  "None":
           self.m_graph.addSeries(eja)
        if eop !=  "None":
           self.m_graph.addSeries(eop)
        if eea !=  "None":
           self.m_graph.addSeries(eea)
        if nbx !=  "None":
           self.m_graph.addSeries(nbx)
        if uxz !=  "None":
           self.m_graph.addSeries(uxz)
        if qck !=  "None":
           self.m_graph.addSeries(qck)
        if evw !=  "None":
           self.m_graph.addSeries(evw)
        if lnv !=  "None":
           self.m_graph.addSeries(lnv)
        if llc !=  "None":
           self.m_graph.addSeries(llc)
        if gnb !=  "None":
           self.m_graph.addSeries(gnb)
        if voa !=  "None":
           self.m_graph.addSeries(voa)
        if cdb !=  "None":
           self.m_graph.addSeries(cdb)
        if cqv !=  "None":
           self.m_graph.addSeries(cqv)
        if kkp !=  "None":
           self.m_graph.addSeries(kkp)
        if ecx !=  "None":
           self.m_graph.addSeries(ecx)
        if ren !=  "None":
           self.m_graph.addSeries(ren)
        if iri !=  "None":
           self.m_graph.addSeries(iri)
        if kmf !=  "None":
           self.m_graph.addSeries(kmf)
        if pep !=  "None":
           self.m_graph.addSeries(pep)
        if bpd !=  "None":
           self.m_graph.addSeries(bpd)
        if thu !=  "None":
           self.m_graph.addSeries(thu)
        if yem !=  "None":
           self.m_graph.addSeries(yem)
        if nac !=  "None":
           self.m_graph.addSeries(nac)
        if ipi !=  "None":
           self.m_graph.addSeries(ipi)
        if jbx !=  "None":
           self.m_graph.addSeries(jbx)
        if owh !=  "None":
           self.m_graph.addSeries(owh)
        if kwx !=  "None":
           self.m_graph.addSeries(kwx)
        if asc !=  "None":
           self.m_graph.addSeries(asc)
        if sfj !=  "None":
           self.m_graph.addSeries(sfj)
        if mct !=  "None":
           self.m_graph.addSeries(mct)
        if drb !=  "None":
           self.m_graph.addSeries(drb)
        if tch !=  "None":
           self.m_graph.addSeries(tch)
        if eko !=  "None":
           self.m_graph.addSeries(eko)
        if tzq !=  "None":
           self.m_graph.addSeries(tzq)
        if iqj !=  "None":
           self.m_graph.addSeries(iqj)
        if tcn !=  "None":
           self.m_graph.addSeries(tcn)
        if cns !=  "None":
           self.m_graph.addSeries(cns)
        if slk !=  "None":
           self.m_graph.addSeries(slk)
        if cje !=  "None":
           self.m_graph.addSeries(cje)
        if hsj !=  "None":
           self.m_graph.addSeries(hsj)
        if elp !=  "None":
           self.m_graph.addSeries(elp)
        if xfs !=  "None":
           self.m_graph.addSeries(xfs)
        if sba !=  "None":
           self.m_graph.addSeries(sba)
        if ocb !=  "None":
           self.m_graph.addSeries(ocb)
        if cnq !=  "None":
           self.m_graph.addSeries(cnq)
        if rnz !=  "None":
           self.m_graph.addSeries(rnz)
        if tcl !=  "None":
           self.m_graph.addSeries(tcl)
        if hxt !=  "None":
           self.m_graph.addSeries(hxt)
        if tmi !=  "None":
           self.m_graph.addSeries(tmi)
        if tiz !=  "None":
           self.m_graph.addSeries(tiz)
        if olz !=  "None":
           self.m_graph.addSeries(olz)
        if qba !=  "None":
           self.m_graph.addSeries(qba)
        if lgr !=  "None":
           self.m_graph.addSeries(lgr)
        if xhs !=  "None":
           self.m_graph.addSeries(xhs)
        if ear !=  "None":
           self.m_graph.addSeries(ear)
        if ddp !=  "None":
           self.m_graph.addSeries(ddp)
        if sjq !=  "None":
           self.m_graph.addSeries(sjq)
        if gnr !=  "None":
           self.m_graph.addSeries(gnr)
        if omc !=  "None":
           self.m_graph.addSeries(omc)
        if ldv !=  "None":
           self.m_graph.addSeries(ldv)
        if ecr !=  "None":
           self.m_graph.addSeries(ecr)
        if zmf !=  "None":
           self.m_graph.addSeries(zmf)
        if emi !=  "None":
           self.m_graph.addSeries(emi)
        if tlj !=  "None":
           self.m_graph.addSeries(tlj)
        if ekt !=  "None":
           self.m_graph.addSeries(ekt)
        if enh !=  "None":
           self.m_graph.addSeries(enh)
        if fkm !=  "None":
           self.m_graph.addSeries(fkm)
        if lmo !=  "None":
           self.m_graph.addSeries(lmo)
        if dqc !=  "None":
           self.m_graph.addSeries(dqc)
        if ovo !=  "None":
           self.m_graph.addSeries(ovo)
        if pqy !=  "None":
           self.m_graph.addSeries(pqy)
        if fqv !=  "None":
           self.m_graph.addSeries(fqv)
        if nmi !=  "None":
           self.m_graph.addSeries(nmi)
        if dcx !=  "None":
           self.m_graph.addSeries(dcx)
        if ypf !=  "None":
           self.m_graph.addSeries(ypf)
        if toa !=  "None":
           self.m_graph.addSeries(toa)
        if ilc !=  "None":
           self.m_graph.addSeries(ilc)
        if ixo !=  "None":
           self.m_graph.addSeries(ixo)
        if kpn !=  "None":
           self.m_graph.addSeries(kpn)
        if nms !=  "None":
           self.m_graph.addSeries(nms)
        if mhh !=  "None":
           self.m_graph.addSeries(mhh)
        if tpw !=  "None":
           self.m_graph.addSeries(tpw)
        if cpg !=  "None":
           self.m_graph.addSeries(cpg)
        if qmw !=  "None":
           self.m_graph.addSeries(qmw)
        if irz !=  "None":
           self.m_graph.addSeries(irz)
        if fxv !=  "None":
           self.m_graph.addSeries(fxv)
        if nwr !=  "None":
           self.m_graph.addSeries(nwr)
        if inx !=  "None":
           self.m_graph.addSeries(inx)
        if ojg !=  "None":
           self.m_graph.addSeries(ojg)
        if ojq !=  "None":
           self.m_graph.addSeries(ojq)
        if rcy !=  "None":
           self.m_graph.addSeries(rcy)
        if pwi !=  "None":
           self.m_graph.addSeries(pwi)
        if rcj !=  "None":
           self.m_graph.addSeries(rcj)
        if cfj !=  "None":
           self.m_graph.addSeries(cfj)
        if wkx !=  "None":
           self.m_graph.addSeries(wkx)
        if npk !=  "None":
           self.m_graph.addSeries(npk)
        if ssj !=  "None":
           self.m_graph.addSeries(ssj)
        if inj !=  "None":
           self.m_graph.addSeries(inj)
        if ika !=  "None":
           self.m_graph.addSeries(ika)
        if mfe !=  "None":
           self.m_graph.addSeries(mfe)
        if sgv !=  "None":
           self.m_graph.addSeries(sgv)
        if hce !=  "None":
           self.m_graph.addSeries(hce)
        if jso !=  "None":
           self.m_graph.addSeries(jso)
        if kxi !=  "None":
           self.m_graph.addSeries(kxi)
        if coo !=  "None":
           self.m_graph.addSeries(coo)
        if dxa !=  "None":
           self.m_graph.addSeries(dxa)
        if euy !=  "None":
           self.m_graph.addSeries(euy)
        if lkk !=  "None":
           self.m_graph.addSeries(lkk)
        if jkd !=  "None":
           self.m_graph.addSeries(jkd)
        if kvo !=  "None":
           self.m_graph.addSeries(kvo)
        if dqz !=  "None":
           self.m_graph.addSeries(dqz)
        if hmy !=  "None":
           self.m_graph.addSeries(hmy)
        if pac !=  "None":
           self.m_graph.addSeries(pac)
        if vhf !=  "None":
           self.m_graph.addSeries(vhf)
        if ohw !=  "None":
           self.m_graph.addSeries(ohw)
        if amv !=  "None":
           self.m_graph.addSeries(amv)
        if sfo !=  "None":
           self.m_graph.addSeries(sfo)
        if wqc !=  "None":
           self.m_graph.addSeries(wqc)
        if mpf !=  "None":
           self.m_graph.addSeries(mpf)
        if rtg !=  "None":
           self.m_graph.addSeries(rtg)
        if fqo !=  "None":
           self.m_graph.addSeries(fqo)
        if qav !=  "None":
           self.m_graph.addSeries(qav)
        if jqa !=  "None":
           self.m_graph.addSeries(jqa)
        if sdm !=  "None":
           self.m_graph.addSeries(sdm)
        if vyv !=  "None":
           self.m_graph.addSeries(vyv)
        if gba !=  "None":
           self.m_graph.addSeries(gba)
        if qhb !=  "None":
           self.m_graph.addSeries(qhb)
        if dyd !=  "None":
           self.m_graph.addSeries(dyd)
        if pzq !=  "None":
           self.m_graph.addSeries(pzq)
        if wxz !=  "None":
           self.m_graph.addSeries(wxz)
        if jxy !=  "None":
           self.m_graph.addSeries(jxy)
        if cpw !=  "None":
           self.m_graph.addSeries(cpw)
        if rfj !=  "None":
           self.m_graph.addSeries(rfj)
        if kqo !=  "None":
           self.m_graph.addSeries(kqo)
        if lkb !=  "None":
           self.m_graph.addSeries(lkb)
        if pol !=  "None":
           self.m_graph.addSeries(pol)
        if nyg !=  "None":
           self.m_graph.addSeries(nyg)
        if wau !=  "None":
           self.m_graph.addSeries(wau)
        if ogo !=  "None":
           self.m_graph.addSeries(ogo)
        if lzw !=  "None":
           self.m_graph.addSeries(lzw)
        if jza !=  "None":
           self.m_graph.addSeries(jza)
        if hqj !=  "None":
           self.m_graph.addSeries(hqj)
        if ivb !=  "None":
           self.m_graph.addSeries(ivb)
        if zlv !=  "None":
           self.m_graph.addSeries(zlv)
        if jgc !=  "None":
           self.m_graph.addSeries(jgc)
        if vda !=  "None":
           self.m_graph.addSeries(vda)
        if gtk !=  "None":
           self.m_graph.addSeries(gtk)
        if aio !=  "None":
           self.m_graph.addSeries(aio)
        if unl !=  "None":
           self.m_graph.addSeries(unl)
        if nwe !=  "None":
           self.m_graph.addSeries(nwe)
        if xza !=  "None":
           self.m_graph.addSeries(xza)
        if rjl !=  "None":
           self.m_graph.addSeries(rjl)
        if gue !=  "None":
           self.m_graph.addSeries(gue)
        if xvo !=  "None":
           self.m_graph.addSeries(xvo)
        if eyc !=  "None":
           self.m_graph.addSeries(eyc)
        if blk !=  "None":
           self.m_graph.addSeries(blk)
        if lzs !=  "None":
           self.m_graph.addSeries(lzs)
        if ibr !=  "None":
           self.m_graph.addSeries(ibr)
        if ndj !=  "None":
           self.m_graph.addSeries(ndj)
        if tld !=  "None":
           self.m_graph.addSeries(tld)
        if fow !=  "None":
           self.m_graph.addSeries(fow)
        if vun !=  "None":
           self.m_graph.addSeries(vun)
        if voh !=  "None":
           self.m_graph.addSeries(voh)
        if wns !=  "None":
           self.m_graph.addSeries(wns)
        if otj !=  "None":
           self.m_graph.addSeries(otj)
        if ahn !=  "None":
           self.m_graph.addSeries(ahn)
        if lhk !=  "None":
           self.m_graph.addSeries(lhk)
        if wpe !=  "None":
           self.m_graph.addSeries(wpe)
        if myq !=  "None":
           self.m_graph.addSeries(myq)
        if ovs !=  "None":
           self.m_graph.addSeries(ovs)
        if yrt !=  "None":
           self.m_graph.addSeries(yrt)
        if ifx !=  "None":
           self.m_graph.addSeries(ifx)
        if dsc !=  "None":
           self.m_graph.addSeries(dsc)
        if jdw !=  "None":
           self.m_graph.addSeries(jdw)
        if wge !=  "None":
           self.m_graph.addSeries(wge)
        if gnv !=  "None":
           self.m_graph.addSeries(gnv)
        if kfx !=  "None":
           self.m_graph.addSeries(kfx)
        if lgd !=  "None":
           self.m_graph.addSeries(lgd)
        if snv !=  "None":
           self.m_graph.addSeries(snv)
        if iva !=  "None":
           self.m_graph.addSeries(iva)
        if wkf !=  "None":
           self.m_graph.addSeries(wkf)
        if cjn !=  "None":
           self.m_graph.addSeries(cjn)
        if aay !=  "None":
           self.m_graph.addSeries(aay)
        if rzt !=  "None":
           self.m_graph.addSeries(rzt)
        if aek !=  "None":
           self.m_graph.addSeries(aek)
        if jtw !=  "None":
           self.m_graph.addSeries(jtw)
        if oye !=  "None":
           self.m_graph.addSeries(oye)
        if vvz !=  "None":
           self.m_graph.addSeries(vvz)
        if qay !=  "None":
           self.m_graph.addSeries(qay)
        if cjj !=  "None":
           self.m_graph.addSeries(cjj)
        if sxw !=  "None":
           self.m_graph.addSeries(sxw)
        if iyd !=  "None":
           self.m_graph.addSeries(iyd)
        if kio !=  "None":
           self.m_graph.addSeries(kio)
        if tud !=  "None":
           self.m_graph.addSeries(tud)
        if dmi !=  "None":
           self.m_graph.addSeries(dmi)
        if yqz !=  "None":
           self.m_graph.addSeries(yqz)
        if hyw !=  "None":
           self.m_graph.addSeries(hyw)
        if dex !=  "None":
           self.m_graph.addSeries(dex)
        if oju !=  "None":
           self.m_graph.addSeries(oju)
        if usw !=  "None":
           self.m_graph.addSeries(usw)
        if hxh !=  "None":
           self.m_graph.addSeries(hxh)
        if mvc !=  "None":
           self.m_graph.addSeries(mvc)
        if pis !=  "None":
           self.m_graph.addSeries(pis)
        if pnx !=  "None":
           self.m_graph.addSeries(pnx)
        if geu !=  "None":
           self.m_graph.addSeries(geu)
        if xau !=  "None":
           self.m_graph.addSeries(xau)
        if noc !=  "None":
           self.m_graph.addSeries(noc)
        if oyd !=  "None":
           self.m_graph.addSeries(oyd)
        if lod !=  "None":
           self.m_graph.addSeries(lod)
        if xyl !=  "None":
           self.m_graph.addSeries(xyl)
        if zmi !=  "None":
           self.m_graph.addSeries(zmi)
        if sob !=  "None":
           self.m_graph.addSeries(sob)
        if axq !=  "None":
           self.m_graph.addSeries(axq)
        if hbb !=  "None":
           self.m_graph.addSeries(hbb)
        if uaj !=  "None":
           self.m_graph.addSeries(uaj)
        if zln !=  "None":
           self.m_graph.addSeries(zln)
        if pnj !=  "None":
           self.m_graph.addSeries(pnj)
        if ylk !=  "None":
           self.m_graph.addSeries(ylk)
        if ghr !=  "None":
           self.m_graph.addSeries(ghr)
        if nag !=  "None":
           self.m_graph.addSeries(nag)
        if wnl !=  "None":
           self.m_graph.addSeries(wnl)
        if kxh !=  "None":
           self.m_graph.addSeries(kxh)
        if roc !=  "None":
           self.m_graph.addSeries(roc)
        if ynv !=  "None":
           self.m_graph.addSeries(ynv)
        if pdk !=  "None":
           self.m_graph.addSeries(pdk)
        if bnc !=  "None":
           self.m_graph.addSeries(bnc)
        if cub !=  "None":
           self.m_graph.addSeries(cub)
        if rbd !=  "None":
           self.m_graph.addSeries(rbd)
        if cgl !=  "None":
           self.m_graph.addSeries(cgl)
        if rtl !=  "None":
           self.m_graph.addSeries(rtl)
        if tln !=  "None":
           self.m_graph.addSeries(tln)
        if xfu !=  "None":
           self.m_graph.addSeries(xfu)
        if aed !=  "None":
           self.m_graph.addSeries(aed)
        if bwk !=  "None":
           self.m_graph.addSeries(bwk)
        if bmm !=  "None":
           self.m_graph.addSeries(bmm)
        if eqf !=  "None":
           self.m_graph.addSeries(eqf)
        if eoa !=  "None":
           self.m_graph.addSeries(eoa)
        if ahm !=  "None":
           self.m_graph.addSeries(ahm)
        if ayv !=  "None":
           self.m_graph.addSeries(ayv)
        if gbm !=  "None":
           self.m_graph.addSeries(gbm)
        if qkq !=  "None":
           self.m_graph.addSeries(qkq)
        if qkz !=  "None":
           self.m_graph.addSeries(qkz)
        if cyb !=  "None":
           self.m_graph.addSeries(cyb)
        if jmp !=  "None":
           self.m_graph.addSeries(jmp)
        if mcg !=  "None":
           self.m_graph.addSeries(mcg)
        if kkz !=  "None":
           self.m_graph.addSeries(kkz)
        if abg !=  "None":
           self.m_graph.addSeries(abg)
        if sqz !=  "None":
           self.m_graph.addSeries(sqz)
        if ttz !=  "None":
           self.m_graph.addSeries(ttz)
        if voz !=  "None":
           self.m_graph.addSeries(voz)
        if nis !=  "None":
           self.m_graph.addSeries(nis)
        if vsw !=  "None":
           self.m_graph.addSeries(vsw)
        if aye !=  "None":
           self.m_graph.addSeries(aye)
        if aya !=  "None":
           self.m_graph.addSeries(aya)
        if vlz !=  "None":
           self.m_graph.addSeries(vlz)
        if pur !=  "None":
           self.m_graph.addSeries(pur)
        if lnl !=  "None":
           self.m_graph.addSeries(lnl)
        if mpa !=  "None":
           self.m_graph.addSeries(mpa)
        if bee !=  "None":
           self.m_graph.addSeries(bee)
        if xrx !=  "None":
           self.m_graph.addSeries(xrx)
        if gwq !=  "None":
           self.m_graph.addSeries(gwq)
        if bpb !=  "None":
           self.m_graph.addSeries(bpb)
        if kyp !=  "None":
           self.m_graph.addSeries(kyp)
        if mbb !=  "None":
           self.m_graph.addSeries(mbb)
        if fdr !=  "None":
           self.m_graph.addSeries(fdr)
        if ixh !=  "None":
           self.m_graph.addSeries(ixh)
        if xey !=  "None":
           self.m_graph.addSeries(xey)
        if jhu !=  "None":
           self.m_graph.addSeries(jhu)
        if hvq !=  "None":
           self.m_graph.addSeries(hvq)
        if hgo !=  "None":
           self.m_graph.addSeries(hgo)
        if sjm !=  "None":
           self.m_graph.addSeries(sjm)
        if vyh !=  "None":
           self.m_graph.addSeries(vyh)
        if mbh !=  "None":
           self.m_graph.addSeries(mbh)
        if etr !=  "None":
           self.m_graph.addSeries(etr)
        if vhy !=  "None":
           self.m_graph.addSeries(vhy)
        if ewc !=  "None":
           self.m_graph.addSeries(ewc)
        if lsx !=  "None":
           self.m_graph.addSeries(lsx)
        if uwb !=  "None":
           self.m_graph.addSeries(uwb)
        if cig !=  "None":
           self.m_graph.addSeries(cig)
        if yyy !=  "None":
           self.m_graph.addSeries(yyy)
        if nwq !=  "None":
           self.m_graph.addSeries(nwq)
        if ixp !=  "None":
           self.m_graph.addSeries(ixp)
        if yqm !=  "None":
           self.m_graph.addSeries(yqm)
        if qaj !=  "None":
           self.m_graph.addSeries(qaj)
        if kyv !=  "None":
           self.m_graph.addSeries(kyv)
        if rln !=  "None":
           self.m_graph.addSeries(rln)
        if lrd !=  "None":
           self.m_graph.addSeries(lrd)
        if tfe !=  "None":
           self.m_graph.addSeries(tfe)
        if kna !=  "None":
           self.m_graph.addSeries(kna)
        if puq !=  "None":
           self.m_graph.addSeries(puq)
        if vve !=  "None":
           self.m_graph.addSeries(vve)
        if esf !=  "None":
           self.m_graph.addSeries(esf)
        if tnf !=  "None":
           self.m_graph.addSeries(tnf)
        if kef !=  "None":
           self.m_graph.addSeries(kef)
        if yqv !=  "None":
           self.m_graph.addSeries(yqv)
        if gtt !=  "None":
           self.m_graph.addSeries(gtt)
        if pou !=  "None":
           self.m_graph.addSeries(pou)
        if fvc !=  "None":
           self.m_graph.addSeries(fvc)
        if eug !=  "None":
           self.m_graph.addSeries(eug)
        if xqv !=  "None":
           self.m_graph.addSeries(xqv)
        if edk !=  "None":
           self.m_graph.addSeries(edk)
        if yrg !=  "None":
           self.m_graph.addSeries(yrg)
        if emx !=  "None":
           self.m_graph.addSeries(emx)
        if zkz !=  "None":
           self.m_graph.addSeries(zkz)
        if xgl !=  "None":
           self.m_graph.addSeries(xgl)
        if ssq !=  "None":
           self.m_graph.addSeries(ssq)
        if eoc !=  "None":
           self.m_graph.addSeries(eoc)
        if thw !=  "None":
           self.m_graph.addSeries(thw)
        if ksf !=  "None":
           self.m_graph.addSeries(ksf)
        if bir !=  "None":
           self.m_graph.addSeries(bir)
        if dcp !=  "None":
           self.m_graph.addSeries(dcp)
        if xll !=  "None":
           self.m_graph.addSeries(xll)
        if axv !=  "None":
           self.m_graph.addSeries(axv)
        if eqt !=  "None":
           self.m_graph.addSeries(eqt)
        if sbp !=  "None":
           self.m_graph.addSeries(sbp)
        if lmr !=  "None":
           self.m_graph.addSeries(lmr)
        if idn !=  "None":
           self.m_graph.addSeries(idn)
        if vyt !=  "None":
           self.m_graph.addSeries(vyt)
        if ecw !=  "None":
           self.m_graph.addSeries(ecw)
        if iuo !=  "None":
           self.m_graph.addSeries(iuo)
        if nho !=  "None":
           self.m_graph.addSeries(nho)
        if gdi !=  "None":
           self.m_graph.addSeries(gdi)
        if llp !=  "None":
           self.m_graph.addSeries(llp)
        if mqd !=  "None":
           self.m_graph.addSeries(mqd)
        if fzv !=  "None":
           self.m_graph.addSeries(fzv)
        if xmf !=  "None":
           self.m_graph.addSeries(xmf)
        if iok !=  "None":
           self.m_graph.addSeries(iok)
        if exr !=  "None":
           self.m_graph.addSeries(exr)
        if upw !=  "None":
           self.m_graph.addSeries(upw)
        if ita !=  "None":
           self.m_graph.addSeries(ita)
        if bgl !=  "None":
           self.m_graph.addSeries(bgl)
        if mxb !=  "None":
           self.m_graph.addSeries(mxb)
        if ayf !=  "None":
           self.m_graph.addSeries(ayf)
        if xqz !=  "None":
           self.m_graph.addSeries(xqz)
        if tqv !=  "None":
           self.m_graph.addSeries(tqv)
        if fgd !=  "None":
           self.m_graph.addSeries(fgd)
        if dvg !=  "None":
           self.m_graph.addSeries(dvg)
        if dcj !=  "None":
           self.m_graph.addSeries(dcj)
        if dph !=  "None":
           self.m_graph.addSeries(dph)
        if fak !=  "None":
           self.m_graph.addSeries(fak)
        if zsy !=  "None":
           self.m_graph.addSeries(zsy)
        if syt !=  "None":
           self.m_graph.addSeries(syt)
        if rgm !=  "None":
           self.m_graph.addSeries(rgm)
        if bmw !=  "None":
           self.m_graph.addSeries(bmw)
        if kia !=  "None":
           self.m_graph.addSeries(kia)
        if zdx !=  "None":
           self.m_graph.addSeries(zdx)
        if jvq !=  "None":
           self.m_graph.addSeries(jvq)
        if lbs !=  "None":
           self.m_graph.addSeries(lbs)
        if uqh !=  "None":
           self.m_graph.addSeries(uqh)
        if bco !=  "None":
           self.m_graph.addSeries(bco)
        if hoq !=  "None":
           self.m_graph.addSeries(hoq)
        if byh !=  "None":
           self.m_graph.addSeries(byh)
        if myn !=  "None":
           self.m_graph.addSeries(myn)
        if shk !=  "None":
           self.m_graph.addSeries(shk)
        if khq !=  "None":
           self.m_graph.addSeries(khq)
        if ttf !=  "None":
           self.m_graph.addSeries(ttf)
        if scm !=  "None":
           self.m_graph.addSeries(scm)
        if qht !=  "None":
           self.m_graph.addSeries(qht)
        if xae !=  "None":
           self.m_graph.addSeries(xae)
        if mlb !=  "None":
           self.m_graph.addSeries(mlb)
        if xtq !=  "None":
           self.m_graph.addSeries(xtq)
        if cxq !=  "None":
           self.m_graph.addSeries(cxq)
        if agb !=  "None":
           self.m_graph.addSeries(agb)
        if hvo !=  "None":
           self.m_graph.addSeries(hvo)
        if iec !=  "None":
           self.m_graph.addSeries(iec)
        if xmy !=  "None":
           self.m_graph.addSeries(xmy)
        if qbl !=  "None":
           self.m_graph.addSeries(qbl)
        if xtg !=  "None":
           self.m_graph.addSeries(xtg)
        if kaz !=  "None":
           self.m_graph.addSeries(kaz)
        if bzx !=  "None":
           self.m_graph.addSeries(bzx)
        if zsl !=  "None":
           self.m_graph.addSeries(zsl)
        if gtn !=  "None":
           self.m_graph.addSeries(gtn)
        if afp !=  "None":
           self.m_graph.addSeries(afp)
        if hvd !=  "None":
           self.m_graph.addSeries(hvd)
        if uen !=  "None":
           self.m_graph.addSeries(uen)
        if ute !=  "None":
           self.m_graph.addSeries(ute)
        if njv !=  "None":
           self.m_graph.addSeries(njv)
        if lvx !=  "None":
           self.m_graph.addSeries(lvx)
        if zzj !=  "None":
           self.m_graph.addSeries(zzj)
        if exc !=  "None":
           self.m_graph.addSeries(exc)
        if krr !=  "None":
           self.m_graph.addSeries(krr)
        if hpd !=  "None":
           self.m_graph.addSeries(hpd)
        if tee !=  "None":
           self.m_graph.addSeries(tee)
        if utf !=  "None":
           self.m_graph.addSeries(utf)
        if rgz !=  "None":
           self.m_graph.addSeries(rgz)
        if ebc !=  "None":
           self.m_graph.addSeries(ebc)
        if rjh !=  "None":
           self.m_graph.addSeries(rjh)
        if rof !=  "None":
           self.m_graph.addSeries(rof)
        if lum !=  "None":
           self.m_graph.addSeries(lum)
        if uli !=  "None":
           self.m_graph.addSeries(uli)
        if huk !=  "None":
           self.m_graph.addSeries(huk)
        if rum !=  "None":
           self.m_graph.addSeries(rum)
        if sog !=  "None":
           self.m_graph.addSeries(sog)
        if mln !=  "None":
           self.m_graph.addSeries(mln)
        if uok !=  "None":
           self.m_graph.addSeries(uok)
        if mif !=  "None":
           self.m_graph.addSeries(mif)
        if hwb !=  "None":
           self.m_graph.addSeries(hwb)
        if lfn !=  "None":
           self.m_graph.addSeries(lfn)
        if imc !=  "None":
           self.m_graph.addSeries(imc)
        if vqj !=  "None":
           self.m_graph.addSeries(vqj)
        if mgm !=  "None":
           self.m_graph.addSeries(mgm)
        if hbi !=  "None":
           self.m_graph.addSeries(hbi)
        if pmb !=  "None":
           self.m_graph.addSeries(pmb)
        if aqr !=  "None":
           self.m_graph.addSeries(aqr)
        if myd !=  "None":
           self.m_graph.addSeries(myd)
        if dcm !=  "None":
           self.m_graph.addSeries(dcm)
        if xgj !=  "None":
           self.m_graph.addSeries(xgj)
        if hvz !=  "None":
           self.m_graph.addSeries(hvz)
        if tyi !=  "None":
           self.m_graph.addSeries(tyi)
        if yhp !=  "None":
           self.m_graph.addSeries(yhp)
        if pfl !=  "None":
           self.m_graph.addSeries(pfl)
        if qpt !=  "None":
           self.m_graph.addSeries(qpt)
        if lvv !=  "None":
           self.m_graph.addSeries(lvv)
        if hyj !=  "None":
           self.m_graph.addSeries(hyj)
        if vlf !=  "None":
           self.m_graph.addSeries(vlf)
        if uzy !=  "None":
           self.m_graph.addSeries(uzy)
        if son !=  "None":
           self.m_graph.addSeries(son)
        if nze !=  "None":
           self.m_graph.addSeries(nze)
        if tmn !=  "None":
           self.m_graph.addSeries(tmn)
        if zfw !=  "None":
           self.m_graph.addSeries(zfw)
        if sid !=  "None":
           self.m_graph.addSeries(sid)
        if yov !=  "None":
           self.m_graph.addSeries(yov)
        if unq !=  "None":
           self.m_graph.addSeries(unq)
        if fqq !=  "None":
           self.m_graph.addSeries(fqq)
        if woy !=  "None":
           self.m_graph.addSeries(woy)
        if fik !=  "None":
           self.m_graph.addSeries(fik)
        if xbw !=  "None":
           self.m_graph.addSeries(xbw)
        if fwa !=  "None":
           self.m_graph.addSeries(fwa)
        if rqs !=  "None":
           self.m_graph.addSeries(rqs)
        if ehd !=  "None":
           self.m_graph.addSeries(ehd)
        if rza !=  "None":
           self.m_graph.addSeries(rza)
        if ngj !=  "None":
           self.m_graph.addSeries(ngj)
        if pxi !=  "None":
           self.m_graph.addSeries(pxi)
        if moo !=  "None":
           self.m_graph.addSeries(moo)
        if jrt !=  "None":
           self.m_graph.addSeries(jrt)
        if hni !=  "None":
           self.m_graph.addSeries(hni)
        if fth !=  "None":
           self.m_graph.addSeries(fth)
        if jyn !=  "None":
           self.m_graph.addSeries(jyn)
        if vef !=  "None":
           self.m_graph.addSeries(vef)
        if hak !=  "None":
           self.m_graph.addSeries(hak)
        if wlj !=  "None":
           self.m_graph.addSeries(wlj)
        if otv !=  "None":
           self.m_graph.addSeries(otv)
        if nwk !=  "None":
           self.m_graph.addSeries(nwk)
        if jfq !=  "None":
           self.m_graph.addSeries(jfq)
        if pbw !=  "None":
           self.m_graph.addSeries(pbw)
        if ffd !=  "None":
           self.m_graph.addSeries(ffd)
        if trl !=  "None":
           self.m_graph.addSeries(trl)
        if eje !=  "None":
           self.m_graph.addSeries(eje)
        if chj !=  "None":
           self.m_graph.addSeries(chj)
        if nen !=  "None":
           self.m_graph.addSeries(nen)
        if pjs !=  "None":
           self.m_graph.addSeries(pjs)
        if uds !=  "None":
           self.m_graph.addSeries(uds)
        if gaf !=  "None":
           self.m_graph.addSeries(gaf)
        if bsn !=  "None":
           self.m_graph.addSeries(bsn)
        if yhs !=  "None":
           self.m_graph.addSeries(yhs)
        if zvz !=  "None":
           self.m_graph.addSeries(zvz)
        if kqe !=  "None":
           self.m_graph.addSeries(kqe)
        if smb !=  "None":
           self.m_graph.addSeries(smb)
        if ulc !=  "None":
           self.m_graph.addSeries(ulc)
        if hrc !=  "None":
           self.m_graph.addSeries(hrc)
        if rdb !=  "None":
           self.m_graph.addSeries(rdb)
        if ytf !=  "None":
           self.m_graph.addSeries(ytf)
        if fwy !=  "None":
           self.m_graph.addSeries(fwy)
        if jvu !=  "None":
           self.m_graph.addSeries(jvu)
        if tfy !=  "None":
           self.m_graph.addSeries(tfy)
        if sci !=  "None":
           self.m_graph.addSeries(sci)
        if oxq !=  "None":
           self.m_graph.addSeries(oxq)
        if edj !=  "None":
           self.m_graph.addSeries(edj)
        if eyd !=  "None":
           self.m_graph.addSeries(eyd)
        if wik !=  "None":
           self.m_graph.addSeries(wik)
        if avc !=  "None":
           self.m_graph.addSeries(avc)
        if che !=  "None":
           self.m_graph.addSeries(che)
        if qin !=  "None":
           self.m_graph.addSeries(qin)
        if iwu !=  "None":
           self.m_graph.addSeries(iwu)
        if adb !=  "None":
           self.m_graph.addSeries(adb)
        if ymt !=  "None":
           self.m_graph.addSeries(ymt)
        if hxl !=  "None":
           self.m_graph.addSeries(hxl)
        if yot !=  "None":
           self.m_graph.addSeries(yot)
        if dud !=  "None":
           self.m_graph.addSeries(dud)
        if omv !=  "None":
           self.m_graph.addSeries(omv)
        if jus !=  "None":
           self.m_graph.addSeries(jus)
        if qau !=  "None":
           self.m_graph.addSeries(qau)
        if qwi !=  "None":
           self.m_graph.addSeries(qwi)
        if etw !=  "None":
           self.m_graph.addSeries(etw)
        if con !=  "None":
           self.m_graph.addSeries(con)
        if kzn !=  "None":
           self.m_graph.addSeries(kzn)
        if bxc !=  "None":
           self.m_graph.addSeries(bxc)
        if kid !=  "None":
           self.m_graph.addSeries(kid)
        if far !=  "None":
           self.m_graph.addSeries(far)
        if wpl !=  "None":
           self.m_graph.addSeries(wpl)
        if pgl !=  "None":
           self.m_graph.addSeries(pgl)
        if oaz !=  "None":
           self.m_graph.addSeries(oaz)
        if fgj !=  "None":
           self.m_graph.addSeries(fgj)
        if lqk !=  "None":
           self.m_graph.addSeries(lqk)
        if dct !=  "None":
           self.m_graph.addSeries(dct)
        if brl !=  "None":
           self.m_graph.addSeries(brl)
        if yxr !=  "None":
           self.m_graph.addSeries(yxr)
        if tcj !=  "None":
           self.m_graph.addSeries(tcj)
        if wrc !=  "None":
           self.m_graph.addSeries(wrc)
        if tof !=  "None":
           self.m_graph.addSeries(tof)
        if lbz !=  "None":
           self.m_graph.addSeries(lbz)
        if sha !=  "None":
           self.m_graph.addSeries(sha)
        if ghv !=  "None":
           self.m_graph.addSeries(ghv)
        if ljk !=  "None":
           self.m_graph.addSeries(ljk)
        if jxs !=  "None":
           self.m_graph.addSeries(jxs)
        if xfh !=  "None":
           self.m_graph.addSeries(xfh)
        if vrd !=  "None":
           self.m_graph.addSeries(vrd)
        if vej !=  "None":
           self.m_graph.addSeries(vej)
        if nkm !=  "None":
           self.m_graph.addSeries(nkm)
        if jnr !=  "None":
           self.m_graph.addSeries(jnr)
        if qwj !=  "None":
           self.m_graph.addSeries(qwj)
        if dbp !=  "None":
           self.m_graph.addSeries(dbp)
        if orl !=  "None":
           self.m_graph.addSeries(orl)
        if ypw !=  "None":
           self.m_graph.addSeries(ypw)
        if xxd !=  "None":
           self.m_graph.addSeries(xxd)
        if agt !=  "None":
           self.m_graph.addSeries(agt)
        if sdr !=  "None":
           self.m_graph.addSeries(sdr)
        if oen !=  "None":
           self.m_graph.addSeries(oen)
        if snx !=  "None":
           self.m_graph.addSeries(snx)
        if mpp !=  "None":
           self.m_graph.addSeries(mpp)
        if ath !=  "None":
           self.m_graph.addSeries(ath)
        if hyi !=  "None":
           self.m_graph.addSeries(hyi)
        if znb !=  "None":
           self.m_graph.addSeries(znb)
        if otb !=  "None":
           self.m_graph.addSeries(otb)
        if nfu !=  "None":
           self.m_graph.addSeries(nfu)
        if nyt !=  "None":
           self.m_graph.addSeries(nyt)
        if aen !=  "None":
           self.m_graph.addSeries(aen)
        if tme !=  "None":
           self.m_graph.addSeries(tme)
        if icb !=  "None":
           self.m_graph.addSeries(icb)
        if gck !=  "None":
           self.m_graph.addSeries(gck)
        if vpk !=  "None":
           self.m_graph.addSeries(vpk)
        if yub !=  "None":
           self.m_graph.addSeries(yub)
        if vio !=  "None":
           self.m_graph.addSeries(vio)
        if zfk !=  "None":
           self.m_graph.addSeries(zfk)
        if dte !=  "None":
           self.m_graph.addSeries(dte)
        if mrs !=  "None":
           self.m_graph.addSeries(mrs)
        if xxt !=  "None":
           self.m_graph.addSeries(xxt)
        if fxo !=  "None":
           self.m_graph.addSeries(fxo)
        if lrk !=  "None":
           self.m_graph.addSeries(lrk)
        if qri !=  "None":
           self.m_graph.addSeries(qri)
        if hoc !=  "None":
           self.m_graph.addSeries(hoc)
        if qvn !=  "None":
           self.m_graph.addSeries(qvn)
        if ibl !=  "None":
           self.m_graph.addSeries(ibl)
        if biu !=  "None":
           self.m_graph.addSeries(biu)
        if zym !=  "None":
           self.m_graph.addSeries(zym)
        if dyk !=  "None":
           self.m_graph.addSeries(dyk)
        if cmu !=  "None":
           self.m_graph.addSeries(cmu)
        if fix !=  "None":
           self.m_graph.addSeries(fix)
        if nvo !=  "None":
           self.m_graph.addSeries(nvo)
        if dlm !=  "None":
           self.m_graph.addSeries(dlm)
        if zzm !=  "None":
           self.m_graph.addSeries(zzm)
        if iko !=  "None":
           self.m_graph.addSeries(iko)
        if rmq !=  "None":
           self.m_graph.addSeries(rmq)
        if jmc !=  "None":
           self.m_graph.addSeries(jmc)
        if lsq !=  "None":
           self.m_graph.addSeries(lsq)
        if eyq !=  "None":
           self.m_graph.addSeries(eyq)
        if suf !=  "None":
           self.m_graph.addSeries(suf)
        if kqb !=  "None":
           self.m_graph.addSeries(kqb)
        if swg !=  "None":
           self.m_graph.addSeries(swg)
        if ium !=  "None":
           self.m_graph.addSeries(ium)
        if voq !=  "None":
           self.m_graph.addSeries(voq)
        if yzv !=  "None":
           self.m_graph.addSeries(yzv)
        if jbu !=  "None":
           self.m_graph.addSeries(jbu)
        if jcr !=  "None":
           self.m_graph.addSeries(jcr)
        if hym !=  "None":
           self.m_graph.addSeries(hym)
        if cmg !=  "None":
           self.m_graph.addSeries(cmg)
        if evz !=  "None":
           self.m_graph.addSeries(evz)
        if znn !=  "None":
           self.m_graph.addSeries(znn)
        if fre !=  "None":
           self.m_graph.addSeries(fre)
        if klv !=  "None":
           self.m_graph.addSeries(klv)
        if ian !=  "None":
           self.m_graph.addSeries(ian)
        if lsw !=  "None":
           self.m_graph.addSeries(lsw)
        if jod !=  "None":
           self.m_graph.addSeries(jod)
        if kxk !=  "None":
           self.m_graph.addSeries(kxk)
        if swi !=  "None":
           self.m_graph.addSeries(swi)
        if kgb !=  "None":
           self.m_graph.addSeries(kgb)
        if eis !=  "None":
           self.m_graph.addSeries(eis)
        if qnc !=  "None":
           self.m_graph.addSeries(qnc)
        if usy !=  "None":
           self.m_graph.addSeries(usy)
        if cmi !=  "None":
           self.m_graph.addSeries(cmi)
        if mjq !=  "None":
           self.m_graph.addSeries(mjq)
        if uie !=  "None":
           self.m_graph.addSeries(uie)
        if inp !=  "None":
           self.m_graph.addSeries(inp)
        if iuy !=  "None":
           self.m_graph.addSeries(iuy)
        if rnj !=  "None":
           self.m_graph.addSeries(rnj)
        if zzv !=  "None":
           self.m_graph.addSeries(zzv)
        if ulv !=  "None":
           self.m_graph.addSeries(ulv)
        if zqt !=  "None":
           self.m_graph.addSeries(zqt)
        if suo !=  "None":
           self.m_graph.addSeries(suo)
        if zeq !=  "None":
           self.m_graph.addSeries(zeq)
        if huv !=  "None":
           self.m_graph.addSeries(huv)
        if ldq !=  "None":
           self.m_graph.addSeries(ldq)
        if abm !=  "None":
           self.m_graph.addSeries(abm)
        if ojp !=  "None":
           self.m_graph.addSeries(ojp)
        if myb !=  "None":
           self.m_graph.addSeries(myb)
        if uyj !=  "None":
           self.m_graph.addSeries(uyj)
        if sbv !=  "None":
           self.m_graph.addSeries(sbv)
        if yif !=  "None":
           self.m_graph.addSeries(yif)
        if fvi !=  "None":
           self.m_graph.addSeries(fvi)
        if rer !=  "None":
           self.m_graph.addSeries(rer)
        if mem !=  "None":
           self.m_graph.addSeries(mem)
        if dig !=  "None":
           self.m_graph.addSeries(dig)
        if zew !=  "None":
           self.m_graph.addSeries(zew)
        if sgk !=  "None":
           self.m_graph.addSeries(sgk)
        if erv !=  "None":
           self.m_graph.addSeries(erv)
        if bxu !=  "None":
           self.m_graph.addSeries(bxu)
        if pns !=  "None":
           self.m_graph.addSeries(pns)
        if ioo !=  "None":
           self.m_graph.addSeries(ioo)
        if jdo !=  "None":
           self.m_graph.addSeries(jdo)
        if aev !=  "None":
           self.m_graph.addSeries(aev)
        if fxh !=  "None":
           self.m_graph.addSeries(fxh)
        if wxv !=  "None":
           self.m_graph.addSeries(wxv)
        if cnd !=  "None":
           self.m_graph.addSeries(cnd)
        if upg !=  "None":
           self.m_graph.addSeries(upg)
        if vux !=  "None":
           self.m_graph.addSeries(vux)
        if ken !=  "None":
           self.m_graph.addSeries(ken)
        if wkw !=  "None":
           self.m_graph.addSeries(wkw)
        if ivm !=  "None":
           self.m_graph.addSeries(ivm)
        if oqm !=  "None":
           self.m_graph.addSeries(oqm)
        if qvx !=  "None":
           self.m_graph.addSeries(qvx)
        if ncx !=  "None":
           self.m_graph.addSeries(ncx)
        if pax !=  "None":
           self.m_graph.addSeries(pax)
        if gkx !=  "None":
           self.m_graph.addSeries(gkx)
        if vrh !=  "None":
           self.m_graph.addSeries(vrh)
        if vsi !=  "None":
           self.m_graph.addSeries(vsi)
        if wnn !=  "None":
           self.m_graph.addSeries(wnn)
        if irs !=  "None":
           self.m_graph.addSeries(irs)
        if igd !=  "None":
           self.m_graph.addSeries(igd)
        if gwf !=  "None":
           self.m_graph.addSeries(gwf)
        if ldo !=  "None":
           self.m_graph.addSeries(ldo)
        if rfx !=  "None":
           self.m_graph.addSeries(rfx)
        if unv !=  "None":
           self.m_graph.addSeries(unv)
        if heg !=  "None":
           self.m_graph.addSeries(heg)
        if xtk !=  "None":
           self.m_graph.addSeries(xtk)
        if axk !=  "None":
           self.m_graph.addSeries(axk)
        if rbz !=  "None":
           self.m_graph.addSeries(rbz)
        if gjd !=  "None":
           self.m_graph.addSeries(gjd)
        if xfj !=  "None":
           self.m_graph.addSeries(xfj)
        if opk !=  "None":
           self.m_graph.addSeries(opk)
        if pwp !=  "None":
           self.m_graph.addSeries(pwp)
        if czh !=  "None":
           self.m_graph.addSeries(czh)
        if nhq !=  "None":
           self.m_graph.addSeries(nhq)
        if wxf !=  "None":
           self.m_graph.addSeries(wxf)
        if wrw !=  "None":
           self.m_graph.addSeries(wrw)
        if nnz !=  "None":
           self.m_graph.addSeries(nnz)
        if riw !=  "None":
           self.m_graph.addSeries(riw)
        if aui !=  "None":
           self.m_graph.addSeries(aui)
        if lgx !=  "None":
           self.m_graph.addSeries(lgx)
        if tue !=  "None":
           self.m_graph.addSeries(tue)
        if yly !=  "None":
           self.m_graph.addSeries(yly)
        if uwj !=  "None":
           self.m_graph.addSeries(uwj)
        if cbv !=  "None":
           self.m_graph.addSeries(cbv)
        if aea !=  "None":
           self.m_graph.addSeries(aea)
        if fav !=  "None":
           self.m_graph.addSeries(fav)
        if hku !=  "None":
           self.m_graph.addSeries(hku)
        if pvc !=  "None":
           self.m_graph.addSeries(pvc)
        if wei !=  "None":
           self.m_graph.addSeries(wei)
        if gkz !=  "None":
           self.m_graph.addSeries(gkz)
        if pgv !=  "None":
           self.m_graph.addSeries(pgv)
        if yuc !=  "None":
           self.m_graph.addSeries(yuc)
        if iwh !=  "None":
           self.m_graph.addSeries(iwh)
        if xqo !=  "None":
           self.m_graph.addSeries(xqo)
        if ota !=  "None":
           self.m_graph.addSeries(ota)
        if qew !=  "None":
           self.m_graph.addSeries(qew)
        if dqg !=  "None":
           self.m_graph.addSeries(dqg)
        if bfg !=  "None":
           self.m_graph.addSeries(bfg)
        if ynz !=  "None":
           self.m_graph.addSeries(ynz)
        if exw !=  "None":
           self.m_graph.addSeries(exw)
        if sud !=  "None":
           self.m_graph.addSeries(sud)
        if vhj !=  "None":
           self.m_graph.addSeries(vhj)
        if ges !=  "None":
           self.m_graph.addSeries(ges)
        if amw !=  "None":
           self.m_graph.addSeries(amw)
        if iqt !=  "None":
           self.m_graph.addSeries(iqt)
        if kol !=  "None":
           self.m_graph.addSeries(kol)
        if hfa !=  "None":
           self.m_graph.addSeries(hfa)
        if fvu !=  "None":
           self.m_graph.addSeries(fvu)
        if qsi !=  "None":
           self.m_graph.addSeries(qsi)
        if qix !=  "None":
           self.m_graph.addSeries(qix)
        if tcr !=  "None":
           self.m_graph.addSeries(tcr)
        if ctk !=  "None":
           self.m_graph.addSeries(ctk)
        if qqg !=  "None":
           self.m_graph.addSeries(qqg)
        if wze !=  "None":
           self.m_graph.addSeries(wze)
        if hod !=  "None":
           self.m_graph.addSeries(hod)
        if hzr !=  "None":
           self.m_graph.addSeries(hzr)
        if nlh !=  "None":
           self.m_graph.addSeries(nlh)
        if qso !=  "None":
           self.m_graph.addSeries(qso)
        if pja !=  "None":
           self.m_graph.addSeries(pja)
        if oqe !=  "None":
           self.m_graph.addSeries(oqe)
        if rst !=  "None":
           self.m_graph.addSeries(rst)
        if fzh !=  "None":
           self.m_graph.addSeries(fzh)
        if awz !=  "None":
           self.m_graph.addSeries(awz)
        if atn !=  "None":
           self.m_graph.addSeries(atn)
        if fwb !=  "None":
           self.m_graph.addSeries(fwb)
        if txd !=  "None":
           self.m_graph.addSeries(txd)
        if ybg !=  "None":
           self.m_graph.addSeries(ybg)
        if tpe !=  "None":
           self.m_graph.addSeries(tpe)
        if how !=  "None":
           self.m_graph.addSeries(how)
        if nuu !=  "None":
           self.m_graph.addSeries(nuu)
        if wam !=  "None":
           self.m_graph.addSeries(wam)
        if oiw !=  "None":
           self.m_graph.addSeries(oiw)
        if mrc !=  "None":
           self.m_graph.addSeries(mrc)
        if wjo !=  "None":
           self.m_graph.addSeries(wjo)
        if yfw !=  "None":
           self.m_graph.addSeries(yfw)
        if nxm !=  "None":
           self.m_graph.addSeries(nxm)
        if rqn !=  "None":
           self.m_graph.addSeries(rqn)
        if aju !=  "None":
           self.m_graph.addSeries(aju)
        if eyh !=  "None":
           self.m_graph.addSeries(eyh)
        if xsj !=  "None":
           self.m_graph.addSeries(xsj)
        if zyp !=  "None":
           self.m_graph.addSeries(zyp)
        if hee !=  "None":
           self.m_graph.addSeries(hee)
        if coj !=  "None":
           self.m_graph.addSeries(coj)
        if xzj !=  "None":
           self.m_graph.addSeries(xzj)
        if uzf !=  "None":
           self.m_graph.addSeries(uzf)
        if sbb !=  "None":
           self.m_graph.addSeries(sbb)
        if wah !=  "None":
           self.m_graph.addSeries(wah)
        if ldz !=  "None":
           self.m_graph.addSeries(ldz)
        if emu !=  "None":
           self.m_graph.addSeries(emu)
        if umg !=  "None":
           self.m_graph.addSeries(umg)
        if fpi !=  "None":
           self.m_graph.addSeries(fpi)
        if zpz !=  "None":
           self.m_graph.addSeries(zpz)
        if mzh !=  "None":
           self.m_graph.addSeries(mzh)
        if hqu !=  "None":
           self.m_graph.addSeries(hqu)
        if eoz !=  "None":
           self.m_graph.addSeries(eoz)
        if zxg !=  "None":
           self.m_graph.addSeries(zxg)
        if ncc !=  "None":
           self.m_graph.addSeries(ncc)
        if kbs !=  "None":
           self.m_graph.addSeries(kbs)
        if usi !=  "None":
           self.m_graph.addSeries(usi)
        if hzi !=  "None":
           self.m_graph.addSeries(hzi)
        if rbh !=  "None":
           self.m_graph.addSeries(rbh)
        if kun !=  "None":
           self.m_graph.addSeries(kun)
        if aoi !=  "None":
           self.m_graph.addSeries(aoi)
        if qwm !=  "None":
           self.m_graph.addSeries(qwm)
        if uyc !=  "None":
           self.m_graph.addSeries(uyc)
        if duh !=  "None":
           self.m_graph.addSeries(duh)
        if eyn !=  "None":
           self.m_graph.addSeries(eyn)
        if gdh !=  "None":
           self.m_graph.addSeries(gdh)
        if lca !=  "None":
           self.m_graph.addSeries(lca)
        if ubu !=  "None":
           self.m_graph.addSeries(ubu)
        if zsz !=  "None":
           self.m_graph.addSeries(zsz)
        if dns !=  "None":
           self.m_graph.addSeries(dns)
        if xxn !=  "None":
           self.m_graph.addSeries(xxn)
        if zyg !=  "None":
           self.m_graph.addSeries(zyg)
        if cec !=  "None":
           self.m_graph.addSeries(cec)
        if bla !=  "None":
           self.m_graph.addSeries(bla)
        if unp !=  "None":
           self.m_graph.addSeries(unp)
        if rjg !=  "None":
           self.m_graph.addSeries(rjg)
        if gti !=  "None":
           self.m_graph.addSeries(gti)
        if qfc !=  "None":
           self.m_graph.addSeries(qfc)
        if nrj !=  "None":
           self.m_graph.addSeries(nrj)
        if hxf !=  "None":
           self.m_graph.addSeries(hxf)
        if ayh !=  "None":
           self.m_graph.addSeries(ayh)
        if hkg !=  "None":
           self.m_graph.addSeries(hkg)
        if akd !=  "None":
           self.m_graph.addSeries(akd)
        if nfw !=  "None":
           self.m_graph.addSeries(nfw)
        if ouc !=  "None":
           self.m_graph.addSeries(ouc)
        if sul !=  "None":
           self.m_graph.addSeries(sul)
        if isf !=  "None":
           self.m_graph.addSeries(isf)
        if biq !=  "None":
           self.m_graph.addSeries(biq)
        if zun !=  "None":
           self.m_graph.addSeries(zun)
        if khc !=  "None":
           self.m_graph.addSeries(khc)
        if xpj !=  "None":
           self.m_graph.addSeries(xpj)
        if grn !=  "None":
           self.m_graph.addSeries(grn)
        if hut !=  "None":
           self.m_graph.addSeries(hut)
        if bzo !=  "None":
           self.m_graph.addSeries(bzo)
        if zzl !=  "None":
           self.m_graph.addSeries(zzl)
        if wpu !=  "None":
           self.m_graph.addSeries(wpu)
        if ihi !=  "None":
           self.m_graph.addSeries(ihi)
        if syo !=  "None":
           self.m_graph.addSeries(syo)
        if rsw !=  "None":
           self.m_graph.addSeries(rsw)
        if ivn !=  "None":
           self.m_graph.addSeries(ivn)
        if jcy !=  "None":
           self.m_graph.addSeries(jcy)
        if ivi !=  "None":
           self.m_graph.addSeries(ivi)
        if biy !=  "None":
           self.m_graph.addSeries(biy)
        if jhc !=  "None":
           self.m_graph.addSeries(jhc)
        if izz !=  "None":
           self.m_graph.addSeries(izz)
        if vlx !=  "None":
           self.m_graph.addSeries(vlx)
        if lyr !=  "None":
           self.m_graph.addSeries(lyr)
        if kmy !=  "None":
           self.m_graph.addSeries(kmy)
        if dsl !=  "None":
           self.m_graph.addSeries(dsl)
        if ptb !=  "None":
           self.m_graph.addSeries(ptb)
        if evn !=  "None":
           self.m_graph.addSeries(evn)
        if ciw !=  "None":
           self.m_graph.addSeries(ciw)
        if kht !=  "None":
           self.m_graph.addSeries(kht)
        if lmb !=  "None":
           self.m_graph.addSeries(lmb)
        if rpp !=  "None":
           self.m_graph.addSeries(rpp)
        if uln !=  "None":
           self.m_graph.addSeries(uln)
        if yha !=  "None":
           self.m_graph.addSeries(yha)
        if dhq !=  "None":
           self.m_graph.addSeries(dhq)
        if tkk !=  "None":
           self.m_graph.addSeries(tkk)
        if ayp !=  "None":
           self.m_graph.addSeries(ayp)
        if ija !=  "None":
           self.m_graph.addSeries(ija)
        if rnd !=  "None":
           self.m_graph.addSeries(rnd)
        if ztc !=  "None":
           self.m_graph.addSeries(ztc)
        if fxl !=  "None":
           self.m_graph.addSeries(fxl)
        if sly !=  "None":
           self.m_graph.addSeries(sly)
        if rig !=  "None":
           self.m_graph.addSeries(rig)
        if xdh !=  "None":
           self.m_graph.addSeries(xdh)
        if xnz !=  "None":
           self.m_graph.addSeries(xnz)
        if ufa !=  "None":
           self.m_graph.addSeries(ufa)
        if ehv !=  "None":
           self.m_graph.addSeries(ehv)
        if zkv !=  "None":
           self.m_graph.addSeries(zkv)
        if jpm !=  "None":
           self.m_graph.addSeries(jpm)
        if jyb !=  "None":
           self.m_graph.addSeries(jyb)
        if jyu !=  "None":
           self.m_graph.addSeries(jyu)
        if ukn !=  "None":
           self.m_graph.addSeries(ukn)
        if qeh !=  "None":
           self.m_graph.addSeries(qeh)
        if yal !=  "None":
           self.m_graph.addSeries(yal)
        if mlg !=  "None":
           self.m_graph.addSeries(mlg)
        if yup !=  "None":
           self.m_graph.addSeries(yup)
        if puk !=  "None":
           self.m_graph.addSeries(puk)
        if cof !=  "None":
           self.m_graph.addSeries(cof)
        if bvl !=  "None":
           self.m_graph.addSeries(bvl)
        if gjv !=  "None":
           self.m_graph.addSeries(gjv)
        if stg !=  "None":
           self.m_graph.addSeries(stg)
        if gjk !=  "None":
           self.m_graph.addSeries(gjk)
        if ofr !=  "None":
           self.m_graph.addSeries(ofr)
        if utn !=  "None":
           self.m_graph.addSeries(utn)
        if sis !=  "None":
           self.m_graph.addSeries(sis)
        if yjo !=  "None":
           self.m_graph.addSeries(yjo)
        if ewj !=  "None":
           self.m_graph.addSeries(ewj)
        if pdb !=  "None":
           self.m_graph.addSeries(pdb)
        if lac !=  "None":
           self.m_graph.addSeries(lac)
        if ajp !=  "None":
           self.m_graph.addSeries(ajp)
        if esr !=  "None":
           self.m_graph.addSeries(esr)
        if ovc !=  "None":
           self.m_graph.addSeries(ovc)
        if bcv !=  "None":
           self.m_graph.addSeries(bcv)
        if nqx !=  "None":
           self.m_graph.addSeries(nqx)
        if znq !=  "None":
           self.m_graph.addSeries(znq)
        if utk !=  "None":
           self.m_graph.addSeries(utk)
        if jmz !=  "None":
           self.m_graph.addSeries(jmz)
        if xwg !=  "None":
           self.m_graph.addSeries(xwg)
        if yfp !=  "None":
           self.m_graph.addSeries(yfp)
        if wkn !=  "None":
           self.m_graph.addSeries(wkn)
        if prm !=  "None":
           self.m_graph.addSeries(prm)
        if elr !=  "None":
           self.m_graph.addSeries(elr)
        if ile !=  "None":
           self.m_graph.addSeries(ile)
        if xpy !=  "None":
           self.m_graph.addSeries(xpy)
        if tss !=  "None":
           self.m_graph.addSeries(tss)
        if gei !=  "None":
           self.m_graph.addSeries(gei)
        if jfy !=  "None":
           self.m_graph.addSeries(jfy)
        if qzl !=  "None":
           self.m_graph.addSeries(qzl)
        if siv !=  "None":
           self.m_graph.addSeries(siv)
        if kyb !=  "None":
           self.m_graph.addSeries(kyb)
        if gil !=  "None":
           self.m_graph.addSeries(gil)
        if kqv !=  "None":
           self.m_graph.addSeries(kqv)
        if gjq !=  "None":
           self.m_graph.addSeries(gjq)
        if vbj !=  "None":
           self.m_graph.addSeries(vbj)
        if gtl !=  "None":
           self.m_graph.addSeries(gtl)
        if cbk !=  "None":
           self.m_graph.addSeries(cbk)
        if ehw !=  "None":
           self.m_graph.addSeries(ehw)
        if eyf !=  "None":
           self.m_graph.addSeries(eyf)
        if fce !=  "None":
           self.m_graph.addSeries(fce)
        if xsu !=  "None":
           self.m_graph.addSeries(xsu)
        if wzs !=  "None":
           self.m_graph.addSeries(wzs)
        if wbn !=  "None":
           self.m_graph.addSeries(wbn)
        if awa !=  "None":
           self.m_graph.addSeries(awa)
        if tze !=  "None":
           self.m_graph.addSeries(tze)
        if zvc !=  "None":
           self.m_graph.addSeries(zvc)
        if fnc !=  "None":
           self.m_graph.addSeries(fnc)
        if rda !=  "None":
           self.m_graph.addSeries(rda)
        if tqe !=  "None":
           self.m_graph.addSeries(tqe)
        if hft !=  "None":
           self.m_graph.addSeries(hft)
        if ctt !=  "None":
           self.m_graph.addSeries(ctt)
        if ufz !=  "None":
           self.m_graph.addSeries(ufz)
        if hjd !=  "None":
           self.m_graph.addSeries(hjd)
        if gsn !=  "None":
           self.m_graph.addSeries(gsn)
        if sgd !=  "None":
           self.m_graph.addSeries(sgd)
        if dji !=  "None":
           self.m_graph.addSeries(dji)
        if wmx !=  "None":
           self.m_graph.addSeries(wmx)
        if qds !=  "None":
           self.m_graph.addSeries(qds)
        if oiv !=  "None":
           self.m_graph.addSeries(oiv)
        if row !=  "None":
           self.m_graph.addSeries(row)
        if mhr !=  "None":
           self.m_graph.addSeries(mhr)
        if jql !=  "None":
           self.m_graph.addSeries(jql)
        if noe !=  "None":
           self.m_graph.addSeries(noe)
        if ohk !=  "None":
           self.m_graph.addSeries(ohk)
        if mdd !=  "None":
           self.m_graph.addSeries(mdd)
        if ocr !=  "None":
           self.m_graph.addSeries(ocr)
        if ltf !=  "None":
           self.m_graph.addSeries(ltf)
        if qrm !=  "None":
           self.m_graph.addSeries(qrm)
        if hou !=  "None":
           self.m_graph.addSeries(hou)
        if tli !=  "None":
           self.m_graph.addSeries(tli)
        if kuh !=  "None":
           self.m_graph.addSeries(kuh)
        if bnn !=  "None":
           self.m_graph.addSeries(bnn)
        if qzm !=  "None":
           self.m_graph.addSeries(qzm)
        if nvz !=  "None":
           self.m_graph.addSeries(nvz)
        if nug !=  "None":
           self.m_graph.addSeries(nug)
        if klc !=  "None":
           self.m_graph.addSeries(klc)
        if hwq !=  "None":
           self.m_graph.addSeries(hwq)
        if xmt !=  "None":
           self.m_graph.addSeries(xmt)
        if ozi !=  "None":
           self.m_graph.addSeries(ozi)
        if fog !=  "None":
           self.m_graph.addSeries(fog)
        if dcq !=  "None":
           self.m_graph.addSeries(dcq)
        if abq !=  "None":
           self.m_graph.addSeries(abq)
        if dio !=  "None":
           self.m_graph.addSeries(dio)
        if pxv !=  "None":
           self.m_graph.addSeries(pxv)
        if ani !=  "None":
           self.m_graph.addSeries(ani)
        if qwr !=  "None":
           self.m_graph.addSeries(qwr)
        if uyu !=  "None":
           self.m_graph.addSeries(uyu)
        if alv !=  "None":
           self.m_graph.addSeries(alv)
        if sce !=  "None":
           self.m_graph.addSeries(sce)
        if onu !=  "None":
           self.m_graph.addSeries(onu)
        if zkd !=  "None":
           self.m_graph.addSeries(zkd)
        if hfc !=  "None":
           self.m_graph.addSeries(hfc)
        if mcc !=  "None":
           self.m_graph.addSeries(mcc)
        if dne !=  "None":
           self.m_graph.addSeries(dne)
        if oak !=  "None":
           self.m_graph.addSeries(oak)
        if uuz !=  "None":
           self.m_graph.addSeries(uuz)
        if deb !=  "None":
           self.m_graph.addSeries(deb)
        if rod !=  "None":
           self.m_graph.addSeries(rod)
        if mzf !=  "None":
           self.m_graph.addSeries(mzf)
        if jzb !=  "None":
           self.m_graph.addSeries(jzb)
        if zvh !=  "None":
           self.m_graph.addSeries(zvh)
        if nzu !=  "None":
           self.m_graph.addSeries(nzu)
        if nzs !=  "None":
           self.m_graph.addSeries(nzs)
        if aza !=  "None":
           self.m_graph.addSeries(aza)
        if gch !=  "None":
           self.m_graph.addSeries(gch)
        if zuh !=  "None":
           self.m_graph.addSeries(zuh)
        if whs !=  "None":
           self.m_graph.addSeries(whs)
        if ugu !=  "None":
           self.m_graph.addSeries(ugu)
        if kuv !=  "None":
           self.m_graph.addSeries(kuv)
        if lqv !=  "None":
           self.m_graph.addSeries(lqv)
        if let !=  "None":
           self.m_graph.addSeries(let)
        if hvw !=  "None":
           self.m_graph.addSeries(hvw)
        if bov !=  "None":
           self.m_graph.addSeries(bov)
        if yna !=  "None":
           self.m_graph.addSeries(yna)
        if xzn !=  "None":
           self.m_graph.addSeries(xzn)
        if pvm !=  "None":
           self.m_graph.addSeries(pvm)
        if jdv !=  "None":
           self.m_graph.addSeries(jdv)
        if sls !=  "None":
           self.m_graph.addSeries(sls)
        if sbr !=  "None":
           self.m_graph.addSeries(sbr)
        if nnd !=  "None":
           self.m_graph.addSeries(nnd)
        if vtb !=  "None":
           self.m_graph.addSeries(vtb)
        if fbk !=  "None":
           self.m_graph.addSeries(fbk)
        if csj !=  "None":
           self.m_graph.addSeries(csj)
        if hqc !=  "None":
           self.m_graph.addSeries(hqc)
        if mrg !=  "None":
           self.m_graph.addSeries(mrg)
        if ozk !=  "None":
           self.m_graph.addSeries(ozk)
        if ctx !=  "None":
           self.m_graph.addSeries(ctx)
        if nvj !=  "None":
           self.m_graph.addSeries(nvj)
        if lrj !=  "None":
           self.m_graph.addSeries(lrj)
        if edx !=  "None":
           self.m_graph.addSeries(edx)
        if lyd !=  "None":
           self.m_graph.addSeries(lyd)
        if bqe !=  "None":
           self.m_graph.addSeries(bqe)
        if laj !=  "None":
           self.m_graph.addSeries(laj)
        if qlo !=  "None":
           self.m_graph.addSeries(qlo)
        if xfd !=  "None":
           self.m_graph.addSeries(xfd)
        if mkb !=  "None":
           self.m_graph.addSeries(mkb)
        if buw !=  "None":
           self.m_graph.addSeries(buw)
        if bgd !=  "None":
           self.m_graph.addSeries(bgd)
        if lmc !=  "None":
           self.m_graph.addSeries(lmc)
        if gll !=  "None":
           self.m_graph.addSeries(gll)
        if ywr !=  "None":
           self.m_graph.addSeries(ywr)
        if uei !=  "None":
           self.m_graph.addSeries(uei)
        if bvk !=  "None":
           self.m_graph.addSeries(bvk)
        if iyb !=  "None":
           self.m_graph.addSeries(iyb)
        if urk !=  "None":
           self.m_graph.addSeries(urk)
        if pmh !=  "None":
           self.m_graph.addSeries(pmh)
        if nzw !=  "None":
           self.m_graph.addSeries(nzw)
        if bmz !=  "None":
           self.m_graph.addSeries(bmz)
        if cmf !=  "None":
           self.m_graph.addSeries(cmf)
        if hzl !=  "None":
           self.m_graph.addSeries(hzl)
        if dr !=  "None":
           self.m_graph.addSeries(dr)
        if tvq !=  "None":
           self.m_graph.addSeries(tvq)
        if csd !=  "None":
           self.m_graph.addSeries(csd)
        if xns !=  "None":
           self.m_graph.addSeries(xns)
        if inq !=  "None":
           self.m_graph.addSeries(inq)
        if xzc !=  "None":
           self.m_graph.addSeries(xzc)
        if nmo !=  "None":
           self.m_graph.addSeries(nmo)
        if pql !=  "None":
           self.m_graph.addSeries(pql)
        if ufl !=  "None":
           self.m_graph.addSeries(ufl)
        if nja !=  "None":
           self.m_graph.addSeries(nja)
        if bya !=  "None":
           self.m_graph.addSeries(bya)
        if cuj !=  "None":
           self.m_graph.addSeries(cuj)
        if ikp !=  "None":
           self.m_graph.addSeries(ikp)
        if zzh !=  "None":
           self.m_graph.addSeries(zzh)
        if tbc !=  "None":
           self.m_graph.addSeries(tbc)
        if jqz !=  "None":
           self.m_graph.addSeries(jqz)
        if hlu !=  "None":
           self.m_graph.addSeries(hlu)
        if mhc !=  "None":
           self.m_graph.addSeries(mhc)
        if bgv !=  "None":
           self.m_graph.addSeries(bgv)
        if xcc !=  "None":
           self.m_graph.addSeries(xcc)
        if sft !=  "None":
           self.m_graph.addSeries(sft)
        if hlm !=  "None":
           self.m_graph.addSeries(hlm)
        if gxj !=  "None":
           self.m_graph.addSeries(gxj)
        if sqx !=  "None":
           self.m_graph.addSeries(sqx)
        if veq !=  "None":
           self.m_graph.addSeries(veq)
        if bos !=  "None":
           self.m_graph.addSeries(bos)
        if ddq !=  "None":
           self.m_graph.addSeries(ddq)
        if cuu !=  "None":
           self.m_graph.addSeries(cuu)
        if jbg !=  "None":
           self.m_graph.addSeries(jbg)
        if fkl !=  "None":
           self.m_graph.addSeries(fkl)
        if jhh !=  "None":
           self.m_graph.addSeries(jhh)
        if dov !=  "None":
           self.m_graph.addSeries(dov)
        if koq !=  "None":
           self.m_graph.addSeries(koq)
        if yze !=  "None":
           self.m_graph.addSeries(yze)
        if xmi !=  "None":
           self.m_graph.addSeries(xmi)
        if cuf !=  "None":
           self.m_graph.addSeries(cuf)
        if yfy !=  "None":
           self.m_graph.addSeries(yfy)
        if lwb !=  "None":
           self.m_graph.addSeries(lwb)
        if pte !=  "None":
           self.m_graph.addSeries(pte)
        if rks !=  "None":
           self.m_graph.addSeries(rks)
        if omz !=  "None":
           self.m_graph.addSeries(omz)
        if rws !=  "None":
           self.m_graph.addSeries(rws)
        if bjg !=  "None":
           self.m_graph.addSeries(bjg)
        if uwl !=  "None":
           self.m_graph.addSeries(uwl)
        if zdm !=  "None":
           self.m_graph.addSeries(zdm)
        if xtm !=  "None":
           self.m_graph.addSeries(xtm)
        if asn !=  "None":
           self.m_graph.addSeries(asn)
        if rzf !=  "None":
           self.m_graph.addSeries(rzf)
        if mzo !=  "None":
           self.m_graph.addSeries(mzo)
        if rqq !=  "None":
           self.m_graph.addSeries(rqq)
        if nbr !=  "None":
           self.m_graph.addSeries(nbr)
        if qxm !=  "None":
           self.m_graph.addSeries(qxm)
        if kdj !=  "None":
           self.m_graph.addSeries(kdj)
        if hrk !=  "None":
           self.m_graph.addSeries(hrk)
        if uhu !=  "None":
           self.m_graph.addSeries(uhu)
        if yge !=  "None":
           self.m_graph.addSeries(yge)
        if ovy !=  "None":
           self.m_graph.addSeries(ovy)
        if mlr !=  "None":
           self.m_graph.addSeries(mlr)
        if jjx !=  "None":
           self.m_graph.addSeries(jjx)
        if qol !=  "None":
           self.m_graph.addSeries(qol)
        if pgy !=  "None":
           self.m_graph.addSeries(pgy)
        if nej !=  "None":
           self.m_graph.addSeries(nej)
        if hbq !=  "None":
           self.m_graph.addSeries(hbq)
        if odw !=  "None":
           self.m_graph.addSeries(odw)
        if baw !=  "None":
           self.m_graph.addSeries(baw)
        if gzw !=  "None":
           self.m_graph.addSeries(gzw)
        if yaj !=  "None":
           self.m_graph.addSeries(yaj)
        if xja !=  "None":
           self.m_graph.addSeries(xja)
        if qni !=  "None":
           self.m_graph.addSeries(qni)
        if dbl !=  "None":
           self.m_graph.addSeries(dbl)
        if clr !=  "None":
           self.m_graph.addSeries(clr)
        if tyh !=  "None":
           self.m_graph.addSeries(tyh)
        if bah !=  "None":
           self.m_graph.addSeries(bah)
        if elg !=  "None":
           self.m_graph.addSeries(elg)
        if kda !=  "None":
           self.m_graph.addSeries(kda)
        if ync !=  "None":
           self.m_graph.addSeries(ync)
        if mzd !=  "None":
           self.m_graph.addSeries(mzd)
        if iku !=  "None":
           self.m_graph.addSeries(iku)
        if tau !=  "None":
           self.m_graph.addSeries(tau)
        if pzx !=  "None":
           self.m_graph.addSeries(pzx)
        if fsy !=  "None":
           self.m_graph.addSeries(fsy)
        if qmq !=  "None":
           self.m_graph.addSeries(qmq)
        if ugi !=  "None":
           self.m_graph.addSeries(ugi)
        if ods !=  "None":
           self.m_graph.addSeries(ods)
        if fjk !=  "None":
           self.m_graph.addSeries(fjk)
        if zfv !=  "None":
           self.m_graph.addSeries(zfv)
        if ecp !=  "None":
           self.m_graph.addSeries(ecp)
        if ukb !=  "None":
           self.m_graph.addSeries(ukb)
        if rhn !=  "None":
           self.m_graph.addSeries(rhn)
        if wgg !=  "None":
           self.m_graph.addSeries(wgg)
        if vbo !=  "None":
           self.m_graph.addSeries(vbo)
        if zws !=  "None":
           self.m_graph.addSeries(zws)
        if hpc !=  "None":
           self.m_graph.addSeries(hpc)
        if qdb !=  "None":
           self.m_graph.addSeries(qdb)
        if oaw !=  "None":
           self.m_graph.addSeries(oaw)
        if lcq !=  "None":
           self.m_graph.addSeries(lcq)
        if grc !=  "None":
           self.m_graph.addSeries(grc)
        if vkb !=  "None":
           self.m_graph.addSeries(vkb)
        if oyz !=  "None":
           self.m_graph.addSeries(oyz)
        if bzk !=  "None":
           self.m_graph.addSeries(bzk)
        if lyh !=  "None":
           self.m_graph.addSeries(lyh)
        if dfp !=  "None":
           self.m_graph.addSeries(dfp)
        if wru !=  "None":
           self.m_graph.addSeries(wru)
        if frg !=  "None":
           self.m_graph.addSeries(frg)
        if izu !=  "None":
           self.m_graph.addSeries(izu)
        if tqq !=  "None":
           self.m_graph.addSeries(tqq)
        if xlh !=  "None":
           self.m_graph.addSeries(xlh)
        if mes !=  "None":
           self.m_graph.addSeries(mes)
        if svf !=  "None":
           self.m_graph.addSeries(svf)
        if ipe !=  "None":
           self.m_graph.addSeries(ipe)
        if vyz !=  "None":
           self.m_graph.addSeries(vyz)
        if hgm !=  "None":
           self.m_graph.addSeries(hgm)
        if wyc !=  "None":
           self.m_graph.addSeries(wyc)
        if iwe !=  "None":
           self.m_graph.addSeries(iwe)
        if gow !=  "None":
           self.m_graph.addSeries(gow)
        if cem !=  "None":
           self.m_graph.addSeries(cem)
        if euv !=  "None":
           self.m_graph.addSeries(euv)
        if pmu !=  "None":
           self.m_graph.addSeries(pmu)
        if qfk !=  "None":
           self.m_graph.addSeries(qfk)
        if qmp !=  "None":
           self.m_graph.addSeries(qmp)
        if zpm !=  "None":
           self.m_graph.addSeries(zpm)
        if ily !=  "None":
           self.m_graph.addSeries(ily)
        if pbc !=  "None":
           self.m_graph.addSeries(pbc)
        if bhc !=  "None":
           self.m_graph.addSeries(bhc)
        if gwa !=  "None":
           self.m_graph.addSeries(gwa)
        if gbq !=  "None":
           self.m_graph.addSeries(gbq)
        if anq !=  "None":
           self.m_graph.addSeries(anq)
        if msq !=  "None":
           self.m_graph.addSeries(msq)
        if nkw !=  "None":
           self.m_graph.addSeries(nkw)
        if xfc !=  "None":
           self.m_graph.addSeries(xfc)
        if tmu !=  "None":
           self.m_graph.addSeries(tmu)
        if nqu !=  "None":
           self.m_graph.addSeries(nqu)
        if fkg !=  "None":
           self.m_graph.addSeries(fkg)
        if muv !=  "None":
           self.m_graph.addSeries(muv)
        if uja !=  "None":
           self.m_graph.addSeries(uja)
        if fjy !=  "None":
           self.m_graph.addSeries(fjy)
        if ppe !=  "None":
           self.m_graph.addSeries(ppe)
        if fpm !=  "None":
           self.m_graph.addSeries(fpm)
        if qob !=  "None":
           self.m_graph.addSeries(qob)
        if acw !=  "None":
           self.m_graph.addSeries(acw)
        if vyc !=  "None":
           self.m_graph.addSeries(vyc)
        if vzt !=  "None":
           self.m_graph.addSeries(vzt)
        if div !=  "None":
           self.m_graph.addSeries(div)
        if pcv !=  "None":
           self.m_graph.addSeries(pcv)
        if kmx !=  "None":
           self.m_graph.addSeries(kmx)
        if brn !=  "None":
           self.m_graph.addSeries(brn)
        if qgf !=  "None":
           self.m_graph.addSeries(qgf)
        if wzu !=  "None":
           self.m_graph.addSeries(wzu)
        if dkm !=  "None":
           self.m_graph.addSeries(dkm)
        if srf !=  "None":
           self.m_graph.addSeries(srf)
        if sdo !=  "None":
           self.m_graph.addSeries(sdo)
        if sby !=  "None":
           self.m_graph.addSeries(sby)
        if rjw !=  "None":
           self.m_graph.addSeries(rjw)
        if eln !=  "None":
           self.m_graph.addSeries(eln)
        if gxz !=  "None":
           self.m_graph.addSeries(gxz)
        if guq !=  "None":
           self.m_graph.addSeries(guq)
        if gsw !=  "None":
           self.m_graph.addSeries(gsw)
        if fsb !=  "None":
           self.m_graph.addSeries(fsb)
        if vtp !=  "None":
           self.m_graph.addSeries(vtp)
        if cxp !=  "None":
           self.m_graph.addSeries(cxp)
        if nea !=  "None":
           self.m_graph.addSeries(nea)
        if iaa !=  "None":
           self.m_graph.addSeries(iaa)
        if pez !=  "None":
           self.m_graph.addSeries(pez)
        if mdm !=  "None":
           self.m_graph.addSeries(mdm)
        if slf !=  "None":
           self.m_graph.addSeries(slf)
        if zfm !=  "None":
           self.m_graph.addSeries(zfm)
        if eak !=  "None":
           self.m_graph.addSeries(eak)
        if cdm !=  "None":
           self.m_graph.addSeries(cdm)
        if ymi !=  "None":
           self.m_graph.addSeries(ymi)
        if eax !=  "None":
           self.m_graph.addSeries(eax)
        if pfu !=  "None":
           self.m_graph.addSeries(pfu)
        if xui !=  "None":
           self.m_graph.addSeries(xui)
        if jrr !=  "None":
           self.m_graph.addSeries(jrr)
        if jiy !=  "None":
           self.m_graph.addSeries(jiy)
        if prv !=  "None":
           self.m_graph.addSeries(prv)
        if nml !=  "None":
           self.m_graph.addSeries(nml)
        if mxy !=  "None":
           self.m_graph.addSeries(mxy)
        if wto !=  "None":
           self.m_graph.addSeries(wto)
        if qoh !=  "None":
           self.m_graph.addSeries(qoh)
        if hvb !=  "None":
           self.m_graph.addSeries(hvb)
        if iqw !=  "None":
           self.m_graph.addSeries(iqw)
        if scj !=  "None":
           self.m_graph.addSeries(scj)
        if qhs !=  "None":
           self.m_graph.addSeries(qhs)
        if moj !=  "None":
           self.m_graph.addSeries(moj)
        if vtl !=  "None":
           self.m_graph.addSeries(vtl)
        if yxy !=  "None":
           self.m_graph.addSeries(yxy)
        if yak !=  "None":
           self.m_graph.addSeries(yak)
        if nta !=  "None":
           self.m_graph.addSeries(nta)
        if csv !=  "None":
           self.m_graph.addSeries(csv)
        if yrl !=  "None":
           self.m_graph.addSeries(yrl)
        if vxi !=  "None":
           self.m_graph.addSeries(vxi)
        if fuf !=  "None":
           self.m_graph.addSeries(fuf)
        if krz !=  "None":
           self.m_graph.addSeries(krz)
        if jvn !=  "None":
           self.m_graph.addSeries(jvn)
        if pnv !=  "None":
           self.m_graph.addSeries(pnv)
        if ezl !=  "None":
           self.m_graph.addSeries(ezl)
        if iau !=  "None":
           self.m_graph.addSeries(iau)
        if aaj !=  "None":
           self.m_graph.addSeries(aaj)
        if xir !=  "None":
           self.m_graph.addSeries(xir)
        if qdj !=  "None":
           self.m_graph.addSeries(qdj)
        if zel !=  "None":
           self.m_graph.addSeries(zel)
        if jej !=  "None":
           self.m_graph.addSeries(jej)
        if vds !=  "None":
           self.m_graph.addSeries(vds)
        if jxq !=  "None":
           self.m_graph.addSeries(jxq)
        if ras !=  "None":
           self.m_graph.addSeries(ras)
        if flw !=  "None":
           self.m_graph.addSeries(flw)
        if lfw !=  "None":
           self.m_graph.addSeries(lfw)
        if uoj !=  "None":
           self.m_graph.addSeries(uoj)
        if ohu !=  "None":
           self.m_graph.addSeries(ohu)
        if lxy !=  "None":
           self.m_graph.addSeries(lxy)
        if vyf !=  "None":
           self.m_graph.addSeries(vyf)
        if znr !=  "None":
           self.m_graph.addSeries(znr)
        if sox !=  "None":
           self.m_graph.addSeries(sox)
        if ukw !=  "None":
           self.m_graph.addSeries(ukw)
        if meh !=  "None":
           self.m_graph.addSeries(meh)
        if qmm !=  "None":
           self.m_graph.addSeries(qmm)
        if yef !=  "None":
           self.m_graph.addSeries(yef)
        if zkn !=  "None":
           self.m_graph.addSeries(zkn)
        if het !=  "None":
           self.m_graph.addSeries(het)
        if zai !=  "None":
           self.m_graph.addSeries(zai)
        if tmq !=  "None":
           self.m_graph.addSeries(tmq)
        if qyn !=  "None":
           self.m_graph.addSeries(qyn)
        if mws !=  "None":
           self.m_graph.addSeries(mws)
        if rwb !=  "None":
           self.m_graph.addSeries(rwb)
        if aok !=  "None":
           self.m_graph.addSeries(aok)
        if efp !=  "None":
           self.m_graph.addSeries(efp)
        if qqi !=  "None":
           self.m_graph.addSeries(qqi)
        if qit !=  "None":
           self.m_graph.addSeries(qit)
        if tfx !=  "None":
           self.m_graph.addSeries(tfx)
        if wxp !=  "None":
           self.m_graph.addSeries(wxp)
        if fjo !=  "None":
           self.m_graph.addSeries(fjo)
        if gtf !=  "None":
           self.m_graph.addSeries(gtf)
        if juo !=  "None":
           self.m_graph.addSeries(juo)
        if bsh !=  "None":
           self.m_graph.addSeries(bsh)
        if gvt !=  "None":
           self.m_graph.addSeries(gvt)
        if cln !=  "None":
           self.m_graph.addSeries(cln)
        if rzk !=  "None":
           self.m_graph.addSeries(rzk)
        if jsk !=  "None":
           self.m_graph.addSeries(jsk)
        if zyv !=  "None":
           self.m_graph.addSeries(zyv)
        if phn !=  "None":
           self.m_graph.addSeries(phn)
        if pco !=  "None":
           self.m_graph.addSeries(pco)
        if gsi !=  "None":
           self.m_graph.addSeries(gsi)
        if jri !=  "None":
           self.m_graph.addSeries(jri)
        if tqs !=  "None":
           self.m_graph.addSeries(tqs)
        if mfh !=  "None":
           self.m_graph.addSeries(mfh)
        if yfm !=  "None":
           self.m_graph.addSeries(yfm)
        if cdi !=  "None":
           self.m_graph.addSeries(cdi)
        if zay !=  "None":
           self.m_graph.addSeries(zay)
        if ecs !=  "None":
           self.m_graph.addSeries(ecs)
        if txv !=  "None":
           self.m_graph.addSeries(txv)
        if ant !=  "None":
           self.m_graph.addSeries(ant)
        if ay !=  "None":
           self.m_graph.addSeries(ay)
        if aul !=  "None":
           self.m_graph.addSeries(aul)
        if kwr !=  "None":
           self.m_graph.addSeries(kwr)
        if zqb !=  "None":
           self.m_graph.addSeries(zqb)
        if wqv !=  "None":
           self.m_graph.addSeries(wqv)
        if jtz !=  "None":
           self.m_graph.addSeries(jtz)
        if cds !=  "None":
           self.m_graph.addSeries(cds)
        if luj !=  "None":
           self.m_graph.addSeries(luj)
        if gal !=  "None":
           self.m_graph.addSeries(gal)
        if hyf !=  "None":
           self.m_graph.addSeries(hyf)
        if jmi !=  "None":
           self.m_graph.addSeries(jmi)
        if npr !=  "None":
           self.m_graph.addSeries(npr)
        if dwy !=  "None":
           self.m_graph.addSeries(dwy)
        if ehs !=  "None":
           self.m_graph.addSeries(ehs)
        if hfq !=  "None":
           self.m_graph.addSeries(hfq)
        if zcw !=  "None":
           self.m_graph.addSeries(zcw)
        if qnu !=  "None":
           self.m_graph.addSeries(qnu)
        if aer !=  "None":
           self.m_graph.addSeries(aer)
        if pej !=  "None":
           self.m_graph.addSeries(pej)
        if fru !=  "None":
           self.m_graph.addSeries(fru)
        if mub !=  "None":
           self.m_graph.addSeries(mub)
        if lkc !=  "None":
           self.m_graph.addSeries(lkc)
        if hjf !=  "None":
           self.m_graph.addSeries(hjf)
        if aab !=  "None":
           self.m_graph.addSeries(aab)
        if eqx !=  "None":
           self.m_graph.addSeries(eqx)
        if rtd !=  "None":
           self.m_graph.addSeries(rtd)
        if byn !=  "None":
           self.m_graph.addSeries(byn)
        if aoy !=  "None":
           self.m_graph.addSeries(aoy)
        if kat !=  "None":
           self.m_graph.addSeries(kat)
        if kru !=  "None":
           self.m_graph.addSeries(kru)
        if dkv !=  "None":
           self.m_graph.addSeries(dkv)
        if djw !=  "None":
           self.m_graph.addSeries(djw)
        if ezm !=  "None":
           self.m_graph.addSeries(ezm)
        if syb !=  "None":
           self.m_graph.addSeries(syb)
        if gbz !=  "None":
           self.m_graph.addSeries(gbz)
        if rhx !=  "None":
           self.m_graph.addSeries(rhx)
        if rge !=  "None":
           self.m_graph.addSeries(rge)
        if ise !=  "None":
           self.m_graph.addSeries(ise)
        if rev !=  "None":
           self.m_graph.addSeries(rev)
        if xwi !=  "None":
           self.m_graph.addSeries(xwi)
        if xti !=  "None":
           self.m_graph.addSeries(xti)
        if wxd !=  "None":
           self.m_graph.addSeries(wxd)
        if sli !=  "None":
           self.m_graph.addSeries(sli)
        if dek !=  "None":
           self.m_graph.addSeries(dek)
        if lgs !=  "None":
           self.m_graph.addSeries(lgs)
        if xkz !=  "None":
           self.m_graph.addSeries(xkz)
        if vpa !=  "None":
           self.m_graph.addSeries(vpa)
        if clv !=  "None":
           self.m_graph.addSeries(clv)
        if haf !=  "None":
           self.m_graph.addSeries(haf)
        if usu !=  "None":
           self.m_graph.addSeries(usu)
        if mmo !=  "None":
           self.m_graph.addSeries(mmo)
        if ntc !=  "None":
           self.m_graph.addSeries(ntc)
        if kay !=  "None":
           self.m_graph.addSeries(kay)
        if edr !=  "None":
           self.m_graph.addSeries(edr)
        if iiv !=  "None":
           self.m_graph.addSeries(iiv)
        if duj !=  "None":
           self.m_graph.addSeries(duj)
        if wtk !=  "None":
           self.m_graph.addSeries(wtk)
        if xdl !=  "None":
           self.m_graph.addSeries(xdl)
        if lwn !=  "None":
           self.m_graph.addSeries(lwn)
        if zrt !=  "None":
           self.m_graph.addSeries(zrt)
        if eol !=  "None":
           self.m_graph.addSeries(eol)
        if kgc !=  "None":
           self.m_graph.addSeries(kgc)
        if zks !=  "None":
           self.m_graph.addSeries(zks)
        if bad !=  "None":
           self.m_graph.addSeries(bad)
        if cyd !=  "None":
           self.m_graph.addSeries(cyd)
        if ach !=  "None":
           self.m_graph.addSeries(ach)
        if lox !=  "None":
           self.m_graph.addSeries(lox)
        if dsw !=  "None":
           self.m_graph.addSeries(dsw)
        if yuh !=  "None":
           self.m_graph.addSeries(yuh)
        if zgp !=  "None":
           self.m_graph.addSeries(zgp)
        if iib !=  "None":
           self.m_graph.addSeries(iib)
        if jkx !=  "None":
           self.m_graph.addSeries(jkx)
        if uwe !=  "None":
           self.m_graph.addSeries(uwe)
        if knh !=  "None":
           self.m_graph.addSeries(knh)
        if chk !=  "None":
           self.m_graph.addSeries(chk)
        if zgj !=  "None":
           self.m_graph.addSeries(zgj)
        if gka !=  "None":
           self.m_graph.addSeries(gka)
        if asa !=  "None":
           self.m_graph.addSeries(asa)
        if ioj !=  "None":
           self.m_graph.addSeries(ioj)
        if qak !=  "None":
           self.m_graph.addSeries(qak)
        if jov !=  "None":
           self.m_graph.addSeries(jov)
        if ynm !=  "None":
           self.m_graph.addSeries(ynm)
        if wdb !=  "None":
           self.m_graph.addSeries(wdb)
        if owe !=  "None":
           self.m_graph.addSeries(owe)
        if uod !=  "None":
           self.m_graph.addSeries(uod)
        if zjw !=  "None":
           self.m_graph.addSeries(zjw)
        if paj !=  "None":
           self.m_graph.addSeries(paj)
        if txi !=  "None":
           self.m_graph.addSeries(txi)
        if sab !=  "None":
           self.m_graph.addSeries(sab)
        if mhu !=  "None":
           self.m_graph.addSeries(mhu)
        if oyc !=  "None":
           self.m_graph.addSeries(oyc)
        if rtc !=  "None":
           self.m_graph.addSeries(rtc)
        if akf !=  "None":
           self.m_graph.addSeries(akf)
        if tzs !=  "None":
           self.m_graph.addSeries(tzs)
        if yba !=  "None":
           self.m_graph.addSeries(yba)
        if grp !=  "None":
           self.m_graph.addSeries(grp)
        if cdw !=  "None":
           self.m_graph.addSeries(cdw)
        if syx !=  "None":
           self.m_graph.addSeries(syx)
        if mnv !=  "None":
           self.m_graph.addSeries(mnv)
        if xeh !=  "None":
           self.m_graph.addSeries(xeh)
        if hxo !=  "None":
           self.m_graph.addSeries(hxo)
        if kkk !=  "None":
           self.m_graph.addSeries(kkk)
        if dwr !=  "None":
           self.m_graph.addSeries(dwr)
        if zpn !=  "None":
           self.m_graph.addSeries(zpn)
        if pnl !=  "None":
           self.m_graph.addSeries(pnl)
        if bgb !=  "None":
           self.m_graph.addSeries(bgb)
        if ivs !=  "None":
           self.m_graph.addSeries(ivs)
        if rcg !=  "None":
           self.m_graph.addSeries(rcg)
        if orn !=  "None":
           self.m_graph.addSeries(orn)
        if nwx !=  "None":
           self.m_graph.addSeries(nwx)
        if zrp !=  "None":
           self.m_graph.addSeries(zrp)
        if rmd !=  "None":
           self.m_graph.addSeries(rmd)
        if jnl !=  "None":
           self.m_graph.addSeries(jnl)
        if fvv !=  "None":
           self.m_graph.addSeries(fvv)
        if gyl !=  "None":
           self.m_graph.addSeries(gyl)
        if wgv !=  "None":
           self.m_graph.addSeries(wgv)
        if sqq !=  "None":
           self.m_graph.addSeries(sqq)
        if qzj !=  "None":
           self.m_graph.addSeries(qzj)
        if yve !=  "None":
           self.m_graph.addSeries(yve)
        if kos !=  "None":
           self.m_graph.addSeries(kos)
        if ece !=  "None":
           self.m_graph.addSeries(ece)
        if igk !=  "None":
           self.m_graph.addSeries(igk)
        if ybw !=  "None":
           self.m_graph.addSeries(ybw)
        if epa !=  "None":
           self.m_graph.addSeries(epa)
        if lsb !=  "None":
           self.m_graph.addSeries(lsb)
        if nvl !=  "None":
           self.m_graph.addSeries(nvl)
        if lem !=  "None":
           self.m_graph.addSeries(lem)
        if idi !=  "None":
           self.m_graph.addSeries(idi)
        if fzm !=  "None":
           self.m_graph.addSeries(fzm)
        if agm !=  "None":
           self.m_graph.addSeries(agm)
        if rja !=  "None":
           self.m_graph.addSeries(rja)
        if vfc !=  "None":
           self.m_graph.addSeries(vfc)
        if emy !=  "None":
           self.m_graph.addSeries(emy)
        if djk !=  "None":
           self.m_graph.addSeries(djk)
        if pw !=  "None":
           self.m_graph.addSeries(pw)
        if efq !=  "None":
           self.m_graph.addSeries(efq)
        if zpl !=  "None":
           self.m_graph.addSeries(zpl)
        if iks !=  "None":
           self.m_graph.addSeries(iks)
        if ypm !=  "None":
           self.m_graph.addSeries(ypm)
        if lme !=  "None":
           self.m_graph.addSeries(lme)
        if jba !=  "None":
           self.m_graph.addSeries(jba)
        if blt !=  "None":
           self.m_graph.addSeries(blt)
        if aod !=  "None":
           self.m_graph.addSeries(aod)
        if dkx !=  "None":
           self.m_graph.addSeries(dkx)
        if mey !=  "None":
           self.m_graph.addSeries(mey)
        if rdm !=  "None":
           self.m_graph.addSeries(rdm)
        if tlz !=  "None":
           self.m_graph.addSeries(tlz)
        if ivw !=  "None":
           self.m_graph.addSeries(ivw)
        if rpa !=  "None":
           self.m_graph.addSeries(rpa)
        if dgz !=  "None":
           self.m_graph.addSeries(dgz)
        if zpa !=  "None":
           self.m_graph.addSeries(zpa)
        if kto !=  "None":
           self.m_graph.addSeries(kto)
        if ltz !=  "None":
           self.m_graph.addSeries(ltz)
        if pfk !=  "None":
           self.m_graph.addSeries(pfk)
        if ema !=  "None":
           self.m_graph.addSeries(ema)
        if tjo !=  "None":
           self.m_graph.addSeries(tjo)
        if jje !=  "None":
           self.m_graph.addSeries(jje)
        if hzd !=  "None":
           self.m_graph.addSeries(hzd)
        if fxt !=  "None":
           self.m_graph.addSeries(fxt)
        if azp !=  "None":
           self.m_graph.addSeries(azp)
        if zmc !=  "None":
           self.m_graph.addSeries(zmc)
        if gxl !=  "None":
           self.m_graph.addSeries(gxl)
        if qiw !=  "None":
           self.m_graph.addSeries(qiw)
        if plt !=  "None":
           self.m_graph.addSeries(plt)
        if zhk !=  "None":
           self.m_graph.addSeries(zhk)
        if wpr !=  "None":
           self.m_graph.addSeries(wpr)
        if zrf !=  "None":
           self.m_graph.addSeries(zrf)
        if dwk !=  "None":
           self.m_graph.addSeries(dwk)
        if cwm !=  "None":
           self.m_graph.addSeries(cwm)
        if kyf !=  "None":
           self.m_graph.addSeries(kyf)
        if kfa !=  "None":
           self.m_graph.addSeries(kfa)
        if jnt !=  "None":
           self.m_graph.addSeries(jnt)
        if jjn !=  "None":
           self.m_graph.addSeries(jjn)
        if fii !=  "None":
           self.m_graph.addSeries(fii)
        if mjl !=  "None":
           self.m_graph.addSeries(mjl)
        if vdt !=  "None":
           self.m_graph.addSeries(vdt)
        if uga !=  "None":
           self.m_graph.addSeries(uga)
        if lff !=  "None":
           self.m_graph.addSeries(lff)
        if omm !=  "None":
           self.m_graph.addSeries(omm)
        if gyf !=  "None":
           self.m_graph.addSeries(gyf)
        if qhn !=  "None":
           self.m_graph.addSeries(qhn)
        if fpx !=  "None":
           self.m_graph.addSeries(fpx)
        if ksm !=  "None":
           self.m_graph.addSeries(ksm)
        if jyq !=  "None":
           self.m_graph.addSeries(jyq)
        if ilo !=  "None":
           self.m_graph.addSeries(ilo)
        if qbe !=  "None":
           self.m_graph.addSeries(qbe)
        if pxs !=  "None":
           self.m_graph.addSeries(pxs)
        if xup !=  "None":
           self.m_graph.addSeries(xup)
        if srs !=  "None":
           self.m_graph.addSeries(srs)
        if nzx !=  "None":
           self.m_graph.addSeries(nzx)
        if gda !=  "None":
           self.m_graph.addSeries(gda)
        if yxq !=  "None":
           self.m_graph.addSeries(yxq)
        if cuc !=  "None":
           self.m_graph.addSeries(cuc)
        if rrv !=  "None":
           self.m_graph.addSeries(rrv)
        if kem !=  "None":
           self.m_graph.addSeries(kem)
        if xbx !=  "None":
           self.m_graph.addSeries(xbx)
        if aug !=  "None":
           self.m_graph.addSeries(aug)
        if sjg !=  "None":
           self.m_graph.addSeries(sjg)
        if rjb !=  "None":
           self.m_graph.addSeries(rjb)
        if ipt !=  "None":
           self.m_graph.addSeries(ipt)
        if qhh !=  "None":
           self.m_graph.addSeries(qhh)
        if bpm !=  "None":
           self.m_graph.addSeries(bpm)
        if sma !=  "None":
           self.m_graph.addSeries(sma)
        if rex !=  "None":
           self.m_graph.addSeries(rex)
        if aql !=  "None":
           self.m_graph.addSeries(aql)
        if evp !=  "None":
           self.m_graph.addSeries(evp)
        if lxm !=  "None":
           self.m_graph.addSeries(lxm)
        if zop !=  "None":
           self.m_graph.addSeries(zop)
        if asm !=  "None":
           self.m_graph.addSeries(asm)
        if twg !=  "None":
           self.m_graph.addSeries(twg)
        if uak !=  "None":
           self.m_graph.addSeries(uak)
        if bwh !=  "None":
           self.m_graph.addSeries(bwh)
        if uke !=  "None":
           self.m_graph.addSeries(uke)
        if cpf !=  "None":
           self.m_graph.addSeries(cpf)
        if xcp !=  "None":
           self.m_graph.addSeries(xcp)
        if quv !=  "None":
           self.m_graph.addSeries(quv)
        if tnq !=  "None":
           self.m_graph.addSeries(tnq)
        if awu !=  "None":
           self.m_graph.addSeries(awu)
        if qud !=  "None":
           self.m_graph.addSeries(qud)
        if lvw !=  "None":
           self.m_graph.addSeries(lvw)
        if kuf !=  "None":
           self.m_graph.addSeries(kuf)
        if eph !=  "None":
           self.m_graph.addSeries(eph)
        if hxs !=  "None":
           self.m_graph.addSeries(hxs)
        if ifi !=  "None":
           self.m_graph.addSeries(ifi)
        if yag !=  "None":
           self.m_graph.addSeries(yag)
        if tbj !=  "None":
           self.m_graph.addSeries(tbj)
        if gah !=  "None":
           self.m_graph.addSeries(gah)
        if ybf !=  "None":
           self.m_graph.addSeries(ybf)
        if vnl !=  "None":
           self.m_graph.addSeries(vnl)
        if rgf !=  "None":
           self.m_graph.addSeries(rgf)
        if ezw !=  "None":
           self.m_graph.addSeries(ezw)
        if xul !=  "None":
           self.m_graph.addSeries(xul)
        if vqb !=  "None":
           self.m_graph.addSeries(vqb)
        if xlt !=  "None":
           self.m_graph.addSeries(xlt)
        if edi !=  "None":
           self.m_graph.addSeries(edi)
        if twn !=  "None":
           self.m_graph.addSeries(twn)
        if krk !=  "None":
           self.m_graph.addSeries(krk)
        if jcq !=  "None":
           self.m_graph.addSeries(jcq)
        if iez !=  "None":
           self.m_graph.addSeries(iez)
        if ady !=  "None":
           self.m_graph.addSeries(ady)
        if via !=  "None":
           self.m_graph.addSeries(via)
        if yiv !=  "None":
           self.m_graph.addSeries(yiv)
        if xyi !=  "None":
           self.m_graph.addSeries(xyi)
        if pif !=  "None":
           self.m_graph.addSeries(pif)
        if ket !=  "None":
           self.m_graph.addSeries(ket)
        if zzq !=  "None":
           self.m_graph.addSeries(zzq)
        if epi !=  "None":
           self.m_graph.addSeries(epi)
        if mxq !=  "None":
           self.m_graph.addSeries(mxq)
        if vby !=  "None":
           self.m_graph.addSeries(vby)
        if jpx !=  "None":
           self.m_graph.addSeries(jpx)
        if lru !=  "None":
           self.m_graph.addSeries(lru)
        if rae !=  "None":
           self.m_graph.addSeries(rae)
        if oiy !=  "None":
           self.m_graph.addSeries(oiy)
        if gam !=  "None":
           self.m_graph.addSeries(gam)
        if ljf !=  "None":
           self.m_graph.addSeries(ljf)
        if gha !=  "None":
           self.m_graph.addSeries(gha)
        if alb !=  "None":
           self.m_graph.addSeries(alb)
        if duq !=  "None":
           self.m_graph.addSeries(duq)
        if wyj !=  "None":
           self.m_graph.addSeries(wyj)
        if dck !=  "None":
           self.m_graph.addSeries(dck)
        if rwc !=  "None":
           self.m_graph.addSeries(rwc)
        if qlk !=  "None":
           self.m_graph.addSeries(qlk)
        if niy !=  "None":
           self.m_graph.addSeries(niy)
        if oxx !=  "None":
           self.m_graph.addSeries(oxx)
        if raz !=  "None":
           self.m_graph.addSeries(raz)
        if bjm !=  "None":
           self.m_graph.addSeries(bjm)
        if hmw !=  "None":
           self.m_graph.addSeries(hmw)
        if uae !=  "None":
           self.m_graph.addSeries(uae)
        if dnk !=  "None":
           self.m_graph.addSeries(dnk)
        if btz !=  "None":
           self.m_graph.addSeries(btz)
        if wgt !=  "None":
           self.m_graph.addSeries(wgt)
        if eoh !=  "None":
           self.m_graph.addSeries(eoh)
        if sgh !=  "None":
           self.m_graph.addSeries(sgh)
        if gri !=  "None":
           self.m_graph.addSeries(gri)
        if fgh !=  "None":
           self.m_graph.addSeries(fgh)
        if pvl !=  "None":
           self.m_graph.addSeries(pvl)
        if vhb !=  "None":
           self.m_graph.addSeries(vhb)
        if cfx !=  "None":
           self.m_graph.addSeries(cfx)
        if rkw !=  "None":
           self.m_graph.addSeries(rkw)
        if ezo !=  "None":
           self.m_graph.addSeries(ezo)
        if juu !=  "None":
           self.m_graph.addSeries(juu)
        if erc !=  "None":
           self.m_graph.addSeries(erc)
        if cyx !=  "None":
           self.m_graph.addSeries(cyx)
        if ewy !=  "None":
           self.m_graph.addSeries(ewy)
        if ylh !=  "None":
           self.m_graph.addSeries(ylh)
        if xwq !=  "None":
           self.m_graph.addSeries(xwq)
        if eri !=  "None":
           self.m_graph.addSeries(eri)
        if jsa !=  "None":
           self.m_graph.addSeries(jsa)
        if llk !=  "None":
           self.m_graph.addSeries(llk)
        if bec !=  "None":
           self.m_graph.addSeries(bec)
        if uhc !=  "None":
           self.m_graph.addSeries(uhc)
        if xhh !=  "None":
           self.m_graph.addSeries(xhh)
        if phf !=  "None":
           self.m_graph.addSeries(phf)
        if lvn !=  "None":
           self.m_graph.addSeries(lvn)
        if dca !=  "None":
           self.m_graph.addSeries(dca)
        if vfz !=  "None":
           self.m_graph.addSeries(vfz)
        if nvc !=  "None":
           self.m_graph.addSeries(nvc)
        if nsw !=  "None":
           self.m_graph.addSeries(nsw)
        if waj !=  "None":
           self.m_graph.addSeries(waj)
        if dqj !=  "None":
           self.m_graph.addSeries(dqj)
        if wnq !=  "None":
           self.m_graph.addSeries(wnq)
        if byw !=  "None":
           self.m_graph.addSeries(byw)
        if ypi !=  "None":
           self.m_graph.addSeries(ypi)
        if ygg !=  "None":
           self.m_graph.addSeries(ygg)
        if njn !=  "None":
           self.m_graph.addSeries(njn)
        if vxj !=  "None":
           self.m_graph.addSeries(vxj)
        if gvq !=  "None":
           self.m_graph.addSeries(gvq)
        if giv !=  "None":
           self.m_graph.addSeries(giv)
        if wpt !=  "None":
           self.m_graph.addSeries(wpt)
        if bog !=  "None":
           self.m_graph.addSeries(bog)
        if gzu !=  "None":
           self.m_graph.addSeries(gzu)
        if kcl !=  "None":
           self.m_graph.addSeries(kcl)
        if uco !=  "None":
           self.m_graph.addSeries(uco)
        if guz !=  "None":
           self.m_graph.addSeries(guz)
        if hby !=  "None":
           self.m_graph.addSeries(hby)
        if axj !=  "None":
           self.m_graph.addSeries(axj)
        if qve !=  "None":
           self.m_graph.addSeries(qve)
        if vov !=  "None":
           self.m_graph.addSeries(vov)
        if yfj !=  "None":
           self.m_graph.addSeries(yfj)
        if bph !=  "None":
           self.m_graph.addSeries(bph)
        if wad !=  "None":
           self.m_graph.addSeries(wad)
        if fpa !=  "None":
           self.m_graph.addSeries(fpa)
        if tnz !=  "None":
           self.m_graph.addSeries(tnz)
        if dbu !=  "None":
           self.m_graph.addSeries(dbu)
        if hyg !=  "None":
           self.m_graph.addSeries(hyg)
        if tav !=  "None":
           self.m_graph.addSeries(tav)
        if vyl !=  "None":
           self.m_graph.addSeries(vyl)
        if ovr !=  "None":
           self.m_graph.addSeries(ovr)
        if juj !=  "None":
           self.m_graph.addSeries(juj)
        if neb !=  "None":
           self.m_graph.addSeries(neb)
        if zwi !=  "None":
           self.m_graph.addSeries(zwi)
        if mio !=  "None":
           self.m_graph.addSeries(mio)
        if bhh !=  "None":
           self.m_graph.addSeries(bhh)
        if hqe !=  "None":
           self.m_graph.addSeries(hqe)
        if xga !=  "None":
           self.m_graph.addSeries(xga)
        if tnp !=  "None":
           self.m_graph.addSeries(tnp)
        if fmx !=  "None":
           self.m_graph.addSeries(fmx)
        if ewo !=  "None":
           self.m_graph.addSeries(ewo)
        if mlh !=  "None":
           self.m_graph.addSeries(mlh)
        if bqk !=  "None":
           self.m_graph.addSeries(bqk)
        if kcb !=  "None":
           self.m_graph.addSeries(kcb)
        if htt !=  "None":
           self.m_graph.addSeries(htt)
        if usp !=  "None":
           self.m_graph.addSeries(usp)
        if oil !=  "None":
           self.m_graph.addSeries(oil)
        if ttx !=  "None":
           self.m_graph.addSeries(ttx)
        if ajx !=  "None":
           self.m_graph.addSeries(ajx)
        if zac !=  "None":
           self.m_graph.addSeries(zac)
        if jll !=  "None":
           self.m_graph.addSeries(jll)
        if qrl !=  "None":
           self.m_graph.addSeries(qrl)
        if tkg !=  "None":
           self.m_graph.addSeries(tkg)
        if vrk !=  "None":
           self.m_graph.addSeries(vrk)
        if puu !=  "None":
           self.m_graph.addSeries(puu)
        if kpw !=  "None":
           self.m_graph.addSeries(kpw)
        if qop !=  "None":
           self.m_graph.addSeries(qop)
        if tkn !=  "None":
           self.m_graph.addSeries(tkn)
        if whe !=  "None":
           self.m_graph.addSeries(whe)
        if juh !=  "None":
           self.m_graph.addSeries(juh)
        if spn !=  "None":
           self.m_graph.addSeries(spn)
        if tcf !=  "None":
           self.m_graph.addSeries(tcf)
        if xxj !=  "None":
           self.m_graph.addSeries(xxj)
        if ogu !=  "None":
           self.m_graph.addSeries(ogu)
        if ywz !=  "None":
           self.m_graph.addSeries(ywz)
        if mwx !=  "None":
           self.m_graph.addSeries(mwx)
        if lvm !=  "None":
           self.m_graph.addSeries(lvm)
        if vzx !=  "None":
           self.m_graph.addSeries(vzx)
        if due !=  "None":
           self.m_graph.addSeries(due)
        if cxr !=  "None":
           self.m_graph.addSeries(cxr)
        if sug !=  "None":
           self.m_graph.addSeries(sug)
        if hhs !=  "None":
           self.m_graph.addSeries(hhs)
        if gbx !=  "None":
           self.m_graph.addSeries(gbx)
        if teu !=  "None":
           self.m_graph.addSeries(teu)
        if tur !=  "None":
           self.m_graph.addSeries(tur)
        if uju !=  "None":
           self.m_graph.addSeries(uju)
        if hhf !=  "None":
           self.m_graph.addSeries(hhf)
        if dma !=  "None":
           self.m_graph.addSeries(dma)
        if nsb !=  "None":
           self.m_graph.addSeries(nsb)
        if kdo !=  "None":
           self.m_graph.addSeries(kdo)
        if akr !=  "None":
           self.m_graph.addSeries(akr)
        if gqd !=  "None":
           self.m_graph.addSeries(gqd)
        if kkg !=  "None":
           self.m_graph.addSeries(kkg)
        if uit !=  "None":
           self.m_graph.addSeries(uit)
        if ibg !=  "None":
           self.m_graph.addSeries(ibg)
        if klu !=  "None":
           self.m_graph.addSeries(klu)
        if vbx !=  "None":
           self.m_graph.addSeries(vbx)
        if get !=  "None":
           self.m_graph.addSeries(get)
        if jqr !=  "None":
           self.m_graph.addSeries(jqr)
        if zuz !=  "None":
           self.m_graph.addSeries(zuz)
        if zkh !=  "None":
           self.m_graph.addSeries(zkh)
        if ppp !=  "None":
           self.m_graph.addSeries(ppp)
        if vtd !=  "None":
           self.m_graph.addSeries(vtd)
        if kzd !=  "None":
           self.m_graph.addSeries(kzd)
        if vhn !=  "None":
           self.m_graph.addSeries(vhn)
        if nuj !=  "None":
           self.m_graph.addSeries(nuj)
        if paq !=  "None":
           self.m_graph.addSeries(paq)
        if kwm !=  "None":
           self.m_graph.addSeries(kwm)
        if hyu !=  "None":
           self.m_graph.addSeries(hyu)
        if wae !=  "None":
           self.m_graph.addSeries(wae)
        if zom !=  "None":
           self.m_graph.addSeries(zom)
        if uth !=  "None":
           self.m_graph.addSeries(uth)
        if mnb !=  "None":
           self.m_graph.addSeries(mnb)
        if gfl !=  "None":
           self.m_graph.addSeries(gfl)
        if uck !=  "None":
           self.m_graph.addSeries(uck)
        if cwn !=  "None":
           self.m_graph.addSeries(cwn)
        if gjm !=  "None":
           self.m_graph.addSeries(gjm)
        if btk !=  "None":
           self.m_graph.addSeries(btk)
        if tlr !=  "None":
           self.m_graph.addSeries(tlr)
        if exb !=  "None":
           self.m_graph.addSeries(exb)
        if szr !=  "None":
           self.m_graph.addSeries(szr)
        if odt !=  "None":
           self.m_graph.addSeries(odt)
        if dwl !=  "None":
           self.m_graph.addSeries(dwl)
        if tez !=  "None":
           self.m_graph.addSeries(tez)
        if qgs !=  "None":
           self.m_graph.addSeries(qgs)
        if etb !=  "None":
           self.m_graph.addSeries(etb)
        if gqt !=  "None":
           self.m_graph.addSeries(gqt)
        if eqb !=  "None":
           self.m_graph.addSeries(eqb)
        if iyc !=  "None":
           self.m_graph.addSeries(iyc)
        if cux !=  "None":
           self.m_graph.addSeries(cux)
        if nlt !=  "None":
           self.m_graph.addSeries(nlt)
        if tcs !=  "None":
           self.m_graph.addSeries(tcs)
        if qdl !=  "None":
           self.m_graph.addSeries(qdl)
        if zea !=  "None":
           self.m_graph.addSeries(zea)
        if ufi !=  "None":
           self.m_graph.addSeries(ufi)
        if ugr !=  "None":
           self.m_graph.addSeries(ugr)
        if png !=  "None":
           self.m_graph.addSeries(png)
        if lbn !=  "None":
           self.m_graph.addSeries(lbn)
        if fye !=  "None":
           self.m_graph.addSeries(fye)
        if gpb !=  "None":
           self.m_graph.addSeries(gpb)
        if atk !=  "None":
           self.m_graph.addSeries(atk)
        if psz !=  "None":
           self.m_graph.addSeries(psz)
        if reg !=  "None":
           self.m_graph.addSeries(reg)
        if rzn !=  "None":
           self.m_graph.addSeries(rzn)
        if kiz !=  "None":
           self.m_graph.addSeries(kiz)
        






