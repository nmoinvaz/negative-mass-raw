"""
#114 pilot: estimate the wall time of one interior evaluation of D(gamma) at a given rtol, without running it.
PolarProblem._integrate_plane integrates the regular plane from r0 to r_m in n = (r_m - r0) gamma / 2 chunks, and that
loop is almost all of an evaluation at large gamma. This script times K chunks (after W untimed warm-up chunks) at P
positions spread over [r0, r_m], with the loop body copied from _integrate_plane, starting from the true plane carried there at rtol 1e-8,
and prints n times the mean time per
chunk. Calibration (planted truth): #4's laptop times at l = 4, gamma = 3000 are 2288 s (rtol 1e-10) and 17168 s
(rtol 1e-12).
Usage, from phase2/nonradial: python pilot_rate.py l gamma rtol [P] [K] [W]
"""
import os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.getcwd())
import background as B
from polar_solver import PolarProblem

l, g, rtol = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
npos, K, W = (int(sys.argv[4]) if len(sys.argv) > 4 else 12), (int(sys.argv[5]) if len(sys.argv) > 5 else 20), \
    (int(sys.argv[6]) if len(sys.argv) > 6 else 3)
P = PolarProblem(B.solve_star(0.7603, -1), l, rtol=rtol)
n = int(max(20, abs(P.rm - P.r0) * max(1.0, g) / 2.0))
grid = np.linspace(P.r0, P.rm, n + 1)
starts = [int((n - K - W) * (j + 0.5) / npos) for j in range(npos)]
Y = np.zeros((6, 3)); r0 = P.r0                              # regular_plane's initial data, copied
Y[0, 0] = r0 ** (l + 1) / l; Y[1, 0] = r0 ** l
Y[2, 1] = r0 ** l; Y[3, 1] = l * r0 ** (l - 1)
Y[4, 2] = r0 ** l; Y[5, 2] = l * r0 ** (l - 1)
Q, _ = P._qr(Y / np.linalg.norm(Y, axis=0))
saved, tp = {}, time.perf_counter()
for i in range(max(starts) + 1):                             # the true plane at rtol 1e-8, saved at each start
    if i in starts:
        saved[i] = Q
    sol = solve_ivp(lambda r, yv: (P.J(r, g) @ yv.reshape(6, 3)).ravel(), (grid[i], grid[i + 1]), Q.ravel(),
                    method='DOP853', rtol=1e-8, atol=1e-14)
    Q, _ = P._qr(sol.y[:, -1].reshape(6, 3))
print(f"  pre-pass at rtol 1e-8 over {max(starts) + 1} chunks: {time.perf_counter() - tp:.0f} s", flush=True)
per = []
for j, i0 in enumerate(starts):
    Q = saved[i0]
    for i in range(i0, i0 + W + K):
        if i == i0 + W:
            t0 = time.perf_counter()
        sol = solve_ivp(lambda r, yv: (P.J(r, g) @ yv.reshape(6, 3)).ravel(), (grid[i], grid[i + 1]), Q.ravel(),
                        method='DOP853', rtol=rtol, atol=1e-14)
        Q, _ = P._qr(sol.y[:, -1].reshape(6, 3))
    per.append((time.perf_counter() - t0) / K)
    print(f"  position {j}: r = {grid[i0]:.4f}, {per[-1] * 1e3:.2f} ms per chunk", flush=True)
est = n * float(np.mean(per))
print(f"l = {l}, gamma = {g:g}, rtol = {rtol:g}: n = {n} chunks, mean {np.mean(per) * 1e3:.2f} ms per chunk "
      f"(min {min(per) * 1e3:.2f}, max {max(per) * 1e3:.2f}), estimated interior time {est:.0f} s = {est / 3600:.2f} h")
