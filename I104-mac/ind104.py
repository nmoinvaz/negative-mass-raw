#!/usr/bin/env python3
"""Coordinator's independent check of #104 (review of RESULTS.md 4.2-4.5). Criteria F1a-F7 in I104-mac/README.md,
fixed before the first run. Shares no code with review_large_l_*.py or #2's scripts; formulas typed from RESULTS.md.
Works in r with Lemma A's c_n, V-hat from its definition g^2 - g_x. 60-digit mpf: numerical evidence, not intervals.
Usage: ind104.py --csv=PATH [--mutate=cn|vsign|rho|csv|l2|sM|vhat]"""
import sys
import time
from mpmath import mp, mpf, besseli, sqrt, fabs
import sympy as sp

mp.dps = 60
ARGS = dict(a.lstrip('-').split('=', 1) for a in sys.argv[1:] if '=' in a)
MUT = ARGS.get('mutate')
CSV = ARGS['csv']
MUTS = ('cn', 'vsign', 'rho', 'csv', 'l2', 'sM', 'vhat')
assert MUT in (None,) + MUTS, MUT

L_SET = list(range(2, 31)) + [80, 100, 137, 138, 139, 499, 500, 501, 502, 1000, 1001, 2000, 2999, 3000]
L_SET += [36, 464, 864, 1461, 1644, 1995]  # random.Random(10404).sample(range(31, 3001), 6)
L_SET = sorted(set(L_SET))
RHO_104 = (mpf('8.485700967373530340930500822'), mpf('9.6359894425861440206961577'))  # review_large_l_roots_output
if MUT == 'rho':
    RHO_104 = (RHO_104[0] + mpf('1e-23'), RHO_104[1])
S_L2, S_NEG_L2 = mpf('3.5525479'), mpf('6.6818585')  # #104 second-order Theorem L, l >= 138
S_M, S_NEG_M = mpf('3.5186068'), mpf('5.9363952')    # #104 Theorem M, l >= 500
if MUT == 'sM':
    S_M = mpf('3.515')
TABLE = {  # RESULTS 4.3: c r_*, c r_neg, l^2 r_*, l^2 r_neg
    2: ('9.115122', '10.696286', '9.115122', '10.696286'), 3: ('8.789041', '10.143519', '7.910137', '9.129167'),
    5: ('8.604503', '9.833910', '7.682592', '8.780277'), 10: ('8.517779', '9.689316', '7.886832', '8.971589'),
    20: ('8.494079', '9.649909', '8.128306', '9.234363'), 80: ('8.486244', '9.636891', '8.384063', '9.520855'),
    100: ('8.486049', '9.636568', '8.403693', '9.543046'), 500: ('8.485715', '9.636013', '8.468845', '9.616856'),
    1000: ('8.485704', '9.635995', '8.477244', '9.626388'), 3000: ('8.485701', '9.635990', '8.482876', '9.632781')}

failed = []


def check(cid, name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + cid + ' ' + name + ('  ' + detail if detail else ''), flush=True)
    if not ok and cid not in failed:
        failed.append(cid)


def bisect(F, a, b, tol=mpf('1e-52')):
    """Illinois regula falsi on a sign change of F over [a, b]."""
    fa, fb = F(a), F(b)
    assert fa * fb < 0
    for _ in range(400):
        x = (a * fb - b * fa) / (fb - fa)
        fx = F(x)
        if fx == 0:
            return x
        if fx * fb < 0:
            a, fa = b, fb
        else:
            fa /= 2
        b, fb = x, fx
        if fabs(b - a) < tol:
            break
    return b


def sign_changes(F, a, b, h):
    pts, k = [], 1
    while a + k * h <= b + h / 1000:
        pts.append(a + k * h)
        k += 1
    vals = [F(x) for x in pts]
    return [(pts[i], pts[i + 1]) for i in range(len(pts) - 1) if vals[i] * vals[i + 1] < 0], vals


# ---------- F1a: the limit l -> infinity ----------
def xinf(rho):
    s, X, X1 = rho / 2, mpf(0), mpf(0)
    fact = mpf(1)  # (n-1)!
    for n in range(1, 201):
        if n > 1:
            fact *= n - 1
        t = (n - 2) * (n - 4) / fact**2
        X += t * s**n
        X1 += t * n * s**(n - 1) / 2
    return X, X1


def xinf_bessel(rho):
    s = rho / 2
    return s * ((s + 3) * besseli(0, 2 * sqrt(s)) - 4 * sqrt(s) * besseli(1, 2 * sqrt(s)))


