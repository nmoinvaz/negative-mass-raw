import sys
sys.argv = ["x"]
sys.path.insert(0, ".")
import numpy as np
import family_causal as fc
for cq, cf in fc.MEMBERS:
    f = fc.Fam(cf, -1.0)
    sol = fc.eh_backward(f, -10.0)
    for v0 in (-10.0, -5.0, -3.0, -2.0):
        rb = float(sol.sol(f.vs - v0)[0])
        print(f"c = {cf}, v0 = {v0}: backward rho_EH = {rb:.10f}")
        for d in (-1e-2, -1e-3, -1e-4, 1e-4, 1e-3, 1e-2):
            kind, ve, re_, _ = fc.ray(f, v0, rb + d)
            print(f"    offset {d:+.0e}: kind {kind:5s} v_end {ve:.9f} rho_end {re_:.4g}")
