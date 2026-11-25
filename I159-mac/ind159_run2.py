#!/usr/bin/env python3
"""ind159: the coordinator's independent check of #159 (limits of conical shifts with det R3 = 0).

Criteria M1-M5 in negative-mass-raw I159-mac/README.md. Imports nothing from the repository: D from #65's formula with
the own static block, an own transseries solver (truncated polynomials in nu = 1/eta and T = ln eta), an own RK4
integrator at 30 digits with Richardson extrapolation, and own Newton steps.
"""
import argparse
import sys
import time

import mpmath as mp
import sympy as sp

MUTS = ['Ysign', 'A1', 'b', 'rk', 'ff', 'eig']
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.0f} s)", flush=True)
    if not ok:
        FAIL.append(name)


x, rho = sp.symbols('x rho', positive=True)
eta = sp.Symbol('eta', positive=True)
G, p, q, nu = sp.symbols('G p q nu')


def D_static(u):
    ux, ur = sp.diff(u, x), sp.diff(u, rho)
    P = -u * sp.diff(u, x, 2) - ux**2
    Q = -(sp.diff(u, rho, 2) + ur / rho) / 2
    Z = sp.diff(u, x, rho) / 2
    Y = u * sp.diff(u, x, rho) / 2 + (-1 if MUT == 'Ysign' else 1) * ux * ur
    h = ur**2 / 2
    return h * (h**2 - P**2 - Q**2 + Y**2 + Z**2) - P * (Y**2 - Z**2) + 2 * Q * Y * Z


A0 = p**2 * (p**2 - q) * (p**2 + q)
A1 = G**2 * p**2 * q**2 + 4 * G * p**4 * q - 2 * G * q**3 + 4 * p**6 - (2 if MUT == 'A1' else 3) * p**2 * q**2
A2 = 2 * (G * (q - p) + p**2) * (G**2 * q**2 + 2 * G * p**3 + 2 * G * p**2 * q + 2 * p**4 - q**2)
NTH = A0 + nu**2 * A1 + nu**4 * A2

# M1 -------------------------------------------------------------------------------------------------------------
print("== M1: N and its theta-form ==", flush=True)
Fc = sp.Function('F')
Gp_, H_ = sp.symbols('Gp H')
e = 8 * rho**6 * D_static(Fc(x / rho))
e = e.subs(x, eta * rho).doit()
e = e.subs({sp.Derivative(Fc(eta), (eta, 2)): H_, sp.Derivative(Fc(eta), eta): Gp_}).subs(Fc(eta), G)
e = e.subs({Gp_: p / eta, H_: (q - p) / eta**2})
m1 = sp.expand(sp.cancel(e - NTH.subs(nu, 1 / eta))) == 0
check('M1', m1, f"8 rho^6 D = A0 + nu^2 A1 + nu^4 A2 with the printed A0, A1, A2: {m1}")

# truncated polynomials in (nu, T): dict {(m, j): coeff} ------------------------------------------------------------


def padd(*ps):
    out = {}
    for a in ps:
        for k, v in a.items():
            out[k] = out.get(k, 0) + v
    return out


def pscale(a, c):
    return {k: c * v for k, v in a.items()}


def pmul(a, b, M):
    out = {}
    for (m1_, j1), c1 in a.items():
        for (m2, j2), c2 in b.items():
            if m1_ + m2 <= M:
                k = (m1_ + m2, j1 + j2)
                out[k] = out.get(k, 0) + c1 * c2
    return out


def ptheta(a):
    """theta = eta d/deta = d/dT: theta(nu^m T^j) = -m nu^m T^j + j nu^m T^(j-1)."""
    out = {}
    for (m, j), c in a.items():
        out[(m, j)] = out.get((m, j), 0) - m * c
        if j:
            out[(m, j - 1)] = out.get((m, j - 1), 0) + j * c
    return out


def shift(a, k):
    return {(m + k, j): c for (m, j), c in a.items()}