def ninf(rho):
    X, X1 = xinf(rho)
    return X - (rho - 6) * X1


def psiinf(rho):
    X, X1 = xinf(rho)
    N = X - (rho - 6) * X1
    NZ0 = rho**3 / 8 - 3 * rho**2 / 4 + 9 * rho / 2 - 9
    return 2 * rho**2 * N**2 - 4 * NZ0 * X**2


t0 = time.time()
print(f'ind104 mutation={MUT}  l set ({len(L_SET)}): {L_SET}')
for rho in (mpf(3), mpf('8.5'), mpf(11)):
    d = fabs(xinf(rho)[0] - xinf_bessel(rho))
    check('F1a', f'series X_inf = Bessel closed form at rho={rho}', d < mpf('1e-45'), f'diff={mp.nstr(d, 3)}')
sc, _ = sign_changes(ninf, mpf(6), mpf(30), mpf('0.01'))
check('F1a', 'N_inf has one sign change on (6, 30]', len(sc) == 1, f'{len(sc)} changes')
rho_s = bisect(ninf, *sc[0])
sc, _ = sign_changes(psiinf, rho_s, mpf(30), mpf('0.01'))
check('F1a', 'Psi_inf has one sign change on [rho_*, 30]', len(sc) == 1, f'{len(sc)} changes')
rho_n = bisect(psiinf, *sc[0])
print(f'  rho_*   = {mp.nstr(rho_s, 30)}\n  rho_neg = {mp.nstr(rho_n, 30)}')
for nm, mine, theirs in (('rho_*', rho_s, RHO_104[0]), ('rho_neg', rho_n, RHO_104[1])):
    d = fabs(mine - theirs)
    check('F1a', f'{nm} agrees with #104 to 1e-24', d < mpf('1e-24'), f'diff={mp.nstr(d, 3)}')
RHO = (rho_s, rho_n)


# ---------- the direct route at finite l ----------
def coeffs(l):
    L = l * (l + 1)
    cs = [mpf(0)] * (l + 3)
    cs[1] = mpf(3) / 2
    A = mpf(1) / 4  # (l-n+3)_{2n-4} / (2^n (n-1)!^2) at n = 2
    for n in range(3, l + 3):
        A = A * (l - n + 3) * (l + n - 2) / (2 * (n - 1)**2)
        cs[n] = (n - 2) * ((n - 4) * L + n - 1) * A
    if MUT == 'cn' and l >= 3:
        cs[5] *= 1 + mpf('1e-12')
    return cs


def chi3(rev, r):
    p = d1 = d2 = mpf(0)
    for a in rev:
        d2 = d2 * r + d1
        d1 = d1 * r + p
        p = p * r + a
    return p, d1, 2 * d2


class Direct:
    def __init__(self, l):
        self.l, self.c = l, l * (l + 1) - 2
        self.cs = coeffs(l)
        self.rev = self.cs[::-1]

    def at(self, rho):
        c = self.c
        r = rho / c
        ch, ch1, ch2 = chi3(self.rev, r)
        f, fr, D = 1 + 2 / r, -2 / r**2, c * r - 6
        w = ch1 / ch - c / D                          # psi0_r / psi0, psi0 = chi/(cr-6)
        wr = ch2 / ch - (ch1 / ch)**2 + c**2 / D**2
        g, gr = f * w, fr * w + f * wr
        gx = f * gr
        vhat = g**2 + gx if MUT == 'vhat' else g**2 - gx
        psi = ch / D
        psir = ch1 / D - c * ch / D**2
        psirr = ch2 / D - 2 * c * ch1 / D**2 + 2 * c**2 * ch / D**3
        psixx = f * (fr * psir + f * psirr)
        lam = mpf(c) / 2
        tail = -9 * (lam * r - 1) if MUT == 'vsign' else 9 * (lam * r - 1)
        V = 2 * f * (lam**2 * r**2 * ((lam + 1) * r - 3) + tail) / (r**3 * (lam * r - 3)**2)
        N = c * ch - D * ch1
        return dict(ch=ch, ch1=ch1, ch2=ch2, f=f, vhat=vhat, psixx=psixx, Vpsi=V * psi, N=N)

    def N(self, rho):
        return self.at(rho)['N']

    def vhat(self, rho):
        return self.at(rho)['vhat']


brk = {}
with open(CSV) as fh:
    next(fh)
    for line in fh:
        l, c, a, b, p, q = line.strip().split(',')
        brk[int(l)] = (mpf(a), mpf(b), mpf(p), mpf(q))
