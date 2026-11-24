import pickle, sympy as sp, mpmath as mp
mp.mp.dps = 40
a, b, c2, e, f, zz = sp.symbols("a b c2 e f zz")
polys = [sp.sympify(s) for s in pickle.load(open("eq_flow.pkl", "rb"))]
vars_ = (a, b, c2, e)
F = sp.lambdify(vars_, polys, "mpmath")
J = sp.lambdify(vars_, sp.Matrix(polys).jacobian(vars_), "mpmath")
x = mp.matrix([-0.240941, -0.606703, 0.830343, -2.948594])
for it in range(30):
    Fv = mp.matrix(F(*x)); Jv = mp.matrix(J(*x))
    dx = mp.lu_solve(Jv.T*Jv, -(Jv.T*Fv))
    x = x + dx
    if mp.norm(dx) < mp.mpf(10)**-30: break
print([mp.nstr(v, 20) for v in x], "residual", mp.nstr(mp.norm(mp.matrix(F(*x))), 5))
Phi = 4*x[0]**2*x[1]**2 - x[1]**4 + (x[1]+x[2])**2
print("Phi", mp.nstr(Phi, 10))
