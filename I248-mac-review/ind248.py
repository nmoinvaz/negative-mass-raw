#!/usr/bin/env python3
"""ind248: c2 of #248's class L by transport along the data ray V = -0.05 (criteria in README.md beside this file).

No 2D solver: the transverse derivatives P = (dr_V, dF_V, dphi_V) obey, along the ray, the linearized evolution equations
r_VU, F_VU, phi_VU (the forms of I217-mac-review/ind217.py, verified there against a brute-force Ricci tensor), and
c2 = dr_V at the horizon crossing U = 0. Background of the c = -1 member in the Kruskal chart, at 30 digits.

    python3 ind248.py [--mutate=eps-sign|no-pot|pulse-centre]
"""
import argparse
import sys
import time

import mpmath as mp
import sympy as sp

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["eps-sign", "no-pot", "pulse-centre"])
OPT = ap.parse_args()
MUT = OPT.mutate
mp.mp.dps = 30
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


C = mp.mpf(-1)
K = -2 * C / mp.pi
KAP = 2 / mp.pi                     # A'(0) / 2 at c = -1
VL, U0 = mp.mpf("-0.05"), mp.mpf(-2)
EPS = 1 if MUT == "eps-sign" else -1
C2_NOTE = mp.mpf("-9.610862e-04")


def A(x):
    return 1 + C * (x * x + 1) + K * (x + (x * x + 1) * mp.atan(x))


def Ap(x):
    return 2 * C * x + K * (2 + 2 * x * mp.atan(x))


def App(x):
    return 2 * C + K * (2 * mp.atan(x) + 2 * x / (1 + x * x))


def Appp(x):
    return K * (2 / (1 + x * x) + (2 * (1 + x * x) - 4 * x * x) / (1 + x * x) ** 2)


A1, A2, A3 = Ap(0), App(0) / 2, Appp(0) / 6
TINY = mp.mpf("1e-24")


def h_fun(x):                       # 1/A - 1/(2 kappa x), regular at 0
    if abs(x) < TINY:
        return -A2 / A1 ** 2
    return 1 / A(x) - 1 / (2 * KAP * x)


def AoverX(x):
    return A1 if abs(x) < TINY else A(x) / x


def dlnG(x):                        # d ln G / d rho = (A' - 2 kappa) / A
    if abs(x) < TINY:
        return 2 * A2 / A1
    return (Ap(x) - 2 * KAP) / A(x)


def ddlnG(x):                       # its derivative
    if abs(x) < TINY:
        return (6 * A3 * A1 - 4 * A2 ** 2) / A1 ** 2 / 2   # series of (A' - A1)/A: 2A2/A1 + (3A3/A1 - 2A2^2/A1^2) x
    return App(x) / A(x) - (Ap(x) - 2 * KAP) * Ap(x) / A(x) ** 2


def I_of(x):                        # 2 kappa int_1^x h
    pts = [mp.mpf(1), mp.mpf(0), x] if x < 0 else [mp.mpf(1), x]
    return 2 * KAP * mp.quad(h_fun, pts)


def bg(x, I, U):
    """Background jets at (V_L, U) from rho = x and I."""
    G = AoverX(x) * mp.e ** (-I) / (2 * KAP)
    rV, rU = -U * G, -VL * G                        # rho_V, rho_U
    R = mp.sqrt(1 + x * x)
    Rp, Rpp = x / R, 1 / R ** 3
    Pp, Ppp = mp.sqrt(2) / (1 + x * x), -2 * mp.sqrt(2) * x / (1 + x * x) ** 2
    dl, ddl = dlnG(x), ddlnG(x)
    Gp = G * dl
    rhoUV = -G - VL * Gp * rV
    rhoUU = -VL * Gp * rU
    FU = -dl * rU
    return dict(G=G, R=R, F=mp.log(KAP) - mp.log(G), phi=mp.sqrt(2) * mp.atan(x),
                r_V=Rp * rV, r_U=Rp * rU, p_V=Pp * rV, p_U=Pp * rU, F_U=FU,
                r_UV=Rpp * rV * rU + Rp * rhoUV, p_UV=Ppp * rV * rU + Pp * rhoUV, F_UV=-(ddl * rV * rU + dl * rhoUV),
                r_UU=Rpp * rU * rU + Rp * rhoUU, p_UU=Ppp * rU * rU + Pp * rhoUU, rho_U=rU)


# the evolution equations (ind217's printed forms, n = 2) and their gradients
r_, F_, p_, rV_, rU_, pV_, pU_ = sp.symbols("r F p rV rU pV pU")
psi = p_ / sp.sqrt(2)
cc, KK = sp.Integer(-1), 2 / sp.pi
Vpot = -cc * (3 - 2 * sp.cos(psi) ** 2) - KK * (3 * sp.sin(psi) * sp.cos(psi) + psi * (3 - 2 * sp.cos(psi) ** 2))
if MUT == "no-pot":
    Vpot = sp.Integer(0)
Vp1 = sp.diff(Vpot, p_)
emF = sp.exp(-F_)
pr_r = -(rV_ * rU_ + emF / 2) / r_ + sp.Rational(1, 2) * Vpot * r_ * emF
pr_F = (2 / r_) * pr_r + EPS * pV_ * pU_ - Vpot * emF
pr_p = -(rV_ * pU_ + rU_ * pV_) / r_ - sp.Rational(EPS, 2) * emF * Vp1
ARGS = (r_, F_, p_, rV_, rU_, pV_, pU_)
GRAD = [sp.lambdify(ARGS, [sp.diff(e, a) for a in ARGS], "mpmath") for e in (pr_r, pr_F, pr_p)]


def zeta(U):
    return mp.mpf("1e-3") * (1 + mp.tanh((U + 1) / mp.mpf("0.2"))) / 2


