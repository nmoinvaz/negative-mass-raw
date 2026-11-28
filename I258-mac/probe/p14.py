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
fn = slice_fn_compact(sl, solE, solO, dphi, dphiN)
pts = [(0.6, -0.2), (1.0, -0.5), (1.5, -0.3), (2.0, -1.2), (0.8, -0.4), (0.4, -0.1), (2.5, -0.2), (1.2, -1.0)]
def resid(Ua, J, h, pts, g=bg):
    out = []
    for (V, U) in pts:
        j, i = int(round(V/h)), int(round(U/h))
        x, d, r, rV, rU, pV, pU, V0_, V1_, V2_, E, FV, FU, rhoV, rhoU = hs.jetsK(j*h, i*h, g.par, g.tab, 0.0)
        f = lambda q, dj, di: Ua[q, j + dj, i + di + J]
        d1V = lambda q: (-f(q, 2, 0) + 8*f(q, 1, 0) - 8*f(q, -1, 0) + f(q, -2, 0))/(12*h)
        d1U = lambda q: (-f(q, 0, 2) + 8*f(q, 0, 1) - 8*f(q, 0, -1) + f(q, 0, -2))/(12*h)
        d2V = lambda q: (-f(q, 2, 0) + 16*f(q, 1, 0) - 30*f(q, 0, 0) + 16*f(q, -1, 0) - f(q, -2, 0))/(12*h*h)
        d2U = lambda q: (-f(q, 0, 2) + 16*f(q, 0, 1) - 30*f(q, 0, 0) + 16*f(q, 0, -1) - f(q, 0, -2))/(12*h*h)
        CV = d2V(0) + FV*d1V(0) + rV*d1V(1) + 0.5*EPS*pV**2*f(0, 0, 0) + EPS*r*pV*d1V(2)
        CU = d2U(0) + FU*d1U(0) + rU*d1U(1) + 0.5*EPS*pU**2*f(0, 0, 0) + EPS*r*pU*d1U(2)
        out.append((CV, CU))
    return np.array(out)
prev = None
for h in (0.02, 0.01, 0.005, 0.0025):
    J = int(round(3.0/h)); L0, L1 = layers_from_slice(bg, h, J, fn); Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
    R = resid(Ua, J, h, pts)
    s = np.max(np.abs(R))
    print(f"h={h}: max|C| over the 8 points = {s:.3e}  ratio to previous {('%.2f' % (prev/s)) if prev else '-'}", flush=True); prev = s
