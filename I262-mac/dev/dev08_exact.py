"""dev08: Y = R e^{W x} solves the Y equation iff (W - K)(R^2 - rho^2) = 0, for every member c (symbolic)."""
import sympy as sp
rho, c, W, x = sp.symbols("rho c W x", real=True)
Ksym = -2 * c / sp.pi
R = sp.sqrt(1 + rho ** 2)
T = sp.atan(rho)
A = 1 + c * R ** 2 + Ksym * (rho + R ** 2 * T)
Ap = sp.diff(A, rho)
P = 2 / rho - Ap / A
Q = 1 / R ** 4 - Ap / (A * rho * R ** 2) - 2 / (A * R ** 2) + W ** 2 / A ** 2
E = sp.Function("E")(rho)               # e^{W x}, E' = W E / A
Y = R * E
Yp = sp.diff(Y, rho).subs(sp.Derivative(E, rho), W * E / A)
Ypp = sp.diff(sp.diff(Y, rho).subs(sp.Derivative(E, rho), W * E / A), rho).subs(sp.Derivative(E, rho), W * E / A)
res = sp.simplify((Ypp - P * Yp - Q * Y) / E)
print("residual / e^{Wx} =", sp.factor(sp.simplify(res)))
print("at W = K(c):", sp.simplify(res.subs(W, Ksym)))
# c = -1: also with A written out
res1 = sp.simplify(res.subs(c, -1).subs(W, 2 / sp.pi))
print("c = -1, W = 2/pi:", res1)
