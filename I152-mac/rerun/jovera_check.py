#!/usr/bin/env python3
"""Recompute |J|/A of the symmetric rotating 5D wormhole from the exact solution printed in arXiv:2610.38659 (a recompute,
not a quote). Inputs, all printed there: Eq. (19) e^{2a}, Eq. (20) e^q, Eq. (21) kappa^2, Eq. (22) A_T, p(0) = 1/2 from the
gauge below Eq. (6), kappa = -16 G J/(pi r0^3) (Eq. (8)), s = pi lambda/4, r0 = 1. G is not stated in the text; the check
finds which G reproduces the printed values.
usage: python3 -I jovera_check.py [--mutate=G1|p0|exponent|lam]   exit 0 iff every case passes
Pass criterion, written before the run: the computed value rounds to the printed digits (G = 1/(4 pi) predicted); the
lambda -> 4 limit is 1/2 within 1e-6 and the lambda -> 2 limit is 0 within 1e-4.
"""
import math
import sys

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)


def jovera(lam, G):
    s = math.pi * lam / 4
    kap = math.sqrt(-lam**3 * math.cos(s) / (16 * math.sin(s) ** 3))
    e2a = math.sin(s) ** 2 / (1 - math.cos(s))
    eq = lam * math.sin(s) / (2 * (1 - math.cos(s)))
    p0 = 0.5 if MUT != "p0" else 1.0
    ex = (e2a * eq) if MUT != "exponent" else (e2a / eq)
    J = math.pi * kap / (16 * G)
    A = 2 * math.pi**2 * p0**1.5 * ex ** -0.5
    return J / A


G = 1 / (4 * math.pi) if MUT != "G1" else 1.0
cases = [  # (lambda, printed value, digits printed, where)
    (2.190024, 0.100628, 6, "EP, Eqs. (27)-(28)"),
    (2.059523, 0.05475, 5, "Fig. 1 caption"),
    (3.948341, 0.48717, 5, "Exceptional point section, paragraph 4"),
]
bad = 0
for lam, want, nd, where in cases:
    if MUT == "lam":
        lam += 0.001
    v = jovera(lam, G)
    ok = round(v, nd) == want
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'} lambda={lam}: computed {v:.8f}, printed {want} ({where})")
v4 = jovera(3.9999999, G)
v2 = jovera(2.0000001, G)
for name, v, want, tol in (("lambda->4", v4, 0.5, 1e-6), ("lambda->2", v2, 0.0, 1e-4)):
    ok = abs(v - want) < tol
    bad += not ok
    print(f"{'PASS' if ok else 'FAIL'} {name}: computed {v:.8f}, printed limit {want}")
ok = round(0.100628, 5) == 0.10063
bad += not ok
print(f"{'PASS' if ok else 'FAIL'} [DFKKR13]'s 0.10063 is 0.100628 rounded to five digits")
print(f"G used: {G:.8f} (= 1/(4 pi) unless mutated); failures: {bad}")
sys.exit(1 if bad else 0)
