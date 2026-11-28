import sys, time, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])
exec(open('p14.py').read().split("prev = None")[0].split("fn = slice_fn_compact")[1].split("\n", 1)[1])   # resid(), pts
bg = Bg(-1.0)
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
def pipeline(mutP=None, mutL=None, fnmode=None, hl=(0.005, 0.0025)):
    sl = Slice(bg, mutP)
    dphi, dphiN, sE, sO = solve_datum(sl, seed_phi, seed_phiN, corr_phi, corr_phiN)
    drT0, n0 = sE.sol(0.0)[1], sO.sol(0.0)[0]
    c2s = 0.5*(drT0 + n0) if fnmode is None else (0.5*drT0 if fnmode == 'fn_aT' else 0.5*(drT0 - n0))
    fn = slice_fn_compact(sl, sE, sO, dphi, dphiN)
    fits = {}; Cres = {}
    for h in hl:
        J = int(round(3.0/h)); L0, L1 = layers_from_slice(bg, h, J, fn, mutL); Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
        c1, c2, rr = hs.horizon_fit(Ua[0, :, J], h*np.arange(J+1)); fits[h] = (c2, rr)
        R = resid(Ua, J, h, pts); Cres[h] = np.max(np.abs(R))
    ri = (4*fits[hl[1]][0] - fits[hl[0]][0])/3
    return dict(c2s=c2s, rich=ri, rel=abs(ri-c2s)/abs(c2s), lin=fits[hl[1]][1], C=Cres[hl[1]])
base = pipeline()
print(f"[ref] c2_slice {base['c2s']:.6e} Rich {base['rich']:.6e} rel diff {base['rel']:.1e}; horizon-law residual {base['lin']:.1e}; max|C| {base['C']:.1e}")
for lab, kw in (("H_P", dict(mutP='H_P')), ("H_eps", dict(mutP='H_eps')), ("M_phi", dict(mutP='M_phi')), ("M_F", dict(mutP='M_F')),
                ("fn_aT", dict(fnmode='fn_aT')), ("fn_sign", dict(fnmode='fn_sign')), ("l1_sign", dict(mutL='l1_sign')), ("l1_noquad", dict(mutL='l1_noquad'))):
    o = pipeline(**kw)
    print(f"[mut {lab}] c2_slice {o['c2s']:.6e}  Rich {o['rich']:.6e}  rel diff {o['rel']:.1e}; horizon-law residual {o['lin']:.1e}; max|C| {o['C']:.1e}", flush=True)
# random data at the finest pair
rng = np.random.default_rng(258); sl = Slice(bg); rows = []
t0 = time.time()
for k in range(20):
    sp = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    spN = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    dp, dpN, sE, sO = solve_datum(sl, sp, spN, corr_phi, corr_phiN)
    c2s = 0.5*(sE.sol(0.0)[1] + sO.sol(0.0)[0]); fnk = slice_fn_compact(sl, sE, sO, dp, dpN)
    F = c2_fits(fnk, (0.005, 0.0025, 0.00125)); r1 = (4*F[0.0025][1] - F[0.005][1])/3; r2 = (4*F[0.00125][1] - F[0.0025][1])/3
    amp = max(max(abs(dp.f(s)) for s in np.linspace(-1, 1, 300)), max(abs(dpN.f(s)) for s in np.linspace(-1, 1, 300)))
    rows.append((c2s, r1-c2s, r2-c2s, amp))
print("[random 20] |c2| min/med/max %.2e %.2e %.2e;  max|Rich(0.005,0.0025)-slice| %.2e; max|Rich(0.0025,0.00125)-slice| %.2e; amplitude max %.2e; max rel (finest) %.2e  [%.0fs]" % (min(abs(r[0]) for r in rows), np.median([abs(r[0]) for r in rows]), max(abs(r[0]) for r in rows), max(abs(r[1]) for r in rows), max(abs(r[2]) for r in rows), max(r[3] for r in rows), max(abs(r[2])/abs(r[0]) for r in rows), time.time()-t0))
