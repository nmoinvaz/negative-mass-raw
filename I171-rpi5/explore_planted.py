# Exploration before the README of I171-rpi5 (not of record). Timing of the planted P1, P2 residual in #78's sheared coordinates.
import time, sympy as sp
t0 = time.time()
T_, Z, R, Th = sp.symbols("T Z R Theta", real=True)
X = (T_, Z, R, Th)

def einstein(g, X):
    n = len(X); gi = g.inv().applyfunc(sp.simplify)
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[cc]) + sp.diff(g[d, cc], X[b]) - sp.diff(g[b, cc], X[d])) for d in range(n)) / 2)
             for cc in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for cc in range(n):
            Ric[b, cc] = sp.simplify(sum(sp.diff(Gam[a][b][cc], X[a]) - sp.diff(Gam[a][a][b], X[cc]) for a in range(n))
                                     + sum(Gam[a][a][d] * Gam[d][b][cc] - Gam[a][cc][d] * Gam[d][a][b] for a in range(n) for d in range(n)))
    Rs = sp.simplify(sum(gi[a, b] * Ric[a, b] for a in range(n) for b in range(n)))
    return Ric, Rs, (Ric - Rs * g / 2).applyfunc(sp.simplify), gi

for tag, den, sgn, V in (("P1", Z, (1, 1), -1 / (8 * sp.pi)), ("P2", None, (-1, -1), 1 / (8 * sp.pi))):
    tau = T_ + Z / 3; z = Z; Rr = R; Thh = Th + T_ / 7 + Z / 5
    d = den if den is not None else tau
    # metric (-dtau^2 + dz^2)/d^2 + dR^2 + R^2 dTheta^2, with d the coordinate expression (z for P1, tau for P2)
    J = sp.Matrix([[sp.diff(f, x) for x in X] for f in (tau, z, Rr, Thh)])
    g0 = sp.diag(-1 / d**2, 1 / d**2, 1, R**2)
    g = (J.T * g0 * J).applyfunc(sp.simplify)
    Ric, Rs, G, gi = einstein(g, X)
    print(tag, "G", G.tolist(), f"[{time.time()-t0:.1f} s]")
    fields = [R * sp.cos(Thh) / sp.sqrt(8 * sp.pi), R * sp.sin(Thh) / sp.sqrt(8 * sp.pi)]
    T = sp.zeros(4, 4)
    for s_, f in zip(sgn, fields):
        dd = sp.Matrix([sp.diff(f, x) for x in X]); k = (dd.T * gi * dd)[0]
        T += s_ * (dd * dd.T - g * k / 2)
    T -= g * V
    Res = (G - 8 * sp.pi * T).applyfunc(sp.simplify)
    print(tag, "Res", Res.tolist(), f"[{time.time()-t0:.1f} s]")
