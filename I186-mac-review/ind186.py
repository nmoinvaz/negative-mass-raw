#!/usr/bin/env python3
"""ind186: the coordinator's out-of-sample comparison of #186's crate with scipy (criteria in README.md beside this file).

    python3 ind186.py --wt=<worktree at f4edcb1> [--mutate=NAME]
"""
import argparse
import os
import sys
import time

ap = argparse.ArgumentParser()
ap.add_argument("--wt", required=True)
ap.add_argument("--mutate", default=None, choices=["wrong-l", "f64-claim"])
a = ap.parse_args()
MUT = a.mutate
NR = os.path.join(a.wt, "phase2", "nonradial")
sys.path.insert(0, NR)
os.chdir(NR)
_argv, sys.argv = sys.argv, [sys.argv[0]]
import background as B              # noqa: E402
from polar_solver import PolarProblem  # noqa: E402
import taylor_polar as TP           # noqa: E402
sys.argv = _argv

RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


POINTS = [(2, 50.0), (3, 10.0), (4, 300.0)]
t0 = time.time()
star = B.solve_star(0.7603, -1)
print(f"[info] star solved by scipy in {time.time() - t0:.1f} s; load {os.getloadavg()}", flush=True)
rows = []
for l, g in POINTS:
    pp = PolarProblem(star, l)
    t1 = time.time()
    ds = pp.D(g)
    ts = time.time() - t1
    lc = l + 1 if MUT == "wrong-l" else l
    t1 = time.time()
    _, dd = TP.d_values(lc, [g], lane="dd")
    tdd = time.time() - t1
    t1 = time.time()
    _, df = TP.d_values(lc, [g], lane="f64")
    tf = time.time() - t1
    Ddd, Df = float(dd[g]["d"]), float(df[g]["d"])
    rows.append((l, g, ds, Ddd, Df, ts, tdd, tf, pp.rm))
    print(f"[info] l = {l}, gamma = {g}: scipy D = {ds:.10e} ({ts:.1f} s, r_m = {pp.rm:.6f}); crate dd {Ddd:.10e} "
          f"({tdd:.1f} s), f64 {Df:.10e} ({tf:.1f} s)", flush=True)

r1 = all(abs(Ddd / ds - 1) <= 1e-7 and (Ddd > 0) == (ds > 0) for (_, _, ds, Ddd, _, *_) in rows)
check("R1", r1, "; ".join(f"({l}, {g}): |dd/scipy - 1| = {abs(Ddd / ds - 1):.2e}" for (l, g, ds, Ddd, *_) in rows))
bar = 1e-15 if MUT == "f64-claim" else 1e-6
r2 = all(abs(Df / Ddd - 1) <= bar for (_, _, _, Ddd, Df, *_) in rows)
check("R2", r2, f"bar {bar}: " + "; ".join(f"({l}, {g}): |f64/dd - 1| = {abs(Df / Ddd - 1):.2e}" for (l, g, _, Ddd, Df, *_) in rows))
print("[info] R3 timing (s): " + "; ".join(f"({l}, {g}): scipy {ts:.1f}, dd {tdd:.1f}, f64 {tf:.1f}"
                                          for (l, g, _, _, _, ts, tdd, tf, _) in rows) + f"; load {os.getloadavg()}", flush=True)
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - t0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
