import numpy as np
import math
import sympy
from sympy import Symbol, symbols
import sympy.abc as abc

class CrystalSystemMatrix:
    def __init__(self, a0, a1, b0, b1, c0, c1, c2, alpha, beta, gamma):
        self.a = [a0, a1, 0]
        self.b = [b0, b1, 0]
        if alpha == abc.alpha:
            cos2a = sympy.cos(alpha) ** 2
            cosa = sympy.cos(alpha)
        else:
            cos2a = round(math.cos(math.radians(alpha))**2,3)
            cosa =  round(math.cos(math.radians(alpha)),3)
        if beta == abc.beta:
            cos2b = sympy.cos(beta) ** 2
            cosb = sympy.cos(beta)
        else:
            cos2b = round(math.cos(math.radians(beta))**2,3)
            cosb = round(math.cos(math.radians(beta)),3)
        if gamma == abc.gamma:
            sin2g = sympy.sin(gamma)**2
            cosg = sympy.sin(gamma)
        else:
            sin2g = round(math.sin(math.radians(gamma))**2,3)
            cosg = round(math.cos(math.radians(gamma)),3)
        if alpha != abc.alpha and beta != abc.beta and gamma != abc.gamma:
            self.C2 = math.sqrt(sin2g - cos2a - cos2b + (2 * cosa * cosb * cosg))
            self.c = [c0, c1, c2 * ((1 / math.sin(math.radians(gamma))) * self.C2)]
        else:
            self.C2 = sympy.sqrt(sin2g - cos2a - cos2b + (2 * cosa * cosb * cosg))
            if gamma != abc.gamma:
                self.c = [c0, c1, c2 * ((1 / math.sin(math.radians(gamma))) * self.C2)]
            else:
                self.c = [c0, c1, c2 * ((1 / sympy.sin(gamma)) * self.C2)]

        self.LatVec = [self.a, self.b, self.c]
        self.LatVec = np.matrix(self.LatVec)

class CubicLattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('a'), c=Symbol('a')):
        alpha  =beta = gamma = 90
        if type(a) != Symbol and type(b) != Symbol and type(c) != Symbol:
            b = a
            c = a
        CrystalSystemMatrix.__init__(self,a,0,0,b,0,0,c,alpha,beta,gamma)

class TetragonalLattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('b'), c=Symbol('c')):
        alpha = beta = gamma = 90
        if type(a) != Symbol and type(b) != Symbol and type(c) != Symbol:
            b = a
        CrystalSystemMatrix.__init__(self, a,0,0,b,0,0,c,alpha,beta,gamma)

class OrthorhombicLattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('b'), c=Symbol('c')):
        alpha = beta = gamma = 90
        CrystalSystemMatrix.__init__(self, a,0,0,b,0,0,c,alpha,beta,gamma)

class HexagonalLattice(CrystalSystemMatrix):
    def __init__(self,a=Symbol('a'), b=Symbol('a'), c=Symbol('c')):
        alpha = beta = 90
        gamma = 120
        a0 = a/2
        a1 = -a * round((math.sqrt(3)/2),3)
        b0 = b/2
        b1 = b * round((math.sqrt(3)/2),3)

        CrystalSystemMatrix.__init__(self,a0,a1,b0,b1,0,0,c,alpha,beta,gamma)

class RhombohedralLattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('a'), c=Symbol('a'), alpha=abc.alpha):
        beta = gamma = alpha
        if type(a) != Symbol and type(b) != Symbol and type(c) != Symbol:
            b_ = a
            c_ = a
        else:
            b_ = b
            c_ = c
        if alpha != abc.alpha:
            beta_ = alpha
            gamma_ = alpha
            a0 = a * round(math.cos(alpha / 2),3)
            a1 = -a * round(math.sin(alpha / 2),3)
            b0 = b_ * round(math.cos(gamma_ / 2),3)
            b1 = b_ * round(math.sin(gamma_ / 2),3)
            c0 = (c_ * round(math.cos(beta_ / 2),3)) / round(math.cos(alpha / 2),3)
        else:
            gamma_ = gamma
            beta_ = beta
            a0 = a * sympy.cos(alpha/2)
            a1 = -a * sympy.sin(alpha/2)
            b0 = b_ * sympy.cos(gamma/2)
            b1 = b_ * sympy.sin(gamma/2)
            c0 = (c_ * sympy.cos(beta/2)) / sympy.cos(alpha/2)
        CrystalSystemMatrix.__init__(self, a0, a1, b0, b1, c0, 0, c_, alpha, beta_, gamma_)

