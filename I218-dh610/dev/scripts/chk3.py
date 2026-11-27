import pickle, sympy as sp, numpy as np
from lin import rho, W, L, R2
As, A1 = sp.symbols("As A1")
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
H0_, H1_, K_ = sp.symbols("H0_0 H1_0 K_0")
M3 = sp.Matrix([[sp.diff(sys3[q], v) for v in (H0_, H1_, K_)] for q in (0, 1, 3)])
f = sp.lambdify((rho, W, As, A1), M3, "numpy")
for r in (5.0, 20.0, 100.0):
    m = np.array(f(r, 0.7, 1.0, 0.0), dtype=float)
    print(r, np.linalg.eigvals(m))
fN = sp.lambdify((rho, W, As, A1), Nn, "numpy")
for r in (5.0, 20.0, 100.0):
    m = np.array(fN(r, 0.7, 1.0, 0.0), dtype=float)
    print("N", r, np.linalg.eigvals(m))
