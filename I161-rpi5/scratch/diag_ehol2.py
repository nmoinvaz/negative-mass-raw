import sys
sys.argv = ["x"]
sys.path.insert(0, "/home/nathan/Source/negative-mass-i161/notes/warp")
import numpy as np
import planar_closure as pc
print("columns: s-grid, dt, domain, rule, L'(10) - 4.5, left/right-most nonzero A' (> 1e-12)", flush=True)
for lo, hi, ns, dt in [(-6, 6, 601, 0.002), (-6, 6, 1201, 0.002), (-6, 6, 2401, 0.002), (-6, 6, 4801, 0.002),
                       (-6, 6, 2401, 0.001), (-3, 3, 1201, 0.002), (-3, 3, 601, 0.002)]:
    sgrid = np.linspace(lo, hi, ns)
    out, H, J = pc.geodesics(sgrid, T=10.0, dt=dt)
    y = out[-1]
    nz = np.where(np.abs(y[5]) > 1e-12)[0]
    trap = np.trapezoid(y[5], sgrid)
    # plain Riemann sum (A' vanishes at the ends, so it equals the trapezoid sum)
    riem = np.sum(y[5]) * (sgrid[1] - sgrid[0])
    print(f"ns={ns} spacing={sgrid[1]-sgrid[0]:.5f} dt={dt} domain=[{lo},{hi}]: trapezoid - 4.5 = {trap - 4.5:+.3e}, Riemann - 4.5 = {riem - 4.5:+.3e}, "
          f"nonzero A' in s in [{sgrid[nz].min():.3f}, {sgrid[nz].max():.3f}]", flush=True)
