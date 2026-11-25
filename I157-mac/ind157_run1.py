#!/usr/bin/env python3
"""ind157: the coordinator's independent check of #157 (the ideal step for three mixed-sign scalars on the wall).

Shares no code with three_scalars.py or three_scalars_ideal.py. The wall metric is written in Cartesian coordinates
(t, x, rho, phi), g = -dt^2 + (dx + w dt)^2 + drho^2 + rho^2 dphi^2 with w = w(R), R = sqrt(x^2 + rho^2), and every
derivative is the chain rule through R on symbols w0..w6 (w_k = w^(k)(R)). At lambda = 0, M = Ric(g), K = d_phi, and h is
the (t, x, rho) block of Ric(g). The Ricci numerator det(h)^2 Ric(h) is assembled at a point from h, dh, d^2h with the
adjugate, then turned into the polar components (t, r, theta) of #157. Criteria: README.md of this folder.

    python3 ind157.py                 all checks; exit 1 if any fails
    python3 ind157.py --mutate=NAME   one control (det-L, ric-sign, point, ode, H-b, weight)
"""
import random
import sys
import time

import sympy as sp

MUT = None
for arg in sys.argv[1:]:
    if arg.startswith("--mutate="):
        MUT = arg.split("=", 1)[1]
assert MUT in (None, "det-L", "ric-sign", "point", "ode", "H-b", "weight"), MUT

x, rho, R = sp.symbols("x rho R", positive=True)
c, S = sp.symbols("c S")
NW = 7
w = sp.symbols("w0:%d" % NW)
T0 = time.time()
RESULTS = []


