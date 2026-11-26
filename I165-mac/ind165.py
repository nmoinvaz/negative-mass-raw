#!/usr/bin/env python3
"""ind165: the coordinator's independent check of #165 (criteria in README.md beside this file).

Derives the static one-sign system with u_xrho != 0 in the invariant jets (u, b = rho u_rho, v = rho u_x / w, s) from
X-bar_i = rho X_i and the chain rule, solves the A and B components of [X1, X2] + X1 = 0 for sigma-bar, and compares C-bar
and the prolongations with the chain stored by #165. Imports nothing from the negative-mass repository.

    python3 ind165.py [--mutate=NAME] [--raw=<negative-mass-raw>/I165-rpi5]
"""
import argparse
import json
import os
import sys
import time

import sympy as sp
from sympy import QQ
from sympy.polys.domains import GF
from sympy.polys.fields import field
from sympy.polys.rings import ring

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None,
                choices=["plant-xr", "toy-flat", "phi3-cs", "strip-D", "c3-swap", "cert-coef", "psi-zero"])
ap.add_argument("--raw", default=os.path.join(os.path.dirname(HERE), "I165-rpi5"))
args = ap.parse_args()
MUT = args.mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def info(text):
    print(f"[info] {text} ({time.time() - T0:.0f} s)", flush=True)


# ----------------------------------------------------------------------------------------------------------------------
# generic machinery: vector fields as component tuples over a rational function field
# ----------------------------------------------------------------------------------------------------------------------

def apply(X, F, gens):
    """X F for a field element F; X a tuple of field elements (components on gens)."""
    out = 0
    for comp, g in zip(X, gens):
        if comp != 0:
            out = out + comp * F.diff(g)
    return out


def bracket(X, Y, gens, k):
    """Component k of [X, Y]: X(Y_k) - Y(X_k)."""
    return apply(X, Y[k], gens) - apply(Y, X[k], gens)


def apply_num(X, F, rgens):
    """Numerator of X F over the lcm of the denominators of X's components, F a ring element (no cancellation)."""
    comps = [(cm, g) for cm, g in zip(X, rgens) if cm != 0]
    L = comps[0][0].denom
    for cm, _ in comps[1:]:
        L = L.lcm(cm.denom)
    N = 0
    for cm, g in comps:
        N = N + L.exquo(cm.denom) * cm.numer * F.diff(g)
    return N


def strip(N, facs):
    """Remove every power of each factor in facs from N by exact division."""
    if N == 0:
        return N
    for q in facs:
        while True:
            Q, r = divmod(N, q)
            if r != 0:
                break
            N = Q
    return N


def proportional(F, G):
    """F = lambda G with lambda in Q, lambda != 0; returns (bool, lambda)."""
    if F == 0 or G == 0:
        return False, None
    lam = QQ(F.LC) / QQ(G.LC)
    return F - G.mul_ground(lam) == 0, lam


# ----------------------------------------------------------------------------------------------------------------------
# the stored objects under test
# ----------------------------------------------------------------------------------------------------------------------

K, u, b, v, s = field("u,b,v,s", QQ)
R = K.ring
ru, rb, rv, rs = R.gens
GENS = (u, b, v, s)

chain = json.load(open(os.path.join(args.raw, "chain", "chain.json")))


def stored(name):
    return R.from_dict({tuple(e): QQ(n, d) for e, n, d in chain["gens"][name]})


SF = {n: stored(n) for n in ("f0", "f1", "f2", "f11", "f12")}
dtxt = open(os.path.join(args.raw, "chain", "delta.txt")).read().strip()
DELTA = R.from_expr(sp.sympify(dtxt, locals={n: sp.Symbol(n) for n in "ubvs"}))
info(f"stored chain read: terms {[len(SF[n].terms()) for n in SF]}; stored Delta' {len(DELTA.terms())} terms")

# ----------------------------------------------------------------------------------------------------------------------
# the system in the invariant jets
# ----------------------------------------------------------------------------------------------------------------------

c = (1 - s**2) / (1 + s**2)
sg = 2 * s / (1 + s**2)
w = u * c - sg
w_u, w_s = w.diff(u), w.diff(s)
Phi1b = (b**2 * c**2 + v**2 - v**2 * w**2) / u                      # rho^2 Phi1, with rho a = v w
Psib = -2 * b * c * v                                                # rho^2 Psi
Phi3b = -b + (1 if MUT == "phi3-cs" else 2) * b**2 * c * sg          # rho^2 Phi3
A = v * w                                                            # rho u_x

