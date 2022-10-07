import DataProcessing
import ase.io.cube as cube
import numpy as np

class ReadingConvertingCube:
    def __init__(self, suffix, spinstate, wavefunction):
        print(suffix, spinstate, wavefunction)
        wfn = DataProcessing.SetupWfnVars.wfnDataStore[str("{}".format(suffix))][str("{}".format(spinstate))][str("{}".format(wavefunction))]
        self.data, self.atoms = cube.read_cube_data(wfn)
        mn = self.data.min()
        mx = self.data.max()

        OptsContours = 4
        n = int(OptsContours)
        d = (mx - mn) /n
        self.contours = np.linspace(mn + d/ 2, mx - d / 2, n).tolist()

        self.A = self.atoms.cell