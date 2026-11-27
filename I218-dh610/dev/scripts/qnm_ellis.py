import sys, time, math, cmath
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root, fsolve
from coef import M4, N2

def frame(rhs, s0, s1, n, rtol=1e-10, atol=1e-30, chunk=None, dim=4, Wr=1.0):
    """integrate k=2 frame from s0 to s1 with QR each chunk; return (dim x 2) Q"""
    s = s0
    Y = np.zeros((dim, 2), dtype=complex)
    Y[0, 0] = 1; Y[1, 1] = 1
    Y[:, 0] += 0.1j * np.arange(1, dim + 1)  # generic
    Y[:, 1] += 0.3 * np.arange(dim, 0, -1)
    Q, _ = np.linalg.qr(Y)
    direction = np.sign(s1 - s0)
    while abs(s - s1) > 1e-12:
        s2 = s + direction * min(abs(s1 - s), chunk)
        f = lambda t, y: (rhs(t, y.reshape(dim, 2))).reshape(-1)
        sol = solve_ivp(f, [s, s2], Q.reshape(-1), method="DOP853", rtol=rtol, atol=atol)
        Y = sol.y[:, -1].reshape(dim, 2)
        Q, Rm = np.linalg.qr(Y)
        # positive real diagonal
        d = np.diag(Rm); ph = d / np.abs(d); Q = Q * ph[None, :]
        s = s2
    return Q

def Dfun(Wv, LL=6.0, theta=0.5, S=None):
    lamv = Wv * Wv
    e = cmath.exp(1j * theta)
    mu = (Wv * e).real
    if S is None:
        S = 22.0 / abs(mu)
    chunk = 6.0 / abs(mu)
    rhsR = lambda s, Phi: e * (M4(s * e, lamv, LL, 1.0, 0.0) @ Phi)
    QR = frame(rhsR, S, 0.0, 4, chunk=chunk)
    rhsL = lambda s, Phi: e * (M4(s * e, lamv, LL, 1.0, 0.0) @ Phi)
    QL = frame(rhsL, -S, 0.0, 4, chunk=chunk)
    return np.linalg.det(np.hstack([QL, QR]))

if __name__ == "__main__":
    t0 = time.time()
    # QNM: omega = 1.74 - 0.305 i -> W = -i omega
    om = 1.74 - 0.305j
    W0 = -1j * om
    print("D at published omega:", Dfun(W0), time.time() - t0)
    for dw in (0.0, 0.05, 0.1, 0.2):
        print(dw, abs(Dfun(W0 + dw)))
