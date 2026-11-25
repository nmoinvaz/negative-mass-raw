import pickle, numpy as np, sympy as sp, random
a, b, c2, e, f, zz = sp.symbols("a b c2 e f zz")
polys = [sp.sympify(s) for s in pickle.load(open("eq_flow.pkl", "rb"))]
vars_ = (a, b, c2, e)
F = sp.lambdify(vars_, polys, "numpy")
J = sp.lambdify(vars_, sp.Matrix(polys).jacobian(vars_), "numpy")
rng = np.random.default_rng(1)
sols = []
for trial in range(600):
    x = rng.normal(size=4) * rng.choice([0.5, 1, 2, 4])
    for it in range(40):
        Fv = np.array(F(*x), dtype=float); Jv = np.array(J(*x), dtype=float)
        try:
            dx = np.linalg.lstsq(Jv, -Fv, rcond=None)[0]
        except Exception:
            break
        x = x + dx
        if np.linalg.norm(dx) < 1e-14 or not np.all(np.isfinite(x)): break
    Fv = np.array(F(*x), dtype=float)
    if np.all(np.isfinite(x)) and np.linalg.norm(Fv) < 1e-9 and abs(x[1]) > 1e-2 and abs(4*x[0]**2*x[1]**2 - x[1]**4 + (x[1]+x[2])**2) > 1e-4 * (1 + np.linalg.norm(x))**4:
        sols.append(x.copy())
print("converged solutions with b != 0:", len(sols))
for s in sols[:10]:
    print(np.round(s, 6))
