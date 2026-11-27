import time, sys
import numpy as np
from scipy.optimize import minimize
from qnm_fast import *
kind = int(sys.argv[1])
t0 = time.time()
reg = np.linspace(0.3, 3.0, 28); imag = np.linspace(-1.5, -0.1, 15)
G = np.array([[abs(D_l1(-1j * (a + 1j * b), 0.5, kind)) for a in reg] for b in imag])
# local minima
cands = []
for i in range(1, G.shape[0] - 1):
    for j in range(1, G.shape[1] - 1):
        if G[i, j] < G[i-1:i+2, j-1:j+2].min() + 1e-15:
            cands.append((G[i, j], reg[j], imag[i]))
cands.sort()
print("grid (%.0fs); local minima:" % (time.time() - t0), [(round(a, 3), round(b, 3), round(c, 3)) for a, b, c in cands[:5]], flush=True)
for _, a, b in cands[:3]:
    f = lambda v: abs(D_l1(-1j * (v[0] + 1j * v[1]), 0.5, kind))
    r = minimize(f, [a, b], method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-16, maxiter=300))
    print("  refined omega = %.6f %+.6fi |D|=%.2e" % (r.x[0], r.x[1], r.fun), flush=True)
