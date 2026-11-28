import sys; sys.path.insert(0, ".")
import numpy as np
from fam import Fam, ray
for c, beta in ((-1.0, -0.7), (-1.0, 0.7), (-1.5, -0.7), (-1.5, 0.7)):
    f = Fam(c, beta)
    v0 = -4.0
    print(f"== c = {c}, beta = {beta}, v* = {f.vstar():.6f}, rho_h = {f.rhoh():.5f}, start v0 = {v0}")
    for r0 in (-50, -5, -2, -1, -0.5, -0.1, -0.01, 0.0, 0.01, 0.1, 0.3, 0.5, 1, 2, 5, 20, 100, 1000):
        sol = ray(f, v0, r0)
        v1, w1 = sol.t[-1], sol.y[0, -1]
        print(f"  rho0 = {r0:8.2f} -> v_end = {v1:12.6f}  rho_end = {np.tan(w1):14.6g}  r = lam R = {np.sqrt(1+f.sv(v1))*np.sqrt(1+np.tan(w1)**2) if 1+f.sv(v1)>0 else float('nan'):10.4g}")
