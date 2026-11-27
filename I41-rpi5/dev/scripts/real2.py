import sys, math, json, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import dn, threshold as th, settled_mass as sm
h = float(sys.argv[1]); delta = float(sys.argv[2]); F1 = float(sys.argv[3]); K = int(sys.argv[4]); Nc = int(sys.argv[5])
fam = sys.argv[6] if len(sys.argv) > 6 else "S"
dxp, dm = 10.0, 3.0
summ = json.load(open(f"/home/nathan/Source/negative-mass-raw/I40-dh610/runs/D4_{fam}_h{h:g}/summary.json"))
ps = 0.5*(summ["lo"]+summ["hi"])
A = ps - delta
pulses, sym, eps = th.family(fam, A)
d0, res = th.evolve_member(2, fam, h, 28.0, A, store=False, stop=True)
j0, i0 = res.events["collapse"]
Np = int(i0 + dxp / h); nm0 = int(j0 + (dm + Nc * h / 4) / h)
d = dn.ellis_rays(2, max(Np, nm0), h, pulses=pulses, symmetric=sym, eps=eps)
Fmax = F1 * 2 ** K
out = sm.chain(2, eps, h, d.Sp[:, :Np + 1], d.Sm, 0.0, 0.0, nm0, None, None, F1, Fmax, Nc, tol=1e-2, log=lambda *a: None)
s = out["ser"]
tag = f"{fam}_h{h:g}_d{delta:g}_F{F1:g}_K{K}_N{Nc}"
np.savez(f"/tmp/claude-1000/dev_real_{tag}.npz", **s)
print(tag, "status", out["status"], "event", out["event"], "secs %.1f" % out["secs"], "cols", len(s["r"]))
# level-by-level: M at start, end, min, max
for k in range(K + 1):
    m = s["level"] == k
    if m.sum() == 0: continue
    print("  level %2d xp %.3f..%.3f F %.3g..%.3g M start %.5f end %.5f" % (k, s["xp"][m][0], s["xp"][m][-1], s["F"][m][0], s["F"][m][-1], s["M"][m][0], s["M"][m][-1]))
