import sys, time, math, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import dn, checks, threshold, throat_locus as tl
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs"
D = int(sys.argv[1]); hk = int(sys.argv[2]); h = threshold.CRIT["H"][D-2][hk]
n = D - 2
name = f"D{D}_G_h{h:g}"
s = json.load(open(f"{RAW}/{name}/summary.json"))
ps = 0.5*(s["lo"] + s["hi"])
Tcap = float(sys.argv[3]) if len(sys.argv) > 3 else 32.0
smax = int(Tcap*math.sqrt(2)/h)
N = smax
rows = []
t0 = time.time()
es = [3.0 + 0.5*k for k in range(19)]
for e in es:
    for side in (-1, 1):
        A = ps + side * 10.0**(-e)
        pl, sym, eps = threshold.family("G", A)
        d = dn.ellis_rays(n, N, h, pulses=pl, symmetric=sym, eps=eps)
        L = tl.sweep(d, smax=smax, stop=True)
        tl.locus_series(L)
        key = next(iter(L["ev40"]), None)
        T40 = tl.ev40_time(L, key) if key else None
        if side == -1:
            c = tl.crossing(L, "c:0.5"); c2 = tl.crossing(L, "c:0.75"); fate = -1
        else:
            c = tl.crossing(L, "e:2.0"); c2 = tl.crossing(L, "e:3.0"); fate = 1
        rows.append(dict(e=e, side=side, A=A, fate40=(-1 if key == "collapse" else 1 if key else 0), T40=T40, t_loc=c and c[0], tau_loc=c and c[1], tau2=c2 and c2[1], t2=c2 and c2[0], v=float(np.nanmean(L["v"][-300:]))))
        print(f"e={e} side={side} fate40={rows[-1]['fate40']} T40={T40} t_loc={c and c[0]} tau_loc={c and c[1]} v_end={rows[-1]['v']:.4f} ({time.time()-t0:.0f}s)", flush=True)
json.dump(rows, open(sys.argv[4] if len(sys.argv) > 4 else "series.json", "w"))
