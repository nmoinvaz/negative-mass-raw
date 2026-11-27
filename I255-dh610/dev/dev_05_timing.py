import sys, os, time, numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i255/notes/wormhole_evolution"))
import throat_locus as tl, threshold
D, hk = 5, int(sys.argv[1]); n = D-2
h = threshold.CRIT["H"][n][hk]
ps, s40 = tl.pstar_raw40(D, "G", hk)
print("h", h, "p*", ps, "G_B", threshold.CRIT["G_B"])
for tcap in (float(sys.argv[2]),):
    t0 = time.time()
    rec, L = tl.run_point(n, "G", h, ps - 1e-9, tl.tcap_smax(h, tcap), bare=True)
    print("tcap", tcap, "secs", time.time()-t0, "rows", L["rows"], "fate", rec["fate40"], rec["fate_loc"], "T40", rec["T40"], rec["loc"])
