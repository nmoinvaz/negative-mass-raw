#!/usr/bin/env python3
"""ind143: the coordinator's independent check of #143 (the even-parity potential from the linearized Einstein equations).

delta R from the Lichnerowicz form 1/2 (nabla^c nabla_a h_bc + nabla^c nabla_b h_ac - box h_ab - nabla_a nabla_b h) with its own
Christoffel symbols and covariant derivatives. DG06 (gr-qc/0604021) eqs. (3)-(6), (9) typed from its TeX. Shares no code with
zerilli_derivation*.py. Criteria Y0-Y5 in I143-mac/README.md.
"""
import argparse
import sys
import time

import sympy as sp
from sympy.polys.matrices import DomainMatrix

ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
ap.add_argument('--only', default='')          # comma list of Y ids to run (mutation runs); default all
args = ap.parse_args()
MUT = args.mutate
ONLY = set(args.only.split(',')) if args.only else None
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.0f} s)", flush=True)
    if not ok:
        FAIL.append(name)


def want(y):
    return ONLY is None or y in ONLY


t, r, x, ph = sp.symbols('t r x phi')
M, s, lam = sp.symbols('M s lambda')
X = [t, r, x, ph]
F = 1 - 2 * M / r
g0 = sp.diag(-F, 1 / F, r**2 / (1 - x**2), r**2 * (1 - x**2))
gi = [sp.cancel(1 / g0[i, i]) for i in range(4)]
# G[a][b][c] = Gamma^a_bc of g0 (diagonal metric)
G = [[[sp.cancel(gi[a] * (sp.diff(g0[a, b], X[c]) + sp.diff(g0[a, c], X[b]) - sp.diff(g0[b, c], X[a])) / 2)
       for c in range(4)] for b in range(4)] for a in range(4)]
E = sp.exp(s * t)


def dR(h):
    """Linearized Ricci tensor of g0 + eps h, Lichnerowicz form."""
    T = {}
    for c in range(4):                                  # T[c,a,b] = nabla_c h_ab
        for a in range(4):
            for b in range(a, 4):
                v = sp.diff(h[a, b], X[c]) - sum(G[d][c][a] * h[d, b] + G[d][c][b] * h[a, d] for d in range(4))
                T[c, a, b] = T[c, b, a] = v

    def U(d, c, a, b):                                  # nabla_d T_cab
        return sp.diff(T[c, a, b], X[d]) - sum(G[e][d][c] * T[e, a, b] + G[e][d][a] * T[c, e, b] + G[e][d][b] * T[c, a, e]
                                               for e in range(4))
    tr = sum(gi[c] * h[c, c] for c in range(4))
    out = {}
    for a in range(4):
        for b in range(a, 4):
            v = sum(gi[c] * (U(c, a, b, c) + U(c, b, a, c) - U(c, c, a, b)) for c in range(4))
            if MUT != 'lich':
                v -= sp.diff(tr, X[a], X[b]) - sum(G[e][a][b] * sp.diff(tr, X[e]) for e in range(4))
            out[a, b] = v / 2
    return out                                          # 10 components, a <= b


def h_even(H0, H1, H2, K, P):
    h = sp.zeros(4)
    h[0, 0] = F * H0 * P * E
    h[0, 1] = h[1, 0] = H1 * P * E
    h[1, 1] = H2 * P * E / F
    h[2, 2] = r**2 * K * P * E / (1 - x**2)
    h[3, 3] = r**2 * (1 - x**2) * K * P * E
    return h


def h_odd(h0, h1, P):
    h = sp.zeros(4)
    dP = sp.diff(P, x)
    h[0, 3] = h[3, 0] = h0 * E * (1 - x**2) * dP
    h[1, 3] = h[3, 1] = h1 * E * (1 - x**2) * dP
    return h


def lam_of(l):
    return sp.Rational((l - 1) * (l + 2), 2)


def V_dg(lm, Mv=M):                                     # DG06 (6)
    k9 = 8 if MUT == 'vz' else 9
    Fv = 1 - 2 * Mv / r
    return 2 * Fv * (lm**2 * r**2 * ((lm + 1) * r + 3 * Mv) + k9 * Mv**2 * (lm * r + Mv)) / (r**3 * (lm * r + 3 * Mv)**2)


