# probe 2: slice constraint ODEs in the gauge dF = dF_N = 0 at c = -1; hom solutions; compact solutions
import sys, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i258/notes/black_universe")
sys.argv = [sys.argv[0]]
import horizon_sector as hs
from scipy.integrate import solve_ivp
kc = hs.KChart(-1.0)
par, tab = kc.par, kc.tab
eps = -1.0
kap = kc.kappa

def bgs(s):
    a = max(abs(s), 1e-8)
    x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = hs.jetsK(a, -a, par, tab, 0.0)
    return dict(rho=x, r=r, rp=rV/a, php=pV/a, Fp=FV/a, E=E, V0=V0, V1=V1)

def coeffs(s):
    b = bgs(s)
    P = s*b['Fp'] + 2*s*b['rp']/b['r']
    Q = b['E']*b['V0'] + b['E']/b['r']**2 - 2*s*s*b['rp']**2/b['r']**2 + eps*s*s*b['php']**2
    return P, Q, b

def bump(x):
    return math.exp(-1.0/(1.0-x*x)) if abs(x) < 1 else 0.0
def dbump(x):
    return bump(x) * (-2.0*x/(1.0-x*x)**2) if abs(x) < 1 else 0.0

def rhs_even(s, y, dphi, dphiT):
    P, Q, b = coeffs(s)
    S = -(b['E']*b['V1']*b['r']*dphi(s) + eps*b['r']*s*b['php']*dphiT(s))
    return [y[1], S - P*y[1] - Q*y[0]]

def rhs_odd(s, y, dphiN):
    P, Q, b = coeffs(s)
    return [-s*b['Fp']*y[0] - eps*b['r']*s*b['php']*dphiN(s)]

if __name__ == "__main__":
    # hom even solutions from s=-2 : two basis; evaluate at s=+2 and growth far out
    for s in (0.0, 0.5, 1.0, 3.0, 10.0, 100.0, 1e4):
        P, Q, b = coeffs(s)
        print(f"s={s:g} rho={b['rho']:.4g} P={P:.4g} Q={Q:.4g} E={b['E']:.4g} Fp={b['Fp']:.4g} rp={b['rp']:.4g}")
