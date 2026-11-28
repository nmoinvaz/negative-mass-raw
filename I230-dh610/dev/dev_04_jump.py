"""#230 development: does the closed form's one free parameter follow the data? Family S plus a step b in the field's end value on each ray (odd mirror):
a 'dphi' pulse (a Gaussian in d phi/ds, centre 3, width 0.5, height b = A_d w sqrt(pi)) added to the static wormhole's field, with the constraint solved for
the total. Prediction: A = (2/pi)(phi_inf + b), phi_inf = (pi/2) sqrt(n/(n-1)); k = 2/(n A^2 - n - 1) and c = n^2 A^2/2 (k < 0 or inf: no finite tau_s).
usage: dev_04_jump.py D h X b_list...   (the ordinary S pulse of amplitude 0.05 is kept)"""
import sys, os, math
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i230/notes/wormhole_evolution"))
import expansion as ex
import dn
import throat_scaling as ts
D, h, X = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
n = D - 2
phi_inf = math.pi / 2 * math.sqrt(n / (n - 1))
w = 0.5
for b in map(float, sys.argv[4:]):
    N = int(round(X / h))
    pulses = [dict(field=0, ray="+", A=0.05, xc=ex.PULSE["xc"], w=ex.PULSE["w"]), dict(field=0, ray="+", A=b / (w * math.sqrt(math.pi)), xc=3.0, w=w, kind="dphi")]
    d = dn.ellis_rays(n, N, h, pulses=pulses, symmetric=True)
    R = ex.stream(d, tol=ex.CRIT["trap_tol"])
    R.update(ex.finish(R))
    M = ex.diag_arrays(R)
    tau, r, H, rho = M["tau"], M["r"], M["H"], M["rho"]
    A = (2 / math.pi) * (phi_inf + b)
    den = n * A * A - n - 1
    kp = 2 / den if den > 0 else float("inf")
    cp = n * n * A * A / 2
    kl = H ** 2 / np.gradient(H, tau)
    c = -rho / H ** 2
    j = np.searchsorted(r, 0.8 * r[-1])
    ki, gam, rms = ts.k_inf(r, kl)
    print(f"D={D} b={b:+.3f}: finite cells {len(r)}/{R['N']} r_end={r[-1]:.1f} n_trap_max={int(R['n_trap'].max())} | A_pred={A:.5f} k_pred={kp:.4f} c_pred={cp:.4f} | "
          f"k_loc(r={r[j]:.0f})={kl[j]:.4f} k_loc(end)={kl[-3]:.4f} c(r={r[j]:.0f})={c[j]:.4f} c(end)={c[-3]:.4f} | k_inf={ki:.4f} (g {gam:.2f}, rms {rms:.1e})", flush=True)
