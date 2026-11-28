"""#230 development: estimators on stored #213 runs and the D = 6 pilots.
 fit_k    : the #213 fit (linear fit of 1/H against tau over the last e-fold of r)
 k_loc    : H^2 / (dH/dtau) along the diagonal; c_loc = -rho/H^2
 k_inf    : least-squares k_loc(r) = k_inf - a r^-g over r in [r_end e^-w, r_end]; w in WINDOWS
prints values for the declared candidates so the bars can be set before the declaration."""
import sys, os, math
import numpy as np
from scipy.optimize import least_squares
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i230/notes/wormhole_evolution"))
import expansion as ex

I213 = os.path.expanduser("~/Source/negative-mass-raw/I213-dh610/runs/")
DEV = os.path.expanduser("~/Source/negative-mass-raw/I230-dh610/dev/")
RUNS = [(I213 + f, n) for f, n in (
    ("D4_tuned_h0.01.npz", 2), ("D4_tuned_h0.02.npz", 2), ("D4_A0.01_h0.01.npz", 2), ("D4_A0.05_h0.01.npz", 2), ("D4_A0.2_h0.01.npz", 2),
    ("D5_tuned_h0.00353553.npz", 3), ("D5_A0.05_h0.00353553.npz", 3))] + [(DEV + f, 4) for f in (
    "dev_01_D6_A0.05_h0.012_X60.npz", "dev_01_D6_A0.2_h0.012_X60.npz", "dev_01_D6_A0.01_h0.012_X60.npz")]


def series(path):
    R = ex.load_run(path)
    R.update(ex.finish(R))
    M = ex.diag_arrays(R)
    return R, M


def extrap(r, kl, w, r_lo_min=0.0):
    sel = r >= max(r[-1] * math.exp(-w), r_lo_min)
    rr, kk = r[sel], kl[sel]
    # thin to ~400 points for speed
    step = max(1, len(rr) // 400)
    rr, kk = rr[::step], kk[::step]
    def res(p):
        return (p[0] - p[1] * (rr / rr[-1]) ** (-p[2])) - kk
    best = None
    for g0 in (0.5, 1.0, 2.0, 3.0, 4.0):
        s = least_squares(res, [kk[-1], max(kk[-1] - kk[0], 1e-4), g0], bounds=([0, -1e3, 0.05], [1e3, 1e3, 12]))
        if best is None or s.cost < best.cost:
            best = s
    return best.x[0], best.x[2], math.sqrt(2 * best.cost / len(rr))


for path, n in RUNS:
    R, M = series(path)
    tau, r, H, rho = M["tau"], M["r"], M["H"], M["rho"]
    kl = H ** 2 / np.gradient(H, tau)
    kp = 2.0 * (n - 1)
    cp = n ** 3 / (2.0 * (n - 1))
    ix = ex.final_window(tau, r, 1.0)
    b, a = np.polyfit(tau[ix], 1 / H[ix], 1)
    kfit, ts = -1 / b, -a / b
    j50 = np.searchsorted(r, 50.0)
    c50 = (-rho / H ** 2)[min(j50, len(r) - 1)]
    out = f"{os.path.basename(path):34s} n={n} r_end={r[-1]:7.2f} kfit={kfit:.5f} (rel {kfit / kp - 1:+.1e}) ts={ts:.5f} c@{r[min(j50, len(r) - 1)]:.0f}={c50:.5f} (rel {c50 / cp - 1:+.1e}) kloc_end={kl[-3]:.5f}"
    print(out)
    for w in (1.0, 1.5, 2.0, 2.5):
        kinf, g, rms = extrap(r, kl, w)
        print(f"      window {w:3.1f} e-folds: k_inf={kinf:.5f} (rel {kinf / kp - 1:+.1e}) gamma={g:.2f} rms={rms:.1e}")
