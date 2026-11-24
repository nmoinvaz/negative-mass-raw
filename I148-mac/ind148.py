#!/usr/bin/env python3
"""ind148: the coordinator's independent check of #148's certificate for the Zerilli forward direction at every l.

Reuses the coordinator's I143-mac/ind143.py operator (Lichnerowicz form) with P abstract and Legendre's equation, L
symbolic. #148's printed equations and certificate coefficients are read from zerilli_certificate_output.txt as data.
Shares no code with zerilli_certificate*.py or zerilli_derivation_lib.py. Criteria R0-R2 in I148-mac/README.md.
"""
import argparse
import re
import sys
import time

import sympy as sp
from sympy.polys.matrices import DomainMatrix

ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
ap.add_argument('--only', default='')
ap.add_argument('--output', required=True)          # comma list of Y ids to run (mutation runs); default all
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



Ls = sp.Symbol('L')
Pf = sp.Function('P')(x)
pP, qP = sp.symbols('pP qP')


def red_P(e):
    """Remove P'' and P''' by Legendre's equation; then P -> pP, P' -> qP."""
    P1 = sp.Derivative(Pf, x)
    k = -2 if MUT == 'legendre' else 2
    P2 = (k * x * P1 - Ls * Pf) / (1 - x**2)
    P3 = sp.diff(P2, x).subs(sp.Derivative(Pf, (x, 2)), P2)
    e = e.xreplace({sp.Derivative(Pf, (x, 3)): P3, sp.Derivative(Pf, (x, 2)): P2})
    e = e.xreplace({sp.Derivative(Pf, x): qP, Pf: pP})
    assert not e.has(sp.Derivative(Pf, x)) and not e.has(Pf)
    return e


def lin_pq(e):
    e = sp.cancel(sp.together(e))
    return sp.cancel(sp.diff(e, pP)), sp.cancel(sp.diff(e, qP)), e


ok_all = True
# ---------------------------------------------------------------- R0: planted
fn = [FN[n] for n in NAMES]
RA = dR(h_even(*fn, Pf))
ABS = {k: red_P(v.subs(t, 0)) for k, v in RA.items()}
if want('R0'):
    bad_a = []
    for l in (2, 3):
        Pl = sp.legendre(l, x)
        RE = dR(h_even(*fn, Pl))
        for k, v in RE.items():
            e1 = jetify(ABS[k].subs({Ls: l * (l + 1), pP: Pl, qP: sp.diff(Pl, x)}))
            if not zero(e1 - jetify(v.subs(t, 0))):
                bad_a.append((l, k))
    Psi = sp.Function('Psi')(r)
    Vrw = F * (Ls / r**2 - 6 * M / r**3)
    _, ders = reducer(Vrw)
    h1 = r * Psi / F
    h0 = F * sp.diff(F * h1, r) / s
    RO = dR(h_odd(h0, h1, Pf))
    bad_b = [k for k, v in RO.items() if not zero(reduce_fn(red_P(v.subs(t, 0)), Psi, ders))]
    check('R0', not bad_a and not bad_b, f"(a) abstract P at L = 6, 12 equals explicit P_2, P_3: differ {bad_a}; "
          f"(b) odd Regge-Wheeler with abstract P, L symbolic: nonzero {bad_b}")

# my radial forms
MINE = {}
shape = []
for nm, key, kind in (('tt', (0, 0), 'p'), ('tr', (0, 1), 'p'), ('rr', (1, 1), 'p'), ('tx', (0, 2), 'q'), ('rx', (1, 2), 'q')):
    cp, cq, _ = lin_pq(jetify(ABS[key]))
    MINE[nm] = cp if kind == 'p' else cq
    shape.append(nm if (cq if kind == 'p' else cp) != 0 or MINE[nm].has(x) else None)
