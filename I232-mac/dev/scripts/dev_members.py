import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np, linear as L
W212 = {-0.3: 0.9700800261, -1.5: 0.4941711675, -1.01: 0.6331476235, -0.99: 0.6401216241, -1.0: None}
classes = {
 "R pulse": dict(R=(1e-3, 3.0, 0.5)),
 "L pulse": dict(L=(1e-3, 3.0, 0.5)),
 "H: a0=1e-3": dict(a0=1e-3),
 "H: a1L=1e-3": dict(a1L=1e-3),
 "H: a1R=1e-3": dict(a1R=1e-3),
}
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.01
for c in (-1.5, -1.01, -1.0, -0.99, -0.3):
    mem = L.ep.Member(c)
    print(f"== c = {c}: kappa = {mem.kappa:.5f}, W212 = {W212[c]}")
    for name, spec in classes.items():
        s = L.Setup(c, h, 14.0, spec)
        r = s.run(xs=(0.0,))
        t, y, yh = r["t"][0], r["Y"][0], r["Yh"]
        rates = [L.window_rate(t, y, a, a + 4) for a in (6, 10, 14)]
        ratesh = [L.window_rate(r["t"][0], yh, a, a + 4) for a in (6, 10, 14)]
        print(f"  {name:12s} wall {s.wall:5.2f}s  rate Y(x=0) [6,10] [10,14] [14,18]: " + " ".join(f"{x:8.5f}" for x in rates) + f"   |Y|(t=18): {abs(y[np.argmin(abs(t-18))]):.2e}   Yh(p): {yh[0]:.2e} {yh[len(yh)//2]:.2e} {yh[-1]:.2e}   Yh rates: " + " ".join(f"{x:8.5f}" for x in ratesh))
