"""
Coordinator's independent check of #102 (the Type III set on D = 0 of the Alcubierre wall, he_type3.md).

Shares no code with he_type3.py, review_he_surface_lib.py, he_surface.py or he_type.py; imports nothing from the
repository. Route: the coordinate Ricci tensor of g = -dt^2 + (dx + w dt)^2 + dy^2 + dz^2, where w is the second-order
Taylor polynomial of v (1 - f(r)) about p = r0 (c, s, 0) (w_i = -v a n_i, w_ij = -v [b n_i n_j + a u (d_ij - n_i n_j)],
a = f', b = f'', F = 1 - f, u = 1/r0), so the Ricci tensor at p is exact and polynomial in (v, F, a, b, u, c, s). Own
Christoffel symbols and Ricci; frame n = d_t - vF d_x, e_x = d_x, e_rho = d_y; B = R on (n, e_x, e_rho), eta =
diag(-1, 1, 1), M = eta B, Sigma(lam) = B - lam eta, det(x - M) = x^3 + c2 x^2 + c1 x + c0, E1 = c2^2 - 3 c1,
E2 = 27 c0 - c2^3, T = b + a u. "mod" means modulo c^2 + s^2 = 1. Formulas quoted from he_type3.md are typed here from
the note's text; the check is that this script's tensor satisfies them.
Usage: python ind102.py [--mutate=gamma|phi|Kdrop|sigma]

Criteria, fixed before the first run:
  C0  Own type test (D, multiplicity, exact rank of M - lam) on planted 3x3 tensors, each also after a boost (rapidity
      artanh 3/5) and a rotation: lam eta + k e + e k (k null, e unit, k.e = 0) is III; lam eta + k k is II with a
      triple root of rank 1; diag(rho, p, p) is I.
  C1  B equals he_type3.md section 1's table in (phi, X, gamma, y, w) exactly, mod; and B = 0 at v = 0.
  C2  E1 equals the note's printed quadratic form, mod; c2 equals the note's [4 phi (gamma + w y) - X (3w + 1)] / 2;
      E1 and E2 reduce to s-free polynomials, even in c, with 17 and 42 terms in (v, F, a, b, u, c).
  C3  27 D + E2^2 = 27 E1 G for the generic cubic, G = (c2^4 + 3 c1 c2^2 + 36 c1^2 - 162 c0 c2) / 27, D its discriminant.
  C4  #101's certificate as the note restates it, K1 T = -cs m01,01 + (c^2 - s^2) m01,02 + vF c^2 m01,12 + cs m02,02
      + vF cs m02,12 with K1 = v^2 a u c s (1 + v^2 F^2) / 2, identically in lam, mod; and at a = 0,
      m01,01 = -Sigma00^2 - Sigma01^2 and Sigma01 = v b s^2 / 2.
  C5  At T = 0 (b = -a u), with the note's lam* = -v^2 a s^2 (a + 2Fu) / 2, Theta = v^2 a (2a + (1 + c^2) F u),
      K = v^2 a^2 [v^2 (a + Fu)(a + c^2 Fu) + c^2 u^2], Gamma = (c^2, cs, 0, s^2, 0, 0), all mod:
      det(x - M) = (x - lam*)[(x - lam*)(x - lam* - Theta) + K]; c2 = -3 lam* - Theta; E1 = Theta^2 - 3K;
      E2 = Theta^3 + 9 lam* (Theta^2 - 3K); m_k(lam*) = -K Gamma_k for the six minors (01,01 01,02 01,12 02,02 02,12
      12,12). And an exact point with T = Theta = K = 0 (c = 3/5, v = 3, F = 5/8, u = 1) is II: D = 0, triple root,
      rank 1, E1 = E2 = 0.
  C6  #72's point: c = 3/5, s = 4/5, v = 2, a = -1/2, phi = (-9 + sqrt 113)/16, F = phi/2, and (lam, u, b) solved
      from Sigma(lam) e = 0, e = (1, -7/25, 24/25). Exactly in Q(sqrt 113): E1 = E2 = 0, D = 0, T != 0, N = M - lam0
      (lam0 = -c2/3) has N^3 = 0, N^2 != 0 and a nonzero 2x2 minor. F, b, u, T and lam0 agree with the note's
      table and output (0.050942057, -0.57042403, 0.28816478, -0.71450642, 0.38708958) to relative 1e-7.
  C7  Re-solve two tanh points at 50 digits from the note's (r, cos theta), f = [tanh s(r + R) - tanh s(r - R)] /
      (2 tanh sR) with own analytic jets (checked against mp.diff to 1e-30): Le (s = 8, R = 1, v = 1/2) at
      (0.990567889806, 0.245054615703) and Rodal (s = 4, R = 5, v = 1) at (5.07106634302, 0.533635342003). findroot of
      (E1, E2) in (r, c) converges within 1e-10 of both; there the three eigenvalues of M agree within 1e-12, the
      singular values of M - lam0 are two above 0.1 and one below 1e-35, and T is within 1e-3 of -8.80794 and 3.7259.
  C8  Own scan at fixed v: the sign changes of the Sylvester resultant in w = c^2 of E1(w) and E2(w) over r in
      [0.05, 4] (step 5e-4, Le) and [1, 12] (step 1e-3, Rodal) at 60 digits, each bisected and polished in (r, c);
      accepted when 0 < w < 1, |T| > 1e-6 and the triple root holds as in C7. Exactly 3 accepted at each wall, at the
      note's radii (0.990567889806, 1.02393326111, 1.09466230932; 4.71448517823, 5.07106634302, 5.10338056385) within
      1e-9. (A grid scan: the count is numerical evidence, as in the note.)
Mutations (each must make the script exit 1):
  gamma  the Gamma Gamma terms dropped from the Ricci tensor: C1 must fail.
  phi    phi + 10^-40 at C6's point: C6 must fail.
  Kdrop  the K Gamma_k term dropped in C5's minors: C5 must fail.
  sigma  Le's sigma 8.001 in C7 and C8: C7 and C8 must fail.
Exit 1 if any criterion fails.
"""
import sys, time
import mpmath as mp
import sympy as sp

