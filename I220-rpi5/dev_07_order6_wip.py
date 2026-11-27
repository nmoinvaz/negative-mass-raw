"""Order 6 of the matched expansion (matched.py, order3.py ... order5.py): Omega4 from G6 = 0 by method B, and the checks of issue #220.

W^2 a^2 = s + Omega, s = 2(D - 3), eps = 1/s, Omega = Omega0 + Omega1 eps + Omega2 eps^2 + ..., R = r^s, l = ln R.
The order equations (E0 derives them from the master equation), the same for every k:
  dY_k/dl = F_{k-1},  F_{k-1} = sum_{j<k} L_{k-1-j} l^j / j!,   (R - 1) L_k' - L_k/2 = h_k,
  h_k = (1 - 1/R) L_{k-1} + sum_{j<k} Y_j c_{k-j} + Y_k/2,   L_k = -2 Omega_{k-1} + u C_k,   G_k = C_k(inf) = 0,
with u = sqrt(R - 1), C_k = int_1^R (h_k - Omega_{k-1}) (R' - 1)^{-3/2} dR'. G_k is affine in Omega_{k-2} with slope -4 pi:
G2 = 0 gives Omega0, G3 = 0 Omega1, G4 = 0 Omega2, G5 = 0 Omega3, **G6 = 0 gives Omega4**. One path computes them all (`omega_chain`).

Method B (order4.py's PanelB, shared): v = sqrt(l), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the
spectral integration matrix; Y_k from the left, the tail C_right from the right, L_k = -2 h_k(1) - u C_right, G_k = C_right(0). It uses no
closed form of Y_k or L_k and no input value of Omega_0 .. Omega_3.

    python3 order6.py grid --grid=N,w,V,dps [--kmax=6]      (a development run of one grid; no gate)
"""
import json
import math
import os
import random
import re
import sys
import time

import mpmath as mp
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv, sys.argv = sys.argv, sys.argv[:1]          # order4.py parses sys.argv when it is imported
from order4 import PanelB  # noqa: E402
import order4 as o4  # noqa: E402
sys.argv = _argv

MUTATIONS = ("wrong_h", "wrong_c6", "wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3", "coarse_B", "short_tail", "pslq_wrong_basis",
             "wrong_Om4_series", "wrong_closed3", "pslq_wrong_target")
MUTATE = None
W2FILE = "w2_output.txt"
SAVE = None
LOAD = None
GRIDARG = None
GRIDSEL = None
CGRIDS_ON = False
W2RAW = None
KMAX = 6
PARTS = []
REAL = True


def parse(argv):
    global MUTATE, W2FILE, W2RAW, SAVE, LOAD, GRIDARG, GRIDSEL, CGRIDS_ON, KMAX, PARTS, REAL
    parts = []
    for a in argv:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
            assert MUTATE in MUTATIONS, f"unknown mutation {MUTATE}; known: {MUTATIONS}"
        elif a.startswith("--w2="):
            W2FILE = a.split("=", 1)[1]
        elif a.startswith("--w2raw="):
            W2RAW = a.split("=", 1)[1]
        elif a.startswith("--save="):
            SAVE = a.split("=", 1)[1]
        elif a.startswith("--load="):
            LOAD = a.split("=", 1)[1]
        elif a.startswith("--grid="):
            GRIDARG = a.split("=", 1)[1]
        elif a.startswith("--grids="):
            GRIDSEL = a.split("=", 1)[1].split(",")
        elif a == "--cgrids":
            CGRIDS_ON = True
        elif a == "--no-real":
            REAL = False
        elif a.startswith("--kmax="):
            KMAX = int(a.split("=", 1)[1])
        else:
            parts.append(a)
    PARTS = parts or ["sym", "evals", "pslq", "remainder"]


RESULTS = []


def report(cid, ok, text):
    RESULTS.append((cid, ok))
    print(f"{'PASS' if ok else 'FAIL'}    {cid}: {text}", flush=True)


