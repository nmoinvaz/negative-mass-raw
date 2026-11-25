#!/usr/bin/env python3
"""ind163: the coordinator's independent check of #163 (second row of [GGS09a] Table I and the large-gamma_1 limit).

Criteria U0-U3 in negative-mass-raw I163-mac/README.md. Imports nothing from the repository: own Numerov with
Richardson extrapolation, own RK4 maps x(rho-bar) and z(rho-hat), the equations retyped from the TeX.
"""
import argparse
import math
import sys
import time

import sympy as sp

MUTS = ['zm', 'num', 'lim', 'brk']
ap = argparse.ArgumentParser()
ap.add_argument('--mutate', default='')
MUT = ap.parse_args().mutate
if MUT and MUT not in MUTS:
    sys.exit(f"unknown mutation {MUT!r}; known: {MUTS}")
FAIL = []
T0 = time.time()


def check(name, ok, msg):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {msg}  ({time.time() - T0:.0f} s)", flush=True)
    if not ok:
        FAIL.append(name)


# U0 -------------------------------------------------------------------------------------------------------------
print("== U0: the zero mode of the limit equation ==", flush=True)
z = sp.Symbol('z', positive=True)
ez = sp.exp(2 * (1 - 1 / z))
chi0 = 2 / sp.pi * (z - (2 if MUT == 'zm' else 1)) / z**2 * sp.exp(1 - 1 / z)
Wlim_s = ez**2 * (2 / z**2 - (9 if MUT == 'lim' else 10) / z**3 + 3 / z**4)
op = -ez * sp.diff(ez * sp.diff(chi0, z), z) + Wlim_s * chi0
u0 = sp.simplify(op) == 0
check('U0', u0, f"(2/pi)(z-1)/z^2 e^(1-1/z) solves the typed limit equation at beta-hat = 0: {u0}")

# solver -----------------------------------------------------------------------------------------------------------
C5 = 6.0 if MUT == 'num' else 5.0


def numerov_in(Wf, beta, h, N):
    c = h * h / 12
    b2 = beta * beta
    rN, rN1 = N * h, (N - 1) * h
    chi = [1 + 1 / (beta * rN), math.exp(beta * h) * (1 + 1 / (beta * rN1))]
    for j in range(2, len(Wf)):
        q0, q1, q2 = Wf[j - 2] + b2, Wf[j - 1] + b2, Wf[j] + b2
        chi.append((2 * (1 + C5 * c * q1) * chi[j - 1] - (1 - c * q0) * chi[j - 2]) / (1 - c * q2))
        if abs(chi[-1]) > 1e150:
            chi = [v * 1e-150 for v in chi]
    return chi


def match(beta, Wp, Wm, h):
    N = len(Wp) - 1
    cR = numerov_in(Wp[::-1], beta, h, N)
    cL = numerov_in(Wm[::-1] + [Wp[1]], beta, h, N)
    R0, R1 = cR[-1], cR[-2]
    L0, L1 = cL[-2], cL[-1]
    return (L0 * R1 - L1 * R0) / (math.hypot(L0, L1) * math.hypot(R0, R1))


def refine(fun, a, b, fa, fb, tol=1e-14):
    side = 0
    for _ in range(300):
        cc = (a * fb - b * fa) / (fb - fa)
        fc = fun(cc)
        if fc * fb < 0:
            a, fa, b, fb, side = b, fb, cc, fc, 0
        else:
            b, fb = cc, fc
            if side == -1:
                fa /= 2
            side = -1
        if abs(b - a) < tol * abs(b) or fc == 0:
            return cc
    return cc


def largest_root(Wp, Wm, h, lo, hi, n=40):
    fun = lambda bb: match(bb, Wp, Wm, h)
    bs = [lo + (hi - lo) * i / (n - 1) for i in range(n)]
    vs = [fun(b) for b in bs]
    br = [(bs[i], bs[i + 1], vs[i], vs[i + 1]) for i in range(n - 1) if vs[i] * vs[i + 1] < 0]
    if not br:
        return None
    return refine(fun, *br[-1])


def rk4_map(f, y0, L, h, sgn):
    N = int(round(L / h))
    ys, y, hh = [y0], y0, sgn * h
    for _ in range(N):
        k1 = f(y)
        k2 = f(y + hh / 2 * k1)
        k3 = f(y + hh / 2 * k2)
        k4 = f(y + hh * k3)
        y += hh / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        ys.append(y)
    return ys


