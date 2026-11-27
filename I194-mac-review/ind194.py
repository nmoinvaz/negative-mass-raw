#!/usr/bin/env python3
"""ind194: the boson stars of #194 by the coordinator's own shooting code (criteria in README.md beside this file).

    python3 ind194.py [--mutate=eps-law|lam|alpha-norm] [--only=K0,K1,K2,K3] [--tols=1e-12,1e-13] [--scan]

Shared with the crate: the field equations of phase2/boson_star.py's docstring and the stored tables (starting guesses only).
"""
import argparse
import math
import os
import sys
import time

import numba as nb
import numpy as np
from scipy.integrate import ode
from scipy.optimize import brentq

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["eps-law", "lam", "alpha-norm"])
ap.add_argument("--only", default="K0,K1")   # A1: K2, K3 not computed
ap.add_argument("--tols", default="1e-10,1e-11")   # A1
ap.add_argument("--scan", action="store_true", help="development: alpha_c along the phantom family against P = phi_c^2")
OPT = ap.parse_args()
MUT = OPT.mutate
ONLY = OPT.only.split(",")
TOLS = [float(x) for x in OPT.tols.split(",")]

LAM = 10240.0 * (1.0001 if MUT == "lam" else 1.0)
MU = 10240.0 ** 2 / 4.8
FOURPI = 4.0 * math.pi
R0, RMAX = 1e-4, 600.0

RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def V(s):
    return 0.5 * s - 0.25 * LAM * s * s + MU * s ** 3 / 6.0


def dV2(s):                       # 2 dV/ds
    return 1.0 - LAM * s + MU * s * s


@nb.njit(cache=False)
def rhs_nb(r, y, wt, eps, lam, mu):
    """The field equations of phase2/boson_star.py's docstring in (phi, phi', m, ln alpha) plus the charge integrand."""
    phi, pi_, m, L = y[0], y[1], y[2], y[3]
    a2 = 1.0 / (1.0 - 2.0 * m / r)
    ia2 = math.exp(-2.0 * L)
    s = phi * phi
    Vs = 0.5 * s - 0.25 * lam * s * s + mu * s ** 3 / 6.0
    kin = 0.5 * (wt * wt * s * ia2 + pi_ * pi_ / a2)
    rho, p = kin + Vs, kin - Vs
    fp = 4.0 * math.pi
    out = np.empty(5)
    out[0] = pi_
    dL = (a2 - 1.0) / (2 * r) + fp * r * a2 * eps * p
    dla = (1.0 - a2) / (2 * r) + fp * r * a2 * eps * rho
    out[1] = -(2.0 / r + dL - dla) * pi_ + a2 * ((1.0 - lam * s + mu * s * s) - wt * wt * ia2) * phi
    out[2] = fp * r * r * eps * rho
    out[3] = dL
    out[4] = fp * r * r * wt * s * math.sqrt(a2) * math.exp(-L)
    return out


def shoot(P, wt, eps, rtol, want_star=False):
    """One shot from the centre with alpha(0) = 1 at code frequency wt. y = (phi, phi', m, ln alpha, N).
    Returns the fate (+1 crosses zero, -1 turns up, 0 neither by RMAX) and, if want_star, the quantities at the
    turning point of a shot that turns up."""
    phic = math.sqrt(P)
    c = dV2(P) - wt * wt
    rhoc = 0.5 * wt * wt * P + V(P)
    pc = 0.5 * wt * wt * P - V(P)
    y0 = [phic * (1 + c * R0 * R0 / 6), phic * c * R0 / 3, FOURPI / 3 * eps * rhoc * R0 ** 3,
          2 * math.pi * eps * R0 * R0 * (rhoc / 3 + pc), FOURPI / 3 * wt * P * R0 ** 3]

    f = lambda r, y: rhs_nb(r, y, wt, float(eps), LAM, MU)  # noqa: E731

    state = {"fate": 0, "y": None, "r": None}

    def solout(r, y):
        if y[0] < 0:
            state["fate"] = 1
            return -1
        if y[1] > 0:
            state["fate"] = -1
            state["y"], state["r"] = list(y), r
            return -1
        return 0
    sol = ode(f).set_integrator("dop853", rtol=rtol, atol=1e-30, nsteps=10 ** 7)
    sol.set_solout(solout)
    sol.set_initial_value(y0, R0)
    sol.integrate(RMAX)
    if not want_star:
        return state["fate"], None
    if state["fate"] != -1:
        return state["fate"], None
    phi, pi_, m, L, N = state["y"]
    r = state["r"]
    ainf = math.exp(L) if MUT == "alpha-norm" else math.exp(L) / math.sqrt(1.0 - 2.0 * m / r)
    return -1, dict(P=P, wt=wt, M=m, N=N, ainf=ainf, omega=wt / ainf, alpha_c=1.0 / ainf, r=r, phi_r=phi)


