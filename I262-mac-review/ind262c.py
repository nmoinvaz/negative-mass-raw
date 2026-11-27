#!/usr/bin/env python3
"""ind262c (amendment A1, A2: ind262b with abstract background functions): is Y = R e^{K(t + x)}, K = -2c/pi, an exact linear radial solution of the black universes?

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
mp.mp.dps = int(next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--dps=")), 40))
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
# explicit forms, used only to evaluate the abstract functions' derivatives numerically at a point
A_ex = 1 + c * (rho ** 2 + 1) + K * (rho + (rho ** 2 + 1) * sp.atan(rho))
R_ex = sp.sqrt(1 + rho ** 2)
P_ex = s2 * sp.atan(rho)
ph = sp.Symbol("ph")
psi = ph / s2
Vf = -c * (3 - 2 * sp.cos(psi) ** 2) - K * (3 * sp.sin(psi) * sp.cos(psi) + psi * (3 - 2 * sp.cos(psi) ** 2))
Vp = sp.diff(Vf, ph)
V0_ex, V1_ex = Vf.subs(ph, P_ex), Vp.subs(ph, P_ex)
# abstract background functions of rho: the algebra below stays small
A, R, P, V0b, V1b = (sp.Function(nm)(rho) for nm in ("A", "R", "P", "V0b", "V1b"))
EXPL = {"A": A_ex, "R": R_ex, "P": P_ex, "V0b": V0_ex, "V1b": V1_ex}

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
Vphi = V0b
Eq = {}
for nm, (i, j) in {"tt": (0, 0), "tr": (0, 1), "rr": (1, 1), "thth": (2, 2)}.items():
    Eq[nm] = lin(ric(i, j) - eps * dphi[i] * dphi[j] - Vphi * g[i, j])
sq = sp.sqrt(-g.det())
box = sum(sp.diff(sq * gi[a_, b_] * dphi[b_], X[a_]) for a_ in range(dim) for b_ in range(dim)) / sq
Eq["scal"] = lin(eps * box - V1b)
print(f"  linearized equations built ({time.time() - t0:.0f} s)", flush=True)

# substitute Q' = Kq Q / A (Kq = K, or kappa under k-kappa), keep W symbolic; name a, b and their derivatives
Kq = sp.Symbol("kap") if MUT == "k-kappa" else K
q1 = Kq * Qf / A
q2 = sp.diff(q1, rho).subs(sp.Derivative(Qf, rho), q1)
a0, a1, a2, b0, b1, b2 = sp.symbols("a0 a1 a2 b0 b1 b2")


def reduce(expr):
    ex = expr.doit()
    ex = ex.subs(sp.Derivative(Qf, (rho, 2)), q2).subs(sp.Derivative(Qf, rho), q1)
    ex = ex.subs({sp.Derivative(af, (rho, 2)): a2, sp.Derivative(af, rho): a1, af: a0,
                  sp.Derivative(bf, (rho, 2)): b2, sp.Derivative(bf, rho): b1, bf: b0})
    return sp.expand(ex / (Qf * T))


Rd = {k: reduce(v) for k, v in Eq.items()}
for k, v in Rd.items():
    assert not v.has(Qf), k
print(f"  reduced ({time.time() - t0:.0f} s)", flush=True)


def lin_coeffs(expr, var):
    """expr = alpha var + beta (checked linear)."""
    al = sp.diff(expr, var)
    assert not al.has(var)
    return al, expr.subs(var, 0)


# E_tr = al_b b0 + be_b  ->  b0 = -be_b/al_b; the b-derivatives by differentiating that expression in rho
al_b, be_b = lin_coeffs(Rd["tr"], b0)
bexpr = -be_b / al_b
sub_b = {b0: bexpr, b1: sp.diff(bexpr, rho), b2: sp.diff(bexpr, rho, 2)}
# scalar equation = al_1 a1 + (rest in a0): a1 = f(rho, a0)
sc = Rd["scal"].subs(sub_b)
al_1, be_1 = lin_coeffs(sc, a1)
a1f = -be_1 / al_1                                # contains a0 linearly
a2f = sp.diff(a1f.subs(a0, af), rho).subs(sp.Derivative(af, rho), a1f.subs(a0, af)).subs(af, a0)
eqs = {}
for k in ("rr", "tt", "thth"):
    e_ = Rd[k].subs(sub_b).subs(a2, a2f).subs(a1, a1f)
    eqs[k] = lin_coeffs(sp.expand(e_), a0)       # (alpha_k, beta_k)
print(f"  linear forms ready ({time.time() - t0:.0f} s)", flush=True)


def jet_symbols(expr):
    reps, keys = {}, []
    for d in sorted(expr.atoms(sp.Derivative), key=lambda z: -z.derivative_count):
        f = d.expr
        if f.func.__name__ in EXPL:
            sym = sp.Symbol(f"{f.func.__name__}_{d.derivative_count}")
            reps[d] = sym
            keys.append((f.func.__name__, d.derivative_count, sym))
    for f in expr.atoms(sp.Function):
        if f.func.__name__ in EXPL and f not in reps:
            sym = sp.Symbol(f"{f.func.__name__}_0")
            reps[f] = sym
            keys.append((f.func.__name__, 0, sym))
    return expr.xreplace(reps), keys


_CACHE = {}


def compiled(expr, cv, kap):
    key = (id(expr), cv)
    if key not in _CACHE:
        e, keys = jet_symbols(expr.subs(c, cv))
        _CACHE[key] = (sp.lambdify([sym for _, _, sym in keys] + [rho, W, sp.Symbol("kap")], e, "mpmath"), keys)
    return _CACHE[key]


def num(expr, cv, x, Wv, kap):
    f, keys = compiled(expr, cv, kap)
    vals = []
    for nm, k, sym in keys:
        fx = sp.lambdify(rho, EXPL[nm].subs(c, cv), "mpmath")
        vals.append(mp.diff(fx, x, k) if k else fx(x))
    return f(*vals, x, Wv, kap)


def kappa_of(cval):
    cq = sp.Rational(cval)
    cm = mp.mpf(cq.p) / mp.mpf(cq.q)
    Kc = -2 * cm / mp.pi
    Af = lambda y: 1 + cm * (y * y + 1) + Kc * (y + (y * y + 1) * mp.atan(y))  # noqa: E731
    rh = mp.findroot(Af, mp.mpf(0) if cq == -1 else mp.mpf("0.5"))
    return rh, mp.diff(Af, rh) / 2


res_all = {}
cases = (-1, sp.Rational(-3, 10), sp.Rational(-3, 2), -10)
for cv in cases:
    rh, kap = kappa_of(cv)
    cq = sp.Rational(cv)
    Kn = kap if MUT == "k-kappa" else -2 * (mp.mpf(cq.p) / mp.mpf(cq.q)) / mp.pi       # exact c, not float(c) (A4)
    Wv = Kn * (1 + mp.mpf("1e-3")) if MUT == "w-off" else Kn
    pts = [rh + mp.mpf(d) for d in ("0.05", "0.2", "0.5", "1", "2", "4", "8", "15")]
    if cv == -1:
        pts += [mp.mpf(d) for d in ("-0.05", "-0.3", "-1", "-3")]
    worst, rows = mp.mpf(0), []
    for x in pts:
        ab = {k: (num(al, cv, x, Wv, kap), num(be, cv, x, Wv, kap)) for k, (al, be) in eqs.items()}
        al_rr, be_rr = ab["rr"]
        sc_ = max(abs(v) for pair in ab.values() for v in pair)
        if abs(al_rr) > mp.mpf("1e-20") * max(sc_, 1):
            a_here = -be_rr / al_rr
            r_tt = ab["tt"][0] * a_here + ab["tt"][1]
            r_th = ab["thth"][0] * a_here + ab["thth"][1]
            # consistency: d a/d rho of a = -be_rr/al_rr against a1f(a)
            afun = lambda y: -num(eqs["rr"][1], cv, y, Wv, kap) / num(eqs["rr"][0], cv, y, Wv, kap)  # noqa: E731
            r_cons = mp.diff(afun, x) - num(a1f, cv, x, Wv, kap).subs(a0, a_here) if hasattr(num(a1f, cv, x, Wv, kap), "subs") else None
            al_1n = sp.lambdify(a0, a1f.subs(c, cv), "mpmath")
            resid = [abs(r_tt), abs(r_th)]
            mode = "a fixed by E_rr"
        else:
            resid = [abs(ab[k][1]) for k in ("rr", "tt", "thth")] + [abs(ab[k][0]) for k in ("tt", "thth")]
            mode = "E_rr, E_tt, E_thth independent of a"
        rel = max(resid) / max(sc_, mp.mpf(1))
        worst = max(worst, rel)
        rows.append((x, mode, rel))
        if "--per-point" in sys.argv:
            print(f"    c = {cv}, rho = {mp.nstr(x, 6)}: {mp.nstr(rel, 3)}", flush=True)
    res_all[cv] = worst
    modes = sorted(set(r[1] for r in rows))
    print(f"  c = {cv}: worst relative residual {mp.nstr(worst, 3)} over {len(pts)} points ({'; '.join(modes)}); "
          f"kappa {mp.nstr(kap, 10)}, K {mp.nstr(-2 * mp.mpf(float(cv)) / mp.pi, 10)}", flush=True)
targets = cases if MUT != "k-kappa" else (sp.Rational(-3, 2),)
check("K1b", all(res_all[cv] < mp.mpf("1e-25") for cv in targets), ", ".join(f"c = {cv}: {mp.nstr(res_all[cv], 3)}" for cv in cases) + "; bar 1e-25")
check("K2", res_all[-1] < mp.mpf("1e-25"), f"c = -1 (K = kappa): {mp.nstr(res_all[-1], 3)}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)