class Monoclinic1Lattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('b'), c=Symbol('c'), beta=abc.beta):
        alpha = gamma = 90
        if beta == abc.beta:
            c1 = c * sympy.cos(beta)
        else:
            c1 = c * round(math.cos(beta),3)
        CrystalSystemMatrix.__init__(self,a,0,0,b,0,c1,c,alpha,beta,gamma)

class Monoclinic2Lattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('b'), c=Symbol('c'), beta=abc.beta):
        alpha = gamma = 90
        if beta == abc.beta:
            c1 = c * sympy.cos(beta)
        else:
            c1 = c * round(math.cos(beta),3)
        CrystalSystemMatrix.__init__(self,0,a,b,0,0,c1,c,alpha,beta,gamma)

class TriclinicLattice(CrystalSystemMatrix):
    def __init__(self, a=Symbol('a'), b=Symbol('b'), c=Symbol('c'), alpha=abc.alpha, beta=abc.beta, gamma=abc.gamma):
        if alpha == abc.alpha and beta == abc.beta and gamma == abc.gamma:
            b0 = b * sympy.cos(gamma)
            b1 = b * sympy.sin(gamma)
            c0 = c * sympy.cos(beta)
            c1mod = sympy.cos(beta) - (sympy.cos(alpha) * sympy.cos(gamma))
            c1 = (c / sympy.sin(gamma)) * c1mod
        else:
            b0 = b * math.cos(gamma)
            b1 = b * math.sin(gamma)
            c0 = c * math.cos(beta)
            c1mod = math.cos(beta) - (math.cos(alpha) * math.cos(gamma))
            if c1mod >= 0:
                c1 = (c / math.sin(gamma)) * c1mod
            elif c1mod <= 0:
                c1 = (c / math.sin(gamma)) * -c1mod
        CrystalSystemMatrix.__init__(self,a,0,b0,b1,c0,c1,c,alpha,beta,gamma)

class IdentifyLatticeSymmetry(CubicLattice,TetragonalLattice,OrthorhombicLattice,HexagonalLattice,RhombohedralLattice,Monoclinic1Lattice,Monoclinic2Lattice,TriclinicLattice):
    def __init__(self,A, B, C):
        self.CrystalSystem = None
        self.LatMatrix = [[round(A[0],3),round(A[1],3),round(A[2],3)], [round(B[0],3),round(B[1],3),round(B[2],3)], [round(C[0],3),round(C[1],3),round(C[2],3)]]
        self.LatMatrix = np.matrix(self.LatMatrix)
        self.A = A
        self.B = B
        self.C = C
        self.Avec = round(np.sqrt(A[0] ** 2 + A[1] ** 2 + A[2] ** 2),3)
        self.Bvec = round(np.sqrt(B[0] ** 2 + B[1] ** 2 + B[2] ** 2),3)
        self.Cvec = round(np.sqrt(C[0] ** 2 + C[1] ** 2 + C[2] ** 2),3)
        self.g = np.arccos(np.dot(A,B)/(self.Avec * self.Bvec))
        self.be = np.arccos(np.dot(A,C)/(self.Avec * self.Cvec))
        self.al = np.arccos(np.dot(B,C)/self.Bvec * self.Cvec)
        CubicLattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec)
        if (self.LatMatrix == self.LatVec).all() == 1:
            self.CrystalSystem = str('CUBIC')
        TetragonalLattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec)
        if (self.LatMatrix== self.LatVec).all() == 1:
            self.CrystalSystem = str('TETRAGONAL')
        OrthorhombicLattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec)
        if (self.LatMatrix== self.LatVec).all() == 1:
            self.CrystalSystem = str('ORTHORHOMBIC')
        HexagonalLattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec)
        if (self.LatMatrix== self.LatVec).all() == 1:
            self.CrystalSystem = str('HEXAGONAL')
        RhombohedralLattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec,alpha=self.al)
        if (self.LatMatrix == self.LatVec).all() == 1:
            self.CrystalSystem = str('RHOMBOHEDRAL')
        Monoclinic1Lattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec,beta=self.be)
        if (self.LatMatrix== self.LatVec).all() == 1:
            self.CrystalSystem = str('MONOCLINIC')
            self.A0B0 = A[0]
            self.A1B1 = B[1]
        Monoclinic2Lattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec,beta=self.be)
        if (self.LatMatrix== self.LatVec).all() == 1:
            self.CrystalSystem = str('MONOCLINIC')
            self.A0B0 = B[0]
            self.A1B1 = A[1]
        TriclinicLattice.__init__(self,a=self.Avec,b=self.Bvec,c=self.Cvec,alpha=self.al,beta=self.be,gamma=self.g)
        if (self.LatMatrix== self.LatVec).all() == 1:
            self.CrystalSystem = str('TRICLINIC')


