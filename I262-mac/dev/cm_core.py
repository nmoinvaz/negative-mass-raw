#!/usr/bin/env python3
"""cm_core: mpmath core for the c = -1 black universe (#262): background, Frobenius series of the Y equation at W = w K,
Taylor-step integrator of the Y equation in rho (any real rho != 0; the equation is real-analytic there).
Y'' = (2/rho - A'/A) Y' + (1/R^4 - A'/(A rho R^2) - 2/(A R^2) + W^2/A^2) Y,  A = -rho^2 + K (rho + R^2 arctan rho), K = 2/pi (c = -1)."""
import mpmath as mp


def setup(dps=50):
    mp.mp.dps = dps
    return mp.mpf(2) / mp.pi


# ---- truncated power series (lists of mpf) ----
def s_mul(a, b, n):
    out = [mp.mpf(0)] * n
    for i, ai in enumerate(a[:n]):
        if ai == 0:
            continue
        for j, bj in enumerate(b[:n - i]):
            out[i + j] += ai * bj
    return out


def s_inv(a, n):
    out = [mp.mpf(0)] * n
    out[0] = 1 / a[0]
    for m in range(1, n):
        acc = mp.mpf(0)
        for j in range(1, min(m, len(a) - 1) + 1):
            acc += a[j] * out[m - j]
        out[m] = -acc / a[0]
    return out


def s_add(a, b, n):
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]


def s_scale(a, c, n):
    return [c * (a[i] if i < len(a) else 0) for i in range(n)]


def s_der(a):
    return [i * a[i] for i in range(1, len(a))]


# ---- background series at rho = 0: A = -rho^2 + K (rho + (1+rho^2) T), T = sum (-1)^n rho^(2n+1)/(2n+1) ----
def bg_series0(K, n):
    T = [mp.mpf(0)] * (n + 2)
    for m in range(0, n + 2):
        if 2 * m + 1 < n + 2:
            T[2 * m + 1] = mp.mpf((-1) ** m) / (2 * m + 1)
    R2 = [mp.mpf(1), mp.mpf(0), mp.mpf(1)]
    A = s_mul(R2, T, n + 2)
    A = [K * x for x in A]
    A[1] += K
    A[2] -= 1
    return A[:n + 2]


def frobenius(K, w, g1, N):
    """g_k, k <= N, of Y = rho^s sum g_k rho^k with s = 1/2 (w = 1; g1 given) as numbers (mpf)."""
    s = mp.mpf(1) / 2
    A = bg_series0(K, N + 4)
    a = A[1:]                                           # A = rho * a
    n = N + 3
    ap = s_der(a)
    R2 = [mp.mpf(1), mp.mpf(0), mp.mpf(1)]
    R4 = s_mul(R2, R2, n)
    a2R4 = s_mul(s_mul(a, a, n), R4, n)
    rap = [mp.mpf(0)] + ap[:n - 1]                      # rho a'
    t1 = s_add(a, [-x for x in rap], n)                 # a - rho a'
    C1 = [-x for x in s_mul(s_mul(a, R4, n), t1, n)]
    t2 = s_mul(s_mul(a, s_add(a, rap, n), n), R2, n)
    rho2a2 = [mp.mpf(0), mp.mpf(0)] + s_mul(a, a, n)[:n - 2]
    t3 = [mp.mpf(0)] + s_scale(s_mul(a, R2, n), 2, n)[:n - 1]
    W2R4 = [K * K * w * w * x for x in R4]
    C0 = [-(rho2a2[i] - t2[i] - t3[i] + W2R4[i]) for i in range(n)]
    C2 = a2R4
    I = lambda sig: C2[0] * sig * (sig - 1) + C1[0] * sig + C0[0]
    g = [mp.mpf(1), mp.mpf(g1)]
    chk = g[0] * (C2[1] * s * (s - 1) + C1[1] * s + C0[1])         # order-1 equation must vanish when g1 is free (no logarithm)
    for m in range(2, N + 1):
        tot = mp.mpf(0)
        for k in range(m):
            j = m - k
            tot += g[k] * (C2[j] * (s + k) * (s + k - 1) + C1[j] * (s + k) + C0[j])
        g.append(-tot / I(s + m))
    return g, chk