def fD(lm):                                             # DG06 (4)
    return (lm * (lm + 1) * r**2 + 3 * lm * M * r + 6 * M**2) / (r**2 * (lm * r + 3 * M))


def hD(lm):
    k = 2 if MUT == 'hcoef' else 3
    return (lm * r**2 - 3 * lm * r * M - k * M**2) / ((r - 2 * M) * (lm * r + 3 * M))


def psi9(lm, H2, K, dK):                                # DG06 (9)
    d1 = (lm + 2) if MUT == 'psi9' else (lm + 1)
    return r * (r - 2 * M) / (d1 * (lm * r + 3 * M)) * (H2 - r * dK) + r * K / (lm + 1)


p0, p1 = sp.symbols('p0 p1')


def reducer(V):
    """Jets of a function obeying psi_xx = (V + s^2) psi, i.e. psi'' = ((V+s^2) psi / F - F' psi') / F."""
    d2 = ((V + s**2) * p0 / F - sp.diff(F, r) * p1) / F

    def D(e):
        return sp.diff(e, r) + p1 * sp.diff(e, p0) + d2 * sp.diff(e, p1)
    ders = [p0, p1]
    for _ in range(5):
        ders.append(sp.cancel(D(ders[-1])))
    return D, ders


def reduce_fn(e, fn, ders):
    rep = {sp.Derivative(fn, (r, k)): ders[k] for k in range(1, len(ders))}
    rep[fn] = p0
    out = e.xreplace(rep)
    assert not out.has(sp.Derivative), 'unreduced derivative'
    return out


def zero(e):
    return sp.cancel(sp.together(e)) == 0


# ---------------------------------------------------------------- Y0: the operator, planted
if want('Y0'):
    l = 2
    P = sp.legendre(l, x)
    ra = dR(sp.diff(g0, M))
    oka = all(zero(v) for v in ra.values())
    A, B, C, D_ = [sp.Function(n)(r) for n in 'ABCD']
    okb = True
    for xi in ([A * P * E, B * P * E, C * sp.diff(P, x) * E, 0], [0, 0, 0, D_ * (1 - x**2) * sp.diff(P, x) * E]):
        h = sp.zeros(4)
        for a in range(4):
            for b in range(4):
                h[a, b] = (sp.diff(xi[b], X[a]) - sum(G[c][a][b] * xi[c] for c in range(4))
                           + sp.diff(xi[a], X[b]) - sum(G[c][b][a] * xi[c] for c in range(4)))
        rb = dR(h)
        okb = okb and all(zero(v.subs(t, 0)) for v in rb.values())
    hc = sp.zeros(4)
    hc[0, 0] = r * E * P
    rc = dR(hc)
    nz = [k for k, v in rc.items() if not zero(v.subs(t, 0))]
    check('Y0', oka and okb and bool(nz), f"(a) h = d_M g: delta R = 0 {oka}; (b) pure gauge, even and odd xi: delta R = 0 {okb}; "
          f"(c) h_tt = r e^st P: nonzero components {nz}")

# ---------------------------------------------------------------- Y1: odd parity, planted
if want('Y1'):
    Psi = sp.Function('Psi')(r)
    ok1, rows = True, []
    for l in (2, 3, 4):
        L = l * (l + 1)
        k6 = 5 if MUT == 'rw' else 6
        Vrw = F * (sp.Integer(L) / r**2 - k6 * M / r**3)
        _, ders = reducer(Vrw)
        h1 = r * Psi / F
        h0 = F * sp.diff(F * h1, r) / s
        res = dR(h_odd(h0, h1, sp.legendre(l, x)))
        bad = [k for k, v in res.items() if not zero(reduce_fn(v.subs(t, 0), Psi, ders))]
        ok1 = ok1 and not bad
        rows.append(f"l = {l}: nonzero {bad}")
    check('Y1', ok1, 'h1 = r Psi / F, s h0 = F (F h1)\', Psi_xx = (V_RW + s^2) Psi; all 10 components vanish: ' + '; '.join(rows))

