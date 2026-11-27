#!/usr/bin/env python3
"""ind262b (amendment A1): is Y = R e^{K(t + x)}, K = -2c/pi, an exact linear radial solution of the black universes?

Static gauge dg_trho = 0, dphi = 0. ds^2 = -A(1 + H0) dt^2 + (1 + H2) drho^2/A + (R + Y)^2 dOmega^2, the linearized
R_ab = eps phi_a phi_b + V g_ab and eps box phi = V'(phi) from a brute-force Ricci tensor. Y = R Q T, H0 = a Q T, H2 = b Q T with
T = e^{Wt}, Q = e^{Kx} (Q' = K Q / A). b from E_trho, a' from the scalar equation, a from E_rhorho; residuals: a' against d a/drho,
E_tt, E_thth. W = K unless mutated.

    python3 ind262b.py [--mutate=w-off|r-to-rho|k-kappa]
"""
import sys
import time

import mpmath as mp
import sympy as sp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
mp.mp.dps = 40
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


t0 = time.time()
t, rho, th, phv = sp.symbols("t rho theta varphi", real=True)
c, W, e = sp.symbols("c W e")
s2 = sp.sqrt(2)
eps = -1
K = -2 * c / sp.pi
A = 1 + c * (rho ** 2 + 1) + K * (rho + (rho ** 2 + 1) * sp.atan(rho))
R = sp.sqrt(1 + rho ** 2)
P = s2 * sp.atan(rho)
ph = sp.Symbol("ph")
psi = ph / s2
Vf = -c * (3 - 2 * sp.cos(psi) ** 2) - K * (3 * sp.sin(psi) * sp.cos(psi) + psi * (3 - 2 * sp.cos(psi) ** 2))
Vp = sp.diff(Vf, ph)

Qf, af, bf = sp.Function("Q")(rho), sp.Function("a")(rho), sp.Function("b")(rho)
T = sp.exp(W * t)
fr = rho if MUT == "r-to-rho" else R
H0, H2, Y = e * af * Qf * T, e * bf * Qf * T, e * fr * Qf * T
X = [t, rho, th, phv]
g = sp.diag(-A * (1 + H0), (1 + H2) / A, (R + Y) ** 2, (R + Y) ** 2 * sp.sin(th) ** 2)


def lin(expr):
    return sp.diff(expr, e).subs(e, 0)


gi = g.inv()
dim = 4
# Christoffels and Ricci, linearized at the end
Gam = [[[sum(gi[a_, d] * (sp.diff(g[d, b_], X[c_]) + sp.diff(g[d, c_], X[b_]) - sp.diff(g[b_, c_], X[d])) for d in range(dim)) / 2
         for c_ in range(dim)] for b_ in range(dim)] for a_ in range(dim)]


def ric(b_, d_):
    s = sum(sp.diff(Gam[a_][b_][d_], X[a_]) - sp.diff(Gam[a_][b_][a_], X[d_]) for a_ in range(dim))
    s += sum(Gam[a_][a_][k] * Gam[k][b_][d_] - Gam[a_][d_][k] * Gam[k][b_][a_] for a_ in range(dim) for k in range(dim))
    return s


phi = P                                         # dphi = 0
dphi = [sp.diff(phi, x) for x in X]
Vphi = Vf.subs(ph, phi)
Eq = {}
for nm, (i, j) in {"tt": (0, 0), "tr": (0, 1), "rr": (1, 1), "thth": (2, 2)}.items():
    Eq[nm] = lin(ric(i, j) - eps * dphi[i] * dphi[j] - Vphi * g[i, j])
sq = sp.sqrt(-g.det())
box = sum(sp.diff(sq * gi[a_, b_] * dphi[b_], X[a_]) for a_ in range(dim) for b_ in range(dim)) / sq
Eq["scal"] = lin(eps * box - Vp.subs(ph, phi))
print(f"  linearized equations built ({time.time() - t0:.0f} s)", flush=True)

# substitute Q' = K Q / A (and its derivatives), divide by Q T, and name a, b and their derivatives
Kq = sp.Symbol("kap") if MUT == "k-kappa" else K
Wv = Kq * (1 + sp.Rational(1, 1000)) if MUT == "w-off" else Kq
q1 = Kq * Qf / A
q2 = sp.diff(q1, rho).subs(sp.Derivative(Qf, rho), q1)
a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")


