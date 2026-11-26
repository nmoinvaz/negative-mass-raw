#!/usr/bin/env python3
"""ind167: the coordinator's independent check of #167 (criteria in README.md beside this file).

Own N = 8 det(block) for a conical shift, own coefficient and monomial analysis, own inward integration with root
tracking in mpmath. Imports nothing from the negative-mass repository and does not use the Rust crate.

    python3 ind167.py [--mutate=NAME]
"""
import argparse
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["d-sign", "eta0-coef", "even-b", "balance-coef", "start-C"])
MUT = ap.parse_args().mutate
T0 = time.time()
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def info(text):
    print(f"[info] {text} ({time.time() - T0:.0f} s)", flush=True)


F, F1, F2, eta = sp.symbols("F F1 F2 eta")


def build_N(mutated):
    w = F1 + eta * F2
    P_, Q_, Z_ = -(F1**2 + F * F2), -eta * w / 2, -w / 2
    Y_ = -(eta * F1**2 + (-1 if mutated else 1) * F * w / 2)
    h_ = eta**2 * F1**2 / 2
    B = sp.Matrix([[P_ - h_, Q_, Z_], [Q_, -P_ - h_, Y_], [Z_, Y_, h_]])
    return sp.expand(8 * B.det())


N = build_N(MUT == "d-sign")
N_ref = build_N(False)  # L5 integrates the unmutated N, so that d-sign's effect stays on L1 to L4
info("N built")

a3 = 2 * F * eta**2 * (F**2 - eta**2 - 1)
a2 = F1 * eta * (4 * F**3 + F**2 * F1 * eta**3 + 6 * F**2 * F1 * eta - 6 * F * eta**2 - 4 * F - F1 * eta**5
                 - 3 * F1 * eta**3 - 2 * F1 * eta)
a1 = 2 * F1**2 * (F**3 + F**2 * F1 * eta**3 + 6 * F**2 * F1 * eta + 2 * F * F1**2 * eta**4 + 4 * F * F1**2 * eta**2
                  - 3 * F * eta**2 - F - F1 * eta**5 - 3 * F1 * eta**3 - 2 * F1 * eta)
a0 = F1**3 * (F**2 * F1 * eta**2 + 2 * F**2 * F1 + 4 * F * F1**2 * eta**3 + 8 * F * F1**2 * eta - 2 * F * eta
              + F1**3 * eta**6 + 4 * F1**3 * eta**4 + 4 * F1**3 * eta**2 - F1 * eta**4 - 3 * F1 * eta**2 - 2 * F1)
N_note = sp.expand(a3 * F2**3 + a2 * F2**2 + a1 * F2 + a0)


def l1():
    ok = sp.expand(N - N_note) == 0
    check("L1", ok, f"8 det(block) = a3 F''^3 + a2 F''^2 + a1 F'' + a0 of the note: {ok}")


def l2():
    k = 3 if MUT == "eta0-coef" else 2
    n0 = sp.expand(N.subs(eta, 0))
    ok1 = sp.expand(n0 - k * F1**2 * (F**2 - 1) * (F * F2 + F1**2)) == 0
    ok2 = sp.expand(sp.diff(N, F2).subs(eta, 0) - 2 * F1**2 * F * (F**2 - 1)) == 0
    check("L2", ok1 and ok2, f"N(eta = 0) = {k} F'^2 (F^2 - 1)(F F'' + F'^2): {ok1}; dN/dF'' at 0 = 2F'^2 F (F^2 - 1): {ok2}")


def series_coeffs(Fexpr):
    Nx = sp.expand(N.subs({F: Fexpr, F1: sp.diff(Fexpr, eta), F2: sp.diff(Fexpr, eta, 2)}))
    return sp.Poly(Nx, eta)


