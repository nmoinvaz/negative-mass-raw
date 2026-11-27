#!/usr/bin/env python3
"""dev_01: family S (symmetric two-sided ghost pulse, phi-Gaussian xc = 3, w = 0.5, as #40) at D = 4, h = 0.02, X = 40.
For each amplitude: events, max e^-f, dead cells, mirror symmetry of the stored grid, the diagonal series (t, tau, r, H), and the
minimum-r slice (throat_min) against the diagonal. Reads only; nothing is gated."""
import math, sys, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn
SQ2 = math.sqrt(2.0)
n = int(sys.argv[1]) if len(sys.argv) > 1 else 2
h = float(sys.argv[2]) if len(sys.argv) > 2 else 0.02
X = float(sys.argv[3]) if len(sys.argv) > 3 else 40.0
amps = [float(a) for a in sys.argv[4].split(",")] if len(sys.argv) > 4 else [0.0, 0.01, 0.05, 0.2]
N = int(round(X / h))
for A in amps:
    t0 = time.time()
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=True)
    res = dn.evolve(d, kernel="numba", excise=True, rexp=1e9)
    G = res.G
    live = ~res.dead.astype(bool)
    emf = np.exp(-G[1])
    sym_r = np.max(np.abs(G[0] - G[0].T)); sym_f = np.max(np.abs(G[1] - G[1].T)); sym_p = np.max(np.abs(G[2] + G[2].T))
    dg = res.diag
    ok = np.isfinite(dg["r"]); jl = np.where(ok)[0][-1]
    print(f"D={n+2} h={h} X={X} A={A}: events {res.events or 'none'}; dead {int(res.dead.sum())}; max e^-f {np.nanmax(np.where(live, emf, np.nan)):.4f}; "
          f"mirror asym max |r-r^T| {sym_r:.1e}, |f-f^T| {sym_f:.1e}, |phi+phi^T| {sym_p:.1e}; last live diag j={jl} t={dg['t'][jl]:.2f}  ({time.time()-t0:.1f} s)")
    th = dn.throat_min(res)
    for tt in (4, 6, 8, 10, 12, 16, 20, 30, 40, 55):
        j = int(np.argmin(np.abs(dg["t"] - tt)))
        if j > jl or abs(dg["t"][j] - tt) > 0.5: continue
        k = int(np.argmin(np.abs(th[:, 0] - dg["t"][j]))) if len(th) else None
        s = f"  t={dg['t'][j]:6.2f} tau={dg['tau'][j]:7.3f} r_diag={dg['r'][j]:9.4f} H={dg['H'][j]:+8.4f} f={dg['f'][j]:+.3f}"
        if k is not None and abs(th[k, 0] - dg["t"][j]) < 0.1:
            s += f" | min-r slice: r={th[k,1]:9.4f} l={th[k,2]:+.4f}"
        print(s)
