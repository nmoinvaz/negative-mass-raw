# shared development helpers (numpy floats); development only
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

def arccot(x):
    return np.arctan2(1.0, x)

class Fam:
    def __init__(s, c, beta):
        s.c, s.beta = c, beta
        s.K = -2*c/np.pi
        s.vs = -np.log(-beta)/s.K if beta < 0 else np.inf
    def A(s, r):
        return 1 + s.K*r - s.K*(1 + r*r)*arccot(r)
    def Ap(s, r):
        return 2*s.K*(1 - r*arccot(r))
    def sv(s, v):
        return s.beta*np.exp(s.K*v) if s.beta > 0 else -np.exp(s.K*(v - s.vs))
    def lam2(s, v):
        return 1 + s.beta*np.exp(s.K*v) if s.beta > 0 else -np.expm1(s.K*(v - s.vs))
    def sfrac(s, v):           # s/(1+s)
        if s.beta > 0:
            S = s.sv(v); return 1/(1 + 1/S)
        x = s.K*(v - s.vs); return np.exp(x)/np.expm1(x)
    def F(s, v, r):
        return s.A(r) - s.sfrac(v)*(1 + s.K*r)
    def P(s, v, r):
        return r*s.A(r) + s.sv(v)*(1 + r*r)*s.Ap(r)/2
    def grad2(s, v, r):
        return r/(1 + r*r)*s.P(v, r)
    def vstar(s):
        return s.vs
    def sAH(s, r):
        return -2*r*s.A(r)/((1 + r*r)*s.Ap(r))
    def rhoh(s):
        return brentq(s.A, 0.0, 10) if s.c < -1 else (0.0 if s.c == -1 else brentq(s.A, -10, 0))

WMAX = np.pi/2 - 1e-9
def ray(fam, v0, r0, vend=None, rtol=1e-11):
    """outgoing null ray drho/dv = F/2 forward from (v0, r0); integrates w = arctan(rho). Stops at |w| >= WMAX or v = vend."""
    if vend is None:
        vend = fam.vs - 1e-12 if fam.beta < 0 else v0 + 60
    def rhs(v, y):
        r = np.tan(y[0])
        return [fam.F(v, r)*np.cos(y[0])**2/2]
    e1 = lambda v, y: y[0] - WMAX
    e2 = lambda v, y: y[0] + WMAX
    e1.terminal = e2.terminal = True
    return solve_ivp(rhs, (v0, vend), [np.arctan(r0)], events=[e1, e2], rtol=rtol, atol=1e-14, method="DOP853")
