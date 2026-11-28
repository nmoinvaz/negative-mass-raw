import sympy as sp, time
import lib1 as L, lib2 as M
from lib1 import Ser
from sympy.polys.matrices import DomainMatrix

def prep(b, kap, N, symbolic=False, ngauge5=True):
    L.setdom(symbolic)
    L.KAPVAL = sp.Rational(kap) if not symbolic else None
    L.TRUNC = N + 4
    bg = L.build_background(b, (N + 4) // 2 + 2, symbolic)
    env = M.make_env(bg)
    E0j, ops = M.load_ops()
    coef = {k: [(fn, a, bb, M.evaluate(co, env)) for fn, a, bb, co in lst] for k, lst in ops.items()}
    r0, Om0, Th0 = [L.pi_to_ser(bg[x]) for x in ('r', 'Om', 'th')]
    # g_theta = dr0/dTh0 = r0_Pi / Th0_Pi  (univariate), as bivariate
    rp = [bg['r'][i] * i for i in range(1, len(bg['r']))]
    tp = [bg['th'][i] * i for i in range(1, len(bg['th']))]
    n = len(tp)
    # series division rp/tp
    q = []
    rem = rp[:] + [L.DOM.zero] * 3
    for i in range(n - 1):
        qi = rem[i] / tp[0]
        q.append(qi)
        for j in range(n):
            if i + j < len(rem): rem[i + j] -= qi * tp[j]
    g_th = L.pi_to_ser(q)
    return dict(bg=bg, env=env, coef=coef, r0=r0, Om0=Om0, Th0=Th0, g_th=g_th, N=N, E0j=E0j)

def mono_deriv(i, j, k, a, b):
    """d_V^a d_U^b of V^i U^j L^k, L = ln V: dict (i,j,k)->coef (python int)"""
    terms = {(i, j, k): 1}
    for _ in range(a):
        new = {}
        for (ii, jj, kk), c in terms.items():
            if ii != 0:
                new[(ii - 1, jj, kk)] = new.get((ii - 1, jj, kk), 0) + c * ii
            if kk > 0:
                new[(ii - 1, jj, kk - 1)] = new.get((ii - 1, jj, kk - 1), 0) + c * kk
        terms = new
    for _ in range(b):
        new = {}
        for (ii, jj, kk), c in terms.items():
            if jj != 0:
                new[(ii, jj - 1, kk)] = new.get((ii, jj - 1, kk), 0) + c * jj
        terms = new
    return terms

def build(P, fields, log, N=None):
    N = N or P['N']
    cols = [(f, i, j, k) for f in fields for i in range(N + 1) for j in range(N + 1 - i) for k in ((0, 1) if log else (0,))]
    cidx = {c: n for n, c in enumerate(cols)}
    rows = {}
    for eq, lst in P['coef'].items():
        for fn, a, b, C in lst:
            if fn not in fields: continue
            for (f, i, j, k), ci in cidx.items():
                if f != fn: continue
                for (ii, jj, kk), cc in mono_deriv(i, j, k, a, b).items():
                    for (p, q), cv_ in C.d.items():
                        m, n = ii + p, jj + q
                        if m + n > N - 2: continue
                        key = (eq, m, n, kk)
                        r = rows.setdefault(key, {})
                        r[ci] = r.get(ci, L.DOM.zero) + cv_ * L.DOM.convert(cc)
    return cols, cidx, rows

def ycols(P, cols, cidx, log, ymax):
    """rows expressing Y = dr - g_th dth, coefficient (i,j,k)"""
    out = {}
    for i in range(ymax + 1):
        for j in range(ymax + 1 - i):
            for k in ((0, 1) if log else (0,)):
                r = {}
                c = cidx.get(('dr', i, j, k))
                if c is not None: r[c] = L.DOM.one
                for (p, q), gv in P['g_th'].d.items():
                    c2 = cidx.get(('dth', i - p, j - q, k))
                    if c2 is not None: r[c2] = r.get(c2, L.DOM.zero) - gv
                out[(i, j, k)] = r
    return out

def to_dm(rowsdict, ncols, rowkeys=None):
    keys = rowkeys or list(rowsdict.keys())
    dok = {}
    for n, kk in enumerate(keys):
        for c, v in rowsdict[kk].items():
            if v != L.DOM.zero: dok[(n, c)] = v
    return DomainMatrix.from_dok(dok, (len(keys), ncols), L.DOM), keys

def target_series(P, kind, N, amp=1):
    """Y target coefficients dict (i,j)->L.DOM: kind 'VR' (c2 V R/R(0)), 'UR', 'R'"""
    R = P['bg']['r']
    R0 = R[0]
    out = {}
    for n, rn in enumerate(R):
        if 2 * n + 1 > N + 1: break
        val = rn * (L.DOM.one if n % 2 == 0 else -L.DOM.one) / R0 if kind != 'R' else rn * (L.DOM.one if n % 2 == 0 else -L.DOM.one)
        if kind == 'VR': out[(n + 1, n)] = val
        elif kind == 'UR': out[(n, n + 1)] = val
        elif kind == 'R': out[(n, n)] = val
    return {k: v * L.DOM.convert(amp) for k, v in out.items() if v != L.DOM.zero}

def solve_affine(P, fields, log, target, N=None, ymax=None, extra_rows=None):
    N = N or P['N']
    ymax = N if ymax is None else ymax
    cols, cidx, rows = build(P, fields, log, N)
    yr = ycols(P, cols, cidx, log, ymax)
    allrows = dict(rows)
    rhs = {}
    for key, r in yr.items():
        i, j, k = key
        allrows[('Y',) + key] = r
        rhs[('Y',) + key] = target.get((i, j), L.DOM.zero) if k == 0 else L.DOM.zero
    keys = list(allrows.keys())
    A, _ = to_dm(allrows, len(cols), keys)
    b = DomainMatrix([[rhs.get(kk, L.DOM.zero)] for kk in keys], (len(keys), 1), L.DOM)
    aug = A.hstack(b)
    rref, piv = aug.rref()
    nc = len(cols)
    consistent = nc not in piv
    out = dict(cols=cols, cidx=cidx, consistent=consistent, A=A, piv=piv, rref=rref, nullity=nc - len([p for p in piv if p < nc]))
    if consistent:
        x = [L.DOM.zero] * nc
        rl = rref.to_Matrix()
        for row, pc in enumerate(piv):
            x[pc] = L.DOM.from_sympy(rl[row, nc])
        out['xp'] = x
        out['Nb'] = A.nullspace()
    return out
