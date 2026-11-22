"""
Coordinator's independent check of #130: item 6's pointwise Weitzenbock identity on g = diag(A^2, B^2, C^2)(x, y, z) in
the frame rotated about z, e'_1 = c e_1 + s e_2, e'_2 = -s e_1 + c e_2, e'_3 = e_3, e_i = d_i / A_i,
    |nabla~ eps|^2 - |D~ eps|^2 + 4 pi (mu |eps|^2 - J'.xi) = div V,
with nabla_i = e'_i + (1/4) omega_jk(e'_i) g^j g^k, omega_jk(X) = g(e'_j, nabla_X e'_k), nabla~_i = nabla_i + (1/2) K'_ij
g^j g^0, V^i = Re<eps, nabla_i eps - g^i D eps> - (1/2) P'_ij xi^j, as in ind99.py.

Shares no code with weitzenbock_conf.py or conventions.py. Differences from the runner's route:
  - the angle is rational: c = (1 - t^2)/(1 + t^2), s = 2t/(1 + t^2) with t = tan(alpha/2) a random polynomial, so no
    reduction modulo c^2 + s^2 = 1 is used and both sides are evaluated exactly at rational points;
  - omega' comes from the Koszul formula of the frame commutators, 2 omega_jk(e_i) = C_ik^j - C_ij^k - C_kj^i with
    [e'_a, e'_b] = C_ab^c e'_c, and needs no Christoffel symbols;
  - J' is the coordinate divergence of P with K_mn = theta^a_m theta^b_n K'_ab, projected on e'.
R, mu and J use Christoffel symbols and Ricci retyped from ind99.py (the coordinator's #99 check, not under test), and
C3 compares the Koszul omega' with the Christoffel route g(e'_j, nabla_{e'_i} e'_k).
Usage: python ind130.py [--mutate=Jsign|sign|frozen]

Criteria, fixed before the first run:
  C0  flat (A = B = C = 1), K = 0, t general: lhs - rhs = 0 and R = 0 exactly at 2 points.
  C4  planted, at C0's points: omega'_21(e'_i) = e'_i(alpha) = 2 e'_i(t) / (1 + t^2) = -omega'_12(e'_i), all other
      components 0, exactly.
  C1  K = 0, A, B, C, t general (Lichnerowicz): lhs - rhs = 0 exactly at 2 points.
  C2  A, B, C, t, K'_ij, eps general: lhs - rhs = 0 exactly at 3 points.
  C3  at C2's points, the Koszul omega' equals the Christoffel-route omega' in all 27 components, exactly.
Mutations (each must make the script exit 1):
  Jsign   +J'.xi in place of -J'.xi: C2 must fail.
  sign    -(1/2) K'_ij g^j g^0 in nabla~: C2 must fail.
  frozen  c and s held constant in the commutators (no e'_i(alpha) in omega'): C1, C2 and C4 must fail.
Exit 1 if any criterion fails.
"""
import sys, random, time
import sympy as sp

