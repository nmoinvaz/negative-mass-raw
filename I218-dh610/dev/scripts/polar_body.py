
# ------------------------------------------------------------------------------------------------ planted values (read from their sources)
# [ABCKY23] = Azad, Blazquez-Salcedo, Chew, Kunz, Yeom, PRD 107, 084024 (2023), arXiv:2212.12601, Table 1, row M/r0 = 0 (massless Ellis wormhole), r0 = 1:
# polar quasinormal modes omega r0 = omega_R + i omega_I, e^{-i omega t}; three printed digits.  Tolerances are half a unit of the last printed digit.
PUB_QNM = {2: (1.74, -0.305), 3: (2.95, -0.410), 4: (4.08, -0.449)}
PUB_TOL = (5e-3, 5e-4)
QNM_THETA = 0.5                                                 # contour rotation for the outgoing conditions, rad (needs |arg omega| < theta)
QNM_THETA_L1 = 0.9                                              # the l = 1 mode has arg omega = -0.73
MA = 1.0                                                        # M-AdS/Ellis radial plant: stability.planted_value() ([TS13] table, W^2 a^2 at D = 4)

# ------------------------------------------------------------------------------------------------ kernels
m4n, m3n, g3n = njit(m4_entries), njit(m3_entries), njit(g3_entries)
m4c, m3c, g3c = njit(m4_entries_c), njit(m3_entries_c), njit(g3_entries_c)


@njit
def Aval(r, c, K):
    """A(rho) of the family; for rho > 5 the series 1 - K sum (-1)^k 2 u^(2k+1)/((2k+1)(2k+3)), u = 1/rho, which has no cancellation"""
    if r > 5.0:
        u = 1.0 / r
        u2 = u * u
        s = 0.0
        term = u
        sg = 1.0
        for k in range(14):
            s += sg * 2.0 * term / ((2 * k + 1) * (2 * k + 3))
            term *= u2
            sg = -sg
        return 1.0 - K * s
    return 1.0 + c * (r * r + 1.0) + K * (r + (r * r + 1.0) * math.atan(r))


@njit
def Apval(r, c, K):
    if r > 5.0:
        u = 1.0 / r
        u2 = u * u
        s = 0.0
        term = u2
        sg = 1.0
        for k in range(14):
            s += sg * 2.0 * term / (2 * k + 3)
            term *= u2
            sg = -sg
        return K * s
    return 2.0 * c * r + 2.0 * K * (1.0 + r * math.atan(r))


@njit
def rhs4(rho, y, lam, L, c, K):
    As = Aval(rho, c, K)
    A1 = Apval(rho, c, K)
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
    """variables (H0, Pi, K, Ft), F = Ft/z: Fuchsian at the horizon"""
    rho = rh + z
    As = Aval(rho, c, K)
    A1 = Apval(rho, c, K)
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
    As = Aval(rho, c, K)
    A1 = Apval(rho, c, K)
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
    """variables (H0, Ht, F), H2 = z Ht: Fuchsian at the horizon"""
    rho = rh + z
    As = Aval(rho, c, K)
    A1 = Apval(rho, c, K)
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


@njit
def rhs4c(s, y, e, lam, L):
    """Ellis wormhole (A = 1) along rho = s e, e = exp(i theta): complex W"""
    r = s * e
    m = m4c(r, lam, L, 1.0, 0.0)
    out = np.empty(8, dtype=np.complex128)
    for col in range(2):
        for i in range(4):
            acc = 0j
            for j in range(4):
                acc += m[i * 4 + j] * y[j * 2 + col]
            out[i * 2 + col] = e * acc
    return out


def integrate_frame(f, args, s0, s1, Y0, chunk, rtol, atol=None):
    """dim x k frame from s0 to s1 in chunks (a float length, or a list of nodes); Gram-Schmidt (QR with positive diagonal) between chunks keeps the span
    and the sign continuous in W"""
    dim, k = Y0.shape
    atol = 0.1 * rtol if atol is None else atol            # the frame is orthonormal at the start of each chunk
    Q, Rm = np.linalg.qr(Y0)
    Q = Q * np.sign(np.diag(Rm))[None, :]
    if isinstance(chunk, (list, tuple)):
        nodes = list(chunk)
    else:
        d = 1.0 if s1 > s0 else -1.0
        n = int(math.ceil(abs(s1 - s0) / chunk - 1e-12))
        nodes = [s0 + d * min(i * chunk, abs(s1 - s0)) for i in range(n + 1)]
    solver = ode(f).set_integrator("dop853", rtol=rtol, atol=atol, nsteps=500000)
    for s, s2 in zip(nodes[:-1], nodes[1:]):
        solver.set_initial_value(Q.reshape(-1), s).set_f_params(*args)
        y = solver.integrate(s2)
        if not solver.successful():
            raise RuntimeError("dop853 failed at s = %g" % s)
        Q, Rm = np.linalg.qr(y.reshape(dim, k))
        Q = Q * np.sign(np.diag(Rm))[None, :]
    return Q


