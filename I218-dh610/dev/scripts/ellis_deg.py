import math, numpy as np
from scipy.linalg import eigh_tridiagonal
from scan4 import *
Lv = 0.0
x = np.linspace(-400, 400, 160001); h = x[1] - x[0]
V = Lv / (x**2 + 1) - 3 / (x**2 + 1)**2
d = 2 / h**2 + V; e = -np.ones(len(x) - 1) / h**2
w = eigh_tridiagonal(d, e, select='i', select_range=(0, 2), eigvals_only=True)
print("lowest eigenvalues of -Z'' + V Z (L=%g):" % Lv, w)
lam0 = -w[0]; W0 = math.sqrt(lam0) if lam0 > 0 else None
print("bound state W0 =", W0)
fam = st.Fam(0.0, "R2"); p = RES["R2"]
for f in (0.5, 0.7, 0.8, 0.9, 1.1, 1.2, 1.5, 2.0):
    print("W/W0 = %.3f  D = %.4e" % (f, detD(W0 * f, Lv, fam, p)))
