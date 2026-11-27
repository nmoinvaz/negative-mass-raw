import sys, math, json, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import dn, threshold as th
n = 2
h = float(sys.argv[1]); X = float(sys.argv[2]); delta = float(sys.argv[3]); fcut = float(sys.argv[4])
summ = json.load(open(f"/home/nathan/Source/negative-mass-raw/I40-dh610/runs/D4_S_h{h:g}/summary.json"))
ps = 0.5*(summ["lo"]+summ["hi"])
A = ps - delta
pulses, sym, eps = th.family("S", A)
N = int(round(X/h))
t0 = time.time()
d = dn.ellis_rays(n, N, h, pulses=pulses, symmetric=sym, eps=eps)
res = dn.evolve(d, store=True, stop=False, rcut=0.05, fcut=fcut)
print("evolve secs", time.time()-t0, "events", res.events)
c, up, um, alive = dn.cell_fields(res)   # [q][i,j] cell centres
r, f = c[0], c[1]
rp, rm = up[0], um[0]
# per column i (x+ fixed): find + -> - crossing of r+ along j with r- < 0
out = []
for i in range(0, N, 10):
    col = rp[i, :]; ok = alive[i, :]
    idx = np.where(ok[:-1] & ok[1:] & (col[:-1] > 0) & (col[1:] <= 0))[0]
    if len(idx) == 0: continue
    j = idx[-1] if False else idx[0]
    fr = col[j]/(col[j]-col[j+1])
    rr = r[i,j] + fr*(r[i,j+1]-r[i,j]); ff = f[i,j] + fr*(f[i,j+1]-f[i,j])
    xm = (j+0.5+fr)*h; xp=(i+0.5)*h
    out.append((xp, xm, rr, math.exp(-ff), rr/2, len(idx), rm[i,j]))
print("xp  xm_AH  r_AH  e^-f  M=r/2  ncross  r-")
for o in out: print("%.3f %.4f %.5f %.4e %.5f %d %.4e" % o)
