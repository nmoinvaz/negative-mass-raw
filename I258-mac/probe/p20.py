import sys, time, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])
bg = Bg(-1.0); sl = Slice(bg)
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
rng = np.random.default_rng(258)
for k in range(20):
    sp = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    spN = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    dp, dpN, sE, sO = solve_datum(sl, sp, spN, corr_phi, corr_phiN)
    c2s = 0.5*(sE.sol(0.0)[1] + sO.sol(0.0)[0]); fnk = slice_fn_compact(sl, sE, sO, dp, dpN)
    F = c2_fits(fnk, (0.005, 0.0025))
    r1 = (4*F[0.0025][1] - F[0.005][1])/3
    ends = (sE.y[0, -1], sE.y[1, -1], sO.y[0, -1])
    sup = [(round(c-w, 2), round(c+w, 2)) for a, c, w in sp.parts + spN.parts]
    print(k, f"c2s {c2s:.3e} err {r1-c2s:.2e}  raw errs {F[0.005][1]-c2s:.2e} {F[0.0025][1]-c2s:.2e} ends {ends[0]:.1e} {ends[1]:.1e} {ends[2]:.1e} support min {min(a for a,b in sup)} max {max(b for a,b in sup)}", flush=True)
