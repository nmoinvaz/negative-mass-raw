#!/usr/bin/env python3
"""ind269: the exact family of #269 against a brute-force Ricci tensor (criteria in README.md beside this file).

ds^2 = -F dv^2 + 2 dv drho + r^2 dOmega^2, r = lam(v) R(rho), F = A - 2 rho lam'/lam + 1/lam^2 - 1, lam^2 = L + beta e^{K v},
phi = sqrt2 arctan rho. Residuals of R_ab = eps phi_a phi_b + V g_ab and eps box phi = V'(phi), with abstract F, r, phi in the algebra
and the explicit jets from mpmath at 40 digits.

    python3 ind269.py [--mutate=no-h|k-off|phi-scale]
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
v, rho, th, ph_ = sp.symbols("v rho theta varphi", real=True)
X = [v, rho, th, ph_]
Ff, rf, pf = sp.Function("F")(v, rho), sp.Function("r")(v, rho), sp.Function("p")(rho)
g = sp.zeros(4, 4)
g[0, 0] = -Ff
g[0, 1] = g[1, 0] = 1
g[2, 2] = rf ** 2
g[3, 3] = rf ** 2 * sp.sin(th) ** 2
gi = g.inv()
dim = 4
Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d])) for d in range(dim)) / 2)
         for c in range(dim)] for b in range(dim)] for a in range(dim)]


def ric(b, d):
    s = sum(sp.diff(Gam[a][b][d], X[a]) - sp.diff(Gam[a][b][a], X[d]) for a in range(dim))
    s += sum(Gam[a][a][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][a] for a in range(dim) for k in range(dim))
    return sp.simplify(s)


eps = -1
Vs, V1s = sp.symbols("Vs V1s")           # V(phi) and V'(phi) at the point
dphi = [sp.diff(pf, x) for x in X]
E = {}
for nm, (i, j) in {"vv": (0, 0), "vr": (0, 1), "rr": (1, 1), "thth": (2, 2)}.items():
    E[nm] = ric(i, j) - eps * dphi[i] * dphi[j] - Vs * g[i, j]
sq = sp.sqrt(-g.det().subs(sp.sin(th) ** 2, sp.sin(th) ** 2))
box = sum(sp.diff(sq * gi[a, b] * dphi[b], X[a]) for a in range(dim) for b in range(dim)) / sq
E["scal"] = sp.simplify(eps * box - V1s)
E = {k: sp.simplify(e.subs(th, sp.pi / 3)) for k, e in E.items()}
print(f"  Ricci built ({time.time() - t0:.0f} s)", flush=True)


def jet_symbols(expr):
    reps, keys = {}, []
    for d in sorted(expr.atoms(sp.Derivative), key=lambda z: -z.derivative_count):
        counts = {x: 0 for x in (v, rho)}
        for var, n in d.variable_count:
            counts[var] += n
        sym = sp.Symbol(f"{d.expr.func.__name__}_{counts[v]}_{counts[rho]}")
        reps[d] = sym
        keys.append((d.expr.func.__name__, counts[v], counts[rho], sym))
    for f in (Ff, rf, pf):
        if f in expr.atoms(sp.Function):
            sym = sp.Symbol(f"{f.func.__name__}_0_0")
            reps[f] = sym
            keys.append((f.func.__name__, 0, 0, sym))
    return expr.xreplace(reps), keys


COMP = {k: jet_symbols(e) for k, e in E.items()}
FUN = {k: (sp.lambdify([s for *_, s in keys] + [Vs, V1s], e, "mpmath"), keys) for k, (e, keys) in COMP.items()}


def member(c, L, beta):
    c = mp.mpf(c)
    K = -2 * c / mp.pi
    Kl = K * mp.mpf("1.01") if MUT == "k-off" else K
    A = lambda y: 1 + c * (y * y + 1) + K * (y + (y * y + 1) * mp.atan(y))  # noqa: E731
    R = lambda y: mp.sqrt(1 + y * y)  # noqa: E731
    lam = lambda s: mp.sqrt(L + beta * mp.e ** (Kl * s))  # noqa: E731
    dlam = lambda s: mp.diff(lam, s)  # noqa: E731
    hterm = (lambda s: 0) if MUT == "no-h" else (lambda s: 1 / lam(s) ** 2 - 1)
    F = lambda s, y: A(y) - 2 * y * dlam(s) / lam(s) + hterm(s)  # noqa: E731
    r = lambda s, y: lam(s) * R(y)  # noqa: E731
    sc = mp.mpf("1.01") if MUT == "phi-scale" else 1
    phi = lambda y: sc * mp.sqrt(2) * mp.atan(y)  # noqa: E731
    psi = lambda p: p / mp.sqrt(2)  # noqa: E731
    Vp = lambda p: -c * (3 - 2 * mp.cos(psi(p)) ** 2) - K * (3 * mp.sin(psi(p)) * mp.cos(psi(p)) + psi(p) * (3 - 2 * mp.cos(psi(p)) ** 2))  # noqa: E731
    return dict(F=F, r=r, p=phi, V=Vp, K=K, lam=lam)


def residuals(mem, s, y):
    out = {}
    for k, (f, keys) in FUN.items():
        vals = []
        for nm, i, j, _ in keys:
            fn = mem[nm]
            if nm == "p":
                vals.append(mp.diff(fn, y, j) if (i == 0) else mp.mpf(0))
            else:
                vals.append(mp.diff(fn, (s, y), (i, j)))
        p = mem["p"](y)
        V0, V1 = mem["V"](p), mp.diff(mem["V"], p)
        val = f(*vals, V0, V1)
        scale = max([abs(x) for x in vals] + [abs(V0), abs(V1), mp.mpf(1)])
        out[k] = abs(val) / scale
    return out


worst = mp.mpf(0)
rows = []
for c in (-1, "-0.3", "-1.5", -10):
    for L, beta in ((1, mp.mpf("0.3")), (1, mp.mpf("-0.4")), (2, mp.mpf("0.7"))):
        mem = member(c, L, beta)
        for s, y in ((mp.mpf("-1"), mp.mpf("0.4")), (mp.mpf("0.2"), mp.mpf("-0.7")), (mp.mpf("-0.5"), mp.mpf("2.5")), (mp.mpf("0.1"), mp.mpf("-3"))):
            if L + beta * mp.e ** (mem["K"] * s) <= 0:
                continue
            res = residuals(mem, s, y)
            w = max(res.values())
            worst = max(worst, w)
            rows.append((c, L, beta, s, y, w, max(res, key=res.get)))
print(f"  {len(rows)} points; worst relative residual {mp.nstr(worst, 3)} ({time.time() - t0:.0f} s)", flush=True)
for r in rows:
    if r[5] > mp.mpf("1e-30"):
        print(f"    c = {r[0]}, L = {r[1]}, beta = {mp.nstr(r[2], 3)}, v = {mp.nstr(r[3], 3)}, rho = {mp.nstr(r[4], 3)}: {mp.nstr(r[5], 3)} ({r[6]})")
check("K1", worst < mp.mpf("1e-30"), f"worst relative residual of vv, vrho, rhorho, thth, scalar over {len(rows)} points: {mp.nstr(worst, 3)}; bar 1e-30")

# K2: d r / d beta at beta = 0 equals R e^{K v} / 2
worst2 = mp.mpf(0)
for c in (-1, "-0.3", "-1.5", -10):
    for s, y in ((mp.mpf("-1"), mp.mpf("0.4")), (mp.mpf("0.2"), mp.mpf("-0.7"))):
        rb = lambda b, c=c: member(c, 1, b)["r"](s, y)  # noqa: E731
        d = mp.diff(rb, 0)
        K = -2 * mp.mpf(c) / mp.pi
        want = mp.sqrt(1 + y * y) * mp.e ** (K * s) / 2
        worst2 = max(worst2, abs(d / want - 1))
check("K2", worst2 < mp.mpf("1e-30"), f"d r/d beta at beta = 0 against R e^(Kv)/2: worst relative {mp.nstr(worst2, 3)}")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)
