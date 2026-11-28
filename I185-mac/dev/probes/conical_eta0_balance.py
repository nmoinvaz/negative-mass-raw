"""Dominant-balance (Newton polygon) code for polynomial ODEs in t = ln(eta), used by conical_eta0.py (issue #185).

The equation is a polynomial E(F, P, Q; s) with P = F_t, Q = F_tt, s = exp(2t) = eta^2 (t -> -infinity, T = -t -> +infinity).
Every regime fixes how the variables scale and returns the faces of the Newton polygon: the exponents at which two or more
monomials tie for dominance, the truncated equation on the face, and its solutions. Exact rational arithmetic throughout.

Regimes (z is the one free exponent):
  exp    F = f + d, d = c e^{pt}(T^r): d, P = p d, Q = p^2 d all ~ X, s = X^sigma, sigma = 2/p.  weight (a+b+c) + sigma e, min.
  alg    F = f + d, d = c T^{-g}: P = -d/dt..., weights g a + (g + 1) b + (g + 2) c, min (s dropped: exponentially small).
  const  P -> p0 != 0, F ~ T, Q ~ T^{-th}: weight a - th c (max), admissible iff th >= 1.
  iter   P = a T^{-m} (m <= 1: F grows like T^(1-m), or ln T at m = 1): weight a w_F - m b - (m + 1) c (max).
  big    F = c e^{-pt} large: (F, P, Q) = F (1, -p, p^2): the top-degree part, roots in p.
"""
from fractions import Fraction

import sympy as sp

Fs, Ps, Qs, Ss, Ds = sp.symbols("F P Q s d")


def monos(expr, variables):
    """{exponent tuple: coefficient} of a polynomial expression in `variables`"""
    P = sp.Poly(sp.expand(expr), *variables)
    return {m: c for m, c in zip(P.monoms(), P.coeffs()) if c != 0}


def envelope(lines, extremum="min", zmin=Fraction(0), zmax=None, incl_max=False):
    """lines: {key: (a, b)}, weight a + b z (Fractions). The dominant (min or max) line group changes or ties at breakpoints.
    Returns [('interval', (z0, z1 or None), keys), (z, keys_tied), ...] in z order: the dominant keys on every open interval
    between breakpoints, and the tied keys at every breakpoint where >= 2 distinct lines tie for dominance."""
    sgn = 1 if extremum == "min" else -1
    groups = {}
    for k, (a, b) in lines.items():
        groups.setdefault((Fraction(a), Fraction(b)), []).append(k)
    ln = list(groups)

    def best(z):
        w = {g: sgn * (g[0] + g[1] * z) for g in ln}
        m = min(w.values())
        return [g for g in ln if w[g] == m]

    cand = set()
    for i in range(len(ln)):
        for j in range(i + 1, len(ln)):
            (a1, b1), (a2, b2) = ln[i], ln[j]
            if b1 != b2:
                z = (a2 - a1) / (b1 - b2)
                if z > zmin and (zmax is None or z < zmax or (incl_max and z == zmax)):
                    cand.add(z)
    pts = sorted(z for z in cand if len(best(z)) >= 2)
    edges = [zmin] + pts + ([zmax] if zmax is not None and (not pts or pts[-1] != zmax) else [])
    out = []
    for i, (z0, z1) in enumerate(zip(edges[:-1], edges[1:])):
        out.append(("interval", (z0, z1), [k for g in best((z0 + z1) / 2) for k in groups[g]]))
    if zmax is None:
        z0 = edges[-1]
        out.append(("interval", (z0, None), [k for g in best(z0 + 1) for k in groups[g]]))
    res = []
    # merge consecutive intervals with the same dominant keys only if no tie between them (none are dropped: ties are kept)
    for z in pts:
        res.append((z, [k for g in best(z) for k in groups[g]]))
    return sorted(out + res, key=lambda r: (r[1][0] if r[0] == "interval" else r[0], 0 if r[0] == "interval" else 1))


def poly_in(E, f):
    """E(F, P, Q, s) at F = f + d, as {(a, b, c, e): coeff} over (d, P, Q, s)"""
    return monos(E.subs(Fs, f + Ds), (Ds, Ps, Qs, Ss))


# --------------------------------------------------------------------------------------------------------------
# exponential regime: d = c e^{pt}
# --------------------------------------------------------------------------------------------------------------
def regime_exp(E, f):
    """faces of E at F = f + c e^{pt}. Returns a list of dicts: kind 'vertex' (all p allowed, p = roots of g) or 'tie' (sigma = 2/p)."""
    mo = poly_in(E, f)
    lines = {m: (m[0] + m[1] + m[2], m[3]) for m in mo}  # weight = degree + sigma*e
    out = []
    p = sp.Symbol("p", positive=True)
    c = sp.Symbol("c", real=True)
    for ev in envelope(lines, "min"):
        if ev[0] == "interval":
            _, rng, keys = ev
            # group by (degree, e): g_{deg,e}(p) = sum coeff p^(b + 2c)
            tops = {}
            for k in keys:
                tops.setdefault((k[0] + k[1] + k[2], k[3]), []).append(k)
            assert len(tops) == 1
            (deg, e), ks = list(tops.items())[0]
            g = sp.expand(sum(mo[k] * p ** (k[1] + 2 * k[2]) for k in ks))
            out.append({"kind": "vertex", "sigma_range": rng, "deg": deg, "e": e, "g": sp.factor(g), "roots_p": sp.roots(sp.Poly(g, p))})
        else:
            sig, keys = ev
            pv = sp.Rational(2) / sp.Rational(sig.numerator, sig.denominator)
            expr = 0
            for k in keys:
                expr += mo[k] * c ** (k[0] + k[1] + k[2]) * pv ** (k[1] + 2 * k[2])
            expr = sp.expand(expr)
            lead = sp.factor(expr)
            nz = sp.solve(sp.cancel(expr / c ** min(k[0] + k[1] + k[2] for k in keys)), c)
            out.append({"kind": "tie", "sigma": sig, "p": pv, "eq": lead, "c": nz})
    return out


