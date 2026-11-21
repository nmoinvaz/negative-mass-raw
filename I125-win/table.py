"""The ten-sector table of #125 as markdown rows: sigma R, m, #75's A and B leading |mu| v_c, A vs B, #120's A and B
(m >= 23/2 only), #75's A against #120's A and B, and the sector's time from the job logs. Reads eig/ and ../I120-win/eig.
Run with the venv python, -X utf8."""
import os
import re

import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
R120 = os.path.join(R, "..", "I120-win", "eig")
times = {}
for job in ("pilot-s4-m20.5", "solve-s2", "solve-s4"):
    for s, m, t in re.findall(r"sigma R = (\d+), m = ([\d.]+): done in (\d+) s",
                              open(os.path.join(R, job + ".log"), encoding="utf-8-sig").read()):
        times[(int(s), float(m))] = int(t)
print("| σR | m | #75 A | #75 B | A vs B | #120 A | #120 B | #75 A vs #120 A / B | time |")
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
            c120 = f"| {ra:.6f} | {rb:.6f} | {abs(a - ra) / ra:.1e} / {abs(a - rb) / rb:.1e}"
        print(f"| {sig} | {int(2 * m)}/2 | {a:.6f} | {b:.6f} | {abs(a - b) / a:.1e} {c120} | {times[(sig, m)]} s |")