mut = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), None)
assert mut in (None, 'Jsign', 'sign', 'frozen')
T0 = time.time()
x, y, z = X = sp.symbols('x y z', real=True)
cc, ss = sp.symbols('cc ss')
I = sp.I
s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -I], [I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
Z2 = sp.zeros(2)
g0 = I * sp.diag(1, 1, -1, -1)
gs = [sp.Matrix(sp.BlockMatrix([[Z2, sj], [sj, Z2]])) for sj in (s1, s2, s3)]
for a, Ga in enumerate([g0] + gs):                       # Clifford relations with eta = diag(-1, 1, 1, 1)
    for b, Gb in enumerate([g0] + gs):
        assert Ga * Gb + Gb * Ga == 2 * (-1 if a == b == 0 else (1 if a == b else 0)) * sp.eye(4)
random.seed(130)
R_ = lambda lo=-1, hi=1, d=11: sp.Rational(random.randint(lo * d, hi * d), d)


def poly(c0=0, scale=1):
    mons = [1, x, y, z, x * x, y * y, z * z, x * y, y * z, x * z]
    return c0 + scale * sum(R_() * m for m in mons)


def inner(a, b):
    return sum(sp.conjugate(a[k]) * b[k] for k in range(4))


def case(flat, withK, pts):
    Af = [sp.Integer(1)] * 3 if flat else [poly(2, sp.Rational(1, 8)) for _ in range(3)]
    t = poly()
    cr, sr = (1 - t ** 2) / (1 + t ** 2), 2 * t / (1 + t ** 2)
    g = sp.diag(*[f ** 2 for f in Af]); gi = sp.diag(*[1 / f ** 2 for f in Af])
    Esym = [[cc / Af[0], ss / Af[1], 0], [-ss / Af[0], cc / Af[1], 0], [0, 0, 1 / Af[2]]]   # E[a][m] = e'^m_a
    real = {cc: cr, ss: sr}
    E = [[sp.sympify(Esym[a][m]).subs(real) for m in range(3)] for a in range(3)]
    th = [[sum(g[m, n] * E[a][n] for n in range(3)) for m in range(3)] for a in range(3)]   # theta^a_m
    # Koszul: commutator coefficients; under 'frozen' c and s are constants while differentiating
    Ed = Esym if mut == 'frozen' else E
    der = lambda f, n: sp.diff(f, X[n]).subs(real) if mut == 'frozen' else sp.diff(f, X[n])
    Cab = [[[None] * 3 for _ in range(3)] for _ in range(3)]
    for a in range(3):
        for b in range(3):
            com = [sum(E[a][n] * der(Ed[b][m], n) - E[b][n] * der(Ed[a][m], n) for n in range(3)) for m in range(3)]
            for c_ in range(3):
                Cab[a][b][c_] = sum(th[c_][m] * com[m] for m in range(3))
    om = [[[(Cab[i][k][j] - Cab[i][j][k] - Cab[k][j][i]) / 2 for k in range(3)] for j in range(3)] for i in range(3)]
    Chr = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(3)) / 2
             for c in range(3)] for b in range(3)] for a in range(3)]
    Ric = sp.zeros(3)
    for b in range(3):
        for c in range(3):
            Ric[b, c] = (sum(sp.diff(Chr[a][b][c], X[a]) - sp.diff(Chr[a][b][a], X[c]) for a in range(3))
                         + sum(Chr[a][a][d] * Chr[d][b][c] - Chr[a][c][d] * Chr[d][b][a] for a in range(3) for d in range(3)))
    Rs = sum(gi[b, b] * Ric[b, b] for b in range(3))
    # Christoffel route for C3: omega_jk(e'_i) = theta^j_m E_i^n (d_n E_k^m + Chr^m_nl E_k^l)
    omC = [[[sum(th[j][m] * E[i][n] * (sp.diff(E[k][m], X[n]) + sum(Chr[m][n][l] * E[k][l] for l in range(3)))
                 for m in range(3) for n in range(3)) for k in range(3)] for j in range(3)] for i in range(3)]
    Kf = sp.zeros(3)
    if withK:
        for i in range(3):
            for j in range(i, 3):
                Kf[i, j] = Kf[j, i] = poly()
    trK = sum(Kf[i, i] for i in range(3))
    eps = sp.Matrix([poly() + I * poly() for _ in range(4)])
    e = lambda i, f: f.applyfunc(lambda q: sum(E[i][m] * sp.diff(q, X[m]) for m in range(3)))
    nab = [e(i, eps) + sum(((om[i][j][k] / 4) * gs[j] * gs[k] * eps for j in range(3) for k in range(3)), sp.zeros(4, 1))
           for i in range(3)]
    ks = -1 if mut == 'sign' else 1
    nabt = [nab[i] + ks * sum(((Kf[i, j] / 2) * gs[j] * g0 * eps for j in range(3)), sp.zeros(4, 1)) for i in range(3)]
    Deps = sum((gs[i] * nab[i] for i in range(3)), sp.zeros(4, 1))
    Dt = sum((gs[i] * nabt[i] for i in range(3)), sp.zeros(4, 1))
    xi = [inner(eps, g0 * gs[j] * eps) for j in range(3)]
    mu = (Rs + trK ** 2 - sum(Kf[i, j] ** 2 for i in range(3) for j in range(3))) / (16 * sp.pi)
    Kc = sp.Matrix(3, 3, lambda m, n: sum(th[a][m] * th[b][n] * Kf[a, b] for a in range(3) for b in range(3)))
    Pc = Kc - g * trK
    Jc = [sum(gi[b, c] * (sp.diff(Pc[a, b], X[c]) - sum(Chr[d][c][a] * Pc[d, b] + Chr[d][c][b] * Pc[a, d] for d in range(3)))
              for b in range(3) for c in range(3)) / (8 * sp.pi) for a in range(3)]
    Jf = [sum(E[i][m] * Jc[m] for m in range(3)) for i in range(3)]
    js = 1 if mut == 'Jsign' else -1
    lhs = (sum(inner(nabt[i], nabt[i]) for i in range(3)) - inner(Dt, Dt)
           + 4 * sp.pi * (mu * inner(eps, eps) + js * sum(Jf[j] * xi[j] for j in range(3))))
    P = Kf - sp.eye(3) * trK
    re = lambda w_: (w_ + sp.conjugate(w_)) / 2
    V = [re(inner(eps, nab[i] - gs[i] * Deps)) - sum(P[i, j] * xi[j] for j in range(3)) / 2 for i in range(3)]
    Vc = [sum(V[a] * E[a][m] for a in range(3)) for m in range(3)]
    vol = Af[0] * Af[1] * Af[2]
    rhs = sum(sp.diff(vol * Vc[m], X[m]) for m in range(3)) / vol
    dal = [2 * sum(E[i][m] * sp.diff(t, X[m]) for m in range(3)) / (1 + t ** 2) for i in range(3)]   # e'_i(alpha)
    out = []
    for pt in pts:
        sub = dict(zip(X, pt))
        ev = lambda q: sp.nsimplify(sp.expand(sp.sympify(q).subs(sub)))
        d = ev(lhs - rhs)
        omv = [[[ev(om[i][j][k]) for k in range(3)] for j in range(3)] for i in range(3)]
        c3 = all(omv[i][j][k] == ev(omC[i][j][k]) for i in range(3) for j in range(3) for k in range(3))
        planted = [[[(ev(dal[i]) if (j, k) == (1, 0) else -ev(dal[i]) if (j, k) == (0, 1) else 0) for k in range(3)]
                    for j in range(3)] for i in range(3)]
        c4 = omv == planted
        out.append((d, ev(Rs), c3, c4, ev(t)))
    return out