def N_series(Gs, M):
    ps = ptheta(Gs)
    qs = ptheta(ps)
    mul = lambda *fs: _mulall(fs, M)
    p2 = mul(ps, ps)
    q2 = mul(qs, qs)
    a0 = mul(p2, padd(p2, pscale(qs, -1)), padd(p2, qs))
    G2 = mul(Gs, Gs)
    p4 = mul(p2, p2)
    a1 = padd(mul(G2, p2, q2), pscale(mul(Gs, p4, qs), 4), pscale(mul(Gs, q2, qs), -2), pscale(mul(p4, p2), 4),
              pscale(mul(p2, q2), -(2 if MUT == 'A1' else 3)))
    f1 = padd(mul(Gs, padd(qs, pscale(ps, -1))), p2)
    f2 = padd(mul(G2, q2), pscale(mul(Gs, p2, ps), 2), pscale(mul(Gs, p2, qs), 2), pscale(p4, 2), pscale(q2, -1))
    a2 = pscale(mul(f1, f2), 2)
    return padd(a0, shift(a1, 2), shift(a2, 4))


def _mulall(fs, M):
    out = fs[0]
    for f in fs[1:]:
        out = pmul(out, f, M)
    return out


def solve_series(Finf, Cval, nmax, jmax_fn, simp):
    """Stage-by-stage solve; returns (coeffs dict, free list, ok, obstruction)."""
    Gs = {(0, 0): Finf, (2, 0): -2 * Finf}
    free = []
    for n in range(3, nmax + 1):
        unk = {j: sp.Symbol(f'a_{n}_{j}') for j in range(jmax_fn(n) + 1)}
        trial = padd(Gs, {(n, j): s for j, s in unk.items()})
        Nn = N_series(trial, n + 6)
        low = [simp(c) for (m, j), c in Nn.items() if m < n + 6]
        if any(c != 0 for c in low):
            return Gs, free, False, f"lower order nonzero at stage {n}"
        eqs = [simp(c) for (m, j), c in Nn.items() if m == n + 6]
        eqs = [e_ for e_ in eqs if e_ != 0]
        sol = sp.solve(eqs, list(unk.values()), dict=True) if eqs else [{}]
        if not sol:
            return Gs, free, False, (n, [sp.factor(e_) for e_ in eqs])
        sol = sol[0]
        for j, s in unk.items():
            if s not in sol:
                free.append(str(s))
                val = Cval if (n == 4 and j == 0) else 0
            else:
                val = simp(sol[s].subs({u: (Cval if (n == 4 and k == 0) else 0) for k, u in unk.items()}))
            if val != 0:
                Gs[(n, j)] = val
    return Gs, free, True, None


