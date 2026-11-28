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
    print(f"== c = {cf}: rho_EH(v0 = -10) = {rb:.10f}")
    for d in (-1e-7, -1e-6, -1e-5, -3e-5, -1e-4, -2e-4, -3e-4, -5e-4, -1e-3, -2e-3, -1e-2, -1e-1, -0.3):
        kind, ve, re_, _ = fc.ray(f, v0, rb + d)
        lam = np.sqrt(f.lam2(ve))
        print(f"   offset {d:+.0e}: kind {kind:5s} tau_end = {f.vs - ve:.3e}  rho_end = {re_:.4g}  r = {lam*np.sqrt(1+re_**2):.5g}")
