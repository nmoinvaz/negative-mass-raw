"""dev probe p4 (#302): the M ODE for z = dphi_N on the exact growing mode Y_N = c2 R (gauge dF_N = 0), integrated inward from s = 0.3: does z ~ zeta ln s?
prediction (M identity + EF gauge vector, two derivations): zeta = -sqrt(2) c2 / kappa = -pi c2 / sqrt(2)."""
import math, sys, os
import numpy as np
from scipy.integrate import solve_ivp
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i302/notes/black_universe"))
_a = sys.argv; sys.argv = sys.argv[:1]
import full_slice as fs
sys.argv = _a
bg = fs.bgc(-1.0); K = fs.KAPPA; EPS = fs.EPS
def aux(s):
    b = bg.at(s); rho, R = b["rho"], b["r"]
    rs = 2 * s * K * b["E"]
    gr = (1 + 2 * rho * rho) / (math.sqrt(2) * R)
    return b, rho, R, rho * R / math.sqrt(2), gr * rs, rho / R * rs
def rhs(s, y):
    b, rho, R, g, gs, Rs = aux(s)
    YN, YNs = R, Rs                      # c2 = 1
    z = y[0]
    # g z' + (g' + eps r s php + s Fp g) z = -(YN' + s Fp YN)
    zs = (-(YNs + s * b["Fp"] * YN) - (gs + EPS * b["r"] * s * b["php"] + s * b["Fp"] * g) * z) / g
    return [zs]
sol = solve_ivp(rhs, [0.3, 1e-4], [0.0], dense_output=True, method="DOP853", rtol=1e-12, atol=1e-16)
zeta = -math.pi / math.sqrt(2)
print("predicted zeta =", zeta)
for s in (0.3, 0.1, 0.03, 0.01, 3e-3, 1e-3, 3e-4, 1e-4):
    z = sol.sol(s)[0]
    # local slope d z / d ln s by centred difference
    e = 1e-3
    sl = (sol.sol(s * (1 + e))[0] - sol.sol(s * (1 - e))[0]) / (math.log(1 + e) - math.log(1 - e))
    print(f"s={s:8.1e}  z={z: .9f}  dz/dln s={sl: .9f}  ratio to zeta={sl / zeta:.9f}")
b = bg.at(1e-4); a = b["rho"] * b["r"] / math.sqrt(2) / 1e-8
print("F_Pi(0)/a * c2 =", b["Fp"] / a, " (pi/sqrt2 =", math.pi / math.sqrt(2), ")")
