import sys, time
import sympy as sp
from lin import *
T0 = time.time()
xt, xr, xs = [sp.Function(n)(rho) for n in ("xt", "xr", "xs")]
xi = [xt * Yf * ex, xr * Yf * ex, xs * sp.diff(Yf, th) * ex, 0]
g0 = sp.diag(-A, 1 / A, R2, R2 * sp.sin(th)**2)
h = sp.zeros(4, 4)
for a in range(4):
    for b in range(4):
        h[a, b] = sum(xi[c] * sp.diff(g0[a, b], X[c]) + g0[c, b] * sp.diff(xi[c], X[a]) + g0[a, c] * sp.diff(xi[c], X[b]) for c in range(4))
dphi = sum(xi[c] * sp.diff(phi0, X[c]) for c in range(4))
dE, dS, E0, S0 = linearize(h, dphi)
print("linearized %.0fs" % (time.time() - T0), flush=True)
def clean(z):
    z = sp.simplify(z / ex)
    return sp.simplify(Asub(angsub(Asub(z))))
print("background residuals:", [sp.simplify(Asub(E0[a, b])) for a in range(4) for b in range(4) if E0[a, b] != 0 or True][:16], sp.simplify(Asub(S0)))
for (a, b) in [(0, 0), (0, 1), (1, 1), (0, 2), (1, 2), (2, 2), (3, 3)]:
    r = clean(dE[a, b]); print((a, b), r, "%.0fs" % (time.time() - T0), flush=True)
print("S", clean(dS))
