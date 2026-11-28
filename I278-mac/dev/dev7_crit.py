import sys
sys.argv = ["x"]
sys.path.insert(0, ".")
import numpy as np
import family_causal as fc
for cq, cf in fc.MEMBERS:
    f = fc.Fam(cf, -1.0)
    sol = fc.eh_backward(f, -10.0)
    v0 = -10.0
    rb = float(sol.sol(f.vs - v0)[0])
    isfall = lambda d: fc.ray(f, v0, rb - d)[0] == "fall"
    lo, hi = 1e-7, 1e-1
    assert not isfall(lo) and isfall(hi)
    for _ in range(80):
        mid = np.sqrt(lo*hi) if hi/lo > 1.5 else 0.5*(lo+hi)
        if isfall(mid): hi = mid
        else: lo = mid
    dc = 0.5*(lo+hi)
    print(f"== c = {cf}: d_crit = {dc:.12e}  (rho_EH(v0) = {rb:.8f}, U-offset)")
    for eps in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
        k1, v1, r1, _ = fc.ray(f, v0, rb - dc*(1-eps))
        lam = np.sqrt(f.lam2(v1))
        k2, v2, r2, _ = fc.ray(f, v0, rb - dc*(1+eps))
        print(f"   eps = {eps:.0e}: inside: kind {k1:5s} rho_end {r1:.4g} r_* = {lam*np.sqrt(1+r1**2):.5g}   | outside: kind {k2:5s} tau_fall = {f.vs - v2:.4e}")
