import sys, time, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])   # reuse helpers (solve_datum, c2_fits)
bg = Bg(-1.0); sl = Slice(bg)
def run(seed, seedN, corr, corrN, label, hl=(0.01, 0.005, 0.0025, 0.00125)):
    dphi, dphiN, sE, sO = solve_datum(sl, seed, seedN, corr, corrN)
    fn = slice_fn_compact(sl, sE, sO, dphi, dphiN)
    out = {}
    for h in hl:
        J = int(round(3.0/h)); L0, L1 = layers_from_slice(bg, h, J, fn); Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
        H = Ua[0, :, J]; V = h*np.arange(J+1); c1, c2, rr = hs.horizon_fit(H, V)
        out[h] = (c1, c2, rr, np.max(np.abs(H)), H[::max(1, J//12)])
    print(label, {h: ('c2=%.3e' % out[h][1], 'max|H|=%.2e' % out[h][3]) for h in hl})
    return out
o = run(Data([(1e-3, 0.78, 0.22), (-0.6e-3, 0.68, 0.12)]), Data([(1e-3, 0.80, 0.2), (0.4e-3, 0.65, 0.1)]), Data([(1.0, 0.76, 0.24)]), Data([(1.0, 0.72, 0.15), (-1.0, 0.86, 0.12)]), "narrow")
print("H samples h=0.00125:", o[0.00125][4])
print("H samples h=0.0025 :", o[0.0025][4])
# smoother one-sided datum, widths >= 0.2 and support [0.55, 1.0]
o2 = run(Data([(1e-3, 0.775, 0.225), (-0.6e-3, 0.70, 0.15)]), Data([(1e-3, 0.775, 0.225), (0.4e-3, 0.70, 0.15)]), Data([(1.0, 0.775, 0.225)]), Data([(1.0, 0.70, 0.15), (-1.0, 0.85, 0.15)]), "smooth")
