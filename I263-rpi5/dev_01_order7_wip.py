"""Order 7 of the matched expansion (matched.py, order3.py ... order6.py): Omega5 from G7 = 0 by method B, and the checks of issue #263.

W^2 a^2 = s + Omega, s = 2(D - 3), eps = 1/s, Omega = Omega0 + Omega1 eps + Omega2 eps^2 + ..., R = r^s, l = ln R = -2 ln cos(theta).
The order equations (E0 derives them from the master equation), the same for every k:
  dY_k/dl = F_{k-1},  F_{k-1} = sum_{j<k} L_{k-1-j} l^j / j!,   (R - 1) L_k' - L_k/2 = h_k,
  h_k = (1 - 1/R) L_{k-1} + sum_{j<k} Y_j c_{k-j} + Y_k/2,   L_k = -2 Omega_{k-1} + u C_k,   G_k = C_k(inf) = 0,
with u = sqrt(R - 1), C_k = int_1^R (h_k - Omega_{k-1}) (R' - 1)^{-3/2} dR'. G_k is affine in Omega_{k-2} with slope -4 pi:
G2 = 0 gives Omega0, ..., G6 = 0 Omega4, **G7 = 0 gives Omega5**. One path computes them all (`omega_chain`).

Method B (order4.py's PanelB, shared): v = sqrt(l), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the
spectral integration matrix; Y_k from the left, the tail C_right from the right, L_k = -2 h_k(1) - u C_right, G_k = C_right(0). It uses no
closed form of Y_k or L_k and no input value of Omega_0 .. Omega_4. Levels below k - 1 do not depend on Omega_{k-2}, so the chain keeps them
(`cached`; the same operations on the same numbers as the uncached chain, which CACHE compares).

    python3 order7.py grid --grid=N,w,V,dps [--kmax=7]      (a development run of one grid; no gate)
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

MUTATIONS = ("wrong_h", "wrong_c6", "wrong_c7", "wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3", "wrong_Om4", "coarse_B", "short_tail",
             "stale_cache", "pslq_wrong_basis", "pslq_wrong_target", "wrong_Om5_series", "wrong_closed4", "e1_sign", "e2_weight", "e3_factor")
MUTATE = None
W2FILE = "w2_output.txt"
SAVE = None
LOAD = None
GRIDARG = None
GRIDSEL = None
CGRIDS_ON = False
W2RAW = None
KMAX = 7
PARTS = []
REAL = True
BASES_SEL = None
PSLQ_CAP = None


def parse(argv):
    global MUTATE, W2FILE, W2RAW, SAVE, LOAD, GRIDARG, GRIDSEL, CGRIDS_ON, KMAX, PARTS, REAL, BASES_SEL, PSLQ_CAP
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
        elif a.startswith("--bases="):
            BASES_SEL = a.split("=", 1)[1].split(",")
        elif a.startswith("--pslq-cap="):
            PSLQ_CAP = int(a.split("=", 1)[1])
        elif a == "--cgrids":
            CGRIDS_ON = True
        elif a == "--no-real":
            REAL = False
        elif a.startswith("--kmax="):
            KMAX = int(a.split("=", 1)[1])
        else:
            parts.append(a)
    PARTS = parts or ["sym", "evals", "values", "pslq", "remainder"]


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
    if m == 7:           # new at this order: the coefficient of eps^7 of (1 + eps Om) e^{eps l} - (1/2 + eps)(1 - 1/R) e^{-eps l} - e^{-eps l}/(2R)
        return (Om[0] * l**6 / 720 + Om[1] * l**5 / 120 + Om[2] * l**4 / 24 + Om[3] * l**3 / 6 + Om[4] * l**2 / 2 + Om[5] * l + Om[6]
                + l**7 / 3360 - l**6 / 720 + (-1 if MUTATE == "wrong_c7" else 1) * l**6 / (720 * R))
    raise ValueError(m)


def hk(m, Om, l, R, Y, L):
    """h_m"""
    if m == 0:
        return Y[0] / 2
    return (1 - 1 / R) * L[m - 1] + sum(Y[j] * cc(m - j, Om, l, R) for j in range(m)) + Y[m] / 2


def Fsum(k, L, l):
    return sum(L[k - 1 - j] * l**j / math.factorial(j) for j in range(k))


# ---------------------------------------------------------------------------------------------------------------
# E0: the epsilon-expansion of the master equation against the table, k = 0 .. 7
# ---------------------------------------------------------------------------------------------------------------
def check_sym():
    t0 = time.time()
    R, eps, l = sp.symbols("R epsilon l", positive=True)
    Om = sp.symbols("Omega0:7")
    Ys, Ls = sp.symbols("Y0:8"), sp.symbols("L0:8")
    kk = 7
    r = sum((eps * l) ** j / sp.factorial(j) for j in range(kk + 1))          # exact through eps^7, which is all that is read
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
           f"h_k (k = 0 .. 7) and dY_k/dl (k = 1 .. 7) from the epsilon-expansion of the master equation against the table: "
           f"residuals {[str(x) for x in res if x != 0] or '0'} ({time.time() - t0:.1f} s)")


# ---------------------------------------------------------------------------------------------------------------
# method B at order k
# ---------------------------------------------------------------------------------------------------------------
class PanelK(PanelB):
    def __init__(self, N, w, V):
        super().__init__(N, w, V)
        self._lp, self._cg, self._Sg = {}, {}, None

    def grid(self, fn):
        return [[fn(p, i) for i in range(self.N)] for p in range(self.P)]

    def lp(self, j):
        """l^j / j! on the nodes"""
        if j not in self._lp:
            self._lp[j] = self.grid(lambda p, i: self.l[p][i] ** j / mp.factorial(j))
        return self._lp[j]

    def cg(self, m, Om):
        """c_m on the nodes (kept while Om[0 .. m - 1] stays the same)"""
        key = tuple(Om[:m])
        hit = self._cg.get(m)
        if hit is None or hit[0] != key:
            hit = (key, self.grid(lambda p, i: cc(m, Om, self.l[p][i], self.R[p][i])))
            self._cg[m] = hit
        return hit[1]

    def Sg(self):
        if self._Sg is None:
            self._Sg = self.grid(lambda p, i: self.Rm1[p][i] / self.R[p][i])                      # 1 - 1/R
        return self._Sg

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

    def yk(self, k, L):
        """Y_k = int_0^l F_{k-1} dl from the left (needs L_0 .. L_{k-1}; k >= 1)"""
        F = self.grid(lambda p, i: 2 * self.v[p][i] * mp.fdot([L[k - 1 - j][p][i] for j in range(k)], [self.lp(j)[p][i] for j in range(k)]))
        return self.cum_left(F)

    def lk(self, k, Om, Y, L, G):
        """append L_k and set G[k], from Y_0 .. Y_k and L_0 .. L_{k-1}; reads Om[0 .. k - 1] (Om[k - 1] is h_k(1), which drops out of G_k)"""
        thr = mp.mpf(1) / 2 if k == 0 else Om[k - 1]
        if k == 0:
            s = self.grid(lambda p, i: Y[0][p][i] / 2 - thr)
        else:
            cg = {m: self.cg(m, Om) for m in range(1, k + 1)}
            Sg = self.Sg()
            s = self.grid(lambda p, i: Sg[p][i] * L[k - 1][p][i] + mp.fdot([Y[j][p][i] for j in range(k)], [cg[k - j][p][i] for j in range(k)])
                          + Y[k][p][i] / 2 - thr)
        Cint = self.grid(lambda p, i: s[p][i] / self.Rm1[p][i] * self.R[p][i] / self.u[p][i] * 2 * self.v[p][i])
        Cr, G[k] = self.cum_right(Cint)
        L.append(self.grid(lambda p, i: -2 * thr - self.u[p][i] * Cr[p][i]))

    def hierarchy(self, Om, kmax):
        """Y_0 .. Y_kmax, L_0 .. L_kmax and G_0 .. G_kmax for the given Omega list, from level 0 (the uncached path)"""
        Y = [self.grid(lambda p, i: mp.mpf(1))]
        L, G = [], {}
        for k in range(kmax + 1):
            if k >= 1:
                Y.append(self.yk(k, L))
            self.lk(k, Om, Y, L, G)
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
    """Omega_0 .. Omega_4 of #26, #208 and #220 (derived there), the planted truth"""
    pi, ln2, z3, z5 = mp.pi, mp.ln2, mp.zeta(3), mp.zeta(5)
    return [-4 * ln2, 2 * pi**2 / 3 + 8 * ln2**2,
            80 * z3 - mp.mpf(8) / 3 * pi**2 * ln2 - mp.mpf(32) / 3 * ln2**3,
            22 * pi**4 / 45 + mp.mpf(16) / 3 * pi**2 * ln2**2 + mp.mpf(32) / 3 * ln2**4 - 320 * z3 * ln2 - 384 * z3,
            -10432 * z5 - 160 * pi**2 * z3 + 640 * ln2**2 * z3 - mp.mpf(64) / 9 * pi**2 * ln2**3 - mp.mpf(88) / 45 * pi**4 * ln2
            - mp.mpf(128) / 15 * ln2**5 - mp.mpf(2432) / 45 * pi**4 + 1536 * ln2 * z3 + 3072 * z3
            + (mp.mpf(1) / 1000 if MUTATE == "wrong_closed4" else 0)]


