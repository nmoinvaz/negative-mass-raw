import sys, time, cmath, math
import numpy as np
from numba import njit
import os
from scipy.integrate import solve_ivp
from scipy.optimize import root
from coef_gen import m3_entries_c as m3_entries, g3_entries_c as g3_entries, m4_entries_c as m4_entries
m3n = njit(m3_entries); g3n = njit(g3_entries); m4n = njit(m4_entries)

@njit
def rhs3c(s, y, e, lam):   # Ellis, A = 1; rho = s e
    r = s * e
    m = m3n(r, lam, 1.0, 0.0)
    out = np.empty(3, dtype=np.complex128)
    for i in range(3):
        acc = 0j
        for j in range(3):
            acc += m[i * 3 + j] * y[j]
        out[i] = e * acc
    return out

@njit
def rhs_schr(s, y, e, lam, kind):
    r = s * e
    R2 = r * r + 1.0
    if kind == 0:
        V = 2.0 / R2 + 1.0 / (R2 * R2)
    elif kind == 1:
        V = 2.0 / R2 - 3.0 / (R2 * R2)
    elif kind == 3:
        V = 1.0 / (R2 * R2)
    else:
        V = 6.0 / R2 - 3.0 / (R2 * R2)
    return np.array([e * y[1], e * (V + lam) * y[0]], dtype=np.complex128)

def frame(rhs, args, s0, s1, dim, chunk):
    rng = np.random.RandomState(5)
    y = rng.randn(dim) + 1j * rng.randn(dim); y /= np.linalg.norm(y)
    s = s0; d = np.sign(s1 - s0)
    while abs(s - s1) > 1e-12:
        s2 = s + d * min(abs(s1 - s), chunk)
        sol = solve_ivp(lambda t, yy: rhs(t, yy, *args), [s, s2], y, method="DOP853", rtol=1e-11, atol=1e-30)
        y = sol.y[:, -1]; y /= np.linalg.norm(y); s = s2
    return y

def D_l1(Wv, theta, kind=None):
    e = cmath.exp(1j * theta); mu = (Wv * e).real; S = 22.0 / abs(mu); ch = 6.0 / abs(mu); lam = Wv * Wv
    if kind is None:
        yR = frame(rhs3c, (e, lam), S, 0.0, 3, ch); yL = frame(rhs3c, (e, lam), -S, 0.0, 3, ch)
        g = np.array(g3n(0.0, lam, 1.0, 0.0), dtype=complex); g /= np.linalg.norm(g)
        return np.linalg.det(np.column_stack([yL, yR, g]))
    yR = frame(rhs_schr, (e, lam, kind), S, 0.0, 2, ch); yL = frame(rhs_schr, (e, lam, kind), -S, 0.0, 2, ch)
    return yL[0] * yR[1] - yL[1] * yR[0]

def find(kind, om0, theta=0.5):
    f = lambda v: (lambda d: [d.real, d.imag])(D_l1(-1j * (v[0] + 1j * v[1]), theta, kind))
    r = root(f, [om0.real, om0.imag], tol=1e-11)
    return r.x[0] + 1j * r.x[1], r.success

if __name__ == "__main__":
    t0 = time.time()
    for name, kind in (("test scalar l=1 (V=2/R2+1/R4)", 0), ("V=2/R2-3/R4", 1), ("l=2 master 6/R2-3/R4", 2), ("polar l=1 (H1=0 gauge system)", None)):
        for om0 in ((1.6 - 0.5j) if kind != 2 else (1.75 - 0.3j),):
            om, ok = find(kind, om0)
            print("%-35s -> omega = %.6f %+.6fi ok=%s (%.0fs)" % (name, om.real, om.imag, ok, time.time() - t0), flush=True)
