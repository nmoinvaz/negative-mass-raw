import sys, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])
bg = Bg(-1.0); sl = Slice(bg)
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
dphi, dphiN, sE, sO = solve_datum(sl, seed_phi, seed_phiN, corr_phi, corr_phiN)
fn = slice_fn_compact(sl, sE, sO, dphi, dphiN)
pts = [(0.6, -0.2), (1.0, -0.5), (1.5, -0.3), (2.0, -1.2), (0.8, -0.4), (0.4, -0.1), (2.5, -0.2), (1.2, -1.0)]
h = 0.0025; J = int(round(3.0/h)); L0, L1 = layers_from_slice(bg, h, J, fn); Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
mxC = 0; mxT = 0
for (V, U) in pts:
    j, i = int(round(V/h)), int(round(U/h))
    x, d, r, rV, rU, pV, pU, V0_, V1_, V2_, E, FV, FU, rhoV, rhoU = hs.jetsK(j*h, i*h, bg.par, bg.tab, 0.0)
    f = lambda q, dj, di: Ua[q, j + dj, i + di + J]
    d1V = lambda q: (-f(q, 2, 0) + 8*f(q, 1, 0) - 8*f(q, -1, 0) + f(q, -2, 0))/(12*h)
    d2V = lambda q: (-f(q, 2, 0) + 16*f(q, 1, 0) - 30*f(q, 0, 0) + 16*f(q, -1, 0) - f(q, -2, 0))/(12*h*h)
    terms = [d2V(0), FV*d1V(0), rV*d1V(1), 0.5*EPS*pV**2*f(0, 0, 0), EPS*r*pV*d1V(2)]
    mxT = max(mxT, max(abs(t) for t in terms))
print("largest term of C_VV at the 8 points, datum G, h=0.0025:", mxT)
# planted c=-1: c2 fit normalised by max|dr| on the slice
bgc = Bg(-1.0)
xi  = lambda V: (0.3 + 0.7*V + 0.2*V*V + 0.1*V**3, 0.7 + 0.4*V + 0.3*V*V)
eta = lambda U: (0.03 + 0.5*U - 0.3*U*U + 0.15*U**3, 0.5 - 0.6*U + 0.45*U*U)
gf = lambda V, U: hs.gaugeK(bgc.par, bgc.tab, V, U, *xi(V), *eta(U))
fnp = fd_slice_fn(bgc, gf)
for h in (0.01, 0.005, 0.0025, 0.00125):
    J = int(round(3.0/h)); L0, L1 = layers_from_slice(bgc, h, J, fnp); Ua = march_diag_full(L0, L1, J, h, bgc.par, bgc.tab)
    c1, c2, rr = hs.horizon_fit(Ua[0, :, J], h*np.arange(J+1)); print(f"[planted c=-1] h={h}: c2_fit={c2:.3e}, max|dr| on the slice {np.max(np.abs(L0[0])):.3f}, ratio {abs(c2)/np.max(np.abs(L0[0])):.2e}")