# X-bar_i^0 (sigma-bar = 0) on (u, b, v, s); X-bar_i = X-bar_i^0 + sigma-bar_i T, T = d_s at fixed (u, A, B)
X1_0 = (A, Psib, Phi1b / w - (v / w) * (w_u * A), K.zero)
X2_0 = (b, b + Phi3b, (A + Psib) / w - (v / w) * (w_u * b), K.zero)
Tf = (K.zero, K.zero, -v * w_s / w, K.one)

t1 = time.time()
# A component: X1(X2 A) - X2(X1 A) + X1 A, with X1 A = Phi1b, X2 A = A + Psib; B component likewise
G_A, H_A = A + Psib, Phi1b
G_B, H_B = b + Phi3b, Psib
eA = apply(X1_0, G_A, GENS) - apply(X2_0, H_A, GENS) + H_A
eB = apply(X1_0, G_B, GENS) - apply(X2_0, H_B, GENS) + H_B
a11, a12 = apply(Tf, G_A, GENS), -apply(Tf, H_A, GENS)
a21, a22 = apply(Tf, G_B, GENS), -apply(Tf, H_B, GENS)
det = a11 * a22 - a12 * a21
sx = (-eA * a22 + a12 * eB) / det
sr = (-a11 * eB + a21 * eA) / det
info(f"sigma-bar solved ({time.time() - t1:.0f} s): numerators {len(sx.numer.terms())}, {len(sr.numer.terms())} terms; "
     f"denominators {len(sx.denom.terms())}, {len(sr.denom.terms())} terms")

X1 = tuple(x0 + sx * tc for x0, tc in zip(X1_0, Tf))
X2 = tuple(x0 + sr * tc for x0, tc in zip(X2_0, Tf))

t1 = time.time()
Cbar = bracket(X1, X2, GENS, 3) + X1[3]
info(f"C-bar built ({time.time() - t1:.0f} s): numerator {len(Cbar.numer.terms())} terms, denominator "
     f"{len(Cbar.denom.terms())} terms")
# consistency (info): the A, B components of [X1, X2] + X1 vanish by construction
info("u, A, B components of [X1, X2] + X1 vanish: "
     f"{(bracket(X1, X2, GENS, 0) + X1[0]) == 0}, "
     f"{(apply(X1, A + Psib, GENS) - apply(X2, Phi1b, GENS) + Phi1b) == 0}, "
     f"{(apply(X1, b + Phi3b, GENS) - apply(X2, Psib, GENS) + Psib) == 0}")

# ----------------------------------------------------------------------------------------------------------------------
# P1: the planted family u = c0 x + C0 ln rho + d0 at s = +-1
# ----------------------------------------------------------------------------------------------------------------------

def p1():
    ok_all, notes = True, []
    xs, rs_ = sp.symbols("x rho", positive=True)
    for c0, C0, u0 in ((2, 3, 5), (-1, sp.Rational(1, 2), 7), (3, -2, 1)):
        for x0, r0 in ((sp.Rational(1, 3), 2), (2, sp.Rational(1, 5))):
            d0 = u0 - c0 * x0 - C0 * sp.log(r0)
            U = c0 * xs + C0 * sp.log(rs_) + d0
            if MUT == "plant-xr":
                U = U + xs * rs_ / 7
            at = {xs: x0, rs_: r0}
            uv = sp.nsimplify(sp.simplify(U.subs(at)))
            av, bv = sp.simplify(U.diff(xs).subs(at)), sp.simplify(U.diff(rs_).subs(at))
            uxx, uxr, urr = (sp.simplify(U.diff(*d).subs(at)) for d in ((xs, 2), (xs, rs_), (rs_, 2)))
            for s0 in (1, -1):
                cs, ss = sp.Rational(1 - s0**2, 1 + s0**2), sp.Rational(2 * s0, 1 + s0**2)
                v0, v1, v2 = bv * cs, bv * ss, av / (uv * cs - ss)
                Ph1, Ps, Ph3 = (v0**2 + v2**2 - av**2) / uv, -2 * v0 * v2, -bv / r0 + (1 if MUT == "phi3-cs" else 2) * v0 * v1
                ok_a = sp.simplify(uxx - Ph1) == 0 and sp.simplify(uxr - Ps) == 0 and sp.simplify(urr - Ph3) == 0
                # invariant jets: b = rho u_rho, v = rho u_x / w, w = u c - sigma
                pt = [QQ(int(sp.fraction(q)[0]), int(sp.fraction(q)[1])) for q in
                      (sp.Rational(uv), sp.Rational(r0 * bv), sp.Rational(r0 * av / (uv * cs - ss)), sp.Rational(s0))]
                vals = []
                for f_ in (sx, sr, Cbar):
                    dn = f_.denom(*pt)
                    vals.append((dn != 0, f_.numer(*pt) == 0 if dn != 0 else None))
                ok_b = all(d and z for d, z in vals[:2])
                ok_c = vals[2][0] and vals[2][1]
                ok = ok_a and ok_b and ok_c
                ok_all &= ok
                if not ok:
                    notes.append(f"(c0, C0, u0) = ({c0}, {C0}, {u0}), (x, rho) = ({x0}, {r0}), s = {s0}: "
                                 f"(a) {ok_a}, (b) {ok_b}, (c) {ok_c}")
    check("P1", ok_all, "u = c0 x + C0 ln rho + d0, 3 parameter sets x 2 points x s = +-1: (a) u_xx = Phi1, u_xrho = Psi, "
          "u_rhorho = Phi3; (b) sigma-bar_x = sigma-bar_rho = 0 with nonzero denominators; (c) C-bar = 0 with nonzero "
          "denominator" + ("" if ok_all else "; failures: " + "; ".join(notes)))


