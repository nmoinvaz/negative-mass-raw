"""dev_28: method A at order 5. G_5 as one integral of the closed forms of order4.py, with Y_4 removed by parts (E3):

  E1, E2 (I26-dh610): G_k = int_0^{pi/2} I_k dth,
      I_k = 8 ell h_{k-1}/S + 2 sum_{j=1}^{k-1} L_{k-1-j} l^j/j! + 2 (sum_{j<k} Y_j c_{k-j} - Omega_{k-1})/S,  ell = ln cos, S = sin^2, l = -2 ell.
  Y_{k-1} enters I_k only through (4 ell + 2 c_1) Y_{k-1}/S = 2 P' Y_{k-1}, P = cot(th) (ell - Omega0), c_1 = Omega0 - 3 ell - S, and
  int 2 P' Y dth = -2 int P Y' dth = -4 int (ell - Omega0) F_{k-2} dth   (E3: Y_j' = 2 tan(th) F_{j-1}, boundary terms 0).
  So I_5 needs Y_0 .. Y_3 and L_0 .. L_3 (all closed in order4.py), not Y_4.

    python order5-dir/dev_28_a5.py [dps] [guard]

Omega0, Omega1, Omega2 are the closed forms; Omega3 is solved from the affine G_5; the result is compared with method B (dev_09_nominal.json)."""
import json
import os
import sys
import time

sys.path.insert(0, "/home/nathan/Source/negative-mass-i208/notes/wormhole_largeD")
_a, sys.argv = sys.argv, sys.argv[:1]
import order4 as o4  # noqa: E402
sys.argv = _a
import order5 as o5  # noqa: E402
import mpmath as mp  # noqa: E402

DPS = int(sys.argv[1]) if len(sys.argv) > 1 else 30
GUARD = int(sys.argv[2]) if len(sys.argv) > 2 else 60


def L3_closed(th, Om, l, R, s2, u, lc, Y, L):
    q = mp.ln2
    Cn = mp.clsin(2, mp.pi - 2 * th)
    sc = mp.sin(th) * mp.cos(th)
    Lc2 = o4.Lc2_poly(th)
    B = -32 * (lc + q) * Cn + 16 * s2 * Cn + 32 * Lc2 + 16 * sc * lc * (lc + 2 * q) - 4 * Om[1] * th - 2 * Om[1] * sc
    return -2 * o5.hk(3, Om, l, R, Y, L) + 2 * u * B


def I5(Om):
    """integrand of G_5 (Y_4 removed by E3); Om = [w0, w1, w2, w3, 0]"""
    def f(th, x, tail):
        with mp.extradps(GUARD):
            c, lc, l, u, R, s2, Y, L, K, T = o4.closed(th, x, tail, Om)
            # L_3 needs th itself; in the tail th = pi/2 - x, which is exact at the working precision
            L3 = L3_closed(th, Om, l, R, s2, u, lc, Y, L)
            LL = [L[0], L[1], L[2], L3]
            h4 = s2 * LL[3] + sum(Y[j] * o5.cc(4 - j, Om, l, R) for j in range(4))        # Y_4/2 removed (E3)
            t1 = 8 * lc * h4 / s2
            t2 = 2 * sum(LL[3 - j] * l ** (j + 1) / mp.factorial(j + 1) for j in range(4))
            o = list(Om)
            o[4] = 0
            t3 = 2 * sum(Y[j] * o5.cc(5 - j, o, l, R) for j in range(4)) / s2
            F3 = sum(LL[3 - j] * l**j / mp.factorial(j) for j in range(4))
            t4 = -4 * (lc - Om[0]) * F3
            return t1 + t2 + t3 + t4
    return f


def G5(Om):
    f = I5(Om)
    left = mp.quad(lambda t: f(t, mp.pi / 2 - t, False), [0, mp.mpf(1) / 2, 1], method="gauss-legendre")
    right = mp.quad(lambda x: f(mp.pi / 2 - x, x, True), [0, mp.pi / 2 - 1])
    return left + right


if __name__ == "__main__":
    t0 = time.time()
    mp.mp.dps = DPS
    cl = o5.closed_omegas()
    Om = [cl[0], cl[1], cl[2], mp.mpf(0), mp.mpf(0)]
    g0 = G5(Om)
    print(f"G5(Omega3 = 0) = {mp.nstr(g0, DPS)}   ({time.time() - t0:.0f} s)", flush=True)
    Om1 = list(Om)
    Om1[3] = mp.mpf(1)
    g1 = G5(Om1)
    slope = g1 - g0
    om3 = -g0 / slope
    print(f"slope = {mp.nstr(slope, DPS)}  against -4 pi: {mp.nstr(slope + 4 * mp.pi, 5)}")
    print(f"Omega3 (A) = {mp.nstr(om3, DPS)}   ({time.time() - t0:.0f} s)")
    ref = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dev_09_nominal.json")))["B4"]
    ob = mp.mpf(ref["Om3"])
    print(f"Omega3 (B4) = {mp.nstr(ob, DPS)}   difference {mp.nstr(om3 - ob, 5)}")