WRONG_OM = ("wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3", "wrong_Om4")


def omega_chain_ref(B, kmax, log=None):
    """Omega_0 .. Omega_{kmax-2} from G_2 .. G_kmax = 0, in turn, each G_k from the whole hierarchy (the uncached path); returns (Om, slopes, secs)"""
    Om = [mp.mpf(0)] * kmax
    slopes, secs = {}, {}
    cl = closed_omegas()
    for k in range(2, kmax + 1):
        t0 = time.time()
        Om_in = list(Om)
        for i, name in enumerate(WRONG_OM):
            if MUTATE == name and k >= i + 3:
                Om_in[i] = cl[i] + mp.mpf(1) / 100
        val, slope = solve_omega(lambda kk, o: B.hierarchy(o, kk)[2][kk], k, Om_in)
        Om[k - 2] = val
        slopes[k] = slope
        secs[k] = time.time() - t0
        if log:
            print(f"    k = {k}: Omega_{k - 2} = {nd(val, 30)}  slope {nd(slope, 20)}  ({secs[k]:.0f} s)", flush=True)
    return Om, slopes, secs, {}


def omega_chain(B, kmax, log=None):
    """The same chain with the levels below k - 1 kept: Y_j, L_j (j <= k - 2) do not depend on Omega_{k-2}. Per step: Y_{k-1}, two trials of
    L_{k-1}, Y_k, G_k at Omega_{k-2} = 0, 1, and L_{k-1} at the root. Returns (Om, slopes, secs, resid) with resid[k] = G_k at the root / |slope|."""
    if MUTATE in WRONG_OM:
        return omega_chain_ref(B, kmax, log=log)           # a wrong input must reach every level: recompute from level 0
    Om = [mp.mpf(0)] * kmax
    slopes, secs, resid = {}, {}, {}
    Y = [B.grid(lambda p, i: mp.mpf(1))]
    L, G = [], {}
    B.lk(0, Om, Y, L, G)
    stale = None
    for k in range(2, kmax + 1):
        t0 = time.time()
        Y.append(B.yk(k - 1, L))                                  # Y_{k-1}: from L_0 .. L_{k-2}, independent of Omega_{k-2}

        def trial(o):
            Omt = list(Om)
            Omt[k - 2] = o
            Yt, Lt, Gt = list(Y), list(L), {}
            B.lk(k - 1, Omt, Yt, Lt, Gt)
            Yt.append(B.yk(k, Lt))
            B.lk(k, Omt, Yt, Lt, Gt)
            return Gt[k], Lt[k - 1]
        g0, l0 = trial(mp.mpf(0))
        g1, _ = trial(mp.mpf(1))
        val, slope = -g0 / (g1 - g0), g1 - g0
        Om[k - 2] = val
        slopes[k] = slope
        if MUTATE == "stale_cache" and k >= 3:
            L.append(l0)                                          # level k - 1 from the first trial, not recomputed at the root
        else:
            B.lk(k - 1, Om, Y, L, G)                              # level k - 1 at the root (G_{k-1} at the root is read below)
        if k >= 3:
            resid[k - 1] = abs(G[k - 1]) / abs(slopes[k - 1])
        if k == kmax:                                             # the last order: G_kmax at the root, through one more pair of levels
            Yt, Lt, Gt = list(Y), list(L), {}
            Yt.append(B.yk(k, Lt))
            B.lk(k, Om, Yt, Lt, Gt)
            resid[k] = abs(Gt[k]) / abs(slope)
        secs[k] = time.time() - t0
        if log:
            print(f"    k = {k}: Omega_{k - 2} = {nd(val, 30)}  slope {nd(slope, 20)}  ({secs[k]:.0f} s)", flush=True)
    return Om, slopes, secs, resid