def hz_nodes(z0, zend, expo):
    """chunk boundaries z0 g^k near the horizon, with g^expo <= e^20 so that the frame never spans more than 20 e-folds of growth between normalizations"""
    g = math.exp(min(2.0, 20.0 / max(expo, 1.0)))
    nodes = [z0]
    while nodes[-1] * g < zend:
        nodes.append(nodes[-1] * g)
    nodes.append(zend)
    return nodes


# ------------------------------------------------------------------------------------------------ horizon: ingoing Frobenius solutions
def A_c(r, c, K):
    return 1 + c * (r * r + 1) + K * (r + (r * r + 1) * np.arctan(r))


def Ap_c(r, c, K):
    return 2 * c * r + 2 * K * (1 + r * np.arctan(r))


def S4(M, z):
    t = np.array([1, 1, 1, 1 / z])
    M2 = M * t[None, :] / t[:, None]
    M2[3, 3] += 1 / z
    return z * M2


def S3(M, z):
    t = np.array([1, z, 1])
    M2 = M * t[None, :] / t[:, None]
    M2[1, 1] -= 1 / z
    return z * M2


def taylor_S(entries, nd, tfun, c, rh, lam, extra, nterm=16, rad=0.35, npts=128):
    """Taylor coefficients C_n of S(z) = z M'(z) at the horizon, M' = T^-1 M T - T^-1 T' (T = diag(1,1,1,1/z) for l = 2, diag(1,z,1) for l = 1),
    by FFT on a circle of radius rad around rho_h; z M' is analytic at z = 0 (Fuchsian)"""
    K = -2 * c / math.pi
    zs = rad * np.exp(2j * np.pi * np.arange(npts) / npts)
    Sv = np.empty((npts, nd, nd), dtype=complex)
    for i, z in enumerate(zs):
        r = rh + z
        Sv[i] = tfun(np.array(entries(r, lam, *extra, A_c(r, c, K), Ap_c(r, c, K)), dtype=complex).reshape(nd, nd), z)
    C = np.fft.fft(Sv, axis=0) / npts
    return [C[n] / rad**n for n in range(nterm)]


def frob_vec(C, s, z0, nmax, nrm_idx):
    """solution z^s sum a_n z^n at z0: (s + n - C0) a_n = sum_{k=1..n} C_k a_{n-k}; a_0 the eigenvector of C0 for the exponent s with a_0[nrm_idx] = 1;
    at a resonance (s + n an exponent) the singular system is solved in the least-squares sense; returns the vector and the worst relative
    inconsistency of the recursion (a log term would show there)"""
    nd = C[0].shape[0]
    w, V = np.linalg.eig(C[0])
    j = np.argmin(abs(w - s))
    if abs(w[j] - s) > 1e-6:
        raise RuntimeError("Frobenius exponent %g not an eigenvalue of the residue matrix (%s)" % (s, np.round(w, 6)))
    a = [V[:, j] / V[nrm_idx, j]]
    incons = 0.0
    for n in range(1, nmax + 1):
        rhs = sum(C[k] @ a[n - k] for k in range(1, n + 1))
        Mn = (s + n) * np.eye(nd) - C[0]
        sol = np.linalg.lstsq(Mn, rhs, rcond=1e-12)[0]
        incons = max(incons, np.linalg.norm(Mn @ sol - rhs) / (np.linalg.norm(rhs) + 1e-300))
        a.append(sol)
    v = sum(a[n] * z0**n for n in range(nmax + 1)) * z0**s
    return v.real, incons


# ------------------------------------------------------------------------------------------------ polar determinants (real W)
def match_point(fam):
    if fam.rh is None:
        return 0.0
    return 1.0 if fam.rh < 0.5 else fam.rh + 1.0


def far_frame_l2(W, L, fam, rm, p, side):
    lam = W * W
    rfar = max(p["rmax0"], p["rmaxW"] / W)
    Y0 = np.random.RandomState(3 if side > 0 else 4).randn(4, 2)
    return integrate_frame(rhs4, (lam, L, fam.c, fam.K), side * rfar, rm, Y0, 8.0 / W, p["rtol"])


