# prototype of the slice construction (probe only, not the script of record)
import sys, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i258/notes/black_universe")
_argv = sys.argv; sys.argv = [sys.argv[0]]
import horizon_sector as hs
import linear as lin
from scipy.integrate import solve_ivp
sys.argv = _argv
EPS = -1.0
_KC = {}
def kchart(c=-1.0):
    if c not in _KC:
        _KC[c] = hs.KChart(c, pi_max=1e12)
    return _KC[c]

class Bg:
    def __init__(self, c=-1.0): self.kc = kchart(c); self.par = self.kc.par; self.tab = self.kc.tab
    def at(self, s):
        a = max(abs(s), 1e-8)
        x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = hs.jetsK(a, -a, self.par, self.tab, 0.0)
        return dict(rho=x, r=r, rp=rV/a, php=pV/a, Fp=FV/a, E=E, V0=V0, V1=V1)

def bump(x):
    return math.e * math.exp(-1.0/(1.0-x*x)) if abs(x) < 1 else 0.0
def dbump(x):
    return bump(x) * (-2.0*x/(1.0-x*x)**2) if abs(x) < 1 else 0.0
def ddbump(x):
    if abs(x) >= 1: return 0.0
    u = 1.0 - x*x
    return bump(x) * ((2.0*x/u**2)**2 - 2.0/u**2 - 8.0*x*x/u**3)

class Data:
    """sum of amp * bump((s - c)/w); parts: list of (amp, c, w)"""
    def __init__(self, parts): self.parts = parts
    def f(self, s):   return sum(a*bump((s-c)/w) for a, c, w in self.parts)
    def fT(self, s):  return sum(a*dbump((s-c)/w)/w for a, c, w in self.parts)
    def fTT(self, s): return sum(a*ddbump((s-c)/w)/w**2 for a, c, w in self.parts)
    def __add__(self, o): return Data(self.parts + o.parts)
    def scaled(self, k): return Data([(a*k, c, w) for a, c, w in self.parts])

class Slice:
    """constraint ODEs on the slice V + U = 0 in the gauge dF = dF_N = 0 (optionally with dF sources); mutations by name"""
    def __init__(self, bg, mut=None): self.bg = bg; self.mut = mut
    def PQ(self, s):
        b = self.bg.at(s); m = self.mut
        P = s*b['Fp'] + (0.0 if m == 'H_P' else 2*s*b['rp']/b['r'])
        Q = b['E']*b['V0'] + b['E']/b['r']**2 - 2*s*s*b['rp']**2/b['r']**2 + (-1 if m == 'H_eps' else 1)*EPS*s*s*b['php']**2
        return P, Q, b
    def rhs_even(self, s, y, dphi, dphiT, dF=0.0, dFT=0.0):
        P, Q, b = self.PQ(s)
        S = -(b['E']*b['V1']*b['r']*dphi + EPS*b['r']*s*b['php']*dphiT) - (b['E']*(1/b['r'] - b['V0']*b['r'])*dF + s*b['rp']*dFT)
        return [y[1], S - P*y[1] - Q*y[0]]
    def rhs_odd(self, s, n, dphiN, dFN=0.0):
        b = self.bg.at(s); m = self.mut
        return -(-1 if m == 'M_F' else 1)*s*b['Fp']*n - s*b['rp']*dFN - (-1 if m == 'M_phi' else 1)*EPS*b['r']*s*b['php']*dphiN
    def even(self, a, b_, dphi, dphiT, y0, **kw):
        return solve_ivp(lambda s, y: self.rhs_even(s, y, dphi(s), dphiT(s)), [a, b_], list(y0), dense_output=True, method="DOP853", rtol=1e-12, atol=1e-18, **kw)
    def odd(self, a, b_, dphiN, n0, **kw):
        return solve_ivp(lambda s, y: [self.rhs_odd(s, y[0], dphiN(s))], [a, b_], [n0], dense_output=True, method="DOP853", rtol=1e-12, atol=1e-18, **kw)

def dm_of(bg, s, dr, drT, dF=0.0):
    b = bg.at(s); eF = 1.0/b['E']
    return dr*(0.5 - eF*s*s*b['rp']**2) - b['r']*eF*s*b['rp']*(s*b['rp']*dF + drT)

import numba as nb
@nb.njit(cache=True)
def march_diag_full(L0, L1, J, h, par, tab):
    """L0[q, j] at node (j, -j), j = 0..J; L1[q, j] at node (j, 1-j), j = 1..J. Returns Ua[q, j, i + J], i = -J..1 (nodes with i <= 0 filled for j + i >= 0)."""
    Ua = np.zeros((3, J + 1, J + 2))
    for q in range(3):
        for j in range(J + 1):
            Ua[q, j, -j + J] = L0[q, j]
        for j in range(1, J + 1):
            Ua[q, j, 1 - j + J] = L1[q, j]
    B0 = np.zeros((3, 3)); Bp = np.zeros((3, 3)); Bm = np.zeros((3, 3)); M = np.zeros((3, 3))
    rhs = np.zeros(3); out = np.zeros(3); Sv = np.zeros(3); Ev = np.zeros(3); Wv = np.zeros(3)
    for l in range(2, J + 1):
        guess = 0.0
        for j in range(l, J + 1):
            i = l - j
            for q in range(3):
                Sv[q] = Ua[q, j - 1, i - 1 + J]; Ev[q] = Ua[q, j, i - 1 + J]; Wv[q] = Ua[q, j - 1, i + J]
            guess = hs._cellK(Sv, Ev, Wv, (j - 1) * h, (i - 1) * h, h, h, par, tab, guess, B0, Bp, Bm, M, rhs, out)
            for q in range(3):
                Ua[q, j, i + J] = out[q]
    return Ua

