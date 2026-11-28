import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
_a = sys.argv; sys.argv = sys.argv[:1]
import numpy as np
import horizon_sector as hs
import linear as lin
sys.argv = _a
t=time.time()
kc = hs.KChart(-1.0, pi_max=300.0)
print("chart", time.time()-t, kc.tab.shape if hasattr(kc.tab,'shape') else None)
for Pi in (-0.37,-0.36,-0.3,-0.2,-0.1,-0.05,-0.02,0.02,0.05,0.12,0.5,1,2,10,60,200,600):
    V,U = (1.0, -Pi)
    try:
        j = hs.jetsK(V,U,kc.par,kc.tab,0.0)
        print(f"Pi={Pi:8.3f} rho={j[0]:.6f} R={j[2]:.6f}")
    except Exception as e:
        print(Pi, "err", e)
