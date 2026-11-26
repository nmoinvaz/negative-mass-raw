#!/usr/bin/env python3
"""ind189: multishoot's plane stepper (PR #70) on a rotated Airy system, against the exact plane and volume in mpmath
(criteria in README.md beside this file).

    python3 ind189.py [--mutate=NAME]
"""
import argparse
import json
import os
import subprocess
import sys

import mpmath as mp

mp.mp.dps = 90
HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["wrong-scale", "scaleonly"])
MUT = ap.parse_args().mutate
H = os.path.join(HERE, "airy_plane")
BIN = os.path.join(H, "target", "release", "airy_plane")
if MUT == "scaleonly":
    subprocess.check_call(["nice", "-n", "10", "cargo", "build", "--release", "-j", "2", "-q", "--features", "mutate",
                           "--target-dir", os.path.join(H, "target", "mutate")], cwd=H)
    BIN = os.path.join(H, "target", "mutate", "release", "airy_plane")
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def qmat():
    q = mp.eye(4)
    for i, j, c, s, d in [(0, 2, 3, 4, 5), (1, 3, 5, 12, 13), (0, 1, 8, 15, 17), (2, 3, 7, 24, 25)]:
        g = mp.eye(4)
        cc, ss = mp.mpf(c) / d, mp.mpf(s) / d
        g[i, i], g[i, j], g[j, i], g[j, j] = cc, -ss, ss, cc
        q = g * q
    return q


AI0, AIP0, BI0, BIP0 = mp.airyai(0), mp.airyai(0, 1), mp.airybi(0), mp.airybi(0, 1)


def fg(x):
    """f, f', g, g' with f(0) = 1, f'(0) = 0, g(0) = 0, g'(0) = 1 for u'' = x u"""
    ai, aip, bi, bip = mp.airyai(x), mp.airyai(x, 1), mp.airybi(x), mp.airybi(x, 1)
    f, fp = mp.pi * (BIP0 * ai - AIP0 * bi), mp.pi * (BIP0 * aip - AIP0 * bip)
    g, gp = mp.pi * (AI0 * bi - BI0 * ai), mp.pi * (AI0 * bip - BI0 * aip)
    return f, fp, g, gp


def exact(k, X):
    c = mp.cbrt(4 * (1 + (mp.mpf("1e-9") if MUT == "wrong-scale" else 0)))
    f, fp, g, gp = fg(X)
    F, Fp, G, Gp = fg(c * X)
    phi = mp.zeros(4, 4)
    phi[0, 0], phi[0, 1], phi[1, 0], phi[1, 1] = f, g, fp, gp
    phi[2, 2], phi[2, 3], phi[3, 2], phi[3, 3] = F, G / c, c * Fp, Gp
    bm = mp.matrix([[1, 0, 0.5, 0.25], [0.5, 1, 0, -0.5], [0.25, -0.5, 1, 0], [0, 0.75, 0.5, 1]])
    y = qmat() * phi * bm[:, :k] if k < 4 else qmat() * phi * bm
    y0 = qmat() * (bm[:, :k] if k < 4 else bm)
    return y, y0


def orth(y):
    n, k = y.rows, y.cols
    u = mp.zeros(n, k)
    for j in range(k):
        v = y[:, j]
        for _ in range(2):
            for i in range(j):
                v = v - (u[:, i].T * v)[0] * u[:, i]
        u[:, j] = v / mp.norm(v)
    return u


def lnvol(y):
    return mp.log(mp.det(y.T * y)) / 2


EPSBAR = 1e4
cells = {1: [], 2: [], 4: []}
for lane in ("f64", "dd", "qd"):
    for k in (1, 2, 4):
        for X in (4, 10):
            args = [BIN, lane, str(k), str(X)] + (["scaleonly"] if MUT == "scaleonly" else [])
            p = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True)
            if p.returncode:
                cells[k].append((lane, X, False, f"{lane} X={X}: harness exit {p.returncode} ({p.stderr.strip()[-120:]})"))
                continue
            o = json.loads(p.stdout)
            eps = o["eps"]
            y, y0 = exact(k, X)
            lv = lnvol(y)
            dlv = abs(mp.mpf(o["ln_vol"]) - lv)
            blv = EPSBAR * eps * max(1.0, float(abs(lv)))
            if k < 4:
                yl = mp.matrix(4, k)
                for c in range(k):
                    for i in range(4):
                        yl[i, c] = mp.mpf(o["cols"][c * 4 + i])
                u = orth(y)
                perr = mp.norm(yl - u * (u.T * yl), 2) if k == 1 else mp.sqrt(sum(x**2 for x in (yl - u * (u.T * yl))))
                bp = EPSBAR * eps
                good = perr <= bp and dlv <= blv
                txt = (f"{lane} X={X}: plane {mp.nstr(perr, 2)} (bar {bp:.1e}), ln_vol {mp.nstr(dlv, 2)} "
                       f"(bar {blv:.1e}, exact {mp.nstr(lv, 12)}), {o['steps']} steps")
            else:
                good = dlv <= blv and abs(lv - mp.log(abs(mp.det(y0)))) < mp.mpf("1e-80")
                txt = (f"{lane} X={X}: ln_vol {mp.nstr(dlv, 2)} (bar {blv:.1e}; exact ln|det| {mp.nstr(lv, 12)}), "
                       f"{o['steps']} steps")
            cells[k].append((lane, X, good, txt))
for name, k in (("Q1", 1), ("Q2", 2), ("Q3", 4)):
    check(name, all(c[2] for c in cells[k]), "; ".join(c[3] for c in cells[k]))
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
