#!/usr/bin/env python3
"""ind39: the double-null equations of #39 derived again by a brute-force Ricci tensor, against dn.py; and the tuned growth
rate at D = 6 with #39's code (criteria in README.md beside this file).

    python3 ind39.py [--mutate=theta-coef|wrong-W] [--wt=WORKTREE_NOTES_DIR] [--only=K1|K2]
"""
import argparse
import math
import random
import sys
import time

import numpy as np
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["theta-coef", "wrong-W"])
ap.add_argument("--wt", default="/Users/nathan/Source/negative-mass-r39/notes/wormhole_evolution")
ap.add_argument("--only", default="K1,K2")
ap.add_argument("--k2b", action="store_true", help="A1: the finer pair, reported as K2b")
OPT = ap.parse_args()
MUT = OPT.mutate
sys.path.insert(0, OPT.wt)
import dn  # noqa: E402  (the code under test)
import checks  # noqa: E402

RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def ricci(g, X):
    """R_bd of the metric matrix g in coordinates X: Christoffels from g, then the contraction (coordinator's own code)"""
    dim = len(X)
    gi = sp.simplify(g.inv())
    Gam = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], X[c]) + sp.diff(g[d, c], X[b]) - sp.diff(g[b, c], X[d]))
                             for d in range(dim)) / 2) for c in range(dim)] for b in range(dim)] for a in range(dim)]
    R = sp.zeros(dim, dim)
    for b in range(dim):
        for d in range(b, dim):
            e = sum(sp.diff(Gam[a][b][d], X[a]) - sp.diff(Gam[a][b][a], X[d]) for a in range(dim))
            e += sum(Gam[a][a][k] * Gam[k][b][d] - Gam[a][d][k] * Gam[k][b][a] for a in range(dim) for k in range(dim))
            R[b, d] = R[d, b] = sp.simplify(e)
    return R, gi


