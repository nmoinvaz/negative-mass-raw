#!/usr/bin/env python3
"""ind322: #262's closed form Q = -J/I0 at #322's three Pi, by nested quadrature, and the printed fits against it (criteria in README.md).

    python3 ind322.py OUTPUT [--mutate=j-sign|rho-is-pi]

OUTPUT is remainder_output.txt of branch wip/i322-remainder. Imports nothing from the repository. Exit 1 when a check fails.
"""
import re
import sys

import mpmath as mp

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
OUT = [a for a in sys.argv[1:] if not a.startswith("--")][0]
mp.mp.dps = 25
K = 2 / mp.pi
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def A(r):
    return 1 - (1 + r * r) + K * (r + (1 + r * r) * mp.atan(r))


def H(rho):
    return mp.quad(lambda r: K / A(r) - 1 / (2 * r), [0, rho])


def jint(r):
    return 2 * K * r * mp.exp(-2 * H(r)) / (A(r) * (1 + r * r))


def J(rho):
    return mp.quad(jint, [0, rho])


I0 = mp.quad(jint, [0, 1, 4, 12, 30, mp.inf])
rel = abs(I0 / mp.mpf("1.0149036099284090") - 1)
check("K1", rel < mp.mpf("1e-12"), f"I0 = {mp.nstr(I0, 17)} against #262's 1.0149036099284090: relative {mp.nstr(rel, 3)} (bar 1e-12)")

txt = open(OUT).read()
m = re.search(r"Q\(rho\) = -J\(rho\)/I0 at Pi = -0\.1, 0\.5, 1\.0 \(rho = ([-0-9.]+), ([-0-9.]+), ([-0-9.]+)\): ([-+0-9.]+), ([-+0-9.]+), ([-+0-9.]+)", txt)
rho_p, q_p = m.groups()[:3], m.groups()[3:]
G0 = mp.exp(2 * H(1))                                                  # A1: the chart's Pi = rho e^{2H} / G0
g0p = re.search(r"G0 = ([0-9.]+)", txt).group(1)
print(f"  G0 = e^(2H(1)) = {mp.nstr(G0, 12)}; printed {g0p}: "
      f"{'equal' if abs(G0 - mp.mpf(g0p)) <= 0.5 * 10 ** -len(g0p.split('.')[1]) else 'DIFFERENT'} to half a unit (reported)")
PIS = (mp.mpf("-0.1"), mp.mpf("0.5"), mp.mpf(1))
ok2, Q = True, {}
for Pi, rs, qs in zip(PIS, rho_p, q_p):
    rho = Pi if MUT == "rho-is-pi" else mp.findroot(lambda y: y * mp.exp(2 * H(y)) - G0 * Pi, mp.mpf(rs))
    q = (1 if MUT == "j-sign" else -1) * J(rho) / I0
    Q[float(Pi)] = q
    hr = 0.5 * 10 ** -len(rs.split(".")[1])
    hq = 0.5 * 10 ** -len(qs.split(".")[1])
    ok = abs(rho - mp.mpf(rs)) <= hr and abs(q - mp.mpf(qs)) <= hq
    ok2 &= ok
    print(f"  Pi = {mp.nstr(Pi, 3)}: rho {mp.nstr(rho, 10)} (printed {rs}), Q {mp.nstr(q, 10)} (printed {qs}) {'ok' if ok else 'OFF'}")
check("K2", ok2, "rho(Pi) and Q at the three Pi equal the printed closed form to half a unit of the last digit")

rows = re.findall(r"^\| (\w+) \| (-?[0-9.]+) \| ([-+0-9.]+) \| ([-+0-9.]+) \| ([-+0-9.e]+) \|", txt, re.M)
worst, n = 0.0, 0
for name, pi, qfit, qpred, _ in rows:
    d = abs(float(qfit) - float(Q[float(pi)]))
    worst = max(worst, d)
    n += 1
data = sorted({r[0] for r in rows})
check("K3", n == 33 and worst <= 4.3e-4 + 5e-6, f"{n} fits of {len(data)} data ({', '.join(data)}): worst |Q fit - Q| = {worst:.2e} (bar 4.35e-4)")

bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
