"""Order 5 of the matched expansion (matched.py, order3.py, order4.py): Omega3 from G5 = 0 by method B, and the checks of issue #208.

W^2 a^2 = s + Omega, s = 2(D - 3), eps = 1/s, Omega = Omega0 + Omega1 eps + Omega2 eps^2 + Omega3 eps^3 + ..., R = r^s, l = ln R.
The order equations (E0 derives them from the master equation), the same for every k:
  dY_k/dl = F_{k-1},  F_{k-1} = sum_{j<k} L_{k-1-j} l^j / j!,   (R - 1) L_k' - L_k/2 = h_k,
  h_k = (1 - 1/R) L_{k-1} + sum_{j<k} Y_j c_{k-j} + Y_k/2,   L_k = -2 Omega_{k-1} + u C_k,   G_k = C_k(inf) = 0,
with u = sqrt(R - 1), C_k = int_1^R (h_k - Omega_{k-1}) (R' - 1)^{-3/2} dR'. G_k is affine in Omega_{k-2} with slope -4 pi:
G2 = 0 gives Omega0, G3 = 0 Omega1, G4 = 0 Omega2, **G5 = 0 gives Omega3**. One path computes them all (`omega_chain`).

Method B (order4.py's PanelB, shared): v = sqrt(l), panels of width w on [0, V], N Chebyshev nodes per panel, cumulative integrals by the
spectral integration matrix; Y_k from the left, the tail C_right from the right, L_k = -2 h_k(1) - u C_right, G_k = C_right(0). It uses no
closed form of Y_k or L_k and no input value of Omega_0 .. Omega_2.

    python3 order5.py [sym] [evals] [pslq] [remainder] [--mutate=NAME] [--w2=w2_output.txt] [--save=FILE] [--load=FILE]
    python3 order5.py grid --grid=N,w,V,dps [--kmax=5]      (a development run of one grid; no gate)

No argument runs sym, evals, pslq, remainder. The exit status is 1 when a check fails. Status words: sympy residual 0 is "checked
symbolically", an agreement of integrals "numerical evidence", a PSLQ relation an "identification"; a spread between grids or precisions
is an estimator range, not a bound.
"""
import math
import os
import re
import sys
import time

import mpmath as mp
import sympy as sp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
_argv, sys.argv = sys.argv, sys.argv[:1]          # order4.py parses sys.argv when it is imported
from order4 import PanelB  # noqa: E402
sys.argv = _argv

MUTATIONS = ("wrong_h", "wrong_c5", "wrong_Om0", "wrong_Om1", "wrong_Om2", "coarse_B", "short_tail", "pslq_wrong_basis",
             "wrong_Om3_series")
MUTATE = None
W2FILE = "w2_output.txt"
SAVE = None
LOAD = None
GRIDARG = None
KMAX = 5
PARTS = []


def parse(argv):
    global MUTATE, W2FILE, SAVE, LOAD, GRIDARG, KMAX, PARTS
    parts = []
    for a in argv:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
            assert MUTATE in MUTATIONS, f"unknown mutation {MUTATE}; known: {MUTATIONS}"
        elif a.startswith("--w2="):
            W2FILE = a.split("=", 1)[1]
        elif a.startswith("--save="):
            SAVE = a.split("=", 1)[1]
        elif a.startswith("--load="):
            LOAD = a.split("=", 1)[1]
        elif a.startswith("--grid="):
            GRIDARG = a.split("=", 1)[1]
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
                + (-1 if MUTATE == "wrong_c5" else 1) * l**4 / (24 * R))
    raise ValueError(m)


def hk(m, Om, l, R, Y, L):
    """h_m"""
    if m == 0:
        return Y[0] / 2
    return (1 - 1 / R) * L[m - 1] + sum(Y[j] * cc(m - j, Om, l, R) for j in range(m)) + Y[m] / 2


def Fsum(k, L, l):
    return sum(L[k - 1 - j] * l**j / math.factorial(j) for j in range(k))


# ---------------------------------------------------------------------------------------------------------------
# E0: the epsilon-expansion of the master equation against the table, k = 0 .. 5
# ---------------------------------------------------------------------------------------------------------------
def check_sym():
    t0 = time.time()
    R, eps, l = sp.symbols("R epsilon l", positive=True)
    Om = sp.symbols("Omega0:5")
    Ys, Ls = sp.symbols("Y0:6"), sp.symbols("L0:6")
    kk = 5
    r = sum((eps * l) ** j / sp.factorial(j) for j in range(kk + 1))          # exact through eps^5, which is all that is read
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
           f"h_k (k = 0 .. 5) and dY_k/dl (k = 1 .. 5) from the epsilon-expansion of the master equation against the table: "
           f"residuals {[str(x) for x in res if x != 0] or '0'} ({time.time() - t0:.1f} s)")


