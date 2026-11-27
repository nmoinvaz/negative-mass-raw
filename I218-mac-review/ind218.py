#!/usr/bin/env python3
"""ind218: the Ellis polar quasinormal modes of #218's planted cases by uniform complex scaling (criteria in README.md)."""
import cmath
import sys

import numpy as np
import scipy.sparse as sps
from scipy.sparse.linalg import eigs

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
TH = 0.0 if MUT == "no-scaling" else 0.9
SC = 1.01 if MUT == "V-scale" else 1.0
L = 160.0 if "--k1b" in sys.argv else 40.0                      # A1: K1b at L = 160
POT = {"l1": lambda R2: 1 / R2 ** 2, "darboux": lambda R2: 2 / R2 - 3 / R2 ** 2,
       "l2": lambda R2: 6 / R2 - 3 / R2 ** 2, "test": lambda R2: 2 / R2 + 1 / R2 ** 2}
RES = []


def check(name, ok, detail):
    RES.append(bool(ok))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def qnm(key, h, target):
    n = int(round(2 * L / h)) - 1
    s = -L + h * np.arange(1, n + 1)
    z = s * np.exp(1j * TH)
    V = SC * POT[key](1 + z * z)
    c = -np.exp(-2j * TH) / (12 * h * h)                       # -u'' scaled: -(1/e^{2i th}) d2/ds2, 4th order
    main = V + c * (-30) * np.ones(n)
    off1 = c * 16 * np.ones(n - 1)
    off2 = c * (-1) * np.ones(n - 2)
    M = sps.diags([off2, off1, main, off1, off2], [-2, -1, 0, 1, 2], format="csc")
    vals = eigs(M, k=1, sigma=target ** 2, return_eigenvectors=False)
    w = cmath.sqrt(vals[0])
    return w if w.real > 0 else -w


ref1, ref2, reft = 0.681367187 - 0.617753448j, 1.737692 - 0.305138j, 1.5727 - 0.5297j
w1 = {h: qnm("l1", h, ref1) for h in (0.02, 0.01)}
wd = qnm("darboux", 0.01, ref1)
w2 = qnm("l2", 0.01, ref2)
wt = qnm("test", 0.01, reft)
for k, v in (("l1 h=0.02", w1[0.02]), ("l1 h=0.01", w1[0.01]), ("darboux", wd), ("l2", w2), ("test", wt)):
    print(f"  {k}: omega = {v.real:.10f} {v.imag:+.10f}i", flush=True)
check("K1b" if L == 160.0 else "K1", abs(w1[0.01] - ref1) <= 1e-6 and abs(w1[0.01] - wd) <= 1e-6 and abs(w1[0.02] - w1[0.01]) <= 1e-5,
      f"|l1 - polar.md| {abs(w1[0.01] - ref1):.1e}, |l1 - Darboux partner| {abs(w1[0.01] - wd):.1e}, h spread {abs(w1[0.02] - w1[0.01]):.1e}")
check("K2", abs(w2 - ref2) <= 2e-6, f"|l2 - polar.md| {abs(w2 - ref2):.1e}")
check("K3", abs(wt - reft) <= 1e-3 and abs(wt - w1[0.01]) > 0.5, f"|test - polar.md| {abs(wt - reft):.1e}, |test - l1| {abs(wt - w1[0.01]):.2f}")
print(f"\n{len(RES)} criteria, {sum(RES)} pass; mutation {MUT}")
sys.exit(0 if all(RES) else 1)
