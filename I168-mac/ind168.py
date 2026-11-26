#!/usr/bin/env python3
"""ind168: the coordinator's independent check of #168 (criteria in README.md beside this file).

Own determinant of the conical block, own exact interval arithmetic over Fractions with branch and bound, own exponential
bounds and own RK4 integrator. Imports nothing from the negative-mass repository.

    python3 ind168.py [--mutate=NAME]
"""
import argparse
import math
import sys
import time
from fractions import Fraction as Q

import numpy as np
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["D-sign", "P-omega", "red-sigma", "box-omega", "ehat-alpha",
                                                   "regb-y", "cf-49", "y-thr", "small-root"])
MUT = ap.parse_args().mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def info(text):
    print(f"[info] {text} ({time.time() - T0:.0f} s)", flush=True)


# ----------------------------------------------------------------------------------------------------------------------
# exact interval arithmetic and branch and bound
# ----------------------------------------------------------------------------------------------------------------------

class Iv:
    __slots__ = ("lo", "hi")

    def __init__(self, lo, hi=None):
        self.lo = Q(lo)
        self.hi = Q(lo) if hi is None else Q(hi)
        assert self.lo <= self.hi

    def __add__(self, o):
        o = iv(o)
        return Iv(self.lo + o.lo, self.hi + o.hi)

    __radd__ = __add__

    def __neg__(self):
        return Iv(-self.hi, -self.lo)

    def __sub__(self, o):
        o = iv(o)
        return Iv(self.lo - o.hi, self.hi - o.lo)

    def __rsub__(self, o):
        return iv(o) - self

    def __mul__(self, o):
        o = iv(o)
        ps = (self.lo * o.lo, self.lo * o.hi, self.hi * o.lo, self.hi * o.hi)
        return Iv(min(ps), max(ps))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = iv(o)
        if not (o.lo > 0 or o.hi < 0):
            raise ZeroDivisionError("interval division by an interval containing 0")
        return self * Iv(1 / o.hi, 1 / o.lo)

    def __rtruediv__(self, o):
        return iv(o) / self

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        if n == 0:
            return Iv(1)
        a, b = self.lo ** n, self.hi ** n
        if n % 2 == 0:
            if self.lo <= 0 <= self.hi:
                return Iv(0, max(a, b))
            return Iv(min(a, b), max(a, b))
        return Iv(a, b)

    def absv(self):
        if self.lo >= 0:
            return self
        if self.hi <= 0:
            return -self
        return Iv(0, max(-self.lo, self.hi))


def iv(x):
    return x if isinstance(x, Iv) else Iv(x)


def prove(fn, box, pred, max_boxes=60000):
    """Branch and bound: True if pred(fn(sub-box)) on a cover of box. False on a midpoint counterexample or at the cap.
    Returns (ok, boxes, note)."""
    widths0 = {k: v[1] - v[0] for k, v in box.items()}
    stack = [box]
    n = 0
    while stack:
        bx = stack.pop()
        n += 1
        if n > max_boxes:
            return False, n, "box cap reached"
        mid = {k: (v[0] + v[1]) / 2 for k, v in bx.items()}
        try:
            if not pred(fn({k: Iv(x) for k, x in mid.items()})):
                return False, n, f"counterexample at {dict((k, float(x)) for k, x in mid.items())}"
        except ZeroDivisionError:
            return False, n, "division by zero at a midpoint"
        try:
            ok = pred(fn({k: Iv(*v) for k, v in bx.items()}))
        except ZeroDivisionError:
            ok = False
        if ok:
            continue
        k = max(bx, key=lambda q: (bx[q][1] - bx[q][0]) / widths0[q] if widths0[q] else 0)
        lo, hi = bx[k]
        m = (lo + hi) / 2
        b1, b2 = dict(bx), dict(bx)
        b1[k] = (lo, m)
        b2[k] = (m, hi)
        stack += [b1, b2]
    return True, n, "proved"


