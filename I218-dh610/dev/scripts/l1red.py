import sys, time, pickle
import sympy as sp
from lin import *
E = pickle.load(open("l1_eqs.pkl", "rb"))
names = ["H0", "H1", "H2", "K"]
fn = {n: sp.Function(n)(rho) for n in names}
jet = {n: [sp.Symbol(f"{n}_{k}") for k in range(5)] for n in names}
As, A1 = sp.symbols("As A1")
def tojet(z):
    z = z.subs(L, 2).doit()
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
d1 = [jet[n][1] for n in names]
sol = sp.solve([J["tth"], J["tr"], J["rth"], J["S"]], d1, dict=True)
assert len(sol) == 1
sol = {k: sp.simplify(v) for k, v in sol[0].items()}
for k, v in sol.items():
    print(k, "=", sp.collect(sp.expand(v), [jet[n][0] for n in names]))
def red(z):
    z = z.subs({jet[n][2]: D(sol[jet[n][1]]) for n in names})
    z = z.subs(sol)
    return sp.simplify(z)
C = {k: sp.factor(red(J[k])) for k in ("tt", "rr", "ang_tr")}
for k, v in C.items():
    print("constraint from", k, ":", v)
pickle.dump((J, sol, C), open("l1red.pkl", "wb"))