mut = next((q.split('=', 1)[1] for q in sys.argv[1:] if q.startswith('--mutate=')), None)
assert mut in (None, 'gamma', 'phi', 'Kdrop', 'sigma')
T0 = time.time()
Q = sp.Rational
fails = []


def report(name, ok, detail):
    print(f"  {name}: {detail}: {'PASS' if ok else 'FAIL'}  [{time.time() - T0:.0f} s]", flush=True)
    if not ok:
        fails.append(name)


v, F, a, b, u, c, s = sp.symbols('v F a b u c s', real=True)
lam, xx, W = sp.symbols('lam x w')
t, X1, X2, X3 = crd = sp.symbols('t X1 X2 X3', real=True)
d = [X1, X2, X3]
nv = [c, s, 0]
wi = [-v * a * nv[i] for i in range(3)]
wij = [[-v * (b * nv[i] * nv[j] + a * u * ((1 if i == j else 0) - nv[i] * nv[j])) for j in range(3)] for i in range(3)]
w = v * F + sum(wi[i] * d[i] for i in range(3)) + sum(wij[i][j] * d[i] * d[j] for i in range(3) for j in range(3)) / 2
g = sp.Matrix([[-1 + w ** 2, w, 0, 0], [w, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
gi = sp.Matrix([[-1, w, 0, 0], [w, 1 - w ** 2, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
assert (g * gi - sp.eye(4)).applyfunc(sp.expand) == sp.zeros(4)
dg = [[[sp.diff(g[m, n], crd[k]) for k in range(4)] for n in range(4)] for m in range(4)]
Gam = [[[sp.expand(sum(gi[l, m] * (dg[m][i][j] + dg[m][j][i] - dg[i][j][m]) for m in range(4)) / 2)
         for j in range(4)] for i in range(4)] for l in range(4)]
at0 = {X1: 0, X2: 0, X3: 0, t: 0}
G0 = [[[Gam[l][i][j].subs(at0) for j in range(4)] for i in range(4)] for l in range(4)]
Ric = sp.zeros(4)
for i in range(4):
    for j in range(i, 4):
        e = sum(sp.diff(Gam[l][i][j], crd[l]).subs(at0) - sp.diff(Gam[l][i][l], crd[j]).subs(at0) for l in range(4))
        if mut != 'gamma':
            e += sum(G0[l][l][m] * G0[m][i][j] - G0[l][j][m] * G0[m][i][l] for l in range(4) for m in range(4))
        Ric[i, j] = Ric[j, i] = sp.expand(e)
E = [[1, -v * F, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]]
B = sp.Matrix(3, 3, lambda i, j: sp.expand(sum(E[i][p] * E[j][q] * Ric[p, q] for p in range(4) for q in range(4))))
eta = sp.diag(-1, 1, 1)
M = eta * B
print(f"# ind102: frame Ricci block built in {time.time() - T0:.0f} s" + (f", mutate={mut}" if mut else ""), flush=True)


def red(e):
    """Reduce mod c^2 + s^2 = 1 to degree <= 1 in s."""
    p = sp.Poly(sp.expand(e), s)
    return sp.expand(sum(cf * s ** (k % 2) * (1 - c ** 2) ** (k // 2) for (k,), cf in p.terms()))


def cubic(Mm):
    p = sp.Poly(sp.expand((xx * sp.eye(3) - Mm).det()), xx)
    cs_ = p.all_coeffs()
    assert cs_[0] == 1 and len(cs_) == 4
    return cs_[1], cs_[2], cs_[3]


def disc3(c2_, c1_, c0_):
    return c2_ ** 2 * c1_ ** 2 - 4 * c1_ ** 3 - 4 * c2_ ** 3 * c0_ - 27 * c0_ ** 2 + 18 * c2_ * c1_ * c0_


def minor(S, rows, cols):
    return sp.expand(S[rows[0], cols[0]] * S[rows[1], cols[1]] - S[rows[0], cols[1]] * S[rows[1], cols[0]])


IDX = [((0, 1), (0, 1)), ((0, 1), (0, 2)), ((0, 1), (1, 2)), ((0, 2), (0, 2)), ((0, 2), (1, 2)), ((1, 2), (1, 2))]


def zero(e):
    return sp.expand(sp.radsimp(sp.expand(e))) == 0


def own_type(Mm):
    """(type, D, multiplicity, rank) by exact arithmetic for a 3x3 M = eta T."""
    c2_, c1_, c0_ = cubic(Mm)
    D = sp.expand(sp.radsimp(disc3(c2_, c1_, c0_)))
    if D != 0:
        return ('I' if D > 0 else 'IV'), D, 1, None
    E1_ = sp.expand(sp.radsimp(c2_ ** 2 - 3 * c1_))
    if E1_ == 0:
        l0, mult = -c2_ / 3, 3
    else:  # double root of x^3 + c2 x^2 + c1 x + c0 with D = 0: (9 c0 - c1 c2) / (2 (c2^2 - 3 c1))
        l0, mult = (9 * c0_ - c1_ * c2_) / (2 * (c2_ ** 2 - 3 * c1_)), 2
    N = (Mm - l0 * sp.eye(3)).applyfunc(lambda q: sp.expand(sp.radsimp(q)))
    rk = 0 if all(q == 0 for q in N) else (1 if all(zero(minor(N, r_, c_)) for r_, c_ in IDX + [((1, 2), (0, 1)),
                                                     ((0, 2), (0, 1)), ((1, 2), (0, 2))]) else 2)
    if mult == 3:
        typ = {0: 'I', 1: 'II', 2: 'III'}[rk]
    else:
        typ = {1: 'I', 2: 'II'}[rk]
    return typ, D, mult, rk


# C0 planted
ch, sh = Q(5, 4), Q(3, 4)
Lt = sp.Matrix([[ch, 0, sh], [0, 1, 0], [sh, 0, ch]]) * sp.Matrix([[1, 0, 0], [0, Q(3, 5), -Q(4, 5)], [0, Q(4, 5), Q(3, 5)]])
assert Lt.T * eta * Lt == eta
kl, el = sp.Matrix([1, 1, 0]), sp.Matrix([0, 0, 1])          # lower components: k null, e unit, k.e = 0
l0p = Q(2, 7)
planted = [("lam eta + k e + e k", l0p * eta + kl * el.T + el * kl.T, 'III'),
           ("lam eta + k k", l0p * eta + kl * kl.T, 'II'), ("diag(rho, p, p)", sp.diag(Q(3, 2), Q(1, 3), Q(1, 3)), 'I')]
got0 = []
for name, Tm, want in planted:
    for lab, Tx in (("", Tm), (" boosted", Lt.T * Tm * Lt)):
        ty = own_type(eta * Tx)
        got0.append((name + lab, ty[0], ty[2], ty[3], ty[0] == want))
report("C0 planted types", all(q[-1] for q in got0), "; ".join(f"{n}: {ty} (mult {m}, rank {r})" for n, ty, m, r, _ in got0))

# C1 frame table
phi, Xv, gam, yv, wv = v * F, v ** 2 * a ** 2, v * a * u, v * (b - a * u), c ** 2
tab = sp.Matrix([[-Xv * (1 + wv) / 2 + phi * (gam + wv * yv), gam + (1 - wv) * yv / 2, -c * s * yv / 2],
                 [0, Xv * (3 * wv - 1) / 2 - phi * (gam + wv * yv), c * s * (Xv - phi * yv / 2)],
                 [0, 0, Xv * (1 - wv) / 2]])
for i in range(3):
    for j in range(i):
        tab[i, j] = tab[j, i]
dif = [red(B[i, j] - tab[i, j]) for i in range(3) for j in range(3)]
flat = B.subs(v, 0) == sp.zeros(3)
report("C1 frame table", all(q == 0 for q in dif) and flat,
       f"B - table mod: {sum(q != 0 for q in dif)} nonzero entries; B = 0 at v = 0: {flat}")

# C2 E1, c2, term counts
c2, c1, c0 = cubic(M)
E1 = red(c2 ** 2 - 3 * c1)
E2 = red(27 * c0 - c2 ** 3)
E1p = (Xv ** 2 - phi * ((3 * wv - 1) * gam + 2 * wv * yv) * Xv + (phi ** 2 - 3) * gam ** 2
       + (2 * phi ** 2 * wv + 3 * wv - 3) * gam * yv + (phi ** 2 * wv ** 2 + 3 * phi ** 2 * wv + 3 * wv - 3) * yv ** 2 / 4)
okE1 = red(E1 - E1p) == 0
okc2 = red(c2 - (4 * phi * (gam + wv * yv) - Xv * (3 * wv + 1)) / 2) == 0
sfree = not E1.has(s) and not E2.has(s)
even = sp.expand(E1 - E1.subs(c, -c)) == 0 and sp.expand(E2 - E2.subs(c, -c)) == 0
n1, n2 = len(sp.Add.make_args(E1)), len(sp.Add.make_args(E2))
report("C2 E1, c2, terms", okE1 and okc2 and sfree and even and (n1, n2) == (17, 42),
       f"E1 = printed form: {okE1}; c2 = printed: {okc2}; s-free: {sfree}; even in c: {even}; terms {n1}, {n2}")

# C3 cert_disc on the generic cubic
C2_, C1_, C0_ = sp.symbols('C2 C1 C0')
Dg = sp.discriminant(xx ** 3 + C2_ * xx ** 2 + C1_ * xx + C0_, xx)
Gg = (C2_ ** 4 + 3 * C1_ * C2_ ** 2 + 36 * C1_ ** 2 - 162 * C0_ * C2_) / 27
okD = sp.expand(Dg - disc3(C2_, C1_, C0_)) == 0
ok3 = sp.expand(27 * Dg + (27 * C0_ - C2_ ** 3) ** 2 - 27 * (C2_ ** 2 - 3 * C1_) * Gg) == 0
report("C3 27 D + E2^2 = 27 E1 G", ok3 and okD, f"identity: {ok3}; own D = sympy discriminant: {okD}")

# C4 rank <= 1 forces T = 0
Sg = B - lam * eta
mk = [minor(Sg, r_, c_) for r_, c_ in IDX]
lhs = (-c * s * mk[0] + (c ** 2 - s ** 2) * mk[1] + v * F * c ** 2 * mk[2] + c * s * mk[3] + v * F * c * s * mk[4])
K1 = v ** 2 * a * u * c * s * (1 + v ** 2 * F ** 2) / 2
ok4a = red(lhs - K1 * (b + a * u)) == 0
S0 = Sg.subs(a, 0)
ok4b = red(minor(S0, (0, 1), (0, 1)) + S0[0, 0] ** 2 + S0[0, 1] ** 2) == 0 and red(S0[0, 1] - v * b * s ** 2 / 2) == 0
report("C4 rank certificate", ok4a and ok4b, f"K1 T = combination of minors, in lam: {ok4a}; a = 0 facts: {ok4b}")

# C5 T = 0 forces rank <= 1 at a triple root
onT = {b: -a * u}
lst = -v ** 2 * a * s ** 2 * (a + 2 * F * u) / 2
Th = v ** 2 * a * (2 * a + (1 + c ** 2) * F * u)
Kk = v ** 2 * a ** 2 * (v ** 2 * (a + F * u) * (a + c ** 2 * F * u) + c ** 2 * u ** 2)
Gm = [c ** 2, c * s, 0, s ** 2, 0, 0]
MT = M.subs(onT)
chi = sp.expand((xx * sp.eye(3) - MT).det())
okA = red(chi - (xx - lst) * ((xx - lst) * (xx - lst - Th) + Kk)) == 0
okB = red(c2.subs(onT) + 3 * lst + Th) == 0
okC = red(E1.subs(onT) - (Th ** 2 - 3 * Kk)) == 0 and red(E2.subs(onT) - (Th ** 3 + 9 * lst * (Th ** 2 - 3 * Kk))) == 0
ST = (B - lst * eta).subs(onT)
okM = all(red(minor(ST, r_, c_) + (0 if mut == 'Kdrop' else Kk * Gm[k])) == 0 for k, (r_, c_) in enumerate(IDX))
pt = {c: Q(3, 5), s: Q(4, 5), v: 3, F: Q(5, 8), u: 1}
pt[a] = -(1 + pt[c] ** 2) * pt[F] * pt[u] / 2
pt[b] = -pt[a] * pt[u]
tyT = own_type(M.subs(pt))
zT = [sp.simplify(q.subs(pt)) for q in (Th, Kk, E1, E2, b + a * u)]
okP = tyT[0] == 'II' and tyT[2] == 3 and tyT[3] == 1 and all(q == 0 for q in zT)
report("C5 T = 0 chain", okA and okB and okC and okM and okP,
       f"chi factors: {okA}; c2 = -3 lam* - Theta: {okB}; E1, E2 at T = 0: {okC}; m_k(lam*) = -K Gamma_k: {okM}; "
       f"point (a, b) = ({pt[a]}, {pt[b]}): type {tyT[0]}, D = {tyT[1]}, mult {tyT[2]}, rank {tyT[3]}, "
       f"(Theta, K, E1, E2, T) = {zT}")

# C6 #72's point in Q(sqrt 113)
phi0 = (-9 + sp.sqrt(113)) / 16
if mut == 'phi':
    phi0 = phi0 + Q(1, 10 ** 40)
p6 = {c: Q(3, 5), s: Q(4, 5), v: 2, a: -Q(1, 2), F: phi0 / 2}
ev = sp.Matrix([1, -Q(7, 25), Q(24, 25)])
lq = sp.Symbol('lq')
eqs = list(((B - lq * eta).subs(p6)) * ev)
sol = sp.solve(eqs, [lq, u, b], dict=True)
ok6 = len(sol) == 1
if ok6:
    p6.update({u: sp.radsimp(sol[0][u]), b: sp.radsimp(sol[0][b])})
    M6 = M.subs(p6).applyfunc(lambda q: sp.expand(sp.radsimp(q)))
    c2_6, c1_6, c0_6 = cubic(M6)
    e1_6, e2_6 = zero(c2_6 ** 2 - 3 * c1_6), zero(27 * c0_6 - c2_6 ** 3)
    D6 = zero(disc3(c2_6, c1_6, c0_6))
    T6 = sp.radsimp(p6[b] + p6[a] * p6[u])
    l06 = sp.radsimp(-c2_6 / 3)
    N6 = (M6 - l06 * sp.eye(3)).applyfunc(lambda q: sp.expand(sp.radsimp(q)))
    N2, N3 = (N6 * N6).applyfunc(sp.expand), (N6 * N6 * N6).applyfunc(sp.expand)
    n3z = all(zero(q) for q in N3)
    n2nz = any(not zero(q) for q in N2)
    mnz = any(not zero(minor(N6, r_, c_)) for r_, c_ in IDX)
    num = [sp.N(q, 20) for q in (p6[F], p6[b], p6[u], T6, l06)]
    ref = [0.050942057, -0.57042403, 0.28816478, -0.71450642, 0.38708958]
    rel = max(abs(float(x_) - y_) / abs(y_) for x_, y_ in zip(num, ref))
    ok6 = e1_6 and e2_6 and D6 and not zero(T6) and n3z and n2nz and mnz and rel < 1e-7
    det6 = (f"E1 = 0: {e1_6}, E2 = 0: {e2_6}, D = 0: {D6}, T = {T6} = {float(T6):.8f}, N^3 = 0: {n3z}, "
            f"N^2 != 0: {n2nz}, a 2x2 minor != 0: {mnz}; (F, b, u, T, lam0) = {[f'{float(q):.9g}' for q in num]}, "
            f"max rel. diff. from the note {rel:.1e}")
else:
    det6 = f"linear solve gave {sol}"
report("C6 #72's point in Q(sqrt 113)", ok6, det6)

# C7, C8 tanh walls
mp.mp.dps = 60
fB = sp.lambdify((v, F, a, b, u, c, s), B, 'mpmath')
fE = sp.lambdify((v, F, a, b, u, c), [E1, E2], 'mpmath')
E1w = sp.Poly(sp.expand(E1.subs(c, sp.sqrt(W))), W)
E2w = sp.Poly(sp.expand(E2.subs(c, sp.sqrt(W))), W)
fC1 = sp.lambdify((v, F, a, b, u), E1w.all_coeffs(), 'mpmath')
fC2 = sp.lambdify((v, F, a, b, u), E2w.all_coeffs(), 'mpmath')
print(f"     E1 has degree {E1w.degree()} and E2 degree {E2w.degree()} in w = c^2", flush=True)


def jets(r, sg, Rb):
    tp, tm = mp.tanh(sg * (r + Rb)), mp.tanh(sg * (r - Rb))
    k = 2 * mp.tanh(sg * Rb)
    f = (tp - tm) / k
    f1 = sg * ((1 - tp ** 2) - (1 - tm ** 2)) / k
    f2 = -2 * sg ** 2 * (tp * (1 - tp ** 2) - tm * (1 - tm ** 2)) / k
    return f, f1, f2


def args(r, vv, sg, Rb):
    f, f1, f2 = jets(r, sg, Rb)
    return vv, 1 - f, f1, f2, 1 / r


def tri(r, cc, vv, sg, Rb):
    """Triple-root spread, singular values of M - lam0, T at (r, cos theta)."""
    vv_, Fv, av, bv, uv = args(r, vv, sg, Rb)
    Bn = mp.matrix(fB(vv_, Fv, av, bv, uv, cc, mp.sqrt(1 - cc ** 2)))
    Mn = mp.diag([-1, 1, 1]) * Bn
    l0 = (Mn[0, 0] + Mn[1, 1] + Mn[2, 2]) / 3
    evs = mp.eig(Mn, left=False, right=False)
    spread = max(abs(e_ - l0) for e_ in evs)
    svm = mp.svd_r(Mn - l0 * mp.eye(3), compute_uv=False)
    sv = sorted((svm[i] for i in range(svm.rows)), reverse=True)
    return spread, sv, bv + av * uv


def polish(r, cc, vv, sg, Rb):
    def fun(rr, c_):
        return fE(*args(rr, vv, sg, Rb), c_)
    return mp.findroot(fun, (mp.mpf(r), mp.mpf(cc)), tol=mp.mpf(10) ** -45, maxsteps=100)


walls = [("Le", mp.mpf(8) if mut != 'sigma' else mp.mpf('8.001'), mp.mpf(1), mp.mpf(1) / 2,
          ('0.990567889806', '0.245054615703'), -8.80794, ['0.990567889806', '1.02393326111', '1.09466230932'],
          (mp.mpf('0.05'), mp.mpf(4), mp.mpf('0.0005'))),
         ("Rodal", mp.mpf(4), mp.mpf(5), mp.mpf(1), ('5.07106634302', '0.533635342003'), 3.7259,
          ['4.71448517823', '5.07106634302', '5.10338056385'], (mp.mpf(1), mp.mpf(12), mp.mpf('0.001')))]
mp.mp.dps = 50
jr = mp.mpf('1.01')
jd = max(abs(mp.diff(lambda r: jets(r, 8, 1)[0], jr, k) - jets(jr, 8, 1)[k]) for k in (1, 2))
ok7 = jd < mp.mpf(10) ** -30
det7 = [f"jets vs mp.diff {mp.nstr(jd, 3)}"]
for name, sg, Rb, vv, (r0s, c0s), Tref, _, _ in walls:
    try:
        rr, cc = polish(mp.mpf(r0s), mp.mpf(c0s), vv, sg, Rb)
        sp_, sv, Tv = tri(rr, cc, vv, sg, Rb)
        ok = (abs(rr - mp.mpf(r0s)) < 1e-10 and abs(cc - mp.mpf(c0s)) < 1e-10 and sp_ < 1e-12 and sv[1] > 0.1
              and sv[2] < mp.mpf(10) ** -35 and abs(Tv - Tref) < 1e-3)
        det7.append(f"{name}: r = {mp.nstr(rr, 15)}, cos = {mp.nstr(cc, 15)} (moved {mp.nstr(abs(rr - mp.mpf(r0s)), 2)}, "
                    f"{mp.nstr(abs(cc - mp.mpf(c0s)), 2)}), eigenvalue spread {mp.nstr(sp_, 2)}, singular values "
                    f"{[mp.nstr(q, 5) for q in sv]}, T = {mp.nstr(Tv, 6)}")
    except Exception as ex:  # noqa: BLE001
        ok = False
        det7.append(f"{name}: findroot raised {type(ex).__name__}: {ex}")
    ok7 &= ok
report("C7 re-solved tanh points", ok7, "; ".join(det7))

mp.mp.dps = 60


def resultant(r, vv, sg, Rb):
    A_ = fC1(*args(r, vv, sg, Rb))
    B_ = fC2(*args(r, vv, sg, Rb))
    m_, n_ = len(A_) - 1, len(B_) - 1
    S_ = mp.zeros(m_ + n_)
    for i in range(n_):
        for j, q in enumerate(A_):
            S_[i, i + j] = q
    for i in range(m_):
        for j, q in enumerate(B_):
            S_[n_ + i, i + j] = q
    return mp.det(S_)


ok8 = True
det8 = []
for name, sg, Rb, vv, _, _, rref, (lo, hi, st) in walls:
    nst = int((hi - lo) / st)
    rs = [lo + k * st for k in range(nst + 1)]
    vals = [resultant(r, vv, sg, Rb) for r in rs]
    brackets = [(rs[k], rs[k + 1]) for k in range(nst) if vals[k] * vals[k + 1] < 0]
    acc, rej = [], []
    for ra, rb in brackets:
        fa = resultant(ra, vv, sg, Rb)
        for _ in range(70):
            rm = (ra + rb) / 2
            fm = resultant(rm, vv, sg, Rb)
            if fm * fa > 0:
                ra, fa = rm, fm
            else:
                rb = rm
        rm = (ra + rb) / 2
        cf = fC1(*args(rm, vv, sg, Rb))
        cand = [q for q in mp.polyroots(cf, maxsteps=200, extraprec=200) if abs(mp.im(q)) < 1e-20]
        if not cand:
            rej.append(f"r = {mp.nstr(rm, 10)}: no real root w of E1")
            continue
        e2c = fC2(*args(rm, vv, sg, Rb))
        wbest = min((mp.re(q) for q in cand), key=lambda q: abs(mp.polyval(e2c, q)))
        if not (0 < wbest < 1):
            rej.append(f"r = {mp.nstr(rm, 10)}: w = {mp.nstr(wbest, 6)}")
            continue
        try:
            rr, cc = polish(rm, mp.sqrt(wbest), vv, sg, Rb)
            sp_, sv, Tv = tri(rr, cc, vv, sg, Rb)
        except Exception as ex:  # noqa: BLE001
            rej.append(f"r = {mp.nstr(rm, 10)}: polish raised {type(ex).__name__}")
            continue
        if any(abs(rr - p_[0]) < 1e-20 for p_ in acc):
            rej.append(f"r = {mp.nstr(rm, 10)}: polished onto an accepted point")
            continue
        if 0 < cc ** 2 < 1 and abs(Tv) > 1e-6 and sp_ < 1e-12 and sv[1] > 0.1 and sv[2] < mp.mpf(10) ** -35:
            acc.append((rr, cc, Tv))
        else:
            rej.append(f"r = {mp.nstr(rm, 10)}: T = {mp.nstr(Tv, 4)}, spread {mp.nstr(sp_, 2)}, sv {mp.nstr(sv[1], 3)}")
    match = len(acc) == 3 and all(abs(p_[0] - mp.mpf(q)) < 1e-9 for p_, q in zip(sorted(acc), rref))
    ok8 &= match
    det8.append(f"{name}: {len(brackets)} sign changes over {nst + 1} radii, {len(acc)} accepted at r = "
                f"{[mp.nstr(p_[0], 12) for p_ in sorted(acc)]} (cos = {[mp.nstr(p_[1], 8) for p_ in sorted(acc)]}), "
                f"rejected {rej}")
report("C8 own scan at fixed v", ok8, "; ".join(det8))
print("RESULT", "FAIL: " + ", ".join(fails) if fails else "PASS", f"[{time.time() - T0:.0f} s]")
sys.exit(1 if fails else 0)
