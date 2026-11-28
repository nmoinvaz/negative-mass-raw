import sys, time, os
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i266/notes/wormhole_evolution"))
import threshold as th
h = float(sys.argv[1])
As = [-0.01, -0.001, 0.0, 0.001, 0.003, 0.005, 0.01, 0.02, 0.03, 0.05, 0.07, 0.1, 0.15, 0.2, 0.3]
for fam, B in (("O", None), ("G", 0.0), ("G", 0.025), ("G", 0.05), ("G", 0.1), ("G", 0.2)):
    if B is not None:
        th.CRIT["G_B"] = B
    X = th.CRIT["X"][fam][2]
    row = []
    for A in As:
        r = th.point(2, fam, h, X, A)
        row.append(f"{A:g}:{r['fate']:+d}")
    print(fam, B, " ".join(row), flush=True)