# ----------------------------------------------------------------------------------------------------------------------
# P2: the toy systems through bracket, apply_num and strip
# ----------------------------------------------------------------------------------------------------------------------

def p2():
    Kt, p, q, r = field("p,q,r", QQ)
    tg = (p, q, r)
    X1t = (Kt.one, Kt.zero, Kt.zero)
    X2_bad = (Kt.zero, Kt.one, p * (q**2 + 1))
    X2_flat = (Kt.zero, Kt.one, q)
    X2_test = X2_flat if MUT == "toy-flat" else X2_bad
    C_t = bracket(X1t, X2_test, tg, 2)
    rq = Kt.ring.gens[1]
    ok1 = C_t != 0 and proportional(C_t.numer, rq**2 + 1)[0] and C_t.denom.is_ground
    f0t = strip(C_t.numer, []) if C_t != 0 else Kt.ring.zero
    f1t = strip(apply_num(X1t, f0t, Kt.ring.gens), []) if f0t != 0 else Kt.ring.zero
    f2t = strip(apply_num(X2_test, f0t, Kt.ring.gens), []) if f0t != 0 else Kt.ring.zero
    gb = sp.groebner([f0t.as_expr(), f2t.as_expr()], *[sp.Symbol(n) for n in "pqr"], domain=QQ) if f0t != 0 else None
    ok2 = f1t == 0 and gb is not None and list(gb.exprs) == [1]
    flat_ok = all(bracket(X1t, X2_flat, tg, k_) == 0 for k_ in range(3))
    check("P2", ok1 and ok2 and flat_ok, f"toy: bracket r component {C_t.as_expr()} (q^2+1 up to a constant: {ok1}); "
          f"f1 = {f1t.as_expr() if f1t != 0 else 0}, f2 = {f2t.as_expr() if f2t != 0 else 0}; groebner(f0, f2) = "
          f"{list(gb.exprs) if gb is not None else None} ([1]: {ok2}); flat toy bracket 0: {flat_ok}")


# ----------------------------------------------------------------------------------------------------------------------
# C1: denominators of sigma-bar against the stored Delta'
# ----------------------------------------------------------------------------------------------------------------------

def c1():
    q1, r1 = divmod(sx.denom, rs * ru * DELTA)
    q2, r2 = divmod(sr.denom, rs * ru * (rs**2 + 1) * DELTA)
    ok1 = r1 == 0 and q1.is_ground and q1 != 0
    ok2 = r2 == 0 and q2.is_ground and q2 != 0
    check("C1", ok1 and ok2, f"den(sigma-bar_x) = k s u Delta': {ok1} (k = {q1.as_expr() if ok1 else '-'}); "
          f"den(sigma-bar_rho) = k' s u (1+s^2) Delta': {ok2} (k' = {q2.as_expr() if ok2 else '-'})")


DOWN, rem = divmod(sx.denom, rs * ru)
DPOL = ru * (1 - rs**2) - 2 * rs
FACS = [ru, rb, rv, rs, rs - 1, rs + 1, rs**2 + 1, DPOL] + ([DOWN] if rem == 0 else [])
info(f"Delta'_165 = den(sigma-bar_x)/(s u): exact {rem == 0}, {len(DOWN.terms())} terms; "
     f"stored Delta' irreducible over Q: {len(sp.factor_list(DELTA.as_expr())[1]) == 1 and sp.factor_list(DELTA.as_expr())[1][0][1] == 1}")


