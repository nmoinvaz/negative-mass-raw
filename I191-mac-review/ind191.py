#!/usr/bin/env python3
"""ind191: multisolver's locate (PR #26) on three planted series of the coordinator's choosing (criteria in README.md).

    python3 ind191.py [--mutate=NAME]
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

import mpmath as mp

mp.mp.dps = 150
HERE = os.path.dirname(os.path.abspath(__file__))
BIN = os.path.join(HERE, "harness", "target", "release", "locate_harness")
ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["wrong-s", "pair-as-real"])
MUT = ap.parse_args().mutate
RESULTS = []
KMAX = 120


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def series_L1(s):
    return [mp.mpf(0)] + [1 / (k * mp.mpf(s)**k) for k in range(1, KMAX + 1)]


def binom_series(alpha, s, n):
    """(1 - x/s)^alpha = sum binom(alpha, k) (-x/s)^k"""
    out, b = [], mp.mpf(1)
    for k in range(n + 1):
        out.append(b * (-1 / mp.mpf(s))**k)
        b = b * (alpha - k) / (k + 1)
    return out


def series_L2(s):
    br = binom_series(mp.mpf(-3) / 2, s, KMAX)
    ch = [(1 / mp.factorial(k)) if k % 2 == 0 else mp.mpf(0) for k in range(KMAX + 1)]
    return [mp.fsum(ch[j] * br[k - j] for j in range(k + 1)) for k in range(KMAX + 1)]


def series_L3():
    out = [mp.mpf(0)] * (KMAX + 1)
    b = mp.mpf(1)
    a = mp.mpf(-1) / 3
    for j in range(KMAX // 2 + 1):
        out[2 * j] = b * (mp.mpf(1) / 4)**j
        b = b * (a - j) / (j + 1)
    return out


CASES = [("L1", series_L1(mp.mpf("1.7")), "Real", 1.7, 0.0, 0.0),
         ("L2", series_L2(mp.mpf("-2.3")), "Real", -2.3 * (1.01 if MUT == "wrong-s" else 1), 0.0, -1.5),
         ("L3", series_L3(), "Real" if MUT == "pair-as-real" else "Pair", 0.0, 2.0, -1.0 / 3)]
ok1 = ok2 = True
n1, n2 = [], []
for name, c, kind, sre, sim, alpha in CASES:
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as fh:
        for v in c:
            fh.write(mp.nstr(v, 140, min_fixed=1, max_fixed=0) + "\n")
        path = fh.name
    for lane, K in (("f64", 30), ("dd", 60), ("qd", 120)):
        p = subprocess.run(["nice", "-n", "10", BIN, lane, str(K), path], capture_output=True, text=True)
        if p.returncode:
            ok1 = ok2 = False
            n1.append(f"{name} {lane}: harness exit {p.returncode} {p.stderr[-120:]}")
            continue
        r = json.loads(p.stdout.strip().splitlines()[-1])
        k_ok = r["kind"] == kind
        ok1 &= k_ok
        n1.append(f"{name} {lane} K={K}: {r['kind']}" + ("" if k_ok else f" (expected {kind})"))
        if r["kind"] in ("Real", "Pair"):
            es = abs(complex(r["re"], r["im"]) - complex(sre, sim))
            ea = abs(r["alpha"] - alpha)
            cov = es <= r["bar"] and ea <= r["alpha_bar"]
            n2.append(f"{name} {lane}: |ds| {es:.1e} (bar {r['bar']:.1e}), |dalpha| {ea:.1e} (bar {r['alpha_bar']:.1e})"
                      + ("" if cov else " NOT COVERED"))
        else:
            cov = False
            n2.append(f"{name} {lane}: {r['kind']}, no bar")
        ok2 &= cov
    os.unlink(path)
check("K1", ok1, "; ".join(n1))
check("K2", ok2, "; ".join(n2))
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
