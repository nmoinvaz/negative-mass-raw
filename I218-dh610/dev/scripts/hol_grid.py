import sys, time
import numpy as np
from hol_root import *
kind = int(sys.argv[1])
reg = np.arange(0.1, 2.61, 0.1); imag = np.arange(-2.0, -0.04, 0.1)
t0 = time.time()
G = np.array([[abs(D_hol(-1j * (a + 1j * b), 0.5, kind)) for a in reg] for b in imag])
mins = []
for i in range(G.shape[0]):
    for j in range(G.shape[1]):
        nb = G[max(i-1,0):i+2, max(j-1,0):j+2]
        if G[i, j] <= nb.min():
            mins.append((G[i, j], round(reg[j], 2), round(imag[i], 2)))
mins.sort()
print("kind", kind, "local minima of |f| (%.0fs):" % (time.time() - t0), [(float("%.2e" % a), b, c) for a, b, c in mins[:6]], flush=True)
for a, b, c in mins[:3]:
    try:
        om = newton(lambda om: D_hol(-1j * om, 0.5, kind), complex(b, c), tol=1e-12, maxiter=60)
        print("  refined %.10f %+.10fi" % (om.real, om.imag), flush=True)
    except Exception as ex:
        print("  refine from", b, c, "failed", flush=True)