cp, cq, _ = lin_pq(jetify(ABS[2, 2]) * (1 - x**2))
MINE['a'], MINE['b'] = cp, sp.cancel(cq / x)
cp, cq, _ = lin_pq(jetify(ABS[3, 3]) / (1 - x**2))
MINE['c'], MINE['d'] = cp, sp.cancel(cq / x)
shape += [n for n in 'abcd' if MINE[n].has(x)]
shape = [z_ for z_ in shape if z_]
if want('R0'):
    check('R0.shape', not shape, f"forms x-free and of the stated angular type: offenders {shape}")

# ---------------------------------------------------------------- #148's printed data
txt = open(args.output).read().splitlines()
loc = {str(v): v for v in JET.values()}
loc.update({'L': Ls, 'M': M, 'r': r, 's': s})
THEIRS, CERT = {}, {}
inside = False
for ln in txt:
    if ln.startswith('# even radial equations'):
        inside = True
        continue
    if inside:
        m_ = re.match(r'^#\s+(\w+): (.*)$', ln)
        if m_:
            THEIRS[m_.group(1)] = sp.sympify(m_.group(2), locals=loc)
        else:
            inside = False
    m_ = re.match(r'^# even certificate c\[(\w+), k=(\d)\] = (.*)$', ln)
    if m_:
        CERT[(m_.group(1), int(m_.group(2)))] = sp.sympify(m_.group(3), locals=loc)
if MUT == 'ccoef':
    CERT[('traceless', 0)] = CERT[('traceless', 0)] / 2

# ---------------------------------------------------------------- R1: their equations are consequences of mine
if want('R1'):
    field = sp.QQ.frac_field(r, M, s, Ls)
    pt = {r: sp.Rational(37, 7), M: sp.Rational(-13, 11), s: sp.Rational(5, 3), Ls: sp.Rational(23, 4)}
    span = {'tt': ['tt'], 'tr': ['tr'], 'rr': ['rr'], 'tx': ['tx'], 'rx': ['rx'], 'trace': list('abcd'), 'traceless': list('abcd')}
    ok1, rows = set(THEIRS) == set(span), []
    for nm, src_ in span.items():
        if nm not in THEIRS:
            continue
        forms = [MINE[k] for k in src_]
        cols = sorted({c for e in forms + [THEIRS[nm]] for c in e.free_symbols if c in JET.values()}, key=str)
        ok, msg = member(forms, THEIRS[nm], cols, field, pt, nm)
        ok1 = ok1 and ok
        rows.append(msg)
        print('  ' + msg, flush=True)
    check('R1', ok1, f"printed equations {sorted(THEIRS)}; " + '; '.join(rows))

# ---------------------------------------------------------------- R2: the certificate
if want('R2'):
    lm = (Ls - 2) / 2
    ps = psi9(lm, JET['H2', 0], JET['K', 0], JET['K', 1])
    Z = F * Dj(F * Dj(ps)) - (V_dg(lm) + s**2) * ps
    S_ = 0
    for (nm, k), c in CERT.items():
        e = THEIRS[nm]
        for _ in range(k):
            e = Dj(e)
        S_ += c * e
    diffe = Z - S_
    jets = sorted({c for c in sp.sympify(diffe).free_symbols if c in JET.values()}, key=str)
    badj = [str(j) for j in jets if not zero(sp.diff(diffe, j))]
    resid0 = zero(diffe.subs({j: 0 for j in jets}))
    q_ = (Ls - 2) * r + 6 * M
    dfac = set()
    for c in CERT.values():
        for f_, _ in sp.factor_list(sp.denom(sp.together(c)))[1]:
            dfac.add(sp.factor(f_))
    okd = all(any(sp.cancel(f_ / g_).is_number for g_ in (Ls, r, q_)) for f_ in dfac)
    check('R2', len(CERT) == 7 and not badj and resid0 and okd,
          f"{len(CERT)} coefficients {sorted(CERT)}; jets whose coefficient does not cancel {badj}; "
          f"denominator factors {sorted(map(str, dfac))} within L, r, (L-2)r + 6M {okd}")

print('ALL PASS' if not FAIL else 'FAILED: ' + ', '.join(FAIL), f'({time.time() - T0:.0f} s)')
sys.exit(1 if FAIL else 0)
