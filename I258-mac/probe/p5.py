# probe 5: compact slice datum, diagonal march, horizon fit vs slice functional
import sys, math, time, numpy as np, numba as nb
sys.argv = [sys.argv[0]]
from p3 import *   # background, ODE helpers, bumps, AB, C, centers
import horizon_sector as hs
import linear as lin

# ---- corrected coefficients: even data a (5), odd data b (5)
w_e = AB[0, :] / AB[0, 0] * 0 + AB[0, :]            # row of A values; condition A_end = 0  (rank 1 so B_end = 0 too)
a0 = np.array([0.0, 0.5, 1.0, 0.2, 0.0]) * 1e-3     # seed coefficients (delta phi), a mix not symmetric in s
b0 = np.array([0.0, 0.0, 1.0, 0.6, 0.0]) * 1e-3     # seed coefficients (delta phi_N)
a = a0 - (w_e @ a0) / (w_e @ w_e) * w_e
b = b0 - (C @ b0) / (C @ C) * C
print("a", a, "b", b, " residual end (A,B):", AB @ a, " C:", C @ b)

def dphi(s):  return sum(ai * mk(c, wid)[0](s) for ai, c in zip(a, centers))
def dphiT(s): return sum(ai * mk(c, wid)[1](s) for ai, c in zip(a, centers))
def dphiN(s): return sum(bi * mk(c, wid)[0](s) for bi, c in zip(b, centers))
def dphiNT(s): return sum(bi * mk(c, wid)[1](s) for bi, c in zip(b, centers))
def ddphiT(s, e=1e-5): return (dphiT(s+e) - dphiT(s-e)) / (2*e)    # probe only

solE = solve_even(dphi, dphiT)
solO = solve_odd(dphiN)
print("end values  dr, dr', n at SR:", solE.y[:, -1], solO.y[:, -1])
c2_slice = 0.5 * (solE.sol(0.0)[1] + solO.sol(0.0)[0])
print("c1 = dr(0) =", solE.sol(0.0)[0], " c2_slice =", c2_slice, " (dr'(0) =", solE.sol(0.0)[1], " n(0) =", solO.sol(0.0)[0], ")")

@nb.njit(cache=True)
def march_diag(L0, L1, J, h, par, tab):
    """L0[q, j] at node (j, -j), j=0..J ; L1[q, j] at node (j, 1-j), j=1..J (L1[:,0] unused). Returns horizon values H[q, j] at (j, 0), j=0..J."""
    Ua = np.zeros((3, J + 1, J + 2))        # Ua[q, j, i + J]  (i from -J..1)
    for q in range(3):
        for j in range(J + 1):
            Ua[q, j, -j + J] = L0[q, j]
        for j in range(1, J + 1):
            Ua[q, j, 1 - j + J] = L1[q, j]
    B0 = np.zeros((3, 3)); Bp = np.zeros((3, 3)); Bm = np.zeros((3, 3)); M = np.zeros((3, 3))
    rhs = np.zeros(3); out = np.zeros(3); Sv = np.zeros(3); Ev = np.zeros(3); Wv = np.zeros(3)
    for l in range(2, J + 1):
        guess = 0.0
        for j in range(l, J + 1):
            i = l - j
            for q in range(3):
                Sv[q] = Ua[q, j - 1, i - 1 + J]
                Ev[q] = Ua[q, j, i - 1 + J]
                Wv[q] = Ua[q, j - 1, i + J]
            guess = hs._cellK(Sv, Ev, Wv, (j - 1) * h, (i - 1) * h, h, h, par, tab, guess, B0, Bp, Bm, M, rhs, out)
            for q in range(3):
                Ua[q, j, i + J] = out[q]
    H = np.zeros((3, J + 1))
    for j in range(J + 1):
        for q in range(3):
            H[q, j] = Ua[q, j, 0 + J]
    return H

def layers(h, J, sol_even, sol_odd, dphi, dphiT, dphiN, ddphiT, dphiNT):
    """L0 at s = j h, L1 at the midpoint offsets (h/2)(1,1) from s = (j - 1/2) h; U = (dr, dF, dphi)."""
    B0 = np.zeros((3, 3)); Bp = np.zeros((3, 3)); Bm = np.zeros((3, 3))
    L0 = np.zeros((3, J + 1)); L1 = np.zeros((3, J + 1))
    for j in range(J + 1):
        s = j * h
        L0[0, j] = sol_even.sol(s)[0]; L0[2, j] = dphi(s)
    for j in range(1, J + 1):
        s = (j - 0.5) * h
        dr, drT = sol_even.sol(s); n = sol_odd.sol(s)[0]
        P, Q, b = coeffs(s)
        S = -(b['E'] * b['V1'] * b['r'] * dphi(s) + eps * b['r'] * s * b['php'] * dphiT(s))
        drTT = S - P * drT - Q * dr
        # n' = -s F' n - eps r s phi' dphiN
        drTN = -s * b['Fp'] * n - eps * b['r'] * s * b['php'] * dphiN(s)
        U = np.array([dr, 0.0, dphi(s)])
        UT = np.array([drT, 0.0, dphiT(s)]); UN = np.array([n, 0.0, dphiN(s)])
        UTT = np.array([drTT, 0.0, ddphiT(s)])
        hs.coefK(s, -s, kc.par, kc.tab, 0.0, B0, Bp, Bm)
        UV = 0.5 * (UT + UN); UU = 0.5 * (UN - UT)
        UNN = UTT + 4.0 * (B0 @ U + Bp @ UV + Bm @ UU)
        L1[:, j] = U + 0.5 * h * UN + h * h / 8.0 * UNN
    return L0, L1

for h in (0.02, 0.01, 0.005):
    J = int(round(3.0 / h))
    t0 = time.time()
    L0, L1 = layers(h, J, solE, solO, dphi, dphiT, dphiN, ddphiT, dphiNT)
    t1 = time.time()
    H = march_diag(L0, L1, J, h, kc.par, kc.tab)
    t2 = time.time()
    V = h * np.arange(J + 1)
    c1f, c2f, res = hs.horizon_fit(H[0], V)
    print(f"h={h}: layers {t1-t0:.1f}s march {t2-t1:.1f}s  c1_fit={c1f:.6e} c2_fit={c2f:.9e}  lin.resid={res:.2e}  c2_slice-c2_fit={c2_slice-c2f:.3e}")
