#!/usr/bin/env python3
"""Coordinator's independent check of #142 (Lemma A(iii), L2-L6, the Zerilli V). Criteria H1-H7 in I142-mac/README.md,
fixed before the first run. Shares no code with review_lemma_a3_*.py or #2's scripts; formulas typed from RESULTS.md.
Usage: ind142.py [--mutate=shift|ident|qform|zr|xlog|kp1|c5|vz]"""
import sys
import time
import traceback
from fractions import Fraction as Fr
from math import factorial

import mpmath as mp
import sympy as sp

ARGS = dict(a.lstrip('-').split('=', 1) for a in sys.argv[1:])
MUT = ARGS.get('mutate')
assert MUT in (None, 'shift', 'ident', 'qform', 'zr', 'xlog', 'kp1', 'c5', 'vz'), MUT
failed = []


def check(cid, name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + cid + ' ' + name + ('  ' + detail if detail else ''), flush=True)
    if not ok and cid not in failed:
        failed.append(cid)


def guarded(cid, fn):
    try:
        fn()
    except Exception:
        check(cid, 'crashed', False, traceback.format_exc().strip().splitlines()[-1])


def poch(a, m):
    """Rising factorial (a)_m for integer m, (a)_{-m} = 1/((a-1)...(a-m))."""
    p = 1
    if m >= 0:
        for j in range(m):
            p *= a + j
        return Fr(p)
    for j in range(1, -m + 1):
        p *= a - j
    return Fr(1, p)


def cn(l, n):
    """Lemma A: c_n = (n-2)((n-4)l(l+1)+n-1)(l-n+3)_{2n-4}/(2^n (n-1)!^2)."""
    return Fr((n - 2) * ((n - 4) * l * (l + 1) + n - 1)) * poch(l - n + 3, 2 * n - 4) / (2 ** n * factorial(n - 1) ** 2)


def chi_over_r(l):
    """Coefficients p_j of chi/r = sum_j p_j r^j, j = 0..l+1 (p_j = c_{j+1})."""
    return [cn(l, j + 1) for j in range(l + 2)]


def Kof(l):
    return (l - 1) * l * (l + 1) * (l + 2)


def horner(p, r):
    v = 0
    for a in reversed(p):
        v = v * r + a
    return v


def dpoly(p):
    return [j * p[j] for j in range(1, len(p))]


# ---------------- H1: chi/r has no root in [0, inf)
def h1():
    bad = []
    for l in list(range(2, 51)) + [75, 100]:
        p = chi_over_r(l)
        assert cn(l, l + 3) == 0 and p[-1] > 0
        if MUT == 'shift' and l == 3:
            p = [p[0] - Fr(51, 100)] + p[1:]
        P = sp.Poly([sp.Rational(a.numerator, a.denominator) for a in reversed(p)], sp.Symbol('r'))
        iv = P.intervals(inf=0)
        if iv:
            bad.append((l, len(iv)))
    check('H1', 'chi/r has no root in [0, inf) for l = 2..50, 75, 100 (Poly.intervals)', not bad, f'roots at {bad}' if bad else '')


# ---------------- H2a: the identity, K-24 factorization, c3..c5
def h2a():
    K, l = sp.symbols('K l')
    e = 6 if MUT != 'ident' else 6
    sh = 24 if MUT != 'ident' else 23
    ident = sp.expand(K ** 2 * 6 * (K - 18) - (18 * (K - 16)) ** 2 - e * (K - sh) ** 3)
    check('H2a', '(Ks)^2 - (18(K-16))^2 - 6(K-24)^3 = 0 with s^2 = 6(K-18)', ident == 0, f'residual {ident}')
    fac = sp.expand((l - 1) * l * (l + 1) * (l + 2) - 24 - (l - 2) * (l + 3) * (l ** 2 + l + 4))
    check('H2a', 'K - 24 = (l-2)(l+3)(l^2+l+4)', fac == 0, f'residual {fac}')
    bad = [l_ for l_ in range(2, 61) if (cn(l_, 3), cn(l_, 4), cn(l_, 5)) !=
           (Fr(-Kof(l_), 32), Fr(Kof(l_), 96), Fr(Kof(l_) * (Kof(l_) - 24), 6144))]
    check('H2a', 'c3, c4, c5 = -K/32, K/96, K(K-24)/6144 for l = 2..60', not bad, f'bad l {bad}' if bad else '')