def digits(a, b):
    """-log10 of the relative difference, capped at the working precision in digits"""
    a, b = mp.mpf(a), mp.mpf(b)
    d = abs(a - b)
    return mp.mpf(mp.mp.dps) if d == 0 else min(mp.mpf(mp.mp.dps), -mp.log10(d / abs(a)))


def nd(x, n=40):
    return mp.nstr(x, n)


# ---------------------------------------------------------------------------------------------------------------
# the table of c_m and h_m (integer and rational arithmetic only, so that it also runs on sympy symbols)
# ---------------------------------------------------------------------------------------------------------------
def cc(m, Om, l, R):
    if m == 1:
        return Om[0] + 3 * l / 2 - 1 + 1 / R
    if m == 2:
        return Om[0] * l + Om[1] + l**2 / 4 + l + (l / R if MUTATE == "wrong_h" else -l / R)
    if m == 3:
        return Om[0] * l**2 / 2 + Om[1] * l + Om[2] + l**3 / 4 - l**2 / 2 + l**2 / (2 * R)
    if m == 4:
        return Om[0] * l**3 / 6 + Om[1] * l**2 / 2 + Om[2] * l + Om[3] + l**4 / 48 + l**3 / 6 - l**3 / (6 * R)
    if m == 5:
        return (Om[0] * l**4 / 24 + Om[1] * l**3 / 6 + Om[2] * l**2 / 2 + Om[3] * l + Om[4] + l**5 / 80 - l**4 / 24
                + l**4 / (24 * R))
    if m == 6:
        return (Om[0] * l**5 / 120 + Om[1] * l**4 / 24 + Om[2] * l**3 / 6 + Om[3] * l**2 / 2 + Om[4] * l + Om[5]
                + l**6 / 1440 + l**5 / 120 + (1 if MUTATE == "wrong_c6" else -1) * l**5 / (120 * R))
    raise ValueError(m)


def hk(m, Om, l, R, Y, L):
    """h_m"""
    if m == 0:
        return Y[0] / 2
    return (1 - 1 / R) * L[m - 1] + sum(Y[j] * cc(m - j, Om, l, R) for j in range(m)) + Y[m] / 2


def Fsum(k, L, l):
    return sum(L[k - 1 - j] * l**j / math.factorial(j) for j in range(k))


# ---------------------------------------------------------------------------------------------------------------
# E0: the epsilon-expansion of the master equation against the table, k = 0 .. 6
# ---------------------------------------------------------------------------------------------------------------
def check_sym():
    t0 = time.time()
    R, eps, l = sp.symbols("R epsilon l", positive=True)
    Om = sp.symbols("Omega0:6")
    Ys, Ls = sp.symbols("Y0:7"), sp.symbols("L0:7")
    kk = 6
    r = sum((eps * l) ** j / sp.factorial(j) for j in range(kk + 1))          # exact through eps^6, which is all that is read
    rinv = sum((-eps * l) ** j / sp.factorial(j) for j in range(kk + 1))
    Y = sum(Ys[k] * eps**k for k in range(kk + 1))
    L = sum(Ls[k] * eps**k for k in range(kk + 1))
    O = sum(Om[k] * eps**k for k in range(kk))
    half = sp.Rational(1, 2)
    rhs = ((1 + eps * O) * r * Y + L / (2 * R) + (half + eps) * L * (R - 1) / R - (half + eps) * Y * (R - 1) / R * rinv
           - Y / (2 * R) * rinv)
    ser = sp.expand(rhs)
    yser = sp.expand(eps * L * r)
    res = []
    for k in range(kk + 1):
        res.append(sp.simplify(ser.coeff(eps, k) - Ls[k] / 2 - hk(k, Om, l, R, Ys, Ls)))
        if k >= 1:
            res.append(sp.simplify(yser.coeff(eps, k) - Fsum(k, Ls, l)))
    report("E0", all(x == 0 for x in res),
           f"h_k (k = 0 .. 6) and dY_k/dl (k = 1 .. 6) from the epsilon-expansion of the master equation against the table: "
           f"residuals {[str(x) for x in res if x != 0] or '0'} ({time.time() - t0:.1f} s)")


