import pickle, sympy as sp, numpy as np
from scipy.integrate import solve_ivp
from lin import rho, W
As, A1 = sp.symbols("As A1")
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
H0_, H1_, K_ = sp.symbols("H0_0 H1_0 K_0")
M3 = sp.Matrix([[sp.diff(sys3[q], v) for v in (H0_, H1_, K_)] for q in (0, 1, 3)])
f = sp.lambdify((rho, W, As, A1), M3, "numpy")
Wv = 0.7
rhs = lambda r, y: np.array(f(r, Wv, 1.0, 0.0), dtype=float) @ y
for y0 in ([1, 0, 0], [0, 1, 0], [0, 0, 1]):
    sol = solve_ivp(rhs, [2.0, 12.0], y0, method="DOP853", rtol=1e-12, atol=1e-30, dense_output=True)
    for r in (4, 8, 12):
        v = sol.sol(r); print(y0, r, np.log(np.abs(v) + 1e-300))