def solve(Wfun, mapf, y0, L, h1, lo, hi):
    out = []
    for h in (h1, h1 / 2):
        Wp = [Wfun(v) for v in rk4_map(mapf, y0, L, h, +1)] if mapf else [Wfun(j * h) for j in range(int(round(L / h)) + 1)]
        Wm = [Wfun(v) for v in rk4_map(mapf, y0, L, h, -1)] if mapf else [Wfun(-j * h) for j in range(int(round(L / h)) + 1)]
        out.append(largest_root(Wp, Wm, h, lo, hi))
    if None in out:
        return None, None
    return (16 * out[1] - out[0]) / 15, abs(out[1] - out[0]) / 15


# U1 -------------------------------------------------------------------------------------------------------------
print("\n== U1: planted Poschl-Teller ==", flush=True)
u1, msgs = True, []
for ell in (1.3, 2.4):
    b, sp_ = solve(lambda y, e=ell: -e * (e + 1) / math.cosh(y)**2, None, 0.0, 45 / ell, 0.002, 0.2, ell + 0.45)
    ok = b is not None and abs(b / ell - 1) < 1e-9
    u1 &= ok
    msgs.append(f"ell = {ell}: beta = {b!r}, rel {abs(b / ell - 1) if b else None}")
check('U1', u1, "; ".join(msgs))

# U2 -------------------------------------------------------------------------------------------------------------
print("\n== U2: the limit equation ==", flush=True)
CL = 9.0 if MUT == 'lim' else 10.0


def Wlim(zv):
    if zv <= 0:
        return 0.0
    return math.exp(4 * (1 - 1 / zv)) * (2 / zv**2 - CL / zv**3 + 3 / zv**4)


zmap = lambda zv: math.exp(2 * (1 - 1 / zv)) if zv > 0 else 0.0
bh, sph = solve(Wlim, zmap, 1.0, 45 / 1.7, 0.002, 0.5, 2.6)
inv = 1 / bh if bh else float('nan')
u2 = bh is not None and abs(inv - 0.588351371) < 1e-8 and round(inv, 3) == 0.588 and abs(inv - 0.590) > 0.001
check('U2', u2, f"beta-hat = {bh!r}, 1/beta-hat = {inv:.12f} (h-spread in beta-hat {sph}); against 0.588351371: "
      f"{abs(inv - 0.588351371):.1e}; rounds to 0.588: {round(inv, 3) == 0.588}; |1/beta-hat - 0.590| = {abs(inv - 0.590):.6f}")

# U3 -------------------------------------------------------------------------------------------------------------
print("\n== U3: the DiffEq centred on the throat ==", flush=True)
C3 = 2.0 if MUT == 'brk' else 3.0


def bracket(xv, g):
    at = math.atan(xv)
    k = g / (1 + g * g)
    F = 1 + k * (1 + g * xv) * at
    Fx = k * ((1 + g * xv) / (1 + xv * xv) + g * at)
    r = Fx / F
    return (-3 / (1 + xv * xv) + C3 * (xv - g)**2 / (1 + xv * xv)**2 + 2 * r * r - 4 * g / (1 + xv * xv) * r
            + 4 * k * (xv - g) / (F * (1 + xv * xv)**2))


PRINTED = {2.0: (0.617891948, 0.618), 2.5: (0.608155106, 0.608), 5.0: (0.593640535, 0.594), 10.0: (0.589696827, 0.590)}
u3, msgs = True, []
for g, (Tp, Ttab) in PRINTED.items():
    ag = math.atan(g)
    afun = lambda xv, g=g, ag=ag: math.exp(2 * g * (math.atan(xv) - ag))
    Wbar = lambda xv, g=g, afun=afun: afun(xv)**2 * bracket(xv, g)
    best = 1 / (math.sqrt(1 + g * g) * Ttab)
    L = 45 / best
    bb, spb = solve(Wbar, afun, g, L, L / 20000, 0.5 * best, 1.5 * best)
    if bb is None:
        u3 = False
        msgs.append(f"gamma = {g}: no root")
        continue
    T = 1 / (math.sqrt(1 + g * g) * bb)
    ok = abs(T / Tp - 1) < 1e-8 and round(T, 3) == Ttab
    line = f"gamma = {g}: beta-bar = {bb:.12f}, T = {T:.10f}, rel to #163 {abs(T / Tp - 1):.1e}, h-spread {spb:.1e}"
    if g == 2.0:
        beta = math.exp(2 * g * ag) * bb
        r_conv = abs(beta / 60.662007295832 - 1)
        r_run = abs(beta / 60.662389104967 - 1)
        ok = ok and r_conv < 1e-8 and r_run > 1e-6
        line += f"; beta = {beta:.10f}: rel to converged {r_conv:.1e}, to #151 as-run {r_run:.1e}"
    u3 &= ok
    msgs.append(line)
check('U3', u3, "; ".join(msgs))

print(f"\nchecks failed: {FAIL}; {time.time() - T0:.0f} s; mutation: {MUT or 'none'}")
sys.exit(1 if FAIL else 0)
