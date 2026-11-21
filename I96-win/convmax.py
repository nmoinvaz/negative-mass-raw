"""Parses the conv logs given as arguments (or every conv-*.log here): the largest relative move of the leading eigenvalue
(not counting the deliberately coarse dK = 12, as the script's check does), the variant and m, the second largest, the
wall time and the peak working set of the job (memory-sampler.log). Run with the venv python, -X utf8."""
import glob
import os
import re
import sys

R = os.path.dirname(os.path.abspath(__file__))
logs = sys.argv[1:] or sorted(glob.glob(os.path.join(R, "conv-*.log")))
peak = {}
for ln in open(os.path.join(R, "memory-sampler.log"), encoding="utf-8-sig"):
    m = re.search(r"peak=([\d,]+)MB cpu=\d+s (tanh_spectrum --part=conv.*)$", ln)
    if m:
        peak[m.group(2).strip()] = max(peak.get(m.group(2).strip(), 0.0), float(m.group(1).replace(",", "")))
for path in logs:
    txt = open(path, encoding="utf-8-sig").read()
    rows, m_cur, sig_cur = [], None, None
    for ln in txt.splitlines():
        m = re.match(r"\s+sigma R = (\d+), m = ([\d.]+)", ln)
        if m:
            sig_cur, m_cur = m.group(1), m.group(2)
            continue
        m = re.match(r"\s+(base|dK = \d+|p = \d+|Lmap = \d+|npan = \d+)\s+\| ([\d.]+)\s+\| ([+-][\d.e+-]+)", ln)
        if m and m_cur:
            name, lead, chg = m.group(1), float(m.group(2)), float(m.group(3))
            rows.append((abs(chg) / lead, name, sig_cur, m_cur, chg))
    rows = [r for r in rows if r[1] not in ("base", "dK = 12")]
    rows.sort(reverse=True)
    w = re.findall(r"wall (\d+) s", txt)
    args = re.search(r"--sigmas=\S+ --p=\S+ --npan=\S+", txt)
    pk = [v for k, v in peak.items() if os.path.basename(path)[:-4] and "--p=" in k and
          re.search(r"--p=(\d+):(\d+)", k) and
          os.path.basename(path).startswith("conv-s%s-p%s-n" % tuple(re.search(r"--sigmas=(\d+).*--p=\d+:(\d+)", k).groups()))]
    print(os.path.basename(path), "wall", w[-1] if w else "?", "s", "peak MiB", max(pk) if pk else "?",
          "| largest", " ; ".join(f"{r[0]:.1e} ({r[1]}, m = {r[3]})" for r in rows[:3]))
