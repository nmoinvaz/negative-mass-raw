#!/usr/bin/env python3
"""dev_07: expansion.stream against dn.evolve (store=True) on a small symmetric expanding run, and on a normal-pulse collapse run:
diagonal series, H, tau, edge/top masses and flux residuals, constraints, the slice minima, anti-trapped cell counts."""
import math, sys
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn, expansion as ex
SQ2 = math.sqrt(2.0)
for name, d in (("S A=0.05 D=4", ex.s_data(2, 0.04, 20.0, 0.05)), ("S A=0.05 D=5", ex.s_data(3, 0.03, 12.0, 0.05)), ("normal pulse (collapse) D=4", ex.normal_data(2, 0.04, 20.0, 0.05))):
    res = dn.evolve(d, kernel="numba", excise=True, rexp=1e9)
    R = ex.stream(d)
    dg = res.diag
    N = d.N
    ok = np.isfinite(dg["r"])
    dif = lambda a, b: float(np.nanmax(np.abs(a - b))) if np.any(np.isfinite(a)) else 0.0
    print(f"== {name}: N={N}, events {res.events or 'none'}, dead cells dn {int(res.dead.sum())}")
    print("  diag r, f, rp, rm, H, tau, t:", [f"{dif(R[k], dg[k]):.1e}" for k in ("r", "f", "rp", "rm", "H", "tau", "t")], " alive equal:", bool(np.array_equal(R['alive_diag'], ok)))
    M = dn.mass_nodes(res)
    for i0 in (N, N // 2, N // 4):
        Mj, flux, I, resid = ex.end_mass(R, i0)
        print(f"  edge column i0={i0}: |M - dn.mass_nodes| {dif(Mj, M[i0, :]):.1e}; flux-identity residual max {np.nanmax(np.abs(resid)):.3e}", end="")
        if i0 == N:
            rr, dM = dn.edge_flux_residual(res)
            print(f"; dn.edge_flux_residual {rr:.3e} (largest M change {dM:.3e})", end="")
        print()
    Mt, fl, It, rt = ex.top_mass(R)
    print(f"  top row: |M_top - dn.mass_nodes[:, N]| {dif(Mt, M[:, N]):.1e}; mirror |M_top - M_edge| {dif(Mt, ex.end_mass(R, N)[0]):.1e}; top flux residual {np.nanmax(np.abs(rt)):.3e}")
    Cpp, Cmm = dn.constraints(res)
    print(f"  constraints: max|C++| dn {np.nanmax(np.abs(Cpp)):.3e} stream {np.nanmax(R['Cpp']):.3e}; max|C--| dn {np.nanmax(np.abs(Cmm)):.3e} stream {np.nanmax(R['Cmm']):.3e}")
    th = dn.throat_min(res)
    s_idx = np.arange(2, 2 * N - 1)
    print("  slice minima: dn.throat_min has", len(th), "slices; stream node-level argmin offset |i - (s-i)|<=1 on", float(np.mean(np.abs(2 * R['argi'][:N] - np.arange(N)) <= 1)))
    c_, up_, um_, alive_ = dn.cell_fields(res)
    cc = dn.cell_class(up_[0], um_[0], 1e-2)
    print("  n_anti, n_trap per row equal to dn's:", bool(np.array_equal(R["n_anti"], ((cc == 1) & alive_).sum(axis=0))), bool(np.array_equal(R["n_trap"], ((cc == -1) & alive_).sum(axis=0))))
    rho, ppar, pperp, w, Tpm = ex.throat_stress(R)
    Tpp, Tmm, Tang, rho_dn = dn.stress(res)
    jj = np.arange(N)
    print(f"  stress on the diagonal: |rho - dn.stress rho| {dif(rho, rho_dn[jj, jj]):.1e}, |p_perp - dn.stress Tang| {dif(pperp, Tang[jj, jj]):.1e}, max|T_+-| {np.nanmax(np.abs(Tpm)):.1e}; w_bar range {np.nanmin(w):.6f} .. {np.nanmax(w):.6f}")
    mc = ex.m_diag_cells(R)
    print(f"  m_diag  |stream - mass at the cell| ", dif(mc, ((c_[0] ** (d.n - 1)) * (1 + 2 * np.exp(c_[1]) * up_[0] * um_[0]) / 2)[jj, jj]))
