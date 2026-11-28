#!/usr/bin/env python3
"""ind310: kappa r_S c1 = -c/pi, the first law, and the r_S = 1 control at the 20 black universes of #212 (criteria in README.md).

    python3 ind310.py [--mutate=no-shift|rs-one]

Imports nothing from the repository; the formulas are those of I301-mac-review/ind301.py. Exit 1 when a check fails.
"""
import sys

import mpmath as mp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
mp.mp.dps = 30
RESULTS = []
# c and rho_h of notes/black_universe/README.md section 4 (#212)
MEMBERS = [("-10", "4.197082"), ("-3", "1.118725"), ("-2", "0.621184"), ("-1.5", "0.339617"), ("-1.1", "0.075763"), ("-1.01", "0.007824"),
           ("-1.001", "0.000785"), ("-1.0001", "0.000079"), ("-1", "0.000000"), ("-0.9999", "-0.000079"), ("-0.999", "-0.000786"),
           ("-0.99", "-0.007884"), ("-0.95", "-0.040055"), ("-0.9", "-0.081826"), ("-0.7", "-0.271920"), ("-0.5", "-0.524073"),
           ("-0.3", "-0.926754"), ("-0.2", "-1.284188"), ("-0.1", "-2.024885"), ("-0.01", "-7.002156")]


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


w1, w2, rh_off, k3 = mp.mpf(0), mp.mpf(0), mp.mpf(0), []
for cs, rhs in MEMBERS:
    c = mp.mpf(cs)
    K = -2 * c / mp.pi
    A = lambda y, c=c, K=K: 1 + c * (y * y + 1) + K * (y + (y * y + 1) * mp.atan(y))  # noqa: E731
    R = lambda y: mp.sqrt(1 + y * y)  # noqa: E731
    rh = mp.findroot(A, mp.mpf(rhs) if rhs != "0.000000" else mp.mpf("1e-3"))
    rh_off = max(rh_off, abs(rh - mp.mpf(rhs)))
    Ap = mp.diff(A, rh)
    kap = Ap / 2
    Rh, Rph = R(rh), mp.diff(R, rh)
    c1 = Rh / 2 + (0 if MUT == "no-shift" else Rph / Ap)
    rS = mp.mpf(1) if MUT == "rs-one" else Rh
    w1 = max(w1, abs(kap * rS * c1 / (K / 2) - 1))
    miss = abs(kap * c1 / (K / 2) - 1)
    k3.append((cs, miss, abs(1 - 1 / Rh)))

    def q(Lv, A=A, R=R, K=K, rh=rh):
        Lv = mp.mpf(Lv)
        F = lambda y: A(y) + 1 / Lv - 1  # noqa: E731
        rr = mp.findroot(F, rh)
        return K * Lv ** mp.mpf(1.5) / 3, 4 * mp.pi * Lv * R(rr) ** 2, mp.sqrt(Lv) * mp.diff(F, rr) / 2

    for Lv in ("0.7", "1.3"):
        dM = mp.diff(lambda l: q(l)[0], mp.mpf(Lv))
        dA = mp.diff(lambda l: q(l)[1], mp.mpf(Lv))
        w2 = max(w2, abs(dM / (q(Lv)[2] * dA / (8 * mp.pi)) - 1))
    print(f"  c = {cs:>8}: rho_h {mp.nstr(rh, 9):>13}, kappa {mp.nstr(kap, 9)}, r_S {mp.nstr(Rh, 9)}, c1 {mp.nstr(c1, 12)}; with r_S = 1: miss {mp.nstr(miss, 4)}")

check("K1", w1 < mp.mpf("1e-25") and rh_off <= mp.mpf("5e-7"), f"kappa r_S c1 = -c/pi at 20 members: worst relative {mp.nstr(w1, 3)} (bar 1e-25); rho_h against the README's 6 decimals: {mp.nstr(rh_off, 2)}")
check("K2", w2 < mp.mpf("1e-12"), f"first law at L = 0.7, 1.3 for 20 members: worst relative {mp.nstr(w2, 3)} (bar 1e-12)")
ok3 = all((abs(m - p) < mp.mpf("1e-20") and m > mp.mpf("1e-12")) if cs != "-1" else m < mp.mpf("1e-25") for cs, m, p in k3)
check("K3", ok3, "r_S = 1 misses by |1 - 1/r_S|: " + ", ".join(f"{cs} {mp.nstr(m, 3)}" for cs, m, _ in k3 if cs in ("-10", "-1.0001", "-1", "-0.01")))
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
