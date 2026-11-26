#!/usr/bin/env python3
"""ind184: the coordinator's independent check of #184 (criteria in README.md beside this file).

Own N from the block's determinant, own exact interval arithmetic over Fractions with branch and bound, own RK4. Imports
nothing from the negative-mass repository.

    python3 ind184.py [--mutate=NAME]
"""
import argparse
import sys
import time
from fractions import Fraction as Fr

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["q1-sign", "q2-coef", "q3-start"])
MUT = ap.parse_args().mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


# ---------------------------------------------------------------------------------------------------------------- N
F, F1, F2, eta = sp.symbols("F F1 F2 eta")
w_ = F1 + eta * F2
P_, Q_, Z_ = -(F1**2 + F * F2), -eta * w_ / 2, -w_ / 2
Y_ = -(eta * F1**2 + F * w_ / 2)
h_ = eta**2 * F1**2 / 2
Nraw = sp.expand(8 * sp.Matrix([[P_ - h_, Q_, Z_], [Q_, -P_ - h_, Y_], [Z_, Y_, h_]]).det())
G, p, q, nu, sig = sp.symbols("G p q nu sigma")
Nth = sp.expand(sp.cancel(Nraw.subs({F1: p * nu, F2: (q - p) * nu**2}).subs(eta, 1 / nu).subs(F, G)))
Nsig = sp.expand(Nth.subs(nu, sp.sqrt(sig)))  # N is even in nu, so a polynomial in sigma
assert not Nsig.has(sp.sqrt(sig))
A0 = Nsig.subs(sig, 0)
A1 = sp.expand(sp.diff(Nsig, sig).subs(sig, 0))
A2 = sp.expand(sp.diff(Nsig, sig, 2).subs(sig, 0) / 2)
assert sp.expand(A0 + sig * A1 + sig**2 * A2 - Nsig) == 0
print(f"[info] N = A0 + sigma A1 + sigma^2 A2 from the own determinant ({time.time() - T0:.0f} s)", flush=True)


# ---------------------------------------------------------------------------------------------------------- intervals
class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo, self.hi = Fr(lo), Fr(lo if hi is None else hi)

    def __add__(self, o):
        o = iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __mul__(self, o):
        o = iv(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(ps), max(ps))

    __rmul__ = __mul__

    def pw(self, n):
        a, b = self.lo ** n, self.hi ** n
        if n % 2 == 0 and self.lo <= 0 <= self.hi:
            return Iv(0, max(a, b))
        return Iv(min(a, b), max(a, b))

    def absv(self):
        return self if self.lo >= 0 else (Iv(-self.hi, -self.lo) if self.hi <= 0 else Iv(0, max(-self.lo, self.hi)))


def iv(x):
    return x if isinstance(x, Iv) else Iv(x)


VARS = sp.symbols("s omega pp kappa")


def poly_fn(expr):
    """Exact evaluator of a polynomial in VARS on intervals (Horner-free, term by term)."""
    P = sp.Poly(sp.expand(expr), *VARS)
    terms = [(m, Fr(int(sp.fraction(c)[0]), int(sp.fraction(c)[1]))) for m, c in P.terms()]

    def f(vals):
        tot = Iv(0)
        for m, c in terms:
            t = Iv(c)
            for v, e in zip(vals, m):
                if e:
                    t = t * v.pw(e)
            tot = tot + t
        return tot
    return f


def prove(fn, box, pred, cap=40000):
    w0 = [b[1] - b[0] for b in box]
    stack, n = [box], 0
    while stack:
        bx = stack.pop()
        n += 1
        if n > cap:
            return False, n, "box cap"
        mid = [Iv((a + b) / 2) for a, b in bx]
        if not pred(fn(mid)):
            return False, n, f"counterexample at {[float((a + b) / 2) for a, b in bx]}"
        if pred(fn([Iv(a, b) for a, b in bx])):
            continue
        k = max(range(len(bx)), key=lambda i: (bx[i][1] - bx[i][0]) / w0[i] if w0[i] else 0)
        a, b = bx[k]
        m = (a + b) / 2
        b1, b2 = list(bx), list(bx)
        b1[k], b2[k] = (a, m), (m, b)
        stack += [b1, b2]
    return True, n, "proved"