# ---------------- H2b: r0, q(r0) closed form, minima of chi/r
def h2b():
    mp.mp.dps = 60
    worst_r0 = worst_q = mp.mpf(0)
    neg = []
    for l in range(3, 51):
        K = mp.mpf(Kof(l))
        a, b, d = K / 32, K / 96, mp.mpf(cn(l, 5).numerator) / cn(l, 5).denominator
        rts = mp.polyroots([4 * d, 3 * b, -2 * a], maxsteps=200, extraprec=200)
        pos = [mp.re(x) for x in rts if abs(mp.im(x)) < mp.mpf('1e-40') and mp.re(x) > 0]
        assert len(pos) == 1, (l, rts)
        r0 = pos[0]
        s = mp.sqrt(6 * (K - 18))
        worst_r0 = max(worst_r0, abs(r0 - 24 / (s + 6)) / r0)
        q0 = mp.mpf(3) / 2 - a * r0 ** 2 + b * r0 ** 3 + d * r0 ** 4
        k16 = 15 if MUT == 'qform' else 16
        closed = 4 * (K - 18) * (K * s - 18 * (K - k16)) / (K - 24) ** 3
        worst_q = max(worst_q, abs(q0 - closed) / abs(closed))
        if not closed > 0:
            neg.append(l)
        if l <= 30:
            p = chi_over_r(l)
            dp = dpoly(p)
            pm = [mp.mpf(x.numerator) / x.denominator for x in p]
            dm = [mp.mpf(x.numerator) / x.denominator for x in dp]
            crit = mp.polyroots(list(reversed(dm)), maxsteps=500, extraprec=500)
            cpos = [mp.re(x) for x in crit if abs(mp.im(x)) < mp.mpf('1e-30') and mp.re(x) > 0]
            mins = [horner(pm, x) for x in cpos]
            ok = bool(cpos) and min(mins) >= closed * (1 - mp.mpf('1e-30')) and min(mins) > 0
            if not ok:
                neg.append(('chi', l, [mp.nstr(m, 8) for m in mins]))
    check('H2b', 'positive root of q\'/r = 24/(s+6), l = 3..50', worst_r0 < mp.mpf('1e-40'), f'max rel {mp.nstr(worst_r0, 3)}')
    check('H2b', 'q(r0) = 4(K-18)(Ks-18(K-16))/(K-24)^3 > 0, l = 3..50; min chi/r >= q(r0) > 0, l = 3..30',
          worst_q < mp.mpf('1e-40') and not neg, f'max rel {mp.nstr(worst_q, 3)}, bad {neg}')
    p2 = chi_over_r(2)
    check('H2b', 'l = 2: chi/r = 3/2 - (3/4)r^2 + (1/4)r^3, value 1/2 at r = 2',
          p2 == [Fr(3, 2), 0, Fr(-3, 4), Fr(1, 4)] and horner(p2, Fr(2)) == Fr(1, 2), str(p2))


# ---------------- H3: Taylor coefficients of r^4 Vhat at 0
def h3():
    r = sp.Symbol('r')
    bad = []
    for l in range(2, 13):
        c = (l + 2) * (l - 1)
        chi = sum(sp.Rational(x.numerator, x.denominator) * r ** n for n, x in enumerate([Fr(0)] + [cn(l, n) for n in range(1, l + 3)]))
        psi = chi / (c * r - 6)
        f = 1 + 2 / r
        g = (1 if MUT == 'zr' else f) * sp.diff(psi, r) / psi
        vh = sp.cancel(r ** 4 * (g ** 2 - f * sp.diff(g, r)))
        N, D = sp.fraction(vh)
        N, D = sp.Poly(N, r), sp.Poly(D, r)
        nc = [N.coeff_monomial(r ** i) for i in range(3)]
        dc = [D.coeff_monomial(r ** i) for i in range(3)]
        if dc[0] == 0:
            bad.append((l, 'pole'))
            continue
        t0 = nc[0] / dc[0]
        t1 = (nc[1] - t0 * dc[1]) / dc[0]
        t2 = (nc[2] - t0 * dc[2] - t1 * dc[1]) / dc[0]
        if (t0, t1, t2) != (12, 2 * (l * l + l + 3), l * (l + 1)):
            bad.append((l, t0, t1, t2))
    check('H3', 'r^4 Vhat = 12 + 2(l^2+l+3) r + l(l+1) r^2 + O(r^3), l = 2..12', not bad, f'bad {bad[:3]}' if bad else '')


