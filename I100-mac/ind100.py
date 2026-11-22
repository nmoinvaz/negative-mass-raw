"""
Coordinator's independent check of #100: the boundary term of item 6's identity on psi^4 delta,
    B = (1/4 pi) lim_{R -> inf} F(R),   F(R) = oint sqrt(g) V^mu n_mu dA_flat = oint psi^4 V^a n_a R^2 dOmega,
(sqrt(g) = psi^6, V^mu = psi^-2 V^a) with V^i = Re<eps, nabla_i eps - g^i D eps> - (1/2) P_ij xi^j, P = K - delta tr K,
xi^j = <eps, g^0 g^j eps>, nabla_i = e_i + (1/4) omega_jk(e_i) g^j g^k, e_i = psi^-2 d_i, against E |eps_0|^2 - P.xi_0.

Shares no code with weitzenbock_boundary.py, weitzenbock_conf.py or conventions.py, and takes a different route:
no series in 1/r and no symbolic sphere moments. Explicit data with fixed numbers are built in sympy in Cartesian
coordinates (r = sqrt(x^2 + y^2 + z^2)), omega comes from the Koszul formula of the frame commutators (as in the
coordinator's ind130.py, retyped), and everything is evaluated in float64: F(R) by Gauss-Legendre (in cos theta) x
trapezoid (in phi) quadrature at R = 100 * 2^k, k = 0..5, and B by fitting F = B + sum_{k=1..5} c_k / R^k exactly
through the six values. A second fit through R = 150 * 2^k gives the extrapolation's spread. E and P_j are also
computed from the ADM surface integrals of the same data the same way. The gammas are mass_bounds.md's.
Usage: python ind100.py [--mutate=Vsign|Dhalf|omega]

Data (numbers fixed below, drawn once with seed 100): m = 0.7, P = (0.3, -0.5, 0.4), psi = 1 + m/2r + (d.n)/r^2 +
q(n)/r^3; K (frame) = psi^-6 (K_BY + K3(n)/r^3), K_BY = (3/2r^2)[P_i n_j + P_j n_i - (delta_ij - n_i n_j) P.n], K3 a
symmetric matrix of degree-1 polynomials in n; eps = eps_0 + eps_1(n)/r + eps_2(n)/r^2, eps_1 and eps_2 complex
polynomials in n of degree 2 and 1.

Criteria, fixed before the first run (tol: |difference| < 1e-8 max(1, |target|); spread: the two fits within 1e-8):
  C0  Schwarzschild: psi = 1 + m/2r, K = 0, eps = eps_0 (|eps_0| arbitrary): B = m |eps_0|^2.
  C1  psi with the d and q terms, K = 0, eps = eps_0: B = m |eps_0|^2.
  C2  ADM integrals of the general data: E = m and P_ADM = P within tol.
  C3  general data (all of the above): B = E |eps_0|^2 - P.xi_0, with E and P_ADM from C2's integrals.
  C4  eps_0 the unit eigenvector of sum_j Phat_j g^0 g^j with eigenvalue +1 (so xi_0 = P/|P|), eps_1 and eps_2 as in
      C3: B = m - |P|.
  Every B is also required to have spread below 1e-8 (else the criterion fails).
Mutations (each must make the script exit 1):
  Vsign   +(1/2) P_ij xi^j in V: C3 and C4 must fail.
  Dhalf   V^i = Re<eps, nabla_i eps - (1/2) g^i D eps> - ...: C3 must fail.
  omega   -omega_jk in nabla: C0 must fail.
Exit 1 if any criterion fails.
"""
import sys, time
import numpy as np
import sympy as sp

