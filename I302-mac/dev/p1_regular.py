#!/usr/bin/env python3
"""dev probe p1 (#302): regular-at-S inverse data of the growing mode Y = c2 V R on the slice V + U = 0, by Chebyshev collocation in w = s^2.
Unknowns: dphi = s f(w) (odd), z = dphi_N = h(w) (even).  H: dr'' + P dr' + Q dr = -[E V1 r dphi + eps r s php dphi'],  M: n' + s Fp n = -eps r s php z (dF = dF_N = 0).
dr = Y + g dphi, n = Y_N + g z, g = rho R/sqrt2, Y = c2 s R, Y_N = c2 R."""
import math, sys, os
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i302/notes/black_universe"))
_a = sys.argv; sys.argv = sys.argv[:1]
import full_slice as fs
sys.argv = _a
from numpy.polynomial import chebyshev as C

N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
S1 = float(sys.argv[2]) if len(sys.argv) > 2 else 1.6
bg = fs.bgc(-1.0)
sl = fs.Slice(bg)
KAPPA = fs.KAPPA
EPS = fs.EPS
W1 = S1 * S1
# Chebyshev-Lobatto nodes on [0, W1]
xn = np.cos(np.pi * np.arange(N + 1) / N)[::-1]         # -1 .. 1
wn = 0.5 * W1 * (xn + 1.0)
sn = np.sqrt(wn)

def basis(x, deriv=0):
    out = []
    for k in range(N + 1):
        c = np.zeros(N + 1); c[k] = 1.0
        cd = C.chebder(c, deriv) if deriv else c
        out.append(C.chebval(x, cd) * (2.0 / W1) ** deriv)
    return np.array(out).T          # (len x, N+1): d^deriv/dw^deriv of T_k

def aux(s):
    b = bg.at(s)
    rho, R = b["rho"], b["r"]
    rs = 2 * s * KAPPA * b["E"]
    rss = 2 * KAPPA * b["E"] * (1 - 2 * s * s * b["Fp"])
    gr = (1 + 2 * rho * rho) / (math.sqrt(2) * R)
    grr = rho * (3 + 2 * rho * rho) / (math.sqrt(2) * R ** 3)
    g, gs, gss = rho * R / math.sqrt(2), gr * rs, grr * rs * rs + gr * rss
    Rs = rho / R * rs
    Rss = rs * rs / R ** 3 + rho / R * rss
    return dict(b=b, g=g, gs=gs, gss=gss, R=R, Rs=Rs, Rss=Rss, rho=rho)

def build(mode="grow", c2=1.0):
    """linear system for (f coeffs, h coeffs) at the nodes; mode 'grow': Y = c2 s R, Y_N = c2 R; 'dec': Y = -c2 s R, Y_N = c2 R."""
    B0, B1, B2 = basis(xn, 0), basis(xn, 1), basis(xn, 2)
    A = np.zeros((2 * (N + 1), 2 * (N + 1)))
    rhs = np.zeros(2 * (N + 1))
    sg = -1.0 if mode == "dec" else 1.0
    for j, s in enumerate(sn):
        a = aux(max(s, 0.0)); b = a["b"]
        P, Q, _ = sl.PQ(max(s, 1e-12))
        g, gs, gss = a["g"], a["gs"], a["gss"]
        R, Rs, Rss = a["R"], a["Rs"], a["Rss"]
        Y, Ys, Yss = sg * c2 * s * R, sg * c2 * (R + s * Rs), sg * c2 * (2 * Rs + s * Rss)
        YN, YNs = c2 * R, c2 * Rs
        # dphi = s f(w): dphi = s f, dphi' = f + 2 s^2 f_w, dphi'' = 6 s f_w + 4 s^3 f_ww
        d0 = s * B0[j]; d1 = B0[j] + 2 * s * s * B1[j]; d2 = 6 * s * B1[j] + 4 * s ** 3 * B2[j]
        # dr = Y + g dphi
        dr0 = g * d0; dr1 = gs * d0 + g * d1; dr2 = gss * d0 + 2 * gs * d1 + g * d2
        src = b["E"] * b["V1"] * b["r"] * d0 + EPS * b["r"] * s * b["php"] * d1
        A[j, :N + 1] = dr2 + P * dr1 + Q * dr0 + src
        rhs[j] = -(Yss + P * Ys + Q * Y)
        # M: n = YN + g z, z = h(w): z' = 2 s h_w
        z0 = B0[j]; z1 = 2 * s * B1[j]
        n0 = g * z0; n1 = gs * z0 + g * z1
        A[N + 1 + j, N + 1:] = n1 + s * b["Fp"] * n0 + EPS * b["r"] * s * b["php"] * z0
        rhs[N + 1 + j] = -(YNs + s * b["Fp"] * YN)
    return A, rhs, (B0, B1, B2)

if __name__ == "__main__":
    for mode in ("grow",):
        A, rhs, Bs = build(mode)
        sol, res, rank, sv = np.linalg.lstsq(A, rhs, rcond=None)
        f, h = sol[:N + 1], sol[N + 1:]
        r = A @ sol - rhs
        print(mode, "N", N, "rank", rank, "of", A.shape[0], "sv min/max", sv[-1] / sv[0], "resid max", np.max(np.abs(r)))
        B0 = Bs[0]
        for s0 in (0.0, 0.1, 0.3, 0.8, 1.6):
            x = 2 * s0 * s0 / W1 - 1
            fv = C.chebval(x, f); hv = C.chebval(x, h)
            print(f"  s = {s0}: dphi = {s0 * fv:.12e}, dphi/s = {fv:.12e}  z = {hv:.12e}")
