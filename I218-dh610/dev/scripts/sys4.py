import sys, time, pickle
import sympy as sp
from lin import *
exec(open("red.py").read().split("J = {k")[0].split("E = pickle")[1].split("\n",1)[1])
J, sol, Rd = pickle.load(open("red.pkl", "rb"))
alg = pickle.load(open("alg.pkl", "rb"))
F_1, F_2 = jet["F"][1], jet["F"][2]
H0_1, H1_1, K_1 = jet["H0"][1], jet["H1"][1], jet["K"][1]
Al = sp.numer(sp.together(alg["tt"]))
F1sol = sp.simplify(sp.solve(Al, F_1)[0])
print("F' =", sp.collect(sp.expand(F1sol), [jet[n][0] for n in names]))
# full first-order system
sysd = {H0_1: sol[H0_1], H1_1: sol[H1_1], K_1: sol[K_1], F_1: F1sol}
# consistency 1: D(F') = F'' from the scalar equation
F2S = sp.solve(Rd["S"], F_2)[0]
def sub_sys(z):
    z = z.subs({jet["H1"][1]: sysd[H1_1], jet["K"][1]: sysd[K_1], jet["H0"][1]: sysd[H0_1]}).subs(F_1, F1sol)
    return z
lhs = sub_sys(D(F1sol))
rhs = sub_sys(F2S)
print("consistency D(F') - F''(scalar eq):", sp.simplify(lhs - rhs))
# consistency 2: all of tt, rr, ang_tr, S hold on the 4-dim system (F'' from D(F'))
for k in ("tt", "rr", "ang_tr", "S"):
    z = J[k]
    z = z.subs({jet["H1"][2]: D(sysd[H1_1]), jet["K"][2]: D(sysd[K_1]), jet["H0"][2]: D(sysd[H0_1]), F_2: D(F1sol)})
    for _ in range(3):
        z = z.subs({jet["H1"][1]: sysd[H1_1], jet["K"][1]: sysd[K_1], jet["H0"][1]: sysd[H0_1], F_1: F1sol})
    print("residual of", k, "on the 4-system:", sp.simplify(z))
# the original 3 first-order equations hold by construction; also the unreduced tt with H0'' etc: done above (J[tt] has H0_2)
# matrix
Pi = sp.Symbol("Pi")
vars4 = [jet["H0"][0], jet["H1"][0], jet["K"][0], jet["F"][0]]
Mrows = []
for q in (H0_1, H1_1, K_1, F_1):
    e = sp.expand(sysd[q])
    Mrows.append([sp.simplify(e.coeff(v)) for v in vars4])
M = sp.Matrix(Mrows)
print("M (H0,H1,K,F) =")
sp.pprint(M)
pickle.dump((M, vars4, sysd), open("sys4.pkl", "wb"))
# in terms of Pi = H1/W
S = sp.diag(1, 1 / W, 1, 1)  # Phi = S Phi_new? H1 = W Pi : Phi = diag(1,W,1,1) Phi_new
T = sp.diag(1, W, 1, 1)
Mn = sp.simplify(T.inv() * M * T)
print("M for (H0,Pi,K,F):")
sp.pprint(Mn)
lam = sp.Symbol("lam")
Mn_l = Mn.subs(W, sp.sqrt(lam))
print("entries free of sqrt(lam)?", all(not e.has(sp.sqrt(lam)) for e in Mn_l))
pickle.dump((Mn_l, lam), open("sys4n.pkl", "wb"))
