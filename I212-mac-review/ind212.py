#!/usr/bin/env python3
"""ind212: an independent count of the growing radial modes of the black universes without a throat in the static region,
by finite differences in the tortoise coordinate (criteria in README.md beside this file).

    python3 ind212.py [--mutate=wrong-V|wrong-m|short-X] [--raw=I212-rpi5 results dir]
"""
import argparse
import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import brentq

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["wrong-V", "wrong-m", "short-X"])
ap.add_argument("--raw", default="/Users/nathan/Source/negative-mass-raw/I212-rpi5/results")
OPT = ap.parse_args()
MUT = OPT.mutate
X = 20.0 if MUT == "short-X" else 400.0
MEMBERS = [-10, -3, -2, -1.5, -1.1, -1.01, -1.001, -1.0001, -1.0]
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


# background (b = 1): A = R^2 [c + 1/R^2 + 3m (rho/R^2 + atan rho)], 3m = -2c/pi (asymptotic flatness)
rho, c_, m3 = sp.symbols("rho c m3", real=True)
R2 = rho**2 + 1
Asym = R2 * (c_ + 1 / R2 + m3 * (rho / R2 + sp.atan(rho)))
A_f = sp.lambdify((rho, c_, m3), Asym, "math")
A1_f = sp.lambdify((rho, c_, m3), sp.diff(Asym, rho), "math")
A2_f = sp.lambdify((rho, c_, m3), sp.diff(Asym, rho, 2), "math")


def m3_of(c):
    return (-c / math.pi) if MUT == "wrong-m" else (-2 * c / math.pi)


def horizon(c):
    m3 = m3_of(c)
    B = lambda r: A_f(r, c, m3) / (r * r + 1)  # noqa: E731
    grid = np.linspace(-60, 60, 24001)
    vals = [B(r) for r in grid]
    roots = [brentq(B, grid[i], grid[i + 1], xtol=1e-15, rtol=1e-15) for i in range(len(grid) - 1)
             if vals[i] == 0 or vals[i] * vals[i + 1] < 0]
    if not roots:                                     # no horizon (A1): reported as a failure, not a crash
        return float("nan"), float("nan")
    rh = max(roots)
    return rh, A1_f(rh, c, m3) / 2


def operator(c, h):
    """the tridiagonal FD matrix of -d^2/dx^2 + V on x in (-X, X), Dirichlet ends; rho = rh + e^z, dz/dx = A/e^z"""
    m3 = m3_of(c)
    rh, kap = horizon(c)
    a1, a2 = A1_f(rh, c, m3), A2_f(rh, c, m3)

    def A_of(d):  # A and A' at rho = rh + d, Taylor near the horizon
        if d < 1e-6:
            return a1 * d + 0.5 * a2 * d * d, a1 + a2 * d
        r = rh + d
        return A_f(r, c, m3), A1_f(r, c, m3)

    def dzdx(_x, z):
        d = math.exp(z[0])
        return [(a1 + 0.5 * a2 * d) if d < 1e-6 else A_f(rh + d, c, m3) / d]

    n = int(round(2 * X / h)) - 1
    xs = -X + h * np.arange(1, n + 1)
    z0 = 0.0                                           # x = 0 at rho = rh + 1
    up = solve_ivp(dzdx, (0, X), [z0], method="DOP853", rtol=1e-13, atol=1e-14, dense_output=True)
    dn = solve_ivp(dzdx, (0, -X), [z0], method="DOP853", rtol=1e-13, atol=1e-14, dense_output=True)
    V = np.empty(n)
    for i, x in enumerate(xs):
        z = (up if x >= 0 else dn).sol(x)[0]
        d = math.exp(z)
        A, Ap = A_of(d)
        r = rh + d
        R4 = (r * r + 1) ** 2
        # V = 2A^2/rho^2 - (1 + 1/R^2) A A'/rho + A^2/R^4 - 2A/R^2 (#212's note, section 2)
        Ar = A / r
        V[i] = (2 * Ar * Ar - (1 + 1 / (r * r + 1)) * Ar * Ap + (2 if MUT == "wrong-V" else 1) * A * A / R4
                - 2 * A / (r * r + 1))
    return 2 / h**2 + V, -np.ones(n - 1) / h**2, rh, kap


def lowest(c, h):
    d, e, _, _ = operator(c, h)
    return eigh_tridiagonal(d, e, select="i", select_range=(0, 1), eigvals_only=True)


def theirs(c):
    with open(os.path.join(OPT.raw, f"member_{float(c)!r}_R2.json".replace("-10.0", "-10").replace("-3.0", "-3")
                           .replace("-2.0", "-2"))) as f:
        return json.load(f)


ok1, ok2, n1, n2, W = True, True, [], [], {}
for c in MEMBERS:
    t = theirs(c)
    rh, kap = horizon(c)
    d1 = max(abs(rh - t["rh"]), abs(kap - t["kappa"]))
    ok1 &= d1 <= 1e-6
    n1.append(f"c={c:g} rh {rh:.9f} kappa {kap:.9f} (|diff| {d1:.1e})")
    if math.isnan(rh):
        ok2 = False
        n2.append(f"c={c:g}: no horizon, no operator")
        continue
    l1, l2 = lowest(c, 0.02), lowest(c, 0.01)
    nneg = [int(np.sum(l < -1e-6)) for l in (l1, l2)]
    if t["n_roots"] == 1:
        lam = (4 * l2[0] - l1[0]) / 3
        Wm = math.sqrt(-lam) if lam < 0 else float("nan")
        Wt = t["roots"][0] if not isinstance(t["roots"][0], dict) else t["roots"][0].get("W")
        good = nneg == [1, 1] and abs(Wm - Wt) / Wt <= 1e-5
        W[c] = (Wm, kap)
        n2.append(f"c={c:g}: negative eigenvalues {nneg}, W {Wm:.10f} vs #212 {Wt:.10f} (rel {abs(Wm - Wt) / Wt:.1e})")
    else:
        good = nneg == [0, 0]
        n2.append(f"c={c:g}: negative eigenvalues {nneg}, lowest {l1[0]:.3e}, {l2[0]:.3e} (#212: none)")
    ok2 &= good
check("K1", ok1, "; ".join(n1))
check("K2", ok2, "; ".join(n2))
Wk = W.get(-1.0001)
ok3 = Wk is not None and abs(Wk[0] / Wk[1] - 1) <= 1e-3
check("K3", ok3, f"c = -1.0001: W/kappa = {Wk[0] / Wk[1]:.6f}" if Wk else "c = -1.0001 has no mode here")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
