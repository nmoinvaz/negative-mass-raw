#!/usr/bin/env python3
"""ind146: the coordinator's independent check of #146 (Regge-Wheeler gauge and the condition at r_s).

Gauge: the coordinate Lie derivative (L_xi g)_ab = xi^c d_c g_ab + g_cb d_a xi^c + g_ac d_b xi^c and an own projection of h
onto the seven functions of zerilli_gauge_rs.md section 2, P_l explicit. r_s: DG06 (gr-qc/0604021) eqs. (3)-(4), (6),
(nv1), (RW17), (cz) typed from the arXiv TeX. Shares no code with zerilli_gauge_rs*.py, zerilli_derivation_lib.py,
ind143.py or ind145.py. Criteria Q0-Q5 in I146-mac/README.md.
"""
import argparse
import sys
import time

import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
ap.add_argument('--only', default='')
args = ap.parse_args()
MUT = args.mutate
ONLY = set(args.only.split(',')) if args.only else None
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.0f} s)", flush=True)
    if not ok:
        FAIL.append(name)


def want(q):
    return ONLY is None or q in ONLY


def zero(e):
    return sp.cancel(sp.together(e)) == 0


t, r, x, ph = sp.symbols('t r x phi')
M, s = sp.symbols('M s')
X = [t, r, x, ph]
F = 1 - 2 * M / r
g = sp.diag(-F, 1 / F, r**2 / (1 - x**2), r**2 * (1 - x**2))


def lie(xi):
    """(L_xi g)_ab for xi with upper indices."""
    out = sp.zeros(4)
    for a in range(4):
        for b in range(a, 4):
            v = sum(xi[c] * sp.diff(g[a, b], X[c]) for c in range(4))
            if MUT != 'lie':
                v += sum(g[c, b] * sp.diff(xi[c], X[a]) for c in range(4))
            v += sum(g[a, c] * sp.diff(xi[c], X[b]) for c in range(4))
            out[a, b] = out[b, a] = v
    return out


def xi_up(a, b, c, P, E):                              # xi^t = aPE, xi^r = bPE, xi_x = cP'E
    return [a * P * E, b * P * E, (1 - x**2) / r**2 * c * sp.diff(P, x) * E, 0]


def h_gen(fn, P, E, L):
    dP = sp.diff(P, x)
    Tn = x * dP - sp.Rational(L, 2) * P
    h = sp.zeros(4)
    h[0, 0] = F * fn['H0'] * P * E
    h[0, 1] = h[1, 0] = fn['H1'] * P * E
    h[1, 1] = fn['H2'] * P * E / F
    h[0, 2] = h[2, 0] = fn['Jt'] * dP * E
    h[1, 2] = h[2, 1] = fn['Jr'] * dP * E
    h[2, 2] = r**2 * E * (fn['K'] * P + fn['G'] * Tn) / (1 - x**2)
    h[3, 3] = r**2 * E * (fn['K'] * P - fn['G'] * Tn) * (1 - x**2)
    return h


def project(h, P, L):
    """The seven functions of h (t set to 0 after differentiation); ok = x-free and no odd or xphi parts."""
    h = h.subs(t, 0)
    dP = sp.diff(P, x)
    q = {'H0': h[0, 0] / (F * P), 'H1': h[0, 1] / P, 'H2': h[1, 1] * F / P, 'Jt': h[0, 2] / dP, 'Jr': h[1, 2] / dP}
    A = h[2, 2] * (1 - x**2) / r**2
    B = h[3, 3] / ((1 - x**2) * r**2)
    q['K'] = (A + B) / (2 * P)
    Tn = x * dP - sp.Rational(L, 2) * P
    q['G'] = (A - B) / (2 * Tn) if Tn != 0 else None
    q = {k: (sp.cancel(sp.together(v)) if v is not None else None) for k, v in q.items()}
    ok = all(v is None or not v.has(x) for v in q.values()) and all(zero(h[i, 3]) for i in range(3))
    return q, ok, sp.cancel(sp.together(A - B))


NAMES = ('H0', 'H1', 'H2', 'Jt', 'Jr', 'K', 'G')


def gauge_abc(q, sv):
    G_, Jt, Jr = q['G'], q['Jt'], q['Jr']
    c = -r**2 * G_ if MUT == 'gform' else -r**2 * G_ / 2
    b = -F * (Jr - r**2 * sp.diff(G_, r) / 2)
    a = (Jt - sv * r**2 * G_ / 2) / F
    return a, b, c


def rw_after(q, a, b, sv, L):
    W = q['Jr'] - r**2 * sp.diff(q['G'], r) / 2
    Fp = sp.diff(F, r)
    return {'K': q['K'] + sp.Rational(L, 2) * q['G'] - 2 * F / r * W,
            'H0': q['H0'] + Fp * W - 2 * sv * a,
            'H1': q['H1'] - F * sp.diff(a, r) - sv * W,
            'H2': q['H2'] + Fp * W + 2 * sp.diff(b, r)}


