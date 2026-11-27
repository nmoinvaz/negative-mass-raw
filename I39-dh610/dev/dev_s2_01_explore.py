# development script (not a check): static order, Tangherlini invariants, Roberts exactness. Output: dev_s2_01_explore.log
import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i39/notes/wormhole_evolution')
import numpy as np, dn
SQ2 = dn.SQ2
print("== static Ellis, error vs exact, region = whole rectangle, t_c = sqrt2 X")
for n, tc, hs in ((2, 4.0, (0.04, 0.02, 0.01, 0.005)), (3, 2.7, (0.028, 0.014, 0.007, 0.0035))):
    X = tc / SQ2
    prev = None
    for h in hs:
        N = int(round(X / h))
        d = dn.ellis_rays(n, N, h)
        res = dn.evolve(d)
        r_ex, ph_ex = dn.ellis_exact_nodes(d)
        e = max(np.max(np.abs(res.G[0] - r_ex)), np.max(np.abs(res.G[1])), np.max(np.abs(res.G[2] - ph_ex)))
        er = np.max(np.abs(res.G[0] - r_ex))
        print(f"n={n} h={h} N={N}: max err (r,f,phi) {e:.4e}  r only {er:.4e}" + (f"  order {np.log2(prev/e):.3f}" if prev else ""))
        prev = e
print("== Tangherlini invariants")
for n in (2, 3, 4):
    prev = None
    for h in (0.04, 0.02, 0.01):
        N = int(round(3.5 / h))
        d = dn.tangherlini_rays(n, N, h)
        res = dn.evolve(d, rcut=0.05)
        M = dn.mass_nodes(res)
        ok = ~res.dead.astype(bool)
        e = np.max(np.abs(M[ok] - d.M0))
        xs, ms, sl = dn.contour(res, '+')
        c, up, um, alive = dn.cell_fields(res)
        # radius on the r_+ = 0 contour: interpolate r at the crossing (use cell-centre r at nearest cell)
        rr = []
        for x, m in zip(xs, ms):
            i = int((x - d.x0p) / h - 0.5); j = int((m - d.x0m) / h - 0.5)
            rr.append(c[0][i, j] + (x - d.x0p - (i + 0.5) * h) * up[0][i, j] * 0 )
        rr = np.array(rr)
        print(f"n={n} h={h} N={N}: M0={d.M0:.4f} rh={d.rh:.5f} max|M-M0| {e:.3e}" + (f" order {np.log2(prev/e):.2f}" if prev else "") +
              f"  contour pts {len(xs)} r on contour mean {rr.mean() if len(rr) else np.nan:.5f} dead {int(res.dead.sum())}")
        prev = e
print("== Roberts")
prev = None
for h in (0.04, 0.02, 0.01, 0.005):
    N = int(round(2.0 / h))
    d = dn.roberts_rays(N, h)
    res = dn.evolve(d)
    i = np.arange(N + 1)[:, None]; j = np.arange(N + 1)[None, :]
    r_ex, ph_ex = dn.roberts_exact(1.0 + i * h, 1.0 + j * h, 0.75)
    e = max(np.max(np.abs(res.G[0] - r_ex)), np.max(np.abs(res.G[1])), np.max(np.abs(res.G[2] - ph_ex)))
    xs, ms, sl = dn.contour(res, '+'); xs2, ms2, sl2 = dn.contour(res, '-')
    ex1 = np.max(np.abs(xs - ms / 1.5)) if len(xs) else np.nan
    ex2 = np.max(np.abs(xs2 - 1.5 * ms2)) if len(xs2) else np.nan
    print(f"h={h} N={N}: max err {e:.4e}" + (f" order {np.log2(prev/e):.3f}" if prev else "") + f"  contour r+=0: n={len(xs)} slope {sl:.5f} (2/3) maxdev {ex1:.3e};  r-=0: n={len(xs2)} slope {sl2:.5f} (3/2) maxdev {ex2:.3e}")
    prev = e
