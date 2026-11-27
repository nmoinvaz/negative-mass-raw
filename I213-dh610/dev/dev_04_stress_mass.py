#!/usr/bin/env python3
"""dev_04: on a stored symmetric expanding run (family S): rho, p_par, p_perp, w on the diagonal, the Misner-Sharp mass there, the edge masses
and the flux identity, the anti-trapped wedge and its horizon contours, and the minimum-r slice over full-length slices."""
import math, sys, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn
SQ2 = math.sqrt(2.0)
n, A, X, h = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
N = int(round(X / h))
d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=True)
t0 = time.time()
res = dn.evolve(d, kernel="numba", excise=True, rexp=1e9)
print(f"D={n+2} h={h} X={X} N={N} A={A}: evolved in {time.time()-t0:.1f} s; events {res.events}; dead {int(res.dead.sum())}")
c, up, um, alive = dn.cell_fields(res)
Tpp, Tmm, Tang, rho = dn.stress(res)
j = np.arange(N)
dg = res.diag
r, f = c[0][j, j], c[1][j, j]
rp, rm = up[0][j, j], um[0][j, j]
phip, phim = up[2][j, j], um[2][j, j]
Tpp_d, Tmm_d, Tang_d, rho_d = Tpp[j, j], Tmm[j, j], Tang[j, j], rho[j, j]
pl = np.exp(f) * (Tpp_d + Tmm_d) / 2           # T_ll = rho (T_+- = 0)
pp = Tang_d
wbar = (pl + n * pp) / ((n + 1) * rho_d)
m_d = r ** (n - 1) * (1 + 2 * np.exp(f) * rp * rm) / 2
print("asym |T++ - T--| diag max", np.max(np.abs(Tpp_d - Tmm_d)), " |phi+ + phi-| max", np.max(np.abs(phip + phim)), " T+- check: eps(phi+phi- - phi+phi-) = 0 by algebra")
print("w identity: w_bar", wbar[[10, 100, 400, N//4, N//2, N-2]], "expected", (1 - n) / (1 + n), "; p_perp/rho min/max", (pp / rho_d).min(), (pp / rho_d).max())
print("   t     tau       r_th       H        rho         |rho|/H^2   p_perp/rho  m_diag      m/(r^3 H^2/2)  rp/rm   r_ll(sign)")
rll = np.full(N, np.nan)
G0 = res.G[0]
# r_ll on the diagonal from the nodes (i, i): the slice neighbours (i+1, i-1), (i-1, i+1)
ii = np.arange(1, N)
rll_nodes = (G0[ii + 1 if False else ii, ii] * 0)  # placeholder
for tt in (4, 6, 8, 10, 15, 20, 30, 40, 60, 80):
    k = int(np.argmin(np.abs(dg["t"] - tt)))
    if k >= N - 2 or abs(dg["t"][k] - tt) > 0.5: continue
    # second difference across the diagonal at node (k+1, k+1): (r(k+2,k) + r(k,k+2) - 2 r(k+1,k+1)) / (h^2) in l = ((i-j) h/sqrt2) -> dl = sqrt2 h
    rl2 = (G0[k + 2, k] + G0[k, k + 2] - 2 * G0[k + 1, k + 1]) / (2 * h * h)
    print(f"  {dg['t'][k]:6.2f} {dg['tau'][k]:7.3f} {r[k]:9.3f} {dg['H'][k]:8.4f} {rho_d[k]:+11.4e} {abs(rho_d[k]) / dg['H'][k]**2:10.4f} {pp[k] / rho_d[k]:+9.4f} {m_d[k]:11.4e} {m_d[k] / (r[k]**3 * dg['H'][k]**2 / 2):9.4f} {rp[k] / rm[k]:7.3f} {rl2:+.4e}")
# edges
M = dn.mass_nodes(res)
MR, ML = M[-1, :], M[:, -1]
print("mirror: max |M_R(j) - M_L(j)|", np.max(np.abs(MR - ML)))
resid, dM = dn.edge_flux_residual(res)
print(f"edge flux residual {resid:.3e}, largest |M change| {dM:.3e}; M_R(0) {MR[0]:.6f}, M_R(end) {MR[-1]:.6f}, min/max {MR.min():.4f}/{MR.max():.4f}")
for jj in (0, 50, 100, 200, 400, N // 4, N // 2, N - 1):
    print(f"   edge x-={jj*h:7.2f} t={(X + jj*h)/SQ2:7.2f}  r_edge {res.G[0][-1, jj]:8.3f}  M_R {MR[jj]:+.6f}")
# anti-trapped wedge: per selected row j, the cells with r+ > tol and r- > tol
cc = dn.cell_class(up[0], um[0], 1e-2)
for tt in (4, 6, 10, 20, 40, 60, 80):
    k = int(np.argmin(np.abs(dg["t"] - tt)))
    if k >= N - 2: continue
    row = cc[:, k]                       # i along x+ at x- = (k + .5) h
    ia = np.where(row == 1)[0]
    if len(ia):
        # horizon contours in this row: sign change of r_+ (left side) and of r_- (right side)
        col_p, col_m = up[0][:, k], um[0][:, k]
        zp = np.where(np.sign(col_p[:-1]) * np.sign(col_p[1:]) < 0)[0]
        zm = np.where(np.sign(col_m[:-1]) * np.sign(col_m[1:]) < 0)[0]
        def rz(z):
            return [(round((i + .5) * h, 3), round(float(c[0][i, k]), 3)) for i in z[:3]]
        print(f"  t={dg['t'][k]:6.2f}: anti-trapped cells i = {ia[0]}..{ia[-1]} (x+ {(ia[0]+.5)*h:.2f}..{(ia[-1]+.5)*h:.2f}), diag at x+ {(k+.5)*h:.2f}, r there {r[k]:.3f}; r+ = 0 crossings (x+, r) {rz(zp)}; r- = 0 crossings {rz(zm)}; 1/H = {1/dg['H'][k]:.3f}")
# min r slice over full-length slices
th = dn.throat_min(res)
full = th[:, 0] * SQ2 <= X
print("throat_min on full-length slices: max |l_min|", np.max(np.abs(th[full, 2])), "max |r_min - r_diag|:", end=" ")
tt_d = dg["t"]; rr = np.interp(th[full, 0], tt_d, dg["r"])
print(np.max(np.abs(th[full, 1] - rr)), "; truncated slices max |l_min|", np.max(np.abs(th[~full, 2])) if (~full).any() else None)