# ---------------------------------------------------------------------------------------------------------------
# method B at order k
# ---------------------------------------------------------------------------------------------------------------
class PanelK(PanelB):
    def cum_left(self, F):
        N, half = self.N, self.half
        out, acc = [], mp.mpf(0)
        for p in range(self.P):
            out.append([acc + half * mp.fdot(self.S[i], F[p]) for i in range(N)])
            acc += half * mp.fdot(self.wend, F[p])
        return out

    def cum_right(self, F):
        N, half = self.N, self.half
        tot = [half * mp.fdot(self.wend, F[p]) for p in range(self.P)]
        out, acc = [None] * self.P, mp.mpf(0)
        for p in range(self.P - 1, -1, -1):
            out[p] = [acc + tot[p] - half * mp.fdot(self.S[i], F[p]) for i in range(N)]
            acc += tot[p]
        return out, acc

    def hierarchy(self, Om, kmax):
        """Y_0 .. Y_kmax, L_0 .. L_kmax and G_0 .. G_kmax for the given Omega list (Om[kmax - 1] is not used: h_kmax(1) = Om[kmax - 1])"""
        N, P = self.N, self.P
        grid = lambda fn: [[fn(p, i) for i in range(N)] for p in range(P)]  # noqa: E731
        lp = [grid(lambda p, i, j=j: self.l[p][i] ** j / mp.factorial(j)) for j in range(kmax + 1)]       # l^j / j!
        cg = {m: grid(lambda p, i, m=m: cc(m, Om, self.l[p][i], self.R[p][i])) for m in range(1, kmax + 1)}
        Sg = grid(lambda p, i: self.Rm1[p][i] / self.R[p][i])                                              # 1 - 1/R
        Y = [grid(lambda p, i: mp.mpf(1))]
        L = []
        G = {}
        for k in range(kmax + 1):
            if k >= 1:
                F = grid(lambda p, i: 2 * self.v[p][i] * mp.fdot([L[k - 1 - j][p][i] for j in range(k)], [lp[j][p][i] for j in range(k)]))
                Y.append(self.cum_left(F))
            thr = mp.mpf(1) / 2 if k == 0 else Om[k - 1]
            if k == 0:
                s = grid(lambda p, i: Y[0][p][i] / 2 - thr)
            else:
                s = grid(lambda p, i: Sg[p][i] * L[k - 1][p][i] + mp.fdot([Y[j][p][i] for j in range(k)], [cg[k - j][p][i] for j in range(k)])
                         + Y[k][p][i] / 2 - thr)
            Cint = grid(lambda p, i: s[p][i] / self.Rm1[p][i] * self.R[p][i] / self.u[p][i] * 2 * self.v[p][i])
            Cr, G[k] = self.cum_right(Cint)
            L.append(grid(lambda p, i: -2 * thr - self.u[p][i] * Cr[p][i]))
        return Y, L, G


def solve_omega(Gfun, k, Om):
    """Omega_{k-2} from the affine G_k; returns (value, slope)"""
    o0 = list(Om)
    o0[k - 2] = mp.mpf(0)
    o1 = list(Om)
    o1[k - 2] = mp.mpf(1)
    g0, g1 = Gfun(k, o0), Gfun(k, o1)
    return -g0 / (g1 - g0), g1 - g0


def closed_omegas():
    """Omega_0 .. Omega_3 of #26 and #208 (derived there), the planted truth"""
    pi, ln2, z3 = mp.pi, mp.ln2, mp.zeta(3)
    return [-4 * ln2, 2 * pi**2 / 3 + 8 * ln2**2,
            80 * z3 - mp.mpf(8) / 3 * pi**2 * ln2 - mp.mpf(32) / 3 * ln2**3,
            22 * pi**4 / 45 + mp.mpf(16) / 3 * pi**2 * ln2**2 + mp.mpf(32) / 3 * ln2**4 - 320 * z3 * ln2 - 384 * z3]