OMEGA_MAX = Q(200) if MUT == "box-omega" else Q(100)
BOX = {"s": (Q(0), Q(1, 500)), "b": (Q(0), Q(1, 500)), "a": (Q(0), Q(1, 1000)), "w": (-OMEGA_MAX, OMEGA_MAX)}


def coeffs(v):
    s, b, a, w = v["s"], v["b"], v["a"], v["w"]
    kap = 1 - b + s
    mu = 1 + 3 * s - b + 2 * s * s - 6 * b * s
    c = 1 + 2 * s
    M = mu + (b - s) * w
    return kap, mu, c, M, a, w


def Pw(v, x):
    kap, mu, c, M, a, w = coeffs(v)
    return -2 * a * kap * Q(x) ** 3 - M * Q(x) ** 2 + 4 * a * c * Q(x) + c * c - w * w


def dPw(v, x):
    kap, mu, c, M, a, w = coeffs(v)
    return -6 * a * kap * Q(x) ** 2 - 2 * M * Q(x) + 4 * a * c


# ----------------------------------------------------------------------------------------------------------------------
# K1, K2, K3: identities
# ----------------------------------------------------------------------------------------------------------------------

G, p, q, nu = sp.symbols("G p q nu")
sig = nu**2
bb = G**2 * sig
aa = G * sig
kap_s = 1 - bb + sig
mu_s = 1 + 3 * sig - bb + 2 * sig**2 - 6 * bb * sig
c_s = 1 + 2 * sig
c3 = -2 * G * sig * kap_s
c2 = -p * (2 * G * (G**2 - 1) * sig**2 + p * mu_s)
c1 = 4 * G * sig * c_s * p**4
c0 = p**4 * (c_s**2 * p**2 - 4 * G**2 * sig**2)
N_note = c3 * q**3 + c2 * q**2 + c1 * q + c0


def k1():
    F, F1, F2, eta = sp.symbols("F F1 F2 eta")
    w_ = F1 + eta * F2
    P_, Q_, Z_ = -(F1**2 + F * F2), -eta * w_ / 2, -w_ / 2
    Y_ = -(eta * F1**2 + (-1 if MUT == "D-sign" else 1) * F * w_ / 2)
    h_ = eta**2 * F1**2 / 2
    B = sp.Matrix([[P_ - h_, Q_, Z_], [Q_, -P_ - h_, Y_], [Z_, Y_, h_]])
    D8 = 8 * B.det()
    N_mine = sp.expand(D8.subs({F1: p * nu, F2: (q - p) * nu**2}).subs(eta, 1 / nu).subs(F, G))
    ok = sp.expand(N_mine - N_note) == 0
    check("K1", ok, f"8 det(block) in (G, p, q, nu) equals c3 q^3 + c2 q^2 + c1 q + c0 of the note: {ok}")
    return N_mine


def k2():
    om = 2 * G * sig / p
    M_s = mu_s + (bb - sig) * om
    wv = q / p**2
    P_note = -2 * aa * kap_s * wv**3 - M_s * wv**2 + 4 * aa * c_s * wv + c_s**2 + (1 if MUT == "P-omega" else -1) * om**2
    ok = sp.simplify(sp.expand(p**6 * P_note) - sp.expand(N_note)) == 0
    check("K2", ok, f"c3 q^3 + ... + c0 = p^6 P(q/p^2) with omega = 2 G sigma/p: {ok}")


def k3():
    Gs, r, s_, eh, sg, wv = sp.symbols("G r s ehat sigma w")
    # (ln G)' = G'/G with G' = sigma r; y = r/G; y' = r'/G - r G'/G^2
    s_e = (Gs**2 * eh - r**2) / (2 * Gs)
    yv = r / Gs
    y_prime = (2 * r + s_e) / Gs - r * (sg * r) / Gs**2
    claim = yv * (4 - yv) / 2 + (1 if MUT == "red-sigma" else -1) * sg * yv**2 + eh / 2
    ok1 = sp.simplify(y_prime - claim) == 0
    ok2 = sp.simplify((sg * r) / Gs - sg * yv) == 0
    eh_w = (r**2 + 2 * Gs * (sg * r**2 * wv)) / Gs**2
    ok3 = sp.simplify(eh_w - yv**2 * (1 + 2 * (Gs * sg) * wv)) == 0
    check("K3", ok1 and ok2 and ok3, f"y' = y(4 - y)/2 - sigma y^2 + ehat/2: {ok1}; (ln G)' = sigma y: {ok2}; "
          f"ehat = y^2 (1 + 2 a w) at s = sigma r^2 w: {ok3}")


