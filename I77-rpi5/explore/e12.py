import sys, time, pickle
import sympy as sp
exec(open("e11.py").read().split("for nm, E in")[0])
E1p = sp.cancel(E1 / (-W1)); E2p = sp.cancel(E2 / (-W1))
t0 = time.time()
R13 = sp.factor(sp.resultant(E1p, E3, W3))
print("Res(E1',E3):", time.time()-t0, [(sp.Poly(g, W0, W1, W2).degree_list(), m) for g, m in sp.factor_list(R13)[1]], flush=True)
R23 = sp.factor(sp.resultant(E2p, E3, W3))
print("Res(E2',E3):", time.time()-t0, [(sp.Poly(g, W0, W1, W2).degree_list(), m) for g, m in sp.factor_list(R23)[1]], flush=True)
pickle.dump((str(R13), str(R23)), open("res_eq.pkl", "wb"))
for nm, R in (("R13", R13), ("R23", R23)):
    for g, m in sp.factor_list(R)[1]:
        print(nm, m, sp.Poly(g, W0, W1, W2).degree_list(), len(sp.Poly(g, W0, W1, W2).terms()), str(g)[:200])
