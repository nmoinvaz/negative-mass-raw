import sys, time, numpy as np
from fs import *
import fs
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])
bg = Bg(-1.0); sl = Slice(bg)
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
rng = np.random.default_rng(258)
for k in range(13):
    sp = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    spN = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
print("seed parts phi:", sp.parts); print("seed parts phiN:", spN.parts)
for (a, b) in ((SL, SR), (-1.2, 1.3)):
    A0 = sl.even(a, b, sp.f, sp.fT, (0, 0), max_step=0.01).y[0, -1]; Ac = sl.even(a, b, corr_phi.f, corr_phi.fT, (0, 0), max_step=0.01).y[0, -1]
    N0 = sl.odd(a, b, spN.f, 0.0, max_step=0.01).y[0, -1]; Nc = sl.odd(a, b, corr_phiN.f, 0.0, max_step=0.01).y[0, -1]
    print(f"interval [{a},{b}]: A0={A0:.3e} Ac={Ac:.3e} -> km={-A0/Ac:.3e};  N0={N0:.3e} Nc={Nc:.3e} -> ko={-N0/Nc:.3e}")
    dp = sp + corr_phi.scaled(-A0/Ac); dpN = spN + corr_phiN.scaled(-N0/Nc)
    sE = sl.even(a, b, dp.f, dp.fT, (0, 0), max_step=0.01); sO = sl.odd(a, b, dpN.f, 0.0, max_step=0.01)
    print("   dr'(0), n(0):", sE.sol(0.0)[1], sO.sol(0.0)[0], " c2s", 0.5*(sE.sol(0.0)[1] + sO.sol(0.0)[0]), " max|dphi|", max(abs(dp.f(s)) for s in np.linspace(-1, 1, 400)), " max|dphiN|", max(abs(dpN.f(s)) for s in np.linspace(-1, 1, 400)))
    fnk = slice_fn_compact(sl, sE, sO, dp, dpN)
    F = c2_fits(fnk, (0.005, 0.0025)); print("   fits:", {h: ('%.9e' % F[h][1], '%.1e' % F[h][2]) for h in F})