# ----------------------------------------------------------------------------------------------------------------------
# K4: Lemma 1 on the box
# ----------------------------------------------------------------------------------------------------------------------

def k4():
    tests = [
        ("kappa in [0.998, 1.002]", lambda v: coeffs(v)[0], lambda I: I.lo >= Q(998, 1000) and I.hi <= Q(1002, 1000)),
        ("mu >= 0.99", lambda v: coeffs(v)[1], lambda I: I.lo >= Q(99, 100)),
        ("c in [1, 1.01]", lambda v: coeffs(v)[2], lambda I: I.lo >= 1 and I.hi <= Q(101, 100)),
        ("M >= 0.79", lambda v: coeffs(v)[3], lambda I: I.lo >= Q(79, 100)),
        ("(A) 4M - 3kappa > 0", lambda v: 4 * coeffs(v)[3] - 3 * coeffs(v)[0], lambda I: I.lo > 0),
        ("(B) kappa - 2M + 32a^2(c^2 - c - w^2) < 0",
         lambda v: (lambda k, m, c, M, a, w: k - 2 * M + 32 * a * a * (c * c - c - w * w))(*coeffs(v)), lambda I: I.hi < 0),
        ("(C) P(2) < 0", lambda v: Pw(v, 2), lambda I: I.hi < 0),
        ("(C) P(-2) < 0", lambda v: Pw(v, -2), lambda I: I.hi < 0),
        ("(C) P'(2) < 0", lambda v: dPw(v, 2), lambda I: I.hi < 0),
        ("(D) c^2 + 16 a kappa + 8 a c <= 1.05^2",
         lambda v: (lambda k, m, c, M, a, w: c * c + 16 * a * k + 8 * a * c)(*coeffs(v)), lambda I: I.hi <= Q(105, 100) ** 2),
    ]
    small = dict(BOX)
    small["w"] = (Q(-1, 2), Q(1, 2))
    tests_E = [(f"(E) P({x}) > 0", (lambda x_: (lambda v: Pw(v, x_)))(x), lambda I: I.lo > 0)
               for x in (Q(0), Q(1, 2), Q(-1, 2))]
    ok_all, notes = True, []
    for name, fn, pred in tests:
        ok, n, note = prove(fn, BOX, pred)
        ok_all &= ok
        notes.append(f"{name}: {ok} ({n} boxes{'' if ok else ', ' + note})")
    for name, fn, pred in tests_E:
        ok, n, note = prove(fn, small, pred)
        ok_all &= ok
        notes.append(f"{name}: {ok} ({n} boxes{'' if ok else ', ' + note})")
    check("K4", ok_all, f"Lemma 1 on the box (omega in [-{OMEGA_MAX}, {OMEGA_MAX}]): " + "; ".join(notes))


# ----------------------------------------------------------------------------------------------------------------------
# K5: Lemma 2
# ----------------------------------------------------------------------------------------------------------------------

