import sys, math, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, throat_locus as tl
SQ2 = math.sqrt(2)
def run(kind, n, h, tmax, par):
    smax = int(tmax*SQ2/h)
    if kind == "boost":
        lam = tl.lam_of_v(par); d = tl.scaled_rays(n, smax, h, lam)
    else:
        d = tl.gauge_rays(n, smax, h)
    L = tl.sweep(d, smax=smax, stop=False); tl.locus_series(L)
    return L
for kind, par in (("boost", 0.1), ("boost", 0.5), ("boost", -0.3), ("gauge", None)):
    for n, hs in ((2, (0.04, 0.02, 0.01)), (3, (0.02, 0.01, 0.005))):
        errs = []
        for h in hs:
            L = run(kind, n, h, 6.0, par)
            t = L["t"]; m = (t >= 1.0) & (t <= (4.0 if n == 2 else 2.7))
            ex = tl.boost_locus_exact(tl.lam_of_v(par), t) if kind == "boost" else tl.gauge_locus_exact(n, t)
            e = dict(l=np.max(np.abs(L["l"][m]-ex["l"][m])), r=np.max(np.abs(L["r"][m]-1.0)), f=np.max(np.abs(L["f"][m]-ex["f"][m])),
                     tau=np.max(np.abs(L["tau"][m]-ex["tau"][m])), v=np.max(np.abs(L["v"][m]-ex["v"][m])))
            errs.append(e)
        print(f"{kind} {par} n={n}: h {hs}")
        for k in ("l", "r", "f", "tau", "v"):
            vals = [e[k] for e in errs]
            ords = [math.log2(vals[i]/vals[i+1]) if vals[i+1] > 0 else float('inf') for i in range(len(vals)-1)]
            print(f"   {k}: " + ", ".join(f"{x:.2e}" for x in vals) + "  orders " + ", ".join(f"{o:.2f}" for o in ords))
