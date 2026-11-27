import sys, time, pickle
import sympy as sp
from lin import *
E = pickle.load(open("l1h_eqs.pkl", "rb"))
names = ["H0", "H2", "F"]
fn = {n: sp.Function(n)(rho) for n in names}
Kf = sp.Function("K")(rho)
jet = {n: [sp.Symbol(f"{n}_{k}") for k in range(5)] for n in names}
As, A1 = sp.symbols("As A1")
def tojet(z):
    z = z.subs(L, 2).subs(Kf, -fn["H2"]).doit()
    for n in names:
        for k in (4, 3, 2, 1):
            z = z.subs(sp.diff(fn[n], rho, k), jet[n][k])
        z = z.subs(fn[n], jet[n][0])
    return z.subs(sp.diff(A, rho), A1).subs(A, As)
def D(z):
    out = sp.diff(z, rho)
    for n in names:
        for k in range(4):
            out += sp.diff(z, jet[n][k]) * jet[n][k + 1]
    return out + sp.diff(z, As) * A1 + sp.diff(z, A1) * 2 * (As - 1) / R2
J = {k: sp.simplify(tojet(v)) for k, v in E.items()}
for k, v in J.items():
    print(k, "->", sp.factor(v))
H0_1, H2_1 = jet["H0"][1], jet["H2"][1]
sol = sp.solve([J["tr"], J["rth"]], [H2_1, H0_1], dict=True)
assert len(sol) == 1
sol = {k: sp.simplify(v) for k, v in sol[0].items()}
for k, v in sol.items(): print(k, "=", v)
def red(z):
    z = z.subs({jet["H0"][2]: D(sol[H0_1]), jet["H2"][2]: D(sol[H2_1])})
    z = z.subs(sol)
    return sp.simplify(z)
C = {k: sp.factor(red(J[k])) for k in ("tt", "rr", "ang_tr", "S")}
for k, v in C.items(): print("after first-order elimination", k, ":", v)
pickle.dump((J, sol, C), open("l1hred.pkl", "wb"))
