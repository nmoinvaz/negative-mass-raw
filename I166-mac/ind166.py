#!/usr/bin/env python3
"""ind166: the coordinator's independent check of #166 (criteria in README.md beside this file).

Own Ricci tensor from Christoffel symbols for ds^2 = -dt^2 + (dx + b dt)^2 + drho^2 + rho^2 dphi^2; the branch A family
identity, the stage at exact points, Lemma Z by elimination, the closure bracket, branch B and the c-ODE. Imports nothing
from the negative-mass repository.

    python3 ind166.py [--mutate=NAME]
"""
import argparse
import sys
import time

import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None,
                choices=["plant-K2", "ode-flip", "t1-pert", "lemz-sign", "bracket-drop", "sep-swap", "ode-k"])
MUT = ap.parse_args().mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def info(text):
    print(f"[info] {text} ({time.time() - T0:.0f} s)", flush=True)


t, x, rho, phi = sp.symbols("t x rho phi", real=True)
X = (t, x, rho, phi)


def metric(b):
    g = sp.zeros(4, 4)
    g[0, 0] = -1 + b**2
    g[0, 1] = g[1, 0] = b
    g[1, 1] = 1
    g[2, 2] = 1
    g[3, 3] = rho**2
    return g


def ricci(g, simp=sp.cancel):
    gi = sp.simplify(g.inv())
    Gam = [[[simp(sum(gi[a, d] * (sp.diff(g[d, c], X[bb]) + sp.diff(g[d, bb], X[c]) - sp.diff(g[bb, c], X[d]))
                      for d in range(4)) / 2) for c in range(4)] for bb in range(4)] for a in range(4)]
    R = sp.zeros(4, 4)
    for bb in range(4):
        for d in range(bb, 4):
            e = 0
            for a in range(4):
                e += sp.diff(Gam[a][bb][d], X[a]) - sp.diff(Gam[a][bb][a], X[d])
                for k in range(4):
                    e += Gam[a][a][k] * Gam[k][bb][d] - Gam[a][d][k] * Gam[k][bb][a]
            R[bb, d] = R[d, bb] = simp(e)
    return R


# ----------------------------------------------------------------------------------------------------------------------
# P0: planted b = x
# ----------------------------------------------------------------------------------------------------------------------

def p0():
    g = metric(x)
    R = ricci(g)
    want = g.copy()
    want[2, 2] = 0
    want[3, 3] = 0
    if MUT == "plant-K2":
        want = 2 * want
    ok = sp.simplify(R - want) == sp.zeros(4, 4)
    check("P0", ok, f"b = x: Ricci = g restricted to (t, x): {ok}; R = {R.tolist()}")


# ----------------------------------------------------------------------------------------------------------------------
# J1, J4: the branch A family with undefined c, C, d
# ----------------------------------------------------------------------------------------------------------------------

c, C, d = (sp.Function(n)(t) for n in ("c", "C", "d"))
gam = C.diff(t) / (2 * C)
w = gam - c
lam = C**2 / (2 * rho**2) + w**2
bA = c * x + C * sp.log(rho) + d


def ode_subs(expr, flip=False):
    rhs = 2 * gam * c + (1 if flip else -1) * gam**2
    rhs2 = sp.diff(rhs, t).subs(c.diff(t), rhs)
    return expr.subs(c.diff(t, 2), rhs2).subs(c.diff(t), rhs)


t1 = time.time()
gA = metric(bA)
RA = ricci(gA)
info(f"Ricci of the branch A family ({time.time() - t1:.0f} s)")


def target_A():
    alpha = sp.Matrix([C / rho * bA, C / rho, w, 0])
    G = gA.copy()
    G[3, 3] = 0
    return lam * G - alpha * alpha.T


