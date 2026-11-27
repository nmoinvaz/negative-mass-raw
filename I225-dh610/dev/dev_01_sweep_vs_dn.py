import sys, time, math
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, checks, threshold, throat_locus as tl

# (a) scaled_rays at lam = 1 equals dn.ellis_rays bit for bit
pu = dict(field=0, ray="+", A=0.0148, xc=3.0, w=0.5)
pn = dict(field=1, ray="+", A=0.1, xc=3.0, w=0.5)
N, h = 400, 0.04
for sym, pl, eps in ((True, [pu], (-1.0,)), (False, [pu, pn], (-1.0, 1.0))):
    a = dn.ellis_rays(2, N, h, pulses=pl, symmetric=sym, eps=eps)
    b = tl.scaled_rays(2, N, h, 1.0, pulses=pl, symmetric=sym, eps=eps)
    print("scaled lam=1 vs dn.ellis_rays: max diff", max(np.max(np.abs(a.Sp - b.Sp)), np.max(np.abs(a.Sm - b.Sm))))

# (b) rect-mode sweep vs stored dn.evolve + throat_min on a small case (G, D=4)
pl, sym, eps = threshold.family("G", 0.0150)
N, h = 500, 0.04
d = dn.ellis_rays(2, N, h, pulses=pl, symmetric=sym, eps=eps)
t0 = time.time(); res = dn.evolve(d, store=True, stop=False, tol=1e-2, rexp=2.0); t1 = time.time()
L = tl.sweep(d, rect=True, stop=False); t2 = time.time()
print("times: evolve", t1 - t0, "sweep", t2 - t1)
print("events dn:", res.events, " sweep ev40:", L["ev40"])
tm = dn.throat_min(res)
print("throat_min slices", len(tm), "sweep slices", len(L["s"]))
# map sweep slices by t
tt = L["t"]
common = np.isin(np.round(tm[:, 0], 9), np.round(tt, 9))
print("common", common.sum())
idx = {round(x, 9): k for k, x in enumerate(tt)}
dr = []; dl = []
for row in tm:
    k = idx.get(round(row[0], 9))
    if k is None: continue
    dr.append(abs(L["r"][k] - row[1])); dl.append(abs(L["l"][k] - row[2]))
print("max |r_min diff|", max(dr), "max |l diff|", max(dl))
missing = [round(x,9) for x in tt if round(x,9) not in set(np.round(tm[:,0],9))]
print("slices in sweep not in throat_min:", len(missing), missing[:5])
miss2 = [r[0] for r in tm if round(r[0],9) not in idx]
print("slices in throat_min not in sweep:", len(miss2), miss2[:5])
# diag
dg = res.diag
print("diag r diff", np.nanmax(np.abs(dg["r"] - L["diag"]["r"][:N])), "H check")
