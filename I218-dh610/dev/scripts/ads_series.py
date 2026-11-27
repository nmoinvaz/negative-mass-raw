import sympy as sp
u, c, W = sp.symbols("u c W", real=True)    # u = 1/rho (rho -> -inf: u -> 0^-)
K = -2 * c / sp.pi
# A(rho) with u = 1/rho, atan(rho) = -pi/2 - atan(u)... for rho<0: atan(rho) = -pi/2 - atan(1/rho)?  atan(rho) = -pi/2 - atan(1/rho) for rho<0
rho = 1 / u
atan_expr = -sp.pi / 2 - sp.series(sp.atan(u), u, 0, 14).removeO()
A = 1 + c * (rho**2 + 1) + K * (rho + (rho**2 + 1) * atan_expr)
A = sp.expand(sp.simplify(A))
print("A =", sp.series(A, u, 0, 4))
# derivative wrt rho: d/drho = -u^2 d/du
D = lambda f: -u**2 * sp.diff(f, u)
Ap = D(A); R2 = rho**2 + 1
P1 = 2 * u - Ap / A
P0 = 1 / R2**2 - Ap / (A * rho * R2) - 2 / (A * R2) + W**2 / A**2
ys = sp.symbols("y1:6")
Y = 1 + sum(ys[k] * u**(k + 1) for k in range(5))
ode = D(D(Y)) - P1 * D(Y) - P0 * Y
ser = sp.series(sp.simplify(ode), u, 0, 7).removeO()
ser = sp.expand(ser)
sol = {}
for n in range(0, 7):
    cn = ser.coeff(u, n).subs(sol)
    if cn == 0: continue
    free = [y for y in ys if cn.has(y) and y not in sol]
    print("order", n, "coefficient:", sp.simplify(cn), "free", free)
    if free:
        s = sp.solve(cn, free[0])
        sol[free[0]] = sp.simplify(s[0])
        print("  ", free[0], "=", sol[free[0]])
