"""P2: Theta_gen = a dr + mu dr' + c dphi + mu s r_Pi dF on exact pure gauge (known 0), c = -1 and -1.5, both signs of s."""
import os, sys, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
import numpy as np
import full_slice as fs


def theta_gen(sl, s, dr, drs, dphi, dF):
    mu, a, c, Q, b = sl.theta_coef(s)
    return a * dr + mu * drs + c * dphi + mu * s * b["rp"] * dF, a * dr + mu * drs + c * dphi


for c in (-1.0, -1.5):
    bg = fs.bgc(c)
    sl = fs.Slice(bg)
    fn = fs.fd_slice_fn(fs.gauge_fun(bg))
    print("c =", c)
    for s in (-3.0, -1.5, -0.3, 0.1, 0.5, 1.0, 3.0, 10.0):
        U0, UT, UN, _ = fn(s)
        tg, to = theta_gen(sl, s, U0[0], UT[0], U0[2], U0[1])
        scale = max(abs(U0[0]), abs(U0[2]), 1e-300)
        print(f"  s={s:7.2f}  dr={U0[0]: .3e} dF={U0[1]: .3e} dphi={U0[2]: .3e}  Theta_gen={tg: .3e}  Theta_old={to: .3e}  (Theta_gen/|dr|={tg/abs(U0[0]): .1e})")
