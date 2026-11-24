import sys, time, pickle
import sympy as sp
exec(open("e11.py").read().split("for nm, E in")[0])
a, b, c2, e, f, zz = sp.symbols("a b c2 e f zz")
sb = {W0: a, W1: b, W2: c2, W3: e, W4: f}
E1p = sp.cancel(E1 / (-W1)).subs(sb); E2p = sp.cancel(E2 / (-W1)).subs(sb); E3s = E3.subs(sb)
A02 = A[(0,2)].subs(sb); B02 = B[(0,2)].subs(sb)   # A02 * f + B02 = 0
Phi = sp.cancel(A02 / b)
def Dflow(G):
    return sp.diff(G, a)*b + sp.diff(G, b)*(b + c2) + sp.diff(G, c2)*(2*c2 + e) + sp.diff(G, e)*(3*e + f)
polys = [E1p, E2p, E3s]
for G in (E1p, E2p, E3s):
    DG = Dflow(G)
    # DG = P + Q f : substitute f = -B02/A02, multiply by A02
    P_ = DG.subs(f, 0); Q_ = sp.expand(sp.diff(DG, f))
    polys.append(sp.expand(P_*A02 - Q_*B02))
print("degrees", [sp.Poly(p, a, b, c2, e).total_degree() for p in polys], "terms", [len(sp.Poly(p, a, b, c2, e).terms()) for p in polys], flush=True)
pickle.dump([str(p) for p in polys], open("eq_flow.pkl", "wb"))
for pr in (32003, 1000003):
    t0 = time.time()
    G = sp.groebner(polys + [sp.expand(zz*b*Phi - 1)], zz, a, b, c2, e, order="grevlex", modulus=pr)
    print("modulus", pr, "groebner time", time.time()-t0, "basis size", len(G.exprs), "unit:", list(G.exprs) == [1], flush=True)
    if list(G.exprs) != [1]:
        print([sp.Poly(g, zz, a, b, c2, e).total_degree() for g in G.exprs][:20])