def j1():
    diff = (ode_subs(RA, flip=(MUT == "ode-flip")) - target_A()).applyfunc(lambda e: sp.simplify(sp.expand(e)))
    ok = diff == sp.zeros(4, 4)
    nz = [(i, j) for i in range(4) for j in range(i, 4) if diff[i, j] != 0]
    check("J1", ok, f"R_ab - [lam (g - rho^2 dphi^2) - alpha alpha] = 0 with c' = 2 gam c - gam^2: {ok}"
          + ("" if ok else f"; nonzero entries {nz}"))


def bracket(Xv, Yv, drop=False):
    out = []
    for mu in range(4):
        e = sum(Xv[nu] * sp.diff(Yv[mu], X[nu]) for nu in range(4))
        if not drop:
            e -= sum(Yv[nu] * sp.diff(Xv[mu], X[nu]) for nu in range(4))
        out.append(sp.simplify(e))
    return out


def j4():
    M = ode_subs(RA) - lam * gA
    nv = sp.Matrix([1, -bA, 0, 0])
    K2 = sp.Matrix([0, w, -C / rho, 0])
    ok_a = (M * nv).applyfunc(lambda e: sp.simplify(sp.expand(e))) == sp.zeros(4, 1) and \
        (M * K2).applyfunc(lambda e: sp.simplify(sp.expand(e))) == sp.zeros(4, 1)
    br = bracket(list(nv), list(K2), drop=(MUT == "bracket-drop"))
    res = [sp.simplify(br[i] - C.diff(t) / C * K2[i]) for i in range(4)]
    r = sp.diff(w, t) + w * c - 2 * gam * w - C**2 / rho**2
    ok_b = res[0] == 0 and res[2] == 0 and res[3] == 0 and sp.simplify(res[1] - r) == 0
    ok_c = sp.simplify(sp.diff(r, rho) - 2 * C**2 / rho**3) == 0
    check("J4", ok_a and ok_b and ok_c, f"(a) M n = 0 and M K2 = 0: {ok_a}; (b) [n, K2] - (C'/C) K2 = r d_x with "
          f"r = w' + w c - 2 gam w - C^2/rho^2: {ok_b}; d_rho r = 2 C^2/rho^3: {ok_c}")


# ----------------------------------------------------------------------------------------------------------------------
# J2: the stage at exact points
# ----------------------------------------------------------------------------------------------------------------------

def stage_member(b, Cexpr, cexpr, pts):
    g = metric(b)
    R = ricci(g)
    out = []
    for x0 in pts:
        at = {t: 0, rho: 1, x: x0}
        Rn = R.subs(at).applyfunc(sp.nsimplify)
        gn = g.subs(at).applyfunc(sp.nsimplify)
        Cv = sp.nsimplify(Cexpr.subs(t, 0))
        gv = sp.nsimplify((sp.diff(Cexpr, t) / (2 * Cexpr)).subs(t, 0))
        cv = sp.nsimplify(cexpr.subs(t, 0))
        l0 = Cv**2 / 2 + (gv - cv)**2
        out.append((Rn, gn, l0))
    return out


