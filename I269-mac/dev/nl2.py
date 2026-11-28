from nl1 import *
lam = sp.Function("lam")(v)
f = sp.Function("f")(v, rho)
F = A + f
g = sp.diag(0,0,lam**2*R**2,lam**2*R**2*sp.sin(th)**2)
g[0,0] = -F; g[0,1] = g[1,0] = 1
E = einstein(g, P, V0, V1)
for k,e in E.items():
    e = sp.simplify(e.doit())
    print(k, ":", e)
