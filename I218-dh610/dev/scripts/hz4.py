import numpy as np, mpmath as mp, itertools
from coef import M4
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import stability as st
fam = st.Fam(-0.3, "R2")
rh, A1v = fam.rh, fam.A1
print("rho_h, kappa", rh, A1v / 2)
lamv, LL = 0.49, 6.0
def Mscaled(z, p):
    r = rh + z
    M = M4(r, lamv, LL, float(fam.A(r)), float(fam.Ap(r))) if abs(z) > 1e-3 else None
    return M
# use high precision for small z via mpmath-evaluated A and A' then plain float M4 (entries are rational so ok if A accurate)
mp.mp.dps = 40
Kc = mp.mpf(fam.K); c = mp.mpf(-0.3)
def A_mp(r): return 1 + c * (r * r + 1) + Kc * (r + (r * r + 1) * mp.atan(r))
def Ap_mp(r): return 2 * c * r + 2 * Kc * (1 + r * mp.atan(r))
rh_mp = mp.findroot(A_mp, mp.mpf(rh))
for z in (1e-3, 1e-5, 1e-7):
    r = rh_mp + z
    M = M4(float(r), lamv, LL, float(A_mp(r)), float(Ap_mp(r)))
    print("z =", z, "max |z M| by row/col:")
    print(np.round(np.abs(z * M), 4))
