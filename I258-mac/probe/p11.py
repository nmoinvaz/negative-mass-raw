import sys, time, numpy as np
from fs import *
bg = Bg(-1.0); sl = Slice(bg)
SL, SR = -1.05, 1.05
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
A0 = sl.even(SL, SR, seed_phi.f, seed_phi.fT, (0, 0), max_step=0.01).y[0, -1]; Ac = sl.even(SL, SR, corr_phi.f, corr_phi.fT, (0, 0), max_step=0.01).y[0, -1]
N0 = sl.odd(SL, SR, seed_phiN.f, 0.0, max_step=0.01).y[0, -1]; Nc = sl.odd(SL, SR, corr_phiN.f, 0.0, max_step=0.01).y[0, -1]
dphi = seed_phi + corr_phi.scaled(-A0/Ac); dphiN = seed_phiN + corr_phiN.scaled(-N0/Nc)
solE = sl.even(SL, SR, dphi.f, dphi.fT, (0, 0), max_step=0.01); solO = sl.odd(SL, SR, dphiN.f, 0.0, max_step=0.01)
c2s = 0.5*(solE.sol(0.0)[1] + solO.sol(0.0)[0]); print("c2_slice", c2s)
fn = slice_fn_compact(sl, solE, solO, dphi, dphiN)
res = {}
for h in (0.01, 0.005, 0.0025, 0.00125):
    J = int(round(3.0/h)); t0 = time.time()
    L0, L1 = layers_from_slice(bg, h, J, fn); t1 = time.time()
    Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab); t2 = time.time()
    H = Ua[0, :, J]; V = h*np.arange(J+1)
    c1f, c2f, rr = hs.horizon_fit(H, V); res[h] = c2f
    print(f"h={h}: layers {t1-t0:.1f}s march {t2-t1:.1f}s  c1_fit={c1f:.3e} c2_fit={c2f:.10e} resid={rr:.2e} diff to slice {c2f-c2s:.3e} (rel {abs(c2f-c2s)/abs(c2s):.2e})", flush=True)
hs_ = sorted(res, reverse=True)
r1 = [(4*res[hs_[k+1]] - res[hs_[k]])/3 for k in range(len(hs_)-1)]
print("Richardson (h,h/2):", r1, " errors:", [x-c2s for x in r1])
r2 = [(16*r1[k+1]-r1[k])/15 for k in range(len(r1)-1)]
print("second Richardson:", r2, [x-c2s for x in r2])
