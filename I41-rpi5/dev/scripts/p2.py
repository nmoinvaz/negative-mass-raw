import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import settled_mass as sm
Nc = int(sys.argv[1])
hs = [float(x) for x in sys.argv[2:]]
E = []
for h in hs:
    out, e = sm.roberts_planted(h, Nc)
    s = out["ser"]
    print("h", h, out["status"], "cols", len(s["r"]), "levels", [int((s["level"] == k).sum()) for k in range(3)], "max e_r %.3e e_m %.3e e_M %.3e" % (e["e_r"].max(), e["e_m"].max(), e["e_M"].max()), "edge min %.0f" % s["edge"].min())
    E.append((e["e_r"].max(), e["e_m"].max()))
for i in range(len(hs) - 1):
    print("ratio e_r %.2f e_m %.2f" % (E[i][0] / E[i + 1][0], E[i][1] / E[i + 1][1]))
