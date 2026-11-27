import pickle, sympy as sp
from lin import rho, W, L, R2
As, A1 = sp.symbols("As A1")
Nn, H2sol, sys3 = pickle.load(open("l1sys2.pkl", "rb"))
lam = sp.Symbol("lam")
Ne = sp.simplify(Nn.subs({As: 1, A1: 0}))
print("Ellis l=1 2x2 system for (I1, I2/W):"); sp.pprint(Ne)
# second order ODE for y = I1: y' = a y + b p, p' = c y + d p
a, b, c, d = Ne[0, 0], Ne[0, 1], Ne[1, 0], Ne[1, 1]
y = sp.Function("y")(rho)
# p = (y' - a y)/b ; p' = c y + d p
p = (sp.diff(y, rho) - a * y) / b
ode = sp.simplify(sp.diff(p, rho) - c * y - d * p)
ypp = sp.solve(ode, sp.diff(y, rho, 2))[0]
ypp = sp.collect(sp.expand(sp.simplify(ypp)), [y, sp.diff(y, rho)])
print("y'' =", ypp)
# Schroedinger form: y = f Z with f chosen to kill Z' term
cy1 = sp.simplify(ypp.coeff(sp.diff(y, rho)))
cy0 = sp.simplify(ypp.coeff(y))
print("coefficient of y':", sp.factor(cy1)); print("coefficient of y:", sp.factor(cy0))
f = sp.exp(sp.integrate(sp.simplify(cy1 / 2), rho))
print("f =", sp.simplify(f))
Vq = sp.simplify(cy0 - sp.diff(cy1, rho) / 2 - cy1**2 / 4)
print("Z'' = (lam + V) Z with V =", sp.factor(sp.simplify(Vq - lam)) if False else sp.factor(sp.simplify(Vq.subs(W, sp.sqrt(lam)) )))
