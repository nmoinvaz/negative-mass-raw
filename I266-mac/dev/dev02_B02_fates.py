import sys, os
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i266/notes/wormhole_evolution"))
import threshold as th
th.CRIT["G_B"] = 0.2
h = float(sys.argv[1])
X = 28.0
for A in (0.04, 0.05, 0.06, 0.065, 0.068, 0.0682, 0.06830, 0.068305, 0.0683054, 0.06830546, 0.068306, 0.0684, 0.0686, 0.07, 0.075, 0.09):
    r = th.point(2, "G", h, X, A)
    print(f"A {A:.8f} fate {r['fate']:+d} T {r['T']} cell ({r['j']},{r['i']})", flush=True)
