"""
Coordinator's independent check of #101's review of #72 (Type I set on D = 0 of the Alcubierre wall, off the equator).

Shares no code with review_he_surface_*.py, he_surface.py, he_type.py, review_he_derive.py or phantom_source.py. Route:
the coordinate Ricci tensor of g = -dt^2 + (dx + w dt)^2 + dy^2 + dz^2 with w = v (1 - f(r)) and an explicit quadratic
profile f(r) = f0 + a (r - r0) + (b/2)(r - r0)^2 (so F = 1 - f0, f' = a, f'' = b at r0), my own Christoffel symbols and
Ricci, evaluated exactly at (x, y, z) = r0 (c, s, 0); frame n = d_t - w d_x, e_x = d_x, e_rho = d_y; M = eta R on
(n, e_x, e_rho), eta = diag(-1, 1, 1), Sigma(lam) = R - lam eta, m_ij,kl the 2x2 minors of Sigma (rows i, j; columns
k, l). Exact sympy arithmetic at rational points, with c, s Pythagorean and v possibly a square root.
Usage: python ind101.py [--mutate=cof|Rsign|T2off]

Criteria, fixed before the first run:
  C0  v = 0 gives R = 0 exactly (flat), and at v != 0 R_00 + R_xx + 2 R_rhorho = 0 (he_surface.md's table identity)
      at 2 random points.
  C1  the review's certificate, -cs m01,01 + (c^2 - s^2) m01,02 + vF c^2 m01,12 + cs m02,02 + vF cs m02,12 =
      (1/2) v^2 a u c s (1 + v^2 F^2)(b + a u), u = 1/r0, as polynomials in lam, exactly at 6 random rational points.
  C2  he_surface.md's factorization D(b = -a u) = v^6 a^6 u^6 (v^2 F^2 s^4 - 4 c^2) P2^2, P2 = v^2 (r a + F)(r a + c^2 F)
      + c^2, exactly at 4 random rational points.
  C3  4 points built on T1 and T2 with T3 != 0 (b = -a/r0, v^2 = -c^2/((X + F)(X + c^2 F)), X = r0 a), 2 with F > 0 and
      2 with F < 0: D = 0, the repeated root has multiplicity 2, rank(M - lam I) = 1 (Type I), exactly.
  C4  1 point on T1 and T2 with T3 = 0 (X = -(1 + c^2) F / 2): D = 0 and it is not Type I (triple root, or rank 2).
  Reported: at the F < 0 points, whether -F < r a < -c^2 F and v F s^2 >= 2|c| hold (the review's gap 1).
Mutations (each must make the script exit 1):
  cof    the cofactor vF c^2 of m01,12 doubled: C1 must fail.
  Rsign  R(n, e_rho) negated in the frame block: C2 and C3 must fail.
  T2off  v^2 times 101/100 at C3's points: C3 must fail.
Exit 1 if any criterion fails.
Run 1 (ind101_run1.txt) failed C3 at 2 of its 4 points: pyth() drew m = 1, so c = 0 and v = 0, outside the claim's
domain (c, s, v != 0). pyth() now excludes c = 0; the criteria are unchanged.
"""
import sys, random, time
import sympy as sp

