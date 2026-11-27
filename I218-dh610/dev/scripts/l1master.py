import pickle, sympy as sp
from lin import rho, W
As, A1 = sp.symbols("As A1")
M3, gv, vars3 = pickle.load(open("l1h3.pkl", "rb"))
sub = {As: 1, A1: 0}
M = sp.simplify(M3.subs(sub)); g = sp.simplify(gv.subs(sub))
print("g(Ellis) =", list(g))
H0, H2, F = sp.symbols("H0 H2 F")
v = sp.Matrix([H0, H2, F])
# invariants with pivot H2:  chi = F - gF/gH2 * H2 ; psi = H0 - gH0/gH2 * H2
chi = F - g[2] / g[1] * H2
psi = H0 - g[0] / g[1] * H2
Dv = lambda expr: sp.diff(expr, rho) + sum(sp.diff(expr, v[i]) * (M * v)[i] for i in range(3))
dchi = sp.simplify(Dv(chi)); dpsi = sp.simplify(Dv(psi))
q1, q2 = sp.symbols("q1 q2")
# express H0 = psi + gH0/gH2*H2 ... H2 must drop out
rep = {F: q1 + g[2] / g[1] * H2, H0: q2 + g[0] / g[1] * H2}
dchi = sp.simplify(dchi.subs(rep)); dpsi = sp.simplify(dpsi.subs(rep))
print("H2 drops out:", not dchi.has(H2), not dpsi.has(H2))
N = sp.Matrix([[sp.diff(dchi, q1), sp.diff(dchi, q2)], [sp.diff(dpsi, q1), sp.diff(dpsi, q2)]]).applyfunc(sp.simplify)
sp.pprint(N)
a, b, c_, d = N[0, 0], N[0, 1], N[1, 0], N[1, 1]
y = sp.Function("y")(rho)
p = (sp.diff(y, rho) - a * y) / b
ode = sp.simplify(sp.diff(p, rho) - c_ * y - d * p)
ypp = sp.solve(ode, sp.diff(y, rho, 2))[0]
cy1 = sp.simplify(ypp.coeff(sp.diff(y, rho))); cy0 = sp.simplify(ypp.coeff(y))
print("y'' = (", sp.factor(cy1), ") y' + (", sp.factor(cy0), ") y")
