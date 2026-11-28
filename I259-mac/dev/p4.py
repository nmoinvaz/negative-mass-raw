"""P4: extrapolating dm(s) -> delta M by fits in 1/rho (with ln rho/rho^j terms) on the exact static mode (known 1/pi); ranges of rho limited as the chart allows (s <= 1e6, rho <= 21)."""
import os, sys, math
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-raw/I259-mac/dev"))
import mpmath as mp
exec(open(os.path.expanduser("~/Source/negative-mass-raw/I259-mac/dev/p3.py")).read().split("sl = fs.Slice(bg)")[0])

def dm_at_s(s):
    return dm_exact(s), mode(s)["rho"]

target = 1 / math.pi
for lo, hi, n in ((300.0, 1e6, 24), (1e3, 1e6, 24), (30.0, 1e6, 40), (1e2, 1e6, 40)):
    ss = np.exp(np.linspace(math.log(lo), math.log(hi), n))
    pts = np.array([dm_at_s(s) for s in ss])
    dm, rho = pts[:, 0], pts[:, 1]
    for J in (1, 2, 3, 4):
        for logs in (False, True):
            cols = [np.ones_like(rho)]
            for j in range(1, J + 1):
                cols.append(rho ** -j)
                if logs:
                    cols.append(np.log(rho) * rho ** -j)
            M = np.vstack(cols).T
            co, res, rk, sv = np.linalg.lstsq(M, dm, rcond=None)
            print(f"s in [{lo:.0e},{hi:.0e}] n={n:2d} J={J} logs={logs!s:5}  M_fit - 1/pi = {co[0]-target: .3e}  (rel {abs(co[0]-target)/target:.1e}) rank {rk}/{M.shape[1]}")
    print()
