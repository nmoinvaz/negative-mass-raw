#!/usr/bin/env python3
"""devsep.py [h]: development. For each TUNED line of logs/tune_*.log: the separation of the route point's r_th and rdot_th from family B's at the same gamma_1
(piecewise-linear and PCHIP interpolation over #266's B = 0 ... 0.125 at the same h)."""
import glob, json, os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i283/notes/wormhole_evolution"))
import settled_mass_route as r
from scipy.interpolate import PchipInterpolator
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.02
R = r.m.load266(h)
Bs = (0.0, 0.025, 0.05, 0.1, 0.125)
g1 = np.array([R[B]["mem"]["g1"] for B in Bs]); g1[0] = 0.0
rth = np.array([R[B]["mem"]["r_th"] for B in Bs]); sp = np.array([R[B]["speed"] for B in Bs])
print("family B at h", h, ": g1", np.round(g1, 5), "rth", np.round(rth, 5), "rdot", np.array2string(sp, precision=2))
pr, ps = PchipInterpolator(g1, rth), PchipInterpolator(g1, sp)
for f in sorted(glob.glob(os.path.dirname(os.path.abspath(__file__)) + "/logs/tune_*.log")):
    for ln in open(f):
        if ln.startswith("TUNED"):
            d = json.loads(ln[6:])
            if "g1" not in d:
                print("  ", d); continue
            x = d["g1"]
            dl = (d["rth"] - np.interp(x, g1, rth), d["rdot"] - np.interp(x, g1, sp))
            dp = (d["rth"] - float(pr(x)), d["rdot"] - float(ps(x)))
            print(f"  xc {d['xc']:g} w {d['w']:g} B {d['B']:.5g} g1 {x:.5f} rth {d['rth']:.5f} rdot {d['rdot']:+.2e} | d_rth lin {dl[0]:+.2e} pchip {dp[0]:+.2e} | d_rdot lin {dl[1]:+.2e} pchip {dp[1]:+.2e}")
