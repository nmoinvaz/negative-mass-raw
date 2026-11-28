"""P5: Theta_gen along the evolved slice V + U = 0 of #248's classes (Kruskal solver, c = -1), h = 0.01, 0.005: against -c1 of the horizon fit."""
import os, sys, math, time
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
import numpy as np
import full_slice as fs
import horizon_sector as hs

bg = fs.bgc(-1.0)
sl = fs.Slice(bg)
V0, V1, U0, U1 = hs.RECT


def theta_gen_at(U, h, s):
    j = int(round((s - V0) / h))
    i = int(round((-s - U0) / h))
    f = lambda q: U[q]
    dr, dF, dphi = U[0, j, i], U[1, j, i], U[2, j, i]
    drs = hs.fd4(U[0], j, i, 1, -1, h)
    mu, a, c, Q, b = sl.theta_coef(s)
    return a * dr + mu * drs + c * dphi + mu * s * b["rp"] * dF, dr, dF, dphi


for name in sys.argv[1:] or ("A0", "A1L", "L", "G"):
    for h in (0.01, 0.005):
        t0 = time.time()
        su = hs.KSetup(-1.0, h, *hs.RECT, hs.CLASSES[name], kc=hs.kchart(-1.0))
        U = su.run()
        V = su.V0 + h * np.arange(su.Nv + 1)
        c1, c2, res = hs.horizon_fit(U[0, :, su.ih], V)
        row = []
        for s in (0.0, 0.1, 0.25, 0.5, 1.0, 1.5, 1.9):
            th, dr, dF, dphi = theta_gen_at(U, h, s) if s > 0 else (-U[0, int(round((0 - V0) / h)), int(round((0 - U0) / h))], 0, 0, 0)
            row.append(th)
        print(f"{name:3s} h={h:7.5f} wall {time.time()-t0:5.1f}s  c1(fit)={c1: .6e} c2={c2: .6e}  Theta_gen(s=0,.1,.25,.5,1,1.5,1.9) = " + " ".join(f"{t: .6e}" for t in row), flush=True)
        print("      (Theta_gen + c1)/|c1| =", " ".join(f"{(t + c1) / abs(c1) if abs(c1) > 0 else float('nan'): .1e}" for t in row), flush=True)
        del U
