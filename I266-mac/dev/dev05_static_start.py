"""Development: can the chain start from a static member? A = 0, B = 0 is the static Ellis wormhole as data. Fate and lifetime on the grid, and what run_real_g does with it."""
import sys, os
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i266/notes/wormhole_evolution"))
import threshold as th
import settled_mass_g as g
th.CRIT["G_B"] = 0.0
g.FAM = "G"
for h in (0.02, 0.01, 0.005):
    r = th.point(2, "G", h, 28.0, 0.0)
    print(f"h {h}: A = 0 (the static wormhole as data): fate {r['fate']}, T {r['T']}, cell ({r['j']}, {r['i']})", flush=True)
    try:
        g.run_real_g(h, 0.0, 0.0)
    except Exception as e:
        print("    run_real_g(delta = 0, ps = 0):", repr(e)[:200], flush=True)
