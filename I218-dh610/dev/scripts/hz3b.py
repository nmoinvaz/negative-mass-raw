import numpy as np, mpmath as mp
from coef1 import M3
mp.mp.dps = 40
for cv in (-0.3, -2.0, -1.0):
    Kc = -2 * mp.mpf(cv) / mp.pi; c = mp.mpf(cv)
    A = lambda r: 1 + c * (r * r + 1) + Kc * (r + (r * r + 1) * mp.atan(r))
    Ap = lambda r: 2 * c * r + 2 * Kc * (1 + r * mp.atan(r))
    rh = mp.findroot(A, mp.mpf(-0.9) if cv > -1 else mp.mpf(1)) if cv != -1 else mp.mpf(0)
    A1v = float(Ap(rh)); print("c", cv, "A1", A1v)
    for lamv in (0.49, 0.81):
        z = mp.mpf(10) ** -9; r = rh + z
        M = M3(float(r), lamv, float(A(r)), float(Ap(r)))
        t = np.array([1.0, float(z), 1.0])
        M2 = M * t[None, :] / t[:, None]; M2[1, 1] -= 1 / float(z)
        ev = np.sort_complex(np.linalg.eigvals(M2 * float(z)))
        print("  lam", lamv, "exponents", np.round(ev.real, 5), "mu = W/A1 =", round(np.sqrt(lamv) / A1v, 5))