def omega_chain(B, kmax, log=None):
    """Omega_0 .. Omega_{kmax-2} from G_2 .. G_kmax = 0, in turn, by the same code at every order; returns (Om, slopes, seconds per order)"""
    Om = [mp.mpf(0)] * kmax
    slopes, secs = {}, {}
    cl = closed_omegas()
    for k in range(2, kmax + 1):
        t0 = time.time()
        Om_in = list(Om)
        for i, name in enumerate(("wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3")):
            if MUTATE == name and k >= i + 3:
                Om_in[i] = cl[i] + mp.mpf(1) / 100
        val, slope = solve_omega(lambda kk, o: B.hierarchy(o, kk)[2][kk], k, Om_in)
        Om[k - 2] = val
        slopes[k] = slope
        secs[k] = time.time() - t0
        if log:
            print(f"    k = {k}: Omega_{k - 2} = {nd(val, 30)}  slope {nd(slope, 20)}  ({secs[k]:.0f} s)", flush=True)
    return Om, slopes, secs


def run_B(N, w, V, dps, kmax=6, log=False):
    t0 = time.time()
    if MUTATE == "coarse_B":
        N = 10
    if MUTATE == "short_tail":
        V = 6
    with mp.workdps(dps):
        w = mp.mpf(w[0]) / w[1] if isinstance(w, tuple) else mp.mpf(w)
        B = PanelK(N, w, V)
        Om, slopes, secs = omega_chain(B, kmax, log=log)
        out = {f"Om{i}": +Om[i] for i in range(kmax - 1)}
        out.update({f"slope{k}": +s for k, s in slopes.items()})
        out["secs"] = time.time() - t0
        out["grid"] = f"N={N} w={mp.nstr(w, 6)} V={V} dps={dps} panels={B.P}"
    return out


# declared grids: name -> (N, w, V, working digits). G1, G2 are the grids of record; B1 .. B3 are reported only; C1, C2 are the grids of the
# control runs (--cgrids), sized to meet the same bars (100 digits) with a few digits to spare.
GRIDS = {"G1": (170, (1, 4), 38, 400), "G2": (150, (3, 10), 36, 360)}              # w as a fraction (num, den), evaluated at the working precision
REPORT_GRIDS = {"B1": (40, (1, 2), 18, 120), "B2": (60, (2, 5), 24, 200), "B3": (100, (1, 4), 30, 260)}
CGRIDS = {"G1": (84, (1, 4), 28, 200), "G2": (80, (3, 10), 28, 190)}

OM4_FIT = "-12794.499860023"          # #195's fit (w2_output.txt: 14 digits, range over the 6 admitted cells 1.5e-30)
OM4_FIT_HALF_ULP = mp.mpf("5e-10")


def save_ev(ev, path):
    with open(path, "w") as f:
        json.dump({n: {k: (mp.nstr(v, 430) if isinstance(v, mp.mpf) else v) for k, v in e.items()} for n, e in ev.items()}, f, indent=1)


def load_ev(paths):
    out = {}
    for path in paths.split(","):
        raw = json.load(open(path))
        out.update({n: {k: (mp.mpf(v) if k.startswith(("Om", "slope")) else v) for k, v in e.items()} for n, e in raw.items()})
    return out


def check_grid():
    """one grid, no gate: the development run"""
    N, w, V, dps = GRIDARG.split(",")
    mp.mp.dps = 60
    e = run_B(int(N), tuple(int(t) for t in w.split("/")) if "/" in w else w, int(V), int(dps), kmax=KMAX, log=True)
    mp.mp.dps = int(dps)
    cl = closed_omegas()
    print(f"  {e['grid']}  {e['secs']:.0f} s")
    for i in range(KMAX - 1):
        print(f"    Omega{i} = {nd(e[f'Om{i}'], int(dps))}")
    for i in range(min(4, KMAX - 1)):
        print(f"    Omega{i} against closed form: {float(digits(cl[i], e[f'Om{i}'])):.1f} digits")
    if "Om4" in e:
        print(f"    Omega4 against #195's fit {OM4_FIT}: difference {nd(e['Om4'] - mp.mpf(OM4_FIT), 5)}")
    for k in range(2, KMAX + 1):
        print(f"    slope G{k} against -4 pi: {float(digits(-4 * mp.pi, e[f'slope{k}'])):.1f} digits")
    return e


