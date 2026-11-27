

# ------------------------------------------------------------------------------------------------ M-AdS wormholes (c > 0): radial modes
# The radial equation, the gauge delta phi = 0, the right-hand condition and the analytic throat crossing are those of stability.py (#212).  New: the
# AdS end rho -> -infinity, where A ~ 2 c rho^2 and Y -> alpha + beta rho; Dirichlet (no source, Psi = -sqrt2 Y/rho -> 0) is beta = 0, the series
# Y = 1 + y2/rho^2 + y4/rho^4 + ... (sympy, polar.md), integrated toward the throat.
def ads_start(fam, W, p):
    c = fam.c
    r0 = -p["ads"] * max(100.0, 400.0 * W / c, 100.0 / math.sqrt(c))
    if mutating("ads_bc"):
        return r0, r0, 1.0                                 # control: the non-normalizable solution Y = rho
    y2 = (W**2 - 4 * c**2 - 4 * c) / (24 * c**2)
    y4 = (W**4 - 40 * W**2 * c + 272 * c**4 + 416 * c**3 + 24 * c**2 * (4 - 3 * W**2)) / (1920 * c**4)
    return r0, 1 + y2 / r0**2 + y4 / r0**4, -2 * y2 / r0**3 - 4 * y4 / r0**5


def rhs_rho(fam, W):
    e = fam.eps

    def f(r, s):
        Y, Yr = s
        A = fam.A(r)
        Ap = fam.Ap(r)
        R2 = r * r + 1
        P1 = -2 * e / (r * R2) + 2 * r / R2 - Ap / A
        P0 = -e / R2**2 + e * Ap / (A * r * R2) - 2 / (A * R2)
        return [Yr, P1 * Yr + P0 * Y + W * W * Y / A**2]
    return f


def left_ads(fam, W, rm, p):
    r0, Y, Yp = ads_start(fam, W, p)
    d, rtol = p["delta"], p["rtol"]
    s = np.array([Y, Yp])
    s /= np.hypot(*s)
    f = rhs_rho(fam, W)
    r = r0
    while r < -d - 1e-12:
        r2 = min(-d, r + max(5.0, abs(r) * 0.5))
        sol = solve_ivp(f, [r, r2], s, method="DOP853", rtol=rtol, atol=[1e-30, 1e-30])
        s = sol.y[:, -1]
        s /= np.hypot(*s)
        r = r2
    sol = solve_ivp(lambda th, y: st.rhs_arc(fam, W, d)(th, y), [np.pi, 0.0], [s[0] + 0j, s[1] + 0j], method="DOP853", rtol=rtol, atol=1e-30)
    Yc, Yrc = sol.y[:, -1]
    flag = abs(Yc.imag) / abs(Yc)                         # monodromy test: no logarithm at the throat
    s0 = np.array([d, Yc.real, (Yrc * fam.A(d)).real])
    s0[1:] /= np.hypot(s0[1], s0[2])
    stop = st.make_ev(lambda x, ss: ss[0] - rm, 1, True)
    s, _, _ = st.run_chunks(st.rhs_x(fam, W), s0, +1, W, rtol, [1e-12, 1e-30, 1e-30], stop, None)
    return s[0], s[1], s[2], flag


def mads_mismatch(fam, W, p, flags=None):
    rm = 1.0
    _, Yl, Ylx, flag = left_ads(fam, W, rm, p)
    if flags is not None:
        flags.append(flag)
    fam.res = dict(rtol=p["rtol"], rmax0=p["rmax0"], rmaxW=p["rmaxW"], delta=p["delta"])
    _, Yr, Yrx, _ = st.right_solution(fam, W, rm)
    return Yl * Yrx - Ylx * Yr


def count_mads(c, res):
    fam = st.Fam(c, "R2")
    p = RES[res]
    lo = 3.0 if mutating("scan_range") else W_LO
    Ws = np.exp(np.linspace(math.log(lo), math.log(W_HI_M), p["nWm"]))
    t0 = time.time()
    flags = []
    D = np.array([mads_mismatch(fam, W, p, flags) for W in Ws])
    roots = [brentq(lambda W: mads_mismatch(fam, W, p, flags), Ws[i], Ws[i + 1], xtol=1e-13, rtol=1e-12) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])]
    return dict(c=c, res=res, n_roots=len(roots), roots=[dict(W=w, W2=w * w) for w in roots], sign_changes=len(roots), D_first=float(D[0]), D_last=float(D[-1]),
                monodromy_imag_max=float(max(flags)), W_lo=lo, W_hi=W_HI_M, nW=p["nWm"], seconds=time.time() - t0, mutate=sorted(MUT))


