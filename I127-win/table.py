"""The table of the two sectors of #127 (sigma R = 2, m = 19/2 and 21/2): #119's window and label, the new window and
label, #75's own window, real eigenvalues in the window A / B, k, smallest |mu| v_c, n, and each solve's time (from its
log) and peak working set (from memory-sampler.log). Run with the venv python, -X utf8, from this folder:
    python -X utf8 table.py OLD_REPORT NEW_REPORT        (old: #119's wide output, new: report-wide.log)"""
import glob
import os
import re
import sys

import numpy as np

R = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, R)


def rows(path):
    out, sig = {}, None
    for ln in open(path, encoding="utf-8-sig").read().splitlines():
        m = re.match(r"== sigma R = (\S+),", ln)
        if m:
            sig = m.group(1)
        m = re.match(r"\s*([\d.]+) \| (\d+) / (\d+) \|", ln)
        if m and sig == "2":
            c = [x.strip() for x in ln.split("|")]
            w = re.match(r"([\d.]+) / ([\d.]+) \(([\d.]+)\)", c[7])
            out[m.group(1)] = dict(w5=w.group(1), w4=w.group(2), own=w.group(3), setby=c[8], real=c[10], dirs=c[-1])
    return out


old, new = rows(sys.argv[1]), rows(sys.argv[2])
peak = {}
for ln in open(os.path.join(R, "memory-sampler.log"), encoding="utf-8-sig"):
    m = re.search(r"peak=([\d,]+)MB cpu=([\d,]+)s (.*)$", ln)
    if m:
        a = m.group(3).strip()
        peak[a] = max(peak.get(a, 0.0), float(m.group(1).replace(",", "")))
print("| m | window 10^-5 #119 | set by | window 10^-5 now | set by | #75's own | real A / B | k A / B | "
      "smallest |mu| v_c A / B | n A / B | time A / B | peak A / B |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|")
for m in ("9.5", "10.5"):
    f = {d: np.load(os.path.join(R, "eig", f"s2_{d}_m{int(2 * float(m))}.npz")) for d in "AB"}
    vc = float(f["A"]["vc"])
    t, p = {}, {}
    for d in "AB":
        for lg in glob.glob(os.path.join(R, "*.log")):
            if ".died" in lg:
                continue
            txt = open(lg, encoding="utf-8-sig").read()
            if f"disc {d} " in txt:
                mm = re.search(rf"m = {m}: h = .*?, (\d+) s$", txt, re.M)
                if mm:
                    t[d] = int(mm.group(1))
                    job = os.path.basename(lg)[:-4]
                    cmd = open(os.path.join(R, f"job_{job}.cmd")).read()
                    ks = [k for k in peak if f"--disc={d}" in k and any(f"--ms={x}" in k for x in re.findall(r"--ms=(\S+)", cmd))]
                    p[d] = max((peak[k] for k in ks), default=float("nan"))
    o, n = old[m], new[m]
    ks = " / ".join(str(len(f[d]["mu"])) for d in "AB")
    sm = " / ".join(f"{abs(f[d]['mu'][-1]) * vc:.4f}" for d in "AB")
    ns = " / ".join(str(int(f[d]["n"])) for d in "AB")
    print(f"| {float(m) * 1:g} | {o['w5']} | {o['setby']} | {n['w5']} | {n['setby']} | {n['own']} | {n['real']} | {ks} | {sm} | "
          f"{ns} | {t.get('A', 'n/a')} s / {t.get('B', 'n/a')} s | "
          f"{p.get('A', float('nan')) / 1024:.2f} / {p.get('B', float('nan')) / 1024:.2f} GiB |")
print("residuals (max over the files):", ", ".join(f"{d} m = {m}: {float(np.load(os.path.join(R, 'eig', f's2_{d}_m{int(2 * float(m))}.npz'))['res']):.1e}"
                                                   for d in "AB" for m in ("9.5", "10.5")))
