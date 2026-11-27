import sys, time, math, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, checks, threshold, throat_locus as tl
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs"
D = int(sys.argv[1]); hk = int(sys.argv[2]); Tcap = float(sys.argv[3]); e = float(sys.argv[4])
h = threshold.CRIT["H"][D-2][hk]; n = D - 2
s = json.load(open(f"{RAW}/D{D}_G_h{h:g}/summary.json")); ps = 0.5*(s["lo"]+s["hi"])
smax = int(Tcap*math.sqrt(2)/h); N = smax
out = {}
for side in (-1, 1):
    A = ps + side * 10.0**(-e)
    pl, sym, eps = threshold.family("G", A)
    d = dn.ellis_rays(n, N, h, pulses=pl, symmetric=sym, eps=eps)
    L = tl.sweep(d, smax=smax, stop=True); tl.locus_series(L)
    out[side] = L
    print("side", side, "ev40", L["ev40"], "cross", L["cross"], "slices", len(L["s"]))
t = out[-1]["t"]
print("   t     tau    l      v     r_min(-)   r_min(+)   f(-)      diff r    ln|diff|   dln|diff|/dtau")
La, Lb = out[-1], out[1]
m = min(len(La["t"]), len(Lb["t"]))
dr = Lb["r"][:m] - La["r"][:m]
tau = La["tau"][:m]
lnd = np.log(np.abs(dr) + 1e-300)
for tt in np.arange(1, 24, 1.0):
    k = np.argmin(abs(La["t"][:m] - tt))
    if k >= m - 3 or k < 3: continue
    kk = slice(max(0, k-40), k+41)
    lam = np.polyfit(tau[kk], lnd[kk], 1)[0]
    print(f"  {La['t'][k]:6.2f} {tau[k]:6.2f} {La['l'][k]:+.4f} {La['v'][k]:+.4f} {La['r'][k]:.6f} {Lb['r'][k]:.6f} {La['f'][k]:+.5f} {dr[k]:+.3e} {lnd[k]:8.3f}  {lam:.4f}   (1/lam {1/lam if lam>0 else float('nan'):.4f})")
