import sympy as sp
rho=sp.Symbol("rho"); W=sp.Symbol("W", positive=True)
c=-1
K=-2*sp.Integer(c)/sp.pi
A=1+c*(rho**2+1)+K*(rho+(rho**2+1)*sp.atan(rho))
R2=rho**2+1
Ap=sp.diff(A,rho)
# Y'' = (2/rho - A'/A) Y' + (1/R^4 - A'/(A rho R^2) - 2/(A R^2) + W^2/A^2) Y
P = 2/rho - Ap/A
Qc = 1/R2**2 - Ap/(A*rho*R2) - 2/(A*R2) + W**2/A**2
N=7
Aser=sp.series(A,rho,0,N+2).removeO()
print("A series:", sp.simplify(Aser))
kap = sp.simplify(Ap.subs(rho,0)/2)
print("kappa =", kap)
s=sp.Symbol("s")
ys=sp.symbols("y0:%d"%N)
Y=sum(ys[n]*rho**(n) for n in range(N))
# Frobenius: Y = rho^s * sum y_n rho^n ; substitute W = kappa*w with w symbol
Y_full = rho**s*Y
expr = sp.diff(Y_full,rho,2) - P*sp.diff(Y_full,rho) - Qc*Y_full
expr = sp.simplify(expr/rho**s)
ser = sp.series(sp.expand(expr*A**2*rho**2/ rho**0), rho, 0, 6).removeO() if False else None
# multiply by A^2 rho^2 to clear denominators
E2 = sp.expand(sp.series(sp.simplify(expr*A**2*rho**2), rho, 0, N).removeO())
coeffs=[sp.simplify(E2.coeff(rho,k)) for k in range(0,4)]
for k,cf in enumerate(coeffs):
    print(k, sp.factor(cf))