if MUT == 'csv':
    a, b, p, q = brk[500]
    brk[500] = (a + mpf('1e-13'), b + mpf('1e-13'), p, q)

roots = {}
far = [mpf(x) for x in (20, 40, 80, 160, 320)]
for l in L_SET:
    t1 = time.time()
    d = Direct(l)
    c = d.c
    K = (l - 1) * l * (l + 1) * (l + 2)
    cs = d.cs
    okA = (fabs(cs[1] - mpf(3) / 2) < mpf('1e-55') and cs[2] == 0 and fabs(cs[3] + mpf(K) / 32) < mpf('1e-50') * K
           and fabs(cs[4] - mpf(K) / 96) < mpf('1e-50') * K and cs[l + 2] > 0)
    res = mpf(0)
    for rho in (mpf(7), mpf('8.5'), mpf('9.6'), mpf(12)):
        q = d.at(rho)
        res = max(res, fabs(q['psixx'] - q['Vpsi']) / (fabs(q['psixx']) + fabs(q['Vpsi'])))
    check('F2', f'l={l} Lemma A c1..c4 and Zerilli residual', okA and res < mpf('1e-40'), f'rel residual {mp.nstr(res, 3)}')
    scN, _ = sign_changes(d.N, mpf(6), mpf(16), mpf('0.02'))
    farN = all(d.N(x) < 0 for x in far)
    ok = len(scN) == 1 and farN
    rs = bisect(d.N, *scN[0]) if scN else None
    scV, _ = sign_changes(d.vhat, rs, mpf(16), mpf('0.02')) if rs else ([], None)
    farV = all(d.vhat(x) > 0 for x in far)
    ok = ok and len(scV) == 1 and farV
    rn = bisect(d.vhat, *scV[0]) if scV else None
    a, b, p, q = brk[l]
    inside = rs is not None and rn is not None and a < rs < b and p < rn < q
    check('F3', f'l={l} one sign change of N and of V-hat beyond r_*, roots inside #104 brackets', ok and inside,
          f'N {len(scN)}, Vhat {len(scV)}, c r_* = {mp.nstr(rs, 20)}, c r_neg = {mp.nstr(rn, 20)}, {time.time() - t1:.1f} s')
    roots[l] = (rs, rn)

# ---------- F1b: extrapolation of the direct roots ----------
for k, (nm, D1ref) in enumerate((('r_*', mpf('3.515486')), ('r_neg', mpf('5.839393')))):
    rows = [(mpf(1) / (l * (l + 1) - 2), roots[l][k]) for l in (1000, 2000, 3000)]
    M = mp.matrix([[1, e, e**2] for e, _ in rows])
    sol = mp.lu_solve(M, mp.matrix([y for _, y in rows]))
    dr, dD = fabs(sol[0] - RHO[k]), fabs(sol[1] - D1ref)
    check('F1b', f'{nm}: fit at l = 1000, 2000, 3000 gives rho and D1', dr < mpf('1e-12') and dD < mpf('2e-6'),
          f'rho fit - F1a = {mp.nstr(dr, 3)}, D1 = {mp.nstr(sol[1], 10)}, D2 = {mp.nstr(sol[2], 6)}')

# ---------- F4: the 1/c constants ----------
print('  l        D_* = (c r_* - rho_*) c   D_neg = (c r_neg - rho_neg) c')
for l in L_SET:
    if l < 138:
        continue
    c = l * (l + 1) - 2
    Ds, Dn = (roots[l][0] - RHO[0]) * c, (roots[l][1] - RHO[1]) * c
    print(f'  {l:<6} {mp.nstr(Ds, 12):<24} {mp.nstr(Dn, 12)}')
    ok = 0 < Ds <= S_L2 and 0 < Dn <= S_NEG_L2
    if l >= 500:
        ok = ok and Ds <= S_M and Dn <= S_NEG_M
    check('F4', f'l={l} 0 < D within #104\'s constants', ok)

# ---------- F5: order and monotonicity ----------
check('F5', 'r_* < r_neg at every l', all(roots[l][0] < roots[l][1] for l in L_SET))


def l2r(l, k):
    c = l * (l + 1) - 2
    return roots[l][k] * (c if MUT == 'l2' else l**2) / c


