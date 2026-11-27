import sys, json, math
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import threshold
rows = json.load(open(sys.argv[1])); D = int(sys.argv[2]); h = threshold.CRIT["H"][D-2][int(sys.argv[3])]
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs"
name = f"D{D}_G_h{h:g}"
s = json.load(open(f"{RAW}/{name}/summary.json")); ps = 0.5*(s["lo"]+s["hi"])
W = threshold.W_EXACT[D-2]
print("1/W", 1/W)
for key in ("T40", "t_loc", "tau_loc", "tau2", "t2"):
    rr = [dict(A=r["A"], side=r["side"], fate=r["side"], T=r[key], e=r["e"]) for r in rows if r[key] is not None and r["fate40"] == r["side"]]
    fits, prim, env = threshold.fit_set(rr, ps)
    sc = [f for f in fits if f["window"]==threshold.CRIT["windows"][0] and f["sides"]==(-1,)][0]
    ex = [f for f in fits if f["window"]==threshold.CRIT["windows"][0] and f["sides"]==(1,)][0]
    print(f"{key:8s}: primary {prim['slope']:.5f} +- {prim['se']:.5f} (rel to 1/W {prim['slope']*W-1:+.4f}); collapse {sc['slope']:.5f}, expansion {ex['slope']:.5f}; spread [{env[0]:.5f}, {env[1]:.5f}]")
