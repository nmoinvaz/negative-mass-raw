#!/usr/bin/env python3
"""ind223: growing radial modes of #223's horizon members as negative eigenvalues of -d^2/dx*^2 + Vhat by finite
differences in the tortoise coordinate (criteria in README.md beside this file). Shares Vhat and A of bounce.py's Bg.

    python3 ind223.py [--mutate=vhat-scale|no-tortoise] [--wt=WORKTREE/notes/black_universe]
"""
import argparse
import math
import os
import sys
import time

import numpy as np
from scipy.integrate import solve_ivp
from scipy.linalg import eigh_tridiagonal

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["vhat-scale", "no-tortoise"])
ap.add_argument("--wt", default=os.path.expanduser("~/Source/negative-mass-r223/notes/black_universe"))
OPT = ap.parse_args()
MUT = OPT.mutate
sys.path.insert(0, OPT.wt)
sys.argv = [sys.argv[0]]
import bounce  # noqa: E402  (Vhat and A only)

L = 3000.0
HS = (0.1, 0.05)
# the README's real modes with W >= 0.005 (section 4 of the #223 note)
MEMBERS = {"S_m0.75": [0.22001], "S_m1": [0.177454], "S_m5": [0.0381208], "B1_q0": [0.282775], "B1_q0.5": [0.00665847, 0.286012]}
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def modes(mid, h):
    spec = bounce.member_spec(mid)
    bg = bounce.Bg(spec["fam"], spec["m"], spec["q"], res="R2", at_throat=spec["at_throat"])
    xh = bg.xh
    x0 = xh + 1.0
    n = int(round(L / h))
    xs = np.arange(-n, n + 1) * h
    if MUT == "no-tortoise":
        x = np.maximum(x0 + xs, xh + 1e-300)
        x = x[x > xh + 1e-12]
        xs = xs[-len(x):]
    else:
        f = lambda s, y: [max(float(bg.A(y[0])), 0.0)]  # noqa: E731
        up = solve_ivp(f, [0, L], [x0], method="DOP853", rtol=1e-12, atol=1e-300, t_eval=xs[xs >= 0], dense_output=False)
        dn = solve_ivp(f, [0, -L], [x0], method="DOP853", rtol=1e-12, atol=1e-300, t_eval=xs[xs <= 0][::-1])
        x = np.concatenate([dn.y[0][::-1][:-1], up.y[0]])
    V = np.zeros_like(x)
    for i, xi in enumerate(x):
        Ai = float(bg.A(xi)) if xi > xh else 0.0
        V[i] = float(bg.Vhat(xi)) if Ai > 1e-300 else 0.0
    if MUT == "vhat-scale":
        V *= 1.05
    d = 2.0 / h ** 2 + V[1:-1]
    e = -np.ones(len(d) - 1) / h ** 2
    w = eigh_tridiagonal(d, e, select="v", select_range=(-1e3, -1e-6), eigvals_only=True)
    return sorted(math.sqrt(-l) for l in w if l < 0)


t0 = time.time()
ok, notes = True, []
for mid, ref in MEMBERS.items():
    got = {h: modes(mid, h) for h in HS}
    big = {h: [W for W in got[h] if W >= 0.005] for h in HS}
    okm = len(big[0.05]) == len(ref) and len(big[0.1]) == len(ref)
    if okm:
        okm &= all(abs(a / b - 1) <= 2e-3 for a, b in zip(big[0.05], ref))
        okm &= all(abs(a / b - 1) <= 2e-3 for a, b in zip(big[0.1], big[0.05]))
    ok &= okm
    rel = ", ".join(f"{a:.6f} ({a / b - 1:+.1e})" for a, b in zip(big[0.05], ref)) if len(big[0.05]) == len(ref) else "count differs"
    notes.append(f"{mid}: W >= 1e-3 at h = 0.05: {[round(W, 6) for W in got[0.05] if W >= 1e-3]}, at 0.1: "
                 f"{[round(W, 6) for W in got[0.1] if W >= 1e-3]}; against {ref}: {rel}")
    print(f"  {notes[-1]} ({time.time() - t0:.0f} s)", flush=True)
check("K1", ok, "; ".join(notes))
bad = [nm for nm, o in RESULTS if not o]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