def subst(expr, theta, extra=1):
    s, om, pp, ka = VARS
    out = expr.subs({G: theta * (1 - s) / s, q: pp**2 * (om - 1), sig: ka * pp**2 * s**3 / 5}).subs(p, pp) * extra
    out = sp.cancel(sp.together(sp.expand(out)))
    num, den = sp.fraction(out)
    return num, den


def q1():
    s, om, pp, ka = VARS
    BOX = [(Fr(0), Fr(1)), (Fr(-1, 2), Fr(1, 2)), (Fr(0), Fr(1, 4)), (Fr(0), Fr(1))]
    notes, ok_all = [], True
    for theta in (1, -1):
        Nexpr = A0 + sig * A1 + sig**2 * A2
        dN = sp.diff(Nexpr, q)
        R = sig * A1 + sig**2 * A2
        items = {
            "a": (Nexpr / p**6, "end", Fr(-1, 2), (lambda I: I.lo > 0) if MUT == "q1-sign" else (lambda I: I.hi < 0)),
            "b": (Nexpr / p**6, "end", Fr(1, 2), lambda I: I.lo > 0),
            "c": (dN / p**4, "all", None, lambda I: I.lo > 0),
        }
        for key, (ex, mode, omv, pred) in items.items():
            num, den = subst(ex, theta)
            dpol = sp.Poly(den, *VARS)
            # the denominator must be a positive monomial (a power of s and pp) so that the sign is the numerator's
            assert len(dpol.terms()) == 1 and dpol.terms()[0][1] > 0, (key, den)
            fn = poly_fn(num)
            bx = list(BOX)
            if mode == "end":
                bx[1] = (omv, omv)
            r = prove(fn, bx, pred)
            ok_all &= r[0]
            notes.append(f"theta={theta} ({key}): {r[0]} ({r[1]} boxes{'' if r[0] else ', ' + r[2]})")
        # (d): |R|/(sigma u^2 p^6) <= 30, i.e. R s^2/(sigma p^6) in [-30, 30]
        num, den = subst(R * (1 / sig) / p**6, theta, extra=VARS[0]**2)  # times s^2 = 1/u^2, before cancelling
        dpol = sp.Poly(den, *VARS)
        assert len(dpol.terms()) == 1 and dpol.terms()[0][1] > 0
        dm = dpol.terms()[0]
        dterm = Fr(int(dm[1]))
        fn0 = poly_fn(num)

        def fnd(vals, fn0=fn0, dm=dm):
            v = fn0(vals)
            dv = Iv(1)
            for var, e in zip(vals, dm[0]):
                if e:
                    dv = dv * var.pw(e)
            return v, dv

        # the denominator is a monomial; only accept it if it is a constant (no division by a vanishing box variable)
        if any(dm[0]):
            ok_all = False
            notes.append(f"theta={theta} (d): denominator {den} is not a constant; not decided by this code")
            continue
        r = prove(lambda vals: fn0(vals) * Iv(Fr(1) / dterm), BOX, lambda I: I.lo >= -30 and I.hi <= 30)
        ok_all &= r[0]
        notes.append(f"theta={theta} (d): {r[0]} ({r[1]} boxes{'' if r[0] else ', ' + r[2]})")
    check("Q1", ok_all, "Lemma 1 on the box s in [0,1], omega in [-1/2,1/2], p in [0,1/4], kappa in [0,1]: " + "; ".join(notes))