def l3():
    Bs, B3 = sp.symbols("B B3")
    p = series_coeffs(1 + sp.Rational(2, 5) * eta**2 + Bs * eta**4 + B3 * eta**6)
    coeffs = {m[0]: c for m, c in p.terms()}
    kB = min(k for k, c in coeffs.items() if c.has(Bs))
    cB = sp.expand(coeffs[kB])
    ok_lin = sp.Poly(cB, Bs).degree() == 1 and not cB.has(B3)
    solB = sp.solve(cB, Bs)
    wantB = sp.Rational(-21, 125) if MUT == "even-b" else sp.Rational(-22, 125)
    okB = ok_lin and len(solB) == 1 and solB[0] == wantB
    coeffs2 = {k: sp.expand(c.subs(Bs, sp.Rational(-22, 125))) for k, c in coeffs.items()}
    k3 = min(k for k, c in coeffs2.items() if c.has(B3))
    c3 = coeffs2[k3]
    ok_lin3 = sp.Poly(c3, B3).degree() == 1
    sol3 = sp.solve(c3, B3)
    ok3 = ok_lin3 and len(sol3) == 1 and sol3[0] == sp.Rational(998, 10625)
    b = sp.Symbol("b")
    pb = series_coeffs(1 + b * eta**2)
    c4 = pb.coeff_monomial(eta**4)
    ok4 = sp.expand(c4 - 64 * b**3 * (5 * b - 2)) == 0
    check("L3", okB and ok3 and ok4, f"B first at eta^{kB}: linear {ok_lin}, solution {solB} (want {wantB}): {okB}; "
          f"B3 first at eta^{k3}: solution {sol3} (want 998/10625): {ok3}; eta^4 coefficient for F = 1 + b eta^2 = "
          f"64 b^3 (5b - 2): {ok4}")


def l4():
    p = sp.Poly(N, F, F1, F2)
    bal = 0
    ok_rest = True
    bad = []
    for (i, j, k), c in p.terms():
        d, s = i + j + k, j + 2 * k
        if d == 4 and s == 6:
            bal += c * F**i * F1**j * F2**k
        elif not (d >= 4 and s <= 6):
            ok_rest = False
            bad.append((i, j, k))
    m = 3 if MUT == "balance-coef" else 2
    claim = -eta**2 * (eta**2 + 1) * F2**2 * ((eta**2 + m) * F1**2 + 2 * F * F2)
    ok_bal = sp.expand(bal - claim) == 0
    al, es = sp.symbols("alpha etastar", positive=True)
    # F ~ c D^alpha: (eta^2 + 2) F'^2 + 2 F F'' ~ c^2 D^(2 alpha - 2) alpha ((eta^2 + 4) alpha - 2)
    expo = sp.factor((es**2 + 2) * al**2 + 2 * al * (al - 1))
    ok_al = sp.solve(expo, al) == [2 / (es**2 + 4)]
    check("L4", ok_bal and ok_rest and ok_al, f"balance = -eta^2(eta^2 + 1)F''^2[(eta^2 + {m})F'^2 + 2FF'']: {ok_bal}; "
          f"every other monomial has d >= 4 and j + 2k <= 6: {ok_rest}{'' if ok_rest else ' ' + str(bad[:5])}; "
          f"alpha = 2/(eta*^2 + 4): {ok_al}")