# ---------------------------------------------------------------------------------------------------------------
# the evaluations and their checks
# ---------------------------------------------------------------------------------------------------------------
def check_evals():
    mp.mp.dps = 60
    ev = {}
    main_grids = CGRIDS if CGRIDS_ON else GRIDS
    todo = list(main_grids.items()) + ([] if CGRIDS_ON else list(REPORT_GRIDS.items()))
    if GRIDSEL:
        todo = [(n, g) for n, g in todo if n in GRIDSEL]
    for name, (N, w, V, dps) in todo:
        ev[name] = run_B(N, w, V, dps)
        e = ev[name]
        print(f"  {name}: {e['grid']}  {e['secs']:.0f} s\n    Omega0 = {nd(e['Om0'], 60)}\n    Omega1 = {nd(e['Om1'], 60)}"
              f"\n    Omega2 = {nd(e['Om2'], 60)}\n    Omega3 = {nd(e['Om3'], 110)}\n    Omega4 = {nd(e['Om4'], dps - 20)}\n    slopes G2 .. G6 = "
              + " ".join(nd(e[f"slope{k}"], 20) for k in range(2, 7)), flush=True)
    if SAVE:
        save_ev(ev, SAVE)
    return ev


def check_values(ev):
    mp.mp.dps = 430
    cl = closed_omegas()
    if MUTATE == "wrong_closed3":
        cl[3] = cl[3] + mp.mpf(1) / 1000
    grids = ["G1", "G2"]
    # PL0 .. PL3: the planted orders by the same code
    for i, cid in enumerate(("PL0", "PL1", "PL2", "PL3")):
        rows = {n: digits(cl[i], ev[n][f"Om{i}"]) for n in ev}
        ok = all(rows[n] >= 100 for n in grids)
        report(cid, ok, f"planted: Omega{i} against its closed form, digits: " + ", ".join(f"{n} {float(d):.1f}" for n, d in rows.items())
               + " (bar 100 on G1, G2; the others reported)")
    # PLW: a wrong input must move the orders above it (the control's own statement, evaluated when a wrong-input mutation is on)
    if MUTATE in ("wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3"):
        i = int(MUTATE[-1]) + 1
        moved = all(abs(ev[n][f"Om{i}"] - (cl[i] if i < 4 else mp.mpf(OM4_FIT))) > mp.mpf(1) / 1000 for n in grids)
        report("PLW", moved, f"control {MUTATE} moves Omega{i} of " + ", ".join(
            f"{n} by {nd(ev[n][f'Om{i}'] - (cl[i] if i < 4 else mp.mpf(OM4_FIT)), 5)}" for n in grids))
    # SL: slopes
    rows, ok = [], True
    for n in ev:
        ds = [digits(-4 * mp.pi, ev[n][f"slope{k}"]) for k in range(2, 7)]
        rows.append(f"{n} " + "/".join(f"{float(d):.1f}" for d in ds))
        ok = ok and (n not in grids or min(ds) >= 100)
    report("SL", ok, "slope of G_k in Omega_(k-2) against -4 pi, k = 2 .. 6, digits: " + ", ".join(rows) + " (bar 100 on G1, G2)")
    # M4: the two grids on Omega4
    a, b = grids
    d4 = digits(ev[a]["Om4"], ev[b]["Om4"])
    report("M4", d4 >= 100, f"Omega4 of {a} against {b} (two grids, two precisions): {float(d4):.1f} digits (bar 100); |diff| = "
           f"{nd(abs(ev[a]['Om4'] - ev[b]['Om4']), 3)}")
    others = [n for n in ev if n not in grids]
    print("  reported: digits between evaluations, Omega3 / Omega4: " + ", ".join(
        f"{x}-{y} " + "/".join(f"{float(digits(ev[x][f'Om{i}'], ev[y][f'Om{i}'])):.1f}" for i in (3, 4))
        for x, y in [("G1", "G2")] + [(o, "G1") for o in others]))
    # X1: Omega4 against #195's fit
    fit = mp.mpf(OM4_FIT)
    dd = {n: abs(ev[n]["Om4"] - fit) for n in ev}
    report("X1", all(dd[n] <= OM4_FIT_HALF_ULP for n in grids),
           "Omega4 against #195's fit " + OM4_FIT + " (14 digits, half a unit of its last digit is 5e-10; the fit's range over its cells is 1.5e-30): "
           + ", ".join(f"{n} {nd(d, 3)}" for n, d in dd.items()) + " (bar 5e-10 on G1, G2)")
    return d4