def q2():
    e = sp.Symbol("e")
    Nq = sp.expand((A0 + sig * A1 + sig**2 * A2).subs(q, -p**2 + sig * e))
    c1 = sp.Poly(Nq, sig).coeff_monomial(sig)
    sol = sp.solve(c1, e)
    k = 4 if MUT == "q2-coef" else 2
    ok = len(sol) == 1 and sp.simplify(sol[0] + p**2 * (G - 1)**2 / k) == 0
    check("Q2", ok, f"sigma^1 coefficient {sp.factor(c1)}; e = {sol} (want -p^2 (G - 1)^2/{k}): {ok}")


def q3():
    mp.mp.dps = 30
    coefs = [sp.lambdify((G, p, sig), sp.Poly(A0 + sig * A1 + sig**2 * A2, q).coeff_monomial(q**k), "mpmath")
             for k in (4, 3, 2, 1, 0)]
    deg = sp.Poly(A0 + sig * A1 + sig**2 * A2, q).degree()
    coefs = coefs[4 - deg:]

    def root(g, pv, t):
        sv = mp.e ** (-2 * t)
        cs = [c(g, pv, sv) for c in coefs]
        rts = mp.polyroots(cs, maxsteps=200, extraprec=80)
        cand = [mp.re(r) for r in rts if abs(mp.im(r)) <= mp.mpf(10) ** -15 * (1 + abs(r))
                and -1.5 * pv**2 <= mp.re(r) <= -0.5 * pv**2]
        if len(cand) != 1:
            raise ValueError(f"{len(cand)} roots in [-3p^2/2, -p^2/2] at t = {mp.nstr(t, 6)}")
        return cand[0]

    g, pv = (mp.mpf(3), mp.mpf(1) / 2) if MUT == "q3-start" else (mp.mpf(3), mp.mpf(1) / 10)
    t, t1, g1, p1 = mp.log(mp.mpf(10) ** 4), mp.log(mp.mpf(10) ** 4), g, pv
    tend = mp.log(mp.mpf(10) ** 12)
    h = mp.mpf(1) / 50
    ok, worst, n = True, None, 0

    def inD(gg, pp_, tt):
        return 0 < pp_ <= mp.mpf(1) / 4 and mp.e ** (-2 * tt) * (1 + abs(gg)) ** 3 <= pp_**2 / 5

    try:
        if not inD(g, pv, t):
            raise ValueError("start state not in D")
        while t < tend - h / 2:
            k1 = (pv, root(g, pv, t))
            k2 = (pv + h / 2 * k1[1], root(g + h / 2 * k1[0], pv + h / 2 * k1[1], t + h / 2))
            k3 = (pv + h / 2 * k2[1], root(g + h / 2 * k2[0], pv + h / 2 * k2[1], t + h / 2))
            k4 = (pv + h * k3[1], root(g + h * k3[0], pv + h * k3[1], t + h))
            g += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            pv += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            t += h
            n += 1
            qv = root(g, pv, t)
            ratio = qv / pv**2
            lower = g1 + mp.mpf(4) / 5 * mp.log(1 + 5 * p1 * (t - t1) / 4)
            if not (inD(g, pv, t) and -1.25 <= ratio <= -0.75 and g >= lower):
                ok = False
                worst = (mp.nstr(t, 8), mp.nstr(ratio, 8), mp.nstr(g - lower, 8))
                break
        check("Q3", ok, f"from (G, p) = ({mp.nstr(g1, 3)}, {mp.nstr(p1, 3)}) at eta = 1e4 to 1e12, {n} steps: in D, "
              f"q/p^2 in [-5/4, -3/4], G above the bound of Theorem 1 at every step: {ok}; G(1e12) = {mp.nstr(g, 15)}, "
              f"p(1e12) = {mp.nstr(pv, 12)}" + ("" if ok else f"; first violation {worst}"))
    except ValueError as e:
        check("Q3", False, f"stopped: {e}")


print(f"ind184.py  mutate={MUT}", flush=True)
for fn in (q1, q2, q3):
    t1 = time.time()
    fn()
    print(f"[info] {fn.__name__} done in {time.time() - t1:.0f} s", flush=True)
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
