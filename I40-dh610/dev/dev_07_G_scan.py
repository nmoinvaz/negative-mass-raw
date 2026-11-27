"""dev_07: fate scan of family G (ghost A tuned + normal B = 0.1, one-sided) at D = 5, 6, with threshold.py's own family code. Usage: n h X."""
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution")
import numpy as np
import threshold as th

n, h, X = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
fam = sys.argv[4] if len(sys.argv) > 4 else "G"
As = np.concatenate([-np.logspace(-3, -0.5, 11)[::-1], [0.0], np.logspace(-3, -0.5, 11)])
row = []
for A in As:
    r = th.point(n, fam, h, X, float(A))
    row.append(r["fate"])
    print(f"A={A:+.5f} fate {r['fate']:+d} T {r['T']} cell ({r['j']}, {r['i']})", flush=True)
s = "".join({-1: "c", 1: "E", 0: "."}[f] for f in row)
print(f"D={n+2} h={h} fam={fam}: {s}")
print("flips:", [(float(As[i]), float(As[i + 1])) for i in range(len(row) - 1) if row[i] != row[i + 1]])
