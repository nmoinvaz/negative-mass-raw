import sympy as sp, pickle
out = pickle.load(open('lin.pkl','rb'))
t, rho, W = sp.symbols('t rho W'); eps = sp.Symbol('epsilon')
A = sp.Function('A')(rho); R = sp.Function('R')(rho); P0 = sp.Function('P0')(rho)
Vs = sp.Function('Vs')(rho); Vp = sp.Function('Vp')(rho); Vpp = sp.Function('Vpp')(rho)
n1, l1, y1, f1 = [sp.Function(s)(t, rho) for s in ('n1', 'l1', 'y1', 'f1')]
N, L, Y, F = [sp.Function(s)(rho) for s in 'NLYF']
def sub_modes(e, Nn=N, Ll=L, Yy=Y, Ff=F):
    e = e.subs({n1: Nn*sp.exp(W*t), l1: Ll*sp.exp(W*t), y1: Yy*sp.exp(W*t), f1: Ff*sp.exp(W*t)}).doit()
    return sp.simplify(e*sp.exp(-W*t))
# background relations
a1, a2 = sp.symbols('a1 a2')
Rpp = -eps*sp.diff(P0, rho)**2*R/2
def bg(e):
    """impose background: R'' , A'', V, V_phi, V_phiphi"""
    e = e.subs(Vpp, sp.diff(Vp, rho)/sp.diff(P0, rho)) if e.has(Vpp) else e
    e = e.subs(Vp, eps*(A*sp.diff(P0, rho, 2) + 2*A*sp.diff(P0, rho)*sp.diff(R, rho)/R + sp.diff(A, rho)*sp.diff(P0, rho))).doit()
    e = e.subs(Vs, -(sp.diff(A, rho, 2)*R**2 + 2*sp.diff(A, rho)*R*sp.diff(R, rho))/(2*R**2))
    # A'' from theta-theta background eq: A (R^2)'' - R^2 A'' = 2
    Ar2 = (A*(2*sp.diff(R, rho)**2 + 2*R*Rpp) - 2)/R**2
    for k in range(4, 1, -1):
        pass
    # replace higher derivatives iteratively
    for _ in range(4):
        e = e.subs(sp.diff(R, rho, 4), sp.diff(Rpp, rho, 2)).subs(sp.diff(R, rho, 3), sp.diff(Rpp, rho)).subs(sp.diff(R, rho, 2), Rpp)
        e = e.subs(sp.diff(A, rho, 4), sp.diff(Ar2, rho, 2)).subs(sp.diff(A, rho, 3), sp.diff(Ar2, rho)).subs(sp.diff(A, rho, 2), Ar2)
        e = e.doit()
    return sp.simplify(e)
res = {}
for k, (e0, e1) in out.items():
    res[k] = e1
# check the background first
for k, (e0, e1) in out.items():
    print(k, 'bg residual:', bg(e0))
pickle.dump(None, open('dummy.pkl','wb'))
