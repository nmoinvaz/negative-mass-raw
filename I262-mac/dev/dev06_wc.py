"""dev06: W(c) near c = -1 from #212's code (stability.py imported, not modified): root of its Wronskian mismatch bracketing kappa."""
import sys, time, json, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i262/notes/black_universe")
import numpy as np
from scipy.optimize import brentq
import stability as st
res = sys.argv[1] if len(sys.argv) > 1 else "R2"
cs = [float(x) for x in sys.argv[2:]] or [-1.01, -1.001, -1.0001, -0.9999, -0.999, -0.99]
for c in cs:
    t0 = time.time()
    fam = st.Fam(c, res)
    kap = fam.A1 / 2
    f = lambda W: st.mismatch(fam, W)
    lo, hi = 0.97 * kap, 1.03 * kap
    flo, fhi = f(lo), f(hi)
    if np.sign(flo) == np.sign(fhi):
        lo, hi = 0.9 * kap, 1.1 * kap; flo, fhi = f(lo), f(hi)
    W = brentq(f, lo, hi, xtol=1e-15, rtol=1e-14)
    print(json.dumps(dict(c=c, res=res, kappa=kap, W=W, w=W / kap, eps=c + 1.0, slope_est=(W / kap - 1) / (c + 1.0), seconds=round(time.time() - t0, 1))), flush=True)