def run_B(N, w, V, dps, kmax=7, log=False, cached=True):
    t0 = time.time()
    if MUTATE == "coarse_B":
        N = 10
    if MUTATE == "short_tail":
        V = 6
    with mp.workdps(dps):
        w = mp.mpf(w[0]) / w[1] if isinstance(w, tuple) else mp.mpf(w)
        tinit = time.time()
        B = PanelK(N, w, V)
        tinit = time.time() - tinit
        Om, slopes, secs, resid = (omega_chain if cached else omega_chain_ref)(B, kmax, log=log)
        out = {f"Om{i}": +Om[i] for i in range(kmax - 1)}
        out.update({f"slope{k}": +s for k, s in slopes.items()})
        out.update({f"resid{k}": +r for k, r in resid.items()})
        out["secs"] = time.time() - t0
        out["init_secs"] = tinit
        out["grid"] = f"N={N} w={mp.nstr(w, 6)} V={V} dps={dps} panels={B.P}"
    return out


# declared grids and the control grids are fixed in the raw README before the runs of record (see there)
GRIDS = {}
REPORT_GRIDS = {}
CGRIDS = {}


def save_ev(ev, path):
    with open(path, "w") as f:
        json.dump({n: {k: (mp.nstr(v, 600) if isinstance(v, mp.mpf) else v) for k, v in e.items()} for n, e in ev.items()}, f, indent=1)