def c2():
    facs = [f for f in FACS if not (MUT == "strip-D" and f == DPOL)]
    N0 = Cbar.numer
    f0m = strip(N0, facs)
    ok, lam = proportional(f0m, SF["f0"])
    check("C2", ok, f"numerator of C-bar ({len(N0.terms())} terms) stripped: {len(f0m.terms())} terms; "
          f"= lambda f0 (stored, {len(SF['f0'].terms())} terms): {ok}" + (f", lambda = {lam}" if ok else ""))


def c3():
    Xs = {1: X2, 2: X1} if MUT == "c3-swap" else {1: X1, 2: X2}
    ok_all, notes = True, []
    for Fn, i, Gn in (("f0", 1, "f1"), ("f0", 2, "f2"), ("f1", 1, "f11"), ("f1", 2, "f12")):
        t1 = time.time()
        N = apply_num(Xs[i], SF[Fn], R.gens)
        g = strip(N, FACS)
        ok, lam = proportional(g, SF[Gn])
        ok_all &= ok
        notes.append(f"X{i} {Fn} -> {len(g.terms())} terms, = lambda {Gn}: {ok}" + (f" (lambda = {lam})" if ok else "")
                     + f", {time.time() - t1:.0f} s")
    check("C3", ok_all, "; ".join(notes))


# ----------------------------------------------------------------------------------------------------------------------
# C4: two stored modular certificates, re-expanded over GF(p)
# ----------------------------------------------------------------------------------------------------------------------

def c4():
    ok_all, notes = True, []
    for p_, s0 in ((2147483629, 2), (2147483587, 7)):
        Rp, t, U, Bp, V = ring("t,u,b,v", GF(p_))

        def sl(terms):
            out = {}
            for (mu, mb, mv, ms), cf in terms:
                cf = QQ(cf)
                val = int(cf.numerator) * pow(int(cf.denominator), -1, p_) * pow(s0, ms, p_) % p_
                key = (0, mu, mb, mv)
                out[key] = (out.get(key, 0) + val) % p_
            return Rp.from_dict({k_: x for k_, x in out.items() if x})

        gl = [sl([(tuple(e), QQ(n, d)) for e, n, d in chain["gens"][nm]]) for nm in ("f0", "f1", "f2", "f11")]
        D0 = U * ((1 - s0 * s0) % p_) - 2 * s0
        Dl0 = sl(list(DELTA.terms()))
        gl.append(1 - t * U * V * Bp * D0 * Dl0)
        rec = json.load(open(os.path.join(args.raw, "certs", f"slice_p{p_}_s{s0}.json")))
        assert rec["p"] == p_ and rec["s0"] == s0 and len(rec["cofactors"]) == 5
        cofs = []
        for j, lst in enumerate(rec["cofactors"]):
            d_ = {}
            for m, cf in lst:
                d_[tuple(m)] = (d_.get(tuple(m), 0) + int(cf)) % p_
            if MUT == "cert-coef" and j == 0:
                m0 = next(iter(d_))
                d_[m0] = (d_[m0] + 1) % p_
            cofs.append(Rp.from_dict({k_: x for k_, x in d_.items() if x}))
        tot = sum((cf * g for cf, g in zip(cofs, gl)), Rp.zero)
        ok = tot != 0 and tot.is_ground
        ok_all &= ok
        notes.append(f"p = {p_}, s0 = {s0}: sum = {tot.as_expr() if ok else str(len(tot.terms())) + ' terms'} "
                     f"({'nonzero constant' if ok else 'not a nonzero constant'})")
    check("C4", ok_all, "modular evidence: " + "; ".join(notes))


# ----------------------------------------------------------------------------------------------------------------------
# C5, C6: s constant and s = 0, re-solved with dsolve
# ----------------------------------------------------------------------------------------------------------------------

