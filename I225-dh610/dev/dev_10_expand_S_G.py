import sys, math, time, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import throat_locus as tl
D = int(sys.argv[1]); hk = int(sys.argv[2]); member = sys.argv[3]; X = float(sys.argv[4]); fam = sys.argv[5]; out = sys.argv[6]
tl.job_expand(D, hk, member, X, out, fam=fam)
import glob
for f in glob.glob(f"{out}/{fam}_D{D}_{member}_*.npz"):
    L = tl.load_run(f)
    W = tl.W_EXACT[D-2]
    S = tl.expansion_summary(L, W)
    cl = S["cl"]
    print(f, "class", cl["class"], "k", round(cl["k"],4), "tau_s", round(cl["tau_s"],4), "Hratio", round(cl["Hratio"],3), "rhoratio", round(cl["rhoratio"],3), "w in", round(cl["wmin"],4), round(cl["wmax"],4), "slope test", S["slope_met"], {k: round(v,3) for k,v in S["slope_vals"].items()})
    o = S["obs"]; ix = S["ix"]
    print("   |rho|/H^2 at end:", abs(o["rho"][ix][-1])/o["H"][ix][-1]**2, " H vs Hf rel max (last half):", np.nanmax(np.abs(o["H"][ix][len(ix)//2:]/o["Hf"][ix][len(ix)//2:]-1)))