# --------------------------------------------------------------------------------------------------------------
# algebraic regime: d = c T^{-g}, T = -t
# --------------------------------------------------------------------------------------------------------------
def regime_alg(E, f, gmax=None, _sym=[]):
    mo = poly_in(E, f)
    lines = {m: (m[1] + 2 * m[2], m[0] + m[1] + m[2]) for m in mo if m[3] == 0}  # weight = b + 2c + g (a + b + c)
    out = []
    c = sp.Symbol("c")
    for ev in envelope(lines, "min"):
        if ev[0] == "interval":
            continue
        g, keys = ev
        gv = sp.Rational(g.numerator, g.denominator)
        # d = c T^-g, P = d/dt d = -d/dT d... with T = -t: d/dt = -d/dT
        dd = c
        P = c * gv       # coefficient of T^(-g-1)
        Q = c * gv * (gv + 1)  # coefficient of T^(-g-2)
        expr = sum(mo[k] * dd ** k[0] * P ** k[1] * Q ** k[2] for k in keys)
        expr = sp.expand(expr)
        nz = sp.solve(sp.cancel(expr / c ** min(k[0] + k[1] + k[2] for k in keys)), c)
        out.append({"gamma": gv, "keys": keys, "eq": sp.factor(expr), "c": [sp.simplify(x) for x in nz if x != 0]})
    return out


# --------------------------------------------------------------------------------------------------------------
# P -> p0 (F ~ p0 t): Q ~ T^(-th), admissible iff th >= 1
# --------------------------------------------------------------------------------------------------------------
def regime_const(E):
    mo = monos(E, (Fs, Ps, Qs, Ss))
    lines = {m: (m[0], -m[2]) for m in mo if m[3] == 0}  # weight = a - th c, max
    out = []
    for ev in envelope(lines, "max", zmin=Fraction(0)):
        if ev[0] == "interval":
            _, rng, keys = ev
            out.append({"kind": "interval", "theta_range": rng, "keys": keys})
        else:
            th, keys = ev
            out.append({"kind": "tie", "theta": th, "admissible": th >= 1, "keys": keys})
    return out, mo


# --------------------------------------------------------------------------------------------------------------
# P = a T^-m: iterated logarithms (F ~ T^(1-m) or ln T at m = 1)
# --------------------------------------------------------------------------------------------------------------
def regime_iter(E):
    mo = monos(E, (Fs, Ps, Qs, Ss))
    # F weight 1 - m (m < 1), P weight -m, Q weight -(m+1); at m = 1 F weight 0 (logarithmic)
    lines = {m: (-(m[2]), m[0] * (-1) + 0 - m[1] - m[2]) for m in mo if m[3] == 0}  # a_F*(1-m) - b*m - c*(m+1) = (a_F - c) + m(-a_F - b - c)
    lines = {m: (Fraction(m[0] - m[2]), Fraction(-m[0] - m[1] - m[2])) for m in mo if m[3] == 0}
    out = []
    a = sp.Symbol("a")
    for ev in envelope(lines, "max", zmin=Fraction(0), zmax=Fraction(1)):
        if ev[0] == "interval":
            continue
        m, keys = ev
        mv = sp.Rational(m.numerator, m.denominator)
        # P = a T^-m (coefficient a), Q = d/dt P = a m T^(-m-1); F coefficient: drop (F weight counted, value left symbolic)
        expr = sum(mo[k] * Fs ** k[0] * a ** k[1] * (a * mv) ** k[2] for k in keys)
        out.append({"m": mv, "keys": keys, "eq": sp.factor(sp.expand(expr))})
    # m = 1 exactly: F logarithmic; compare the Q and P^2 style ties directly
    return out, mo


# --------------------------------------------------------------------------------------------------------------
# large F: F = c e^{-pt}
# --------------------------------------------------------------------------------------------------------------
def regime_big(E):
    mo = monos(E, (Fs, Ps, Qs, Ss))
    p = sp.Symbol("p")
    top = max(m[0] + m[1] + m[2] for m in mo if m[3] == 0)
    g = sp.expand(sum(c_ * (-p) ** m[1] * (p ** 2) ** m[2] for m, c_ in mo.items() if m[3] == 0 and m[0] + m[1] + m[2] == top))
    return {"deg": top, "g": sp.factor(g), "roots_p": sp.roots(sp.Poly(g, p))}