# ---------------------------------------------------------------------------------------------------------------
# PSLQ
# ---------------------------------------------------------------------------------------------------------------
PSLQ_DIGITS = 200             # cap on the working digits; the digits the two grids share if fewer
PSLQ_SLACK = 12               # tolerance 10^-(d - slack)
# basis name -> (maxcoeff H, planted seed)
PSLQ_BASES = {"P1": (10**9, 220001), "P2": (10**8, 220002), "P3": (10**7, 220003), "P4": (10**9, 220004)}
PSLQ_BASES_C = {"P1": (10**9, 220001), "P2": (10**5, 220002), "P3": (10**4, 220003), "P4": (10**9, 220004)}   # --cgrids: d ~ 113 < the budgets above


def constants(name):
    pi, ln2, z3, z5 = mp.pi, mp.ln2, mp.zeta(3), mp.zeta(5)
    li4, li5 = mp.polylog(4, mp.mpf(1) / 2), mp.polylog(5, mp.mpf(1) / 2)
    w5 = [("pi^4 ln 2", pi**4 * ln2), ("pi^2 ln^3 2", pi**2 * ln2**3), ("ln^5 2", ln2**5), ("pi^2 zeta(3)", pi**2 * z3),
          ("zeta(3) ln^2 2", z3 * ln2**2), ("zeta(5)", z5)]
    w4 = [("pi^4", pi**4), ("pi^2 ln^2 2", pi**2 * ln2**2), ("ln^4 2", ln2**4), ("zeta(3) ln 2", z3 * ln2)]
    low = [("zeta(3)", z3), ("pi^2 ln 2", pi**2 * ln2), ("ln^3 2", ln2**3), ("pi^2", pi**2), ("ln^2 2", ln2**2), ("ln 2", ln2), ("1", mp.mpf(1))]
    if name == "P1":
        return w5
    if name == "P2":
        return w5 + w4 + low
    if name == "P3":
        return w5 + w4 + low + [("Li4(1/2)", li4), ("Li4(1/2) ln 2", li4 * ln2), ("Li5(1/2)", li5)]
    if name == "P4":
        return w5 + [("Li4(1/2) ln 2", li4 * ln2), ("Li5(1/2)", li5)]
    raise ValueError(name)


def planted(n, seed):
    """the planted relation: denominator and n integer coefficients, drawn once from a fixed seed (declared in the raw README)"""
    r = random.Random(seed)
    den = r.choice([3, 5, 7, 9, 11, 13, 15, 21, 45])
    return den, [r.choice([-1, 1]) * r.randint(100, 9999) for _ in range(n)]


def pslq_run(x, tau, H):
    t0 = time.time()
    r = mp.pslq(x, tol=tau, maxcoeff=H, maxsteps=10**6)
    return r, time.time() - t0


def residual(r, x):
    return abs(sum(c * v for c, v in zip(r, x)))


