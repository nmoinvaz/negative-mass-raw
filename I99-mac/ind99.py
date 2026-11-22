"""
Coordinator's independent check of #99: item 6's pointwise Weitzenbock identity on a diagonal slice
g = diag(A^2, B^2, C^2)(x, y, z), frame e_i = d_i / A_i,
    |nabla~ eps|^2 - |D~ eps|^2 + 4 pi (mu |eps|^2 - J.xi) = div V,
    V^i = Re<eps, nabla_i eps - g^i D eps> - (1/2) P_ij xi^j,  P_ij = K_ij - delta_ij tr K,  xi^j = <eps, g^0 g^j eps>,
    nabla_i = e_i + (1/4) omega_jk(e_i) g^j g^k,  omega_jk(X) = g(e_j, nabla_X e_k),  nabla~_i = nabla_i + (1/2) K_ij g^j g^0,
    16 pi mu = R + (tr K)^2 - K_ij K_ij,  8 pi J_i = D^j (K_ij - g_ij tr K),  div V = (1/ABC) d_a (ABC V^a / A_a),
in mass_bounds.md's gammas (g^0 = i diag(1, 1, -1, -1), g^j = [[0, s_j], [s_j, 0]]) and <a, b> = a^dagger b.

Shares no code with weitzenbock_conf.py or conventions.py: its own Christoffel symbols, Ricci scalar, spin connection,
covariant divergence and spinor algebra, all from the formulas above (retyped from mass_bounds.md and the docstring of
weitzenbock_conf.py). Method: A, B, C, the six frame components K_ij and the four complex components of eps are random
polynomials of degree 2 with rational (Gaussian rational for eps) coefficients; both sides are formed with sympy and
evaluated exactly at a random rational point. An identity test at points, not a symbolic proof.

Criteria, fixed before the first run:
  C0  flat slice (A = B = C = 1) with K = 0: the difference is exactly 0 at 2 points.
  C1  K = 0 on the diagonal slice (Lichnerowicz): exactly 0 at 3 points.
  C2  general A, B, C, K_ij, eps: exactly 0 at 3 points.
Mutations (each must make the script exit 1):
  Jsign  +J.xi in place of -J.xi: C2 must fail.     sign   nabla~ with -(1/2) K_ij g^j g^0: C2 must fail.
  omega  omega_jk(X) = g(nabla_X e_j, e_k), the other sign: C1 must fail.
Exit 1 if any criterion fails.
Run 1 (ind99_run1.txt) stopped with a TypeError before any criterion was evaluated (a sum of matrices without a zero
start); fixed, criteria unchanged.
"""
import sys, random, time
import sympy as sp

mut = next((a.split('=', 1)[1] for a in sys.argv[1:] if a.startswith('--mutate=')), None)
assert mut in (None, 'Jsign', 'sign', 'omega')
T0 = time.time()
x, y, z = X = sp.symbols('x y z', real=True)
I = sp.I
s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -I], [I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]])
Z2 = sp.zeros(2)
g0 = I * sp.diag(1, 1, -1, -1)
gs = [sp.Matrix(sp.BlockMatrix([[Z2, sj], [sj, Z2]])) for sj in (s1, s2, s3)]
for a, Ga in enumerate([g0] + gs):                       # Clifford relations with eta = diag(-1, 1, 1, 1)
    for b, Gb in enumerate([g0] + gs):
        assert Ga * Gb + Gb * Ga == 2 * (-1 if a == b == 0 else (1 if a == b else 0)) * sp.eye(4)
random.seed(99)
R_ = lambda lo=-1, hi=1, d=11: sp.Rational(random.randint(lo * d, hi * d), d)


def poly(c0=0, scale=1):
    mons = [1, x, y, z, x * x, y * y, z * z, x * y, y * z, x * z]
    return c0 + scale * sum(R_() * m for m in mons)


def cpoly():
    return poly() + I * poly()


def inner(a, b):
    return sum(sp.conjugate(a[k]) * b[k] for k in range(4))