def k5():
    a_, k_, M_, c_, om, x = sp.symbols("a kappa M c omega x", positive=True)
    Pm = -2 * a_ * k_ * (-x)**3 - M_ * x**2 + 4 * a_ * c_ * (-x) + c_**2 - om**2
    lhs = k_ * (1 - 2 * a_ * x)
    rhs = (k_ - M_) - 4 * a_ * c_ / x - (om**2 - c_**2) / x**2
    ok_a = sp.simplify(lhs - rhs + Pm / x**2) == 0  # lhs - rhs = -P(-x)/x^2, zero exactly when P(-x) = 0
    box = {"f": (Q(0), Q(1)), "u": (Q(0), Q(1, 500))}

    def parts(v):
        f, u = v["f"], v["u"]
        s, b = f * u, (1 - f) * u
        kap = 1 - b + s
        c = 1 + 2 * s
        fq = f * (1 - f)
        y2 = (2 * f + 2 * f * f * u + 6 * fq * u + 16 * fq * u * (c + c * c)) / kap
        y1 = 2 * (1 - 2 * f).absv() / kap
        y0 = 64 * fq * u / kap
        return y2, y1, y0

    alpha_claim = Q(199, 100) if MUT == "ehat-alpha" else Q(51, 25)
    r2 = prove(lambda v: parts(v)[0], box, lambda I: I.hi <= alpha_claim)
    r1 = prove(lambda v: parts(v)[1], box, lambda I: I.hi <= Q(201, 100))
    r0 = prove(lambda v: parts(v)[2], box, lambda I: I.hi <= Q(321, 10000))
    ok_c = Q(321, 10000) <= (Q(181, 50) - Q(201, 100)) / 50
    ok = ok_a and r2[0] and r1[0] and r0[0] and ok_c
    check("K5", ok, f"(a) identity from P(-x) = 0: {ok_a}; (b) y^2 coefficient <= {alpha_claim}: {r2[0]} ({r2[1]} boxes"
          f"{'' if r2[0] else ', ' + r2[2]}); y coefficient <= 201/100: {r1[0]} ({r1[1]}); constant <= 321/10000: "
          f"{r0[0]} ({r0[1]}); 321/10000 <= (beta - 201/100)/50: {ok_c}")


# ----------------------------------------------------------------------------------------------------------------------
# K6, K7: regime B and the small branch
# ----------------------------------------------------------------------------------------------------------------------

def k6():
    ymax = Q(1, 5) if MUT == "regb-y" else Q(1, 50)
    box = dict(BOX)
    box["y"] = (-ymax, ymax)
    del box["w"]
    lim = Q(121, 10000)

    def r2(v):
        s, b = v["s"], v["b"]
        kap = 1 - b + s
        mu = 1 + 3 * s - b + 2 * s * s - 6 * b * s
        return (b - s + v["y"] * mu / 2).absv() / kap

    def r1(v):
        s, b, a, y = v["s"], v["b"], v["a"], v["y"]
        return (2 * (1 + 2 * s) / (1 - b + s)) * a * a * y * y

    def r0(v):
        s, b, a, y = v["s"], v["b"], v["a"], v["y"]
        c = 1 + 2 * s
        return a * a * y.absv() * (c * c * y * y - 4).absv() / (2 * (1 - b + s))

    p2 = prove(r2, box, lambda I: I.hi <= lim)
    p1 = prove(r1, box, lambda I: I.hi <= lim**2)
    p0 = prove(r0, box, lambda I: I.hi <= lim**3)
    ok = p2[0] and p1[0] and p0[0] and 3 * lim <= Q(363, 10000)
    check("K6", ok, f"|y| <= {ymax}: |c2/c3|/|p| <= 121/10000: {p2[0]} ({p2[1]}{'' if p2[0] else ', ' + p2[2]}); "
          f"|c1/c3| <= (121/10000)^2 p^2: {p1[0]}; |c0/c3| <= (121/10000)^3 |p|^3: {p0[0]}; so 3 Theta <= 363/10000 |p|")


def k7():
    bound = 4 * Q(1, 500) + 8 * Q(1, 1000)
    ok = bound <= Q(16, 1000) and -2 + bound <= Q(-1984, 1000)
    check("K7", ok, f"4 sigma + 8 a <= {bound} on the box, so (ln|omega|)' <= {-2 + bound}: {ok}")


# ----------------------------------------------------------------------------------------------------------------------
# K8: the huge branch
# ----------------------------------------------------------------------------------------------------------------------

AL, BE = Q(51, 25), Q(181, 50)