CASES = [(l, E, sv) for l in (2, 3, 4) for (E, sv) in ((sp.exp(s * t), s), (sp.Integer(1), sp.Integer(0)))]

# ---------------------------------------------------------------- Q0: planted, pure gauge
if want('Q0'):
    ok0, rows = True, []
    al, be, ga = [sp.Function(n)(r) for n in ('alpha', 'beta', 'gamma')]
    for l, E, sv in CASES:
        L = l * (l + 1)
        P = sp.legendre(l, x)
        h = lie(xi_up(al, be, ga, P, E))
        q, okp, _ = project(h, P, L)
        a, b, c = gauge_abc(q, sv)
        okx = zero(a + al) and zero(b + be) and zero(c + ga)
        hp = h + lie(xi_up(a, b, c, P, E))
        okh = all(zero(hp[i, j].subs(t, 0)) for i in range(4) for j in range(i, 4))
        ok0 = ok0 and okp and okx and okh
        rows.append(f"l = {l}, {'e^st' if sv != 0 else 'static'}: projection ok {okp}, xi = -eta {okx}, h' = 0 {okh}")
    check('Q0', ok0, '; '.join(rows))

# ---------------------------------------------------------------- Q1: the gauge solve on a general h
if want('Q1'):
    ok1, rows = True, []
    fn = {n: sp.Function(n)(r) for n in NAMES}
    for l, E, sv in CASES:
        L = l * (l + 1)
        P = sp.legendre(l, x)
        h = h_gen(fn, P, E, L)
        q, okp, _ = project(h, P, L)
        okq = okp and all(zero(q[n] - fn[n]) for n in NAMES)
        a, b, c = gauge_abc(fn, sv)
        hp = h + lie(xi_up(a, b, c, P, E))
        qp, okp2, _ = project(hp, P, L)
        okrw = okp2 and all(zero(qp[n]) for n in ('Jt', 'Jr', 'G'))
        want_ = rw_after(fn, a, b, sv, L)
        okf = all(zero(qp[n] - want_[n]) for n in ('K', 'H0', 'H1', 'H2'))
        ok1 = ok1 and okq and okrw and okf
        rows.append(f"l = {l}, {'e^st' if sv != 0 else 'static'}: projection inverts h_gen {okq}, J_t' = J_r' = G' = 0 {okrw}, "
                    f"K', H0', H1', H2' as the note {okf}")
    check('Q1', ok1, '; '.join(rows))

# ---------------------------------------------------------------- Q2: the seven Delta formulas, uniqueness, l = 1
if want('Q2'):
    ok2, rows = True, []
    a, b, c = [sp.Function(n)(r) for n in 'abc']
    E = sp.exp(s * t)
    Fp = sp.diff(F, r)
    for l in (2, 3, 4):
        L = l * (l + 1)
        P = sp.legendre(l, x)
        q, okp, _ = project(lie(xi_up(a, b, c, P, E)), P, L)
        note = {'Jt': -F * a + s * c, 'Jr': b / F + sp.diff(c, r) - 2 * c / r, 'G': 2 * c / r**2,
                'K': 2 * b / r - L * c / r**2, 'H0': -(Fp / F) * b - 2 * s * a, 'H1': -F * sp.diff(a, r) + s * b / F,
                'H2': -(Fp / F) * b + 2 * sp.diff(b, r)}
        bad = [n for n in NAMES if not zero(q[n] - note[n])]
        ok2 = ok2 and okp and not bad
        rows.append(f"l = {l}: Delta formulas differ in {bad}")
    P1 = sp.legendre(1, x)
    cc = sp.Function('c')(r)
    q1, okp1, amb = project(lie(xi_up(s * cc / F, -F * (sp.diff(cc, r) - 2 * cc / r), cc, P1, E)), P1, 2)
    fn = {n: sp.Function(n)(r) for n in NAMES}
    _, _, amb_gen = project(h_gen(fn, P1, E, 2), P1, 2)
    ok_l1 = okp1 and zero(q1['Jt']) and zero(q1['Jr']) and zero(amb) and zero(amb_gen)
    ok2 = ok2 and ok_l1
    rows.append(f"l = 1: traceless part of every h is 0 {zero(amb_gen)}; the c-family gives Delta J_t = Delta J_r = 0 and no "
                f"traceless part {okp1 and zero(q1['Jt']) and zero(q1['Jr']) and zero(amb)}")
    check('Q2', ok2, '; '.join(rows))

# ---------------------------------------------------------------- Q3-Q5: DG06 at r_s
lam, mu = sp.symbols('lambda mu')
z0, z1, z2, z3 = sp.symbols('z0 z1 z2 z3')
Mm = -mu / 2
Fm = 1 + mu / r
D = 2 * lam * r - 3 * mu
rs = 3 * mu / (2 * lam)