# ---------------- common numeric pieces
def V_of(l, r):
    lam = mp.mpf((l + 2) * (l - 1)) / 2
    f = 1 + 2 / r
    return 2 * f * (lam ** 2 * r ** 2 * ((lam + 1) * r - 3) + 9 * (lam * r - 1)) / (r ** 3 * (lam * r - 3) ** 2)


# ---------------- H4: x-series of Vhat at 0 (DG09 eq. (61))
def h4():
    mp.mp.dps = 100
    rows = []
    ok = True
    for l in (2, 3, 7):
        c = (l + 2) * (l - 1)
        p = [mp.mpf(x.numerator) / x.denominator for x in [Fr(0)] + [cn(l, n) for n in range(1, l + 3)]]
        dp = dpoly(p)
        r = mp.mpf('1e-10')
        f = 1 + 2 / r
        g = f * (horner(dp, r) / horner(p, r) - c / (c * r - 6))
        vh = 2 * g ** 2 - V_of(l, r)
        x = r - 2 * mp.log(1 + r / 2) + (r ** 3 / 1000 if MUT == 'xlog' else 0)
        R = x * (vh - mp.mpf(3) / (4 * x ** 2) - mp.mpf(l * l + l - 1) / (4 * x ** mp.mpf(1.5)))
        C = x ** mp.mpf(1.5) * (vh - mp.mpf(3) / (4 * x ** 2))
        okl = abs(R) < mp.mpf('1e-6') and abs(R + mp.mpf(l * (l + 1)) / 4) > 1 and abs(C - mp.mpf(l * l + l - 1) / 4) < mp.mpf('1e-6')
        ok &= okl
        rows.append(f'l={l}: x^-1 coeff {mp.nstr(R, 3)} (DG {-l * (l + 1) / 4}), x^-3/2 coeff {mp.nstr(C, 12)}')
    check('H4', 'Vhat = 3/(4x^2) + (l^2+l-1)/(4x^1.5) + 0/x + ..., not DG09 (61)\'s -l(l+1)/(4x)', ok, '; '.join(rows))


# ---------------- H5: DG mode identity, analytic derivatives
def h5():
    mp.mp.dps = 60
    worst = mp.mpf(0)
    for l in range(2, 9):
        c = (l + 2) * (l - 1)
        k = mp.mpf(c * (c + 2)) / 6 + (1 if MUT == 'kp1' else 0)
        rs = mp.mpf(6) / c
        for r in (mp.mpf('0.05'), rs / 2, 3 * rs, mp.mpf(1), mp.mpf(4)):
            W = r * (r + 2) ** k * mp.exp(-k * r / 2)
            u = 1 / r + k / (r + 2) - k / 2
            W1 = W * u
            W2 = W * (u ** 2 - 1 / r ** 2 - k / (r + 2) ** 2)
            D = c * r - 6
            P = W / D
            P1 = W1 / D - c * W / D ** 2
            P2 = W2 / D - 2 * c * W1 / D ** 2 + 2 * c ** 2 * W / D ** 3
            f = 1 + 2 / r
            Pxx = f ** 2 * P2 + f * (-2 / r ** 2) * P1
            res = -Pxx + V_of(l, r) * P + (k / 2) ** 2 * P
            worst = max(worst, abs(res) / ((k / 2) ** 2 * abs(P)))
    check('H5', 'H_Z Psi_DG = -(k/2)^2 Psi_DG, l = 2..8, 5 points each', worst < mp.mpf('1e-25'), f'max rel residual {mp.nstr(worst, 3)}')


