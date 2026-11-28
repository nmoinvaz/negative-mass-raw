"""P6: x-form (rho-form) of H at delta phi = delta F = 0: dr_xx + p dr_x + q dr = 0, p = -A'/2 + A rho/R^2, q = -(A/2)(A'' + rho A'/R^2);
first integral Theta = (R/kappa)(dr_x - A' dr/2); dm = c_b dr - kappa Theta rho/R, c_b = (1 - A rho^2/R^2)/2 - rho A'/2. Against the s-form of full_slice.py."""
import os, sys, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
import numpy as np
from scipy.integrate import solve_ivp
import full_slice as fs

c = -1.0
K = -2 * c / math.pi
kap = 2 / math.pi
Ac = lambda r: 1 + c * (r * r + 1) + K * (r + (r * r + 1) * math.atan(r))
Ap = lambda r: 2 * c * r + 2 * K * (1 + r * math.atan(r))
App = lambda r: 2 * c + 2 * K * (math.atan(r) + r / (1 + r * r))
bg = fs.bgc(c)
sl = fs.Slice(bg)

print("(a) coefficients: s-form P,Q against x-form p,q")
for s in (0.1, 0.5, 1.0, 2.0, 5.0, 30.0, 1e3, 1e5):
    P, Q, b = sl.PQ(s)
    rho = b["rho"]
    R = math.sqrt(1 + rho * rho)
    p_x = kap * s * P - kap
    q_x = kap ** 2 * s * s * Q
    p_c = -Ap(rho) / 2 + Ac(rho) * rho / R ** 2
    q_c = -(Ac(rho) / 2) * (App(rho) + rho * Ap(rho) / R ** 2)
    print(f"  s={s:8.3g} rho={rho:8.4f}  p: {p_x: .10e} vs {p_c: .10e} (rel {(p_x-p_c)/abs(p_c): .1e})   q: {q_x: .10e} vs {q_c: .10e} (rel {(q_x-q_c)/abs(q_c): .1e})")

print("(b) Theta: s-form vs x-form on the homogeneous solution h(1.0, 0) from SL")
h = sl.hom_even(fs.SL, fs.SFAR, (1.0, 0.0))
for s in (1.05, 3.0, 30.0, 1e3, 1e4, 3e4):
    dr, drs = h.sol(s)
    b = bg.at(s)
    rho = b["rho"]
    R = math.sqrt(1 + rho * rho)
    dr_x = kap * s * drs
    th_x = (R / kap) * (dr_x - Ap(rho) * dr / 2)
    th_s = sl.theta(s, dr, drs)
    dm_s = fs.dm_of(bg, s, dr, drs)
    cb = 0.5 * (1 - Ac(rho) * rho ** 2 / R ** 2) - rho * Ap(rho) / 2
    dm_x = cb * dr - kap * th_x * rho / R
    print(f"  s={s:8.3g} rho={rho:8.4f} Theta s-form {th_s: .10e} x-form {th_x: .10e} (rel {(th_x-th_s)/abs(th_s): .1e});  dm s-form {dm_s: .10e} x-form {dm_x: .10e};  -kappa Theta = {-kap*th_s: .10e}")

print("(c) tail in rho to 1e8: ODE in u = ln rho from rho(s=1.05); dm(rho) and -kappa Theta")
s0 = 1.05
dr0, drs0 = h.sol(s0)
b0 = bg.at(s0)
rho0 = b0["rho"]
dr_x0 = kap * s0 * drs0


def rhs(u, y):
    rho = math.exp(u)
    R = math.sqrt(1 + rho * rho)
    A, A1, A2 = Ac(rho), Ap(rho), App(rho)
    # dr_xx + p dr_x + q dr = 0 with d/dx = A d/drho; y = (dr, dr_x); d dr/drho = dr_x / A ; d(dr_x)/drho = dr_xx / A
    p = -A1 / 2 + A * rho / R ** 2
    q = -(A / 2) * (A2 + rho * A1 / R ** 2)
    return [rho * y[1] / A, rho * (-p * y[1] - q * y[0]) / A]


sol = solve_ivp(rhs, [math.log(rho0), math.log(1e8)], [dr0, dr_x0], method="DOP853", rtol=1e-13, atol=1e-18, dense_output=True)
print("   ok", sol.success)
th0 = (math.sqrt(1 + rho0 ** 2) / kap) * (dr_x0 - Ap(rho0) * dr0 / 2)
for rho in (rho0, 16.0, 1e2, 1e3, 1e4, 1e6, 1e8):
    dr, dr_x = sol.sol(math.log(rho))
    R = math.sqrt(1 + rho * rho)
    th = (R / kap) * (dr_x - Ap(rho) * dr / 2)
    cb = 0.5 * (1 - Ac(rho) * rho ** 2 / R ** 2) - rho * Ap(rho) / 2
    dm = cb * dr - kap * th * rho / R
    print(f"   rho={rho:9.3e} dr={dr: .8e} dr_x={dr_x: .8e} Theta={th: .12e} (vs start {th0: .12e}, rel {(th-th0)/abs(th0): .1e})  dm={dm: .10e}  -kappa Theta0 = {-kap*th0: .10e}  c_b={cb: .2e}")
