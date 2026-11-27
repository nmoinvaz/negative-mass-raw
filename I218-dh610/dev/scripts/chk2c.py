import pickle, sympy as sp, numpy as np
from scipy.integrate import solve_ivp
from lin import rho, W
As, A1 = sp.symbols("As A1")
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
f = sp.lambdify((rho, W, As, A1), Nn, "numpy")
Wv = 0.7
rhs = lambda r, y: np.array(f(r, Wv, 1.0, 0.0), dtype=float) @ y
for y0 in ([1, 0], [0, 1]):
    sol = solve_ivp(rhs, [2.0, 40.0], y0, method="DOP853", rtol=1e-12, atol=1e-30, dense_output=True)
    prev = None
    for r in (10, 20, 30, 40):
        v = sol.sol(r); l = np.log(np.abs(v) + 1e-300)
        print(y0, r, l, "" if prev is None else (l - prev) / 10); prev = l