def check_pslq(ev):
    grids = ["G1", "G2"]
    mp.mp.dps = 430
    agree = digits(ev[grids[0]]["Om4"], ev[grids[1]]["Om4"])
    d = int(max(30, min(PSLQ_DIGITS, math.floor(agree))))      # PSLQ needs at least 53 bits
    pert = mp.sqrt(2) / 1000        # irrational, so that the shifted constant is outside every basis's rational span (1 is in P2, P3)
    print(f"  PSLQ at {d} digits (the two grids share {float(agree):.1f}), tolerance 1e-{d - PSLQ_SLACK}")
    for name, (H, seed) in (PSLQ_BASES_C if CGRIDS_ON else PSLQ_BASES).items():
        with mp.workdps(d):
            tau = mp.mpf(10) ** (-(d - PSLQ_SLACK))
            names, cs = zip(*constants(name))
            cs_true = list(cs)
            cs = list(cs)
            if MUTATE == "pslq_wrong_basis":                  # PSLQ is given a basis that is not the one the target was built from
                cs[0] = cs[0] + pert
            n = len(cs)
            budget = (n + 1) * math.log10(2 * H + 1) + 1
            om4 = +ev[grids[1]]["Om4"]
            # planted truth: den * x = sum c_i b_i, through the same call
            den, c = planted(n, seed)
            xp = sum(ci * b for ci, b in zip(c, cs_true)) / den
            if MUTATE == "pslq_wrong_target":                 # the planted target is off by 1e-20 relative
                xp = xp * (1 + mp.mpf(10) ** -20)
            rp, tp = pslq_run([xp] + cs, tau, H)
            want = [den] + [-ci for ci in c]
            okp = rp is not None and (list(rp) == want or list(rp) == [-v for v in want])
            # perturbed basis on the planted target: must find nothing
            csp = list(cs)
            csp[1] = csp[1] + pert
            rpp, _ = pslq_run([xp] + csp, tau, H)
            report("Q" + name[1], okp and rpp is None,
                   f"{name} = {{Omega4, {', '.join(names)}}}, n = {n + 1}, H = {H}, d = {d}: planted relation (den {den}, seed {seed}) "
                   f"recovered: {okp} ({tp:.0f} s); perturbed basis on the planted target finds {'nothing' if rpp is None else list(rpp)}; "
                   f"budget (n + 1) log10(2H + 1) + 1 = {budget:.1f}")
            # the real target
            if not REAL:
                print(f"    REAL {name}: skipped (--no-real)", flush=True)
                continue
            rr, tr = pslq_run([om4] + cs, tau, H)
            found, why = False, "not found"
            if rr is not None:
                res = residual(rr, [om4] + cs)
                found = res <= tau and budget < d and rr[0] != 0      # a relation without Omega4 is among the constants alone
                why = f"relation {list(rr)}, residual {nd(res, 3)} (bar {nd(tau, 2)}), budget with H = {H}: {budget:.1f} < {d}: {budget < d}; Omega4 coefficient {rr[0]}"
                if found:
                    j = next(i for i in range(1, len(rr)) if rr[i] != 0)
                    csr = list(cs)
                    csr[j - 1] = csr[j - 1] + pert
                    rrp, _ = pslq_run([om4] + csr, tau, H)
                    found = found and rrp is None
                    why += f"; perturbed basis (constant {names[j - 1]} + sqrt(2)/1000) finds {'nothing' if rrp is None else list(rrp)}"
            print(f"    REAL {name}: " + (("FOUND (counts) " if found else "found but does not count ") + why if rr is not None
                                           else f"not found at H = {H} ({tr:.0f} s)"), flush=True)


# ---------------------------------------------------------------------------------------------------------------
# the remainder against #195's W^2
# ---------------------------------------------------------------------------------------------------------------
def read_w2(path):
    """{D: W2 string} of the 64-value list of w2_output.txt (qd values, 60 digits)"""
    lst = {}
    for line in open(path):
        m = re.match(r"\s*D=(\d+)\s+(\S+)\s+digits qd/od", line)
        if m:
            lst[int(m.group(1))] = m.group(2)
    return lst


