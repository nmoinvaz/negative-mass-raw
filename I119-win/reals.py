"""Real eigenvalues returned below the windows (#75 lists 30 to 66 unconverged real ones per sector below its windows).
For each of the 36 files of eig/: the number of real eigenvalues (|Im mu| <= 1e-9 |mu|, the report's tolerance) and the
largest real |mu| v_c, against the sector's window (the smaller of the 1e-5 and 1e-4 windows of report-wide.log, where
the report searches for real eigenvalues). Prints a markdown table, and exits 1 if a real eigenvalue lies above its
window in any file. Run with the venv python, -X utf8."""
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
win, sig = {}, None
for ln in open(os.path.join(HERE, "report-wide.log"), encoding="utf-8"):
    h = re.match(r"== sigma R = (\d+)", ln)
    if h:
        sig = float(h.group(1))
    if sig is not None and re.match(r"^\s+\d+\.?\d* \| \d+ / \d+ \|", ln):
        f = [x.strip() for x in ln.split("|")]
        w = re.match(r"([\d.]+) / ([\d.]+) \(", f[7])
        win[(sig, float(f[0]))] = min(float(w.group(1)), float(w.group(2)))
SECTORS = [(2.0, m + 0.5) for m in range(11)] + [(4.0, m + 0.5) for m in range(4, 11)]
print("| σR | m | window | real, A | largest real \\|μ\\|v_c, A | real, B | largest real \\|μ\\|v_c, B |")
print("|---|---|---|---|---|---|---|")
bad = 0
tot = {"A": 0, "B": 0}
for s, m in SECTORS:
    cells = []
    for d in "AB":
        z = np.load(os.path.join(HERE, "eig", f"s{s:g}_{d}_m{int(2 * m)}.npz"))
        mu, vc = z["mu"], float(z["vc"])
        re_ = mu[np.abs(mu.imag) <= 1e-9 * np.abs(mu)]
        top = float(np.abs(re_).max() * vc) if len(re_) else 0.0
        if top > win[(s, m)]:
            bad += 1
        tot[d] += len(re_)
        cells += [str(len(re_)), f"{top:.4f}" if len(re_) else "-"]
    print(f"| {s:g} | {m:g} | {win[(s, m)]:.4f} | " + " | ".join(cells) + " |")
print(f"\nreal eigenvalues returned in the 18 sectors: A {tot['A']}, B {tot['B']}; files with one above its window: {bad}")
sys.exit(1 if bad else 0)