mut = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), None)
assert mut in (None, 'Vsign', 'Dhalf', 'omega')
T0 = time.time()
x, y, z = X = sp.symbols('x y z', real=True)
r = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
nn = [x / r, y / r, z / r]
I = 1j
s1 = np.array([[0, 1], [1, 0]], complex); s2 = np.array([[0, -I], [I, 0]]); s3 = np.array([[1, 0], [0, -1]], complex)
Z2 = np.zeros((2, 2), complex)
g0 = I * np.diag([1, 1, -1, -1]).astype(complex)
gs = [np.block([[Z2, sj], [sj, Z2]]) for sj in (s1, s2, s3)]
eta = np.diag([-1, 1, 1, 1])
for a, Ga in enumerate([g0] + gs):
    for b, Gb in enumerate([g0] + gs):
        assert np.allclose(Ga @ Gb + Gb @ Ga, 2 * eta[a, b] * np.eye(4))
rng = np.random.default_rng(100)
m = 0.7
Pv = np.array([0.3, -0.5, 0.4])
dvec = rng.uniform(-1, 1, 3)
qc = rng.uniform(-1, 1, 6)
K3c = rng.uniform(-1, 1, (3, 3, 4)); K3c = (K3c + K3c.transpose(1, 0, 2)) / 2
e0 = rng.uniform(-1, 1, 4) + I * rng.uniform(-1, 1, 4)
e1c = rng.uniform(-1, 1, (4, 10)) + I * rng.uniform(-1, 1, (4, 10))
e2c = rng.uniform(-1, 1, (4, 4)) + I * rng.uniform(-1, 1, (4, 4))
mons2 = [1, nn[0], nn[1], nn[2], nn[0] ** 2, nn[1] ** 2, nn[2] ** 2, nn[0] * nn[1], nn[1] * nn[2], nn[0] * nn[2]]
mons1 = mons2[:4]
Phat = Pv / np.linalg.norm(Pv)
w, U = np.linalg.eigh(sum(Phat[j] * (g0 @ gs[j]) for j in range(3)))
e0_al = U[:, np.argmax(w)]
assert abs(w.max() - 1) < 1e-12


