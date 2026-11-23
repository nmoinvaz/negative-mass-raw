#!/usr/bin/env python3
"""ind145: the coordinator's independent check of #145 (the static, s = 0, even-parity reduction).

Reuses the coordinator's I143-mac/ind143.py: delta R from the Lichnerowicz form with its own covariant derivatives, DG06
(gr-qc/0604021) eqs. (3)-(6), (9) typed from its TeX, the span-certificate routine. Shares no code with zerilli_static*.py,
zerilli_derivation*.py or zerilli_derivation_lib.py. Static: h has no t-dependence (s = 0). Criteria X0-X5 in I145-mac/README.md.
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


def reducer(V, s2=0):
    """Jets of a function obeying psi_xx = (V + s2) psi, i.e. psi'' = ((V+s2) psi / F - F' psi') / F (static: s2 = 0)."""
    d2 = ((V + s2) * p0 / F - sp.diff(F, r) * p1) / F

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



def static(h):
    return h.subs(s, 0)


# ---------------------------------------------------------------- X0: planted, static
if want('X0'):
    P1 = sp.legendre(1, x)
    ok_kerr = all(zero(v) for v in dR(static(h_odd((1 / r**2 if MUT == 'kerr' else 1 / r), 0, P1))).values())
    ok_rot = all(zero(v) for v in dR(static(h_odd(r**2, 0, P1))).values())
    nz = [k for k, v in dR(static(h_odd(1 / r**2, 0, P1))).items() if not zero(v)]
    P = sp.legendre(2, x)
    A, B, C = [sp.Function(n)(r) for n in 'ABC']
    xi = [A * P, B * P, C * sp.diff(P, x), 0]
    h = sp.zeros(4)
    for a_ in range(4):
        for b_ in range(4):
            h[a_, b_] = (sp.diff(xi[b_], X[a_]) - sum(G[c][a_][b_] * xi[c] for c in range(4))
                         + sp.diff(xi[a_], X[b_]) - sum(G[c][b_][a_] * xi[c] for c in range(4)))
    ok_g = all(zero(v) for v in dR(h).values())
    check('X0', ok_kerr and ok_rot and bool(nz) and ok_g,
          f"(a) l = 1 odd static: h0 = 1/r gives 0 {ok_kerr}; h0 = r^2 gives 0 {ok_rot}; h0 = 1/r^2 nonzero in {nz}; "
          f"(b) static even pure gauge, l = 2: delta R = 0 {ok_g}")

# ---------------------------------------------------------------- X1: the H1 sector
if want('X1'):
    ok1, rows = True, []
    H1f = sp.Function('H1')(r)
    for l in (2, 3, 4):
        L = l * (l + 1)
        P = sp.legendre(l, x)
        res = dR(static(h_even(0, H1f, 0, 0, P)))
        ctr = sp.Integer(L) / (r**2 if MUT == 'h1c' else 2 * r**2)
        sg = [g for g in (1, -1) if zero(res[0, 1] - g * ctr * H1f * P)]
        sg2 = [g for g in (1, -1) if zero(res[0, 2] - g * sp.diff(F * H1f, r) * sp.diff(P, x) / 2)]
        others = [k for k, v in res.items() if k not in ((0, 1), (0, 2)) and not zero(v)]
        ok = len(sg) == 1 and len(sg2) == 1 and not others
        ok1 = ok1 and ok
        rows.append(f"l = {l}: tr sign {sg}, tx sign {sg2}, other nonzero {others}")
    check('X1', ok1, 'H1 only: delta R_tr = s L H1 P/(2r^2), delta R_tx = s\' (F H1)\' P\'/2, the rest 0: ' + '; '.join(rows))

# ---------------------------------------------------------------- X2: converse at s = 0
if want('X2'):
    psi = sp.Function('psi')(r)
    ok2, rows = True, []
    for l in (2, 3, 4):
        lm = lam_of(l)
        _, ders = reducer(V_dg(lm))
        K = fD(lm) * psi + F * sp.diff(psi, r)
        H2 = sp.diff(F * (hD(lm) * psi + r * sp.diff(psi, r)), r) - K
        res = dR(static(h_even(H2, 0, H2, K, sp.legendre(l, x))))
        bad = [k for k, v in res.items() if not zero(reduce_fn(v, psi, ders))]
        ok2 = ok2 and not bad
        rows.append(f"l = {l}: nonzero {bad}")
    check('X2', ok2, 'DG06 (3)-(4) at s = 0, H1 = 0, H0 = H2, psi_xx = V psi: all 10 components vanish: ' + '; '.join(rows))

# ---------------------------------------------------------------- X3-X5: certificates on the static forms
k0, hh0 = sp.symbols('k0 hh0')


def flow(lm, Mv=M):
    a = (lm + 1) if MUT == 'flowc' else lm
    fK = (a / Mv) * k0 - ((lm * r + 2 * Mv) / (Mv * r)) * hh0
    fH = (lm / Mv) * k0 - ((lm * r**2 - 2 * (lm - 1) * Mv * r - 2 * Mv**2) / (Mv * r * (r - 2 * Mv))) * hh0
    return fK, fH


FORMS = {}


def forms(l, Mv):
    """Static radial forms (x = 0, 1/3, 3/5) and their first two r-derivatives, at M = Mv."""
    if l not in FORMS:
        FORMS[l] = dR(static(h_even(FN['H0'], FN['H1'], FN['H2'], FN['K'], sp.legendre(l, x))))
    base = []
    for _, v in sorted(FORMS[l].items()):
        v0 = jetify(v).subs(M, Mv)
        for x0 in (0, sp.Rational(1, 3), sp.Rational(3, 5)):
            e = sp.cancel(v0.subs(x, x0))
            if e != 0:
                base.append(e)
    d1 = [sp.cancel(Dj(e)) for e in base]
    d2 = [sp.cancel(Dj(e)) for e in d1]
    used = sorted({c for e in base + d1 + d2 for c in e.free_symbols if c in JET.values()}, key=str)
    return base, d1, d2, used


def fieldpt(Mv):
    if Mv == M:
        return sp.QQ.frac_field(r, M), {r: sp.Rational(37, 7), M: sp.Rational(-13, 11)}
    return sp.QQ.frac_field(r), {r: sp.Rational(37, 7)}


if want('X3'):
    ok3, msgs = True, []
    for Mv in (M, sp.Integer(0)):
        for l in (2, 3, 4):
            lm = lam_of(l)
            base, d1, d2, used = forms(l, Mv)
            field, pt = fieldpt(Mv)
            oka, ma = member(base, JET['H1', 0], used, field, pt, f"M = {Mv}, l = {l} (i) H1")
            okb, mb = member(base, JET['H0', 0] - JET['H2', 0], used, field, pt, f"M = {Mv}, l = {l} (i) H0 - H2")
            Fv = 1 - 2 * Mv / r
            ps = psi9(lm, JET['H2', 0], JET['K', 0], JET['K', 1]).subs(M, Mv)
            Z0 = sp.cancel(Fv * Dj(Fv * Dj(ps)) - V_dg(lm, Mv) * ps)
            okz, mz = member(base + d1 + d2, Z0, used, field, pt, f"M = {Mv}, l = {l} (ii) Z0")
            ok3 = ok3 and oka and okb and okz
            msgs += [ma, mb, mz]
            print('  ' + ma + '\n  ' + mb + '\n  ' + mz, flush=True)
    check('X3', ok3, '; '.join(msgs))

if want('X4'):
    ok4a, rows = True, []
    Kf, Hf = sp.Function('Kf')(r), sp.Function('Hf')(r)
    for l in (2, 3, 4):
        lm = lam_of(l)
        fK, fH = flow(lm)

        def Dflow(e):
            return sp.diff(e, r) + fK * sp.diff(e, k0) + fH * sp.diff(e, hh0)
        dK, dH = [k0, fK], [hh0, fH]
        for _ in range(2):
            dK.append(sp.cancel(Dflow(dK[-1])))
            dH.append(sp.cancel(Dflow(dH[-1])))
        rep = {Kf: k0, Hf: hh0}
        for k in range(1, 4):
            rep[sp.Derivative(Kf, (r, k))] = dK[k]
            rep[sp.Derivative(Hf, (r, k))] = dH[k]
        res = dR(static(h_even(Hf, 0, Hf, Kf, sp.legendre(l, x))))
        bad = [k for k, v in res.items() if not zero(v.xreplace(rep))]
        ok4a = ok4a and not bad
        rows.append(f"(a) l = {l}: nonzero {bad}")
    ok4b = True
    for l in (2, 3):
        lm = lam_of(l)
        fK, fH = flow(lm)
        base, d1, d2, used = forms(l, M)
        field, pt = fieldpt(M)
        sub = {k0: JET['K', 0], hh0: JET['H2', 0]}
        for nm, z in (("K'", JET['K', 1] - fK.subs(sub)), ("H'", JET['H2', 1] - fH.subs(sub))):
            ok, m_ = member(base + d1, sp.cancel(z), used, field, pt, f"(b) l = {l} {nm} flow")
            ok4b = ok4b and ok
            rows.append(m_)
            print('  ' + m_, flush=True)
    check('X4', ok4a and ok4b, '; '.join(rows))

if want('X5'):
    ok5, rows = True, []
    for l in (2, 3):
        lm = lam_of(l)
        base, d1, d2, used = forms(l, M)
        field, pt = fieldpt(M)
        ps = psi9(lm, JET['H2', 0], JET['K', 0], JET['K', 1])
        dps = Dj(ps)
        K3 = fD(lm) * ps + F * dps
        H3 = Dj(F * (hD(lm) * ps + r * dps)) - K3
        for nm, z in (('K', JET['K', 0] - K3), ('H2', JET['H2', 0] - H3)):
            ok, m_ = member(base + d1 + d2, sp.cancel(z), used, field, pt, f"l = {l} {nm} - {nm}_3(psi)")
            ok5 = ok5 and ok
            rows.append(m_)
            print('  ' + m_, flush=True)
    check('X5', ok5, '; '.join(rows))

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL), f'({time.time() - T0:.0f} s)')
sys.exit(1 if FAIL else 0)
