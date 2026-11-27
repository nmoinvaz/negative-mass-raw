import math, sys, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import _dev_polar as P
from scipy.linalg import eigh_tridiagonal
fam = P.st.Fam(0.0, "R2"); p = P.RES["R1"]
for Lv in (-1.0, -2.0):
    x = np.linspace(-500, 500, 200001); h = x[1] - x[0]
    V = Lv / (x**2 + 1) - 3 / (x**2 + 1)**2
    w = eigh_tridiagonal(2 / h**2 + V, -np.ones(len(x) - 1) / h**2, select='i', select_range=(0, 4), eigvals_only=True)
    print("L=%g FD bound states W:" % Lv, [round(math.sqrt(-e), 5) for e in w if e < -1e-3], flush=True)
    W0 = math.sqrt(-w[0])
    t0 = time.time()
    for f in (0.7, 0.85, 0.95, 0.99, 1.01, 1.05, 1.2):
        try:
            print("  W/W0=%.2f D=%.4e (%.0fs)" % (f, P.D_l2(W0 * f, fam, p, L=Lv), time.time() - t0), flush=True)
        except Exception as e:
            print("  W/W0=%.2f ERROR %s" % (f, e), flush=True)
