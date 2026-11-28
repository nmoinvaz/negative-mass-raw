#!/usr/bin/env python3
"""ind282: f_7 of the ln 2 factor from #282's printed Omega_k against its identified closed form (criteria in README.md).

    python3 ind282.py OUTPUT [--mutate=zeta3|ln2]

OUTPUT is order8_output.txt of branch wip/i282-omega6. Imports nothing from the repository. Exit 1 when a check fails.
"""
import re
import sys

import mpmath as mp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
OUT = [a for a in sys.argv[1:] if not a.startswith("--")][0]
mp.mp.dps = 200
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


txt = open(OUT).read()
printed = {int(k): v for k, v in re.findall(r"^\s+Omega([0-6]) = (-?[0-9.]+)$", txt, re.M)}
L2, z3, z5, z7, pi = mp.log(2), mp.zeta(3), mp.zeta(5), mp.zeta(7), mp.pi
Om = {0: -4 * L2, 1: 2 * pi ** 2 / 3 + 8 * L2 ** 2, 2: 80 * z3 - mp.mpf(8) / 3 * pi ** 2 * L2 - mp.mpf(32) / 3 * L2 ** 3}
for k in (3, 4, 5, 6):
    Om[k] = mp.mpf(printed[k])
digits = {k: len(printed[k].split(".")[1]) for k in (3, 4, 5, 6)}
print("  printed digits after the point:", digits)
for k in (0, 1, 2):
    print(f"  Omega{k}: closed form against printed (60 digits): {mp.nstr(abs(Om[k] - mp.mpf(printed[k])), 3)}")

sgn = -1 if MUT == "ln2" else 1
a = [mp.mpf(1)] + [Om[k] for k in range(7)]
b = [(sgn * 4 * L2) ** m / mp.factorial(m) for m in range(8)]
f = [sum(a[k] * b[n - k] for k in range(n + 1)) for n in range(8)]

e2 = abs(f[2] - 2 * pi ** 2 / 3)
e3 = abs(f[3] - 80 * z3)
check("K1", e2 < mp.mpf("1e-50") and e3 < mp.mpf("1e-50"), f"f2 - 2pi^2/3 = {mp.nstr(e2, 3)}, f3 - 80 zeta(3) = {mp.nstr(e3, 3)} (bar 1e-50)")

c = 589824 if MUT == "zeta3" else 565248
f7 = (mp.mpf(7656704) / 2835 * pi ** 6 + mp.mpf(328672) / 45 * pi ** 4 * z3 - mp.mpf(74752) / 5 * pi ** 4 + 30720 * pi ** 2 * z3
      - 2176 * pi ** 2 * z5 + 36864 * z3 ** 2 + c * z3 - 307200 * z5 + 974336 * z7)
rel = abs(f[7] / f7 - 1)
check("K2", rel < mp.mpf("1e-90"), f"f7 from the printed Omega = {mp.nstr(f[7], 30)}; identified closed form = {mp.nstr(f7, 30)}; relative difference {mp.nstr(rel, 3)} (bar 1e-90)")
for n in (4, 5, 6):
    print(f"  f{n} = {mp.nstr(f[n], 25)}")
check("K3", True, "f4 .. f6 printed above (reported)")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
