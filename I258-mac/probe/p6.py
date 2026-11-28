# probe 6: data supported away from S (two bump groups |s| in [0.6,1.0]) with both end conditions; c2 and the solution at S
import sys, math, numpy as np
sys.argv = [sys.argv[0]]
from p2 import *
SL, SR = -1.05, 1.05
tol = dict(method="DOP853", rtol=1e-12, atol=1e-16)
cen = [-0.8, 0.8]; wd = 0.2
def mkb(c, w):
    return (lambda s: bump((s-c)/w)), (lambda s: dbump((s-c)/w)/w)
def run_even(f, fT):
    return solve_ivp(lambda s, y: rhs_even(s, y, f, fT), [SL, SR], [0.0, 0.0], dense_output=True, max_step=0.01, **tol)
def run_odd(f):
    return solve_ivp(lambda s, y: rhs_odd(s, y, f), [SL, SR], [0.0], dense_output=True, max_step=0.01, **tol)
E = [run_even(*mkb(c, wd)) for c in cen]; O = [run_odd(mkb(c, wd)[0]) for c in cen]
Aend = np.array([e.y[0, -1] for e in E]); Bend = np.array([e.y[1, -1] for e in E]); Cend = np.array([o.y[0, -1] for o in O])
print("even end A", Aend, "B", Bend, "odd end", Cend)
# conditions: one mass-like condition -> a = (Aend[1], -Aend[0]) ; odd: b = (Cend[1], -Cend[0])
a = np.array([Aend[1], -Aend[0]]); a = 1e-3 * a / np.max(np.abs(a))
b = np.array([Cend[1], -Cend[0]]); b = 1e-3 * b / np.max(np.abs(b))
dr0 = sum(ai * e.sol(0.0)[0] for ai, e in zip(a, E)); drT0 = sum(ai * e.sol(0.0)[1] for ai, e in zip(a, E))
n0 = sum(bi * o.sol(0.0)[0] for bi, o in zip(b, O))
print("a", a, "b", b)
print("even: end", sum(ai*e.y[:, -1] for ai, e in zip(a, E)), " dr(0), dr'(0)=", dr0, drT0, " odd: end", sum(bi*o.y[0, -1] for bi, o in zip(b, O)), " n(0)=", n0)
print("c2 slice =", 0.5*(drT0 + n0))