def Y_frob(g, rho):
    """Y, Y' from the series at rho (real, either sign): |rho|^{1/2} sum g_k rho^k"""
    s = mp.mpf(1) / 2
    ar = abs(rho)
    S = sum(gk * rho ** k for k, gk in enumerate(g))
    dS = sum(k * gk * rho ** (k - 1) for k, gk in enumerate(g) if k > 0)
    Y = ar ** s * S
    Yp = ar ** s * (s * S / rho + dS)
    return Y, Yp


# ---- Taylor stepping in rho ----
def local_series(K, rho0, n):
    """series in h of rho0 + h, R^2, T = arctan, A, A' at rho0 + h, to n terms"""
    r = [rho0, mp.mpf(1)] + [mp.mpf(0)] * (n - 2)
    R2 = [1 + rho0 ** 2, 2 * rho0, mp.mpf(1)] + [mp.mpf(0)] * (n - 3)
    iR2 = s_inv(R2, n)
    T = [mp.atan(rho0)] + [iR2[i - 1] / i for i in range(1, n)]
    A = s_add(s_scale(s_mul(R2, T, n), K, n), s_add(s_scale(r, K, n), [-(x) for x in s_mul(r, r, n)], n), n)
    return r, R2, iR2, T, A


def step(K, w, rho0, Y0, Yp0, h, n=50):
    """one Taylor step of the Y equation from rho0 to rho0 + h; n terms. Returns Y, Y' at rho0 + h"""
    r, R2, iR2, T, A = local_series(K, rho0, n + 2)
    Ap = s_der(A)
    iA = s_inv(A, n + 2)
    ir = s_inv(r, n + 2)
    iR4 = s_mul(iR2, iR2, n + 2)
    AA = s_mul(Ap, iA, n + 2)                                   # A'/A
    P = s_add([2 * x for x in ir], [-x for x in AA], n + 2)
    t1 = s_mul(s_mul(AA, ir, n + 2), iR2, n + 2)
    t2 = s_scale(s_mul(iA, iR2, n + 2), 2, n + 2)
    t3 = s_scale(s_mul(iA, iA, n + 2), K * K * w * w, n + 2)
    Q = [iR4[i] - t1[i] - t2[i] + t3[i] for i in range(n + 2)]
    y = [Y0, Yp0] + [mp.mpf(0)] * n
    for m in range(0, n - 1):
        # (m+2)(m+1) y_{m+2} = sum_j P_j (m-j+1) y_{m-j+1} + Q_j y_{m-j}
        acc = mp.mpf(0)
        for j in range(m + 1):
            acc += P[j] * (m - j + 1) * y[m - j + 1] + Q[j] * y[m - j]
        y[m + 2] = acc / ((m + 2) * (m + 1))
    Y = sum(y[i] * h ** i for i in range(n))
    Yp = sum(i * y[i] * h ** (i - 1) for i in range(1, n))
    return Y, Yp


def frobenius_s(K, w, s, g1, N):
    """general exponent s (1/2 or 3/2 at w = 1). For s = 3/2 the series is unique (g0 = 1). For s = 1/2, g1 is the free resonance."""
    A = bg_series0(K, N + 4)
    a = A[1:]
    n = N + 3
    ap = s_der(a)
    R2 = [mp.mpf(1), mp.mpf(0), mp.mpf(1)]
    R4 = s_mul(R2, R2, n)
    a2R4 = s_mul(s_mul(a, a, n), R4, n)
    rap = [mp.mpf(0)] + ap[:n - 1]
    t1 = s_add(a, [-x for x in rap], n)
    C1 = [-x for x in s_mul(s_mul(a, R4, n), t1, n)]
    t2 = s_mul(s_mul(a, s_add(a, rap, n), n), R2, n)
    rho2a2 = [mp.mpf(0), mp.mpf(0)] + s_mul(a, a, n)[:n - 2]
    t3 = [mp.mpf(0)] + s_scale(s_mul(a, R2, n), 2, n)[:n - 1]
    W2R4 = [K * K * w * w * x for x in R4]
    C0 = [-(rho2a2[i] - t2[i] - t3[i] + W2R4[i]) for i in range(n)]
    C2 = a2R4
    I = lambda sig: C2[0] * sig * (sig - 1) + C1[0] * sig + C0[0]
    s = mp.mpf(s)
    g = [mp.mpf(1)]
    start = 1
    if s == mp.mpf(1) / 2:
        g.append(mp.mpf(g1)); start = 2
    for m in range(start, N + 1):
        tot = mp.mpf(0)
        for k in range(m):
            j = m - k
            tot += g[k] * (C2[j] * (s + k) * (s + k - 1) + C1[j] * (s + k) + C0[j])
        g.append(-tot / I(s + m))
    return g


