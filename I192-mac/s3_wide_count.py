#!/usr/bin/env python3
"""s3_wide_count.py A B: the number of J-table steps under mutate=wide_table, for two binaries (JT4 of README A4).

Written before the run. For l = 2 over [5e-4, 34.7] (`jtable`'s defaults): the number of steps of each binary without and with `mutate=wide_table`, and the
number of the star's own steps that overlap the range (from `starsteps`). Declared: under `wide_table` both binaries have exactly the star's number of
steps (a table step as wide as a star step), and without it more (464). Exit 0 when that holds for both, 1 otherwise.
"""
import json
import os
import subprocess
import sys

HERE = "/Users/nathan/Source/negative-mass-i192/phase2/nonradial"
sys.path.insert(0, HERE)
import taylor_polar as tp  # noqa: E402


def run(b, cmd, mutate=None, **kw):
    args = [b, cmd] + [f"{k}={v}" for k, v in kw.items()] + ([f"mutate={mutate}"] if mutate else [])
    p = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True, cwd=HERE, env=dict(os.environ, RAYON_NUM_THREADS="2"))
    if p.returncode:
        raise RuntimeError(f"{' '.join(args)[:150]} exited {p.returncode}: {p.stderr[-300:]}")
    return [json.loads(x) for x in p.stdout.splitlines() if x.startswith("{")]


def main():
    a, b = sys.argv[1:3]
    s = run(a, "star", **tp.MODEL)[0]
    star = dict(tp.MODEL, pc=s["pc"], zc=s["zc"])
    rmin, rmax = 5e-4, 34.7
    ss = [r for r in run(a, "starsteps", **star) if r["cmd"] == "starstep"]
    nstar = sum(1 for r in ss if not (r["x1"] < rmin or r["x0"] > rmax))
    ok = True
    for name, bin_ in (("A", a), ("B", b)):
        plain = len(run(bin_, "jtable", l=2, rmin=rmin, rmax=rmax, **star)) - 1
        wide = len(run(bin_, "jtable", mutate="wide_table", l=2, rmin=rmin, rmax=rmax, **star)) - 1
        good = wide == nstar and plain > wide
        ok &= good
        print(f"{name} {bin_}: steps {plain} without wide_table, {wide} with it; the star's steps in the range: {nstar} -> {'ok' if good else 'FAIL'}", flush=True)
    print(f"SUMMARY: {'wide_table gives the star steps in both builds' if ok else 'FAIL'}")
    return 0 if ok else 1


sys.exit(main())