def D_l2(W, fam, p, L=6.0):
    """det[QL | QR] at the matching point: QL the two ingoing (c < 0: horizon; c = 0: left infinity) solutions, QR the two decaying at +infinity"""
    if mutating("L_sign"):
        L = -L                                             # control: attractive angular term
    if mutating("rmax"):
        p = dict(p, rmax0=4.0, rmaxW=0.0)                  # control: far boundary at rho = 4
    rm = match_point(fam)
    QR = far_frame_l2(W, L, fam, rm, p, +1)
    if fam.rh is None:
        QL = far_frame_l2(W, L, fam, rm, p, -1)
    else:
        lam = W * W
        mu = W / fam.A1
        C = taylor_S(m4_entries, 4, S4, fam.c, fam.rh, lam, (L,))
        sg = -1.0 if mutating("hz_out") else 1.0           # control: the outgoing exponents -mu instead of +mu
        v1, i1 = frob_vec(C, 1 + sg * mu, p["z0"], p["nfrob"], 2)
        v2, i2 = frob_vec(C, -1 + sg * mu, p["z0"], p["nfrob"], 2)
        if max(i1, i2) > 1e-6:
            raise RuntimeError("Frobenius recursion inconsistent: %g" % max(i1, i2))
        QL = integrate_frame(rhs4_hz, (lam, L, fam.c, fam.K, fam.rh), p["z0"], rm - fam.rh, np.stack([v1, v2], axis=1), hz_nodes(p["z0"], rm - fam.rh, 1 + abs(mu)), p["rtol"])
        QL = QL.copy()
        QL[3, :] = QL[3, :] / (rm - fam.rh)                # F = Ft / z
    QL, _ = np.linalg.qr(QL)
    QR, _ = np.linalg.qr(QR)
    return float(np.linalg.det(np.hstack([QL, QR])))


def gauge_vec(rho, lam, fam):
    g = np.array(g3n(rho, lam, float(Aval(rho, fam.c, fam.K)), float(Apval(rho, fam.c, fam.K))))
    if mutating("g1_wrong"):
        g = np.array([0.0, 1.0, 0.0])                      # control: a wrong third column (H2 only) in place of the pure-gauge solution
    return g / np.linalg.norm(g)


def D_l1(W, fam, p):
    """det[QL | QR | g] for l = 1: g the pure-gauge solution (xi^theta = sqrt(A)/R), QL, QR the ingoing and decaying solutions"""
    if mutating("rmax"):
        p = dict(p, rmax0=4.0, rmaxW=0.0)
    lam = W * W
    rm = match_point(fam)
    rfar = max(p["rmax0"], p["rmaxW"] / W)
    QR = integrate_frame(rhs3, (lam, fam.c, fam.K), rfar, rm, np.random.RandomState(3).randn(3, 1), 8.0 / W, p["rtol"])
    if fam.rh is None:
        QL = integrate_frame(rhs3, (lam, fam.c, fam.K), -rfar, rm, np.random.RandomState(4).randn(3, 1), 8.0 / W, p["rtol"])
    else:
        mu = W / fam.A1
        C = taylor_S(m3_entries, 3, S3, fam.c, fam.rh, lam, ())
        sg = -1.0 if mutating("hz_out") else 1.0
        v, inc = frob_vec(C, sg * mu, p["z0"], p["nfrob"], 2)
        if inc > 1e-6:
            raise RuntimeError("Frobenius recursion inconsistent: %g" % inc)
        QL = integrate_frame(rhs3_hz, (lam, fam.c, fam.K, fam.rh), p["z0"], rm - fam.rh, v.reshape(3, 1), hz_nodes(p["z0"], rm - fam.rh, 1 + abs(mu)), p["rtol"])
        QL = QL.copy()
        QL[1, :] *= rm - fam.rh                            # H2 = z Ht
        QL = QL / np.linalg.norm(QL)
    return float(np.linalg.det(np.column_stack([QL[:, 0], QR[:, 0], gauge_vec(rm, lam, fam)])))