def spectral_mads(c, N, X):
    """Chebyshev collocation of the Y-form Y_xx = Cx Y_x + Dx Y + lam Y on x in [x_L, X] (x_L the finite AdS end): Neumann at x_L (the Dirichlet
    solution Y = 1 + O(s^2)), Y = 0 at X; rho(x) by inversion of x(rho).  Shares with the shooting code the background A and the coefficients of the Y-form,
    nothing of the AdS series, the throat crossing, the matching or the root search."""
    from scipy.integrate import quad
    from scipy.linalg import eig
    fam = st.Fam(c, "R2")
    xL = -quad(lambda r: 1 / fam.A(r), -np.inf, 0, epsabs=1e-14, epsrel=1e-13, limit=400)[0]
    D, xc = st.cheb(N)
    xs = X + (xc - 1.0) * (X - xL) / 2                    # xc = 1 -> X, xc = -1 -> xL
    rho = np.empty(N + 1)
    for j in range(N + 1):
        xj = xs[j]
        if j == N:
            rho[j] = -np.inf
        elif xj >= 0:
            rho[j] = brentq(lambda r: quad(lambda q: 1 / fam.A(q), 0, r, epsabs=1e-14, epsrel=1e-13)[0] - xj, 0, xj + 10, xtol=1e-14) if xj > 0 else 0.0
        else:
            s = xj - xL
            rho[j] = brentq(lambda r: quad(lambda q: 1 / fam.A(q), -np.inf, r, epsabs=1e-16, epsrel=1e-12, limit=400)[0] - s, -1e12, -1e-9, xtol=1e-14)
    rho[np.abs(rho) < 1e-6] = 1e-6                        # a node at the throat: its Y-form coefficients have the removable pole 1/rho
    A = np.empty(N + 1)
    Ap = np.empty(N + 1)
    for j in range(N):
        A[j], Ap[j] = fam.A(rho[j]), fam.Ap(rho[j])
    A[N], Ap[N] = np.inf, np.inf
    Cx = np.zeros(N + 1)
    Dx = np.zeros(N + 1)
    for j in range(N):
        Cx[j], Dx[j] = st.coef_x(fam, rho[j], A[j], A[j] / rho[j], Ap[j])
    D1 = D * 2 / (X - xL) * -1.0                           # d/dx = (2/(X - xL)) d/dxc, xc decreasing with x
    D1 = D / ((X - xL) / 2)
    D2 = D1 @ D1
    sgn = -1.0 if mutating("spec_sign") else 1.0
    Aop = np.zeros((N + 1, N + 1))
    Bop = np.zeros((N + 1, N + 1))
    for j in range(1, N):
        Aop[j, :] = D2[j, :] - Cx[j] * D1[j, :] - sgn * Dx[j] * np.eye(N + 1)[j, :]
        Bop[j, j] = 1.0
    Aop[0, 0] = 1.0                                        # Y(X) = 0
    Aop[N, :] = D1[N, :]                                   # Y_x(x_L) = 0
    ev = eig(Aop, Bop, right=False)
    ev = ev[np.isfinite(ev)]
    return ev[(ev.real > 1e-4) & (ev.real < 100.0)]


SPEC = {"S-A": dict(N=240, X=40.0, tol=2e-3), "S-B": dict(N=360, X=60.0, tol=2e-4)}
SPEC_CMIN = 0.01                                           # below it the AdS end is at |rho| > 70 and the finite domain is not resolved (development: 6e-2 at c = 1e-4):
                                                           # there the count only is compared, the rates are reported


def spectral_command(d):
    ok_all = True
    rows = {}
    for fn in sorted(glob.glob(d + "/mads_*_R2.json")):
        o = json.load(open(fn))
        rows[o["c"]] = o
    for c in sorted(rows):
        ref = sorted(r["W"] for r in rows[c]["roots"])
        for which in ("S-A", "S-B"):
            ev = spectral_mads(c, SPEC[which]["N"], SPEC[which]["X"])
            realpos = sorted(e.real for e in ev if abs(e.imag) < 1e-6 * abs(e) and e.real < W_HI_M**2)
            cplx = [e for e in ev if abs(e.imag) >= 1e-6 * abs(e)]
            rel = [abs(math.sqrt(a) - b) / b for a, b in zip(realpos, ref)]
            tol = SPEC[which]["tol"] if c >= SPEC_CMIN else float("inf")
            ok = len(realpos) == len(ref) and not cplx and all(r <= tol for r in rel)
            ok_all &= ok
            print(("PASS  " if ok else "FAIL  ") + f"S6 spectral {which} c = {c:g}: eigenvalues with Re lam > 1e-4: real {len(realpos)} (shooting {len(ref)}), complex {len(cplx)}, "
                  f"|dW|/W = {['%.2e' % r for r in rel]} (declared <= {SPEC[which]['tol'] if c >= SPEC_CMIN else 'n/a, c < %g' % SPEC_CMIN})", flush=True)
    return ok_all