def report(name, ok, msg):
    RESULTS.append((name, ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg} ({time.time() - T0:.0f} s)", flush=True)


def D(F, i):
    """d/dx^i of F(x, rho, R, w0..w6) with R = sqrt(x^2 + rho^2) and w_k = w^(k)(R); i = 0 t, 1 x, 2 rho, 3 phi."""
    if i in (0, 3):
        return sp.Integer(0)
    v = x if i == 1 else rho
    out = sp.diff(F, v) + sp.diff(F, R) * v / R
    for k in range(NW - 1):
        dk = sp.diff(F, w[k])
        if dk != 0:
            out += dk * w[k + 1] * v / R
    assert sp.diff(F, w[NW - 1]) == 0, "jet order exceeded"
    return out


def ricci4(g, ginv):
    n = 4
    dg = [[[D(g[a, b], e) for e in range(n)] for b in range(n)] for a in range(n)]
    Gam = [[[sp.cancel(sum(ginv[a, d] * (dg[d][b][cc] + dg[d][cc][b] - dg[b][cc][d]) for d in range(n)) / 2)
             for cc in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n)
    for b in range(n):
        for cc in range(b, n):
            v = sum(D(Gam[a][b][cc], a) - D(Gam[a][a][b], cc) for a in range(n))
            v += sum(Gam[a][a][d] * Gam[d][b][cc] - Gam[a][cc][d] * Gam[d][a][b] for a in range(n) for d in range(n))
            Ric[b, cc] = Ric[cc, b] = sp.cancel(v)
    return Ric


def ricci_num(h0, h1, h2):
    """det(h)^2 Ric(h)_bc and det(h) at a point, from h, h1[e] = d_e h and h2[e][f] = d_e d_f h (3 x 3)."""
    n = 3
    A = h0.adjugate()
    d = h0.det()

    def B(dd, b, cc):
        return h1[b][dd, cc] + h1[cc][dd, b] - h1[dd][b, cc]

    def dB(e, dd, b, cc):
        return h2[e][b][dd, cc] + h2[e][cc][dd, b] - h2[e][dd][b, cc]

    G = [[[sum(A[a, dd] * B(dd, b, cc) for dd in range(n)) / 2 for cc in range(n)] for b in range(n)] for a in range(n)]
    AhA = [A * h1[e] * A for e in range(n)]

    def dG(e, a, b, cc):  # det^2 * d_e Gamma^a_bc
        return sum(-AhA[e][a, dd] * B(dd, b, cc) + d * A[a, dd] * dB(e, dd, b, cc) for dd in range(n)) / 2

    sgn = -1 if MUT == "ric-sign" else 1
    N = sp.zeros(n)
    for b in range(n):
        for cc in range(b, n):
            v = sum(dG(a, a, b, cc) - dG(cc, a, b, a) for a in range(n))
            v += sgn * sum(G[a][a][dd] * G[dd][b][cc] - G[a][cc][dd] * G[dd][b][a] for a in range(n) for dd in range(n))
            N[b, cc] = N[cc, b] = sp.expand(v)
    return N, sp.expand(d)


# ---- the wall: Ric(g) and its (t, x, rho) block h, symbolic in (x, rho, R, w0..w2) ----
g = sp.Matrix([[-1 + w[0] ** 2, w[0], 0, 0], [w[0], 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, rho ** 2]])
ginv = sp.simplify(g.inv())
RIC = ricci4(g, ginv)
H = RIC[:3, :3]
H1 = [sp.zeros(3), H.applyfunc(lambda F: D(F, 1)), H.applyfunc(lambda F: D(F, 2))]
H2 = [[sp.zeros(3) for _ in range(3)] for _ in range(3)]
for e in (1, 2):
    for f in (1, 2):
        H2[e][f] = H1[f].applyfunc(lambda F: D(F, e))
print(f"Ric(g) and the jets of h built ({time.time() - T0:.0f} s)", flush=True)


def pt(F, R0, cc, SS, W):
    sub = {x: R0 * cc, rho: R0 * SS, R: R0}
    sub.update({w[k]: (W[k] if k < len(W) else 0) for k in range(NW)})
    return sp.expand(sp.cancel(F.xreplace(sub)))


def N_polar(R0, cc, SS, W):
    """#157's numerators N_ab = det_polar(h)^2 Ric(h)_ab in (t, r, theta), and det_polar h, at radius R0, angle (cc, SS)."""
    h0 = H.applyfunc(lambda F: pt(F, R0, cc, SS, W))
    h1 = [M.applyfunc(lambda F: pt(F, R0, cc, SS, W)) for M in H1]
    h2 = [[M.applyfunc(lambda F: pt(F, R0, cc, SS, W)) for M in row] for row in H2]
    Nc, dc = ricci_num(h0, h1, h2)
    E = sp.Matrix([[1, 0, 0], [0, cc, SS], [0, -R0 * SS, R0 * cc]])  # rows: d_t, d_r, d_theta in (t, x, rho)
    Np = (E * Nc * E.T).applyfunc(lambda F: sp.expand(R0 ** 4 * F))
    return Np, sp.expand(R0 ** 2 * dc)


def circ(F):
    """F reduced modulo S^2 + c^2 - 1 (degree <= 1 in S)."""
    return sp.expand(sp.rem(sp.expand(F), S ** 2 + c ** 2 - 1, S))


rnd = random.Random(157)


def rq():
    return sp.Rational(rnd.randint(-9, 9), rnd.randint(1, 7))


IDX = [(0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)]

# ---- P1: K = d_phi is in the kernel of Ric(g); w constant gives Ric(g) = 0 ----
bad = []
for (cc, SS) in [(sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(-5, 13), sp.Rational(12, 13)), (sp.Rational(8, 17), sp.Rational(15, 17))]:
    W = [rq() for _ in range(3)]
    R0 = sp.Rational(rnd.randint(1, 9), rnd.randint(1, 5))
    for a in range(4):
        if pt(RIC[3, a], R0, cc, SS, W) != 0:
            bad.append(("phi", a))
    W0 = [rq(), 0, 0]
    for a in range(4):
        for b in range(4):
            if pt(RIC[a, b], R0, cc, SS, W0) != 0:
                bad.append(("const", a, b))
report("P1", not bad, f"Ric(g)(d_phi, .) = 0 at 3 random exact points, and Ric(g) = 0 for constant w: failures {bad}")


# ---- P2, P3: planted metrics through ricci_num ----
def planted(hsym, X, point):
    sub = dict(zip(X, point))
    h0 = hsym.applyfunc(lambda F: F.subs(sub))
    h1 = [hsym.applyfunc(lambda F: sp.diff(F, X[e]).subs(sub)) for e in range(3)]
    h2 = [[hsym.applyfunc(lambda F: sp.diff(F, X[e], X[f]).subs(sub)) for f in range(3)] for e in range(3)]
    return h0, ricci_num(h0, h1, h2)


Tt, Xx, Yy = sp.symbols("T X Y")
h0, (Nr, dr) = planted(sp.diag(-Xx ** 2, 1, 1), (Tt, Xx, Yy), (sp.Rational(1, 3), 2, sp.Rational(5, 7)))
y = sp.symbols("y1:4")
hs = sp.eye(3) * 4 / (1 + y[0] ** 2 + y[1] ** 2 + y[2] ** 2) ** 2
h0s, (Ns, ds) = planted(hs, y, (sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 5)))
okP2 = Nr == sp.zeros(3)
report("P2", okP2, f"Rindler -X^2 dT^2 + dX^2 + dY^2 at X = 2: det^2 Ric = 0: {okP2}")
okP3 = (Ns - 2 * ds ** 2 * h0s).applyfunc(sp.simplify) == sp.zeros(3)
report("P3", okP3, f"stereographic unit 3-sphere at y = (1/2, 1/3, 1/5): det^2 Ric = 2 det^2 h: {okP3}")

# ---- C1: det h vanishes for every theta on L; not at a jet off L ----
u1, u3, u4 = sp.symbols("u1 u3 u4")
L_W = [u1 / 2, u1, (u1 if MUT == "det-L" else -u1), u3, u4]  # 2 u0 = u1, u1 + u2 = 0
h0L = H.applyfunc(lambda F: pt(F, 1, c, S, L_W))
detL = circ(h0L.det())
Woff = [sp.Rational(1, 3), sp.Rational(2, 7), sp.Rational(-1, 5)]
detoff = sp.expand(H.applyfunc(lambda F: pt(F, 1, sp.Rational(3, 5), sp.Rational(4, 5), Woff)).det())
report("C1", detL == 0 and detoff != 0,
       f"det h on L, reduced mod S^2 + c^2 - 1: {'0' if detL == 0 else str(detL)[:120]}; at u = (1/3, 2/7, -1/5), "
       f"theta with c = 3/5: {detoff}")

# ---- C2, C4: on L, N_theta_theta vanishes identically; some other component does not ----
NL, _ = N_polar(1, c, S, L_W)
NLc = {ab: circ(NL[ab]) for ab in IDX}
report("C2", NLc[(2, 2)] == 0,
       f"N_theta_theta on L (u1, u3, u4 free), mod S^2 + c^2 - 1: {'0' if NLc[(2, 2)] == 0 else 'nonzero'}")
nonzero = [ab for ab in IDX if NLc[ab] != 0]
report("C4", any(ab != (2, 2) for ab in nonzero),
       f"components not identically 0 on L: {nonzero} (t = 0, r = 1, theta = 2)")

# ---- C3: #157's exact point of R1 at the equator ----
uR1 = [sp.Rational(2, 5), 1, sp.Rational(-2, 5), sp.Rational(-83, 75) + (1 if MUT == "point" else 0), 0]
NR1, dR1 = N_polar(1, 0, 1, uR1)
vals = {ab: NR1[ab] for ab in IDX}
report("C3", all(v == 0 for v in vals.values()) and dR1 == 0,
       f"u = (2/5, 1, -2/5, -83/75, 0), theta = pi/2: N_ab = {[str(vals[ab]) for ab in IDX]}, det h = {dR1}")

# ---- C5: H at specialized (u1, u3, u4): the N'_22 coefficients generate (2u0 - u1, (u1 + u2)^2) in Q[u0, u2] ----
U0, U2 = sp.symbols("U0 U2")
outH = []
okH = True
for trial in range(3):
    a1, a3, a4 = sp.Rational(rnd.randint(1, 9), rnd.randint(1, 5)) * rnd.choice([1, -1]), rq(), rq()
    Np, _ = N_polar(1, c, S, [U0, a1, U2, a3, a4])
    n22 = circ(Np[2, 2])
    q, r_ = sp.div(sp.Poly(n22, c, S), sp.Poly((1 - c ** 2) ** 3, c, S))
    assert r_.is_zero, "N_theta_theta not divisible by (1 - c^2)^3"
    gens = [sp.expand(co) for co in sp.Poly(q.as_expr(), c, S).coeffs()]
    gb = sp.groebner(gens, U0, U2, order="lex")
    want = sp.groebner([2 * U0 - a1, (a1 + U2) if MUT == "H-b" else (a1 + U2) ** 2], U0, U2, order="lex")
    same = list(gb.exprs) == list(want.exprs)
    okH &= same
    outH.append((str(a1), str(a3), str(a4), len(gens), [str(e) for e in gb.exprs], same))
report("C5", okH, f"(u1, u3, u4), number of N'_22 coefficients, reduced lex basis in (u0, u2), equal to (a, b^2): {outH}")

# ---- C6: the ODE step without Singular: 2w = r w' and r w' + r^2 w'' = 0 on an interval force w' = 0 ----
r_ = sp.symbols("r", positive=True)
wf = sp.Function("w")
sol = sp.dsolve(sp.Eq(2 * wf(r_) - r_ * wf(r_).diff(r_), 0), wf(r_)).rhs
second = (r_ * sol.diff(r_) - r_ ** 2 * sol.diff(r_, 2)) if MUT == "ode" else (r_ * sol.diff(r_) + r_ ** 2 * sol.diff(r_, 2))
const = [s_ for s_ in sol.free_symbols if s_ != r_]
cs = sp.solve(sp.Poly(sp.expand(second), r_).coeffs(), const, dict=True)
forced = [sp.simplify(sol.diff(r_).subs(cc_)) for cc_ in cs] if cs else []
okode = bool(cs) and all(f == 0 for f in forced) and sp.simplify(sp.expand(second)) != 0
report("C6", okode, f"2w = r w' gives w = {sol}; then r w' + r^2 w'' = {sp.simplify(second)}, which vanishes on an "
       f"interval only for {cs}, so w' = {forced}")

# ---- C7: weights N(r0; W) = r0^m N(1; r0^k W_k), m from the homothety (t, x, rho) -> r0 (t, x, rho) ----
m = {(0, 0): -10, (0, 1): -10, (0, 2): -9, (1, 1): -10, (1, 2): -9, (2, 2): -9 if MUT == "weight" else -8}
badw = []
for (r0, cc, SS) in [(2, sp.Rational(3, 5), sp.Rational(4, 5)), (sp.Rational(3, 2), sp.Rational(-5, 13), sp.Rational(12, 13))]:
    W = [rq() for _ in range(5)]
    Na, _ = N_polar(r0, cc, SS, W)
    Nb, _ = N_polar(1, cc, SS, [sp.Rational(r0) ** k * W[k] for k in range(5)])
    for ab in IDX:
        if sp.simplify(Na[ab] - sp.Rational(r0) ** m[ab] * Nb[ab]) != 0:
            badw.append((str(r0), ab))
report("C7", not badw, f"at r0 = 2 and 3/2 with random jets, all six components: failures {badw}")

failed = [n for n, ok in RESULTS if not ok]
print(f"checks: {len(RESULTS) - len(failed)} passed, {len(failed)} failed {failed}. mutation: {MUT}. {time.time() - T0:.0f} s")
sys.exit(1 if failed else 0)
