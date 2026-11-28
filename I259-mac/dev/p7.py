"""P7: c1 as a functional of the slice data on #232's own linear solutions (c = -1): c1 = dr(p0, horizon) - e^{b p0} c2_slice(p0), against the horizon fit.
Classes A0, A1R, A1L (corner constants), L, R pulses; h = 0.01, 0.005, 0.0025, P = 7."""
import os, sys, math, time
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
_argv = sys.argv; sys.argv = sys.argv[:1]
import numpy as np
import horizon_sector as hs
import linear as lin
sys.argv = _argv

b = lin.ep.Member(-1.0).kappa * math.sqrt(2.0)
P = 7.0
SPEC = {"A0": dict(a0=1e-3), "A1R": dict(a1R=1e-3), "A1L": dict(a1L=1e-3), "L": dict(L=(1e-3, 3.5, 0.5)), "R": dict(R=(1e-3, 3.5, 0.5))}
names = sys.argv[1:] or list(SPEC)
for name in names:
    rows = {}
    for h in (0.01, 0.005, 0.0025):
        t0 = time.time()
        su = lin.mksetup(-1.0, h, P, SPEC[name])
        U = lin.march_full(su.UL, su.UR, su.chart.par, su.chart.tab, su.hp, su.hs)
        ih = su.jh
        p = h * np.arange(su.Np + 1)
        c1, c2, res = hs.horizon_fit(U[0, :, ih], np.exp(b * p))
        sl = {}
        for pj in (0.5, 1.0, 2.0, 4.0, 6.0):
            j = int(round(pj / h))
            V0 = math.exp(b * pj)
            c2s = hs.slice_V_derivative(U[0], j, ih, h) / (b * V0)
            sl[pj] = (U[0][j, ih] - V0 * c2s, c2s)
        rows[h] = (c1, c2, sl)
        print(f"{name} h={h} wall {time.time()-t0:.1f}s mem {U.nbytes/1e6:.0f}MB c1fit={c1: .6e} c2fit={c2: .6e}", flush=True)
        del U, su
    r = lambda a, bb: (4 * bb - a) / 3
    c1f = r(rows[0.005][0], rows[0.0025][0])
    c2f = r(rows[0.005][1], rows[0.0025][1])
    print(f"== {name}: Richardson(0.005, 0.0025): c1 fit {c1f: .9e}, c2 fit {c2f: .9e}")
    for pj in (0.5, 1.0, 2.0, 4.0, 6.0):
        c1s = r(rows[0.005][2][pj][0], rows[0.0025][2][pj][0])
        c2s = r(rows[0.005][2][pj][1], rows[0.0025][2][pj][1])
        V0 = math.exp(b * pj)
        print(f"   p0={pj}: V0={V0:8.2f}  c1 slice {c1s: .9e}  dev {c1s-c1f: .2e}  rel to |c1| {abs(c1s-c1f)/max(abs(c1f),1e-300): .1e}  (V0 |c2| = {V0*abs(c2f): .2e}; dev/(V0 |c2|) = {abs(c1s-c1f)/(V0*abs(c2f)+1e-300): .1e});  c2 slice rel dev {abs(c2s-c2f)/max(abs(c2f),1e-300): .1e}")