def k8():
    su = {"s": (Q(0), Q(1, 500)), "u": (Q(0), Q(1, 500))}

    def g(v):
        y = v["y"]
        return (4 - y) / 2 - v["s"] * y - v["u"] * (AL * y + BE) / 2

    def gplus(v):
        y = v["y"]
        return (4 - y) / 2 - v["s"] * y + v["u"] * (AL * y + BE) / 2

    lo1 = Q(3, 2) if MUT == "y-thr" else Q(14923, 10000)
    b1 = dict(su, y=(Q(1, 50), Q(1)))
    r1 = prove(g, b1, lambda I: I.lo >= lo1)
    b2 = dict(su, y=(Q(1), Q(15, 4)))
    r2 = prove(lambda v: v["y"] * g(v), b2, lambda I: I.lo >= Q(1062, 10000))
    b3 = dict(su, y=(Q(17, 4), Q(17, 4)))
    r3 = prove(gplus, b3, lambda I: I.hi <= Q(-1042, 10000))
    r4 = prove(lambda v: -Q(1, 2) - v["s"] + v["u"] * AL / 2, su, lambda I: I.hi < 0)
    ok = r1[0] and r2[0] and r3[0] and r4[0]
    check("K8", ok, f"g >= {lo1} on [1/50, 1]: {r1[0]} ({r1[1]}{'' if r1[0] else ', ' + r1[2]}); y g >= 0.1062 on "
          f"[1, 15/4]: {r2[0]} ({r2[1]}); g+(17/4) <= -0.1042: {r3[0]}; slope of g+ < 0: {r4[0]}")


# ----------------------------------------------------------------------------------------------------------------------
# K9: the chain of Theorem A
# ----------------------------------------------------------------------------------------------------------------------

def exp_upper_taylor(x):
    x = Q(x)
    assert 0 <= x < 6
    s = sum(x**k / math.factorial(k) for k in range(5))
    return s + (x**5 / 120) / (1 - x / 6)


def k9():
    ce = AL * Q(9, 2) ** 2 + BE * Q(9, 2)
    cf = Q(49) if MUT == "cf-49" else Q(50)
    ok_ce = ce <= 58
    ok_cf = cf >= ce / 2 + Q(9, 2) ** 2
    x = Q(9, 2) * Q(1, 1000)  # 9 sigma0/2 with sigma0 <= u0 <= 1/1000
    ubar = Q(1, 1000) / (1 - x)  # e^x <= 1/(1 - x)
    ok_u = ubar <= Q(10046, 10**7)
    B = Q(1, 4) + 4 * cf * ubar
    ok_B = B <= Q(451, 1000) < Q(1, 2)
    H = B / Q(7, 2)
    ok_H = H <= Q(129, 1000)
    eH = exp_upper_taylor(Q(129, 1000))
    ok_eH = eH <= Q(114, 100)
    ok = ok_ce and ok_cf and ok_u and ok_B and ok_H and ok_eH
    check("K9", ok, f"c_e = {float(ce)} <= 58: {ok_ce}; c_f = {cf} >= c_e/2 + 81/4 = {float(ce / 2 + Q(81, 4))}: {ok_cf}; "
          f"ubar <= {float(ubar):.7g} <= 1.0046e-3: {ok_u}; B <= {float(B):.6f} <= 0.451: {ok_B}; H <= {float(H):.6f} "
          f"<= 0.129: {ok_H}; e^0.129 <= {float(eH):.6f} <= 1.14: {ok_eH}")


# ----------------------------------------------------------------------------------------------------------------------
# K10: re-solve one case with an own RK4
# ----------------------------------------------------------------------------------------------------------------------

def cubic_coeffs(Gv, pv, nv):
    s = nv * nv
    b = Gv * Gv * s
    kap = 1 - b + s
    mu = 1 + 3 * s - b + 2 * s * s - 6 * b * s
    c = 1 + 2 * s
    return [-2 * Gv * s * kap, -pv * (2 * Gv * (Gv * Gv - 1) * s * s + pv * mu), 4 * Gv * s * c * pv**4,
            pv**4 * (c * c * pv * pv - 4 * Gv * Gv * s * s)]


