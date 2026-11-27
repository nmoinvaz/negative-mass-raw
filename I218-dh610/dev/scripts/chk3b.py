import pickle, sympy as sp
from lin import rho, W
As, A1 = sp.symbols("As A1")
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
H0_, H1_, K_ = sp.symbols("H0_0 H1_0 K_0")
M3 = sp.Matrix([[sp.diff(sys3[q], v) for v in (H0_, H1_, K_)] for q in (0, 1, 3)]).subs({As: 1, A1: 0})
sp.pprint(sp.simplify(M3))
print(sp.simplify(H2sol.subs({As: 1, A1: 0})))
