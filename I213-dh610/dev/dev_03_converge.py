#!/usr/bin/env python3
"""dev_03: resolution agreement of the diagonal series of the symmetric expanding run, family S, D = 4 or 5, store=False.
Runs h, h/2, h/4 on a rectangle of the same X, interpolates tau, r, H onto common t and prints the relative differences at doublings of t."""
import math, sys, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn
n, A, X = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
hs = [float(x) for x in sys.argv[4].split(",")]
out = []
for h in hs:
    N = int(round(X / h)); t0 = time.time()
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=True)
    res = dn.evolve(d, kernel="numba", store=False, excise=True, rexp=1e9)
    dg = res.diag; ok = np.isfinite(dg["r"])
    print(f"D={n+2} h={h} N={N} A={A}: {time.time()-t0:.1f} s, live diag cells {int(ok.sum())} of {N}", flush=True)
    out.append((h, dg))
ts = [10, 20, 40, 80, 120, 160, 200, 280]
print("   t     " + "  ".join(f"[{hs[k]} vs {hs[k+1]}] dr/r      dH/H      dtau" for k in range(len(hs) - 1)))
for t in ts:
    row = []
    for k in range(len(hs) - 1):
        a, b = out[k][1], out[k + 1][1]
        if t > min(a["t"][np.isfinite(a["r"])][-1], b["t"][np.isfinite(b["r"])][-1]): row.append("   (beyond)"); continue
        va = {q: np.interp(t, a["t"], a[q]) for q in ("r", "H", "tau")}
        vb = {q: np.interp(t, b["t"], b[q]) for q in ("r", "H", "tau")}
        row.append(f"{va['r']/vb['r']-1:+.2e}  {va['H']/vb['H']-1:+.2e}  {va['tau']-vb['tau']:+.2e}")
    print(f"  {t:4d}   " + "   ".join(row))
