import pickle, sympy as sp, numpy as np
from lin import rho, W, L, R2
As, A1 = sp.symbols("As A1")
Mn, lam = pickle.load(open("sys4n.pkl", "rb"))
f = sp.lambdify((rho, lam, L, As, A1), Mn, "numpy")
for r in (5.0, 20.0, 100.0, 1000.0):
    m = np.array(f(r, 0.49, 6.0, 1.0, 0.0), dtype=float)
    print(r, np.linalg.eigvals(m))