# M2 -------------------------------------------------------------------------------------------------------------
print("\n== M2: the series with logarithms ==", flush=True)
Fi, Cs = sp.symbols('F_inf C', nonzero=True)
simp = lambda e_: sp.factor(sp.cancel(sp.expand(e_)))
Gs, free, ok, obst = solve_series(Fi, Cs, 9, lambda n: n // 2 + 1, simp)
co = lambda n, j: Gs.get((n, j), 0)
b_expect = Fi * (Fi**2 + (8 if MUT == 'b' else 7))
printed = {(4, 1): b_expect,
           (6, 0): -(107 * Fi**6 - 134 * Fi**4 + 587 * Fi**2 + 48 * Cs * Fi**3 - 384 * Cs * Fi + 144 * Cs**2) / (216 * Fi),
           (6, 1): -2 * (Fi**2 + 7) * (Fi**3 - 8 * Fi + 6 * Cs) / 9, (6, 2): -2 * Fi * (Fi**2 + 7)**2 / 3,
           (8, 3): Fi * (Fi**2 + 7)**3 / 2}
match = {k: sp.cancel(co(*k) - v) == 0 for k, v in printed.items()}
odd0 = all(m % 2 == 0 for (m, j) in Gs)
resid = N_series(Gs, 15)
res0 = all(simp(c) == 0 for (m, j), c in resid.items() if m <= 15)  # shifted A1, A2 terms above nu^15 are incomplete
Gp_pure, free_p, ok_p, obst_p = solve_series(Fi, Cs, 4, lambda n: 0, simp)
pure_ok = (not ok_p) and isinstance(obst_p, tuple) and obst_p[0] == 4 and all(
    sp.factor(e_ / (Fi**4 * (Fi**2 + 7))).is_number for e_ in obst_p[1])
m2 = ok and free == ['a_4_0'] and all(match.values()) and odd0 and res0 and pure_ok
check('M2', m2, f"stages solvable: {ok}; free: {free}; printed coefficients match: {match}; odd zero: {odd0}; N through "
      f"nu^15 zero: {res0}; pure series stops at n = 4 with {obst_p[1] if isinstance(obst_p, tuple) else obst_p}: {pure_ok}")

# M3 -------------------------------------------------------------------------------------------------------------
print("\n== M3: numerical integration ==", flush=True)
mp.mp.dps = 40
NTHf = sp.lambdify((G, p, q, nu), NTH, modules='mpmath')
dNdq = sp.lambdify((G, p, q, nu), sp.diff(NTH, q), modules='mpmath')
W = (1, 3, 1, 1) if MUT == 'rk' else (1, 2, 2, 1)


def series_val(Gs, et):
    T, v = mp.log(et), 1 / mp.mpf(et)
    g = mp.mpf(0)
    pv = mp.mpf(0)
    for (m, j), c in Gs.items():
        c = mp.mpf(sp.Rational(c).p) / sp.Rational(c).q
        g += c * v**m * T**j
        pv += c * v**m * (-m * T**j + (j * T**(j - 1) if j else 0))
    return g, pv


def qsolve(g, pv, v, q0):
    qq = q0
    for _ in range(60):
        f = NTHf(g, pv, qq, v)
        d = dNdq(g, pv, qq, v)
        dq = f / d
        qq -= dq
        if abs(dq) <= mp.mpf(10)**-38 * (abs(qq) + mp.mpf(10)**-60):
            break
    return qq


def rk4(g, pv, s0, s1, nsteps, q0):
    h = (mp.mpf(s1) - s0) / nsteps
    s, qq = mp.mpf(s0), q0

    def f(s_, g_, p_):
        nonlocal qq
        qq = qsolve(g_, p_, mp.e**(-s_), qq)
        return p_, qq
    for _ in range(nsteps):
        k1 = f(s, g, pv)
        k2 = f(s + h / 2, g + h / 2 * k1[0], pv + h / 2 * k1[1])
        k3 = f(s + h / 2, g + h / 2 * k2[0], pv + h / 2 * k2[1])
        k4 = f(s + h, g + h * k3[0], pv + h * k3[1])
        g += h / 6 * (W[0] * k1[0] + W[1] * k2[0] + W[2] * k3[0] + W[3] * k4[0])
        pv += h / 6 * (W[0] * k1[1] + W[1] * k2[1] + W[2] * k3[1] + W[3] * k4[1])
        s += h
    return g, pv, qq


CASES = [(sp.Integer(1), sp.Integer(0)), (sp.Rational(-3, 2), sp.Integer(1)), (sp.Integer(2), sp.Rational(1, 2))]
m3_ok, m3_msgs = True, []
for Fv, Cv in CASES:
    nmax = 13 if (Fv, Cv) == (2, sp.Rational(1, 2)) else 9
    S9, f9, ok9, _ = solve_series(Fv, Cv, 9, lambda n: n // 2 + 1, sp.expand)
    S13 = solve_series(Fv, Cv, 13, lambda n: n // 2 + 1, sp.expand)[0] if nmax == 13 else None
    m3_ok &= ok9 and f9 == ['a_4_0']
    marks = [200, 100] + ([50] if nmax == 13 else [])
    res = {}
    for hdiv in (400, 800):
        g, pv = series_val(S9, 1000)
        q0 = -pv**2 / (2 * g * mp.mpf(1000)**-2)
        s_prev = mp.log(1000)
        for et in marks:
            s_next = mp.log(et)
            nst = int(mp.nint((s_prev - s_next) * hdiv))
            g, pv, q0 = rk4(g, pv, s_prev, s_next, nst, q0)
            res.setdefault(et, []).append((g, pv))
            s_prev = s_next
    for et in marks:
        (g1, p1), (g2, p2) = res[et]
        gR, pR = (16 * g2 - g1) / 15, (16 * p2 - p1) / 15
        g9, p9 = series_val(S9, et)
        dG, dP = abs(gR - g9), abs(pR - p9)
        line = f"(F, C) = ({Fv}, {Cv}) eta = {et}: |dG| {mp.nstr(dG, 3)}, |dp| {mp.nstr(dP, 3)} vs n<=9 series"
        if et == 50:
            g13, p13 = series_val(S13, et)
            dG13, dP13 = abs(gR - g13), abs(pR - p13)
            line += f"; vs n<=13 series |dG| {mp.nstr(dG13, 3)}, |dp| {mp.nstr(dP13, 3)}"
            m3_ok &= dG13 < 1e-10 and dP13 < 1e-10
        else:
            m3_ok &= dG < 1e-10 and dP < 1e-10
        line += f"; Richardson h-spread {mp.nstr(max(abs(g2 - g1), abs(p2 - p1)) / 15, 3)}"
        m3_msgs.append(line)
check('M3', m3_ok, "; ".join(m3_msgs))

# M4 -------------------------------------------------------------------------------------------------------------
print("\n== M4: the far field ==", flush=True)
U, eps = sp.symbols('U epsilon', nonzero=True)
w = -2 * U * rho**2 / x**2
Dff = sp.expand(D_static(U + eps * w))
cf = [sp.simplify(Dff.coeff(eps, k)) for k in range(7)]
low0 = all(c == 0 for c in cf[:3])
Zw = sp.diff(w, x, rho) / 2
c3_formula = -U * Zw**2 * ((1 - U**2) * sp.diff(w, x, 2) + sp.diff(w, rho, 2) + sp.diff(w, rho) / rho)
c3ok = sp.simplify(cf[3] - c3_formula) == 0
lims = [sp.limit(sp.simplify(cf[k] * x**8 / rho**2), x, sp.oo) for k in (3, 4, 5, 6)]
want = [128 * U**4, (128 if MUT == 'ff' else -128) * U**4, 0, 0]
m4 = low0 and c3ok and all(sp.simplify(a - b) == 0 for a, b in zip(lims, want))
check('M4', m4, f"eps^0..2 vanish: {low0}; eps^3 is section 7's formula: {c3ok}; x^8/rho^2 limits of eps^3..6: {lims}")

# M5 -------------------------------------------------------------------------------------------------------------
print("\n== M5: the reduced system ==", flush=True)
r_, s_, sig = sp.symbols('r s sigma')
Rred = sp.expand(sp.cancel(NTH.subs({p: nu**2 * r_, q: nu**2 * s_}) / nu**8))
try:
    PR = sp.Poly(Rred, nu)
    polyok = Rred.free_symbols <= {G, r_, s_, nu} and all(m[0] % 2 == 0 for m in PR.monoms())
except sp.PolynomialError:
    polyok = False
Rs = sp.expand(Rred.subs(nu, sp.sqrt(sig)))
R0ok = sp.expand(Rs.subs(sig, 0) + s_**2 * (r_**2 + 2 * G * s_)) == 0
pt = {r_: 4 * G, s_: -8 * G, sig: 0}
Rpt = sp.simplify(Rs.subs(pt))
Rsd = sp.simplify(sp.diff(Rs, s_).subs(pt))
Sr = sp.simplify(-sp.diff(Rs, r_).subs(pt) / Rsd)
SG = sp.simplify(-sp.diff(Rs, G).subs(pt) / Rsd)
Ssig = sp.simplify(-sp.diff(Rs, sig).subs(pt) / Rsd)
Jm = sp.Matrix([[0, 0, 4 * G], [SG, 2 + Sr, Ssig], [0, 0, -2]])
ev = Jm.eigenvals()
m5 = polyok and R0ok and Rpt == 0 and sp.simplify(Rsd + 128 * G**3) == 0 and Sr == (-3 if MUT == 'eig' else -4) and \
    SG == 8 and ev == {0: 1, -2: 2}
check('M5', m5, f"R polynomial in sigma = nu^2: {polyok}; R(G, r, s, 0) = -s^2(r^2 + 2Gs): {R0ok}; R = {Rpt}, dR/ds = "
      f"{Rsd} at (4G, -8G); dS/dr = {Sr}, dS/dG = {SG}; eigenvalues {ev}")

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)