class CellBounds(IdentifyLatticeSymmetry):
    def __init__(self,A,B,C,x,z):
        IdentifyLatticeSymmetry.__init__(self,A,B,C)
        self.lowerXbound = None
        self.upperXbound = None
        self.lowerYbound = None
        self.upperYbound = None
        self.A = A
        self.B = B
        self.C = C
        if self.CrystalSystem == 'CUBIC' or 'TETRAGONAL' or 'ORTHORHOMBIC':
            self.returnBoxbounds()
        elif self.CrystalSystem == 'HEXAGONAL':
            self.returnHexagonalbounds(x)
        elif self.CrystalSystem == 'TRICLINIC':
            self.returnTriclinicbounds(z)
        elif self.CrystalSystem == 'MONOCLINIC':
            self.returnMonoclinicbounds(z)

    def returnHexagonalbounds(self,x):
        xmid = self.B[0]
        if x < xmid:
            self.lowerYbound= -self.B[1] * x /self.A[0]
            self.upperYbound= -self.A[1] * x / self.B[0]
        elif x > xmid:
            self.upperYbound = ((self.A[0] * self.B[1]) - (self.A[1] * self.B[0]) -(self.B[1] * x)) / self.A[0]
            self.lowerYbound = ((self.A[0] * self.B[1]) - (self.A[1] * self.B[0]) - (self.A[1] * x)) / self.B[0]
        self.lowerXbound = x
        self.lowerYbound = x
        return self.lowerXbound, self.upperXbound, self.lowerYbound, self.upperYbound

    def returnBoxbounds(self):
        self.lowerXbound = self.lowerYbound = 0
        self.upperXbound = self.A[0]
        self.upperYbound = self.B[1]
        return self.lowerXbound, self.upperXbound, self.lowerYbound, self.upperYbound

    def returnTriclinicbounds(self, z):
        self.lowerYbound = (z * self.C[1]) / self.C[2]
        self.upperYbound = ((self.B[1] * self.C[2]) + (z * self.C[1])) / self.C[2]
        self.lowerXbound = (((self.B[0] * self.C[2]) * self.lowerYbound) + (((self.C[0] * self.B[1]) - (self.B[0] * self.C[1])) * Z)) / (self.B[1] * self.C[2])
        self.upperXbound = (((self.B[0] * self.C[2]) * self.lowerYbound) + (((self.C[0] * self.B[1]) - (self.B[0] * self.C[1])) * z) - (self.A[0] * self.B[1] * self.C[2])) / (self.B[1] * self.C[2])
        return self.lowerXbound, self.upperXbound, self.lowerYbound, self.upperYbound

    def returnMonoclinicbounds(self,z):
        self.lowerXbound = 0
        self.upperXbound = self.A0B0
        self.lowerYbound = (self.C[1] * z) / self.C[2]
        self.upperYbound = ((self.C[2] * self.A1B1) + (self.C[1] * z)) / self.C[2]

        return self.lowerXbound, self.upperXbound, self.lowerYbound, self.upperYbound
