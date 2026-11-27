import sys, math, time
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/wormhole_evolution")
import numpy as np, linear as L
import dev_nl_lib as D
from scipy.interpolate import CubicSpline
W = math.sqrt(1.39705243433350684)
for h in (0.02, 0.01, 0.005):
    su = L.Setup(0.0, h, 14.0, dict(R=(1e-6, 3.0, 0.5)))
    r = su.run(xs=(0.0,))
    tl, yl = r["t"][0], r["Y"][0]
    tn, yn, ye = D.nl_response(su)
    ok = np.isfinite(yl)
    sp = CubicSpline(tl[ok], yl[ok])
    print(f"h={h}")
    for (a, b) in ((4, 8), (6, 10), (8, 12), (10, 14), (12, 16)):
        rl = L.window_rate(tl, yl, a, b)
        rn = L.window_rate(tn, yn, a, b)
        print(f"   window [{a},{b}]: linear {rl:.6f}  nonlinear odd {rn:.6f}  diff {rn-rl:+.2e}  W={W:.6f}   W^2: lin {rl*rl:.6f} nl {rn*rn:.6f}")
    for tt in (6, 10, 14):
        i = np.argmin(abs(tn - tt))
        print(f"   t={tn[i]:.2f} ratio nl/lin = {yn[i]/sp(tn[i]):.6f}  even drift {ye[i]:.2e}")