# ---------------- H6: Psi-hat at 0 and at r_s
def h6():
    mp.mp.dps = 100
    rows = []
    worst = mp.mpf(0)
    for l in range(2, 7):
        c = (l + 2) * (l - 1)
        k0 = mp.mpf(c * (c + 2)) / 6
        k = k0 + (1 if MUT == 'kp1' else 0)
        pf = [Fr(0)] + [cn(l, n) for n in range(1, l + 3)]
        if MUT == 'c5':
            pf[5] = pf[5] * (1 + Fr(1, 1000))
        p = [mp.mpf(x.numerator) / x.denominator for x in pf]
        dp = dpoly(p)
        r = mp.mpf('1e-12')
        W = r * (r + 2) ** k * mp.exp(-k * r / 2)
        u = 1 / r + k / (r + 2) - k / 2
        ph = (1 + 2 / r) * W * (horner(dp, r) / horner(p, r) - u) / (c * r - 6)
        want = 2 ** k0 * k0 ** 2 / 192
        rel = abs(ph / r ** 3 - want) / want
        worst = max(worst, rel)
        rows.append(f'l={l} rel {mp.nstr(rel, 3)}')
    check('H6a', 'Psi-hat / r^3 -> 2^k k^2/192 at r = 1e-12, l = 2..6', worst < mp.mpf('1e-6'), ', '.join(rows))
    worst = mp.mpf(0)
    for l in range(2, 31):
        c = (l + 2) * (l - 1)
        k = mp.mpf(c * (c + 2)) / 6 + (1 if MUT == 'kp1' else 0)
        p = [mp.mpf(x.numerator) / x.denominator for x in [Fr(0)] + [cn(l, n) for n in range(1, l + 3)]]
        rs = mp.mpf(6) / c
        u = 1 / rs + k / (rs + 2) - k / 2
        worst = max(worst, abs(horner(dpoly(p), rs) / horner(p, rs) - u) / abs(u))
    check('H6b', 'W\'/W = chi\'/chi at r_s (Psi-hat regular there), l = 2..30', worst < mp.mpf('1e-50'), f'max rel {mp.nstr(worst, 3)}')


# ---------------- H7: V against the standard Zerilli form
def h7():
    r, lam, M, l = sp.symbols('r lambda M l')
    Vt = 2 * (1 - 2 * M / r) * (lam ** 2 * (lam + 1) * r ** 3 + 3 * lam ** 2 * M * r ** 2 + 9 * lam * M ** 2 * r + 9 * M ** 3) / (r ** 3 * (lam * r + 3 * M) ** 2)
    a3 = 2 if MUT == 'vz' else 3
    Vr = 2 * (1 + 2 / r) * (lam ** 2 * r ** 2 * ((lam + 1) * r - a3) + 9 * (lam * r - 1)) / (r ** 3 * (lam * r - 3) ** 2)
    d = sp.cancel(Vt.subs(M, -1) - Vr)
    check('H7', 'standard Zerilli V at M = -1 equals RESULTS\' V', d == 0, f'difference {d}' if d != 0 else '')
    lim = sp.limit(r ** 2 * Vt, r, sp.oo)
    ll = sp.expand(lim.subs(lam, (l - 1) * (l + 2) / 2) - l * (l + 1))
    check('H7', 'r^2 V -> 2(lambda+1) = l(l+1) for any M', sp.simplify(lim - 2 * (lam + 1)) == 0 and ll == 0, f'limit {lim}')


t00 = time.time()
print(f'ind142 mutation={MUT}', flush=True)
for cid, fn in (('H1', h1), ('H2a', h2a), ('H2b', h2b), ('H3', h3), ('H4', h4), ('H5', h5), ('H6', h6), ('H7', h7)):
    t0 = time.time()
    guarded(cid, fn)
    print(f'    [{cid} {time.time() - t0:.1f} s]', flush=True)
print(f'FAILED: {failed}' if failed else 'ALL PASS', f'({time.time() - t00:.0f} s)')
sys.exit(1 if failed else 0)
