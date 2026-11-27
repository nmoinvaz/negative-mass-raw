import time, sys
import numpy as np
from scipy.optimize import minimize
from qnm_fast import *
kind = int(sys.argv[1]); om0 = complex(sys.argv[2])
t0 = time.time()
f = lambda v: abs(D_l1(-1j * (v[0] + 1j * v[1]), 0.5, kind))
# coarse local grid first
best = min(((f([a, b]), a, b) for a in np.linspace(om0.real - 0.3, om0.real + 0.3, 7) for b in np.linspace(om0.imag - 0.25, om0.imag + 0.25, 6)))
print("local grid min:", best, "(%.0fs)" % (time.time() - t0), flush=True)
r = minimize(f, [best[1], best[2]], method="Nelder-Mead", bounds=[(0.1, 3.0), (-2.0, -0.05)], options=dict(xatol=1e-10, fatol=1e-18, maxiter=300))
print("kind %d start %s -> omega = %.8f %+.8fi |D|=%.2e (%.0fs)" % (kind, om0, r.x[0], r.x[1], r.fun, time.time() - t0), flush=True)