def Y_frob_s(g, s, rho):
    s = mp.mpf(s)
    ar = abs(rho)
    S = sum(gk * rho ** k for k, gk in enumerate(g))
    dS = sum(k * gk * rho ** (k - 1) for k, gk in enumerate(g) if k > 0)
    return ar ** s * S, ar ** s * (s * S / rho + dS)


def integrate(K, w, rho0, Y0, Yp0, rho1, n=60, frac=mp.mpf("0.25"), hmax=mp.mpf(3), record=None):
    """Taylor-step integration along the real axis from rho0 to rho1 (same sign, no crossing of 0). Steps h = frac * distance to the nearest singularity
    (0 and +-i), at most hmax. record: list of rho values at which to store (Y, Y')."""
    rho = mp.mpf(rho0); Y, Yp = Y0, Yp0
    d = 1 if rho1 > rho0 else -1
    out = {}
    recs = sorted(record or [], reverse=(d < 0))
    ri = 0
    while (rho1 - rho) * d > 0:
        dist = min(abs(rho), mp.sqrt(1 + rho ** 2))
        h = min(frac * dist, hmax, abs(rho1 - rho))
        while ri < len(recs) and (recs[ri] - rho) * d > 0 and (recs[ri] - rho) * d < h:
            h = abs(recs[ri] - rho)
        Y, Yp = step(K, w, rho, Y, Yp, d * h, n=n)
        rho = rho + d * h
        if ri < len(recs) and abs(rho - recs[ri]) < mp.mpf(10) ** (-mp.mp.dps + 5):
            out[recs[ri]] = (Y, Yp); ri += 1
    return rho, Y, Yp, out


# ---- the closed form: Y_ref = R e^{kappa x}, e^{kappa x} = |rho|^{1/2} exp(H(rho)), H = int_0^rho (K/A - 1/(2 rho')) d rho' ----
def h_series(K, N=80):
    """Taylor coefficients h_k of h(rho) = K/A - 1/(2 rho) = -(sum_{j>=1} a_j rho^{j-1}) / (2 a(rho)),  a = A/rho"""
    A = bg_series0(K, N + 4)
    a = A[1:N + 3]
    num = [-a[j + 1] for j in range(N + 1)]
    ia = s_inv(a, N + 1)
    hs = s_mul(num, ia, N + 1)
    return [x / 2 for x in hs]


_HS = {}


def H_of(K, rho, series_radius=mp.mpf("0.25")):
    """H(rho) = int_0^rho h(rho') d rho', by series for |rho| <= 0.25, else series to 0.25 plus quadrature"""
    key = (mp.mp.dps, K)
    if key not in _HS:
        _HS[key] = h_series(K, 90)
    hs = _HS[key]
    def Hs(r):
        return sum(hk * r ** (k + 1) / (k + 1) for k, hk in enumerate(hs))
    rho = mp.mpf(rho)
    if abs(rho) <= series_radius:
        return Hs(rho)
    sgn = 1 if rho > 0 else -1
    r0 = sgn * series_radius
    Aof = lambda r: -r * r + K * (r + (1 + r * r) * mp.atan(r))
    hf = lambda r: K / Aof(r) - 1 / (2 * r)
    pts = [r0]
    r = abs(r0)
    while r < abs(rho):
        r = min(r * 2, abs(rho)); pts.append(sgn * r)
    return Hs(r0) + mp.quad(hf, pts)


def Yref_closed(K, rho, mut=None):
    """R e^{kappa x} with the normalisation e^{kappa x} = |rho|^{1/2}(1 + O(rho)); mut: None | 'R2coef' | 'kscale' | 'xsign' | 'Rpow'"""
    rho = mp.mpf(rho)
    H = H_of(K, rho)
    R2 = 1 + rho * rho
    kk = 1
    if mut == "R2coef":
        R2 = 1 + mp.mpf("1.01") * rho * rho
    if mut == "kscale":
        kk = mp.mpf("1.01")
    if mut == "xsign":
        kk = -1
    R = mp.sqrt(R2)
    return R * abs(rho) ** (mp.mpf(kk) / 2) * mp.exp(kk * H)
