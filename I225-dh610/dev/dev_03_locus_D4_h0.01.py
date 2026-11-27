import sys, time, math, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, checks, threshold, throat_locus as tl
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs"
D, h, X = 4, 0.01, 40.0
n = D - 2
s = json.load(open(f"{RAW}/D4_G_h{h:g}/summary.json"))
ps = 0.5*(s["lo"] + s["hi"])
for side in (-1, 1):
    A = ps + side * 1e-8
    pl, sym, eps = threshold.family("G", A)
    N = int(round(X / h))
    d = dn.ellis_rays(n, N, h, pulses=pl, symmetric=sym, eps=eps)
    t0 = time.time()
    L = tl.sweep(d, smax=int(34*SQ2/h) if False else int(34*math.sqrt(2)/h), stop=True)
    print(f"side {side}: {time.time()-t0:.1f}s ev40 {L['ev40']} T40 {tl.ev40_time(L, next(iter(L['ev40'])))} cross {L['cross']} nslices {len(L['s'])}")
    t, l, r, f = L["t"], L["l"], L["r"], L["f"]
    for tt in (1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22):
        k = np.argmin(abs(t - tt))
        if abs(t[k]-tt) < 0.02:
            print(f"   t={t[k]:6.2f} l={l[k]:+.5f} r_min={r[k]:.6f} f={f[k]:+.6f}")