def load_ev(paths):
    out = {}
    for path in paths.split(","):
        raw = json.load(open(path))
        out.update({n: {k: (mp.mpf(v) if k.startswith(("Om", "slope", "resid")) else v) for k, v in e.items()} for n, e in raw.items()})
    return out


def check_grid():
    """one grid, no gate: the development run"""
    N, w, V, dps = GRIDARG.split(",")
    mp.mp.dps = 60
    e = run_B(int(N), tuple(int(t) for t in w.split("/")) if "/" in w else w, int(V), int(dps), kmax=KMAX, log=True)
    mp.mp.dps = int(dps)
    cl = closed_omegas()
    print(f"  {e['grid']}  {e['secs']:.0f} s (panel setup {e['init_secs']:.0f} s)")
    for i in range(KMAX - 1):
        print(f"    Omega{i} = {nd(e[f'Om{i}'], int(dps))}")
    for i in range(min(5, KMAX - 1)):
        print(f"    Omega{i} against closed form: {float(digits(cl[i], e[f'Om{i}'])):.1f} digits")
    for k in range(2, KMAX + 1):
        print(f"    slope G{k} against -4 pi: {float(digits(-4 * mp.pi, e[f'slope{k}'])):.1f} digits")
    for k, r in sorted((int(n[5:]), e[n]) for n in e if n.startswith("resid")):
        print(f"    |G{k}| at the root / |slope| = {nd(r, 3)}")
    return e


def check_cache():
    """CACHE: the cached chain against the uncached chain, on a small grid: the same Omegas"""
    N, w, V, dps = 24, (1, 2), 12, 60
    mp.mp.dps = 40
    a = run_B(N, w, V, dps, kmax=7)
    b = run_B(N, w, V, dps, kmax=7, cached=False)
    mp.mp.dps = dps
    worst = max(abs(a[f"Om{i}"] - b[f"Om{i}"]) / abs(b[f"Om{i}"]) for i in range(6))
    dig = [float(digits(b[f"Om{i}"], a[f"Om{i}"])) for i in range(6)]
    report("CACHE", worst <= mp.mpf(10) ** -(dps - 5),
           f"cached chain against the uncached chain on (N {N}, w 1/2, V {V}, {dps} digits): Omega0 .. Omega5 equal to "
           + ", ".join(f"{d:.1f}" for d in dig) + f" digits, worst relative difference {nd(worst, 3)} (bar 1e-{dps - 5}); times {a['secs']:.0f} s and {b['secs']:.0f} s")


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
        print(f"  {name}: {e['grid']}  {e['secs']:.0f} s (panel setup {e['init_secs']:.0f} s)\n    Omega0 = {nd(e['Om0'], 60)}\n    Omega1 = {nd(e['Om1'], 60)}"
              f"\n    Omega2 = {nd(e['Om2'], 60)}\n    Omega3 = {nd(e['Om3'], 110)}\n    Omega4 = {nd(e['Om4'], 200)}\n    Omega5 = {nd(e['Om5'], dps - 40)}"
              "\n    slopes G2 .. G7 = " + " ".join(nd(e[f"slope{k}"], 20) for k in range(2, 8))
              + "\n    |G_k| at the root / |slope|, k = 2 .. 7 = " + " ".join(nd(e[f"resid{k}"], 3) for k in range(2, 8)), flush=True)
    if SAVE:
        save_ev(ev, SAVE)
    return ev


OM5_REF = None          # the Omega5 of record (set in the controls after the runs of record, for PLW of `wrong_Om4`)