def read_w2raw(path):
    """{D: W2 string} of the RESULT lines of I195-dh610/run_02 (qd, 60 digits) at D = 200, 500, 1000, 2000"""
    out = {}
    for line in open(path):
        m = re.search(r'"D":(\d+),"W2":"([^"]+)"', line)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def check_remainder(ev):
    mp.mp.dps = 80
    grids = ["G1", "G2"]
    om = [ev[grids[1]][f"Om{i}"] for i in range(1, 5)]
    if MUTATE == "wrong_Om4_series":
        om[3] = om[3] + mp.mpf(1) / 100
    lst = read_w2(W2FILE)
    if W2RAW:
        lst.update(read_w2raw(W2RAW))      # D = 1000, 2000 are not in the 64-value list

    def x(D):
        s = mp.mpf(2 * (D - 3))
        rem = mp.mpf(lst[D]) - (s - 4 * mp.ln2 + om[0] / s + om[1] / s**2 + om[2] / s**3 + om[3] / s**4)
        return rem, rem * s**5
    print("  six-term series s - 4 ln 2 + Omega1/s + ... + Omega4/s^4 against W^2 (qd, w2_output.txt), s = 2(D - 3):")
    print("  D       s       remainder              rem*s^5 (tends to Omega5)")
    xs = {}
    for D in (1000, 2000, 5103, 10000):
        rem, xs[D] = x(D)
        print(f"  {D:<6d} {2 * (D - 3):<7d} {nd(rem, 12):<22s} {nd(xs[D], 12)}")
    falls = xs[1000] > xs[2000] > xs[5103] > xs[10000] > 0
    s1, s2 = mp.mpf(2 * (5103 - 3)), mp.mpf(2 * (10000 - 3))
    est = (s2 * xs[10000] - s1 * xs[5103]) / (s2 - s1)
    report("R5", falls and abs(xs[10000] - xs[5103]) <= 500, f"rem*s^5 at D = 1000, 2000, 5103, 10^4 falls ({falls}); |x(10^4) - x(5103)| = "
           f"{nd(abs(xs[10000] - xs[5103]), 5)} (bar 500: a wrong Omega4 adds (error)*s, 10^4 per unit)")
    report("R6", mp.mpf("4.0e4") <= est <= mp.mpf("4.2e4"), f"two-point extrapolation (s2 x2 - s1 x1)/(s2 - s1) from D = 5103, 10^4: Omega5 ~ {nd(est, 8)} "
           f"(bar 4.0e4 to 4.2e4: an estimate, not a bound)")
    print("  reported, not gated: rem*s^5 at the D of the list")
    print("  D       rem*s^5")
    for D in sorted(lst):
        print(f"  {D:<7d} {nd(x(D)[1], 14)}")


def main():
    parse(sys.argv[1:])
    mp.mp.dps = 60
    print(f"order6.py  mutate={MUTATE}  parts={PARTS}  mpmath {mp.__version__}  sympy {sp.__version__}", flush=True)
    t0 = time.time()
    if "grid" in PARTS:
        check_grid()
    if "sym" in PARTS:
        check_sym()
    ev = None
    if "evals" in PARTS:
        ev = check_evals()
        if "values" in PARTS or not GRIDSEL:
            check_values(ev)
    elif LOAD and any(p in PARTS for p in ("values", "pslq", "remainder")):
        mp.mp.dps = 430
        ev = load_ev(LOAD)
        if "values" in PARTS:
            check_values(ev)
    if "pslq" in PARTS:
        check_pslq(ev)
    if "remainder" in PARTS:
        check_remainder(ev)
    nfail = sum(1 for _, ok in RESULTS if not ok)
    print(f"\n{len(RESULTS) - nfail} passed, {nfail} failed of {len(RESULTS)} checks; {time.time() - t0:.0f} s")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
