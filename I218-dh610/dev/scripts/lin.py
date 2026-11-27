"""Development: linearization of R_ab - eps d_a phi d_b phi - V g_ab = 0, eps sign passed in, about the black-universe family
(R^2 = rho^2 + 1, phi0' = sqrt2/R^2, A generic with A'' = 2(A-1)/R^2)."""
import sympy as sp
import time

t, rho, th, ph = sp.symbols('t rho theta varphi', real=True)
W, L = sp.symbols('W L')
eta = sp.Symbol('eta')
X = [t, rho, th, ph]
A = sp.Function('A')(rho)
R2 = rho**2 + 1
Rr = sp.sqrt(R2)
phi0 = sp.sqrt(2) * sp.atan(rho)
Yf = sp.Function('Y')(th)
Ys, Yps = sp.symbols('Ys Yps')
ex = sp.exp(W * t)
N = 4


def bg_rules(A, mut=()):
    """closed forms of V, V_phi, V_phiphi along the background, as functions of rho (family, [BF06])"""
    Ap = sp.diff(A, rho)
    App = 2 * (A - 1) / R2
    Vs = -(A - 1 + rho * Ap) / R2
    Vp = -sp.sqrt(2) * Ap / R2
    Vpp = -App + 2 * rho * Ap / R2
    return Vs, Vp, Vpp


def Asub(z, depth=4):
    """A'' -> 2 (A - 1)/R^2 and its derivatives"""
    App = 2 * (A - 1) / R2
    for _ in range(depth):
        z = z.subs(sp.diff(A, rho, 4), sp.diff(App, rho, 2)).subs(sp.diff(A, rho, 3), sp.diff(App, rho)).subs(sp.diff(A, rho, 2), App)
    return z


def linearize(h, dphi, eps=-1, mut=()):
    """first-order variation of E_ab = R_ab - eps phi_a phi_b - V g_ab (components given) and of S = eps Box phi - V_phi.
    h: 4x4 sympy Matrix (functions of t, rho, theta); dphi: perturbation of phi. Background: family with generic A."""
    g0 = sp.diag(-A, 1 / A, R2, R2 * sp.sin(th)**2)
    g0i = g0.inv()
    g = g0 + eta * h
    gi = g0i - eta * g0i * h * g0i
    Vs, Vp, Vpp = bg_rules(A, mut)
    phi = phi0 + eta * dphi

    def Gam(gm, gim):
        return [[[sum(gim[a, d] * (sp.diff(gm[d, b], X[c]) + sp.diff(gm[d, c], X[b]) - sp.diff(gm[b, c], X[d])) for d in range(N)) / 2
                  for c in range(N)] for b in range(N)] for a in range(N)]
    Gfull = Gam(g, gi)
    G0 = [[[sp.simplify(Gfull[a][b][c].subs(eta, 0)) for c in range(N)] for b in range(N)] for a in range(N)]
    dG = [[[sp.expand(sp.diff(Gfull[a][b][c], eta).subs(eta, 0)) for c in range(N)] for b in range(N)] for a in range(N)]

    def ric(Gm):
        Rm = sp.zeros(N, N)
        for a in range(N):
            for b in range(N):
                Rm[a, b] = sum(sp.diff(Gm[c][a][b], X[c]) - sp.diff(Gm[c][a][c], X[b])
                               + sum(Gm[c][c][d] * Gm[d][a][b] - Gm[c][b][d] * Gm[d][a][c] for d in range(N)) for c in range(N))
        return Rm
    R0 = ric(G0).applyfunc(sp.simplify)
    dR = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            dR[a, b] = sum(sp.diff(dG[c][a][b], X[c]) - sp.diff(dG[c][a][c], X[b])
                           + sum(dG[c][c][d] * G0[d][a][b] + G0[c][c][d] * dG[d][a][b]
                                 - dG[c][b][d] * G0[d][a][c] - G0[c][b][d] * dG[d][a][c] for d in range(N)) for c in range(N))
    dph = [sp.diff(phi, x) for x in X]
    E = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            E[a, b] = sp.diff(dR[a, b], eta) * 0 + dR[a, b]
    # delta(phi_a phi_b) and delta(V g_ab)
    dE = sp.zeros(N, N)
    for a in range(N):
        for b in range(N):
            dpp = sp.diff(dph[a] * dph[b], eta).subs(eta, 0)
            dVg = Vp * dphi * g0[a, b] + Vs * h[a, b]
            dE[a, b] = dR[a, b] - eps * dpp - dVg
    E0 = sp.zeros(N, N)
    dphi0 = [sp.diff(phi0, x) for x in X]
    for a in range(N):
        for b in range(N):
            E0[a, b] = R0[a, b] - eps * dphi0[a] * dphi0[b] - Vs * g0[a, b]
    sq0 = R2 * sp.sin(th)
    trh = sum(g0i[a, b] * h[a, b] for a in range(N) for b in range(N))
    sq = sq0 * (1 + eta * trh / 2)
    box = sum(sp.diff(sq * sum(gi[a, b] * dph[b] for b in range(N)), X[a]) for a in range(N)) / sq
    S = eps * box - (Vp + eta * Vpp * dphi)
    dS = sp.diff(S, eta).subs(eta, 0)
    S0 = S.subs(eta, 0)
    return dE, dS, E0, S0


def angsub(z):
    """Y'' -> -cot Y' - L Y, then Y, Y' -> symbols"""
    Ypp = -sp.cos(th) / sp.sin(th) * sp.diff(Yf, th) - L * Yf
    for _ in range(3):
        z = z.subs(sp.diff(Yf, th, 4), sp.diff(Ypp, th, 2)).subs(sp.diff(Yf, th, 3), sp.diff(Ypp, th)).subs(sp.diff(Yf, th, 2), Ypp)
    z = z.subs(sp.diff(Yf, th), Yps).subs(Yf, Ys)
    return sp.expand(z)