def zetap(U):
    return mp.mpf("1e-3") / (2 * mp.mpf("0.2")) / mp.cosh((U + 1) / mp.mpf("0.2")) ** 2


S0 = mp.mpf("0.01") if MUT == "pulse-centre" else mp.mpf(0)
AMP, W = mp.mpf("1e-3"), mp.mpf("0.3")


def pulse(U):
    return AMP * mp.e ** (-((U - S0) / W) ** 2) - AMP * mp.e ** (-((U0 - S0) / W) ** 2)


def pulsep(U):
    return AMP * (-2 * (U - S0) / W ** 2) * mp.e ** (-((U - S0) / W) ** 2)


def rhs(U, y, mode):
    x, I, dr, drU, Pr, PF, Pp = y
    b = bg(x, I, U)
    dxdU = b["rho_U"]
    dI = 2 * KAP * h_fun(x) * dxdU
    if mode == "L":
        dF, dp, dpU = mp.mpf(0), pulse(U), pulsep(U)
        ddr = drU
        # constraint: dr'' = -eps r phi' dphi' - F' dr' - (eps/2) phi'^2 dr; at eps = -1: r phi' dphi' - F' dr' + phi'^2 dr / 2
        ddrU = -EPS * b["R"] * b["p_U"] * dpU - b["F_U"] * drU - EPS * mp.mpf(0.5) * b["p_U"] ** 2 * dr
        drU_now = drU
    else:                                           # pure gauge, exact data
        z, zp = zeta(U), zetap(U)
        dr, drU_now = z * b["r_U"], zp * b["r_U"] + z * b["r_UU"]
        dp, dpU = z * b["p_U"], zp * b["p_U"] + z * b["p_UU"]
        dF = b["F_U"] * z - zp
        ddr, ddrU = mp.mpf(0), mp.mpf(0)
    vals = (b["R"], b["F"], b["phi"], b["r_V"], b["r_U"], b["p_V"], b["p_U"])
    pert = (dr, dF, dp, Pr, drU_now, Pp, dpU)
    dP = [mp.fsum(g * d for g, d in zip(GR(*vals), pert)) for GR in GRAD]
    return [dxdU, dI, ddr, ddrU, dP[0], dP[1], dP[2]]


def rk4(mode, n, record=False):
    Pi0 = -VL * U0
    x0 = mp.findroot(lambda x: x * mp.e ** I_of(x) - Pi0, mp.mpf("-0.05"))
    I0 = I_of(x0)
    if mode == "L":
        y = [x0, I0, mp.mpf(0), mp.mpf(0), mp.mpf(0), mp.mpf(0), mp.mpf(0)]
    else:
        b = bg(x0, I0, U0)
        z = zeta(U0)
        y = [x0, I0, mp.mpf(0), mp.mpf(0), z * b["r_UV"], z * b["F_UV"], z * b["p_UV"]]
    hh = -U0 / n
    U = U0
    worst = mp.mpf(0)
    scale = mp.mpf(0)
    pidev = mp.mpf(0)
    for k in range(n):
        k1 = rhs(U, y, mode)
        k2 = rhs(U + hh / 2, [a + hh / 2 * b_ for a, b_ in zip(y, k1)], mode)
        k3 = rhs(U + hh / 2, [a + hh / 2 * b_ for a, b_ in zip(y, k2)], mode)
        k4 = rhs(U + hh, [a + hh * b_ for a, b_ in zip(y, k3)], mode)
        y = [a + hh / 6 * (p + 2 * q + 2 * r + s) for a, p, q, r, s in zip(y, k1, k2, k3, k4)]
        U = U0 + (k + 1) * hh
        pidev = max(pidev, abs(y[0] * mp.e ** y[1] - (-VL * U)))
        if mode == "G" and k < n - 1:
            b = bg(y[0], y[1], U)
            z = zeta(U)
            ex = (z * b["r_UV"], z * b["F_UV"], z * b["p_UV"])
            worst = max(worst, *[abs(a - e) for a, e in zip(y[4:], ex)])
            scale = max(scale, *[abs(e) for e in ex])
    return y, worst, scale, pidev


t0 = time.time()
yA, _, _, pd1 = rk4("L", 4000)
yB, _, _, pd2 = rk4("L", 8000)
c2a, c2b = yA[4], yB[4]
print(f"  class L: c2 = {mp.nstr(c2a, 15)} (4000 steps), {mp.nstr(c2b, 15)} (8000); rho at U = 0: {mp.nstr(yB[0], 3)}; "
      f"max |rho e^I - Pi| {mp.nstr(pd2, 3)}; {time.time() - t0:.0f} s", flush=True)
rel0 = abs(c2a / c2b - 1)
check("K0", rel0 <= mp.mpf("1e-10"), f"relative difference of c2 at 4000 and 8000 steps {mp.nstr(rel0, 3)}; bar 1e-10")
rel1 = abs(c2b / C2_NOTE - 1)
check("K1", rel1 <= mp.mpf("1e-6"), f"c2 = {mp.nstr(c2b, 12)} against the note's {mp.nstr(C2_NOTE, 7)}: relative {mp.nstr(rel1, 3)}; bar 1e-6")
yG, worst, scale, _ = rk4("G", 4000)
relg = worst / scale
check("K2", relg <= mp.mpf("1e-8") and abs(yG[4]) <= mp.mpf("1e-12"),
      f"pure gauge: max |P - exact| / max |exact| = {mp.nstr(relg, 3)} (scale {mp.nstr(scale, 3)}); c2 = {mp.nstr(yG[4], 3)}; bars 1e-8, 1e-12")
bad = [nm for nm, o in RESULTS if not o]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}; {time.time() - t0:.0f} s", flush=True)
sys.exit(1 if bad else 0)
