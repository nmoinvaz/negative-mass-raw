"""dev numerics: radial modes of the black-universe family (b = 1), master equation in the gauge dphi = 0.
   Y'' = (2/rho - A'/A) Y' + [1/R^4 - A'/(A rho R^2) - 2/(A R^2)] Y + W^2 Y / A^2        (rho-form)
   x-form (dx = d rho / A):  Y_xx = (2A/rho) Y_x + [A^2/R^4 - A A'/(rho R^2) - 2A/R^2] Y + W^2 Y
"""
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
import mpmath as mp

class Fam:
    def __init__(self, c, epsflip=False, rtol=1e-12, atol=1e-14, z0=1e-13, rmax=None, delta=0.3):
        self.c = c; self.K = -2*c/np.pi
        self.eps = +1 if epsflip else -1
        self.rtol, self.atol, self.z0, self.delta = rtol, atol, z0, delta
        self.rmax = rmax
        if c < 0:
            self.rh = brentq(self.A, -1e4 if c > -1e-6 else -1e3, self.K + 5) if c != -1 else 0.0
            # robust: bracket search
            self.rh = self._horizon()
            self.A1 = float(self.Ap(self.rh))
        else:
            self.rh = None; self.A1 = None
    def _horizon(self):
        if self.c == -1: return 0.0
        lo = -1.0; 
        while self.A(lo) > 0: lo *= 2
        hi = self.K + 1.0
        return brentq(self.A, lo, hi, xtol=1e-15, rtol=1e-15)
    def A(self, r):
        c, K = self.c, self.K
        return 1 + c*(r*r + 1) + K*(r + (r*r + 1)*np.arctan(r))
    def Ap(self, r):
        return 2*self.c*r + 2*self.K*(1 + r*np.arctan(r))
    def a_over_z(self, z):
        """A(rh+z)/z, series for small z"""
        rh = self.rh
        if abs(z) < 1e-3:
            # A = A1 z + A2/2 z^2 + A3/6 z^3 ; derivatives at rh
            K, c = self.K, self.c
            A1 = self.A1
            A2 = 2*c + 2*K*(np.arctan(rh) + rh/(1 + rh*rh))
            A3 = 2*K*(2/(1 + rh*rh)**2)
            return A1 + A2*z/2 + A3*z*z/6
        return self.A(rh + z)/z

def rhs_x(fam, W):
    K, c = fam.K, fam.c
    def f(x, s):   # state (rho, Y, Yx)
        r, Y, Yx = s
        A = fam.A(r); Ap = fam.Ap(r); R2 = r*r + 1
        Ar = A/r
        return [A, Yx, 2*Ar*Yx + (A*A/R2**2 - A*Ap/(r*R2) - 2*A/R2)*Y + W*W*Y]
    return f

def rhs_zeta(fam, W):
    def f(x, s):   # state (zeta = ln z, Y, Yx)
        zeta, Y, Yx = s
        z = np.exp(zeta); r = fam.rh + z
        at = fam.a_over_z(z); A = z*at; Ap = fam.Ap(r); R2 = r*r + 1
        Ar = at if fam.rh == 0.0 else A/r
        # A*Ap/(r R2) : A/r = Ar
        return [at, Yx, 2*Ar*Yx + (A*A/R2**2 - Ar*Ap/R2 - 2*A/R2)*Y + W*W*Y]
    return f

def rhs_rho_complex(fam, W):
    def f(th, s, r0, sgn):
        Y, Yr = s
        r = r0*np.exp(1j*th)
        A = fam.A(r); Ap = fam.Ap(r); R2 = r*r + 1
        Yrr = (2/r - Ap/A)*Yr + (1/R2**2 - Ap/(A*r*R2) - 2/(A*R2))*Y + W*W*Y/A**2
        return [1j*r*Yr, 1j*r*Yrr]
    return f

def Vhat(fam, r):
    A = fam.A(r); Ap = fam.Ap(r); R2 = r*r + 1
    return 2*A*A/r**2 - (1 + 1/R2)*A*Ap/r + A*A/R2**2 - 2*A/R2
