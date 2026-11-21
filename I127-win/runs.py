"""Per job: exit, wall (the log's last 'wall N s'), peak working set (from memory-sampler.log), and the largest
residual of the files of eig/. Run with the venv python, -X utf8."""
import glob
import os
import re

import numpy as np
from collections import defaultdict

R = os.path.dirname(os.path.abspath(__file__))
peak = defaultdict(float)
for ln in open(os.path.join(R, "memory-sampler.log"), encoding="utf-8-sig"):
    m = re.search(r"peak=([\d,]+)MB cpu=([\d,]+)s (.*)$", ln)
    if m:
        a = m.group(3).replace(R + "\\eig", "").strip()
        peak[a] = max(peak[a], float(m.group(1).replace(",", "")))
free = [float(x) for x in re.findall(r"free=([\d.]+)GB", open(os.path.join(R, "memory-sampler.log"), encoding="utf-8-sig").read())]
print(f"free memory over the run: min {min(free):.1f}, max {max(free):.1f} GiB, {len(free)} samples")
rows = []
for f in sorted(glob.glob(os.path.join(R, "*.log.exit"))):
    job = os.path.basename(f)[:-len(".log.exit")]
    ex = open(f).read().strip()
    log = open(os.path.join(R, job + ".log"), encoding="utf-8-sig").read()
    w = re.findall(r"^wall (\d+) s", log, re.M)
    # peak: the sampler's args string for this job
    args = [a for a in peak if all(t in a for t in re.findall(r"--(?:sigma|disc|ms)=\S+", open(os.path.join(R, f"job_{job}.cmd")).read()))]
    rows.append((job, ex, int(w[0]) if w else -1, max((peak[a] for a in args), default=float("nan")) / 1024))
tot = 0
for job, ex, w, p in rows:
    tot += w
    print(f"{job:22s} exit {ex}  wall {w:6d} s ({w / 60:6.1f} min)  peak {p:5.2f} GiB")
print(f"sum of wall times {tot} s = {tot / 3600:.1f} h")
res = sorted((float(np.load(f)["res"]), os.path.basename(f)) for f in glob.glob(os.path.join(R, "eig", "*.npz")))
print(f"residual over {len(res)} files: smallest {res[0][0]:.1e} ({res[0][1]}), largest {res[-1][0]:.1e} ({res[-1][1]})")