# ---------------------------------------------------------------- Y2: converse, even parity
if want('Y2'):
    psi = sp.Function('psi')(r)
    ok2, rows = True, []
    for l in (2, 3, 4):
        lm = lam_of(l)
        _, ders = reducer(V_dg(lm))
        K = fD(lm) * psi + F * sp.diff(psi, r)
        H1 = s * (hD(lm) * psi + r * sp.diff(psi, r))
        H2 = sp.diff(F * (hD(lm) * psi + r * sp.diff(psi, r)), r) - K
        res = dR(h_even(H2, H1, H2, K, sp.legendre(l, x)))
        bad = [k for k, v in res.items() if not zero(reduce_fn(v.subs(t, 0), psi, ders))]
        ok2 = ok2 and not bad
        rows.append(f"l = {l}: nonzero {bad}")
    check('Y2', ok2, 'DG06 (3)-(4), H0 = H2, psi_xx = (V + s^2) psi with DG06 (6); all 10 components vanish: ' + '; '.join(rows))

# ---------------------------------------------------------------- Y3: forward, even parity (the case re-solved)
NAMES = ('H0', 'H1', 'H2', 'K')
FN = {n: sp.Function(n)(r) for n in NAMES}
NJ = 7
JET = {(n, k): sp.Symbol(f'{n}_{k}') for n in NAMES for k in range(NJ)}


def jetify(e):
    rep = {}
    for n, f in FN.items():
        for k in range(1, NJ):
            rep[sp.Derivative(f, (r, k))] = JET[n, k]
        rep[f] = JET[n, 0]
    out = e.xreplace(rep)
    assert not out.has(sp.Derivative) and not any(out.has(f) for f in FN.values())
    return out


def Dj(e):
    return sp.diff(e, r) + sum(JET[n, k + 1] * sp.diff(e, JET[n, k]) for n in NAMES for k in range(NJ - 1))


def rat(a, pt):
    v = sp.cancel(a.subs(pt))
    assert v.is_Rational, v
    return v


def member(rows, z, cols, field, pt, label):
    """Is z in the span of rows (linear forms in the jet symbols cols) over field? Certificate checked exactly."""
    vec = lambda e: [sp.cancel(sp.diff(e, c)) for c in cols]
    for e in rows + [z]:
        assert zero(e - sum(sp.diff(e, c) * c for c in cols)), 'not a homogeneous linear form'
    A = [vec(e) for e in rows]
    zv = vec(z)
    A0 = DomainMatrix.from_list_sympy(len(A), len(cols), [[rat(a, pt) for a in row] for row in A]).convert_to(sp.QQ)
    rk = A0.rank()
    _, piv = A0.transpose().rref()                      # independent rows at the point
    B = [A[i] for i in piv]
    z0 = DomainMatrix.from_list_sympy(1, len(cols), [[rat(a, pt) for a in zv]]).convert_to(sp.QQ)
    if A0.vstack(z0).rank() != rk:
        return False, f"{label}: not in the span at the point {pt} (rank {rk})"
    B0 = DomainMatrix.from_list_sympy(len(B), len(cols), [[rat(a, pt) for a in row] for row in B]).convert_to(sp.QQ)
    _, pc = B0.rref()                                   # columns that make the square system nonsingular at the point
    S = DomainMatrix.from_list_sympy(len(B), len(B), [[B[i][j] for i in range(len(B))] for j in pc]).convert_to(field)
    rhs = DomainMatrix.from_list_sympy(len(B), 1, [[zv[j]] for j in pc]).convert_to(field)
    c = S.lu_solve(rhs)
    BT = DomainMatrix.from_list_sympy(len(cols), len(B), [[B[i][j] for i in range(len(B))] for j in range(len(cols))]).convert_to(field)
    zt = DomainMatrix.from_list_sympy(len(cols), 1, [[a] for a in zv]).convert_to(field)
    ok = (BT * c - zt).is_zero_matrix
    cs = [field.to_sympy(c[i, 0].element) for i in range(len(B))]
    den = sp.factor(sp.lcm([sp.denom(sp.together(v)) for v in cs if v != 0]))
    return ok, f"{label}: rank {rk} of {len(A)} forms, certificate of {len(B)} coefficients exact {ok}, denominators {den}"