def check_values(ev):
    mp.mp.dps = max(int(e["grid"].split("dps=")[1].split()[0]) for e in ev.values()) + 30
    cl = closed_omegas()
    grids = ["G1", "G2"]
    # PL0 .. PL4: the planted orders by the same code
    for i, cid in enumerate(("PL0", "PL1", "PL2", "PL3", "PL4")):
        rows = {n: digits(cl[i], ev[n][f"Om{i}"]) for n in ev}
        ok = all(rows[n] >= 100 for n in grids)
        report(cid, ok, f"planted: Omega{i} against its closed form, digits: " + ", ".join(f"{n} {float(d):.1f}" for n, d in rows.items())
               + " (bar 100 on G1, G2; the others reported)")
    # PLW: a wrong input must move the orders above it (the control's own statement, evaluated when a wrong-input mutation is on)
    if MUTATE in WRONG_OM:
        i = int(MUTATE[-1]) + 1
        ref = cl[i] if i < 5 else mp.mpf(OM5_REF)
        moved = all(abs(ev[n][f"Om{i}"] - ref) > mp.mpf(1) / 1000 for n in grids)
        report("PLW", moved, f"control {MUTATE} moves Omega{i} of " + ", ".join(f"{n} by {nd(ev[n][f'Om{i}'] - ref, 5)}" for n in grids))
    # SL: slopes
    rows, ok = [], True
    for n in ev:
        ds = [digits(-4 * mp.pi, ev[n][f"slope{k}"]) for k in range(2, 8)]
        rows.append(f"{n} " + "/".join(f"{float(d):.1f}" for d in ds))
        ok = ok and (n not in grids or min(ds) >= 100)
    report("SL", ok, "slope of G_k in Omega_(k-2) against -4 pi, k = 2 .. 7, digits: " + ", ".join(rows) + " (bar 100 on G1, G2)")
    # RES: G_k at the root
    rs = {n: max(ev[n][f"resid{k}"] for k in range(2, 8)) for n in ev}
    report("RES", all(rs[n] <= mp.mpf(10) ** -100 for n in grids),
           "max over k = 2 .. 7 of |G_k at the chain's root| / |slope|: " + ", ".join(f"{n} {nd(r, 3)}" for n, r in rs.items()) + " (bar 1e-100 on G1, G2)")
    # M5: the two grids on Omega5
    a, b = grids
    d5 = digits(ev[a]["Om5"], ev[b]["Om5"])
    report("M5", d5 >= 100, f"Omega5 of {a} against {b} (two grids, two precisions): {float(d5):.1f} digits (bar 100); |diff| = "
           f"{nd(abs(ev[a]['Om5'] - ev[b]['Om5']), 3)}")
    # RNG: the range of the estimate
    report("RNG", all(mp.mpf("4.0e4") <= ev[n]["Om5"] <= mp.mpf("4.2e4") for n in grids), "Omega5 between 4.0e4 and 4.2e4: "
           + ", ".join(f"{n} {nd(ev[n]['Om5'], 12)}" for n in grids))
    others = [n for n in ev if n not in grids]
    print("  reported: digits between evaluations, Omega4 / Omega5: " + ", ".join(
        f"{x}-{y} " + "/".join(f"{float(digits(ev[x][f'Om{i}'], ev[y][f'Om{i}'])):.1f}" for i in (4, 5))
        for x, y in [("G1", "G2")] + [(o, "G1") for o in others]))
    return d5


# ---------------------------------------------------------------------------------------------------------------
# PSLQ
# ---------------------------------------------------------------------------------------------------------------
PSLQ_DIGITS = 330             # cap on the working digits; the digits the two grids share, less 32, if fewer
PSLQ_SLACK = 12               # tolerance 10^-(d - slack)
VERIFY_EXTRA = 20             # a relation must hold at this many more digits than were used to find it