def reduce(expr):
    ex = expr.subs(W, Wv).doit()
    ex = ex.subs(sp.Derivative(Qf, (rho, 2)), q2).subs(sp.Derivative(Qf, rho), q1)
    ex = ex.subs({sp.Derivative(af, (rho, 2)): a2, sp.Derivative(af, rho): a1, af: a0,
                  sp.Derivative(bf, (rho, 2)): b2, sp.Derivative(bf, rho): b1, bf: b0})
    ex = ex / (Qf * T)
    return sp.expand(ex)


Rd = {k: reduce(v) for k, v in Eq.items()}
for k, v in Rd.items():
    assert not v.has(Qf), k
print(f"  reduced ({time.time() - t0:.0f} s); unknowns in each: " +
      ", ".join(f"{k}: {sorted(str(s) for s in v.free_symbols & {a0, a1, a2, b0, b1, b2})}" for k, v in Rd.items()), flush=True)

# solve: b0 from E_tr (it has no a; b1 if present is handled by the derivative of the solution)
bsol = sp.solve(Rd["tr"], b0)
assert len(bsol) == 1, bsol
bsol = bsol[0]
assert not bsol.has(b1) and not bsol.has(a0), bsol.free_symbols
b1sol = sp.diff(bsol, rho)
b2sol = sp.diff(b1sol, rho)
sub_b = {b0: bsol, b1: b1sol, b2: b2sol}
sc = Rd["scal"].subs(sub_b)
a1sol = sp.solve(sc, a1)
assert len(a1sol) == 1
a1sol = a1sol[0]
rr = Rd["rr"].subs(sub_b).subs(a1, a1sol)
a0sol = sp.solve(rr, a0)
assert len(a0sol) == 1
a0sol = a0sol[0]
a1sol = a1sol.subs(a0, a0sol)
a2sol = sp.diff(a1sol, rho)
resid = {
    "a' consistency": sp.diff(a0sol, rho) - a1sol,
    "E_tt": Rd["tt"].subs(sub_b).subs({a2: a2sol, a1: a1sol, a0: a0sol}),
    "E_thth": Rd["thth"].subs(sub_b).subs({a2: a2sol, a1: a1sol, a0: a0sol}),
}
scales = {
    "a' consistency": a1sol,
    "E_tt": Rd["tt"].subs(sub_b).subs({a2: 0, a1: 0, a0: 0}),
    "E_thth": Rd["thth"].subs(sub_b).subs({a2: 0, a1: 0, a0: 0}),
}
print(f"  solved ({time.time() - t0:.0f} s)", flush=True)


def kappa_of(cval):
    cm = mp.mpf(cval)
    Kc = -2 * cm / mp.pi
    Af = lambda y: 1 + cm * (y * y + 1) + Kc * (y + (y * y + 1) * mp.atan(y))  # noqa: E731
    rh = mp.findroot(Af, mp.mpf(0) if cval == -1 else mp.mpf("0.5"))
    return rh, mp.diff(Af, rh) / 2


res_all = {}
cases = (-1, sp.Rational(-3, 10), sp.Rational(-3, 2), -10)
for cv in cases:
    rh, kap = kappa_of(float(cv))
    fns = {k: sp.lambdify(rho, v.subs(c, cv).subs(sp.Symbol("kap"), kap), "mpmath") for k, v in resid.items()}
    fsc = {k: sp.lambdify(rho, v.subs(c, cv).subs(sp.Symbol("kap"), kap), "mpmath") for k, v in scales.items()}
    pts = [rh + mp.mpf(d) for d in ("0.05", "0.2", "0.5", "1", "2", "4", "8", "15")]
    if cv == -1:
        pts += [mp.mpf(d) for d in ("-0.05", "-0.3", "-1", "-3")]
    worst = mp.mpf(0)
    for x in pts:
        for k in fns:
            v = abs(fns[k](x))
            s_ = max(abs(fsc[k](x)), mp.mpf(1))
            worst = max(worst, v / s_)
    res_all[cv] = worst
    print(f"  c = {cv}: worst relative residual {mp.nstr(worst, 3)} over {len(pts)} points; kappa {mp.nstr(kap, 10)}, K {mp.nstr(-2 * mp.mpf(float(cv)) / mp.pi, 10)}",
          flush=True)
targets = cases if MUT != "k-kappa" else (sp.Rational(-3, 2),)
check("K1b", all(res_all[cv] < mp.mpf("1e-25") for cv in targets), ", ".join(f"c = {cv}: {mp.nstr(res_all[cv], 3)}" for cv in cases) + "; bar 1e-25")
check("K2", res_all[-1] < mp.mpf("1e-25"), f"c = -1 (K = kappa): {mp.nstr(res_all[-1], 3)}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)
