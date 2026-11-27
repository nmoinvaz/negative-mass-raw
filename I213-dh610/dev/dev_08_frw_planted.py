#!/usr/bin/env python3
"""dev_08: the planted homogeneous ghost (exact open FRW, D = 4) through expansion.stream: errors of (r, f, phi) on the diagonal, H(tau),
rho, p_perp, p_par and w_bar against the exact values, at three h; orders. The comoving observer is the diagonal of the rectangle (chi const)."""
import math, sys
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn, expansion as ex
SQ2 = math.sqrt(2.0)
eta0, chi0, X = -1.0, 3.0, 2.5
hs = [float(x) for x in (sys.argv[1] if len(sys.argv) > 1 else "0.04,0.02,0.01").split(",")]
errs = {k: [] for k in ("r", "f", "phi", "H", "tau", "rho", "pperp", "ppar", "w")}
for h in hs:
    d = ex.frw_data(h, X, eta0, chi0)
    R = ex.stream(d, excise=False)
    N = d.N
    j = np.arange(N)
    eta = eta0 + (j + 0.5) * h                      # cell centre of the diagonal: u = u0 + x, v = v0 + x, eta = eta0 + x
    a, ph, H, rho = ex.frw_exact(eta)
    # cell-centre values are averages of four nodes: compare with the exact value at the centre (second order)
    r_ex = a * np.sinh(chi0)
    f_ex = -np.log(a * a / 2)
    # tau exact: int a d eta from eta0 to the centre (Gauss-Legendre on the cell grid)
    from scipy.integrate import quad
    tau_ex = np.array([quad(lambda e: math.sqrt(math.cosh(2 * e)), eta0, e0, epsabs=1e-13, epsrel=1e-13)[0] for e0 in eta])
    rhoN, ppar, pperp, w, Tpm = ex.throat_stress(R)
    for k, a_, b_ in (("r", R["r"], r_ex), ("f", R["f"], f_ex), ("phi", R["phi"][0], ph), ("H", R["H"], H), ("tau", R["tau"], tau_ex),
                      ("rho", rhoN, rho), ("pperp", pperp, rho), ("ppar", ppar, rho), ("w", w, np.ones(N))):
        errs[k].append(float(np.nanmax(np.abs(a_ - b_))))
    print(f"h={h}: N={N}, eta in [{eta[0]:.3f}, {eta[-1]:.3f}], H range [{H.min():+.3f}, {H.max():+.3f}] (bounce inside: {H.min() < 0 < H.max()}), rho range [{rho.min():.3f}, {rho.max():.3f}]; max|T+-| {np.nanmax(np.abs(Tpm)):.1e}")
print("errors by h:")
for k, v in errs.items():
    o = [math.log2(v[i] / v[i + 1]) if v[i + 1] > 0 else float('inf') for i in range(len(v) - 1)]
    print(f"  {k:6s}", ["%.3e" % x for x in v], "orders", ["%.3f" % x for x in o])
