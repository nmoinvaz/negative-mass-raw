# dev: nonlinear Einstein-phantom-scalar in ingoing null gauge, phi = sqrt2 arctan(rho), G=1, r = lam(v) R(rho)
import sympy as sp, sys
v, rho, th, ph = sp.symbols("v rho theta varphi", real=True)
c = sp.Symbol("c")
K = -2*c/sp.pi
eps = -1
A = 1 + c*(rho**2+1) + K*(rho + (rho**2+1)*sp.atan(rho))
R = sp.sqrt(1+rho**2)
P = sp.sqrt(2)*sp.atan(rho)
psi = sp.Symbol("psi")
Vf = -c*(3-2*sp.cos(psi)**2) - K*(3*sp.sin(psi)*sp.cos(psi) + psi*(3-2*sp.cos(psi)**2))
V0 = Vf.subs(psi, sp.atan(rho))              # V as function of rho
V1 = (sp.diff(Vf, psi)/sp.sqrt(2)).subs(psi, sp.atan(rho))   # dV/dphi
X = [v, rho, th, ph]

def einstein(g, phi, V0, V1):
    gi = g.inv(); n = 4
    Gam = [[[sum(gi[a,d]*(sp.diff(g[d,b],X[cc])+sp.diff(g[d,cc],X[b])-sp.diff(g[b,cc],X[d])) for d in range(n))/2
             for cc in range(n)] for b in range(n)] for a in range(n)]
    def ric(b,d):
        s = sum(sp.diff(Gam[a][b][d],X[a]) - sp.diff(Gam[a][b][a],X[d]) for a in range(n))
        s += sum(Gam[a][a][k]*Gam[k][b][d]-Gam[a][d][k]*Gam[k][b][a] for a in range(n) for k in range(n))
        return s
    dphi = [sp.diff(phi,x) for x in X]
    E = {}
    for nm,(i,j) in {"vv":(0,0),"vr":(0,1),"rr":(1,1),"thth":(2,2)}.items():
        E[nm] = ric(i,j) - eps*dphi[i]*dphi[j] - V0*g[i,j]
    sq = sp.sqrt(-g.det())
    box = sum(sp.diff(sq*gi[a,b]*dphi[b],X[a]) for a in range(n) for b in range(n))/sq
    E["scal"] = eps*box - V1
    return E

if __name__ == "__main__":
    # static check
    g = sp.diag(0,0,R**2,R**2*sp.sin(th)**2)
    g[0,0] = -A; g[0,1] = g[1,0] = 1
    E = einstein(g, P, V0, V1)
    for k,e in E.items():
        for cv in (sp.Rational(-3,10), -1):
            val = sp.N(e.subs({c:cv, rho:sp.Rational(7,10), th:sp.Rational(1,3)}), 30)
            print("static", k, cv, val)
