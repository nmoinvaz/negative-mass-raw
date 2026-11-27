import sys, math, time, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import throat_locus as tl, threshold
D = int(sys.argv[1]); hk = int(sys.argv[2]); v = float(sys.argv[3])
t0 = time.time()
P = tl.planted_series(D, hk, v)
print(f"bisect {P['lo']:.15e} {P['hi']:.15e} stopped {P['stopped']} ps {P['pstar']:.12e}  ({time.time()-t0:.0f}s)")
W = threshold.W_EXACT[D-2]
for name, rows in (("locus tau", P["rows"]), ("diag t (#40 events)", P["drows"])):
    rr = [r for r in rows if r["T"] is not None and r["fate"] == r["side"]]
    fits, prim, env = threshold.fit_set(rr, P["pstar"])
    print(f"  {name}: primary {prim['slope']:.6f} +- {prim['se']:.6f} rel to 1/W {prim['slope']*W-1:+.2e} spread [{env[0]:.6f}, {env[1]:.6f}] 1/W = {1/W:.6f} inside {env[0] <= 1/W <= env[1]}")
