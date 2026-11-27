"""pilot (development): solve_ivp work per chunk at (5, 1000, base, rtol 1e-10) with no noise, 1 ulp per entry, 1 ulp of the row maximum: the first n chunks of the interior plane"""
import sys, time
import numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i196/phase2/nonradial")
import taylor_drift as T
from scipy.integrate import solve_ivp
DP = T.make_problem_class()
st = T.scipy_star()
n = int(sys.argv[1]) if len(sys.argv) > 1 else 300
for label, kw in (("none", {}), ("entry 1 ulp", dict(noise_ulp=1.0, noise_seed=1)), ("row 1 ulp", dict(noise_row=1.0, noise_seed=1)), ("row 0.01 ulp", dict(noise_row=0.01, noise_seed=1))):
    pp = DP(st, 5, rtol=1e-10, phi_cut=1e-9, **kw)
    s = 1000.0
    Y = np.zeros((6, 3)); l, r0 = 5, pp.r0
    Y[0, 0] = r0 ** (l + 1) / l; Y[1, 0] = r0 ** l; Y[2, 1] = r0 ** l; Y[3, 1] = l * r0 ** (l - 1); Y[4, 2] = r0 ** l; Y[5, 2] = l * r0 ** (l - 1)
    Y /= np.linalg.norm(Y, axis=0)
    nch = int(max(20, abs(pp.rm - r0) * s / 2.0))
    grid = np.linspace(r0, pp.rm, nch + 1)
    # start in the middle of the star (r ~ 10): where the run spends most of its time
    i0 = nch // 2
    Q, ph = pp._qr(Y)
    t = time.time(); nfev = nrej = nst = 0
    for i in range(i0, i0 + n):
        sol = solve_ivp(lambda r, yv: (pp.J(r, s) @ yv.reshape(6, 3)).ravel(), (grid[i], grid[i + 1]), Q.ravel() if i > i0 else np.linalg.qr(np.random.default_rng(0).standard_normal((6, 3)))[0].ravel(),
                        method="DOP853", rtol=1e-10, atol=1e-14)
        Q, p = pp._qr(sol.y[:, -1].reshape(6, 3)); nfev += sol.nfev; nst += sol.t.size - 1
    print(f"{label:>14s}: {n} chunks at r ~ {grid[i0]:.1f}: {time.time() - t:.2f} s, {nst / n:.1f} steps and {nfev / n:.0f} rhs calls per chunk", flush=True)