def c5():
    x, rho = sp.symbols("x rho", positive=True)
    cc, ss = sp.symbols("c sigma", nonzero=True)
    kap = 2 * cc * ss
    Bf = sp.Function("B")
    sol = sp.dsolve(sp.Eq(Bf(rho).diff(rho), kap * Bf(rho)**2 / rho), Bf(rho))
    sols = sol if isinstance(sol, list) else [sol]
    ok_a = any(s_.rhs != 0 and sp.simplify((1 / s_.rhs + kap * sp.log(rho)).diff(rho)) == 0 for s_ in sols)
    k, d = sp.Function("k")(x), sp.Function("d")(x)
    W = k - kap * sp.log(rho)
    uu = -sp.log(W) / kap + d
    ok_b = sp.simplify(rho * uu.diff(rho) - 1 / W) == 0
    uxr, ur, ux = uu.diff(x, rho), uu.diff(rho), uu.diff(x)
    Rres = uxr if MUT == "psi-zero" else uxr * (uu * cc - ss) + 2 * cc * ur * ux
    Ks, Es, L, Ws = sp.symbols("K E L W")
    e = (Rres * rho * W**2).subs({k.diff(x): Ks, d.diff(x): Es}).subs(sp.log(W), L).subs(sp.log(rho), (k - Ws) / kap)
    e = sp.expand(sp.cancel(sp.together(e)))
    poly = sp.Poly(e, L, Ws)
    cL = poly.coeff_monomial(L)
    ratio = sp.simplify(cL / Ks) if cL != 0 else 0
    ok_c1 = cL != 0 and sp.simplify(cL.subs(Ks, 0)) == 0 and ratio != 0 and Ks not in ratio.free_symbols
    rest = sp.expand(e.subs(Ks, 0))
    r2 = sp.simplify(rest / (Es * Ws)) if rest != 0 else 0
    ok_c2 = rest != 0 and r2 != 0 and not ({Es, Ws, L} & r2.free_symbols)
    ok_d = sp.simplify(sp.wronskian([1, Ws, sp.log(Ws)], Ws)) != 0
    ok_e = sp.simplify(ux.subs({k.diff(x): 0, d.diff(x): 0})) == 0
    check("C5", ok_a and ok_b and ok_c1 and ok_c2 and ok_d and ok_e,
          f"(a) dsolve: 1/B = const - kappa ln rho: {ok_a}; (b) rho u_rho = 1/W: {ok_b}; (c) rho W^2 R = {e}: "
          f"L coefficient {cL} a nonzero multiple of K: {ok_c1}; at K = 0: {rest}, a nonzero multiple of E W: {ok_c2}; "
          f"(d) Wronskian(1, W, ln W) != 0: {ok_d}; (e) u_x = 0 at K = E = 0: {ok_e}")


def c6():
    x, rho = sp.symbols("x rho", positive=True)
    Uf = sp.Function("U")
    sol = sp.dsolve(Uf(rho).diff(rho, 2) + Uf(rho).diff(rho) / rho, Uf(rho))
    ok_a = sp.simplify((rho * sol.rhs.diff(rho)).diff(rho)) == 0 and sp.simplify(sol.rhs.diff(rho)) != 0
    f, g = sp.Function("f")(x), sp.Function("g")(x)
    uu = f * sp.log(rho) + g
    uxr, ur, ux = uu.diff(x, rho), uu.diff(rho), uu.diff(x)
    Rres = uxr if MUT == "psi-zero" else uu * uxr + 2 * ux * ur
    Fp, Gp, L = sp.symbols("Fp Gp L")
    e = sp.expand(Rres * rho).subs({f.diff(x): Fp, g.diff(x): Gp}).subs(sp.log(rho), L)
    e = sp.expand(e)
    cL = sp.Poly(e, L).coeff_monomial(L)
    ratio = sp.simplify(cL / (f * Fp)) if cL != 0 else 0
    ok_b1 = cL != 0 and ratio != 0 and not ({Fp, Gp, L} & ratio.free_symbols) and not ratio.has(f)
    rest = sp.expand(e.subs(Fp, 0))
    r2 = sp.simplify(rest / (f * Gp)) if rest != 0 else 0
    ok_b2 = rest != 0 and r2 != 0 and not ({Fp, Gp, L} & r2.free_symbols) and not r2.has(f)
    ok_c = sp.simplify(ux.subs({f.diff(x): 0, g.diff(x): 0})) == 0
    check("C6", ok_a and ok_b1 and ok_b2 and ok_c,
          f"(a) dsolve: u = {sol.rhs}, of the form f ln rho + g: {ok_a}; (b) rho R = {e}: L coefficient a nonzero "
          f"multiple of f f': {ok_b1}; at f' = 0: {rest}, a nonzero multiple of f g': {ok_b2}; (c) u_x = 0: {ok_c}")


print(f"ind165.py  mutate={MUT}  raw={args.raw}", flush=True)
for fn in (p1, p2, c1, c2, c3, c4, c5, c6):
    t1 = time.time()
    fn()
    info(f"{fn.__name__} done in {time.time() - t1:.0f} s")
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