def pick_root(Gv, pv, nv, branch):
    rts = np.roots(cubic_coeffs(Gv, pv, nv))
    real = [z.real for z in rts if abs(z.imag) <= 1e-9 * max(1.0, abs(z))]
    if not real:
        raise ValueError("no real root")
    ws = [z / pv**2 for z in real]
    if branch == "huge":
        return real[int(np.argmin(ws))], min(ws)
    cand = [(z, wv) for z, wv in zip(real, ws) if 0.5 < wv < 2]
    if not cand:
        raise ValueError("no root w in (1/2, 2)")
    return cand[0]


def k10():
    branch = "small" if MUT == "small-root" else "huge"
    G0, zeta0, u0 = 1.0, 0.25, 1e-3
    s0 = u0 / (1 + G0**2)
    t0 = -0.5 * math.log(s0)
    y0 = 4 + zeta0
    p0 = s0 * G0 * y0
    ubar = math.exp(4.5 * s0) * u0
    h = 1.0 / 200
    nsteps = 2000
    lG, lp, t = math.log(G0), math.log(p0), t0
    ok_root, ok_b, ok_c = True, True, True
    worst_b, worst_c = 0.0, 0.0

    def rhs(tt, lGc, lpc):
        Gc, pc = math.exp(lGc), math.exp(lpc)
        qq, wv = pick_root(Gc, pc, math.exp(-tt), branch)
        return pc / Gc, qq / pc, wv

    try:
        for i in range(nsteps):
            k1g, k1p, w1 = rhs(t, lG, lp)
            a_now = math.exp(lG) * math.exp(-2 * t)
            if branch == "huge" and not (w1 <= -1 / (4 * a_now)):
                ok_root = False
            k2g, k2p, _ = rhs(t + h / 2, lG + h / 2 * k1g, lp + h / 2 * k1p)
            k3g, k3p, _ = rhs(t + h / 2, lG + h / 2 * k2g, lp + h / 2 * k2p)
            k4g, k4p, _ = rhs(t + h, lG + h * k3g, lp + h * k3p)
            lG += h / 6 * (k1g + 2 * k2g + 2 * k3g + k4g)
            lp += h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p)
            t = t0 + (i + 1) * h
            if not (math.isfinite(lG) and math.isfinite(lp)):
                raise ValueError("not finite")
            tau = t - t0
            y = math.exp(lp + 2 * t - lG)
            zeta = y - 4
            bb_ = 0.451 * math.exp(-7 * tau / 4)
            bc = 1.14 * (abs(zeta0) + 50 * ubar * tau) * math.exp(-2 * tau)
            worst_b = max(worst_b, abs(zeta) / bb_)
            worst_c = max(worst_c, abs(zeta) / bc)
            ok_b &= abs(zeta) <= bb_
            ok_c &= abs(zeta) <= bc
        Gv, pv = math.exp(lG), math.exp(lp)
        y_end = pv / (math.exp(-2 * t) * Gv)
        ok_end = abs(y_end - 4) <= 1e-6
        detail = (f"{branch} root: w <= -1/(4a) at every step: {ok_root}; (b) at every step: {ok_b} (largest |zeta|/bound "
                  f"{worst_b:.3g}); (c) at every step: {ok_c} (largest |zeta|/bound {worst_c:.3g}); y(tau = 10) = {y_end:.12f}, "
                  f"|y - 4| <= 1e-6: {ok_end}; G(tau = 10) = {Gv:.15f}")
        check("K10", ok_root and ok_b and ok_c and ok_end, detail)
    except (ValueError, FloatingPointError, OverflowError) as e:
        check("K10", False, f"{branch} root: the integration stopped at t - t0 = {t - t0:.3f}: {e}")


print(f"ind168.py  mutate={MUT}", flush=True)
for fn in (k1, k2, k3, k4, k5, k6, k7, k8, k9, k10):
    t1 = time.time()
    fn()
    info(f"{fn.__name__} done in {time.time() - t1:.0f} s")
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