def Dr(e):
    return sp.diff(e, r) + z1 * sp.diff(e, z0) + z2 * sp.diff(e, z1) + z3 * sp.diff(e, z2)


psi = z0 / D
dpsi = Dr(psi)
fD = (lam * (lam + 1) * r**2 + 3 * lam * Mm * r + 6 * Mm**2) / (r**2 * (lam * r + 3 * Mm))
hD = (lam * r**2 - 3 * lam * r * Mm - 3 * Mm**2) / ((r - 2 * Mm) * (lam * r + 3 * Mm))
K3 = sp.cancel(fD * psi + Fm * dpsi)
H1_3 = sp.cancel(s * (hD * psi + r * dpsi))
H2_3 = sp.cancel(Dr(Fm * (hD * psi + r * dpsi)) - K3)
kk = (lam * r + mu) if MUT == 'nv1k' else (lam * r - mu)
K_nv = ((mu + r) * r * z1 + kk * z0) / (r**2 * D)
H1_nv = s * (2 * r * (mu + r) * z1 + mu * z0) / (r * (r + mu) * D)
H2_nv = ((r + mu) / D * z2 - (4 * lam * r**2 + 6 * lam * mu * r - 3 * mu**2) / (2 * r * D**2) * z1
         + (3 * mu**2 - 6 * lam * mu * r + 4 * lam**2 * r**2) / (2 * r**2 * D**2) * z0)
cstar = (1 if MUT == 'czs' else -1) * 2 * lam**2 / (3 * mu * (2 * lam + 3))
c_printed = 2 * lam**2 / (3 * mu * (2 * lam + 3))
k6 = 5 if MUT == 'rw17' else 6
Ozeta = ((r + mu)**2 / r**2 * z2 - (4 * lam * r**2 + k6 * lam * mu * r - 3 * mu**2) * (r + mu) / (r**3 * D) * z1
         - (r + mu) * (3 * mu**2 - 6 * lam * mu * r + 4 * lam**2 * r**2) / (r**4 * D) * z0)


def coef(e, z):
    return sp.cancel(sp.diff(e, z))


if want('Q3'):
    assert not H2_3.has(z3)
    a3 = zero(K_nv - K3)
    b3 = zero(H1_nv - 2 / r * H1_3)
    c3 = zero(coef(H2_3, z2) - coef(H2_nv, z2)) and zero(coef(H2_3, z1) - coef(H2_nv, z1)) and zero(coef(H2_3, z0) + coef(H2_nv, z0))
    check('Q3', a3 and b3 and c3, f"(a) K of (nv1) = K of (3) {a3}; (b) H1 of (nv1) = (2/r) H1 of (3) {b3}; (c) H2 of (3) = (nv1)'s H2 with "
          f"its zeta term reversed {c3}; ratio H1_nv/H1_3 = {sp.factor(sp.cancel(H1_nv / H1_3)) if not zero(H1_3) else None}")


def ratio_at_rs(e):
    v = sp.cancel(sp.cancel(e).subs(r, rs))
    assert not v.has(z2) and not v.has(z3), v
    return sp.factor(sp.cancel(-coef(v, z0) / coef(v, z1)))


if want('Q4'):
    ra = ratio_at_rs(sp.cancel(K3 * r**2 * D))
    rb = ratio_at_rs(sp.cancel((Ozeta - s**2 * z0) * r**4 * D))
    a4, b4 = zero(ra - cstar), zero(rb - cstar)
    c4 = zero(c_printed + cstar)
    d4 = zero(cstar.subs(mu, 2) - (-1 / ((3 / lam) * (3 / lam + 2))))
    check('Q4', a4 and b4 and c4 and d4, f"(a) K numerator at r_s: zeta'/zeta = {ra}, = c* {a4}; (b) (RW17) at r_s: zeta'/zeta = {rb}, "
          f"= c* {b4}, s-free {not rb.has(s)}; (c) printed (cz) = -c* {c4}; (d) c* at mu = 2 = -1/(r_s(r_s+2)) {d4}")

if want('Q5'):
    p0, p1 = sp.symbols('p0 p1')
    V = 2 * Fm * (lam**2 * r**2 * ((lam + 1) * r + 3 * Mm) + 9 * Mm**2 * (lam * r + Mm)) / (r**3 * (lam * r + 3 * Mm)**2)
    p2 = ((V + s**2) * p0 / Fm - sp.diff(Fm, r) * p1) / Fm
    zs = {z0: D * p0, z1: sp.diff(D, r) * p0 + D * p1, z2: 2 * sp.diff(D, r) * p1 + D * p2}
    res = sp.cancel(sp.together((Ozeta - s**2 * z0).subs(zs)))
    check('Q5', res == 0, f"(RW17) with zeta = (2 lambda r - 3 mu) psi and the Zerilli equation: residual {res}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL), f'({time.time() - T0:.0f} s)')
sys.exit(1 if FAIL else 0)