def layers_from_slice(bg, h, J, fn, mut=None):
    """fn(s) -> (U, UT, UN, UTT): 3-vectors of the slice data at s. L0 at s = j h; L1 = U + (h/2) U_N + (h^2/8) U_NN at s = (j - 1/2) h."""
    B0 = np.zeros((3, 3)); Bp = np.zeros((3, 3)); Bm = np.zeros((3, 3))
    L0 = np.zeros((3, J + 1)); L1 = np.zeros((3, J + 1))
    for j in range(J + 1):
        L0[:, j] = fn(j * h)[0]
    for j in range(1, J + 1):
        s = (j - 0.5) * h
        U, UT, UN, UTT = fn(s)
        hs.coefK(s, -s, bg.par, bg.tab, 0.0, B0, Bp, Bm)
        UV = 0.5 * (UT + UN); UU = 0.5 * (UN - UT)
        UNN = UTT + 4.0 * (B0 @ U + Bp @ UV + Bm @ UU)
        sgn = -1.0 if mut == 'l1_sign' else 1.0
        quad = 0.0 if mut == 'l1_noquad' else 1.0
        L1[:, j] = U + sgn * 0.5 * h * UN + quad * h * h / 8.0 * UNN
    return L0, L1

def slice_fn_compact(sl, solE, solO, dphi, dphiN):
    bg = sl.bg
    def fn(s):
        if abs(s) > 1.05:          # beyond the integration interval the solution is zero (compact support); no extrapolation of the dense output
            return np.zeros(3), np.zeros(3), np.zeros(3), np.zeros(3)
        dr, drT = solE.sol(s); n = solO.sol(s)[0]
        P, Q, b = sl.PQ(s)
        S = -(b['E']*b['V1']*b['r']*dphi.f(s) + EPS*b['r']*s*b['php']*dphi.fT(s))
        drTT = S - P*drT - Q*dr
        U = np.array([dr, 0.0, dphi.f(s)]); UT = np.array([drT, 0.0, dphi.fT(s)])
        UN = np.array([n, 0.0, dphiN.f(s)]); UTT = np.array([drTT, 0.0, dphi.fTT(s)])
        return U, UT, UN, UTT
    return fn

@nb.njit(cache=True)
def march_diamond(L0, L1, J, h, par, tab):
    """Full diamond over the slice nodes j = -J..J. L0[q, j + J] at (j, -j); L1[q, j + J] at (j, 1 - j), j = 1 - J..J. Returns Ua[q, j + J, i + J] (i, j in -J..J)."""
    n = 2 * J + 1
    Ua = np.zeros((3, n, n))
    for q in range(3):
        for j in range(-J, J + 1):
            Ua[q, j + J, -j + J] = L0[q, j + J]
        for j in range(1 - J, J + 1):
            Ua[q, j + J, 1 - j + J] = L1[q, j + J]
    B0 = np.zeros((3, 3)); Bp = np.zeros((3, 3)); Bm = np.zeros((3, 3)); M = np.zeros((3, 3))
    rhs = np.zeros(3); out = np.zeros(3); Sv = np.zeros(3); Ev = np.zeros(3); Wv = np.zeros(3)
    for l in range(2, 2 * J + 1):
        guess = 0.0
        for j in range(l - J, J + 1):
            i = l - j
            for q in range(3):
                Sv[q] = Ua[q, j - 1 + J, i - 1 + J]; Ev[q] = Ua[q, j + J, i - 1 + J]; Wv[q] = Ua[q, j - 1 + J, i + J]
            guess = hs._cellK(Sv, Ev, Wv, (j - 1) * h, (i - 1) * h, h, h, par, tab, guess, B0, Bp, Bm, M, rhs, out)
            for q in range(3):
                Ua[q, j + J, i + J] = out[q]
    return Ua

def layers_diamond(bg, h, J, fn, mut=None):
    B0 = np.zeros((3, 3)); Bp = np.zeros((3, 3)); Bm = np.zeros((3, 3))
    n = 2 * J + 1
    L0 = np.zeros((3, n)); L1 = np.zeros((3, n))
    for j in range(-J, J + 1):
        L0[:, j + J] = fn(j * h)[0]
    for j in range(1 - J, J + 1):
        s = (j - 0.5) * h
        U, UT, UN, UTT = fn(s)
        hs.coefK(s, -s, bg.par, bg.tab, 0.0, B0, Bp, Bm)
        UV = 0.5 * (UT + UN); UU = 0.5 * (UN - UT)
        UNN = UTT + 4.0 * (B0 @ U + Bp @ UV + Bm @ UU)
        L1[:, j + J] = U + 0.5 * h * UN + h * h / 8.0 * UNN
    return L0, L1

def fd_slice_fn(kc_bg, gauge_fn, hfd=1e-3):
    """exact slice data of a pure-gauge solution: gauge_fn(V, U) -> 3-vector; derivatives by 4th-order differences (step hfd)"""
    def f(s, a, b): return gauge_fn(s + a, -s + b)
    def fn(s):
        U0 = f(s, 0, 0)
        def d1(dV, dU):
            v = [f(s, m*hfd*dV, m*hfd*dU) for m in (-2, -1, 1, 2)]
            return (v[0] - 8*v[1] + 8*v[2] - v[3]) / (12*hfd)
        UT = d1(1, -1); UN = d1(1, 1)
        v = [f(s, m*hfd, -m*hfd) for m in (-2, -1, 0, 1, 2)]
        UTT = (-v[0] + 16*v[1] - 30*v[2] + 16*v[3] - v[4]) / (12*hfd**2)
        return U0, UT, UN, UTT
    return fn
