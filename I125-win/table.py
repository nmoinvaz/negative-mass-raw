"""The ten-sector table of #125 as markdown rows: sigma R, m, #75's A and B leading |mu| v_c, A vs B, #120's A and B
(m >= 23/2 only), #75's A against #120's A and B, the sector's time and its process's peak working set (memory-sampler.log,
the job's processes, worker included). Reads eig/ and ../I120-win/eig. Run with the venv python, -X utf8."""
import os
import re
from collections import defaultdict

import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
R120 = os.path.join(R, "..", "I120-win", "eig")
jobs = {}
for ln in open(os.path.join(R, "jobs.txt"), encoding="utf-8"):
    if ln.strip():
        j, a = ln.rstrip("\n").split("|", 1)
        jobs[j] = a.replace("%~dp0", "")
peak = defaultdict(float)
for ln in open(os.path.join(R, "memory-sampler.log"), encoding="utf-8-sig"):
    m = re.search(r"peak=([\d,]+)MB cpu=\d+s (.*)$", ln)
    if m:
        peak[m.group(2).strip()] = max(peak[m.group(2).strip()], float(m.group(1).replace(",", "")))
times = {}  # (sigma R, m) -> (seconds, peak GiB of the process)
for job, args in jobs.items():
    for s, m, t in re.findall(r"sigma R = (\d+), m = ([\d.]+): done in (\d+) s",
                              open(os.path.join(R, job + ".log"), encoding="utf-8-sig").read()):
        times[(int(s), float(m))] = (int(t), peak[args] / 1024)
print("| σR | m | #75 A | #75 B | A vs B | #120 A | #120 B | #75 A vs #120 A / B | time, peak of its process |")
print("|---|---|---|---|---|---|---|---|---|")
for sig in (2, 4):
    for m in (10.5, 11.5, 14.5, 17.5, 20.5):
        d = np.load(os.path.join(R, "eig", f"tanh_sigma{sig}_m{m:g}.npz"))
        vc = float(d["vc"])
        a, b = np.abs(d["muA"]).max() * vc, np.abs(d["muB"]).max() * vc
        if m == 10.5:
            c120 = "| — | — | —"
        else:
            fa = np.load(os.path.join(R120, f"s{sig}_A_m{int(2 * m)}.npz"))
            fb = np.load(os.path.join(R120, f"s{sig}_B_m{int(2 * m)}.npz"))
            ra, rb = np.abs(fa["mu"]).max() * float(fa["vc"]), np.abs(fb["mu"]).max() * float(fb["vc"])
            c120 = f"| {ra:.8f} | {rb:.8f} | {abs(a - ra) / ra:.1e} / {abs(a - rb) / rb:.1e}"
        t, p = times[(sig, m)]
        print(f"| {sig} | {int(2 * m)}/2 | {a:.8f} | {b:.8f} | {abs(a - b) / a:.1e} {c120} | {t} s, {p:.2f} GiB |")
