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

MUTATIONS = ("wrong_h", "wrong_c6", "wrong_Om0", "wrong_Om1", "wrong_Om2", "wrong_Om3", "coarse_B", "short_tail")
MUTATE = None
W2FILE = "w2_output.txt"
SAVE = None
LOAD = None
GRIDARG = None
W2RAW = None
KMAX = 6
PARTS = []
REAL = True


def parse(argv):
    global MUTATE, W2FILE, W2RAW, SAVE, LOAD, GRIDARG, KMAX, PARTS, REAL
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


OM4_FIT = "-12794.499860023"          # #195's fit (w2_output.txt: 14 digits, range over the 6 admitted cells 1.5e-30)


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


def main():
    parse(sys.argv[1:])
    mp.mp.dps = 60
    print(f"order6.py  mutate={MUTATE}  parts={PARTS}  mpmath {mp.__version__}  sympy {sp.__version__}", flush=True)
    t0 = time.time()
    if "grid" in PARTS:
        check_grid()
    nfail = sum(1 for _, ok in RESULTS if not ok)
    print(f"\n{len(RESULTS) - nfail} passed, {nfail} failed of {len(RESULTS)} checks; {time.time() - t0:.0f} s")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
