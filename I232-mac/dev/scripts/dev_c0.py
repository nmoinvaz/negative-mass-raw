import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np, linear as L
W = math.sqrt(1.39705243433350684)
print("W(c=0) =", W)
for h in (0.02, 0.01, 0.005):
    s = L.Setup(0.0, h, 14.0, dict(R=(1e-3, 3.0, 0.5)))
    r = s.run(xs=(0.0, 1.0))
    for k, x in enumerate((0.0, 1.0)):
        t, y = r["t"][k], r["Y"][k]
        print(f"h={h} x={x} wall {s.wall:.2f}s", [f"{L.window_rate(t, y, a, a+4):.5f}" for a in (6, 8, 10, 12, 14, 16)], " W =", f"{W:.5f}")
