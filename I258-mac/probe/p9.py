import sys, time, numpy as np
from fs import *
bg = Bg(-1.0)
SL, SR, SMAX = -1.05, 1.05, 3.0e4
t0 = time.time()
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)])
seed_phiN = Data([(1e-3, 0.30, 0.45), ( 0.5e-3, -0.25, 0.45)])
corr_phi  = Data([(1.0, 0.0, 0.6)])                         # P-even, even sector
corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])      # P-odd, odd sector

def end_even(sl, D, a=SL, b=SR):
    return sl.even(a, b, D.f, D.fT, (0.0, 0.0), max_step=0.01).y[:, -1]
def end_odd(sl, D, a=SL, b=SR):
    return sl.odd(a, b, D.f, 0.0, max_step=0.01).y[0, -1]

def make(sl, mass=True, odd=True):
    A0 = end_even(sl, seed_phi)[0]; Ac = end_even(sl, corr_phi)[0]
    N0 = end_odd(sl, seed_phiN);   Nc = end_odd(sl, corr_phiN)
    km = -A0/Ac if mass else 0.0
    ko = -N0/Nc if odd else 0.0
    return seed_phi + corr_phi.scaled(km), seed_phiN + corr_phiN.scaled(ko), km, ko, (A0, Ac, N0, Nc)

sl = Slice(bg)
dphi, dphiN, km, ko, ends = make(sl)
print("uncorrected end values A0, Ac, N0, Nc:", ends, " corrections km, ko:", km, ko)
def report(sl, dphi, dphiN, label, start="left"):
    solE = sl.even(SL, SR, dphi.f, dphi.fT, (0.0, 0.0), max_step=0.01)
    solO = sl.odd(SL, SR, dphiN.f, 0.0, max_step=0.01)
    dr0, drT0 = solE.sol(0.0); n0 = solO.sol(0.0)[0]
    endE = solE.y[:, -1]; endO = solO.y[0, -1]
    # tail to SMAX (data zero beyond SR): integrate hom
    tE = sl.even(SR, SMAX, lambda s: 0.0, lambda s: 0.0, tuple(endE))
    tO = sl.odd(SR, SMAX, lambda s: 0.0, endO)
    dmR = dm_of(bg, SMAX, tE.y[0, -1], tE.y[1, -1])
    maxdr = max(abs(solE.sol(s)[0]) for s in np.linspace(SL, SR, 400))
    print(f"[{label}] c1={dr0:.4e} dr'(0)={drT0:.6e} n(0)={n0:.6e} c2_slice={0.5*(drT0+n0):.6e} | end(SR): dr={endE[0]:.2e} dr'={endE[1]:.2e} n={endO:.2e} | tail at s={SMAX:g}: dr={tE.y[0,-1]:.3e} n={tO.y[0,-1]:.3e} dm_R={dmR:.3e}  max|dr|={maxdr:.2e}")
    return dict(c1=dr0, drT0=drT0, n0=n0, c2=0.5*(drT0+n0), dmR=dmR, solE=solE, solO=solO)
R0 = report(sl, dphi, dphiN, "full")
# mutations of the asymptotic conditions
d1, d1N, *_ = make(sl, mass=False, odd=True);  R1 = report(sl, d1, d1N, "mass_off")
d2, d2N, *_ = make(sl, mass=True, odd=False);  R2 = report(sl, d2, d2N, "odd_off")
# zero constants at S instead (integrate outward from S both ways): c2 = 0 by construction; show tails
def asym_S():
    solR = sl.even(0.0, SR, dphi.f, dphi.fT, (0.0, 0.0), max_step=0.01); solL = sl.even(0.0, SL, dphi.f, dphi.fT, (0.0, 0.0), max_step=0.01)
    oR = sl.odd(0.0, SR, dphiN.f, 0.0, max_step=0.01); oL = sl.odd(0.0, SL, dphiN.f, 0.0, max_step=0.01)
    for lab, so, oo, s_end in (("R", solR, oR, SR), ("L", solL, oL, SL)):
        print(f"[asym_S] {lab}: end dr={so.y[0,-1]:.3e} dr'={so.y[1,-1]:.3e} n={oo.y[0,-1]:.3e}   c2_slice=0 (constants set to zero at S)")
    tE = sl.even(SR, SMAX, lambda s: 0.0, lambda s: 0.0, tuple(solR.y[:, -1]))
    print(f"[asym_S] dm_R at s={SMAX:g}: {dm_of(bg, SMAX, tE.y[0,-1], tE.y[1,-1]):.3e}")
asym_S()
# right-start integration for the consistency check S5
solE_r = sl.even(SR, SL, dphi.f, dphi.fT, (0.0, 0.0), max_step=0.01)
solO_r = sl.odd(SR, SL, dphiN.f, 0.0, max_step=0.01)
print("right-start vs left-start at S: dr'(0):", solE_r.sol(0.0)[1], R0['drT0'], " n(0):", solO_r.sol(0.0)[0], R0['n0'])
for lab, Rm in (("mass_off", R1), ("odd_off", R2)):
    dd, ddN = (d1, d1N) if lab == "mass_off" else (d2, d2N)
    se = sl.even(SR, SL, dd.f, dd.fT, (0.0, 0.0), max_step=0.01); so = sl.odd(SR, SL, ddN.f, 0.0, max_step=0.01)
    print(f"[{lab}] right-start: dr'(0)={se.sol(0.0)[1]:.6e} n(0)={so.sol(0.0)[0]:.6e} c2_right={0.5*(se.sol(0.0)[1]+so.sol(0.0)[0]):.6e}  vs left-start c2={Rm['c2']:.6e}")
print("time", time.time()-t0)
