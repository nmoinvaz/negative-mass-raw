import sys, math, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import settled_mass as sm
lam, kp, xh = 0.6, 2.0, 5.0
F1 = float(sys.argv[1]); K = int(sys.argv[2]); Nc = int(sys.argv[3])
hs = [float(x) for x in sys.argv[4:]]
Fmax = F1 * 2 ** K
Xf = 3.0 + math.log(Fmax) / kp + 1.0
res = {}
for h in hs:
    Np = int(round(Xf / h)); nm0 = int(round(xh / h)) + Nc // 4 + 6
    Sp, Sm = sm.schw_rays(lam, kp, xh, h, Np, nm0)
    t0 = time.time()
    out = sm.chain(2, [], h, Sp, Sm, 0.0, 0.0, nm0, 0, xh / h, F1, Fmax, Nc, tol=0.0, log=lambda *a: None)
    res[h] = out
    s = out["ser"]
    print("h", h, out["status"], "secs %.1f" % out["secs"], "ncols", len(s["M"]), "max|M-.3| %.3e" % np.max(np.abs(s["M"]-lam/2)), "max|xm-xh| %.3e" % np.max(np.abs(s["xm"]-xh)))
# per-level errors by F window
print("level: err(M) at each h, then ratios")
for k in range(K + 1):
    e = []
    for h in hs:
        r = res[h]["recs"][k]
        e.append(np.max(np.abs(r["M"] - lam / 2)) if len(r["M"]) else np.nan)
    print(k, ["%.3e" % x for x in e], ["%.2f" % (e[i]/e[i+1]) for i in range(len(e)-1)])
