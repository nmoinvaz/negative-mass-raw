import sys, time, pickle
import sympy as sp
from lin import *
exec(open("l1hred.py").read().split("J = {k")[0].split("E = pickle")[1].split("\n",1)[1])
J, sol, C = pickle.load(open("l1hred.pkl", "rb"))
H0_1, H2_1, F_1, F_2 = jet["H0"][1], jet["H2"][1], jet["F"][1], jet["F"][2]
Al = sp.numer(sp.together(C["tt"]))
F1sol = sp.simplify(sp.solve(Al, F_1)[0])
sysd = {H0_1: sol[H0_1], H2_1: sol[H2_1], F_1: F1sol}
F2S = sp.solve(C["S"], F_2)[0]
def sub_sys(z):
    return z.subs({H0_1: sysd[H0_1], H2_1: sysd[H2_1]}).subs(F_1, F1sol)
print("consistency D(F') - F''(S):", sp.simplify(sub_sys(D(F1sol)) - sub_sys(F2S)))
for k in ("tt", "rr", "ang_tr", "S"):
    z = J[k]
    z = z.subs({jet["H0"][2]: D(sysd[H0_1]), jet["H2"][2]: D(sysd[H2_1]), F_2: D(F1sol)})
    for _ in range(3):
        z = z.subs({H0_1: sysd[H0_1], H2_1: sysd[H2_1], F_1: F1sol})
    print("residual", k, sp.simplify(z))
vars3 = [jet["H0"][0], jet["H2"][0], jet["F"][0]]
M3 = sp.Matrix([[sp.simplify(sp.expand(sysd[q]).coeff(v)) for v in vars3] for q in (H0_1, H2_1, F_1)])
print("M3 (H0, H2, F):"); sp.pprint(M3)
# gauge solution: xi^theta = c = sqrt(A)/R, xi^rho = -A R^2 c', xi^t = R^2 W c / A
Afun = A; c = sp.sqrt(Afun) / sp.sqrt(R2)
xr = -Afun * R2 * sp.diff(c, rho)
xt = R2 * W * c / Afun
# fields from Lie derivative: h_tt = -2 A W xi^t + xi^rho d_rho g_tt ; h_rr = 2 (xi^rho)'/A - xi^rho A'/A^2 ; K = -2c (l=1: Y''=-Y); F = xr * phi0'
htt = -2 * Afun * W * xt + xr * sp.diff(-Afun, rho)
hrr = 2 * sp.diff(xr, rho) / Afun + xr * sp.diff(1 / Afun, rho)
H0g = htt / Afun; H2g = hrr * Afun; Kg = -2 * c; Fg = xr * sp.sqrt(2) / R2
# check h_tr = 0 and K = -H2 (gauge H1 = 0 requires K = -H2)
htr = -Afun * sp.diff(xt, rho) + W * xr / Afun
def toS(z):
    z = z.doit()
    z = z.subs(sp.diff(Afun, rho, 3), sp.diff(2 * (Afun - 1) / R2, rho, 1)).subs(sp.diff(Afun, rho, 2), 2 * (Afun - 1) / R2)
    z = z.subs(sp.diff(Afun, rho), A1).subs(Afun, As)
    return sp.simplify(z)
g = [toS(H0g), toS(H2g), toS(Fg)]
print("gauge: h_tr =", toS(htr), "; K + H2 =", toS(Kg + H2g))
print("gauge solution:", g)
gv = sp.Matrix(g)
Dv = lambda z: sp.diff(z, rho) + sp.diff(z, As) * A1 + sp.diff(z, A1) * 2 * (As - 1) / R2
res = (gv.applyfunc(Dv) - M3 * gv).applyfunc(sp.simplify)
print("gauge solution residual:", res.T)
pickle.dump((M3, gv, vars3), open("l1h3.pkl", "wb"))
