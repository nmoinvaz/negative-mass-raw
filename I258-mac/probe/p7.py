# probe 7: largest c2 for bounded data (LP over a bump basis), both conditions imposed
import sys, math, numpy as np
sys.argv = [sys.argv[0]]
from p2 import *
from scipy.optimize import linprog
SL, SR = -1.05, 1.05
tol = dict(method="DOP853", rtol=1e-12, atol=1e-16)
cen = np.linspace(-0.75, 0.75, 7); wd = 0.3
def mkb(c, w):
    return (lambda s: bump((s-c)/w)), (lambda s: dbump((s-c)/w)/w)
def run_even(f, fT):
    return solve_ivp(lambda s, y: rhs_even(s, y, f, fT), [SL, SR], [0.0, 0.0], dense_output=True, max_step=0.01, **tol)
def run_odd(f):
    return solve_ivp(lambda s, y: rhs_odd(s, y, f), [SL, SR], [0.0], dense_output=True, max_step=0.01, **tol)
E = [run_even(*mkb(c, wd)) for c in cen]; O = [run_odd(mkb(c, wd)[0]) for c in cen]
Aend = np.array([e.y[0, -1] for e in E]); Cend = np.array([o.y[0, -1] for o in O])
drT0 = np.array([e.sol(0.0)[1] for e in E]); n0 = np.array([o.sol(0.0)[0] for o in O])
sk = np.linspace(-1, 1, 81)
Fm = np.array([[bump((s-c)/wd) for c in cen] for s in sk])   # samples of basis
N = len(cen)
# variables: a (N) for dphi, b (N) for dphiN ; maximize 0.5*(drT0.a + n0.b)
cobj = -0.5 * np.concatenate([drT0, n0])
Aeq = np.zeros((2, 2*N)); Aeq[0, :N] = Aend; Aeq[1, N:] = Cend
Aub = np.vstack([np.hstack([Fm, np.zeros_like(Fm)]), np.hstack([-Fm, np.zeros_like(Fm)]), np.hstack([np.zeros_like(Fm), Fm]), np.hstack([np.zeros_like(Fm), -Fm])])
bub = 1e-3 * np.ones(Aub.shape[0])
res = linprog(cobj, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=np.zeros(2), bounds=[(None, None)]*(2*N))
print(res.status, "c2_max =", -res.fun, " even part", 0.5*drT0@res.x[:N], " odd part", 0.5*n0@res.x[N:])
print("a", res.x[:N], "b", res.x[N:])
# without the conditions
res2 = linprog(cobj, A_ub=Aub, b_ub=bub, bounds=[(None, None)]*(2*N))
print("without conditions c2_max =", -res2.fun)