def ground(P, eps, rtol, lo=0.05, hi=0.9999):
    """The nodeless star at central P: bisection on the code frequency between 'turns up' and 'crosses zero'."""
    flo, _ = shoot(P, lo, eps, rtol)
    fhi, _ = shoot(P, hi, eps, rtol)
    if not (flo == -1 and fhi == 1):
        raise RuntimeError(f"no bracket at P = {P}: fates {flo}, {fhi}")
    while True:
        mid = 0.5 * (lo + hi)
        if mid <= lo or mid >= hi:
            break
        fm, _ = shoot(P, mid, eps, rtol)
        if fm == -1:
            lo = mid
        elif fm == 1:
            hi = mid
        else:
            raise RuntimeError(f"no fate at P = {P}, wt = {mid}")
    _, st = shoot(P, lo, eps, rtol, want_star=True)
    return st


def row_at(eps, target, key, Plo, Phi, rtol):
    """The star with st[key] = target, Brent on P in [Plo, Phi]."""
    g = lambda P: ground(P, eps, rtol)[key] - target  # noqa: E731
    P = brentq(g, Plo, Phi, xtol=1e-17, rtol=4e-16, maxiter=200)
    return ground(P, eps, rtol)


if OPT.scan:
    t0 = time.time()
    for lp in np.linspace(math.log10(2.0e-4), math.log10(2.0e-2), 41):
        P = 10 ** lp
        try:
            st = ground(P, -1, 1e-11)
            print(f"P {P:.6e}: alpha_c {st['alpha_c']:.6f} omega {st['omega']:.8f} N {st['N']:.5f} M {st['M']:.5f} "
                  f"r_turn {st['r']:.1f} ({time.time() - t0:.0f} s)", flush=True)
        except RuntimeError as e:
            print(f"P {P:.6e}: {e}", flush=True)
    sys.exit(0)

# ----------------------------------------------------------------------------------------------------------------------
# K1 (and K0 at the canonical points): the crossing
# ----------------------------------------------------------------------------------------------------------------------
CRATE_WM = {1: 0.9258444557595977280332, -1: 0.928908431058166525237}
P0 = {1: 2.0504432387354122617e-04, -1: 2.0728052897904927504e-04}


def crossing(eps, rtol):
    Ps = [P0[eps] * (1 + 0.01 * (j - 4)) for j in range(9)]
    sts = [ground(P, eps, rtol) for P in Ps]
    x = np.array([(st["P"] - P0[eps]) / P0[eps] for st in sts])
    M = np.array([st["M"] for st in sts])
    w = np.array([st["omega"] for st in sts])
    cM = np.polynomial.polynomial.polyfit(x, M, 4)
    cw = np.polynomial.polynomial.polyfit(x, w, 4)
    d = np.polynomial.polynomial.polyder(cM)
    roots = [z.real for z in np.roots(d[::-1]) if abs(z.imag) < 1e-12 and -0.05 < z.real < 0.05]
    xs = min(roots, key=abs)
    return float(np.polynomial.polynomial.polyval(xs, cw)), sts


