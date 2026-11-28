# K independent of c; also a0 (the constant in A) free
import nl1
from nl1 import *
Ks, a0 = sp.symbols("Ks a0")
A2 = a0 + c*(rho**2+1) + Ks*(rho + (rho**2+1)*sp.atan(rho))
Vf2 = -c*(3-2*sp.cos(psi)**2) - Ks*(3*sp.sin(psi)*sp.cos(psi) + psi*(3-2*sp.cos(psi)**2))
# static check with a0 = 1: does the potential below support A2?  (a0 != 1 needs another V term, test residuals)
V02 = Vf2.subs(psi, sp.atan(rho)); V12 = (sp.diff(Vf2,psi)/sp.sqrt(2)).subs(psi, sp.atan(rho))
lam = sp.Function("lam")(v)
f = -2*rho*sp.diff(lam,v)/lam + 1/lam**2 - 1
g = sp.diag(0,0,lam**2*R**2,lam**2*R**2*sp.sin(th)**2)
g[0,0] = -(A2+f); g[0,1] = g[1,0] = 1
E = einstein(g, P, V02, V12)
for k,e in E.items():
    e = sp.simplify(e.doit().subs(a0,1))
    print(k, ":", e)
