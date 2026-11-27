import sys, math, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import settled_mass as sm
lam, kp, xh = 0.6, 2.0, 1.0
h = float(sys.argv[1]); F1 = float(sys.argv[2]); K = int(sys.argv[3]); Nc = int(sys.argv[4])
Fmax = F1 * 2 ** K
Xf = 3.0 + math.log(Fmax) / kp + 1.0
Np = int(round(Xf / h)); nm0 = int(round((xh + 0.9) / h))
Sp, Sm = sm.schw_rays(lam, kp, xh, h, Np, nm0)
# exactness of the rays: F on horizon
r, f = sm.schw_exact(lam, kp, xh, np.array([3.0, 4.0]), np.array([xh, xh]))
print("r on horizon", r, "F", np.exp(-f), "expect", np.exp(kp*np.array([0.0, 1.0])))
t0 = time.time()
out = sm.chain(2, [], h, Sp, Sm, 0.0, 0.0, nm0, 0, xh / h, F1, Fmax, Nc, tol=0.0)
print("status", out["status"], "secs", out["secs"])
s = out["ser"]
M = s["M"]
print("columns", len(M), "M err max", np.max(np.abs(M - lam/2)), "x- err max", np.max(np.abs(s["xm"] - xh)))
for k in range(len(out["recs"])):
    r = out["recs"][k]
    if len(r["r"]) == 0: continue
    print("level", k, "n", len(r["r"]), "xp %.3f..%.3f" % (r["xp"][0], r["xp"][-1]), "F %.3g..%.3g" % (r["F"][0], r["F"][-1]),
          "max|M-0.3| %.3e" % np.max(np.abs(r["M"] - lam/2)), "max|xm-xh| %.3e" % np.max(np.abs(r["xm"] - xh)), "Mcell-M %.2e" % np.max(np.abs(r["Mcell"]-r["M"])), "edge min %.1f" % r["edge"].min())
