import sys, time, pickle
import sympy as sp
from lin import *
T0 = time.time()
E = pickle.load(open("rw_eqs.pkl", "rb"))
names = ["H0", "H1", "K", "F"]
fn = {n: sp.Function(n)(rho) for n in names}
H2 = sp.Function("H2")(rho)
jet = {n: [sp.Symbol(f"{n}_{k}") for k in range(5)] for n in names}
As, A1 = sp.symbols("As A1")

def tojet(z):
    z = z.subs(H2, fn["H0"])
    z = z.doit()
    for n in names:
        for k in (4, 3, 2, 1):
            z = z.subs(sp.diff(fn[n], rho, k), jet[n][k])
        z = z.subs(fn[n], jet[n][0])
    z = z.subs(sp.diff(A, rho), A1).subs(A, As)
    return z

def D(z):
    out = sp.diff(z, rho)
    for n in names:
        for k in range(4):
            out += sp.diff(z, jet[n][k]) * jet[n][k + 1]
    out += sp.diff(z, As) * A1 + sp.diff(z, A1) * 2 * (As - 1) / R2
    return out

J = {k: sp.simplify(tojet(v)) for k, v in E.items()}
for k, v in J.items():
    print(k, "->", v)
H0_1, H1_1, K_1 = jet["H0"][1], jet["H1"][1], jet["K"][1]
F_1, F_2 = jet["F"][1], jet["F"][2]
sol = sp.solve([J["tth"], J["tr"], J["rth"]], [H1_1, K_1, H0_1], dict=True)
assert len(sol) == 1
sol = {k: sp.simplify(v) for k, v in sol[0].items()}
print("first-order system:")
for k, v in sol.items():
    print(" ", k, "=", sp.collect(sp.expand(v), [jet[n][0] for n in names]))
def sub1(z, extra=None):
    # substitute second derivatives then first derivatives
    z = z.subs({jet["H1"][2]: D(sol[H1_1]), jet["K"][2]: D(sol[K_1]), jet["H0"][2]: D(sol[H0_1])})
    z = z.subs(sol)
    return sp.simplify(z)
# D(sol) contains first jets of H0,H1,K which are then substituted by sol
def subs_all(z):
    z = z.subs({jet["H1"][2]: D(sol[H1_1]), jet["K"][2]: D(sol[K_1]), jet["H0"][2]: D(sol[H0_1])})
    z = z.subs(sol)
    return sp.simplify(z)
R = {}
for k in ("tt", "rr", "ang_tr", "S"):
    R[k] = subs_all(J[k])
    print(k, "after first-order elimination: has F2?", R[k].has(F_2), "has F1?", R[k].has(F_1), "%.0fs" % (time.time() - T0), flush=True)
pickle.dump((J, sol, R), open("red.pkl", "wb"))
