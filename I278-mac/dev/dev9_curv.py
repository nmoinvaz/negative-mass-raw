# dev9: curvature along the outgoing rays that reach the cone v = v* (after #277's note: Ricci along such a ray tends to 0 "by hand")
import sys
sys.argv = ["x"]
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i278/notes/black_universe")
import numpy as np
import mpmath as mp
import sympy as sp
import family_causal as fc
em = fc.em
for cq, cf in fc.MEMBERS:
    f = fc.Fam(cf, -1.0)
    sol = fc.eh_backward(f, -10.0)
    rb = float(sol.sol(f.vs + 10.0)[0])
    print(f"== c = {cf}")
    for name, d in (("right d=+1e-4", 1e-4), ("right d=+1e-6", 1e-6), ("left d=-1e-5", -1e-5), ("left d=-3e-5 (c=-1)", -3e-5)):
        kind, ve, re_, s = fc.ray(f, -10.0, rb + d, dense=True)
        out = []
        for tau in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-8):
            v = f.vs - tau
            if v > ve: continue
            rho = float(np.tan(s.sol(v)[0]))
            u = mp.nstr(-mp.expm1(-mp.mpf(f.K) * tau), 30)
            J, V, Vp, v0, _ = em.eval_family(cq, "1", "-1", u, mp.nstr(mp.mpf(rho), 25))
            Kret = em.kretschmann(J)
            Ricci = -J["F"] * (2 / (1 + mp.mpf(rho) ** 2) ** 2) + 4 * V
            r = J["r"]
            out.append(f"tau {tau:.0e}: rho {rho:.3g}, r {mp.nstr(r, 5)}, Ricci {mp.nstr(Ricci, 4)}, Kretschmann {mp.nstr(Kret, 5)}")
        print(f"  {name}:\n    " + "\n    ".join(out))
