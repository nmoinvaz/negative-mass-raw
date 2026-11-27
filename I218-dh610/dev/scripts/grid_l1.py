import time, sys
import numpy as np
from scipy.optimize import minimize
from qnm_fast import *
kind = None if sys.argv[1] == "polar" else int(sys.argv[1])
t0 = time.time()
reg = np.linspace(1.2, 2.0, 9); imag = np.linspace(-0.8, -0.2, 7)
G = np.array([[abs(D_l1(-1j * (a + 1j * b), 0.5, kind)) for a in reg] for b in imag])
i, j = np.unravel_index(np.argmin(G), G.shape)
print("grid min at omega = %.3f %+.3fi |D|=%.3e (%.0fs)" % (reg[j], imag[i], G[i, j], time.time() - t0), flush=True)
f = lambda v: abs(D_l1(-1j * (v[0] + 1j * v[1]), 0.5, kind))
r = minimize(f, [reg[j], imag[i]], method="Nelder-Mead", options=dict(xatol=1e-9, fatol=1e-16, maxiter=400))
print("refined omega = %.6f %+.6fi |D|=%.2e (%.0fs)" % (r.x[0], r.x[1], r.fun, time.time() - t0))