# ------------------------------------------------------------------------------------------------ planted cases
# P3 (ruling of the coordinator, 2026-11-27): no published number for polar l = 1.  The derived l = 1 system at c = 0 has the quasinormal mode of
# [ABCKY23]'s master equation (52), (53) at L = 2 (the two are isospectral, Darboux partners, polar_derive.py D6e, D6f), computed by an independent 1D code.
L1_START = complex(0.6814, -0.6177)                             # starting point of the root searches (complex-scaling development run: 0.681429 - 0.617763i)
L1_TOL = 1e-7                                                   # |omega_derived - omega_master|, both by shooting
L1_TOL_FD = 1e-8                                                # against the finite-difference eigenvalue code (theta = 1.1, X = 60, N = 20000, Richardson)
# P4: the Ellis wormhole at the unphysical L = -1: the decoupled master equation has bound states of known W (finite differences); each is a double
# root of the polar determinant (two identical fields), found as a flagged dip of |D|.
P4_L, P4_WLO, P4_TOL = -1.0, 0.2, 5e-5                          # relative tolerance on W
# P5: the M-AdS radial mode at c -> 0+: W^2(c) - W^2_Ellis = a1 c + a2 c^2 + ..., quadratic fit through c = 1e-4, 1e-3, 1e-2
P5_C, P5_TOL = (1e-4, 1e-3, 1e-2), 1e-8


def planted_command():
    ok_all = True

    def line(tag, ok, msg):
        nonlocal ok_all
        ok_all &= ok
        print(("PASS  " if ok else "FAIL  ") + tag + ": " + msg, flush=True)
    t0 = time.time()
    for ell in (2, 3, 4):
        om, conv, res_ = qnm_l2(ell)
        pr, pi = PUB_QNM[ell]
        ok = conv and abs(om.real - pr) <= PUB_TOL[0] and abs(om.imag - pi) <= PUB_TOL[1]
        line("P2 Ellis polar l = %d quasinormal mode against [ABCKY23] Table 1 (M = 0)" % ell, ok,
             "omega = %.6f %+.6fi (printed %.2f %+.3fi), |dRe| = %.1e, |dIm| = %.1e (declared <= %g, %g), |D| at the root %.1e (%.0f s)" %
             (om.real, om.imag, pr, pi, abs(om.real - pr), abs(om.imag - pi), PUB_TOL[0], PUB_TOL[1], res_, time.time() - t0))
    om1, c1 = qnm_root(D_qnm_l1, L1_START)
    om2, c2 = qnm_root(lambda W: D_qnm_schr(W, 0), L1_START)
    line("P3a Ellis polar l = 1 quasinormal mode of the derived system against the master equation (52), (53) of [ABCKY23] at L = 2 (1D shooting)",
         c1 and c2 and abs(om1 - om2) <= L1_TOL, "derived %.9f %+.9fi, master %.9f %+.9fi, |difference| = %.1e (declared <= %g) (%.0f s)" %
         (om1.real, om1.imag, om2.real, om2.imag, abs(om1 - om2), L1_TOL, time.time() - t0))
    Vm = (lambda r: 2 / (r * r + 1) + 1 / (r * r + 1)**2) if mutating("l1_pot") else (lambda r: 2 / (r * r + 1) - 3 / (r * r + 1)**2)
    om3 = cscale_qnm(Vm, L1_START)
    line("P3b the same against the complex-scaled eigenvalue problem for the master equation at L = 2 (finite differences, Richardson in h^2)", abs(om1 - om3) <= L1_TOL_FD,
         "derived %.9f %+.9fi, eigenvalue code %.9f %+.9fi, |difference| = %.1e (declared <= %g)" % (om1.real, om1.imag, om3.real, om3.imag, abs(om1 - om3), L1_TOL_FD))
    ref = fd_bound_states(P4_L)
    ref = [w for w in ref if w >= P4_WLO]
    fam = st.Fam(0.0, "R2")
    p = RES["R1"]
    Ws = np.exp(np.linspace(math.log(P4_WLO), math.log(W_HI), p["nW"]))
    roots, dips, _ = find_roots(lambda W: D_l2(W, fam, p, P4_L), Ws)
    found = sorted(d["W"] for d in dips if d["flagged"])
    ok = len(found) == len(ref) and not roots and all(abs(a - b) / b <= P4_TOL for a, b in zip(found, sorted(ref)))
    line("P4 Ellis, L = %g (unphysical): double roots of the polar determinant against the bound states of the master equation (finite differences)" % P4_L, ok,
         "found %s, finite differences %s, sign changes %d (declared relative <= %g)" % (["%.6f" % w for w in found], ["%.6f" % w for w in sorted(ref)], len(roots), P4_TOL))
    ref2 = float(st.planted_value())
    ds = []
    for c in P5_C:
        o = count_mads(c, "R1")
        ds.append(o["roots"][0]["W2"] - ref2 if o["n_roots"] == 1 else float("nan"))
    a0 = np.linalg.solve(np.vander(np.array(P5_C), 3, increasing=True), np.array(ds))[0]
    line("P5 M-AdS radial mode as c -> 0+ against the Ellis value %s (stability.py planted value)" % st.planted_value(), all(np.isfinite(ds)) and abs(a0) <= P5_TOL,
         "W^2(c) - W^2_Ellis = %s at c = %s; quadratic extrapolation to c = 0: %.2e (declared <= %g) (%.0f s)" % (["%.6e" % x for x in ds], P5_C, a0, P5_TOL, time.time() - t0))
    return ok_all
