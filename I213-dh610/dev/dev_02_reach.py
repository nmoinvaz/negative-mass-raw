#!/usr/bin/env python3
"""dev_02: how far the symmetric expanding run goes. family S, one amplitude, store=False (diagonal series only). Prints the diagonal at
doublings of t, the last live diagonal cell, dead cells (not stored: events only) and timing."""
import math, sys, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn
n, h, X, A = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
N = int(round(X / h))
t0 = time.time()
d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=True)
res = dn.evolve(d, kernel="numba", store=False, excise=True, rexp=1e9)
dg = res.diag
ok = np.isfinite(dg["r"]); jl = np.where(ok)[0][-1]
print(f"D={n+2} h={h} X={X} N={N} A={A}: {time.time()-t0:.1f} s; last live diag j={jl} of {N-1} (t={dg['t'][jl]:.2f}); nan count {int((~ok).sum())}")
for tt in (10, 20, 40, 80, 120, 160, 200, 280):
    j = int(np.argmin(np.abs(dg["t"] - tt)))
    if j > jl or abs(dg["t"][j]-tt) > 0.5: continue
    print(f"  t={dg['t'][j]:7.2f} tau={dg['tau'][j]:8.4f} r={dg['r'][j]:10.3f} H={dg['H'][j]:8.4f} f={dg['f'][j]:7.3f} H*(tau_s-tau)?  r/t={dg['r'][j]/dg['t'][j]:.4f}")