mut = next((q.split('=', 1)[1] for q in sys.argv[1:] if q.startswith('--mutate=')), None)
assert mut in (None, 'cof', 'Rsign', 'T2off')
T0 = time.time()
t, x, y, z = X4 = sp.symbols('t x y z', real=True)
v_, f0_, a_, b_, r0_ = sp.symbols('v f0 a b r0', real=True)
rr = sp.sqrt(x ** 2 + y ** 2 + z ** 2)
fprof = f0_ + a_ * (rr - r0_) + b_ / 2 * (rr - r0_) ** 2
w = v_ * (1 - fprof)
g = sp.Matrix([[-1 + w ** 2, w, 0, 0], [w, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi = sp.Matrix([[-1, w, 0, 0], [w, 1 - w ** 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
assert sp.simplify(g * gi - sp.eye(4)) == sp.zeros(4)
dg = [[[sp.diff(g[m, n], X4[k]) for k in range(4)] for n in range(4)] for m in range(4)]
Gam = [[[sum(gi[l, m] * (dg[m][i][j] + dg[m][j][i] - dg[i][j][m]) for m in range(4)) / 2 for j in range(4)]
        for i in range(4)] for l in range(4)]
Ric = sp.zeros(4)
for i in range(4):
    for j in range(i, 4):
        e = sum(sp.diff(Gam[l][i][j], X4[l]) - sp.diff(Gam[l][i][l], X4[j]) for l in range(4))
        e += sum(Gam[l][l][m] * Gam[m][i][j] - Gam[l][j][m] * Gam[m][i][l] for l in range(4) for m in range(4))
        Ric[i, j] = Ric[j, i] = e
print(f"# ind101: coordinate Ricci built in {time.time() - T0:.0f} s" + (f", mutate={mut}" if mut else ""), flush=True)


def block(v, F, a, b, r0, c, s):
    """Exact 3x3 frame Ricci block on (n, e_x, e_rho) at r0 (c, s, 0)."""
    sub = {v_: v, f0_: 1 - F, a_: a, b_: b, r0_: r0, x: r0 * c, y: r0 * s, z: 0, t: 0}
    R = Ric.subs(sub)
    R = R.applyfunc(lambda q: sp.radsimp(sp.nsimplify(q) if q.is_Float else q))
    wv = v * F
    n = [1, -wv, 0, 0]; ex = [0, 1, 0, 0]; er = [0, 0, 1, 0]
    E = [n, ex, er]
    B = sp.Matrix(3, 3, lambda i, j: sp.expand(sum(E[i][p] * E[j][q] * R[p, q] for p in range(4) for q in range(4))))
    if mut == 'Rsign':
        B[0, 2] = -B[0, 2]; B[2, 0] = -B[2, 0]
    return B


lam = sp.Symbol('lam')
eta = sp.diag(-1, 1, 1)
rnd = random.Random(101)
Q = sp.Rational
fails = []


def pyth():
    while True:  # c != 0 and s != 0: the claim's domain (run 1 drew m = 1, so c = 0 and v = 0)
        m = Q(rnd.randint(1, 9), rnd.randint(2, 11))
        if m != 1:
            return (1 - m ** 2) / (1 + m ** 2), 2 * m / (1 + m ** 2)


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


def minor(S, rows, cols):
    return sp.expand(S[rows[0], cols[0]] * S[rows[1], cols[1]] - S[rows[0], cols[1]] * S[rows[1], cols[0]])


def disc_of(B):
    p = sp.Poly((lam * sp.eye(3) - eta * B).det(), lam)
    return sp.discriminant(p.as_expr(), lam), p


# C0
B0 = block(0, Q(1, 2), Q(1, 3), Q(-2, 5), Q(3, 2), *pyth())
okA = B0 == sp.zeros(3)
okB = True
for _ in range(2):
    c, s = pyth()
    Bt = block(Q(rnd.randint(1, 9), 4), Q(rnd.randint(1, 9), 10), Q(rnd.randint(-9, 9), 7), Q(rnd.randint(-9, 9), 5),
               Q(rnd.randint(2, 9), 3), c, s)
    okB &= sp.simplify(Bt[0, 0] + Bt[1, 1] + 2 * Bt[2, 2]) == 0
report("C0 flat and trace", okA and okB, f"R = 0 at v = 0: {okA}; R00 + Rxx + 2 Rrr = 0 at 2 points: {okB}")

# C1 certificate
okC = True
for k in range(6):
    c, s = pyth()
    v, F, a, b, r0 = (Q(rnd.randint(1, 9), 4), Q(rnd.randint(-9, 9), 10), Q(rnd.randint(-9, 9), 7),
                      Q(rnd.randint(-9, 9), 5), Q(rnd.randint(2, 9), 3))
    S = block(v, F, a, b, r0, c, s) - lam * eta
    u = 1 / r0
    cf = 2 * v * F * c ** 2 if mut == 'cof' else v * F * c ** 2
    lhs = (-c * s * minor(S, (0, 1), (0, 1)) + (c ** 2 - s ** 2) * minor(S, (0, 1), (0, 2)) + cf * minor(S, (0, 1), (1, 2))
           + c * s * minor(S, (0, 2), (0, 2)) + v * F * c * s * minor(S, (0, 2), (1, 2)))
    rhs = Q(1, 2) * v ** 2 * a * u * c * s * (1 + v ** 2 * F ** 2) * (b + a * u)
    okC &= sp.expand(lhs - rhs) == 0
report("C1 certificate", okC, "6 random rational points, as polynomials in lam")

# C2 factorization on T1
okD = True
for k in range(4):
    c, s = pyth()
    v, F, a, r0 = Q(rnd.randint(1, 9), 4), Q(rnd.randint(-9, 9), 10), Q(rnd.randint(-9, 9), 7), Q(rnd.randint(2, 9), 3)
    u = 1 / r0
    D, _ = disc_of(block(v, F, a, -a * u, r0, c, s))
    P2 = v ** 2 * (r0 * a + F) * (r0 * a + c ** 2 * F) + c ** 2
    okD &= sp.simplify(D - v ** 6 * a ** 6 * u ** 6 * (v ** 2 * F ** 2 * s ** 4 - 4 * c ** 2) * P2 ** 2) == 0
report("C2 D on T1", okD, "4 random rational points")


def typeinfo(B):
    D, p = disc_of(B)
    D = sp.simplify(D)
    if D != 0:  # distinct roots: no repeated root to test
        return D, 1, None
    roots = sp.roots(p)
    lr, mult = max(roots.items(), key=lambda kv: kv[1])
    rk = (eta * B - lr * sp.eye(3)).applyfunc(sp.radsimp).rank(simplify=True)
    return D, mult, rk


# C3 Type I points on T1, T2 with T3 != 0
okE = True
gapinfo = []
specs = [(Q(3, 5), Q(1, 2)), (Q(4, 5), Q(2, 3)), (Q(-3, 5), Q(1, 2)), (Q(-4, 5), Q(1, 3))]   # (F, position in interval)
for F, th in specs:
    c, s = pyth()
    lo, hi = sorted([-F, -c ** 2 * F])
    Xv = lo + th * (hi - lo)
    if 2 * Xv + (1 + c ** 2) * F == 0:
        Xv = lo + (th / 2) * (hi - lo)
    r0 = Q(rnd.randint(2, 9), 3)
    a = Xv / r0
    v2 = -c ** 2 / ((Xv + F) * (Xv + c ** 2 * F))
    if mut == 'T2off':
        v2 = v2 * Q(101, 100)
    v = sp.sqrt(v2)
    D, mult, rk = typeinfo(block(v, F, a, -a / r0, r0, c, s))
    ok = D == 0 and mult == 2 and rk == 1
    okE &= ok
    if F < 0:
        gapinfo.append((-F < Xv < -c ** 2 * F, bool(sp.simplify(v * F * s ** 2 - 2 * abs(c)) >= 0)))
    print(f"     F = {F}, c = {c}, r a = {Xv}, v^2 = {v2}: D = {D}, multiplicity {mult}, rank {rk}", flush=True)
report("C3 Type I on T1, T2, T3", okE, "4 points, 2 with F < 0")
print(f"     reported, at the F < 0 points (-F < r a < -c^2 F, v F s^2 >= 2|c|): {gapinfo}", flush=True)

# C4 T3 = 0
c, s = pyth()
F, r0 = Q(3, 5), Q(5, 3)
Xv = -(1 + c ** 2) * F / 2
v = sp.sqrt(-c ** 2 / ((Xv + F) * (Xv + c ** 2 * F)))
D, mult, rk = typeinfo(block(v, F, Xv / r0, -Xv / r0 ** 2, r0, c, s))
report("C4 T3 = 0 is not Type I", D == 0 and not (mult == 2 and rk == 1), f"D = {D}, multiplicity {mult}, rank {rk}")
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
