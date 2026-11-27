"""dev: linearize R_mn - eps phi_m phi_n - V g_mn = 0 about a static background, generic functions."""
import sympy as sp, pickle, sys
t, rho, th, ph, eta = sp.symbols('t rho theta varphi eta')
eps = sp.Symbol('epsilon')
A = sp.Function('A')(rho); R = sp.Function('R')(rho); P0 = sp.Function('P0')(rho)  # background A, R, phi0
Vs = sp.Function('Vs')(rho); Vp = sp.Function('Vp')(rho); Vpp = sp.Function('Vpp')(rho)  # V, V_phi, V_phiphi on background
n1, l1, y1, f1 = [sp.Function(s)(t, rho) for s in ('n1', 'l1', 'y1', 'f1')]
X = [t, rho, th, ph]
nu = sp.log(A)/2 + eta*n1
lam = -sp.log(A)/2 + eta*l1
r = R + eta*y1
phi = P0 + eta*f1
g = sp.diag(-sp.exp(2*nu), sp.exp(2*lam), r**2, r**2*sp.sin(th)**2)
gi = g.inv()
def christ(g, gi):
    G = [[[0]*4 for _ in range(4)] for _ in range(4)]
    for a in range(4):
        for b in range(4):
            for c in range(4):
                G[a][b][c] = sum(gi[a, d]*(sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(4))/2
    return G
G = christ(g, gi)
def ricci():
    Ric = sp.zeros(4, 4)
    for b in range(4):
        for c in range(b, 4):
            s = 0
            for a in range(4):
                s += sp.diff(G[a][b][c], X[a]) - sp.diff(G[a][b][a], X[c])
                for d in range(4):
                    s += G[a][a][d]*G[d][b][c] - G[a][c][d]*G[d][b][a]
            Ric[b, c] = Ric[c, b] = s
    return Ric
Ric = ricci()
# V(phi) expanded to first order: V = Vs + eta Vp f1 ; V_phi = Vp + eta Vpp f1
Vexp = Vs + eta*Vp*f1
dphi = [sp.diff(phi, x) for x in X]
E = sp.zeros(4, 4)
for a in range(4):
    for b in range(a, 4):
        E[a, b] = Ric[a, b] - eps*dphi[a]*dphi[b] - Vexp*g[a, b]
# scalar eq: eps box phi - V_phi
sq = sp.sqrt(-g.det())
box = sum(sp.diff(sq*gi[a, a]*dphi[a], X[a]) for a in range(4))/sq
S = eps*box - (Vp + eta*Vpp*f1)
def lin(e):
    e0 = sp.simplify(e.subs(eta, 0).doit())
    e1 = sp.diff(e, eta).subs(eta, 0).doit()
    return e0, e1
out = {}
for (a, b) in [(0, 0), (0, 1), (1, 1), (2, 2)]:
    out[(a, b)] = lin(E[a, b]); print(a, b, 'done', flush=True)
out['S'] = lin(S); print('S done', flush=True)
pickle.dump(out, open('lin.pkl', 'wb'))
for k, (e0, e1) in out.items():
    print(k, 'background:', e0)