def find_roots(Dfun, Ws):
    """sign changes of D on the grid Ws (odd-multiplicity roots, refined by Brent) and interior minima of |D| refined by a bounded search: a minimum
    below DIP_RATIO of its neighbors is a root of even multiplicity (a double root, as at the Ellis wormhole, where the two polar fields are degenerate)"""
    D = np.array([Dfun(W) for W in Ws])
    roots = [brentq(Dfun, Ws[i], Ws[i + 1], xtol=1e-14, rtol=1e-13) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])]
    dips = []
    for i in range(1, len(Ws) - 1):
        if abs(D[i]) < abs(D[i - 1]) and abs(D[i]) < abs(D[i + 1]):
            r = minimize_scalar(lambda W: abs(Dfun(W)), bounds=(Ws[i - 1], Ws[i + 1]), method="bounded", options=dict(xatol=1e-12))
            ratio = r.fun / min(abs(D[i - 1]), abs(D[i + 1]))
            dips.append(dict(W=r.x, Dmin=r.fun, ratio=ratio, flagged=bool(ratio < DIP_RATIO)))
    return roots, dips, D


def count_polar(ell, c, res, L=None):
    fam = st.Fam(c, "R2")
    p = RES[res]
    Dfun = (lambda W: D_l2(W, fam, p, 6.0 if L is None else L)) if ell == 2 else (lambda W: D_l1(W, fam, p))
    lo = 3.0 if mutating("scan_range") else W_LO
    Ws = np.exp(np.linspace(math.log(lo), math.log(W_HI), p["nW"]))
    t0 = time.time()
    roots, dips, D = find_roots(Dfun, Ws)
    probes = {("%g" % W): Dfun(W) for W in PROBES}
    return dict(ell=ell, c=c, res=res, rh=fam.rh, A1=fam.A1, n_roots=len(roots) + 2 * sum(d["flagged"] for d in dips), roots=roots, dips=dips,
                sign_changes=len(roots), D_first=float(D[0]), D_last=float(D[-1]), D_absmin=float(np.min(np.abs(D))), probes=probes,
                W_lo=lo, W_hi=W_HI, nW=p["nW"], seconds=time.time() - t0, mutate=sorted(MUT))


# ------------------------------------------------------------------------------------------------ polar quasinormal modes (complex W), Ellis wormhole
def frame_c(rhs, args, s0, s1, dim, k, chunk, seed):
    rng = np.random.RandomState(seed)
    Q, _ = np.linalg.qr(rng.randn(dim, k) + 1j * rng.randn(dim, k))
    s = s0
    d = np.sign(s1 - s0)
    while abs(s - s1) > 1e-12:
        s2 = s + d * min(abs(s1 - s), chunk)
        sol = solve_ivp(lambda t, y: rhs(t, y, *args), [s, s2], Q.reshape(-1), method="DOP853", rtol=1e-11, atol=1e-30)
        Q, Rm = np.linalg.qr(sol.y[:, -1].reshape(dim, k))
        Q = Q * (np.diag(Rm) / np.abs(np.diag(Rm)))[None, :]
        s = s2
    return Q


def D_qnm_l2(Wc, L, theta=QNM_THETA):
    """Ellis polar determinant at complex W = -i omega; the radial coordinate is rotated, rho = s e^{i theta}, so that both outgoing conditions
    (decay of exp(-+W rho)) are decaying solutions along the contour; matching at rho = 0"""
    if mutating("qnm_L"):
        L = L + 1.0                                        # control: wrong angular eigenvalue
    e = np.exp(1j * theta)
    mu = (Wc * e).real
    S = 22.0 / abs(mu)
    chunk = 6.0 / abs(mu)
    args = (e, Wc * Wc, L)
    QR = frame_c(rhs4c, args, S, 0.0, 4, 2, chunk, 3)
    QL = frame_c(rhs4c, args, -S, 0.0, 4, 2, chunk, 4)
    return complex(np.linalg.det(np.hstack([QL, QR])))


def qnm_l2(ell, start=None):
    L = ell * (ell + 1.0)
    om0 = complex(*PUB_QNM[ell]) if start is None else start
    f = lambda v: (lambda d: [d.real, d.imag])(D_qnm_l2(-1j * (v[0] + 1j * v[1]), L))
    r = root(f, [om0.real, om0.imag], tol=1e-11)
    return complex(r.x[0], r.x[1]), bool(r.success), float(np.hypot(*f(r.x)))


@njit
def rhs3c(s, y, e, lam):
    """Ellis wormhole, polar l = 1 system (H0, H2, F) along rho = s e"""
    r = s * e
    m = m3c(r, lam, 1.0, 0.0)
    out = np.empty(3, dtype=np.complex128)
    for i in range(3):
        acc = 0j
        for j in range(3):
            acc += m[i * 3 + j] * y[j]
        out[i] = e * acc
    return out


