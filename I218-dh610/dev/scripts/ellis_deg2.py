import math, numpy as np
from scipy.linalg import eigh_tridiagonal
from scipy.optimize import minimize_scalar
from scan4 import *
fam = st.Fam(0.0, "R2"); p = RES["R2"]
for Lv in (-2.0, -6.0):
    x = np.linspace(-600, 600, 240001); h = x[1] - x[0]
    V = Lv / (x**2 + 1) - 3 / (x**2 + 1)**2
    w = eigh_tridiagonal(2 / h**2 + V, -np.ones(len(x) - 1) / h**2, select='i', select_range=(0, 6), eigvals_only=True)
    bs = [math.sqrt(-e) for e in w if e < -1e-3]
    print("L=%g FD bound-state W (e<-1e-3):" % Lv, [round(b, 5) for b in bs[:6]], flush=True)
    Ws = np.exp(np.linspace(math.log(0.2), math.log(8.0), 120))
    D = []
    for W in Ws:
        try: D.append(detD(W, Lv, fam, p))
        except Exception as e: D.append(np.nan)
    D = np.array(D)
    print("  nan count", int(np.isnan(D).sum()), "sign changes", [(round(Ws[i], 3), round(Ws[i + 1], 3)) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])])
    mins = [i for i in range(1, len(Ws) - 1) if abs(D[i]) < abs(D[i - 1]) and abs(D[i]) < abs(D[i + 1])]
    for i in mins:
        r = minimize_scalar(lambda W: abs(detD(W, Lv, fam, p)), bracket=(Ws[i - 1], Ws[i], Ws[i + 1]), tol=1e-12)
        print("   dip near W=%.5f  refined W=%.6f |D|=%.2e" % (Ws[i], r.x, r.fun), flush=True)