if "K1" in OPT.only:
    t0 = time.time()
    u, v = sp.symbols("u v")
    ok1, notes = True, []
    for n in (2, 3):
        th = sp.symbols(f"th1:{n + 1}")
        X = [u, v, *th]
        r, f = sp.Function("r")(u, v), sp.Function("f")(u, v)
        ph = [sp.Function("phg")(u, v), sp.Function("phn")(u, v)]     # a ghost and a normal field
        eps = [-1, 1]
        g = sp.zeros(n + 2, n + 2)
        g[0, 1] = g[1, 0] = -sp.exp(-f)                                 # -2 e^{-f} du dv
        w = r**2
        for i in range(n):
            g[2 + i, 2 + i] = w
            w = w * sp.sin(th[i])**2
        R, gi = ricci(g, X)
        src = lambda a, b: sum(e * sp.diff(p, X[a]) * sp.diff(p, X[b]) for e, p in zip(eps, ph))  # noqa: E731
        sq = sp.sqrt(-g.det())
        box = [sp.simplify(sum(sp.diff(sq * gi[a, b] * sp.diff(p, X[b]), X[a]) for a in range(n + 2) for b in range(n + 2)) / sq)
               for p in ph]
        ruv, fuv = sp.Derivative(r, u, v), sp.Derivative(f, u, v)
        puv = [sp.Derivative(p, u, v) for p in ph]
        sol_r = sp.solve(sp.Eq(R[2, 2].doit(), 0), ruv.doit())
        sol_r = sol_r[0] if sol_r else None
        Euv = (R[0, 1] - src(0, 1)).doit().subs(sp.diff(r, u, v), sol_r)
        sol_f = sp.solve(sp.Eq(Euv, 0), sp.diff(f, u, v))[0]
        sol_p = [sp.solve(sp.Eq(b_, 0), sp.diff(p, u, v))[0] for b_, p in zip(box, ph)]
        ru, rv, fu, fv = sp.diff(r, u), sp.diff(r, v), sp.diff(f, u), sp.diff(f, v)
        theirs_r = -(n - 1) * (ru * rv + sp.exp(-f) / 2) / r
        theirs_f = (sp.Integer(n) / r) * theirs_r + sum(e * sp.diff(p, u) * sp.diff(p, v) for e, p in zip(eps, ph))
        theirs_p = [-n * (ru * sp.diff(p, v) + rv * sp.diff(p, u)) / (2 * r) for p in ph]
        res = [sp.simplify(sol_r - theirs_r), sp.simplify(sol_f - theirs_f)] + [sp.simplify(a - b) for a, b in zip(sol_p, theirs_p)]
        sym_ok = all(x == 0 for x in res)
        # constraints, reported: R_uu - sum eps phi_u^2 = 0 solved for r_uu
        cu = sp.solve(sp.Eq((R[0, 0] - src(0, 0)).doit(), 0), sp.diff(r, u, 2))
        # numerical: dn.F_np at random states
        syms = sp.symbols("R F Pg Pn Ru Rv Fu Fv Pgu Pgv Pnu Pnv")
        Rs, Fs, Pgs, Pns, Rus, Rvs, Fus, Fvs, Pgus, Pgvs, Pnus, Pnvs = syms
        sub = {sp.diff(r, u): Rus, sp.diff(r, v): Rvs, sp.diff(f, u): Fus, sp.diff(f, v): Fvs,
               sp.diff(ph[0], u): Pgus, sp.diff(ph[0], v): Pgvs, sp.diff(ph[1], u): Pnus, sp.diff(ph[1], v): Pnvs}
        sub2 = {r: Rs, f: Fs, ph[0]: Pgs, ph[1]: Pns}
        exprs = [e.subs(sub).subs(sub2) for e in (sol_r, sol_f, *sol_p)]
        fn = sp.lambdify(syms, exprs, "math")
        dn.MUT = "theta_coef" if MUT == "theta-coef" else None
        par = dn.kernel_params(n, np.array([-1.0, 1.0]))
        rng = random.Random(1000 + n)
        worst = 0.0
        for _ in range(20):
            st = [rng.uniform(0.5, 3.0), rng.uniform(-1, 1), rng.uniform(-1, 1), rng.uniform(-1, 1)] + \
                 [rng.uniform(-1, 1) for _ in range(8)]
            mine = fn(*st)
            c = np.array([[st[0]], [st[1]], [st[2]], [st[3]]])
            up = np.array([[st[4]], [st[6]], [st[8]], [st[10]]])
            um = np.array([[st[5]], [st[7]], [st[9]], [st[11]]])
            got = dn.F_np(c, up, um, par, np.array([-1.0, 1.0]))[:, 0]
            for a, b in zip(mine, got):
                worst = max(worst, abs(a - b) / max(1.0, abs(a)))
        dn.MUT = None
        num_ok = worst <= 1e-12
        ok1 &= sym_ok and num_ok
        notes.append(f"n={n}: symbolic residuals {[str(x) for x in res]}, dn.F_np worst rel diff {worst:.1e}; "
                     f"constraint r_uu = {sp.simplify(cu[0].subs(sub).subs(sub2)) if cu else 'none'}")
    check("K1", ok1, "; ".join(notes) + f" ({time.time() - t0:.0f} s)")

if "K2" in OPT.only:
    t0 = time.time()
    n, W = 4, math.sqrt(4.68662054311946479)
    Wref = W * (1.02 if MUT == "wrong-W" else 1.0)
    out = []
    for h in ((0.005 / math.sqrt(3), 0.0025 / math.sqrt(3)) if OPT.k2b else (0.01 / math.sqrt(3), 0.005 / math.sqrt(3))):
        lo, hi, k = checks.bisect_A(n, h, 12.0, -0.01, 0.01, 1e-10)
        sl = [checks.fit_growth(checks.fate_run(n, h, A, 12.0), W, (1e-3, 1e-2)) for A in (lo, hi)]
        Wfit = 0.5 * (sl[0][0] + sl[1][0])
        out.append((h, Wfit, 0.5 * (lo + hi), k, [s[1] for s in sl]))
        print(f"  D=6 h={h:.6f}: A*_h {0.5 * (lo + hi):.6e} ({k} runs), slopes {sl[0][0]:.6f} {sl[1][0]:.6f} ({sl[0][1]}, {sl[1][1]} pts), "
              f"W_fit {Wfit:.6f} vs W {W:.6f} ({time.time() - t0:.0f} s)", flush=True)
    ok_bar = all(abs(o[1] / Wref - 1) <= 0.01 for o in out)
    ok_ag = abs(out[0][1] / out[1][1] - 1) <= 0.005
    check("K2b" if OPT.k2b else "K2", ok_bar and ok_ag, f"W_fit {out[0][1]:.6f}, {out[1][1]:.6f} against {Wref:.6f}: rel {out[0][1] / Wref - 1:+.2e}, "
          f"{out[1][1] / Wref - 1:+.2e}; agreement {out[0][1] / out[1][1] - 1:+.2e}; A*_h ratio {out[0][2] / out[1][2]:.3f}")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
