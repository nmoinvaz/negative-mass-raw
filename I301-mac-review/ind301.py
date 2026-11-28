#!/usr/bin/env python3
"""ind301: the static mass mode at c = -1.5, -0.3 and Schwarzschild from closed forms (criteria in README.md beside this file).

    python3 ind301.py [--mutate=no-shift|rs-one|no-norm]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import sys

import mpmath as mp
import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


rho, L, r, x = sp.symbols("rho L r x", positive=True)
c = sp.Symbol("c", negative=True)
K = -2 * c / sp.pi
A_bu = 1 + c * (rho ** 2 + 1) + K * (rho + (rho ** 2 + 1) * sp.atan(rho))

# J1: the asymptotic mass of r = sqrt(L) R, F_L = A + 1/L - 1 (black universes, c symbolic; Schwarzschild)
def mass_of(A, R):
    FL = A + 1 / L - 1
    Fr = sp.simplify(L * FL.subs(rho, r / sp.sqrt(L)))
    ser = sp.series(Fr.subs(r, 1 / x), x, 0, 2).removeO()
    return sp.simplify(ser.coeff(x, 0)), sp.simplify(-ser.coeff(x, 1) / 2)


c0b, Mb = mass_of(A_bu, sp.sqrt(1 + rho ** 2))
c0s, Ms = mass_of(1 - 1 / rho, rho)
dMb = sp.simplify(sp.diff(Mb, L).subs(L, 1))
dMs = sp.simplify(sp.diff(Ms, L).subs(L, 1))
check("J1", sp.simplify(c0b - 1) == 0 and sp.simplify(Mb - K / 3 * L ** sp.Rational(3, 2)) == 0 and sp.simplify(dMb - K / 2) == 0
      and sp.simplify(Ms - L ** sp.Rational(3, 2) / 2) == 0,
      f"black universe: M(L) = {Mb}, dM/dL = {dMb}; Schwarzschild: M(L) = {Ms}, dM/dL = {dMs}")

# J2, J3, J4 at the three members, 30 digits
mp.mp.dps = 30
MEMBERS = {}
for cv in ("-1.5", "-0.3"):
    cm = mp.mpf(cv)
    Kc = -2 * cm / mp.pi
    MEMBERS[f"c = {cv}"] = (lambda y, cm=cm, Kc=Kc: 1 + cm * (y * y + 1) + Kc * (y + (y * y + 1) * mp.atan(y)),
                             lambda y: mp.sqrt(1 + y * y), Kc / 2, Kc / 3, mp.mpf("0.5"))
MEMBERS["Schwarzschild 2M = 1"] = (lambda y: 1 - 1 / y, lambda y: y, mp.mpf("0.75"), mp.mpf("0.5"), mp.mpf("1.5"))

w2, w3, w4, rs_miss = mp.mpf(0), mp.mpf(0), mp.mpf(0), {}
for name, (Af, Rf, dM, m0, guess) in MEMBERS.items():
    rh = mp.findroot(Af, guess)
    Ap = mp.diff(Af, rh)
    kap = Ap / 2
    Rh, Rph = Rf(rh), mp.diff(Rf, rh)
    shift = mp.mpf(0) if MUT == "no-shift" else 1 / Ap            # d rho_h / dL at L = 1
    c1 = Rh / 2 + Rph * shift
    rS = mp.mpf(1) if MUT == "rs-one" else Rh
    lhs = kap * rS * c1
    rel = abs(lhs / dM - 1)
    w2 = max(w2, rel)
    rs_miss[name] = abs(kap * c1 / dM - 1)
    Kstat = (Rh ** 2 * Ap - 2 * rh * Af(rh)) / 2 + Rh * Rph          # 1/2 (R^2 A' - 2 rho A) + R R' at the horizon
    w4 = max(w4, abs((kap * Rh ** 2 + Rh * Rph) - Kstat))
    print(f"  {name}: rho_h {mp.nstr(rh, 12)}, kappa {mp.nstr(kap, 12)}, r_S {mp.nstr(Rh, 12)}, R'_h {mp.nstr(Rph, 8)}, c1 {mp.nstr(c1, 12)}; "
          f"kappa r_S c1 {mp.nstr(lhs, 15)}, dM/dL {mp.nstr(dM, 15)}, relative {mp.nstr(rel, 3)}; with r_S = 1: {mp.nstr(rs_miss[name], 3)}")

    def q(Lv, Af=Af, Rf=Rf, m0=m0, rh=rh):
        Lv = mp.mpf(Lv)
        F = lambda y: Af(y) + 1 / Lv - 1  # noqa: E731
        rr = mp.findroot(F, rh)
        kx = (1 if MUT == "no-norm" else mp.sqrt(Lv)) * mp.diff(F, rr) / 2
        return m0 * Lv ** mp.mpf(1.5), 4 * mp.pi * Lv * Rf(rr) ** 2, kx

    for Lv in ("0.7", "1.3"):
        dMdL = mp.diff(lambda l: q(l)[0], mp.mpf(Lv))
        dAdL = mp.diff(lambda l: q(l)[1], mp.mpf(Lv))
        w3 = max(w3, abs(dMdL / (q(Lv)[2] * dAdL / (8 * mp.pi)) - 1))

check("J2", w2 < mp.mpf("1e-25"), f"kappa r_S c1 = dM/dL at the three members: worst relative {mp.nstr(w2, 3)} (bar 1e-25); "
      + "with r_S = 1: " + ", ".join(f"{k}: {mp.nstr(v, 3)}" for k, v in rs_miss.items()))
check("J3", w3 < mp.mpf("1e-12"), f"first law along each family at L = 0.7, 1.3: worst relative {mp.nstr(w3, 3)} (bar 1e-12)")
check("J4", w4 < mp.mpf("1e-25"), f"kappa R_h^2 + R_h R'_h equals the static constant 1/2 (R^2 A' - 2 rho A) + R R' at the horizon: worst {mp.nstr(w4, 3)} (reported)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