# ---------------------------------------------------------------------------------------------------------------
# method B at order k
# ---------------------------------------------------------------------------------------------------------------
class PanelK(PanelB):
    def hierarchy(self, Om, kmax):
        """Y_0 .. Y_kmax, L_0 .. L_kmax and G_0 .. G_kmax for the given Omega list (Om[kmax - 1] is not used: h_kmax(1) = Om[kmax - 1])"""
        N, P = self.N, self.P
        grid = lambda fn: [[fn(p, i) for i in range(N)] for p in range(P)]  # noqa: E731
        Y = [grid(lambda p, i: mp.mpf(1))]
        L = []
        G = {}
        for k in range(kmax + 1):
            if k >= 1:
                F = grid(lambda p, i: 2 * self.v[p][i] * sum(L[k - 1 - j][p][i] * self.l[p][i] ** j / mp.factorial(j)
                                                             for j in range(k)))
                Y.append(self.cum_left(F))
            thr = mp.mpf(1) / 2 if k == 0 else Om[k - 1]
            s = grid(lambda p, i: hk(k, Om, self.l[p][i], self.R[p][i], [y[p][i] for y in Y],
                                     [lv[p][i] for lv in L] if k else None) - thr)
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


def omega_chain(B, kmax, log=None):
    """Omega_0 .. Omega_{kmax-2} from G_2 .. G_kmax = 0, in turn, by the same code at every order; returns (Om, slopes, seconds per order)"""
    Om = [mp.mpf(0)] * kmax
    slopes, secs = {}, {}
    for k in range(2, kmax + 1):
        t0 = time.time()
        Om_in = list(Om)
        if MUTATE == "wrong_Om0" and k >= 3:
            Om_in[0] = -4 * mp.ln2 + mp.mpf(1) / 100
        if MUTATE == "wrong_Om1" and k >= 4:
            Om_in[1] = 2 * mp.pi**2 / 3 + 8 * mp.ln2**2 + mp.mpf(1) / 100
        if MUTATE == "wrong_Om2" and k >= 5:
            Om_in[2] = (80 * mp.zeta(3) - mp.mpf(8) / 3 * mp.pi**2 * mp.ln2 - mp.mpf(32) / 3 * mp.ln2**3) + mp.mpf(1) / 100
        val, slope = solve_omega(lambda kk, o: B.hierarchy(o, kk)[2][kk], k, Om_in)
        Om[k - 2] = val
        slopes[k] = slope
        secs[k] = time.time() - t0
        if log:
            print(f"    k = {k}: Omega_{k - 2} = {nd(val, 30)}  slope {nd(slope, 20)}  ({secs[k]:.0f} s)", flush=True)
    return Om, slopes, secs


def run_B(N, w, V, dps, kmax=5, log=False):
    t0 = time.time()
    if MUTATE == "coarse_B":
        N = 10
    if MUTATE == "short_tail":
        V = 6
    with mp.workdps(dps):
        B = PanelK(N, w, V)
        Om, slopes, secs = omega_chain(B, kmax, log=log)
        out = {f"Om{i}": +Om[i] for i in range(kmax - 1)}
        out.update({f"slope{k}": +s for k, s in slopes.items()})
        out["secs"] = time.time() - t0
        out["grid"] = f"N={N} w={mp.nstr(mp.mpf(w), 6)} V={V} dps={dps} panels={B.P}"
    return out


# ---------------------------------------------------------------------------------------------------------------
# the closed forms of the planted orders, #195's fit
# ---------------------------------------------------------------------------------------------------------------
def closed_omegas():
    return [-4 * mp.ln2, 2 * mp.pi**2 / 3 + 8 * mp.ln2**2,
            80 * mp.zeta(3) - mp.mpf(8) / 3 * mp.pi**2 * mp.ln2 - mp.mpf(32) / 3 * mp.ln2**3]


def read_fit(path):
    txt = open(path).read()
    return mp.mpf(re.search(r"Omega3 = (\S+)", txt).group(1)), mp.mpf(re.search(r"Omega4 = (\S+)", txt).group(1))


# declared grids: name -> (N, w, V, working digits)
GRIDS = {}


def check_grid():
    """one grid, no gate: the development run"""
    N, w, V, dps = GRIDARG.split(",")
    mp.mp.dps = 60
    e = run_B(int(N), mp.mpf(w), int(V), int(dps), kmax=KMAX, log=True)
    mp.mp.dps = int(dps)
    cl = closed_omegas()
    fit, _ = read_fit(W2FILE)
    print(f"  {e['grid']}  {e['secs']:.0f} s")
    for i in range(KMAX - 1):
        print(f"    Omega{i} = {nd(e[f'Om{i}'], int(dps))}")
    for i in range(3):
        if f"Om{i}" in e:
            print(f"    Omega{i} against closed form: {float(digits(cl[i], e[f'Om{i}'])):.1f} digits")
    if "Om3" in e:
        print(f"    Omega3 against #195's fit: difference {nd(e['Om3'] - fit, 5)}")
    for k in range(2, KMAX + 1):
        print(f"    slope G{k} against -4 pi: {float(digits(-4 * mp.pi, e[f'slope{k}'])):.1f} digits")
    return e


def main():
    parse(sys.argv[1:])
    mp.mp.dps = 60
    print(f"order5.py  mutate={MUTATE}  parts={PARTS}  mpmath {mp.__version__}  sympy {sp.__version__}", flush=True)
    t0 = time.time()
    if "grid" in PARTS:
        check_grid()
    if "sym" in PARTS:
        check_sym()
    nfail = sum(1 for _, ok in RESULTS if not ok)
    print(f"\n{len(RESULTS) - nfail} passed, {nfail} failed of {len(RESULTS)} checks; {time.time() - t0:.0f} s")
    sys.exit(1 if nfail else 0)


if __name__ == "__main__":
    main()