fails = []
print("# ind130: item 6's identity on diag(A^2, B^2, C^2) in the frame rotated about z by alpha = 2 atan t, exact at "
      "random rational points" + (f", mutate={mut}" if mut else ""), flush=True)
rp = lambda n: [[sp.Rational(random.randint(-20, 20), 23) for _ in range(3)] for _ in range(n)]
for name, flat, withK, npts in (('C0 flat, K = 0', True, False, 2), ('C1 diagonal, K = 0', False, False, 2),
                                ('C2 general', False, True, 3)):
    pts = rp(npts)
    for p, (pt, (d, Rv, c3, c4, tv)) in enumerate(zip(pts, case(flat, withK, pts))):
        ok = d == 0 and (Rv == 0 if flat else True)
        print(f"  {name}, point {p} {tuple(pt)}, t = {tv}: lhs - rhs = {d}" + (f", R = {Rv}" if flat else "")
              + f": {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
        if not ok:
            fails.append(f"{name.split()[0]} at point {p}")
        if flat:
            print(f"    C4 planted omega'_21(e'_i) = e'_i(alpha), others 0: {'PASS' if c4 else 'FAIL'}", flush=True)
            if not c4:
                fails.append(f"C4 at point {p}")
        if withK:
            print(f"    C3 Koszul omega' = Christoffel omega' (27 components): {'PASS' if c3 else 'FAIL'}", flush=True)
            if not c3:
                fails.append(f"C3 at point {p}")
print("RESULT", "FAIL: " + "; ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
