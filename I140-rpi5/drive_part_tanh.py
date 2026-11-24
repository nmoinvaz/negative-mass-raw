#!/usr/bin/env python3
"""#140: run tanh_spectrum.py's part_tanh, the code the window helper was wired into, on the stored arrays instead of a solve.

No spectrum is computed. ts.sector_task is replaced by a function that returns the stored eigenvalues of a sector in the shape
solve_sector gives them (one block of mu; one stand-in diag entry, so the diagnostics print), and ts.ProcessPoolExecutor by a
serial stand-in. part_tanh then prints its sector table and window table. This script parses those two tables and compares, for
the 22 sectors of sigma R = 8 and 16, the window counts of A and B, the cut and the symmetry value with retab.py's csv.

    drive_part_tanh.py [--ts=DIR] [--csv=retab_rpi5.csv] [--mutate=abscut]

Exit 1 if any value differs. With --mutate=abscut part_tanh must print A windows 2 below the csv in the six sectors where
np.abs(array) < abs(scalar) at the cut, and the comparison must fail there."""
import argparse
import contextlib
import csv
import io
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--ts", default=os.path.expanduser("~/Source/negative-mass-i140/notes/warp"))
ap.add_argument("--csv", default=os.path.join(HERE, "retab_rpi5.csv"))
ap.add_argument("--mutate", default="", choices=["", "abscut"])
args = ap.parse_args()
sys.path.insert(0, args.ts)
import tanh_spectrum as ts  # noqa: E402

RUNS = {8: "I96-win", 16: "I96-dh610"}
ts.MUT = args.mutate


def fake_sector(t):
    d = np.load(os.path.join(RAW, RUNS[int(t["sig"])], "eig", f"tanh_sigma{t['sig']:g}_m{t['m']:g}.npz"))
    dg = {"k": 0, "qrel": 0.0, "res": 0.0, "clus": 1, "grel": 0.0, "real": False}
    return t["sig"], t["m"], {"A": [{"mu": d["muA"], "chs": [], "diag": [dg]}], "B": [{"mu": d["muB"], "chs": [], "diag": []}]}, 0.0, 0.0


class Serial:
    def __init__(self, **kw):
        pass

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def map(self, fn, it):
        return map(fn, it)


ts.sector_task, ts.ProcessPoolExecutor = fake_sector, Serial
cfg = dict(ts.FULL)
cfg["p"] = {8.0: 200, 16.0: 340}
want = {(int(r["sigma"]), float(r["m"])): r for r in csv.DictReader(open(args.csv))}
bad, n = [], 0
for sig in RUNS:
    ns = argparse.Namespace(sigmas=str(sig), ms=None, procs=1, raw="")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        ts.part_tanh(cfg, ns)
    out = buf.getvalue()
    sec = {}
    for ln in out.splitlines():
        m = re.match(r"\s+([\d.]+) \| (\S+ \S+ \S+ \S+) \| ([\d.]+) / ([\d.]+) \| +([\d.]+) \| ([\d.e+-]+)$", ln)
        if m:
            sec[float(m.group(1))] = (m.group(5), m.group(6))
    win = {}
    for ln in out.splitlines():
        m = re.match(r"\s+(\d+) \| +([\d.]+) \| +([\d.]+) \| +(\d+) / +(\d+) \| (\d+) / (\d+) \|", ln)
        if m:
            win[float(m.group(2))] = (m.group(3), int(m.group(4)), int(m.group(5)))
    for m_ in (0.5 + k for k in range(11)):
        w = want[(sig, m_)]
        got = dict(cut=sec[m_][0], sym=sec[m_][1], lo=win[m_][0], nwA=win[m_][1], nwB=win[m_][2])
        exp = dict(cut=w["cut4"], sym=w["sym2"], lo=w["cut4"], nwA=int(w["nwA"]), nwB=int(w["nwB"]))
        n += 1
        d = {k: (got[k], exp[k]) for k in exp if str(got[k]) != str(exp[k])}
        if d:
            bad.append(f"sigma R = {sig}, m = {m_:g}: " + ", ".join(f"{k} part_tanh {a} csv {b}" for k, (a, b) in d.items()))
        print(f"  sigma R = {sig:2d}, m = {m_:4.1f}: part_tanh cut {got['cut']}, window A / B {got['nwA']} / {got['nwB']}, "
              f"symmetry {got['sym']}; csv {exp['nwA']} / {exp['nwB']}, {exp['sym']}" + ("   DIFFERS" if d else ""))
    print(f"  (part_tanh's own failed checks at sigma R = {sig}: {ts.FAILED or 'none'})")
print(f"{n} sectors compared, {len(bad)} differ" + ("" if not bad else ": " + "; ".join(bad)))
if bad:
    print("FAILED: part_tanh's window columns differ from retab.py's")
    sys.exit(1)
print("all checks passed")