def j2():
    lam_s = sp.Symbol("lam")
    xs = sp.Symbol("X")
    pts = (sp.Rational(1, 3), -2, 5)
    members = {
        "T1": (x / 2 + sp.exp(2 * t) * sp.log(rho), sp.exp(2 * t), sp.Rational(1, 2)),
        "T2": ((sp.Rational(1, 2) + sp.exp(2 * t) / 3) * x + sp.exp(2 * t) * sp.log(rho), sp.exp(2 * t),
               sp.Rational(1, 2) + sp.exp(2 * t) / 3),
        "T4'": (-x / (t - 1) + sp.log(rho) / (t - 1)**2, 1 / (t - 1)**2, -1 / (t - 1)),
        "S": (sp.Rational(3, 2) * x + 2 * sp.log(rho) + sp.Rational(1, 5), sp.Integer(2), sp.Rational(3, 2)),
    }
    if MUT == "t1-pert":
        b1, C1, c1 = members["T1"]
        members["T1"] = (b1 + x**2 / 10, C1, c1)
    ok_all, notes = True, []
    for name, (b, Ce, ce) in members.items():
        for Rn, gn, l0 in stage_member(b, Ce, ce, pts):
            M = Rn - l0 * gn
            cp = sp.Poly(M.charpoly(xs).as_expr(), xs)
            co = cp.all_coeffs()  # x^4 + a3 x^3 + a2 x^2 + a1 x + a0
            ok = len(co) == 5 and co[3] == 0 and co[4] == 0 and -co[1] < 0 < co[2]
            ok_all &= ok
            if not ok:
                notes.append(f"{name}: lam0 = {l0}, charpoly {cp.as_expr()}")
    # F1 rejected: the 3x3 minors of R - lam g have no common root other than lam = 0
    F1 = members["S"][0] + x**2 / 10
    g = metric(F1)
    R = ricci(g)
    rej = True
    for x0 in pts:
        at = {t: 0, rho: 1, x: x0}
        M = (R.subs(at).applyfunc(sp.nsimplify) - lam_s * g.subs(at).applyfunc(sp.nsimplify))
        mins = [sp.Poly(M.extract([i for i in range(4) if i != r_], [j for j in range(4) if j != c_]).det(), lam_s)
                for r_ in range(4) for c_ in range(4)]
        gg = mins[0]
        for m_ in mins[1:]:
            gg = sp.gcd(gg, m_)
        if len(gg.terms()) != 1:  # the gcd is c lam^k (or a constant) exactly when it has one term
            rej = False
            notes.append(f"F1 at x = {x0}: gcd of minors {gg.as_expr()}")
    check("J2", ok_all and rej, f"T1, T2, T4', S at t = 0, rho = 1, x in {list(pts)}: charpoly of R - lam0 g is "
          f"X^2 (X^2 - tau X + e), tau < 0 < e: {ok_all}; F1 = S + x^2/10 has no common root of the minors: {rej}"
          + ("" if ok_all and rej else "; " + "; ".join(notes)))


# ----------------------------------------------------------------------------------------------------------------------
# J3: Lemma Z by elimination
# ----------------------------------------------------------------------------------------------------------------------

def j3():
    P, Q, Y, h, v0, v1, v2 = sp.symbols("P Q Y h v0 v1 v2")
    gA_ = sp.groebner([P + v2**2, Q, Y + v1 * v2, 2 * h - v1**2], v1, v2, P, Q, Y, h, order="lex")
    eA = [e for e in gA_.exprs if not ({v1, v2} & e.free_symbols)]
    gB_ = sp.groebner([P + v0**2, Q + v0 * v1, Y, 2 * h - v0**2 - v1**2], v0, v1, P, Q, Y, h, order="lex")
    eB = [e for e in gB_.exprs if not ({v0, v1} & e.free_symbols)]
    wantA = [Q, 2 * h * P + (-1 if MUT == "lemz-sign" else 1) * Y**2]
    wantB = [Y, Q**2 + P * (2 * h + P)]
    red = lambda L: list(sp.groebner(L, P, Q, Y, h, order="grevlex").exprs)
    okA = red(eA) == red(wantA)
    okB = red(eB) == red(wantB)
    check("J3", okA and okB, f"v0 = 0: elimination ideal {eA}, = <Q, 2hP + Y^2>: {okA}; v2 = 0: {eB}, = "
          f"<Y, Q^2 + P(2h + P)>: {okB}")


# ----------------------------------------------------------------------------------------------------------------------
# J5: branch B
# ----------------------------------------------------------------------------------------------------------------------

