import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
from scipy.integrate import quad
import remainder as rm
sc = rm.hb.sc
K = 2/math.pi
def A(r): return sc.A_(r)
def Hf(r):  # H = int_0^r (K/A - 1/(2s)) ds
    f = lambda s: (K/A(s) - 0.5/s) if abs(s) > 1e-6 else (0.0)  # limit: K/A - 1/(2s) -> finite
    return quad(f, 0, r, epsabs=1e-14, epsrel=1e-13, limit=200)[0]
def integrand(r):
    R2 = 1 + r*r
    if abs(r) < 1e-9: return 1.0
    return 2*K*r*math.exp(-2*Hf(r))/(A(r)*R2)
# limit of K/A - 1/(2s) at 0: A = 2K s + A''/2 s^2 -> K/A = 1/(2s) (1 - A''/(4K) s)  => -A''/(8K)... compute by series numerically
def Hf2(r):
    def f(s):
        if abs(s) < 1e-4:
            # series: A ~ 2K s + a2 s^2, a2 = A''(0)/2 = -1 -> K/A - 1/(2s) = (1/(2s))(1/(1 + a2 s/(2K)) - 1) ~ -a2/(4K)
            a2 = -1.0
            return -a2/(4*K)
        return K/A(s) - 0.5/s
    return quad(f, 0, r, epsabs=1e-14, epsrel=1e-13, limit=200)[0]
def integrand2(r):
    R2 = 1 + r*r
    if abs(r) < 1e-8: return 1.0
    return 2*K*r*math.exp(-2*Hf2(r))/(A(r)*R2)
I0 = quad(integrand2, 0, 60, epsabs=1e-13, epsrel=1e-13, limit=400)[0] + quad(integrand2, 60, 400, epsabs=1e-14)[0]
print("I0", I0, "(#262: 1.0149036099284089)")
for Pi in (-0.2, -0.1, -0.05, 0.05, 0.12, 0.5, 1.0, 2.0, 10.0):
    rho, R = rm.rho_of_Pi(Pi)
    J = quad(integrand2, 0, rho, epsabs=1e-13, epsrel=1e-13, limit=200)[0]
    print(f"Pi={Pi:6.2f} rho={rho: .5f}  J={J: .6f}  Q_pred=-J/I0={-J/I0: .6f}")
