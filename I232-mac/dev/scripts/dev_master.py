import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np, linear as L
classes = {
 "R pulse": dict(R=(1e-3, 3.0, 0.5)),
 "L pulse": dict(L=(1e-3, 3.0, 0.5)),
 "H: a0=1e-3": dict(a0=1e-3),
 "H: a1R=1e-3": dict(a1R=1e-3),
}
h = 0.01
for c in (-1.5, -1.01, -1.0):
    print("== c =", c)
    for name, spec in classes.items():
        s = L.Setup(c, h, 14.0, spec)
        r = s.run(xs=(0.0,))
        t, y = r["t"][0], r["Y"][0]
        t1, y1 = L.master_from_setup(s)
        m = np.isfinite(y) & (t > 2)
        ratio = y1[m] / y[m]
        rr = [L.window_rate(t1, y1, a, a + 4) for a in (6, 10, 14)]
        rd = [L.window_rate(t, y, a, a + 4) for a in (6, 10, 14)]
        idx = [np.argmin(abs(t - tt)) for tt in (4, 8, 12, 16, 19)]
        print(f"  {name:12s} ratio Y_1D/Y_DN at t=4,8,12,16,19: " + " ".join(f"{y1[i]/y[i]:9.4f}" for i in idx) + "   rates 1D: " + " ".join(f"{x:8.5f}" for x in rr) + "  DN: " + " ".join(f"{x:8.5f}" for x in rd))
