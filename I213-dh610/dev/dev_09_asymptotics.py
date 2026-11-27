#!/usr/bin/env python3
"""dev_09: the late diagonal of the streamed symmetric runs. Per member: e-folds, tau_s and k of H = k/(tau_s - tau) from a linear fit of 1/H
against tau over the last e-fold of r, |rho|/H^2, m/(r^3 H^2/2), r_ll > 0, the horizon positions; at h and h/2."""
import math, sys, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn, checks, expansion as ex
SQ2 = math.sqrt(2.0)
n = int(sys.argv[1]); X = float(sys.argv[2]); hs = [float(x) for x in sys.argv[3].split(",")]
amps = sys.argv[4].split(",")
W = checks.W_EXACT[n]
def fit_window(R, nfold=1.0):
    ok = np.isfinite(R["r"]) & np.isfinite(R["H"])
    j = np.where(ok)[0]
    rmax = R["r"][j[-1]]
    m = ok & (R["r"] >= rmax / math.exp(nfold))
    tau, H = R["tau"][m], R["H"][m]
    A = np.polyfit(tau, 1 / H, 1)
    res = 1 / H - np.polyval(A, tau)
    return -1 / A[0], -A[1] / A[0], float(np.max(np.abs(res)) / np.mean(1 / H)), m.sum()
for h in hs:
    N = int(round(X / h))
    for a in amps:
        if a == "tuned":
            lo, hi, k = checks.bisect_A(n, h, 20.0 if n == 2 else 15.0, -0.01, 0.01, 1e-10)
            A = 0.5 * (lo + hi) + 1e-6
            lab = f"p*_h+1e-6 = {A:.6e}"
        else:
            A = float(a); lab = f"A={A}"
        t0 = time.time()
        d = ex.s_data(n, h, X, A)
        R = ex.stream(d)
        rho, ppar, pperp, w, Tpm = ex.throat_stress(R)
        k_, ts, relres, npt = fit_window(R)
        jl = np.where(R["alive_diag"])[0][-1]
        m = ex.m_diag_cells(R)
        print(f"D={n+2} h={h} X={X} {lab}: {time.time()-t0:.0f} s; last diag t={R['t'][jl]:.1f} tau={R['tau'][jl]:.4f} r={R['r'][jl]:.2f} (e-folds ln r {math.log(R['r'][jl]):.3f}) H={R['H'][jl]:.3f}; "
              f"1/H linear fit over the last e-fold of r ({npt} pts): k={k_:.4f} tau_s={ts:.4f} max|res|/mean={relres:.1e}; |rho|/H^2={abs(rho[jl])/R['H'][jl]**2:.4f}; m/(r^{n+1}H^2/2)={m[jl]/(R['r'][jl]**(n+1)*R['H'][jl]**2/2):.4f}; "
              f"min r_ll {np.nanmin(R['rll']):+.3e}; max e^-f {np.nanmax(R['emf_max']):.4f}; min e^-f {np.nanmin(R['emf_min']):.2e}; dead {int(R['n_dead'].max())}; w_bar {np.nanmin(w):.6f}..{np.nanmax(w):.6f}")
        # H at fixed r
        for r0 in (3, 5, 10, 25, 50, 100):
            jj = np.where(R["alive_diag"] & (R["r"] >= r0))[0]
            if len(jj) and R["r"][jl] > r0:
                j0 = jj[0]
                print(f"      r={r0:4d}: tau={R['tau'][j0]:.4f} H={R['H'][j0]:.4f} H/W={R['H'][j0]/W:.3f}  d ln(r-1)/dtau={np.gradient(np.log(R['r'] - 1), R['tau'])[j0]/W:.3f} W   |rho|/H^2 {abs(rho[j0])/R['H'][j0]**2:.3f}")