def weighted_constants():
    """{weight: [(name, value)]}: the monomials ln2^a (pi^2)^b zeta(3)^c zeta(5)^e zeta(7)^f of weight a + 2b + 3c + 5e + 7f, and the
    polylogarithm products Li4(1/2) x {1, ln 2, ln^2 2, pi^2}, Li5(1/2) x {1, ln 2}, Li6(1/2)"""
    pi, q, z3, z5, z7 = mp.pi, mp.ln2, mp.zeta(3), mp.zeta(5), mp.zeta(7)
    p2 = pi**2
    li4, li5, li6 = mp.polylog(4, mp.mpf(1) / 2), mp.polylog(5, mp.mpf(1) / 2), mp.polylog(6, mp.mpf(1) / 2)
    w = {0: [("1", mp.mpf(1))], 1: [("ln 2", q)], 2: [("ln^2 2", q**2), ("pi^2", p2)],
         3: [("ln^3 2", q**3), ("pi^2 ln 2", p2 * q), ("zeta(3)", z3)],
         4: [("ln^4 2", q**4), ("pi^2 ln^2 2", p2 * q**2), ("pi^4", p2**2), ("zeta(3) ln 2", z3 * q)],
         5: [("ln^5 2", q**5), ("pi^2 ln^3 2", p2 * q**3), ("pi^4 ln 2", p2**2 * q), ("zeta(3) ln^2 2", z3 * q**2), ("pi^2 zeta(3)", p2 * z3),
             ("zeta(5)", z5)],
         6: [("ln^6 2", q**6), ("pi^2 ln^4 2", p2 * q**4), ("pi^4 ln^2 2", p2**2 * q**2), ("pi^6", p2**3), ("zeta(3) ln^3 2", z3 * q**3),
             ("pi^2 zeta(3) ln 2", p2 * z3 * q), ("zeta(3)^2", z3**2), ("zeta(5) ln 2", z5 * q)],
         7: [("ln^7 2", q**7), ("pi^2 ln^5 2", p2 * q**5), ("pi^4 ln^3 2", p2**2 * q**3), ("pi^6 ln 2", p2**3 * q), ("zeta(3) ln^4 2", z3 * q**4),
             ("pi^2 zeta(3) ln^2 2", p2 * z3 * q**2), ("pi^4 zeta(3)", p2**2 * z3), ("zeta(3)^2 ln 2", z3**2 * q), ("zeta(5) ln^2 2", z5 * q**2),
             ("pi^2 zeta(5)", p2 * z5), ("zeta(7)", z7)]}
    li = {4: [("Li4(1/2)", li4)], 5: [("Li4(1/2) ln 2", li4 * q), ("Li5(1/2)", li5)], 6: [("Li4(1/2) ln^2 2", li4 * q**2), ("Li4(1/2) pi^2", li4 * p2),
                                                                                           ("Li5(1/2) ln 2", li5 * q), ("Li6(1/2)", li6)]}
    return w, li


# basis name -> (weights of the monomials, weights of the polylogarithm products, maxcoeff H, planted seed); the bases of the raw README
PSLQ_BASES = {"Q1": ((6,), (), 10**12, 263001), "Q2": ((6,), (6,), 10**12, 263002), "Q3": ((6, 5), (), 10**11, 263003),
              "Q4": ((6, 5, 4), (), 10**10, 263004), "Q5": ((6, 5, 4, 3), (), 10**10, 263005), "Q6": ((6, 5, 4, 3, 2, 1, 0), (), 10**9, 263006),
              "Q7": ((6, 5, 4, 3, 2, 1, 0), (4, 5, 6), 10**9, 263007), "Q8": ((6, 5, 4, 3), (4, 5, 6), 10**9, 263008),
              "Q9": ((7, 6, 5, 4, 3, 2, 1, 0), (), 10**8, 263009)}
PSLQ_BASES_C = {n: (a, b, min(h, 10**5 if n in ("Q6", "Q7", "Q8", "Q9") else h), s) for n, (a, b, h, s) in PSLQ_BASES.items()}      # --cgrids: d ~ 110


