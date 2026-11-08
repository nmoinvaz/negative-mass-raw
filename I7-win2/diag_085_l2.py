"""Diagnostic for the crashed scan_085_l2 of issue 7: D(g) on the scan's grid, one serial process.

Builds the star and PolarProblem as scan_growing.py's init() does (eps = -1, w = 0.85, l = 2, same RTOL and PHICUT
defaults) and evaluates D on logspace(1e-3, 300, 100). Before each point it prints and flushes g, after it appends
{"g": ..., "D": ...} to diag_085_l2.jsonl. faulthandler writes to the log. It records D only, no brentq, no CSV.

    python diag_085_l2.py              all 100 points
    python diag_085_l2.py --index 37   only grid[37], appended to diag_085_l2_index37.jsonl
"""
import faulthandler
import json
import os
import sys
import time

import numpy as np

RAW = os.path.dirname(os.path.abspath(__file__))
NR = r"C:\Users\nathan\Source\negative-mass-i7\phase2\nonradial"
sys.path.insert(0, NR)

only = int(sys.argv[sys.argv.index("--index") + 1]) if "--index" in sys.argv else None
stem = "diag_085_l2" + (f"_index{only}" if only is not None else "")
log = open(os.path.join(RAW, stem + ".log"), "a", buffering=1)
sys.stdout = sys.stderr = log
faulthandler.enable(file=log, all_threads=True)

import background as B  # noqa: E402
from polar_solver import PolarProblem  # noqa: E402

eps, w, l = -1, 0.85, 2
npts, gmin, gmax = 100, float("1e-3"), 300.0
rtol = float(os.environ.get("RTOL", "1e-10"))
phi_cut = float(os.environ.get("PHICUT", "1e-9"))

print(f"=== {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())} {stem} pid {os.getpid()} rtol={rtol} phi_cut={phi_cut}",
      flush=True)
st = B.solve_star(w, eps)
P = PolarProblem(st, l, rtol=rtol, phi_cut=phi_cut)
grid = np.logspace(np.log10(gmin), np.log10(gmax), npts)
idx = range(npts) if only is None else [only]
T0 = time.time()
with open(os.path.join(RAW, stem + ".jsonl"), "a") as out:
    for i in idx:
        g = float(grid[i])
        print(f"i={i} g={g!r}", flush=True)
        D = float(P.D(g))
        out.write(json.dumps({"i": i, "g": g, "D": D}) + "\n")
        out.flush()
        print(f"   D={D!r} ({time.time() - T0:.0f}s)", flush=True)
print(f"=== {time.strftime('%Y-%m-%d %H:%M:%SZ', time.gmtime())} {stem} done, {len(idx)} points", flush=True)
