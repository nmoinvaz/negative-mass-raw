"""P3: the exact static mass mode r = sqrt(L) R, F_L = A + 1/L - 1 (exact_mode.md Sec. 3, N6) in the Kruskal chart at fixed Pi, d/dL at L = 1.
Data on the slice V + U = 0 through the same Slice/theta/dm code: Theta_gen = -c1 = -1/2 at every s, dm -> 1/pi (kappa c1 = 1/pi)."""
import os, sys, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
import numpy as np
from scipy.integrate import solve_ivp
import full_slice as fs

c = -1.0
K = -2 * c / math.pi
kap = 2 / math.pi
A1 = 2 * K
Ac = lambda r: 1 + c * (r * r + 1) + K * (r + (r * r + 1) * math.atan(r))
Ap = lambda r: 2 * c * r + 2 * K * (1 + r * math.atan(r))
App = lambda r: 2 * c + 2 * K * (math.atan(r) + r / (1 + r * r))
khat = App(0.0) / A1 ** 2            # kappa'/kappa
print("A1", A1, "khat", khat, " -pi^2/8 =", -math.pi ** 2 / 8)

bg = fs.bgc(c)
s0 = 1e-3
b0 = bg.at(s0)
rho0 = b0["rho"]
q0 = 1.0 / A1                                  # d_1 = 0 normalization; error O(Pi0^2)
y0 = 2 * math.log(s0)
y1 = 2 * math.log(3e6)


def rhs(y, u):
    rho, q = u
    A, Ap_ = Ac(rho), Ap(rho)
    return [A / (2 * kap), (Ap_ * q - 1.0 - khat * A) / (2 * kap)]


sol = solve_ivp(rhs, [y0, y1], [rho0, q0], method="DOP853", rtol=1e-13, atol=1e-18, dense_output=True)
print("ok", sol.success, sol.t[-1])


def mode(s):
    s = abs(s)
    y = 2 * math.log(s)
    rho, q = sol.sol(y)
    A, Ap_, App_ = Ac(rho), Ap(rho), App(rho)
    rho_y = A / (2 * kap)
    q_y = (Ap_ * q - 1.0 - khat * A) / (2 * kap)
    q_yy = (App_ * rho_y * q + Ap_ * q_y - khat * Ap_ * rho_y) / (2 * kap)
    rho_yy = Ap_ * rho_y / (2 * kap)
    R = math.sqrt(1 + rho * rho)
    Rp, Rpp = rho / R, 1.0 / R ** 3
    dr = R / 2 + Rp * q
    dr_y = Rp * rho_y / 2 + Rpp * rho_y * q + Rp * q_y
    dphi = math.sqrt(2) * q / R ** 2
    dF = khat - q_y / rho_y
    dF_y = -(q_yy * rho_y - q_y * rho_yy) / rho_y ** 2
    return dict(rho=rho, q=q, dr=dr, dr_s=dr_y * 2 / s, dphi=dphi, dF=dF, dF_s=dF_y * 2 / s, R=R, A=A, Ap=Ap_)


def dm_exact(s):
    m = mode(s)
    rho, R, A, Apv, q = m["rho"], m["R"], m["A"], m["Ap"], m["q"]
    dmL = 1 / (4 * R) + 3 * rho ** 2 * (1 - A) / (4 * R)
    m_rho = (2 * rho * (1 - A) - rho ** 2 * Apv) / (2 * R) - rho * (1 + rho ** 2 * (1 - A)) / (2 * R ** 3)
    return dmL + m_rho * q


sl = fs.Slice(bg)
print("s, rho, dr, dphi, dF, Theta_gen, Theta_old, dm(slice formula), dm(exact d_L m at fixed Pi)")
for s in (0.05, 0.1, 0.3, 0.7, 1.0, 2.0, 5.0, 20.0, 1e2, 1e3, 1e4, 3e4, 1e5, 1e6):
    m = mode(s)
    mu, a, cc, Q, b = sl.theta_coef(s)
    th_old = a * m["dr"] + mu * m["dr_s"] + cc * m["dphi"]
    th = th_old + mu * s * b["rp"] * m["dF"]
    dm1 = fs.dm_of(bg, s, m["dr"], m["dr_s"], m["dF"])
    dm2 = dm_exact(s)
    print(f"{s:9.3g} {m['rho']:8.4f} {m['dr']: .6e} {m['dphi']: .3e} {m['dF']: .6e} {th: .10e} {th_old: .3e} {dm1: .10e} {dm2: .10e} (diff {dm1-dm2: .1e})")
print("target: Theta = -1/2, dm -> 1/pi =", 1 / math.pi, " kappa c1 =", kap * 0.5)
