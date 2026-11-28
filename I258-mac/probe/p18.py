import sys, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])
bg = Bg(-1.0); sl = Slice(bg)
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
dphi, dphiN, sE, sO = solve_datum(sl, seed_phi, seed_phiN, corr_phi, corr_phiN)
SL, SR, SMAX = -1.05, 1.05, 3.0e4
zero = lambda s: 0.0
# hom solutions from SL
H = {}
for k, y0 in enumerate(((1.0, 0.0), (0.0, 1.0))):
    s1 = sl.even(SL, SMAX, zero, zero, y0)
    H[k] = s1
    print(f"hom{k} y0={y0}: dm at s=1e2,1e3,1e4,3e4:", ["%.4e" % dm_of(bg, s, *s1.sol(s)) for s in (1e2, 1e3, 1e4, 3e4)], " dr(3e4)=%.3e" % s1.sol(3e4)[0])
# start vector with a unit mass at infinity: choose combination with dm(3e4) = 1 and dr(3e4)=0
M = np.array([[dm_of(bg, 3e4, *H[k].sol(3e4)), H[k].sol(3e4)[0]] for k in (0, 1)]).T   # rows: dm, dr ; cols: hom0, hom1
w = np.linalg.solve(M, np.array([1.0, 0.0]))
print("start vector for unit mass, zero const tail:", w)
dM = 1e-4
for lab, y0 in (("left_mass dM=1e-4", tuple(dM*w)),):
    se = sl.even(SL, SR, dphi.f, dphi.fT, y0, max_step=0.01); so = sl.odd(SL, SR, dphiN.f, 0.0, max_step=0.01)
    tE = sl.even(SR, SMAX, zero, zero, tuple(se.y[:, -1]))
    c2 = 0.5*(se.sol(0.0)[1] + so.sol(0.0)[0]); c1 = se.sol(0.0)[0]
    print(f"[{lab}] c1={c1:.3e}  c2_slice={c2:.6e} (full: -6.653515e-04, change {c2+6.653515e-04:.3e}); dm_R(3e4)={dm_of(bg, 3e4, *tE.y[:, -1]):.4e}; dr tail {tE.y[0,-1]:.3e}")
    # right-start gives what
    se2 = sl.even(SR, SL, dphi.f, dphi.fT, (0.0, 0.0), max_step=0.01)
    print("   right-start c2:", 0.5*(se2.sol(0.0)[1] + so.sol(0.0)[0]))
# asym_S effect on dm tails (zero constants at S)
