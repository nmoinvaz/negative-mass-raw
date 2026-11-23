#!/usr/bin/env python3
"""Coordinator's independent check of #138 (Lemma A, L1, T1, T2 of phase2/dg_proof/RESULTS.md). Criteria K1a-K6 in
I138-mac/README.md, fixed before the first run. Shares no code with review_lemma_a_*.py or #2's scripts.
Usage: ind138.py [--mutate=ode|cn|rs|cubic|shift]"""
import sys
import time
from fractions import Fraction as Fr

import sympy as sp

ARGS = dict(a.lstrip('-').split('=', 1) for a in sys.argv[1:] if '=' in a)
MUT = ARGS.get('mutate')
assert MUT in (None, 'ode', 'cn', 'rs', 'cubic', 'shift'), MUT
failed = []


def check(cid, name, ok, detail=''):
    print(('PASS ' if ok else 'FAIL ') + cid + ' ' + name + ('  ' + detail if detail else ''), flush=True)
    if not ok and cid not in failed:
        failed.append(cid)


t0 = time.time()
r, c, l, m, n, u, eps = sp.symbols('r c l m n u epsilon')
lam = c / 2
f = 1 + 2 / r
tail = 9 * (lam * r + 1) if MUT == 'ode' else 9 * (lam * r - 1)
V = 2 * f * (lam**2 * r**2 * ((lam + 1) * r - 3) + tail) / (r**3 * (lam * r - 3)**2)

# ---------- the chi ODE from psi0_xx = V psi0, psi0 = chi/(c r - 6), d/dx = f d/dr ----------
chi = sp.Function('chi')(r)
psi = chi / (c * r - 6)
expr = f**2 * sp.diff(psi, r, 2) + f * sp.diff(f, r) * sp.diff(psi, r) - V * psi
num = sp.numer(sp.together(expr))
d2, d1 = sp.diff(chi, r, 2), sp.diff(chi, r)
x2, x1, x0 = sp.symbols('x2 x1 x0')
lin = sp.expand(num.subs(d2, x2).subs(d1, x1).subs(chi, x0))
P2, P1, P0 = [sp.factor(lin.coeff(s)) for s in (x2, x1, x0)]
g = sp.gcd(sp.gcd(sp.Poly(P2, r, c), sp.Poly(P1, r, c)), sp.Poly(P0, r, c)).as_expr()
P2, P1, P0 = [sp.cancel(P / g) for P in (P2, P1, P0)]
ratio = sp.cancel(P2 / (-r**2 * (r + 2) * (c * r - 6)))
check('K1a', 'P2 proportional to -r^2 (r+2)(cr-6)', ratio.free_symbols == set(), f'P2 = {sp.factor(P2)}, ratio {ratio}')
print(f'  P1 = {sp.factor(P1)}\n  P0 = {sp.factor(P0)}')
# coefficient of r^m: sum over n of c_n [p2_{m-n+2} n(n-1) + p1_{m-n+1} n + p0_{m-n}]
p2, p1, p0 = [sp.Poly(sp.expand(P), r) for P in (P2, P1, P0)]
shifts = {}
for poly, off, w in ((p2, 2, n * (n - 1)), (p1, 1, n), (p0, 0, sp.Integer(1))):
    for (j,), a in poly.terms():
        k = j - off  # r^n -> r^(n+k): contributes to r^m with n = m - k
        shifts[k] = shifts.get(k, 0) + a * w
shifts = {k: sp.factor(v) for k, v in shifts.items() if sp.simplify(v) != 0}
print('  coefficient of r^m = sum_k A_k(n = m - k) c_{m-k}, with k:', sorted(shifts))
check('K1a', 'three-term: only c_m, c_(m-1), c_(m-2)', sorted(shifts) == [0, 1, 2])
A = {k: sp.factor(v.subs(n, m - k)) for k, v in shifts.items()}


# ---------- Lemma A's c_n ----------
def gfac(nn):  # c_n = gfac(n) * Q_n
    return (nn - 2) * ((nn - 3 if MUT == 'cn' else nn - 4) * l * (l + 1) + nn - 1)


def qstep(nn):  # Q_n / Q_(n-1) = (l - n + 3)(l + n - 2) / (2 (n - 1)^2)
    return (l - nn + 3) * (l + nn - 2) / (2 * (nn - 1)**2)