if "K1" in ONLY:
    t0 = time.time()
    ok, notes = True, []
    for eps in (1, -1):
        ws = []
        for rt in TOLS:
            wM, sts = crossing(eps, rt)
            ws.append(wM)
            print(f"  eps={eps:+d} rtol={rt:g}: dM/dw = 0 at w = {wM:.15f}; stars w {sts[0]['omega']:.8f} .. {sts[-1]['omega']:.8f}, "
                  f"M {sts[4]['M']:.12e}, N {sts[4]['N']:.12e}, alpha_c {sts[4]['alpha_c']:.10f} ({time.time() - t0:.0f} s)", flush=True)
        okE = abs(ws[-1] - CRATE_WM[eps]) <= 1e-9 and abs(ws[0] - ws[1]) <= 1e-10
        ok &= okE
        notes.append(f"eps={eps:+d}: {ws[-1]:.13f} against the crate's {CRATE_WM[eps]:.13f} (diff {ws[-1] - CRATE_WM[eps]:+.1e}; "
                     f"tolerances differ by {ws[0] - ws[1]:+.1e}; RESULTS.md's stored dM/dw = 0 is "
                     f"{'0.92584446' if eps == 1 else '0.92890838'})")
    check("K1", ok, "; ".join(notes))

# ----------------------------------------------------------------------------------------------------------------------
# K0: the first law dM = eps w dN, 5-point central differences in P
# ----------------------------------------------------------------------------------------------------------------------
def first_law(eps, P, rtol):
    h = 1e-3 * P
    st = [ground(P + k * h, eps, rtol) for k in (-2, -1, 1, 2)]
    d = lambda q: (st[0][q] - 8 * st[1][q] + 8 * st[2][q] - st[3][q]) / (12 * h)  # noqa: E731
    mid = ground(P, eps, rtol)
    want = (-eps if MUT == "eps-law" else eps) * mid["omega"]
    return d("M") / d("N"), want, mid


# ----------------------------------------------------------------------------------------------------------------------
# K2, K3: the phantom rows
# ----------------------------------------------------------------------------------------------------------------------
STORED = {}
for line in open(os.path.expanduser("~/Source/negative-mass/phase2/radial/phantom_family.txt")):
    if line.startswith("#") or not line.strip():
        continue
    t = line.split()
    STORED[round(float(t[0]), 6)] = dict(omega=t[1], N=t[3], M=t[4])
CRATE = {   # the crate's tokens where it differs from the stored print (C1 of taylor_radial_output.txt)
    (2.0, "N"): "120.14872", (2.1, "N"): "141.36644", (2.4, "N"): "213.38901", (2.8, "N"): "328.15124",
    (3.5, "N"): "578.11027", (3.9, "N"): "748.13400", (2.3, "omega"): "0.62757000", (2.8, "omega"): "0.73465188",
    (3.9, "omega"): "0.97410303", (2.4, "M"): "-116.14249"}
CONTROL_ROWS = (1.5, 2.5, 3.0)


def fmt_like(x, tok):
    nd = len(tok.split(".")[1]) if "." in tok else 0
    return f"{x:.{nd}f}"


def half_units(x, tok):
    nd = len(tok.split(".")[1]) if "." in tok else 0
    return (x - float(tok)) / (0.5 * 10.0 ** (-nd))


