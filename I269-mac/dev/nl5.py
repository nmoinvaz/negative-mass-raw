# exact family: lam^2 = L + beta e^{K v}; residuals symbolic, and linearization
import nl1
from nl1 import *
L, beta, vv_ = sp.symbols("L beta vv_", positive=True)
s = beta*sp.exp(K*v)
lam = sp.sqrt(L + s)
f = -2*rho*sp.diff(lam,v)/lam + 1/lam**2 - 1
F = A + f
print("F =", sp.simplify(F - A))
g = sp.diag(0,0,lam**2*R**2,lam**2*R**2*sp.sin(th)**2)
g[0,0] = -F; g[0,1] = g[1,0] = 1
E = einstein(g, P, V0, V1)
for k,e in E.items():
    e = sp.simplify(e.doit())
    print(k, ":", e)