cc = (l + 2) * (l - 1)
Q = {0: 1, 1: qstep(m - 1), 2: qstep(m - 1) * qstep(m)}  # Q_(m-k) / Q_(m-2), k = 2, 1, 0
expr_rec = sum(A[k].subs(c, cc) * gfac(m - k) * Q[2 - k] for k in (0, 1, 2))
rec = sp.factor(sp.cancel(expr_rec))
check('K1b', 'recurrence identically 0 in (l, m), m >= 5', rec == 0, f'residual {rec}')
Kq = (l - 1) * l * (l + 1) * (l + 2)
low = {1: sp.Rational(3, 2), 2: 0, 3: -Kq / 32, 4: Kq / 96}
if MUT == 'cn':
    low[4] = gfac(4) * qstep(3) * qstep(4) / 4  # the mutated formula at n = 4
ok = True
for mm in range(1, 5):
    s_ = sum(A[k].subs({c: cc, m: mm}) * low.get(mm - k, 0) for k in (0, 1, 2) if mm - k >= 1)
    ok = ok and sp.simplify(s_) == 0
check('K1b', 'orders m = 1..4 vanish symbolically in l', ok)
k0 = sp.cancel(A[0] / (12 * (m - 1)**2))
k2 = sp.cancel(A[2].subs(c, cc) / (cc * (l - m + 4) * (l + m - 3)))
same = sp.simplify(k0 - k2) == 0 and k0.free_symbols <= {c} and sp.simplify(k0.subs(c, cc) - k2) == 0
mid = sp.factor(A[1] / k0) if same else None
w1 = sp.simplify(mid + 2 * (m - 2) * (c * (m - 4) - 3 * (m - 1))) == 0 if same else False
check('K1c', 'normalisation of RESULTS recurrence; middle coefficient', same and w1,
      f'constant {k0}; middle / constant = {mid}; equals -2(m-2)(c(m-4) - 3(m-1)): {w1}')


# ---------- K2: psi0_xx = V psi0 exactly at l outside 2..40 ----------
def cn_exact(L_):
    LL = L_ * (L_ + 1)
    cs = {1: Fr(3, 2), 2: Fr(0)}
    q = Fr(1, 4)
    for k in range(3, L_ + 3):
        q *= Fr((L_ - k + 3) * (L_ + k - 2), 2 * (k - 1)**2)
        cs[k] = (k - 2) * ((k - 3 if MUT == 'cn' else k - 4) * LL + k - 1) * q
    return cs


for L_ in (41, 45, 60, 100):
    cs = cn_exact(L_)
    chi_p = sp.Poly(sum(sp.Rational(v.numerator, v.denominator) * r**k for k, v in cs.items()), r)
    lhs = sp.Poly(P2.subs(c, L_ * (L_ + 1) - 2), r) * chi_p.diff((r, 2)) + sp.Poly(P1.subs(c, L_ * (L_ + 1) - 2), r) * chi_p.diff(r) \
        + sp.Poly(P0.subs(c, L_ * (L_ + 1) - 2), r) * chi_p
    check('K2', f'l={L_} chi-ODE residual exactly 0', lhs.is_zero, f'{len(lhs.terms())} nonzero terms')

# ---------- K3: L1 symbolic in c ----------
rs = 6 / (c + 1) if MUT == 'rs' else 6 / c
P2p = sp.diff(P2, r)
e2 = sp.cancel((1 - P1 / P2p).subs(r, rs))
p2zero = sp.cancel(P2.subs(r, rs)) == 0
check('K3', 'P2(r_s) = 0 and exponents 0 and 3', p2zero and sp.simplify(e2 - 3) == 0, f'second exponent {sp.simplify(e2)}')
lr = sp.cancel((-P0 / P1).subs(r, rs) + 1 / (rs * (rs + 2)))
check('K3', "chi'/chi(r_s) = -1/(r_s (r_s+2))", lr == 0, f'difference {lr}')
cond = sp.cancel(((sp.diff(P1, r) + P0) * P0 - sp.diff(P0, r) * P1).subs(r, rs))
check('K3', "differentiated ODE at r_s forces chi''(r_s) = 0", cond == 0 and sp.cancel((P2p + P1).subs(r, rs)) != 0,
      f'(P1\' + P0) P0 - P0\' P1 at r_s = {cond}')

