#!/usr/bin/env python3
"""dev_14 (after the runs of record, a consistency check of a relation derived by hand, not a declared check): on the diagonal
dH/dtau = -(n+1) H^2/2 - (n-1)/(2 r^2) - rho/n, from m = r^(n-1)(1 + rdot^2)/2 and dm/dtau = -(r^n/n) rho rdot (the ray identity at the diagonal).
Compared on the stored series with a centred difference of H in tau."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i213/notes/wormhole_evolution"))
import expansion as ex
RAW = os.path.expanduser("~/Source/negative-mass-raw/I213-dh610/runs")
for f in sorted(os.listdir(RAW)):
    if not (f.startswith("D") and f.endswith(".npz")):
        continue
    R = ex.load_run(os.path.join(RAW, f)); n, h = R["n"], R["h"]
    g = ex.diag_arrays(R)
    tau, r, H, rho = g["tau"], g["r"], g["H"], g["rho"]
    Hdot = np.gradient(H, tau)
    rhs = -(n + 1) * H ** 2 / 2 - (n - 1) / (2 * r ** 2) - rho / n
    for lab, m in (("r/a in [1.5, 10]", (r > 1.5) & (r < 10)), ("r/a in [10, 100]", (r > 10) & (r < 100)), ("r/a > 100", r > 100)):
        if m.sum() > 5:
            rel = np.abs(Hdot[m] - rhs[m]) / np.abs(rhs[m])
            print(f"{f:34s} {lab:18s} max |Hdot - rhs|/|rhs| = {rel.max():.2e}  (median {np.median(rel):.2e})")
