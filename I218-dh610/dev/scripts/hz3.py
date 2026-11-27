import numpy as np, mpmath as mp
from coef1 import M3
mp.mp.dps = 40
cv = -0.3
Kc = -2 * mp.mpf(cv) / mp.pi; c = mp.mpf(cv)
A = lambda r: 1 + c * (r * r + 1) + Kc * (r + (r * r + 1) * mp.atan(r))
Ap = lambda r: 2 * c * r + 2 * Kc * (1 + r * mp.atan(r))
rh = mp.findroot(A, mp.mpf(-0.9)); A1v = float(Ap(rh))
for z in (1e-5, 1e-7):
    r = rh + z
    M = M3(float(r), 0.49, float(A(r)), float(Ap(r)))
    print("z", z); print(np.array2string(np.abs(M) * z, precision=4)); print(np.array2string(np.abs(M) * z**2, precision=4))
# try scalings T = diag(z^a, z^b, z^c)
import itertools
best = None
for p in itertools.product([-2, -1, 0, 1], repeat=3):
    z = 1e-6; r = rh + z
    M = M3(float(r), 0.49, float(A(r)), float(Ap(r)))
    t = np.array([float(z) ** q for q in p])
    M2 = M * t[None, :] / t[:, None] - np.diag([q / z for q in p])  # -T^{-1}T'
    # note T^{-1} T' = diag(q/z)
    sz = np.abs(M2 * z).max()
    z2 = 1e-7; r2 = rh + z2
    Mb = M3(float(r2), 0.49, float(A(r2)), float(Ap(r2)))
    t2 = np.array([float(z2) ** q for q in p]); Mb2 = Mb * t2[None, :] / t2[:, None] - np.diag([q / z2 for q in p])
    sz2 = np.abs(Mb2 * z2).max()
    print(p, "max|zM'| at 1e-6, 1e-7:", round(sz, 3), round(sz2, 3))
