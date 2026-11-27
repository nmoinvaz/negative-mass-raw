#!/usr/bin/env python3
"""dev_05: M(x+, x-) along rows x- = const (the Bondi-like mass as x+ grows), the r_- = 0 contour as a function of x+ (columns), and
the null-ray identity from the diagonal to the edge: M(edge) - m(diag) = -int (r^n/n) e^f r_- T_++ dx+."""
import math, sys, time
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i213/notes/wormhole_evolution")
import dn
SQ2 = math.sqrt(2.0)
n, A, X, h = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
N = int(round(X / h))
d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=True)
res = dn.evolve(d, kernel="numba", excise=True, rexp=1e9)
M = dn.mass_nodes(res)
print(f"D={n+2} h={h} X={X} A={A}")
print("M(x+, x-) at x- = const rows, as x+ grows (node values)")
xs = [0.0, 1.0, 2.0, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 12.0]
print("  x-\\x+  " + "  ".join(f"{xp:9.1f}" for xp in (5, 10, 20, 40, 70, 100) if xp <= X))
for xm in xs:
    j = int(round(xm / h))
    print(f"  {xm:5.1f}  " + "  ".join(f"{M[int(round(xp / h)), j]:+9.3e}" for xp in (5, 10, 20, 40, 70, 100) if xp <= X))
# r_- = 0 contour in columns: for column i (fixed x+), scan x-
c, up, um, alive = dn.cell_fields(res)
print("contour r_- = 0 (x- of the sign change in column x+):")
for xp in (3, 4, 5, 6, 8, 10, 15, 20, 40, 70, 100):
    i = min(int(round(xp / h)), N - 1)
    col = um[0][i, :]
    z = np.where(np.sign(col[:-1]) * np.sign(col[1:]) < 0)[0]
    zz = [((jj + 0.5) * h + (col[jj] / (col[jj] - col[jj + 1])) * h, float(c[0][i, jj])) for jj in z[:4]]
    print(f"  x+={xp:6.1f}: crossings (x-, r) {[(round(a, 3), round(b, 2)) for a, b in zz]}   r_- min along column {col.min():+.3e}")
# along rows: contour r_+ = 0 as function of x-
print("contour r_+ = 0 (x+ of the sign change in row x-):")
for xm in (2, 3, 3.5, 4, 5, 6, 8, 12, 20, 40, 70, 100):
    j = min(int(round(xm / h)), N - 1)
    col = up[0][:, j]
    z = np.where(np.sign(col[:-1]) * np.sign(col[1:]) < 0)[0]
    zz = [((ii + 0.5) * h + (col[ii] / (col[ii] - col[ii + 1])) * h, float(c[0][ii, j])) for ii in z[:4]]
    print(f"  x-={xm:6.1f}: crossings (x+, r) {[(round(a, 3), round(b, 2)) for a, b in zz]}")
# ray identity from the diagonal to the edge, cell-centred
Tpp = sum(d.eps[a] * up[2 + a] ** 2 for a in range(len(d.eps)))
mc = c[0] ** (n - 1) * (1 + 2 * np.exp(c[1]) * up[0] * um[0]) / 2
print("ray identity m(edge cell) - m(diag cell) = int -(r^n/n) e^f r_- T++ dx+ over the cells i = j..N-1, row j (x- = (j+.5)h)")
for xm in (3.0, 3.5, 4.0, 5.0, 6.0, 8.0, 12.0, 20.0, 40.0, 80.0):
    j = int(round(xm / h))
    if j >= N - 2: continue
    ii = np.arange(j, N)
    integrand = -(c[0][ii, j] ** n / n) * np.exp(c[1][ii, j]) * um[0][ii, j] * Tpp[ii, j]
    I = float(np.sum(integrand) * h - 0.5 * h * (integrand[0] + integrand[-1]))
    dm = float(mc[N - 1, j] - mc[j, j])
    pos = float(np.sum(np.where(integrand > 0, integrand, 0)) * h); neg = float(np.sum(np.where(integrand < 0, integrand, 0)) * h)
    print(f"  x-={xm:5.1f}: m_diag {mc[j, j]:+.4e}, m_edge {mc[N-1, j]:+.4e}, diff {dm:+.4e}, quadrature {I:+.4e}  (rel {abs(dm - I)/max(abs(dm), 1e-30):.1e}); +part {pos:+.3e} -part {neg:+.3e}")
