"""dev: polar shooting (real W) for the black-universe members and the Ellis wormhole"""
import math, sys, os, time
import numpy as np
os.environ.setdefault("NUMBA_CACHE_DIR", "/tmp/nm_i218_numba")
from numba import njit
from scipy.integrate import ode
from scipy.optimize import brentq
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import stability as st
from coef_gen import m4_entries, m3_entries, g3_entries
m4n = njit(m4_entries); m3n = njit(m3_entries); g3n = njit(g3_entries)

@njit
def Aval(r, c, K):
    if r > 5.0:
        u = 1.0 / r; u2 = u * u
        s = 0.0; term = u; sg = 1.0
        for k in range(0, 14):
            s += sg * 2.0 * term / ((2 * k + 1) * (2 * k + 3))
            term *= u2; sg = -sg
        return 1.0 - K * s
    return 1.0 + c * (r * r + 1.0) + K * (r + (r * r + 1.0) * math.atan(r))

@njit
def Apval(r, c, K):
    if r > 5.0:
        u = 1.0 / r; u2 = u * u
        # d/dr of -K * sum_k (-1)^k 2 u^(2k+1)/((2k+1)(2k+3)) , du/dr = -u^2
        s = 0.0; term = u2; sg = 1.0
        for k in range(0, 14):
            s += sg * 2.0 * term / (2 * k + 3)
            term *= u2; sg = -sg
        return K * s
    return 2.0 * c * r + 2.0 * K * (1.0 + r * math.atan(r))

@njit
def rhs4(rho, y, lam, L, c, K):
    As = Aval(rho, c, K); A1 = Apval(rho, c, K)
    m = m4n(rho, lam, L, As, A1)
    out = np.empty(8)
    for col in range(2):
        for i in range(4):
            s = 0.0
            for j in range(4):
                s += m[i * 4 + j] * y[j * 2 + col]
            out[i * 2 + col] = s
    return out

@njit
def rhs4_hz(z, y, lam, L, c, K, rh):
    # variables (H0, Pi, K, Ft) with F = Ft / z
    rho = rh + z
    As = Aval(rho, c, K); A1 = Apval(rho, c, K)
    m = m4n(rho, lam, L, As, A1)
    out = np.empty(8)
    t = np.array([1.0, 1.0, 1.0, 1.0 / z])
    for col in range(2):
        for i in range(4):
            s = 0.0
            for j in range(4):
                s += m[i * 4 + j] * t[j] / t[i] * y[j * 2 + col]
            if i == 3:
                s += y[i * 2 + col] / z
            out[i * 2 + col] = s
    return out

@njit
def rhs3(rho, y, lam, c, K):
    As = Aval(rho, c, K); A1 = Apval(rho, c, K)
    m = m3n(rho, lam, As, A1)
    out = np.empty(3)
    for i in range(3):
        s = 0.0
        for j in range(3):
            s += m[i * 3 + j] * y[j]
        out[i] = s
    return out

@njit
def rhs3_hz(z, y, lam, c, K, rh):
    # variables (H0, Ht, F), H2 = z Ht
    rho = rh + z
    As = Aval(rho, c, K); A1 = Apval(rho, c, K)
    m = m3n(rho, lam, As, A1)
    out = np.empty(3)
    t = np.array([1.0, z, 1.0])
    for i in range(3):
        s = 0.0
        for j in range(3):
            s += m[i * 3 + j] * t[j] / t[i] * y[j]
        if i == 1:
            s -= y[i] / z
        out[i] = s
    return out

def integrate_frame(f, args, s0, s1, Y0, chunk, rtol=1e-10, atol=1e-30):
    """integrate dim x k frame with QR (positive diag) between chunks; f(t, yflat, *args)"""
    dim, k = Y0.shape
    Q, Rm = np.linalg.qr(Y0); Q = Q * np.sign(np.diag(Rm))[None, :]
    s = s0; d = 1.0 if s1 > s0 else -1.0
    solver = ode(f).set_integrator("dop853", rtol=rtol, atol=atol, nsteps=200000)
    while abs(s - s1) > 1e-13:
        s2 = s + d * min(abs(s1 - s), chunk)
        solver.set_initial_value(Q.reshape(-1), s).set_f_params(*args)
        y = solver.integrate(s2)
        if not solver.successful():
            raise RuntimeError("dop853 failed")
        Y = y.reshape(dim, k)
        Q, Rm = np.linalg.qr(Y)
        Q = Q * np.sign(np.diag(Rm))[None, :]
        s = s2
    return Q

# ---------------------------------------------------------------------------------------------- Frobenius
def A_c(r, c, K):
    return 1 + c * (r * r + 1) + K * (r + (r * r + 1) * np.arctan(r))
def Ap_c(r, c, K):
    return 2 * c * r + 2 * K * (1 + r * np.arctan(r))

def taylor_S(entries, nd, tmat_fun, c, rh, lam, extra, nterm=14, rad=0.35, Npts=128):
    """Taylor coefficients of S(z) = z M'(z), M' = T^-1 M T - T^-1 T' , via FFT on a circle of radius rad around rh"""
    K = -2 * c / math.pi
    th = 2 * np.pi * np.arange(Npts) / Npts
    Sv = np.empty((Npts, nd, nd), dtype=complex)
    for i in range(Npts):
        z = rad * np.exp(1j * th[i]); r = rh + z
        M = np.array(entries(r, lam, *extra, A_c(r, c, K), Ap_c(r, c, K)), dtype=complex).reshape(nd, nd)
        Sv[i] = tmat_fun(M, z)
    C = np.fft.fft(Sv, axis=0) / Npts
    return [C[n] / rad**n for n in range(nterm)]

def S4(M, z):
    t = np.array([1, 1, 1, 1 / z]); M2 = M * t[None, :] / t[:, None]; M2[3, 3] += 1 / z
    return z * M2
def S3(M, z):
    t = np.array([1, z, 1]); M2 = M * t[None, :] / t[:, None]; M2[1, 1] -= 1 / z
    return z * M2

def frob_vec(C, s, z0, nmax=10, nrm_idx=2):
    nd = C[0].shape[0]
    w, V = np.linalg.eig(C[0]); j = np.argmin(abs(w - s)); a0 = V[:, j]
    a0 = a0 / a0[nrm_idx]
    a = [a0]
    for n in range(1, nmax + 1):
        rhs = sum(C[k] @ a[n - k] for k in range(1, n + 1))
        sol = np.linalg.lstsq((s + n) * np.eye(nd) - C[0], rhs, rcond=1e-12)[0]
        a.append(sol)
    v = sum(a[n] * z0**n for n in range(nmax + 1)) * z0**s
    dv = sum(a[n] * (s + n) * z0**(n - 1) for n in range(nmax + 1)) * z0**s
    return v.real, w
