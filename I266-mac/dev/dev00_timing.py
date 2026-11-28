import sys, time, os, json
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i266/notes/wormhole_evolution"))
import numpy as np
import threshold as th
B = float(sys.argv[1]); h = float(sys.argv[2]); fam = sys.argv[3] if len(sys.argv) > 3 else "G"
th.CRIT["G_B"] = B
X = th.CRIT["X"][fam][2]
t0 = time.time()
for A in (-0.01, 0.0, 0.005, 0.01, 0.03, 0.06, 0.1, 0.15):
    r = th.point(2, fam, h, X, A)
    print(f"B={B} fam={fam} h={h} A={A}: fate {r['fate']} T {r['T']} cell ({r['j']},{r['i']}) {r['secs']} s", flush=True)
print("total", time.time() - t0)
