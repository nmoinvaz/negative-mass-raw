import sys, time, pickle
import sympy as sp
from lin import *
exec(open("l1red.py").read().split("J = {k")[0].split("E = pickle")[1].split("\n",1)[1])
J, sol, C = pickle.load(open("l1red.pkl", "rb"))
Al = sp.numer(sp.together(C["tt"]))
H2_0 = jet["H2"][0]
H2sol = sp.simplify(sp.solve(Al, H2_0)[0])
print("H2 =", H2sol)
H0_, H1_, K_ = jet["H0"][0], jet["H1"][0], jet["K"][0]
# 3-dim system with H2 eliminated
sys3 = {q: sp.simplify(sol[jet[n][1]].subs(H2_0, H2sol)) for q, n in ((0, "H0"), (1, "H1"), (3, "K"))}
dH0, dH1, dK = sys3[0], sys3[1], sys3[3]
# propagation of the constraint: D(H2 - H2sol) on the system
H2p = sol[jet["H2"][1]]
prop = sp.simplify(((H2p - D(H2sol)).subs({jet["H0"][1]: sol[jet["H0"][1]], jet["H1"][1]: sol[jet["H1"][1]], jet["K"][1]: sol[jet["K"][1]], jet["H2"][1]: sol[jet["H2"][1]]})).subs(H2_0, H2sol))
print("constraint propagation (H2' - D(H2sol)) on the constraint surface:", prop)
# gauge solution
Wg = W; Rg2 = R2
vg = {H0_: -2 * Rg2 * W**2 / As, H1_: -W * (2 * rho - Rg2 * A1 / As), K_: -2}
# check the gauge solution solves the 3-system: v' = M v, where v(rho) explicit with A -> As jets
def Dv(expr):  # total derivative of expressions in rho, As, A1
    return sp.diff(expr, rho) + sp.diff(expr, As) * A1 + sp.diff(expr, A1) * 2 * (As - 1) / R2
for q, sym in ((0, H0_), (1, H1_), (3, K_)):
    lhs = Dv(vg[sym])
    rhs = sys3[q].subs({H0_: vg[H0_], H1_: vg[H1_], K_: vg[K_]})
    print("gauge solution residual for", sym, ":", sp.simplify(lhs - rhs))
# invariants
I1 = H0_ - (Rg2 * W**2 / As) * K_
I2 = H1_ - (W * (2 * rho - Rg2 * A1 / As) / 2) * K_
def dI(I):
    z = D_total = sp.diff(I, rho) + sp.diff(I, As) * A1 + sp.diff(I, A1) * 2 * (As - 1) / R2
    z += sp.diff(I, H0_) * dH0 + sp.diff(I, H1_) * dH1 + sp.diff(I, K_) * dK
    return sp.simplify(z)
dI1, dI2 = dI(I1), dI(I2)
# express through I1, I2: K should drop out; H0 = I1 + (R2 W^2/As) K, H1 = I2 + ...
q1, q2 = sp.symbols("q1 q2")
rep = {H0_: q1 + (Rg2 * W**2 / As) * K_, H1_: q2 + (W * (2 * rho - Rg2 * A1 / As) / 2) * K_}
dI1q = sp.simplify(dI1.subs(rep)); dI2q = sp.simplify(dI2.subs(rep))
print("K drops out of I1', I2'? ", not dI1q.has(K_), not dI2q.has(K_))
N = sp.Matrix([[sp.simplify(sp.diff(dI1q, q1)), sp.simplify(sp.diff(dI1q, q2))], [sp.simplify(sp.diff(dI2q, q1)), sp.simplify(sp.diff(dI2q, q2))]])
sp.pprint(N)
Tm = sp.diag(1, W)
Nn = sp.simplify(Tm.inv() * N * Tm)
print("scaled (I1, I2/W):")
sp.pprint(Nn)
lam = sp.Symbol("lam")
print("sqrt-free in lam:", all(not e.has(sp.sqrt(lam)) for e in Nn.subs(W, sp.sqrt(lam))))
pickle.dump((Nn, H2sol, sys3), open("l1sys2.pkl", "wb"))
