import numpy as np, mpmath as mp
from coef import M4
mp.mp.dps = 40
def setup(cv):
    Kc = -2 * mp.mpf(cv) / mp.pi; c = mp.mpf(cv)
    A = lambda r: 1 + c * (r * r + 1) + Kc * (r + (r * r + 1) * mp.atan(r))
    Ap = lambda r: 2 * c * r + 2 * Kc * (1 + r * mp.atan(r))
    rh = mp.findroot(A, mp.mpf(-0.9) if cv > -1 else mp.mpf(1)) if cv != -1 else mp.mpf(0)
    return A, Ap, rh
for cv in (-0.3, -2.0, -1.0):
    A, Ap, rh = setup(cv)
    A1v = float(Ap(rh))
    print("c =", cv, "rho_h =", float(rh), "A1 =", A1v, "kappa =", A1v / 2)
    for LL in (6.0, 2.0):
        for lamv in (0.49, 0.81):
            z = mp.mpf(10) ** -9
            r = rh + z
            M = M4(float(r), lamv, LL, float(A(r)), float(Ap(r)))
            Mp = M.copy(); Mp[3, 3] += 1 / float(z)           # F = F~/z
            Mp[:, 3] = Mp[:, 3] / float(z); Mp[3, :] = Mp[3, :] * float(z)   # T^{-1} M T with T = diag(1,1,1,1/z): F = F~ / z
            # careful: T^{-1} M T: entry (i,j) * t_j / t_i with t = (1,1,1,1/z)
            M2 = M.copy().astype(complex)
            t = np.array([1, 1, 1, 1 / float(z)])
            M2 = M2 * t[None, :] / t[:, None]
            M2[3, 3] += 1 / float(z)
            res = M2 * float(z)
            ev = np.sort_complex(np.linalg.eigvals(res))
            print("  L=%g lam=%g exponents:" % (LL, lamv), np.round(ev.real, 5), " W/A1 =", round(np.sqrt(lamv) / A1v, 5))