def case(flat, withK, pt):
    Af = [sp.Integer(1)] * 3 if flat else [poly(2, sp.Rational(1, 4)) for _ in range(3)]
    g = sp.diag(*[f ** 2 for f in Af]); gi = sp.diag(*[1 / f ** 2 for f in Af])
    Chr = [[[sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(3)) / 2
             for c in range(3)] for b in range(3)] for a in range(3)]
    Ric = sp.zeros(3)
    for b in range(3):
        for c in range(3):
            Ric[b, c] = (sum(sp.diff(Chr[a][b][c], X[a]) - sp.diff(Chr[a][b][a], X[c]) for a in range(3))
                         + sum(Chr[a][a][d] * Chr[d][b][c] - Chr[a][c][d] * Chr[d][b][a] for a in range(3) for d in range(3)))
    Rs = sum(gi[b, b] * Ric[b, b] for b in range(3))
    # frame e_k = d_k / A_k; omega_jk(e_i) = g(e_j, nabla_{e_i} e_k)
    def nab_e(i, k):   # coordinate components of nabla_{e_i} e_k
        v = [sp.Integer(0)] * 3
        v[k] += sp.diff(1 / Af[k], X[i]) / Af[i]
        for d in range(3):
            v[d] += Chr[d][i][k] / (Af[i] * Af[k])
        return v
    om = [[[sp.Integer(0)] * 3 for _ in range(3)] for _ in range(3)]       # om[i][j][k] = omega_jk(e_i)
    for i in range(3):
        for k in range(3):
            v = nab_e(i, k)
            for j in range(3):
                om[i][j][k] = Af[j] * v[j]                                   # g(e_j, d_d) = A_j delta_jd
    if mut == 'omega':
        om = [[[-om[i][j][k] for k in range(3)] for j in range(3)] for i in range(3)]
    Kf = sp.zeros(3)
    if withK:
        for i in range(3):
            for j in range(i, 3):
                Kf[i, j] = Kf[j, i] = poly()
    trK = sum(Kf[i, i] for i in range(3))
    eps = sp.Matrix([cpoly() for _ in range(4)])
    e = lambda i, f: f.applyfunc(lambda c: sp.diff(c, X[i]) / Af[i])
    nab = [e(i, eps) + sum(((om[i][j][k] / 4) * gs[j] * gs[k] * eps for j in range(3) for k in range(3)), sp.zeros(4, 1)) for i in range(3)]
    ks = -1 if mut == 'sign' else 1
    nabt = [nab[i] + ks * sum(((Kf[i, j] / 2) * gs[j] * g0 * eps for j in range(3)), sp.zeros(4, 1)) for i in range(3)]
    Deps = sum((gs[i] * nab[i] for i in range(3)), sp.zeros(4, 1))
    Dt = sum((gs[i] * nabt[i] for i in range(3)), sp.zeros(4, 1))
    xi = [inner(eps, g0 * gs[j] * eps) for j in range(3)]
    mu = (Rs + trK ** 2 - sum(Kf[i, j] ** 2 for i in range(3) for j in range(3))) / (16 * sp.pi)
    Kc = sp.Matrix(3, 3, lambda a, b: Af[a] * Af[b] * Kf[a, b])            # coordinate components
    Pc = Kc - g * trK
    Jc = [sum(gi[b, c] * (sp.diff(Pc[a, b], X[c]) - sum(Chr[d][c][a] * Pc[d, b] + Chr[d][c][b] * Pc[a, d] for d in range(3)))
              for b in range(3) for c in range(3)) / (8 * sp.pi) for a in range(3)]
    Jf = [Jc[a] / Af[a] for a in range(3)]                                  # frame components
    js = 1 if mut == 'Jsign' else -1
    lhs = (sum(inner(nabt[i], nabt[i]) for i in range(3)) - inner(Dt, Dt)
           + 4 * sp.pi * (mu * inner(eps, eps) + js * sum(Jf[j] * xi[j] for j in range(3))))
    P = Kf - sp.eye(3) * trK
    re = lambda w_: (w_ + sp.conjugate(w_)) / 2
    V = [re(inner(eps, nab[i] - gs[i] * Deps)) - sum(P[i, j] * xi[j] for j in range(3)) / 2 for i in range(3)]
    vol = Af[0] * Af[1] * Af[2]
    rhs = sum(sp.diff(vol * V[a] / Af[a], X[a]) for a in range(3)) / vol
    sub = dict(zip(X, pt))
    d = sp.nsimplify(sp.expand((lhs - rhs).subs(sub)))
    return sp.simplify(d), sp.nsimplify(sp.re(sp.expand(inner(eps, eps).subs(sub))))


fails = []
print("# ind99: item 6's identity on diag(A^2, B^2, C^2), exact at random rational points" + (f", mutate={mut}" if mut else ""), flush=True)
for name, flat, withK, npts in (('C0 flat, K = 0', True, False, 2), ('C1 diagonal, K = 0', False, False, 3), ('C2 general', False, True, 3)):
    for p in range(npts):
        pt = [sp.Rational(random.randint(-20, 20), 23) for _ in range(3)]
        d, n2 = case(flat, withK, pt)
        ok = d == 0
        print(f"  {name}, point {p} {tuple(pt)}: lhs - rhs = {d}  (|eps|^2 = {n2}): {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
        if not ok:
            fails.append(f"{name.split()[0]} at point {p}")
print("RESULT", "FAIL: " + "; ".join(fails) if fails else "PASS")
sys.exit(1 if fails else 0)
