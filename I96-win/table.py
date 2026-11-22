"""Markdown tables of #96's sector runs, from a sectors log and the sector files in eig/. Usage (venv python, -X utf8):
    table.py <sectors log> <sigma R>
The sector table (section 4 of tanh_spectrum.md): m, the leading mu v_c as a + bi (a, b >= 0), |mu| v_c of A and B, the next
|mu| v_c (the fifth, after the quadruple), "converged above" and the symmetry, the last two parsed from the log. The window
table (section 5): per sector the window, the eigenvalues in it (A / B), the real ones in it, the real ones anywhere (A / B),
the largest of them and how many B reproduces, the identity's worst value and the number of eigenfunctions. Then the totals
and the summary lines of the log. Reads only; writes to stdout."""
import os
import re
import sys

import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
log, sig = sys.argv[1], sys.argv[2]
txt = open(log, encoding="utf-8-sig").read()
rows, reals = {}, {}
for ln in txt.splitlines():
    m = re.match(r"\s+([\d.]+) \| (\S+ \S+ \S+ \S+) \| ([\d.]+) / ([\d.]+) \| +([\d.]+) \| ([\d.e+-]+)$", ln)
    if m:
        rows[float(m.group(1))] = {"A": float(m.group(3)), "B": float(m.group(4)), "cut": float(m.group(5)), "asym": m.group(6)}
    m = re.match(r"\s+(\d+) \| +([\d.]+) \| +([\d.]+) \| +(\d+) / +(\d+) \| (\d+) / (\d+) \| +(\d+) / +(\d+), ([\d.e+-]+), "
                 r"(\d+) \| .* ([\d.e+-]+) on (\d+) eigenfunctions, (\d+) real", ln)
    if m and m.group(1) == str(int(float(sig))):
        reals[float(m.group(2))] = [m.group(i) for i in range(3, 15)]
print(f"| m | leading mu v_c (a quadruple +-a +-bi) | \\|mu\\|v_c, A | \\|mu\\|v_c, B | next \\|mu\\|v_c | converged above | "
      f"symmetric to |")
print("|---|---|---|---|---|---|---|")
for m_ in sorted(rows):
    d = np.load(os.path.join(R, "eig", f"tanh_sigma{sig}_m{m_:g}.npz"))
    vc = float(d["vc"])
    mu = d["muA"] * vc
    mu = mu[np.argsort(-np.abs(mu))]
    cand = [z for z in mu[:4] if z.imag > 0 and z.real >= 0]
    z = cand[0] if cand else mu[0]
    r = rows[m_]
    print(f"| {m_:g} | {abs(z.real):.5f} + {abs(z.imag):.5f}i | {r['A']:.6f} | {r['B']:.6f} | {abs(mu[4]):.6f} | "
          f"{r['cut']:.4f} | {r['asym']} |")
print()
print("| m | window \\|mu\\|v_c >= | eigenvalues in it (A / B) | real in it (A / B) | real with \\|mu\\|v_c > 1e-8 (A / B) | "
      "largest | reproduced by B | identity worst | eigenfunctions (real) |")
print("|---|---|---|---|---|---|---|---|---|")
tot = np.zeros(4, int)
anyA, anyB, ev, lg = [], [], [], []
for m_ in sorted(reals):
    g = reals[m_]
    print(f"| {m_:g} | {g[0]} | {g[1]} / {g[2]} | {g[3]} / {g[4]} | {g[5]} / {g[6]} | {g[7]} | {g[8]} | {g[9]} | "
          f"{g[10]} ({g[11]}) |")
    tot += [int(g[1]), int(g[2]), int(g[3]), int(g[4])]
    anyA.append(int(g[5])), anyB.append(int(g[6])), lg.append(float(g[7])), ev.append(float(g[9]))
if reals:
    print()
    print(f"totals over {len(reals)} sectors: eigenvalues in the windows {tot[0]} / {tot[1]}, real in the windows "
          f"{tot[2]} / {tot[3]}; real with |mu| v_c > 1e-8 per sector {min(anyA)} to {max(anyA)} (A) / {min(anyB)} to "
          f"{max(anyB)} (B), the largest {max(lg):.1e}; worst identity value {max(ev):.1e}")
seen = set()
for key in ("rho(T1) v_c", "window:", "[PASS] converged", "[FAIL] converged", "[PASS] ref63", "[FAIL] ref63", "peak resident", "FAILED:",
            "all checks passed"):
    for ln in txt.splitlines():
        if key in ln and ln.strip() not in seen:
            seen.add(ln.strip())
            print(ln.strip())
