import numpy as np
from fs import *
bg = Bg(-1.0); sl = Slice(bg)
SL, SR = -1.05, 1.05
rng = np.random.default_rng(1)
for k in range(4):
    parts = [(rng.normal()*1e-3, rng.uniform(-0.6, 0.6), rng.uniform(0.2, 0.4)) for _ in range(3)]
    D = Data(parts)
    sol = sl.even(SL, SR, D.f, D.fT, (0.0, 0.0), max_step=0.01)
    # P-even and P-odd parts
    De = Data([(a/2, c, w) for a, c, w in parts] + [(a/2, -c, w) for a, c, w in parts])
    Do = Data([(a/2, c, w) for a, c, w in parts] + [(-a/2, -c, w) for a, c, w in parts])
    se = sl.even(SL, SR, De.f, De.fT, (0.0, 0.0), max_step=0.01); so = sl.even(SL, SR, Do.f, Do.fT, (0.0, 0.0), max_step=0.01)
    print(f"dr(0)={sol.sol(0.0)[0]:.3e}  P-even part: dr(0)={se.sol(0.0)[0]:.3e} dr'(0)={se.sol(0.0)[1]:.3e} end={se.y[:,-1]} | P-odd part: dr(0)={so.sol(0.0)[0]:.3e} dr'(0)={so.sol(0.0)[1]:.3e} end={so.y[:,-1]}")