if any(k in ONLY for k in ("K2", "K3")):   # A1: K0 no longer needs the phantom rows
    BR = {}                                                     # alpha_c -> (Plo, Phi), from a coarse scan
    t0 = time.time()
    grid = [10 ** lp for lp in np.linspace(math.log10(2.0e-4), math.log10(2.0e-2), 41)]
    ac = [ground(P, -1, 1e-11)["alpha_c"] for P in grid]
    print(f"  coarse scan of the phantom family: alpha_c {ac[0]:.4f} .. {max(ac):.4f} over P {grid[0]:.1e} .. {grid[-1]:.1e} "
          f"({time.time() - t0:.0f} s)", flush=True)
    for a in sorted({k[0] for k in CRATE} | set(CONTROL_ROWS)):
        for i in range(len(grid) - 1):
            if (ac[i] - a) * (ac[i + 1] - a) <= 0:
                BR[a] = (grid[i], grid[i + 1])
                break
    ROWS = {}
    for a in sorted(BR):
        ROWS[a] = [row_at(-1, a, "alpha_c", *BR[a], rt) for rt in TOLS]
        st = ROWS[a][-1]
        print(f"  alpha_c={a}: P {st['P']:.12e} omega {st['omega']:.12f} N {st['N']:.10f} M {st['M']:.10f}; tolerances differ "
              f"by {ROWS[a][0]['omega'] - st['omega']:+.1e}, {ROWS[a][0]['N'] - st['N']:+.1e}, {ROWS[a][0]['M'] - st['M']:+.1e} "
              f"({time.time() - t0:.0f} s)", flush=True)

    if "K2" in ONLY:
        ok, notes = True, []
        for (a, q), tok in sorted(CRATE.items()):
            if a not in ROWS:
                ok, _ = False, notes.append(f"alpha_c={a} {q}: no row")
                continue
            x, x0 = ROWS[a][-1][q], ROWS[a][0][q]
            mine = fmt_like(x, tok)
            hu, dhu = half_units(x, tok), abs(half_units(x, tok) - half_units(x0, tok))
            okq = mine == tok and dhu <= 0.1
            ok &= okq
            notes.append(f"alpha_c={a} {q}: {x:.10f} -> {mine} (crate {tok}, stored {STORED[a][q]}; {hu:+.2f} half-units from the "
                         f"crate's token, tolerance spread {dhu:.1e}){'' if okq else ' MISMATCH'}")
        check("K2", ok, "; ".join(notes))
    if "K3" in ONLY:
        ok, notes = True, []
        for a in CONTROL_ROWS:
            for q in ("omega", "N", "M"):
                tok = STORED[a][q]
                x = ROWS[a][-1][q] if a in ROWS else float("nan")
                mine = fmt_like(x, tok)
                ok &= mine == tok
                notes.append(f"alpha_c={a} {q}: {mine} (stored and crate {tok})")
        check("K3", ok, "; ".join(notes))

if "K0" in ONLY:
    t0 = time.time()
    ok, notes = True, []
    for eps, label, target, key, br in ((1, "w=0.95", 0.95, "omega", None), (1, "w=0.90", 0.90, "omega", None),
                                        (-1, "w=0.95", 0.95, "omega", None)):        # A1: the eps = -1 point at w = 0.95
        if True:
            # walk out from the crossing in P until omega passes the target
            Pa = P0[eps]
            wa = ground(Pa, eps, TOLS[-1])["omega"]
            found = None
            for sgn in (-1, 1):
                Pb, wb = Pa, wa
                for _ in range(60):
                    Pn = Pb * (1 + sgn * 0.05)
                    wn = ground(Pn, eps, TOLS[-1])["omega"]
                    if (wb - target) * (wn - target) <= 0:
                        found = (min(Pb, Pn), max(Pb, Pn))
                        break
                    Pb, wb = Pn, wn
                if found:
                    break
            P = brentq(lambda P: ground(P, eps, TOLS[-1])["omega"] - target, *found, xtol=1e-17, rtol=4e-16)
        ratio, want, mid = first_law(eps, P, TOLS[-1])
        okp = abs(ratio / want - 1) <= 1e-7
        ok &= okp
        notes.append(f"eps={eps:+d} {label}: (dM/dP)/(dN/dP) = {ratio:.12f} against eps*w = {want:.12f} (rel {ratio / want - 1:+.1e})")
        print(f"  {notes[-1]} ({time.time() - t0:.0f} s)", flush=True)
    check("K0", ok, "; ".join(notes))

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
