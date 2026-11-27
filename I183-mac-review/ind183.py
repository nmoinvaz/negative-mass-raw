#!/usr/bin/env python3
"""ind183: four off-grid points of #183 integrated independently by scipy (criteria in README.md beside this file).

    python3 ind183.py [--mutate=NAME] [--wt=WORKTREE]
"""
import argparse
import json
import os
import subprocess
import sys
from fractions import Fraction

import mpmath as mp
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["k1-c", "k2-drift"])
ap.add_argument("--wt", default="/Users/nathan/Source/negative-mass-r183")
A = ap.parse_args()
MUT = A.mutate
WARP = os.path.join(A.wt, "notes", "warp")
sys.path.insert(0, WARP)
import det_classify as dc  # noqa: E402
import conical_global as cg  # noqa: E402

BIN = os.path.join(WARP, "conical_global", "target", "release", "offgrid")
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


# N and its derivatives
N = dc.conical_N()
syms = (dc.ETA, dc.F0_, dc.F1_, dc.F2_)
Nf = sp.lambdify(syms, N, "numpy")
dN = [sp.lambdify(syms, sp.diff(N, v), "numpy") for v in syms]
terms = [sp.lambdify(syms, t, "numpy") for t in sp.Add.make_args(sp.expand(N))]


def rhs(eta, y):
    F, F1, F2 = y
    a = (eta, F, F1, F2)
    F3 = -(dN[0](*a) + dN[1](*a) * F1 + dN[2](*a) * F2) / dN[3](*a)
    return [F1, F2, F3]


def crate_verdict(fi, c):
    r = subprocess.run(["nice", "-n", "10", BIN, "scan", "--prec", "dd", "--mode", "conserve", "--fi", repr(fi),
                        "--c", repr(c)], capture_output=True, text=True, env=dict(os.environ, RAYON_NUM_THREADS="2"))
    if r.returncode:
        raise RuntimeError(r.stderr[-300:])
    return [json.loads(ln) for ln in r.stdout.splitlines() if ln.startswith("{")][0]


CANDS = [(0.05, 100), (0.2, -30), (8, 300), (24, -1000), (0.01, 3), (6, -100), (0.1, 1000), (12, 30)]
chosen = []
for fi, c in CANDS:
    v = crate_verdict(float(fi), float(c))
    if v["l"] <= 800:
        chosen.append((fi, c, v))
    if len(chosen) == 4:
        break

ok1, ok2, notes1, notes2 = True, True, [], []
for fi, c, v in chosen:
    L = v["l"]
    cc = Fraction(c) * (Fraction(1001, 1000) if MUT == "k1-c" else 1)
    F, F1, F2 = [float(x) for x in cg.series_mp(Fraction(fi), cc, mp.mpf(L), 1)]
    stop_f = lambda eta, y: abs(y[1]) - 1e8  # noqa: E731
    stop_f.terminal = True
    sol = solve_ivp(rhs, (L, 1e-6), [F, F1, F2], method="DOP853", rtol=1e-12, atol=1e-14, events=[stop_f])
    eta_end = sol.t[-1]
    Fe, F1e, F2e = sol.y[:, -1]
    if abs(eta_end - 1e-6) <= 1e-12:
        kind = "FLOOR"
    elif abs(Fe) < 1e-3 * abs(fi) or abs(F1e) >= 1e8 * (1 - 1e-12):
        kind = "F->0"
    elif abs(Fe**2 - eta_end**2 - 1) < 1e-3:
        kind = "a3->0"
    else:
        kind = f"other ({sol.message})"
    ck = v["kind"] if v["class"] == "SINGULAR" else v["class"]
    if v["class"] == "SINGULAR":
        xs = v["xstar"]
        good = kind == ck and abs(eta_end - xs) <= 1e-4 * max(1.0, abs(xs))
        notes1.append(f"({fi}, {c}) L={L:g}: crate {ck} at {xs:.10g}, scipy {kind} at {eta_end:.10g} "
                      f"(diff {abs(eta_end - xs):.2e}, {len(sol.t)} steps)")
    else:
        good = kind == ck == "FLOOR" and np.sign(eta_end * F1e) * np.sign(fi) > 0
        notes1.append(f"({fi}, {c}) L={L:g}: crate {ck}, scipy {kind}, p = eta F' = {eta_end * F1e:.4g}")
    ok1 &= good
    a = (eta_end, Fe, F1e, F2e * (1 + 1e-6 if MUT == "k2-drift" else 1))
    rel = abs(Nf(*a)) / sum(abs(t(*a)) for t in terms)
    ok2 &= rel <= 1e-8
    notes2.append(f"({fi}, {c}): |N|/sum {rel:.1e}")
check("K1", ok1 and len(chosen) == 4, "; ".join(notes1))
check("K2", ok2, "; ".join(notes2))
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
