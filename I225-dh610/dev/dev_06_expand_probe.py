import sys, time, math, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, checks, threshold, throat_locus as tl
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs"
D = int(sys.argv[1]); h = float(sys.argv[2]); X = float(sys.argv[3]); dA = float(sys.argv[4])
n = D - 2
# p*_h at this h is not known: use the I40 value at the nearest h (dev only): 
hk = {4: 0.02, 5: 0.00707107}[D]
s = json.load(open(f"{RAW}/D{D}_G_h{hk:g}/summary.json")); ps = 0.5*(s["lo"]+s["hi"])
A = ps + dA
pl, sym, eps = threshold.family("G", A)
N = int(round(X/h))
d = dn.ellis_rays(n, N, h, pulses=pl, symmetric=sym, eps=eps)
t0 = time.time()
L = tl.sweep(d, rect=True, stop=False)
tl.locus_series(L)
print(f"D{D} h={h} X={X} A={A:.8f}: {time.time()-t0:.1f}s, slices {len(L['s'])}, ev40 {L['ev40']}, rows {L['rows']}")
t, tau, r, l, v, f = L["t"], L["tau"], L["r"], L["l"], L["v"], L["f"]
lnr = np.log(r)
H = np.gradient(lnr, tau)
for tt in (10, 15, 20, 25, 30, 40, 50, 60, 80, 100, 120, 140):
    k = np.argmin(abs(t - tt))
    if abs(t[k]-tt) < 0.1:
        print(f"  t={t[k]:7.2f} tau={tau[k]:8.3f} l={l[k]:+8.3f} v={v[k]:+.4f} r={r[k]:9.3f} f={f[k]:+.4f} H={H[k]:.4f} e^{{-f}}={math.exp(-f[k]):.3e}  r*H={r[k]*H[k]:.2f}")
print("last valid slice t", t[-1], "ic frac", L["ic"][-1]/L["s"][-1])
dgr = L["diag"]
j = np.where(np.isfinite(dgr["r"]))[0]
print("diag last r", dgr["r"][j[-1]], "j", j[-1], "H_diag approx check later")
np.savez_compressed(sys.argv[5], t=t, tau=tau, r=r, l=l, v=v, f=f)