@njit
def rhs_schr(s, y, e, lam, kind):
    """Z'' = (V + lam) Z along rho = s e; kind 0: V = 2/R^2 - 3/R^4 ([ABCKY23] (53) at L = 2), kind 1: V = 2/R^2 + 1/R^4 (test scalar, l = 1)"""
    r = s * e
    R2 = r * r + 1.0
    V = 2.0 / R2 - 3.0 / (R2 * R2) if kind == 0 else 2.0 / R2 + 1.0 / (R2 * R2)
    return np.array([e * y[1], e * (V + lam) * y[0]], dtype=np.complex128)


def D_qnm_l1(Wc, theta=QNM_THETA_L1):
    """Ellis polar l = 1 determinant det[QL | QR | g] at complex W, rotated contour as in D_qnm_l2"""
    e = np.exp(1j * theta)
    mu = (Wc * e).real
    S, chunk = 22.0 / abs(mu), 6.0 / abs(mu)
    args = (e, Wc * Wc)
    QR = frame_c(rhs3c, args, S, 0.0, 3, 1, chunk, 3)
    QL = frame_c(rhs3c, args, -S, 0.0, 3, 1, chunk, 4)
    g = np.array(g3c(0.0, Wc * Wc, 1.0, 0.0), dtype=complex)
    return complex(np.linalg.det(np.column_stack([QL[:, 0], QR[:, 0], g / np.linalg.norm(g)])))


def D_qnm_schr(Wc, kind, theta=QNM_THETA_L1):
    """the independent 1D code: Z'' = (V + W^2) Z, outgoing at both ends; shares nothing with the polar system"""
    if mutating("l1_pot"):
        kind = 1                                           # control: the test-scalar l = 1 potential in place of the master equation at L = 2
    e = np.exp(1j * theta)
    mu = (Wc * e).real
    S, chunk = 22.0 / abs(mu), 6.0 / abs(mu)
    args = (e, Wc * Wc, kind)
    QR = frame_c(rhs_schr, args, S, 0.0, 2, 1, chunk, 3)
    QL = frame_c(rhs_schr, args, -S, 0.0, 2, 1, chunk, 4)
    return complex(QL[0, 0] * QR[1, 0] - QL[1, 0] * QR[0, 0])


def qnm_root(Dfun, om0):
    f = lambda v: (lambda d: [d.real, d.imag])(Dfun(-1j * (v[0] + 1j * v[1])))
    r = root(f, [om0.real, om0.imag], tol=1e-11)
    return complex(r.x[0], r.x[1]), bool(r.success)


def fd_bound_states(Lv, X=400.0, N=160001, k=6):
    """bound states W of -Z'' + V Z = -W^2 Z, V = L/R^2 - 3/R^4, finite differences on two grids with Richardson extrapolation in h^2 (the other 1D code)"""
    from scipy.linalg import eigh_tridiagonal
    out = []
    for n in (N, 2 * N - 1):
        x = np.linspace(-X, X, n)
        h = x[1] - x[0]
        V = Lv / (x**2 + 1) - 3 / (x**2 + 1)**2
        out.append(eigh_tridiagonal(2 / h**2 + V, -np.ones(n - 1) / h**2, select="i", select_range=(0, k - 1), eigvals_only=True))
    lam = (4 * out[1] - out[0]) / 3
    return [math.sqrt(-e) for e in lam if e < -1e-3]


def cscale_qnm(Vf, near, theta=1.1, X=60.0, N=20000):
    """the quasinormal mode of Z'' + (omega^2 - V) Z = 0 nearest to `near`, as a discrete eigenvalue of the complex-scaled operator
    -e^{-2 i theta} d^2/ds^2 + V(s e^{i theta}) on s in [-X, X] (finite differences, Dirichlet ends; shift-invert Arnoldi), Richardson in h^2 from N and 2N;
    the other independent 1D code (an eigenvalue problem, no shooting)"""
    import scipy.sparse as sps
    from scipy.sparse.linalg import eigs
    lam = []
    for n in (N, 2 * N):
        s = np.linspace(-X, X, n + 2)[1:-1]
        h = s[1] - s[0]
        ph = np.exp(-2j * theta)
        H = sps.diags([-np.ones(n - 1) / h**2 * ph, 2 / h**2 * ph + Vf(s * np.exp(1j * theta)), -np.ones(n - 1) / h**2 * ph], [-1, 0, 1], format="csc")
        w, _ = eigs(H, k=1, sigma=near**2, which="LM")
        lam.append(w[0])
    return np.sqrt((4 * lam[1] - lam[0]) / 3)
