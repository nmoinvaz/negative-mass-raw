"""P9: the first law dM = (kappa_xi / 8 pi) dA on the exact static family r = sqrt(L) R, F_L = A + 1/L - 1, at finite L.
M(L) = 2 L^{3/2}/(3 pi); horizon rho_h: A(rho_h) = 1 - 1/L; area 4 pi L R(rho_h)^2; xi = sqrt(L) d_t is unit at infinity (F -> 1/L): kappa_xi = sqrt(L) A'(rho_h)/2."""
import mpmath as mp
mp.mp.dps = 40
c, K = mp.mpf(-1), 2 / mp.pi
A = lambda r: 1 + c * (r * r + 1) + K * (r + (r * r + 1) * mp.atan(r))
Ap = lambda r: 2 * c * r + 2 * K * (1 + r * mp.atan(r))
def rh(L):
    return mp.findroot(lambda r: A(r) - (1 - 1 / L), mp.mpf(1) / 10 * (L - 1) * 1.2 if L != 1 else mp.mpf(0))
def area(L):
    r = rh(L)
    return 4 * mp.pi * L * (1 + r * r)
def kap(L):
    return mp.sqrt(L) * Ap(rh(L)) / 2
M = lambda L: 2 * L ** mp.mpf(1.5) / (3 * mp.pi)
for L in (mp.mpf("0.5"), mp.mpf("0.9"), mp.mpf(1), mp.mpf("1.5"), mp.mpf(2), mp.mpf(4)):
    dM = mp.diff(M, L)
    dA = mp.diff(area, L)
    print(f"L={float(L):5.2f} rho_h={float(rh(L)): .6f} kappa_xi={float(kap(L)): .8f} dM/dL={float(dM): .12f} kappa dA/dL/(8 pi) = {float(kap(L) * dA / (8 * mp.pi)): .12f}  ratio {float(kap(L) * dA / (8 * mp.pi) / dM): .12f}")
