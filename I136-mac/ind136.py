#!/usr/bin/env python3
"""ind136: the coordinator's independent check of #136's review of #133's Type III count of the tanh wall.

E1, E2 from the frame table of he_type3.md section 1 by sympy's charpoly, P as their resultant in w; the roots of P and of
y = B' - A' by a sign scan of the tanh form (mpmath, no intervals); the common root w at each root of P; a direct 2D Newton
solve of E1 = E2 = 0 in (r, w) with no resultant; the two ends as limits along the curve. Shares no code with
review_he_type3_count*.py, he_type3_count.py or he_type3.py. Criteria J1-J4 are in README.md, fixed before the first run.
"""
import argparse
import re
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument('--table', required=True)    # I136-rpi5/P_table.tsv, the Lean input
ap.add_argument('--printed', required=True)  # notes/warp/he_type3_output.txt, for the printed E2
ap.add_argument('--mutate', default=None)
args = ap.parse_args()
MUT = args.mutate
FAIL = []


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}", flush=True)
    if not ok:
        FAIL.append(name)


t0 = time.time()
print(f"ind136  mutation: {MUT}")

# ---------------------------------------------------------------- J1: the algebra
phi, A, B, w, X, g, y, cs, lam = sp.symbols('phi A B w X gamma y cs lam')
R00 = -X * (1 + w) / 2 + phi * (g + w * y)
R0x = g + (1 - w) * y / 2 if MUT != 'tab' else g - (1 - w) * y / 2   # tab: one sign of the typed table
R0r = -cs * y / 2
Rxx = X * (3 * w - 1) / 2 - phi * (g + w * y)
Rxr = cs * (X - phi * y / 2)
Rrr = X * (1 - w) / 2
Rm = sp.Matrix([[R00, R0x, R0r], [R0x, Rxx, Rxr], [R0r, Rxr, Rrr]])
M = sp.diag(-1, 1, 1) * Rm
cp = sp.Poly(sp.expand((lam * sp.eye(3) - M).det()), cs)
odd_zero = all(cp.coeff_monomial(cs**k) == 0 for k in (1, 3, 5))
cpw = sp.expand(sum(cp.coeff_monomial(cs**k) * (w * (1 - w))**(k // 2) for k in (0, 2, 4, 6)))
cl = sp.Poly(cpw, lam)
c2, c1, c0 = (cl.coeff_monomial(lam**k) for k in (2, 1, 0))
monic = cl.coeff_monomial(lam**3) == 1
E1x = sp.expand(c2**2 - 3 * c1)
E2x = sp.expand(27 * c0 - c2**3)
c2_pr = (4 * phi * (g + w * y) - X * (3 * w + 1)) / 2
E1_pr = (X**2 - phi * ((3 * w - 1) * g + 2 * w * y) * X + (phi**2 - 3) * g**2 + (2 * phi**2 * w + 3 * w - 3) * g * y
         + sp.Rational(1, 4) * (phi**2 * w**2 + 3 * phi**2 * w + 3 * w - 3) * y**2)
line = [ln for ln in open(args.printed) if 'polynomials:' in ln][0]
E2_str = re.search(r'E2 = (X\*\*3.*)$', line.strip()).group(1)
E2_pr = sp.sympify(E2_str, locals={'X': X, 'gamma': g, 'y': y, 'phi': phi, 'w': w})
e2_monos = len(sp.Poly(E2x, X, g, y).terms())
e2_cubic = all(sum(m) == 3 for m, _ in sp.Poly(E2x, X, g, y).terms())
ok1a = odd_zero and monic and sp.expand(c2 - c2_pr) == 0 and sp.expand(E1x - E1_pr) == 0 and sp.expand(E2x - E2_pr) == 0
check('J1a', ok1a and e2_monos == 10 and e2_cubic,
      f"cs odd powers vanish {odd_zero}, monic {monic}, c2 = printed {sp.expand(c2 - c2_pr) == 0}, E1 = printed "
      f"{sp.expand(E1x - E1_pr) == 0}, E2 = printed (he_type3_output.txt) {sp.expand(E2x - E2_pr) == 0}, E2 cubic form in "
      f"(X, gamma, y) {e2_cubic} with {e2_monos} monomials")

sub = {X: A**2, g: A, y: B - A}
E1 = sp.expand(E1x.subs(sub))
E2 = sp.expand(E2x.subs(sub))
n1, n2 = len(sp.Poly(E1, phi, A, B, w).terms()), len(sp.Poly(E2, phi, A, B, w).terms())
check('J1b', (n1, n2) == (17, 42), f"terms in (phi, A', B', w): E1 {n1}, E2 {n2} (claim 17, 42)")

ta = time.time()
Res = sp.resultant(E1, E2, w)
Pq, rem = sp.div(sp.Poly(Res, phi, A, B), sp.Poly(sp.Rational(27, 256) * phi**3 * (A - B)**3, phi, A, B))
P = Pq.as_expr()
exact_div = rem.is_zero
if MUT == 'drop':  # drop: the term phi^0 A'^4 B'^6 of P
    P = sp.expand(P - Pq.coeff_monomial(A**4 * B**6) * A**4 * B**6)
PP = sp.Poly(P, phi, A, B)
fl = sp.factor_list(P)
irreducible = len(fl[1]) == 1 and fl[1][0][1] == 1
degs = sorted({sum(m) for m in PP.monoms()})
check('J1c', exact_div and irreducible and len(PP.terms()) == 167 and degs == [10, 12, 14, 16, 18],
      f"Res_w(E1, E2) / ((27/256) phi^3 (A' - B')^3) exact {exact_div}, irreducible {irreducible}, "
      f"{len(PP.terms())} terms, total degrees {degs} ({time.time() - ta:.0f} s)")

tab = {}
for ln in open(args.table):
    if ln.startswith('#'):
        continue
    f = ln.rstrip('\n').split('\t')
    if f[0] == 'P':
        tab[(int(f[2]), int(f[3]), int(f[4]))] = sp.Rational(f[5])
mine = {m: c for m, c in PP.terms()}
check('J1d', mine == tab, f"P equals I136-rpi5/P_table.tsv term by term: {mine == tab} ({len(tab)} table rows)")

jk = sorted({m[1] + m[2] for m in PP.monoms()})
kmax = max(m[2] for m in PP.monoms())
check('J1e', min(jk) >= 9 and kmax <= 9 and jk == list(range(9, 16)),
      f"(A', B')-degrees j + k of P: {jk}; max B'-degree k = {kmax}")

ps, dl = sp.symbols('psi delta')
Ph = sp.Poly(sp.expand(P.subs({A: ps - 2 * phi, B: ps - 2 * phi + dl}, simultaneous=True)), phi, ps, dl)
wts = sorted({2 * m[0] + 4 * m[1] + 4 * m[2] for m in Ph.monoms()})
w24 = sum(c * phi**m[0] * ps**m[1] * dl**m[2] for m, c in Ph.terms() if 2 * m[0] + 4 * m[1] + 4 * m[2] == 24)
check('J1f', len(Ph.terms()) == 358 and wts[0] == 24 and sp.expand(w24 - 774144 * phi**8 * dl**2) == 0,
      f"P-hat has {len(Ph.terms())} terms, weights {wts[0]}..{wts[-1]}, weight-24 part {w24}")

# ---------------------------------------------------------------- numerics on the tanh form
PT = [(m[0], m[1], m[2], c.p, c.q) for m, c in PP.terms()]
E1c = [sp.lambdify((phi, A, B), c, 'mpmath') for c in sp.Poly(E1, w).all_coeffs()]  # highest power first
E2c = [sp.lambdify((phi, A, B), c, 'mpmath') for c in sp.Poly(E2, w).all_coeffs()]


def jets(r, s, Rb, v):
    """phi, A', B' of the tanh profile f = [tanh s(r + Rb) - tanh s(r - Rb)] / (2 tanh s Rb), analytic derivatives."""
    tp, tm, t0_ = mp.tanh(s * (r + Rb)), mp.tanh(s * (r - Rb)), mp.tanh(s * Rb)
    hp, hm = mp.sech(s * (r + Rb))**2, mp.sech(s * (r - Rb))**2
    f = (tp - tm) / (2 * t0_)
    f1 = s * (hp - hm) / (2 * t0_)
    f2 = -2 * s**2 * (hp * tp - hm * tm) / (2 * t0_)
    return v * (1 - f), v * r * f1, v * r**2 * f2


def Pval(ph, a, b):
    pw = [[mp.mpf(1)], [mp.mpf(1)], [mp.mpf(1)]]
    for k, x in enumerate((ph, a, b)):
        for _ in range(18):
            pw[k].append(pw[k][-1] * x)
    return mp.fsum(mp.mpf(p) / q * pw[0][i] * pw[1][j] * pw[2][k] for i, j, k, p, q in PT)


WALLS = {  # sigma, R_b, v, z_t; roots of P and y and the common w, T from review_he_type3_count.md / he_type3_count.md
    'le': dict(s=8, Rb=1, v=mp.mpf(1) / 2, zt=40,
               P=['0.9905678898', '1.006345187', '1.023933261', '1.094662309'], Y='0.9921149667',
               W=['0.06005176468', '58.459064', '0.04098687975', '0.9128666766'],
               adm=[('0.990567889806', '-8.80794'), ('1.02393326111', '7.90635'), ('1.09466230932', '22.0305')],
               G0='1.09451e-67', Sb='0.49998278'),
    'rodal': dict(s=4, Rb=5, v=mp.mpf(1), zt=60,
                  P=['4.714485178', '5.020434866', '5.033740947', '5.071066343', '5.076353993', '5.103380564'],
                  Y='4.993740859',
                  W=['0.9576393947', '4.1006549', '8.7172638', '0.2847666782', '1.030003', '0.9770299367'],
                  adm=[('4.71448517823', '-4.51919'), ('5.07106634302', '3.7259'), ('5.10338056385', '4.97171')],
                  G0='6.58941e-169', Sb='3.9999386'),
}

for name, W in WALLS.items():
    mp.mp.dps = 80
    s0, Rb, v, zt = W['s'], W['Rb'], W['v'], W['zt']
    s = mp.mpf(s0) + (mp.mpf('1e-3') if MUT == 'sig' else 0)  # sig: sigma + 1e-3 in the profile
    Pr = lambda r: Pval(*jets(r, s, Rb, v))
    Yr = lambda r: (lambda j: j[2] - j[1])(jets(r, s, Rb, v))

    # J2: sign scan in z = 2 sigma r over [1/4, z_t], step 1e-3, then bisection to 1e-40
    ta = time.time()
    N = int((zt - mp.mpf(1) / 4) * 1000)
    rs = [(mp.mpf(1) / 4 + mp.mpf(i) / 1000) / (2 * s0) for i in range(N + 1)]
    roots = {}
    for lab, fn in (('P', Pr), ('y', Yr)):
        vals = [fn(r) for r in rs]
        zero_hit = any(x == 0 for x in vals)
        out = []
        for i in range(N):
            if vals[i] * vals[i + 1] < 0:
                a, b, fa = rs[i], rs[i + 1], vals[i]
                for _ in range(140):
                    m = (a + b) / 2
                    fm = fn(m)
                    if fm * fa > 0:
                        a, fa = m, fm
                    else:
                        b = m
                out.append((a + b) / 2)
        roots[lab] = (out, zero_hit)
    pr, yr = roots['P'][0], roots['y'][0]
    dP = [abs(x - mp.mpf(e)) for x, e in zip(pr, W['P'])] if len(pr) == len(W['P']) else [mp.inf]
    dY = abs(yr[0] - mp.mpf(W['Y'])) if len(yr) == 1 else mp.inf
    check(f'J2:{name}', len(pr) == len(W['P']) and len(yr) == 1 and max(dP) < 1e-9 and dY < 1e-9
          and not roots['P'][1] and not roots['y'][1],
          f"{N + 1} radii, z step 1e-3: P {len(pr)} sign changes at r = {[mp.nstr(x, 11) for x in pr]} "
          f"(max |diff| {mp.nstr(max(dP), 2)}), y {len(yr)} at r = {[mp.nstr(x, 11) for x in yr]} "
          f"(|diff| {mp.nstr(dY, 2)}) ({time.time() - ta:.0f} s)")

    # J3a: the common root w of E1, E2 at each root of P, and the admissible ones
    lo, hi = (0, 100) if MUT == 'win' else (0, 1)  # win: the admissible window (0, 100)
    rows, adm, ok3a = [], [], len(pr) == len(W['W'])
    for idx, r in enumerate(pr):
        ph, a, b = jets(r, s, Rb, v)
        e = [c(ph, a, b) for c in E1c]
        f = [c(ph, a, b) for c in E2c]
        rel = []
        for x in mp.polyroots(e, maxsteps=200, extraprec=200):
            sc = mp.fsum(abs(c) * abs(x)**(len(f) - 1 - k) for k, c in enumerate(f))
            rel.append((abs(mp.polyval(f, x)) / sc, x))
        rel.sort(key=lambda t: t[0])
        wc = rel[0][1]
        sep = rel[0][0] < 1e-20 and all(t[0] > 1e-6 for t in rel[1:])
        T = (a + b) / (v * r**2)
        good = abs(mp.im(wc)) < 1e-30 and sep
        if idx < len(W['W']):
            good = good and abs(mp.re(wc) - mp.mpf(W['W'][idx])) <= 1e-6 * max(1, abs(mp.mpf(W['W'][idx])))
        ok3a = ok3a and good
        wr = mp.re(wc)
        rows.append(f"r {mp.nstr(r, 11)}: w {mp.nstr(wr, 11)} (rel |E2| {mp.nstr(rel[0][0], 2)}, other root "
                    f"{mp.nstr(rel[1][0], 2) if len(rel) > 1 else '-'}), T {mp.nstr(T, 7)}")
        if lo < wr < hi and abs(T) > 1e-6:
            adm.append((r, wr, T))
    dadm = []
    if len(adm) == len(W['adm']):
        for (r, wr, T), (re_, Te) in zip(adm, W['adm']):
            dadm.append(max(abs(r - mp.mpf(re_)) / 1e-9, abs(T - mp.mpf(Te)) / 1e-4))
    check(f'J3a:{name}', ok3a and len(adm) == 3 and len(dadm) == 3 and max(dadm) < 1,
          f"{len(adm)} admissible of {len(pr)} roots of P; " + '; '.join(rows))

    # J3b: re-solve E1 = E2 = 0 in (r, w) directly, no resultant, from (r, w) rounded to 4 and 3 decimals
    mp.mp.dps = 80
    def F2(r, ww):
        ph, a, b = jets(r, s, Rb, v)
        return [mp.polyval([c(ph, a, b) for c in E1c], ww), mp.polyval([c(ph, a, b) for c in E2c], ww)]
    res3b = []
    ok3b = True
    for (re_, Te), wi in zip(W['adm'], [x for x in W['W'] if 0 < float(x) < 1]):
        x0 = [mp.mpf(round(float(re_), 4)), mp.mpf(round(float(wi), 3))]
        try:
            sol = mp.findroot(F2, x0, tol=mp.mpf(10)**-70, maxsteps=100, verify=False)
            rr, ww = sol[0], sol[1]
            ph, a, b = jets(rr, s, Rb, v)
            sc1 = mp.fsum(abs(c(ph, a, b)) * abs(ww)**(2 - k) for k, c in enumerate(E1c))
            sc2 = mp.fsum(abs(c(ph, a, b)) * abs(ww)**(3 - k) for k, c in enumerate(E2c))
            r1, r2 = F2(rr, ww)
            resid = max(abs(r1) / sc1, abs(r2) / sc2)
            d = abs(rr - mp.mpf(re_))
            ok3b = ok3b and resid < 1e-40 and d < 1e-9
            res3b.append(f"r {mp.nstr(rr, 13)} (|diff| {mp.nstr(d, 2)}), w {mp.nstr(ww, 11)}, residual {mp.nstr(resid, 2)}")
        except Exception as ex:  # noqa: BLE001
            ok3b = False
            res3b.append(f"no convergence from {x0}: {ex}")
    check(f'J3b:{name}', ok3b, '; '.join(res3b))

    # J3c: at the root of y, the leading coefficients of E1 and E2 vanish and no root of E1 with |w| <= 1e4 is one of E2
    ry = pr[0] if MUT == 'yatp' else (yr[0] if yr else mp.mpf(W['Y']))  # yatp: test at a root of P
    ph, a, b = jets(ry, s, Rb, v)
    e = [c(ph, a, b) for c in E1c]
    f = [c(ph, a, b) for c in E2c]
    lead = (abs(e[0]) / max(abs(x) for x in e), abs(f[0]) / max(abs(x) for x in f))
    e_trim = e[1:] if lead[0] < 1e-20 else e
    rel = []
    for x in mp.polyroots(e_trim, maxsteps=200, extraprec=200):
        if abs(x) <= 1e4:
            sc = mp.fsum(abs(c) * abs(x)**(len(f) - 1 - k) for k, c in enumerate(f))
            rel.append(abs(mp.polyval(f, x)) / sc)
    check(f'J3c:{name}', lead[0] < 1e-20 and lead[1] < 1e-20 and all(t > 1e-6 for t in rel),
          f"at r = {mp.nstr(ry, 11)}: leading coefficients relative {mp.nstr(lead[0], 2)}, {mp.nstr(lead[1], 2)}; "
          f"roots of E1 with |w| <= 1e4: {len(rel)}, min relative |E2| there {mp.nstr(min(rel), 3) if rel else '-'}")

    # J4a: P/z^24 -> G(0) at z = 1e-3, and P > 0, y < 0 at 500 points of (0, 1/4]
    mp.mp.dps = 160
    z = mp.mpf('1e-3')
    G = Pr(z / (2 * s0)) / z**24
    dG = abs(G / mp.mpf(W['G0']) - 1)
    zs = [mp.mpf('1e-3') + (mp.mpf(1) / 4 - mp.mpf('1e-3')) * i / 499 for i in range(500)]
    pos = all(Pr(zz / (2 * s0)) > 0 for zz in zs)
    neg = all(Yr(zz / (2 * s0)) < 0 for zz in zs)
    check(f'J4a:{name}', dG < 1e-4 and pos and neg,
          f"P/z^24 at z = 1e-3: {mp.nstr(G, 7)} against {W['G0']} (relative {mp.nstr(dG, 2)}); P > 0 at 500 points of "
          f"[1e-3, 1/4]: {pos}; y < 0 there: {neg}")

    # J4b: S = P/(tau z)^9 along [z_t, 300] stays above #136's lower bound and tends to 4 v^3; y > 0 there
    mp.mp.dps = 80
    C = mp.cosh(2 * s0 * Rb)
    zlo = 4 if MUT == 'zt' else zt  # zt: start at z = 4
    zs = [mp.mpf(zlo) + (mp.mpf(300) - zlo) * i / 999 for i in range(1000)]
    Sv, ypos = [], True
    for zz in zs:
        tau = 2 * v * (1 + C) * zz * mp.exp(-zz)
        r = zz / (2 * s0)
        Sv.append(Pr(r) / (tau * zz)**9)
        ypos = ypos and Yr(r) > 0
    # run 2 (after run 1's failure of the limit test at z = 300): S = sum_n L_n z^-n + O(e^-z) with
    # L_n = sum_i (-1)^n c_(i, n, 9 - n) v^i, exact from this script's P; L_0 must be 4 v^3 and S(300) must match the sum
    vq = sp.Rational(1, 2) if name == 'le' else sp.Rational(1)  # run 3: v as an exact rational (run 2 crashed here)
    Ln = [sum((-1)**n * c * vq**m[0] for m, c in PP.terms() if m[1] == n and m[2] == 9 - n) for n in range(10)]
    ser = mp.fsum(mp.mpf(x.p) / x.q / mp.mpf(300)**n for n, x in enumerate(Ln))
    dser = abs(Sv[-1] / ser - 1)
    check(f'J4b:{name}', min(Sv) >= mp.mpf(W['Sb']) and Ln[0] == 4 * vq**3 and dser < 1e-6 and ypos,
          f"min S over 1000 points of [{zlo}, 300]: {mp.nstr(min(Sv), 9)} (bound {W['Sb']}); L_0 = {Ln[0]} (4 v^3 = "
          f"{4 * vq**3}), L_1 = {Ln[1]}; S(300) = {mp.nstr(Sv[-1], 12)} against sum L_n 300^-n = {mp.nstr(ser, 12)} "
          f"(relative {mp.nstr(dser, 2)}); y > 0: {ypos}")

print(f"{'ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL)}  ({time.time() - t0:.0f} s)")
sys.exit(1 if FAIL else 0)
