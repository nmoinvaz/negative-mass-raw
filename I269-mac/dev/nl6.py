# dev: invariants of the exact family (fate): Misner-Sharp, 2D curvature, Kretschmann; apparent horizon locus
import sympy as sp
v, rho = sp.symbols("v rho", real=True)
c, beta = sp.symbols("c beta")
K = -2*c/sp.pi
A = 1 + c*(rho**2+1) + K*(rho + (rho**2+1)*sp.atan(rho))
R = sp.sqrt(1+rho**2)
s = beta*sp.exp(K*v)
lam2 = 1 + s
lam = sp.sqrt(lam2)
F = A - 2*rho*sp.diff(lam,v)/lam + 1/lam2 - 1
r = lam*R
X = [v, rho]
h = sp.Matrix([[-F, 1], [1, 0]]); hi = h.inv()
Gam = [[[sum(hi[a,d]*(sp.diff(h[d,b],X[cc])+sp.diff(h[d,cc],X[b])-sp.diff(h[b,cc],X[d])) for d in range(2))/2
         for cc in range(2)] for b in range(2)] for a in range(2)]
def Riem(a,b,cc,d):  # R^a_{bcd}
    return (sp.diff(Gam[a][b][d],X[cc]) - sp.diff(Gam[a][b][cc],X[d])
            + sum(Gam[a][cc][e]*Gam[e][b][d] - Gam[a][d][e]*Gam[e][b][cc] for e in range(2)))
R2 = sp.simplify(sum(hi[b,d]*Riem(a,b,a,d) for a in range(2) for b in range(2) for d in range(2)))
dr = [sp.diff(r,x) for x in X]
Hr = sp.Matrix(2,2, lambda a,b: sp.diff(r,X[a],X[b]) - sum(Gam[k][a][b]*dr[k] for k in range(2)))
Hup = hi*Hr*hi
HH = sum(Hr[a,b]*Hup[a,b] for a in range(2) for b in range(2))
grad2 = sum(hi[a,b]*dr[a]*dr[b] for a in range(2) for b in range(2))
Kret = R2**2 + 8*HH/r**2 + 4*(1-grad2)**2/r**4
mMS = r/2*(1-grad2)
print("R2 =", sp.simplify(R2))
print("grad2 (Dr)^2 =", sp.simplify(grad2))
print("mMS =", sp.simplify(mMS))
import mpmath as mp
mp.mp.dps = 30
def num(expr, cv, bv, vv, rv):
    return sp.N(expr.subs({c:cv, beta:bv, v:vv, rho:rv}), 25)
print("Kretschmann, c=-1, beta=-1, L=1: v* = -ln(1)/K = 0; v = v*-d")
for d in ("1e-1","1e-2","1e-3","1e-4","1e-5"):
    vv = -sp.Float(d)
    kr = num(Kret, -1, -1, vv, sp.Rational(1,2)); lam4 = num(lam2**2, -1, -1, vv, sp.Rational(1,2))
    print(d, kr, kr*lam4)
print("Kretschmann, c=-1, beta=+1, v -> inf, rho=1/2 and 3")
for vv in (0, 5, 10, 20, 40, 80):
    print(vv, num(Kret, -1, 1, sp.Integer(vv), sp.Rational(1,2)), num(Kret, -1, 1, sp.Integer(vv), 3), num(F, -1, 1, sp.Integer(vv), sp.Rational(1,2)))