def constants(name):
    w, li = weighted_constants()
    mons, lis, _, _ = PSLQ_BASES[name]
    return [c for k in mons for c in w[k]] + [c for k in lis for c in li[k]]


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
    mp.mp.dps = max(int(e["grid"].split("dps=")[1].split()[0]) for e in ev.values()) + 30
    agree = digits(ev[grids[0]]["Om5"], ev[grids[1]]["Om5"])
    cap = PSLQ_CAP or PSLQ_DIGITS
    d = int(max(30, min(cap, math.floor(agree) - (PSLQ_SLACK + VERIFY_EXTRA))))      # PSLQ needs at least 53 bits
    pert = mp.sqrt(2) / 1000        # irrational, so that the shifted constant is outside every basis's rational span (1 is in some bases)
    print(f"  PSLQ at {d} digits (the two grids share {float(agree):.1f}), tolerance 1e-{d - PSLQ_SLACK}, verification at {d + VERIFY_EXTRA} digits", flush=True)
    for name, (_, _, H, seed) in (PSLQ_BASES_C if CGRIDS_ON else PSLQ_BASES).items():
        if BASES_SEL and name not in BASES_SEL:
            continue
        with mp.workdps(d):
            tau = mp.mpf(10) ** (-(d - PSLQ_SLACK))
            names, cs = zip(*constants(name))
            cs_true = list(cs)
            cs = list(cs)
            if MUTATE == "pslq_wrong_basis":                  # PSLQ is given a basis that is not the one the target was built from
                cs[0] = cs[0] + pert
            n = len(cs)
            budget = (n + 1) * math.log10(2 * H + 1) + 1
            om5 = +ev[grids[1]]["Om5"]
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
            csp[1 if n > 1 else 0] = csp[1 if n > 1 else 0] + pert
            rpp, _ = pslq_run([xp] + csp, tau, H)
            report("P" + name, okp and rpp is None,
                   f"{name} = {{Omega5, {', '.join(names)}}}, n = {n + 1}, H = {H}, d = {d}: planted relation (den {den}, seed {seed}) "
                   f"recovered: {okp} ({tp:.0f} s); perturbed basis on the planted target finds {'nothing' if rpp is None else list(rpp)}; "
                   f"budget (n + 1) log10(2H + 1) + 1 = {budget:.1f}")
            # the real target
            if not REAL:
                print(f"    REAL {name}: skipped (--no-real)", flush=True)
                continue
            rr, tr = pslq_run([om5] + cs, tau, H)
            found, why = False, "not found"
            if rr is not None:
                res = residual(rr, [om5] + cs)
                found = res <= tau and budget < d and rr[0] != 0      # a relation without Omega5 is among the constants alone
                why = f"relation {list(rr)}, residual {nd(res, 3)} (bar {nd(tau, 2)}), budget with H = {H}: {budget:.1f} < {d}: {budget < d}; Omega5 coefficient {rr[0]}"
                if found:
                    j = next(i for i in range(1, len(rr)) if rr[i] != 0)
                    csr = list(cs)
                    csr[j - 1] = csr[j - 1] + pert
                    rrp, _ = pslq_run([om5] + csr, tau, H)
                    found = found and rrp is None
                    why += f"; perturbed basis (constant {names[j - 1]} + sqrt(2)/1000) finds {'nothing' if rrp is None else list(rrp)}"
                    # verification at VERIFY_EXTRA more digits, on both grids
                    with mp.workdps(d + VERIFY_EXTRA):
                        csv = [c_ for _, c_ in constants(name)]
                        tv = mp.mpf(10) ** -(d + VERIFY_EXTRA - PSLQ_SLACK)
                        vres = {g: residual(rr, [ev[g]["Om5"]] + csv) for g in grids}
                        vok = all(r_ <= tv for r_ in vres.values())
                        found = found and vok
                        why += (f"; verified at {d + VERIFY_EXTRA} digits (bar {nd(tv, 2)}): " + ", ".join(f"{g} {nd(r_, 3)}" for g, r_ in vres.items())
                                + f" -> {vok}")
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


def refit_windows(lst, om, Ks=(14, 18, 22, 26, 30, 36, 44)):
    """Omega5 from the 64 values of W^2 with Omega0 .. Omega4 fixed: y = (W^2 - [s + Omega0 + Omega1/s + ... + Omega4/s^4]) s^5 =
    Omega5 + Omega6/s + ..., polynomial extrapolation to 1/s = 0 through the K points of largest s; returns {K: estimate}"""
    pts = []
    for D in sorted(lst):
        s = mp.mpf(2 * (D - 3))
        pts.append((1 / s, (mp.mpf(lst[D]) - (s + sum(om[i] / s**i for i in range(5)))) * s**5))
    out = {}
    for K in Ks:
        w = pts[len(pts) - K:]
        est = mp.mpf(0)
        for i, (ti, yi) in enumerate(w):
            Li = mp.mpf(1)
            for j, (tj, _) in enumerate(w):
                if j != i:
                    Li *= (0 - tj) / (ti - tj)
            est += Li * yi
        out[K] = est
    return out


X3_BAR = None           # declared in the raw README after the development run (see there)
R7_BAR = None


