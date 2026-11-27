import sys, math
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, throat_locus as tl
SQ2 = math.sqrt(2)
for n, hs, tc in ((2, (0.04, 0.02, 0.01), 4.0), (3, (0.02, 0.01, 0.005), 2.7)):
    for kind, par in (("boost", 0.1), ("boost", 0.5), ("boost", -0.3), ("gauge", None)):
        errs = []
        for h in hs:
            smax = int((tc + 2)*SQ2/h)
            d = tl.scaled_rays(n, smax, h, tl.lam_of_v(par)) if kind == "boost" else tl.gauge_rays(n, smax, h)
            L = tl.sweep(d, smax=smax, stop=False); tl.locus_series(L)
            t = L["t"]; m = (t >= 0.8) & (t <= tc)
            ex = tl.boost_locus_exact(tl.lam_of_v(par), t) if kind == "boost" else tl.gauge_locus_exact(n, t)
            errs.append({k: float(np.max(np.abs(a[m] - b[m]))) for k, a, b in (("l", L["l"], ex["l"]), ("r", L["r"], np.ones_like(t)), ("f", L["f"], ex["f"]), ("tau", L["tau"], ex["tau"]), ("v", L["v"], ex["v"]))})
        print(f"n={n} {kind} {par}: " + "; ".join(f"{k} {errs[-1][k]:.1e} (ord {math.log2(errs[0][k]/errs[1][k]):.2f},{math.log2(errs[1][k]/errs[2][k]):.2f})" for k in errs[0]))
