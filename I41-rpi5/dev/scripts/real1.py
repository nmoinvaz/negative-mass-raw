import sys, math, json, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import dn, threshold as th, settled_mass as sm
h = float(sys.argv[1]); delta = float(sys.argv[2]); F1 = float(sys.argv[3]); K = int(sys.argv[4]); Nc = int(sys.argv[5])
dxp = float(sys.argv[6]) if len(sys.argv) > 6 else 10.0
dm = float(sys.argv[7]) if len(sys.argv) > 7 else 3.0
summ = json.load(open(f"/home/nathan/Source/negative-mass-raw/I40-dh610/runs/D4_S_h{h:g}/summary.json"))
ps = 0.5*(summ["lo"]+summ["hi"])
A = ps - delta
pulses, sym, eps = th.family("S", A)
# event location from the stored I40 stall run at 1e-8 or an own quick pilot
def pilot():
    d, res = th.evolve_member(2, "S", h, 28.0, A, store=False, stop=True)
    return res.events
ev = pilot()
print("pilot event", ev, flush=True)
j0, i0 = ev["collapse"]
Np = int(i0 + dxp / h); nm0 = int(j0 + (dm + Nc * h / 4) / h)
N = max(Np, nm0)
d = dn.ellis_rays(2, N, h, pulses=pulses, symmetric=sym, eps=eps)
Fmax = F1 * 2 ** K
t0 = time.time()
out = sm.chain(2, eps, h, d.Sp[:, :Np + 1], d.Sm, 0.0, 0.0, nm0, None, None, F1, Fmax, Nc, tol=1e-2)
print("status", out["status"], "event", out["event"], "secs %.1f" % out["secs"], "cols", len(out["ser"]["r"]) if out["ser"] else 0)
s = out["ser"]
np.savez(f"/tmp/claude-1000/dev_real_h{h:g}_d{delta:g}_F{F1:g}_K{K}_N{Nc}.npz", **s)
sel = np.arange(0, len(s["r"]), max(1, len(s["r"]) // 60))
print("xp    xm      t     r      M      F      level  edge  Mcell-M")
for i in sel:
    print("%.3f %.5f %.3f %.5f %.5f %.3e %d %.0f %.1e" % (s["xp"][i], s["xm"][i], (s["xp"][i]+s["xm"][i])/math.sqrt(2), s["r"][i], s["M"][i], s["F"][i], s["level"][i], s["edge"][i], s["Mcell"][i]-s["M"][i]))