def check_remainder(ev):
    mp.mp.dps = 80
    grids = ["G1", "G2"]
    om = [ev[grids[1]][f"Om{i}"] for i in range(1, 6)]
    if MUTATE == "wrong_Om5_series":
        om[4] = om[4] + 1
    lst = read_w2(W2FILE)
    if W2RAW:
        lst.update(read_w2raw(W2RAW))      # D = 1000, 2000 are not in the 64-value list

    def x(D, nterms):
        s = mp.mpf(2 * (D - 3))
        rem = mp.mpf(lst[D]) - (s - 4 * mp.ln2 + sum(om[i] / s ** (i + 1) for i in range(nterms)))
        return rem, rem * s ** (nterms + 1)
    print("  W^2 (qd, w2_output.txt) against the series s - 4 ln 2 + Omega1/s + ... (Omega1 .. Omega5 of G2), s = 2(D - 3):")
    print("  D       s       rem6 s^5 (tends to Omega5)    (rem6 s^5 - Omega5) s (tends to Omega6)   rem7 s^6 (tends to Omega6)")
    xs6, xs7 = {}, {}
    for D in (1000, 2000, 5103, 10000):
        s = mp.mpf(2 * (D - 3))
        _, xs6[D] = x(D, 4)
        _, xs7[D] = x(D, 5)
        print(f"  {D:<6d} {2 * (D - 3):<7d} {nd(xs6[D], 14):<28s} {nd((xs6[D] - om[4]) * s, 12):<40s} {nd(xs7[D], 12)}")
    s1, s2 = mp.mpf(2 * (5103 - 3)), mp.mpf(2 * (10000 - 3))
    est6 = (s2 * xs6[10000] - s1 * xs6[5103]) / (s2 - s1)
    report("R6", abs(est6 - om[4]) <= mp.mpf(1) / 1000 * abs(om[4]), f"two-point extrapolation (s2 x2 - s1 x1)/(s2 - s1) of rem6 s^5 from D = 5103, 10^4: {nd(est6, 8)} against the computed "
           f"Omega5 {nd(om[4], 8)}, relative difference {nd((est6 - om[4]) / om[4], 3)} (bar 1e-3: an estimate, not a bound)")
    falls = all(xs7[a] != 0 for a in xs7) and R7_BAR is not None and abs(xs7[10000] - xs7[5103]) <= R7_BAR
    report("R7", falls, f"rem7 s^6 at D = 5103 and 10^4 differs by {nd(abs(xs7[10000] - xs7[5103]), 5)} (bar {R7_BAR}: a wrong Omega5 adds (error) s, about 10^4 per unit)")
    # X3: Omega5 from the crate's 64 values with Omega0 .. Omega4 fixed (the closed forms)
    mp.mp.dps = 120
    est = refit_windows(read_w2(W2FILE), closed_omegas())
    rows = {n: {K: abs(e - ev[n]["Om5"]) for K, e in est.items()} for n in grids}
    mx = max(max(r.values()) for r in rows.values())
    report("X3", X3_BAR is not None and mx <= X3_BAR, "Omega5 against the polynomial extrapolation in 1/s of #195's 64 W^2 values (Omega0 .. Omega4 fixed at the closed forms), "
           "windows of the K largest s, |difference| " + "; ".join(f"{n}: " + ", ".join(f"K = {K} {nd(d, 2)}" for K, d in r.items()) for n, r in rows.items())
           + f" (bar {X3_BAR} on every window; the spread over windows is an estimator range, {nd(mx, 2)}; not a bound)")
    mp.mp.dps = 80
    print("  reported, not gated: rem6 s^5 at the D of the list")
    print("  D       rem6 s^5")
    for D in sorted(lst):
        print(f"  {D:<7d} {nd(x(D, 4)[1], 14)}")


def main():
    parse(sys.argv[1:])
    mp.mp.dps = 60
    print(f"order7.py  mutate={MUTATE}  parts={PARTS}  mpmath {mp.__version__}  sympy {sp.__version__}", flush=True)
    t0 = time.time()
    if "grid" in PARTS:
        check_grid()
    if "cache" in PARTS:
        check_cache()
    if "sym" in PARTS:
        check_sym()
    ev = None
    if "evals" in PARTS:
        ev = check_evals()
        if "values" in PARTS or not GRIDSEL:
            check_values(ev)
    elif LOAD and any(p in PARTS for p in ("values", "pslq", "remainder", "reduce7")):
        mp.mp.dps = 600
        ev = load_ev(LOAD)
        if "values" in PARTS:
            check_values(ev)
    if "exch7" in PARTS:
        check_exch7()
    if "reduce7" in PARTS:
        check_reduce7(ev)
    if "pslq" in PARTS:
        check_pslq(ev)
    if "remainder" in PARTS:
        check_remainder(ev)
    nfail = sum(1 for _, ok in RESULTS if not ok)
    print(f"\n{len(RESULTS) - nfail} passed, {nfail} failed of {len(RESULTS)} checks; {time.time() - t0:.0f} s")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