def l5():
    mp.mp.dps = 30
    coef = [sp.lambdify((F, F1, eta), sp.Poly(N_ref, F2).coeff_monomial(F2**k), "mpmath") for k in (3, 2, 1, 0)]
    Cc = mp.mpf(10) if MUT == "start-C" else mp.mpf(0)
    # own formal series through nu^8 with logs (README A2): stages solved here from N in theta-variables
    G_, P_, Q_, nu_, L_ = sp.symbols("G p q nu L")
    Nth = sp.expand(N_ref.subs({F1: P_ * nu_, F2: (Q_ - P_) * nu_**2}).subs(eta, 1 / nu_).subs(F, G_))
    Nth = sp.expand(sp.cancel(Nth))
    unk = {(6, j): sp.Symbol(f"a6{j}") for j in range(4)}
    unk.update({(8, j): sp.Symbol(f"a8{j}") for j in range(5)})
    Fi, Ci = sp.Integer(1), sp.Integer(10) if MUT == "start-C" else sp.Integer(0)
    terms = {(2, 0): -2 * Fi, (4, 0): Ci, (4, 1): Fi * (Fi**2 + 7)}
    terms.update(unk)

    def theta(expr):  # theta = eta d/deta on polynomials in nu and L = ln eta
        return sp.expand(-nu_ * sp.diff(expr, nu_) + sp.diff(expr, L_))

    Gs = Fi + sum(c * nu_**n * L_**j for (n, j), c in terms.items())
    Ps = theta(Gs)
    Qs = theta(Ps)
    Ns = sp.expand(Nth.subs({G_: Gs, P_: Ps, Q_: Qs}))
    pN = sp.Poly(Ns, nu_, L_)
    eqs = {}
    for (kn, kl), c in pN.terms():
        if kn <= 14:
            eqs.setdefault(kn, []).append(c)
    sol = {}
    for kn in sorted(eqs):
        es = [sp.expand(e.subs(sol)) for e in eqs[kn]]
        es = [e for e in es if e != 0]
        if not es:
            continue
        free = sorted({s for e in es for s in e.free_symbols if s in unk.values()}, key=str)
        if not free:
            raise ValueError(f"inconsistent series at nu^{kn}: {es[:2]}")
        s_ = sp.solve(es, free, dict=True)
        if len(s_) != 1:
            raise ValueError(f"series stage nu^{kn}: {len(s_)} solutions")
        sol.update(s_[0])
    left = [u for u in unk.values() if u not in sol]
    sol.update({u: 0 for u in left})  # unknowns no equation through nu^14 reaches are set to 0 and reported
    info(f"own series through nu^8: {dict((str(k), str(v)) for k, v in sol.items())}; unset {[str(u) for u in left]}")
    Gser = sp.lambdify((nu_, L_), Gs.subs(sol), "mpmath")
    Pser = sp.lambdify((nu_, L_), Ps.subs(sol), "mpmath")
    Qser = sp.lambdify((nu_, L_), Qs.subs(sol), "mpmath")
    e0 = mp.mpf(200)

    def ser(x):
        nv, Lv = 1 / x, mp.log(x)
        g, pp, qq = Gser(nv, Lv), Pser(nv, Lv), Qser(nv, Lv)
        return g, pp / x, (qq - pp) / x**2

    def root(f, f1, x, ref):
        cs = [c(f, f1, x) for c in coef]
        rts = mp.polyroots(cs, maxsteps=200, extraprec=60)
        real = [mp.re(r) for r in rts if abs(mp.im(r)) <= mp.mpf(10) ** -12 * max(1, abs(r))]
        if not real:
            raise ValueError("no real root")
        return min(real, key=lambda r: abs(r - ref))

    f, f1, f2s = ser(e0)
    f2 = root(f, f1, e0, f2s)
    x = e0
    hist = []
    try:
        for it in range(200000):
            # step in t = ln eta, inward; |dt| limited so that F changes by at most 2 percent
            dF_dt = x * f1
            dt = -min(mp.mpf(1) / 400, mp.mpf("0.02") * abs(f) / max(abs(dF_dt), mp.mpf(10) ** -30))
            ref = f2

            def rhs(xx, ff, gg):
                hh = root(ff, gg, xx, ref)
                return xx * gg, xx * hh, hh  # dF/dt, dF'/dt, F''

            k1 = rhs(x, f, f1)
            x2 = x * mp.exp(dt / 2)
            k2 = rhs(x2, f + dt / 2 * k1[0], f1 + dt / 2 * k1[1])
            k3 = rhs(x2, f + dt / 2 * k2[0], f1 + dt / 2 * k2[1])
            x4 = x * mp.exp(dt)
            k4 = rhs(x4, f + dt * k3[0], f1 + dt * k3[1])
            f = f + dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            f1 = f1 + dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            x = x4
            f2 = root(f, f1, x, k4[2])
            hist.append((x, f))
            if f < mp.mpf(10) ** -4 or x < mp.mpf(10) ** -6:
                break
        (xa, fa), (xb, fb) = hist[-2], hist[-1]
        alpha = 2 / (xb**2 + 4)
        ya, yb = fa ** (1 / alpha), fb ** (1 / alpha)
        estar = xb - yb * (xa - xb) / (ya - yb)
        ok = fb < mp.mpf(10) ** -4 and abs(estar - mp.mpf("1.28193326312")) <= mp.mpf(10) ** -4
        check("L5", ok, f"(F_inf, C) = (1, {mp.nstr(Cc, 3)}): walk ends at eta = {mp.nstr(xb, 12)} with F = {mp.nstr(fb, 3)}, "
              f"eta* = {mp.nstr(estar, 12)} (want 1.28193326312 within 1e-4): {ok}; {len(hist)} steps")
    except (ValueError, ZeroDivisionError) as e:
        check("L5", False, f"walk stopped at eta = {mp.nstr(x, 8)}, F = {mp.nstr(f, 4)}: {e}")


print(f"ind167.py  mutate={MUT}", flush=True)
for fn in (l1, l2, l3, l4, l5):
    t1 = time.time()
    fn()
    info(f"{fn.__name__} done in {time.time() - t1:.0f} s")
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad} ({time.time() - T0:.0f} s)", flush=True)
sys.exit(1 if bad else 0)