# ---------- K4: T1 ----------
cn_ = sp.Symbol('c_n')
term = sp.expand(cn_ * r**(n - 1) * (6 * n - (n - 1) * c * r) - (n - 1) * cn_ * r**(n - 1) * (6 - c * r) - 6 * cn_ * r**(n - 1))
check('K4', 'per-term identity of the T1 split', sp.simplify(term) == 0)
c3, c4 = -c * (c + 2) / 32, c * (c + 2) / 96  # K = (l-1)l(l+1)(l+2) = c(c+2)
cubic = 9 + (17 if MUT == 'cubic' else 18) * c3 * r**2 + (6 * c4 - 2 * c * c3) * r**3
gu = sp.expand(cubic.subs(r, 6 * u / c).subs(c, 1 / eps))
crit = [z for z in sp.solve(sp.diff(gu, u), u) if z != 0]
vals = [sp.simplify(gu.subs(u, z)) for z in crit] + [gu.subs(u, 0), sp.simplify(gu.subs(u, 1))]
claim = sp.Rational(9, 4) + sp.Rational(27, 4) * eps**2 / (1 + eps)**2
mins = [sp.simplify(v - claim) for v in vals]
check('K4', "cubic's minimum on [0, r_s] is 9/4 + (27/4) eps^2/(1+eps)^2", 0 in mins,
      f'g(u) = {sp.factor(gu)}; critical points {crit}; value - claim {mins}')
gmin = vals[mins.index(0)] if 0 in mins else None
E3 = (sp.Rational(1, 4), sp.Rational(1, 100), sp.Rational(1, 10**6))
ok = gmin is not None and all(sp.simplify(v - gmin).subs(eps, e) >= 0 for v in vals for e in E3)
zstar = crit[mins.index(0)] if 0 in mins and mins.index(0) < len(crit) else None
inside = zstar is not None and all(0 <= zstar.subs(eps, e) <= 1 for e in E3)
check('K4', 'that critical point lies in [0, 1] and its value is the minimum (compared at eps = 1/4, 1/100, 1e-6)',
      ok and inside, f'u* = {zstar}')


# ---------- K5, K6: T1 and T2 exactly at finite l ----------
def taylor(cs, x0, deg):
    poly = [Fr(0)] * (deg + 1)
    for k, v in cs.items():
        poly[k] = v
    d = []
    for mm in range(deg + 1):  # synthetic division: coefficients of the Taylor expansion at x0
        acc = Fr(0)
        rem = []
        for a in reversed(poly):
            acc = acc * x0 + a
            rem.append(acc)
        d.append(rem[-1])
        poly = list(reversed(rem[:-1]))
    return d


for L_ in list(range(2, 31)) + [50, 150]:
    cv = L_ * (L_ + 1) - 2
    cs = cn_exact(L_)
    rsv = Fr(6, cv) * (Fr(1001, 1000) if MUT == 'shift' else 1)
    d = taylor(cs, rsv, L_ + 2)
    coeffs = [(1 - k) * d[k] for k in range(L_ + 3)]
    signs = [x for x in coeffs if x != 0]
    changes = sum(1 for a, b in zip(signs, signs[1:]) if (a > 0) != (b > 0))
    ok = (d[0] > 0 and d[1] == -d[0] / (Fr(6, cv) * (Fr(6, cv) + 2)) and d[2] == 0
          and all(d[k] > 0 for k in range(4, L_ + 3)) and changes == 1)
    detail = f'd3 {"+" if d[3] > 0 else "-"}, sign changes {changes}'
    if L_ <= 50:
        Np = sp.Poly(sum(sp.Rational(v.numerator, v.denominator) * r**(k - 1) * (6 * k - (k - 1) * cv * r)
                         for k, v in cs.items()), r)
        beyond = Np.count_roots(inf=sp.Rational(6, cv))
        below = Np.count_roots(inf=0, sup=sp.Rational(6, cv))
        n0 = Np.eval(0)
        ok = ok and beyond == 1 and Np.eval(sp.Rational(6, cv)) != 0
        check('K6', f'l={L_} no root of N in [0, r_s], N(0) = 9', below == 0 and n0 == 9, f'{below} roots, N(0) = {n0}')
        detail += f', roots of N beyond r_s {beyond}'
    check('K5', f'l={L_} Taylor coefficients at r_s and one sign change', ok, detail)

print(f'FAILED: {failed}' if failed else 'ALL PASS', f'({time.time() - t0:.0f} s)')
sys.exit(1 if failed else 0)
