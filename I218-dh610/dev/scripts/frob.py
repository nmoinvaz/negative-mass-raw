import numpy as np, mpmath as mp, cmath, math, sys
from coef_gen import m4_entries, m3_entries
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")

def A_c(r, c, K):
    return 1 + c * (r * r + 1) + K * (r + (r * r + 1) * np.arctan(r))
def Ap_c(r, c, K):
    return 2 * c * r + 2 * K * (1 + r * np.arctan(r))

def taylor_S4(c, rh, lam, L, nterm=14, rad=0.35):
    """Taylor coefficients C_n of S(z) = z M'(z) for T = diag(1,1,1,1/z) (complex-circle FFT)"""
    K = -2 * c / math.pi
    Npts = 128
    th = 2 * np.pi * np.arange(Npts) / Npts
    zs = rad * np.exp(1j * th)
    Sv = np.empty((Npts, 4, 4), dtype=complex)
    for i, z in enumerate(zs):
        r = rh + z
        M = np.array(m4_entries(r, lam, L, A_c(r, c, K), Ap_c(r, c, K)), dtype=complex).reshape(4, 4)
        t = np.array([1, 1, 1, 1 / z])
        M2 = M * t[None, :] / t[:, None]
        M2[3, 3] += 1 / z
        Sv[i] = z * M2
    C = np.fft.fft(Sv, axis=0) / Npts
    return [C[n] / rad**n for n in range(nterm)]

def frob_series(C, s, nmax, idx_free=None):
    """a_0 eigenvector of C0 for exponent s; recursion (s+n-C0) a_n = sum_{k=1}^n C_k a_{n-k}. returns list a_n and compat residuals"""
    n4 = C[0].shape[0]
    w, V = np.linalg.eig(C[0])
    j = np.argmin(abs(w - s)); a0 = V[:, j]
    a = [a0 / a0[2]]   # normalize by K component (index 2) = 1
    resid = []
    for n in range(1, nmax + 1):
        rhs = sum(C[k] @ a[n - k] for k in range(1, n + 1))
        Mn = (s + n) * np.eye(n4) - C[0]
        sol, res, rk, sv = np.linalg.lstsq(Mn, rhs, rcond=1e-12)
        resid.append(np.linalg.norm(Mn @ sol - rhs) / (np.linalg.norm(rhs) + 1e-300))
        a.append(sol)
    return a, resid, w

if __name__ == "__main__":
    cv = -0.3
    import stability as st
    fam = st.Fam(cv, "R2"); rh = fam.rh; A1v = fam.A1
    lam, L = 0.49, 6.0
    mu = math.sqrt(lam) / A1v
    C = taylor_S4(cv, rh, lam, L)
    print("|C_n| decay:", [round(np.linalg.norm(c_), 3) for c_ in C])
    w = np.linalg.eigvals(C[0]); print("exponents", np.sort_complex(w), "mu", mu)
    for s in (1 + mu, -1 + mu):
        a, resid, _ = frob_series(C, s, 8)
        print("s =", s, "compat residuals", ["%.1e" % r for r in resid])
