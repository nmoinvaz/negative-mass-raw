import sys, math, numpy as np
sys.argv = [sys.argv[0]]
from p2 import *
SL, SR = -1.05, 1.05
centers = [-0.6, -0.3, 0.0, 0.3, 0.6]; wid = 0.4
def mk(c, w):
    f  = lambda s: bump((s-c)/w)
    fT = lambda s: dbump((s-c)/w)/w
    return f, fT
tol = dict(method="DOP853", rtol=1e-12, atol=1e-16)
def solve_even(dphi, dphiT, y0=(0.0, 0.0), pts=None):
    sol = solve_ivp(lambda s, y: rhs_even(s, y, dphi, dphiT), [SL, SR], list(y0), dense_output=True, max_step=0.01, **tol)
    return sol
def solve_odd(dphiN, n0=0.0):
    sol = solve_ivp(lambda s, y: rhs_odd(s, y, dphiN), [SL, SR], [n0], dense_output=True, max_step=0.01, **tol)
    return sol
# functionals: end values (delta r, delta r') at SR for each even basis function; (n) at SR for odd basis
AB = []; dr0 = []; dr0T = []
for c in centers:
    f, fT = mk(c, wid)
    sol = solve_even(f, fT)
    AB.append(sol.y[:, -1]); dr0.append(sol.sol(0.0)[0]); dr0T.append(sol.sol(0.0)[1])
AB = np.array(AB).T          # 2 x N
C = []; n0 = []
for c in centers:
    f, fT = mk(c, wid)
    sol = solve_odd(f)
    C.append(sol.y[0, -1]); n0.append(sol.sol(0.0)[0])
C = np.array(C)
print("even end values (A,B) per basis:\n", AB)
print("delta r'(0) per basis:", np.array(dr0T))
print("odd end value per basis:", C, " n(0):", np.array(n0))
# compact even solutions: null space of AB (2 x 5) -> 3-dim; c2_even = 0.5*dr'(0)
u, sv, vt = np.linalg.svd(AB)
ns = vt[2:].T
print("null space dim", ns.shape[1], " singular values", sv)
print("dr'(0) over null space:", np.array(dr0T) @ ns)
nso = np.linalg.svd(C.reshape(1, -1))[2][1:].T
print("n(0) over odd null space:", np.array(n0) @ nso)
