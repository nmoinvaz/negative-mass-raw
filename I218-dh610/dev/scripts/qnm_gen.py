import time, cmath
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root

def frame(rhs, s0, s1, chunk, dim, k, rtol=1e-11, atol=1e-30):
    rng = np.random.RandomState(7)
    Y = rng.randn(dim, k) + 1j * rng.randn(dim, k)
    Q, _ = np.linalg.qr(Y)
    s = s0; d = np.sign(s1 - s0)
    while abs(s - s1) > 1e-12:
        s2 = s + d * min(abs(s1 - s), chunk)
        sol = solve_ivp(lambda t, y: rhs(t, y.reshape(dim, k)).reshape(-1), [s, s2], Q.reshape(-1), method="DOP853", rtol=rtol, atol=atol)
        Y = sol.y[:, -1].reshape(dim, k)
        Q, Rm = np.linalg.qr(Y)
        dg = np.diag(Rm); Q = Q * (dg / np.abs(dg))[None, :]
        s = s2
    return Q

def Dgen(Wv, Mfun, dim, k, theta, extra=None, S=None):
    """Mfun(rho, lam) -> dim x dim; k decaying columns per side; extra(rho,lam) -> dim x m extra columns (e.g. gauge)"""
    e = cmath.exp(1j * theta); mu = (Wv * e).real
    S = S or 22.0 / abs(mu); chunk = 6.0 / abs(mu)
    lamv = Wv * Wv
    rhs = lambda s, Phi: e * (Mfun(s * e, lamv) @ Phi)
    QR = frame(rhs, S, 0.0, chunk, dim, k); QL = frame(rhs, -S, 0.0, chunk, dim, k)
    cols = [QL, QR]
    if extra is not None:
        gcol = extra(0.0, lamv).reshape(dim, -1); gcol = gcol / np.linalg.norm(gcol, axis=0)
        cols.append(gcol)
    return np.linalg.det(np.hstack(cols))

def qnm(Dfun, om0):
    f = lambda v: (lambda d: [d.real, d.imag])(Dfun(-1j * (v[0] + 1j * v[1])))
    r = root(f, [om0.real, om0.imag], tol=1e-12)
    return r.x[0] + 1j * r.x[1], r.success
