# dev1: symbolic check of (grad r)^2 and the expansions of the family; development only.
import sympy as sp
v, rho = sp.symbols("v rho", real=True)
c, beta = sp.symbols("c beta")
K = -2*c/sp.pi
R2 = 1 + rho**2
A = 1 + c*R2 + K*(rho + R2*sp.atan(rho))
s = beta*sp.exp(K*v)
lam = sp.sqrt(1 + s)
r = lam*sp.sqrt(R2)
F = A - 2*rho*sp.diff(lam, v)/lam + 1/lam**2 - 1
# 2D inverse metric of -F dv^2 + 2 dv drho: g^vv = 0, g^vrho = 1, g^rhorho = F
grad2 = 2*sp.diff(r, v)*sp.diff(r, rho) + F*sp.diff(r, rho)**2
closed = rho/R2*(rho*A + s*R2*sp.diff(A, rho)/2)
print("grad2 - closed:", sp.simplify(sp.expand(grad2 - closed)))
# identity R^2 A' = 2K + 2 rho (A - 1)
print("R^2 A' - 2K - 2 rho (A-1):", sp.simplify(R2*sp.diff(A, rho) - 2*K - 2*rho*(A-1)))
# ell(r) = r_v + F r_rho/2, n(r) = -r_rho
ell = sp.diff(r, v) + F*sp.diff(r, rho)/2
print("ell(r) - P/(2 R lam):", sp.simplify(ell - (rho*A + s*R2*sp.diff(A, rho)/2)/(2*sp.sqrt(R2)*lam)))
