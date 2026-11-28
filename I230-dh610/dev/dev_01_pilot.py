"""#230 development pilot: one streamed run of family S with expansion.py's code (imported, unchanged), then the local exponents.
usage: dev_01_pilot.py D A h X OUT.npz   (A a float, or 'tuned' with h = 0.01 at D = 4 uses the stored #213 member)
prints the table k_loc = H^2/Hdot, c = -rho/H^2, A^2/(n/(n-1)) - 1 against r, and the smallest e^{-f}."""
import sys, os, math, time
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i230/notes/wormhole_evolution"))
import expansion as ex

D, A, h, X, out = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), sys.argv[5]
n = D - 2
t0 = time.time()
d = ex.s_data(n, h, X, A)
R = ex.stream(d, tol=ex.CRIT["trap_tol"])
secs = time.time() - t0
ex.save_run(out, R, dict(kind="S", n=n, h=h, X=X, A=A, secs=secs, member=str(A), mut=None, dn_mut=None))
R.update(ex.finish(R))
M = ex.diag_arrays(R)
tau, r, H, rho = M["tau"], M["r"], M["H"], M["rho"]
Hd = np.gradient(H, tau)
kl = H ** 2 / Hd
c = -rho / H ** 2
A2 = 2 * c / n ** 2
print(f"D={D} A={A} h={h} X={X} N={R['N']} secs={secs:.1f} finite diag cells={len(r)} of {R['N']}  r_end={r[-1]:.2f}  tau_end={tau[-1]:.4f}")
print("min e^{-f} on the diagonal:", float(np.nanmin(np.exp(-R['f'][M['ix']]))), " first dead cell:", R.get("first_dead"))
ref = n / (n - 1)
print("k_pred", 2 * (n - 1), "c_pred", n ** 3 / (2 * (n - 1)))
for r0 in (3, 5, 10, 15, 20, 30, 40, 50, 60, 80, 100, 150, 200):
    j = np.searchsorted(r, r0)
    if j >= len(r) - 2:
        break
    print(f" r={r[j]:8.2f} tau={tau[j]:9.4f} H={H[j]:9.4f} k_loc={kl[j]:9.5f} c={c[j]:10.5f}  A2/ref-1={A2[j] / ref - 1:+.3e}")
ok = np.isfinite(r)
ix = ex.final_window(tau, r, 1.0)
b, a = np.polyfit(tau[ix], 1 / H[ix], 1)
print(f"fit over last e-fold: k={-1 / b:.5f} tau_s={-a / b:.5f} tau_end={tau[-1]:.4f}  (tau_s-tau_end={-a / b - tau[-1]:.4f})")
