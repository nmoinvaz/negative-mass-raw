import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np, linear as L
c = -1.0
mem = L.ep.Member(c); b = mem.kappa*math.sqrt(2)
for h in (0.02, 0.01, 0.005):
    out = []
    for s0 in (2.5, 3.5, 4.5):
        su = L.Setup(c, h, 16.0, dict(L=(1e-3, s0, 0.5)))
        r = su.run(xs=(0.0,))
        p, yh = r["p"], r["Yh"]
        m = p >= 1.0
        Mx = np.vstack([np.ones(m.sum()), np.exp(b * p[m])]).T
        co = np.linalg.lstsq(Mx / np.abs(yh[m])[:, None], yh[m] / np.abs(yh[m]), rcond=None)[0]
        res = np.max(np.abs(Mx @ co - yh[m]) / np.abs(yh[m]))
        # free exponent fit: ln|Yh| slope
        slope = np.polyfit(p[(p > 8)], np.log(np.abs(yh[p > 8])), 1)[0]
        out.append((res, slope))
    print(f"h={h}: residual {[f'{x[0]:.2e}' for x in out]}, late slope of ln|Y_h| {[f'{x[1]:.6f}' for x in out]} (b = {b:.6f})")