if want('Y3'):
    ok3, msgs = True, []
    for l, Mv in ((2, M), (3, sp.Integer(-1))):
        lm = lam_of(l)
        res = dR(h_even(FN['H0'], FN['H1'], FN['H2'], FN['K'], sp.legendre(l, x)))
        base = []
        for (a, b), v in sorted(res.items()):
            v0 = jetify(v.subs(t, 0)).subs(M, Mv)
            for x0 in (0, sp.Rational(1, 3), sp.Rational(3, 5)):
                e = sp.cancel(v0.subs(x, x0))
                if e != 0:
                    base.append(e)
        d1 = [sp.cancel(Dj(e)) for e in base]
        d2 = [sp.cancel(Dj(e)) for e in d1]
        used = sorted({c for e in base + d1 + d2 for c in e.free_symbols if c in JET.values()}, key=str)
        field = sp.QQ.frac_field(r, M, s) if Mv == M else sp.QQ.frac_field(r, s)
        pt = {r: sp.Rational(37, 7), M: sp.Rational(-13, 11), s: sp.Rational(5, 3)} if Mv == M else \
            {r: sp.Rational(37, 7), s: sp.Rational(5, 3)}
        oki, mi = member(base, JET['H0', 0] - JET['H2', 0], used, field, pt, f"l = {l} (i) H0 - H2")
        lm_ = lm
        V = V_dg(lm_, Mv)
        Fv = 1 - 2 * Mv / r
        ps = psi9(lm_, JET['H2', 0], JET['K', 0], JET['K', 1]).subs(M, Mv)
        Z = sp.cancel(Fv * Dj(Fv * Dj(ps)) - (V + s**2) * ps)
        okz, mz = member(base + d1 + d2, Z, used, field, pt, f"l = {l} (ii) Z")
        ok3 = ok3 and oki and okz
        msgs += [mi, mz]
        print('  ' + mi + '\n  ' + mz, flush=True)
    check('Y3', ok3, '; '.join(msgs))

# ---------------------------------------------------------------- Y4: (9) inverts (3)-(4)
if want('Y4'):
    D, _ = reducer(V_dg(lam))
    K = fD(lam) * p0 + F * p1
    H2 = D(F * (hD(lam) * p0 + r * p1)) - K
    back = psi9(lam, H2, K, D(K))
    check('Y4', zero(back - p0), f"(9) of the map (3)-(4) minus psi = {sp.cancel(sp.together(back - p0))}, symbolic in r, lambda, M, s")

# ---------------------------------------------------------------- Y5: the potential's forms
if want('Y5'):
    V143 = 2 * F * (lam**2 * (lam + 1) * r**3 + 3 * lam**2 * M * r**2 + 9 * lam * M**2 * r + 9 * M**3) / (r**3 * (lam * r + 3 * M)**2)
    a = zero(V_dg(lam) - V143)
    f1 = 1 + 2 / r
    k = 1 if MUT == 'vres' else -1
    Vres = 2 * f1 * (lam**2 * r**2 * ((lam + 1) * r - 3) + 9 * (lam * r + k)) / (r**3 * (lam * r - 3)**2)
    b = zero(V_dg(lam).subs(M, -1) - Vres)
    Lsym = 2 * lam + 2
    pole = sp.cancel(sp.cancel((lam * r + 3 * M)**2 * V_dg(lam)).subs(r, -3 * M / lam))
    c1 = zero(pole - (Lsym - 2)**2 * (Lsym + 1)**2 / 18)
    l_ = sp.Symbol('l')
    c2 = zero((-3 * M / lam).subs({M: -1, lam: (l_ - 1) * (l_ + 2) / 2}) - 6 / ((l_ + 2) * (l_ - 1)))
    check('Y5', a and b and c1 and c2, f"(a) DG06 (6) = #143's form {a}; (b) at M = -1 = RESULTS 4.2's V {b}; "
          f"(c) (lambda r + 3M)^2 V at r = -3M/lambda = {sp.factor(pole)}, = (L-2)^2 (L+1)^2 / 18 {c1}; -3M/lambda = 6/c at M = -1 {c2}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL), f'({time.time() - T0:.0f} s)')
sys.exit(1 if FAIL else 0)
