import sys, time
import numpy as np
from scipy.optimize import root
from qnm_fast import *
kind = int(sys.argv[1])
t0 = time.time()
reg = np.arange(0.40, 1.01, 0.04); imag = np.arange(-0.90, -0.09, 0.05)
G = np.array([[abs(D_l1(-1j * (a + 1j * b), 0.5, kind)) for a in reg] for b in imag])
idx = np.dstack(np.unravel_index(np.argsort(G.ravel()), G.shape))[0][:4]
print("kind", kind, "smallest |D| on grid (%.0fs):" % (time.time() - t0), [(round(reg[j], 2), round(imag[i], 2), float("%.2e" % G[i, j])) for i, j in idx], flush=True)
f = lambda v: (lambda d: [d.real, d.imag])(D_l1(-1j * (v[0] + 1j * v[1]), 0.5, kind))
for i, j in idx[:2]:
    r = root(f, [reg[j], imag[i]], tol=1e-10)
    print("   root from (%.2f, %.2f): omega = %.8f %+.8fi success=%s" % (reg[j], imag[i], r.x[0], r.x[1], r.success), flush=True)