runs = [list(range(2, 31)), [137, 138, 139], [499, 500, 501, 502], [1000, 1001], [2999, 3000]]
for k, nm in ((0, 'r_*'), (1, 'r_neg')):
    dec = all(roots[s[i + 1]][k] < roots[s[i]][k] for s in runs for i in range(len(s) - 1))
    above = all(roots[l][k] > RHO[k] for l in L_SET)
    check('F5', f'c {nm} strictly decreases and stays above rho', dec and above)
    small = [l2r(l, k) for l in range(2, 31)]
    inc = all(l2r(s[i + 1], k) > l2r(s[i], k) for s in [list(range(5, 31))] + runs[1:] for i in range(len(s) - 1))
    below = all(l2r(l, k) < RHO[k] for l in L_SET if l >= 3)
    check('F5', f'l^2 {nm}: minimum over 2..30 at l = 5, increasing from 5, below rho for l >= 3',
          small.index(min(small)) == 3 and inc and below, f'min {mp.nstr(min(small), 8)}')
worst = mpf(0)
for l, row in TABLE.items():
    c = l * (l + 1) - 2
    mine = (roots[l][0], roots[l][1], roots[l][0] * l**2 / c, roots[l][1] * l**2 / c)
    worst = max(worst, max(fabs(m - mpf(t)) for m, t in zip(mine, row)))
check('F5', 'RESULTS 4.3 table rows within 1e-6', worst < mpf('1e-6'), f'worst {mp.nstr(worst, 3)}')

# ---------- F6: Theorem 3 (P1), (P2) ----------
r, c, sig, mu, tau, m = sp.symbols('r c sigma mu tau m', positive=True)
lam = c / 2
tail = -9 * (lam * r - 1) if MUT == 'vsign' else 9 * (lam * r - 1)
num = lam**2 * r**2 * ((lam + 1) * r - 3) + tail
p1 = sp.Poly(sp.expand(num.subs(c, 2 / mu).subs(r, (3 + sig) * mu)), sig, mu)
check('F6', '(P1) numerator of V in (sigma, mu) has positive coefficients', all(k > 0 for k in p1.coeffs()),
      f'{len(p1.coeffs())} terms: {p1.as_expr()}')
V = 2 * (1 + 2 / r) * num / (r**3 * (lam * r - 3)**2)
Q = sp.cancel(-sp.diff(V, r) * r**5 * (c * r - 6)**3 / 2)
qn, qd = sp.fraction(Q)
isquint = qd.free_symbols == set() and sp.Poly(qn, r).degree() == 5
p2e = sp.cancel(sp.expand((c**5 * Q).subs(r, (6 + tau) / c)).subs(c, (m + 4) * (m + 1))) if isquint else None
ispoly = p2e is not None and sp.fraction(p2e)[1] == 1
co = sp.Poly(p2e, tau, m).coeffs() if ispoly else []
check('F6', '(P2) Q is a quintic in r; c^5 Q in (tau, m) has 64 terms, all positive',
      isquint and ispoly and len(co) == 64 and all(k > 0 for k in co), f'quintic={isquint}, {len(co)} terms, min coeff {min(co) if co else None}')

# ---------- F7: V-hat identities at large l ----------
for l in (2, 7, 30, 500, 3000):
    d = Direct(l)
    cc = d.c
    eps = mpf(1) / cc
    worst = mpf(0)
    for rho in (mpf(7), mpf(9), mpf(11)):
        q = d.at(rho)
        X, X1, X2 = cc * q['ch'], q['ch1'], q['ch2'] / cc
        N = X - (rho - 6) * X1
        N1 = -(rho - 6) * X2
        NZ = (1 + 2 * eps) * rho**3 / 8 - 3 * rho**2 / 4 + 9 * rho / 2 - 9
        S = rho * X * (eps * N + (2 + eps * rho) * N1) - (2 + eps * rho) * N * (X + 2 * rho * X1)
        Psi = rho**2 * (2 + eps * rho) * N**2 - 4 * NZ * X**2
        vS = cc**3 * q['f'] * S / (rho**2 * (rho - 6) * X**2)
        vP = 2 * cc**4 * (2 + eps * rho) * Psi / (rho**4 * (rho - 6)**2 * X**2)
        worst = max(worst, fabs(vS / q['vhat'] - 1), fabs(vP / q['vhat'] - 1))
    check('F7', f'l={l} V-hat direct = S form = Psi form', worst < mpf('1e-35'), f'worst rel {mp.nstr(worst, 3)}')

print(f'FAILED: {failed}' if failed else 'ALL PASS', f'({time.time() - t0:.0f} s)')
sys.exit(1 if failed else 0)