def j5():
    kap, e_, m, r0 = (sp.Function(n)(t) for n in ("kappa", "e", "m", "r0"))
    F = sp.Function("F")(rho)
    f = F.diff(rho)
    b = kap * x + e_ + m * F + r0
    bx, brho = sp.diff(b, x), sp.diff(b, rho)
    n_ = lambda q: sp.diff(q, t) - b * sp.diff(q, x)
    P = sp.simplify(n_(bx) - bx**2)
    Q = -(sp.diff(b, rho, 2) + brho / rho) / 2
    Y = -n_(brho) / 2 + bx * brho
    h = brho**2 / 2
    okY = sp.simplify(Y - (-m.diff(t) / 2 + kap * m) * f) == 0
    p = kap**2 - kap.diff(t)
    gq = (f.diff(rho) + f / rho)**2 / 4
    E = (Q**2 + P * (2 * h + P)).subs(m.diff(t), 2 * kap * m)
    okE = sp.simplify(sp.expand(E - (m**2 * gq - p * m**2 * f**2 + p**2))) == 0
    ps, M2, ga, gb, Fa, Fb = sp.symbols("p M2 g_a g_b F_a F_b")
    sols = sp.solve([M2 * ga - ps * M2 * Fa + ps**2, M2 * gb - ps * M2 * Fb + ps**2], [ps, M2], dict=True)
    nontriv = [s_ for s_ in sols if sp.simplify(s_.get(ps, ps)) != 0 and sp.simplify(s_.get(M2, M2)) != 0]
    pw = (ga - gb) / ((Fb - Fa) if MUT == "sep-swap" else (Fa - Fb))
    okS = len(nontriv) >= 1 and all(sp.simplify(s_[ps] - pw) == 0 and t not in s_[M2].free_symbols for s_ in nontriv)
    check("J5", okY and okE and okS, f"(a) Y = (-m'/2 + kappa m) f: {okY}; at m' = 2 kappa m, Q^2 + P(2h + P) = m^2 g - "
          f"p m^2 f^2 + p^2: {okE}; (b) solve for (p, m^2) with p, m^2 != 0: {nontriv}, p = (g_a - g_b)/(F_a - F_b): {okS}")


# ----------------------------------------------------------------------------------------------------------------------
# J6: the c-ODE
# ----------------------------------------------------------------------------------------------------------------------

def j6():
    cf = sp.Function("cf")
    s1 = sp.dsolve(sp.Eq(cf(t).diff(t), 2 * cf(t) - 1), cf(t)).rhs
    base1 = -sp.Rational(1, 2) if MUT == "ode-k" else sp.Rational(1, 2)
    ok1 = t not in sp.simplify((s1 - base1) / sp.exp(2 * t)).free_symbols
    T1c, T2c = sp.Rational(1, 2), sp.Rational(1, 2) + sp.exp(2 * t) / 3
    ok1m = all(sp.simplify(q.diff(t) - (2 * q - 1)) == 0 for q in (T1c, T2c))
    s2 = sp.dsolve(sp.Eq(cf(t).diff(t), -2 * cf(t) / t - 1 / t**2), cf(t)).rhs
    ok2 = t not in sp.simplify((s2 + 1 / t) * t**2).free_symbols
    T4c = -1 / t
    ok2m = sp.simplify(T4c.diff(t) - (-2 * T4c / t - 1 / t**2)) == 0
    Cp = sp.Function("Cp", positive=True)(t)
    K = sp.Function("K")(t)
    k0 = sp.Symbol("k0")
    gp = Cp.diff(t) / (2 * Cp)
    cc = Cp * (k0 - K)
    res = (cc.diff(t) - 2 * gp * cc + gp**2).subs(K.diff(t), gp**2 / Cp)
    ok3 = sp.simplify(res) == 0
    check("J6", ok1 and ok1m and ok2 and ok2m and ok3, f"c' = 2c - 1: dsolve {s1}, = 1/2 + k e^(2t): {ok1}, T1, T2 solve "
          f"it: {ok1m}; c' = -2c/t - 1/t^2: dsolve {s2}, = -1/t + k/t^2: {ok2}, T4 solves it: {ok2m}; c = |C|(k0 - K) "
          f"solves c' = 2 gam c - gam^2: {ok3}")


print(f"ind166.py  mutate={MUT}", flush=True)
for fn in (p0, j1, j2, j3, j4, j5, j6):
    t1 = time.time()
    fn()
    info(f"{fn.__name__} done in {time.time() - t1:.0f} s")
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
