"""Diagnostic for L5: the same walk started at larger eta0 (series through eta^-4)."""
#!/usr/bin/env python3
"""ind167: the coordinator's independent check of #167 (criteria in README.md beside this file).

Own N = 8 det(block) for a conical shift, own coefficient and monomial analysis, own inward integration with root
tracking in mpmath. Imports nothing from the negative-mass repository and does not use the Rust crate.

    python3 ind167.py [--mutate=NAME]
"""
import argparse
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["d-sign", "eta0-coef", "even-b", "balance-coef", "start-C"])
MUT = ap.parse_args([]).mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def info(text):
    print(f"[info] {text} ({time.time() - T0:.0f} s)", flush=True)


F, F1, F2, eta = sp.symbols("F F1 F2 eta")


def build_N(mutated):
    w = F1 + eta * F2
    P_, Q_, Z_ = -(F1**2 + F * F2), -eta * w / 2, -w / 2
    Y_ = -(eta * F1**2 + (-1 if mutated else 1) * F * w / 2)
    h_ = eta**2 * F1**2 / 2
    B = sp.Matrix([[P_ - h_, Q_, Z_], [Q_, -P_ - h_, Y_], [Z_, Y_, h_]])
    return sp.expand(8 * B.det())


N = build_N(MUT == "d-sign")
N_ref = build_N(False)  # L5 integrates the unmutated N, so that d-sign's effect stays on L1 to L4
info("N built")

a3 = 2 * F * eta**2 * (F**2 - eta**2 - 1)
a2 = F1 * eta * (4 * F**3 + F**2 * F1 * eta**3 + 6 * F**2 * F1 * eta - 6 * F * eta**2 - 4 * F - F1 * eta**5
                 - 3 * F1 * eta**3 - 2 * F1 * eta)
a1 = 2 * F1**2 * (F**3 + F**2 * F1 * eta**3 + 6 * F**2 * F1 * eta + 2 * F * F1**2 * eta**4 + 4 * F * F1**2 * eta**2
                  - 3 * F * eta**2 - F - F1 * eta**5 - 3 * F1 * eta**3 - 2 * F1 * eta)
a0 = F1**3 * (F**2 * F1 * eta**2 + 2 * F**2 * F1 + 4 * F * F1**2 * eta**3 + 8 * F * F1**2 * eta - 2 * F * eta
              + F1**3 * eta**6 + 4 * F1**3 * eta**4 + 4 * F1**3 * eta**2 - F1 * eta**4 - 3 * F1 * eta**2 - 2 * F1)
N_note = sp.expand(a3 * F2**3 + a2 * F2**2 + a1 * F2 + a0)


def l5(e0start):
    mp.mp.dps = 30
    coef = [sp.lambdify((F, F1, eta), sp.Poly(N_ref, F2).coeff_monomial(F2**k), "mpmath") for k in (3, 2, 1, 0)]
    Finf = mp.mpf(1)
    Cc = mp.mpf(10) if MUT == "start-C" else mp.mpf(0)
    bcoef = Finf * (Finf**2 + 7)
    e0 = mp.mpf(e0start)

    def ser(x):
        L = mp.log(x)
        f = Finf - 2 * Finf / x**2 + (Cc + bcoef * L) / x**4
        f1 = 4 * Finf / x**3 + (bcoef / x - 4 * (Cc + bcoef * L) / x) / x**4
        f2 = -12 * Finf / x**4 + (-bcoef / x**2 - 4 * bcoef / x**2 + 20 * (Cc + bcoef * L) / x**2) / x**4 \
            - 4 * bcoef / x**6
        return f, f1, f2

    def root(f, f1, x, ref):
        cs = [c(f, f1, x) for c in coef]
        rts = mp.polyroots(cs, maxsteps=200, extraprec=60)
        real = [mp.re(r) for r in rts if abs(mp.im(r)) <= mp.mpf(10) ** -12 * max(1, abs(r))]
        if not real:
            raise ValueError("no real root")
        return min(real, key=lambda r: abs(r - ref))

    f, f1, f2s = ser(e0)
    f2 = root(f, f1, e0, f2s)
    x = e0
    hist = []
    try:
        for it in range(200000):
            # step in t = ln eta, inward; |dt| limited so that F changes by at most 2 percent
            dF_dt = x * f1
            dt = -min(mp.mpf(1) / 400, mp.mpf("0.02") * abs(f) / max(abs(dF_dt), mp.mpf(10) ** -30))
            ref = f2

            def rhs(xx, ff, gg):
                hh = root(ff, gg, xx, ref)
                return xx * gg, xx * hh, hh  # dF/dt, dF'/dt, F''

            k1 = rhs(x, f, f1)
            x2 = x * mp.exp(dt / 2)
            k2 = rhs(x2, f + dt / 2 * k1[0], f1 + dt / 2 * k1[1])
            k3 = rhs(x2, f + dt / 2 * k2[0], f1 + dt / 2 * k2[1])
            x4 = x * mp.exp(dt)
            k4 = rhs(x4, f + dt * k3[0], f1 + dt * k3[1])
            f = f + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            f1 = f1 + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            x = x4
            f2 = root(f, f1, x, k4[2])
            hist.append((x, f))
            if f < mp.mpf(10) ** -4 or x < mp.mpf(10) ** -6:
                break
        (xa, fa), (xb, fb) = hist[-2], hist[-1]
        alpha = 2 / (xb**2 + 4)
        ya, yb = fa ** (1 / alpha), fb ** (1 / alpha)
        estar = xb - yb * (xa - xb) / (ya - yb)
        ok = fb < mp.mpf(10) ** -4 and abs(estar - mp.mpf("1.28193326312")) <= mp.mpf(10) ** -4
        print(f"eta0 = {e0start}:", ok, f"(F_inf, C) = (1, {mp.nstr(Cc, 3)}): walk ends at eta = {mp.nstr(xb, 12)} with F = {mp.nstr(fb, 3)}, "
              f"eta* = {mp.nstr(estar, 12)} (want 1.28193326312 within 1e-4): {ok}; {len(hist)} steps")
    except (ValueError, ZeroDivisionError) as e:
        print(f"eta0 = {e0start}: stopped", f"walk stopped at eta = {mp.nstr(x, 8)}, F = {mp.nstr(f, 4)}: {e}")



for e in (1000, 10000, 100000):
    l5(e)
