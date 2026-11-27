# probe 23: parity of the corrected solutions; left tail of G by right-start integration; c1 of X20
import sys, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])
bg = Bg(-1.0); sl = Slice(bg); kap = bg.kc.kappa
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
def parts(D, sign):   # P-even (sign=+1) or P-odd (sign=-1) projection of a Data
    return Data([(a/2, c, w) for a, c, w in D.parts] + [(sign*a/2, -c, w) for a, c, w in D.parts])
# P-even part of dphi and P-odd part of dphi_N: need the conditions; after them dr'(0) and n(0) vanish?
dpe, dpNo = parts(seed_phi, +1), parts(seed_phiN, -1)
dp, dpN, sE, sO = solve_datum(sl, dpe, dpNo, corr_phi, corr_phiN)
print(f"P-even dphi + P-odd dphi_N, corrected: dr(0)={sE.sol(0.0)[0]:.2e} dr'(0)={sE.sol(0.0)[1]:.2e} n(0)={sO.sol(0.0)[0]:.2e}  (before: P-even part alone had dr'(0) ~ 1e-3)")
# P-odd dphi and P-even dphi_N: no correction needed
dpo, dpNe = parts(seed_phi, -1), parts(seed_phiN, +1)
sEo = sl.even(-1.05, 1.05, dpo.f, dpo.fT, (0, 0), max_step=0.01); sOe = sl.odd(-1.05, 1.05, dpNe.f, 0.0, max_step=0.01)
print(f"P-odd dphi + P-even dphi_N, uncorrected: end vector {sEo.y[:, -1]}, n end {sOe.y[0, -1]:.2e}; c2 = {0.5*(sEo.sol(0.0)[1] + sOe.sol(0.0)[0]):.6e}")
# G: right-start integration to the left tail and beyond
dpG, dpNG, sEG, sOG = solve_datum(sl, seed_phi, seed_phiN, corr_phi, corr_phiN)
rE = sl.even(1.05, -1.05, dpG.f, dpG.fT, (0, 0), max_step=0.01); rO = sl.odd(1.05, -1.05, dpNG.f, 0.0, max_step=0.01)
tE = sl.even(-1.05, -3.0e4, lambda s: 0.0, lambda s: 0.0, tuple(rE.y[:, -1])); tO = sl.odd(-1.05, -3.0e4, lambda s: 0.0, rO.y[0, -1])
mx = max(max(abs(tE.sol(s)[0]), abs(tE.sol(s)[1]), abs(kap*s*tO.sol(s)[0]), abs(dm_of(bg, s, *tE.sol(s)))) for s in (-1.05, -10.0, -100.0, -1e3, -1e4, -3e4))
print(f"left tail of G by right-start integration, s in [-3e4, -1.05]: max of |dr|, |dr'|, |kappa s n|, |dm| = {mx:.2e}")
# c1 of the 20 random data
rng = np.random.default_rng(258); c1s = []
for k in range(20):
    sp = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    spN = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    d1, d2, sE_, sO_ = solve_datum(sl, sp, spN, corr_phi, corr_phiN); c1s.append(sE_.sol(0.0)[0])
print("c1 of X20: max |dr(0)| =", max(abs(x) for x in c1s))
