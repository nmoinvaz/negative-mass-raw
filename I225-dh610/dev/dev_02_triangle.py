import sys, time, math
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, checks, threshold, throat_locus as tl

for A in (0.0140, 0.0160):
    pl, sym, eps = threshold.family("G", A)
    N, h = 1400, 0.02          # X = 28
    d = dn.ellis_rays(2, N, h, pulses=pl, symmetric=sym, eps=eps)
    t0 = time.time(); res = dn.evolve(d, store=False, stop=True, tol=1e-2, rexp=2.0); t1 = time.time()
    Lr = tl.sweep(d, rect=True, stop=False); t2 = time.time()
    smax = 1000
    Lt = tl.sweep(d, smax=smax, stop=True); t3 = time.time()
    print(f"A={A}: dn stop events {res.events}; rect {Lr['ev40']}; tri {Lt['ev40']}; times {t1-t0:.1f} {t2-t1:.1f} {t3-t2:.1f}; rows tri {Lt['rows']}")
    print("   cross rect:", {k: v for k, v in Lr["cross"].items()}, " tri:", Lt["cross"])
    ns = len(Lt["s"])
    ok = np.array_equal(Lt["s"], Lr["s"][:ns])
    print("   same slices:", ok, "max diff r,l:", np.max(np.abs(Lt["r"] - Lr["r"][:ns])), np.max(np.abs(Lt["l"] - Lr["l"][:ns])),
          "f:", np.max(np.abs(Lt["f"] - Lr["f"][:ns])), "rp:", np.nanmax(np.abs(Lt["rp"] - Lr["rp"][:ns])), "rm:", np.nanmax(np.abs(Lt["rm"] - Lr["rm"][:ns])))
    # event times
    for key in Lt["ev40"]:
        print("   T40 tri", tl.ev40_time(Lt, key), "dn", dn.event_time(res, key)[2])