def build(general, eps0, psi_extra=True):
    """Lambdified psi, eps (4), d eps (4 x 3), omega (3 x 3 x 3) and K (3 x 3, frame)."""
    Pv_, dvec_, qc_, K3c_, e1c_, e2c_ = (np.asarray(a).tolist() for a in (Pv, dvec, qc, K3c, e1c, e2c))
    eps0 = [complex(c) for c in eps0]
    psi = 1 + m / (2 * r)
    if psi_extra:
        psi += sum(dvec_[i] * nn[i] for i in range(3)) / r ** 2
        psi += (qc_[0] * nn[0] ** 2 + qc_[1] * nn[1] ** 2 + qc_[2] * nn[0] * nn[2] + qc_[3] * nn[1] * nn[2]
                + qc_[4] * nn[0] + qc_[5]) / r ** 3
    E = [[psi ** -2 if a == mu else 0 for mu in range(3)] for a in range(3)]       # e_a = psi^-2 d_a
    th = [[psi ** 2 if a == mu else 0 for mu in range(3)] for a in range(3)]       # theta^a = psi^2 dx^a
    Cab = [[[0] * 3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            com = [sum(E[a][k] * sp.diff(E[b][mu], X[k]) - E[b][k] * sp.diff(E[a][mu], X[k]) for k in range(3))
                   for mu in range(3)]
            for c in range(3):
                Cab[a][b][c] = sum(th[c][mu] * com[mu] for mu in range(3))
    om = [[[(Cab[i][k][j] - Cab[i][j][k] - Cab[k][j][i]) / 2 for k in range(3)] for j in range(3)] for i in range(3)]
    if general:
        KBY = [[sp.Rational(3, 2) / r ** 2 * (Pv_[i] * nn[j] + Pv_[j] * nn[i]
                                              - ((1 if i == j else 0) - nn[i] * nn[j]) * sum(Pv_[k] * nn[k] for k in range(3)))
                for j in range(3)] for i in range(3)]
        K = [[psi ** -6 * (KBY[i][j] + sum(K3c_[i][j][k] * mons1[k] for k in range(4)) / r ** 3) for j in range(3)]
             for i in range(3)]
        eps = [eps0[a] + sum(e1c_[a][k] * mons2[k] for k in range(10)) / r
               + sum(e2c_[a][k] * mons1[k] for k in range(4)) / r ** 2 for a in range(4)]
    else:
        K = [[0] * 3 for _ in range(3)]
        eps = [sp.sympify(eps0[a]) for a in range(4)]
    deps = [[sp.diff(eps[a], X[k]) for k in range(3)] for a in range(4)]
    dpsi = [sp.diff(psi, X[k]) for k in range(3)]
    L = lambda e: sp.lambdify(X, e, 'numpy')
    return dict(psi=L(psi), dpsi=[L(e) for e in dpsi], eps=[L(e) for e in eps],
                deps=[[L(e) for e in row] for row in deps], om=[[[L(e) for e in rr] for rr in row] for row in om],
                K=[[L(e) for e in row] for row in K])


def ev(f, P):
    v = f(*P)
    return np.broadcast_to(np.asarray(v, dtype=complex), P[0].shape)


NT, NP = 48, 96
ct, wt = np.polynomial.legendre.leggauss(NT)
ph = 2 * np.pi * np.arange(NP) / NP
CT, PH = np.meshgrid(ct, ph, indexing='ij')
ST = np.sqrt(1 - CT ** 2)
NV = np.array([ST * np.cos(PH), ST * np.sin(PH), CT])
WQ = wt[:, None] * (2 * np.pi / NP) * np.ones_like(PH)


def sphere(f_of_points, R):
    pts = [R * NV[k] for k in range(3)]
    return np.sum(WQ * f_of_points(pts)) * R ** 2


def V_dot_n(D, pts):
    psi = ev(D['psi'], pts).real
    eps = np.array([ev(f, pts) for f in D['eps']])                     # (4, ...)
    de = np.array([[ev(f, pts) for f in row] for row in D['deps']])   # (4, 3, ...)
    om = np.array([[[ev(f, pts).real for f in rr] for rr in row] for row in D['om']])
    K = np.array([[ev(f, pts).real for f in row] for row in D['K']])
    osg = -1.0 if mut == 'omega' else 1.0
    nab = []
    for i in range(3):
        v = psi ** -2 * de[:, i]
        for j in range(3):
            for k in range(3):
                v = v + osg * 0.25 * om[i, j, k] * np.einsum('ab,b...->a...', gs[j] @ gs[k], eps)
        nab.append(v)
    Deps = sum(np.einsum('ab,b...->a...', gs[i], nab[i]) for i in range(3))
    inner = lambda a, b: np.sum(np.conj(a) * b, axis=0)
    xi = [inner(eps, np.einsum('ab,b...->a...', g0 @ gs[j], eps)).real for j in range(3)]
    trK = K[0, 0] + K[1, 1] + K[2, 2]
    Pm = K - np.eye(3)[:, :, None, None] * trK
    dh = 0.5 if mut == 'Dhalf' else 1.0
    ks = 0.5 if mut == 'Vsign' else -0.5
    V = [inner(eps, nab[i] - dh * np.einsum('ab,b...->a...', gs[i], Deps)).real + ks * sum(Pm[i, j] * xi[j] for j in range(3))
         for i in range(3)]
    nhat = [pts[k] / np.sqrt(pts[0] ** 2 + pts[1] ** 2 + pts[2] ** 2) for k in range(3)]
    return psi ** 4 * sum(V[a] * nhat[a] for a in range(3))


def adm(D, pts):
    """Integrands of 16 pi E and 8 pi P_j on g = psi^4 delta, K_mn (coordinate) = psi^4 K_ab (frame)."""
    psi = ev(D['psi'], pts).real
    dpsi = np.array([ev(f, pts).real for f in D['dpsi']])
    K = np.array([[ev(f, pts).real for f in row] for row in D['K']]) * psi ** 4
    nhat = np.array([pts[k] for k in range(3)]) / np.sqrt(pts[0] ** 2 + pts[1] ** 2 + pts[2] ** 2)
    # d_j g_ij - d_i g_jj with g = psi^4 delta: 4 psi^3 (d_i psi - 3 d_i psi) = -8 psi^3 d_i psi
    eint = sum(-8 * psi ** 3 * dpsi[i] * nhat[i] for i in range(3))
    trK = (K[0, 0] + K[1, 1] + K[2, 2]) / psi ** 4
    pint = [sum((K[i, j] - (psi ** 4 if i == j else 0) * trK) * nhat[i] for i in range(3)) for j in range(3)]
    return eint, pint


def extrap(vals, Rs):
    A = np.array([[(Rs[0] / R) ** k for k in range(len(Rs))] for R in Rs])
    return np.linalg.solve(A, np.array(vals))[0]


def limit(fn):
    out = []
    for base in (100.0, 150.0):
        Rs = [base * 2 ** k for k in range(6)]
        out.append(extrap([fn(R) for R in Rs], Rs))
    return out[0], abs(out[0] - out[1])


fails = []
tolok = lambda d, tgt: abs(d) < 1e-8 * max(1.0, abs(tgt))


def crit(name, val, tgt, spread):
    ok = tolok(val - tgt, tgt) and spread < 1e-8
    print(f"  {name}: B = {val:.12f}, target {tgt:.12f}, diff {val - tgt:.2e}, spread {spread:.1e}: "
          f"{'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name.split()[0])


print("# ind100: boundary term of item 6's identity on psi^4 delta, float64 flux at R = 100..4800 extrapolated"
      + (f", mutate={mut}" if mut else ""), flush=True)
n0 = float(np.vdot(e0, e0).real)
D0 = build(False, e0, psi_extra=False)
b, sp_ = limit(lambda R: sphere(lambda p: V_dot_n(D0, p), R).real / (4 * np.pi))
crit("C0 Schwarzschild, eps = eps_0", b, m * n0, sp_)
D1 = build(False, e0, psi_extra=True)
b, sp_ = limit(lambda R: sphere(lambda p: V_dot_n(D1, p), R).real / (4 * np.pi))
crit("C1 psi with dipole and r^-3 terms, K = 0", b, m * n0, sp_)
D2 = build(True, e0)
Eadm, sE = limit(lambda R: sphere(lambda p: adm(D2, p)[0], R).real / (16 * np.pi))
Padm, sP = [], []
for j in range(3):
    v, s_ = limit(lambda R: sphere(lambda p: adm(D2, p)[1][j], R).real / (8 * np.pi))
    Padm.append(v); sP.append(s_)
okE = tolok(Eadm - m, m) and sE < 1e-8 and all(tolok(Padm[j] - Pv[j], Pv[j]) and sP[j] < 1e-8 for j in range(3))
print(f"  C2 ADM: E = {Eadm:.12f} (m = {m}), P = ({Padm[0]:.12f}, {Padm[1]:.12f}, {Padm[2]:.12f}), spreads "
      f"{max([sE] + sP):.1e}: {'PASS' if okE else 'FAIL'}", flush=True)
if not okE:
    fails.append("C2")
xi0 = np.array([np.vdot(e0, g0 @ gs[j] @ e0).real for j in range(3)])
b, sp_ = limit(lambda R: sphere(lambda p: V_dot_n(D2, p), R).real / (4 * np.pi))
crit("C3 general", b, Eadm * n0 - float(np.dot(np.array(Padm), xi0)), sp_)
print(f"     (|eps_0|^2 = {n0:.6f}, xi_0 = {np.round(xi0, 6)}, P.xi_0 = {np.dot(Pv, xi0):.6f})", flush=True)
D4 = build(True, e0_al)
b, sp_ = limit(lambda R: sphere(lambda p: V_dot_n(D4, p), R).real / (4 * np.pi))
crit("C4 aligned eps_0 (xi_0 = P/|P|)", b, m - np.linalg.norm(Pv), sp_)
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
