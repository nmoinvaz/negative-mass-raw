"""Per job: exit, wall (the log's last 'wall N s'), each sector's time (the log's 'done in N s') and the peak working set
(the largest peak= of memory-sampler.log over the processes of that job, worker included). A job that was restarted has
its dead logs kept as <job>.died<N>.log; they are listed with their sector times. Run with the venv python, -X utf8, from
any directory. With job names as arguments only those are listed."""
import glob
import os
import re
import sys
from collections import defaultdict

R = os.path.dirname(os.path.abspath(__file__))
jobs = {}
for ln in open(os.path.join(R, "jobs.txt"), encoding="utf-8"):
    if ln.strip() and not ln.startswith("#"):
        j, script, a = ln.rstrip("\n").split("|", 2)
        jobs[j] = script.replace(".py", "") + " " + a.replace("%~dp0", "")
peak, free = defaultdict(float), []
for ln in open(os.path.join(R, "memory-sampler.log"), encoding="utf-8-sig"):
    m = re.search(r"peak=([\d,]+)MB cpu=\d+s (.*)$", ln)
    if m:
        a = m.group(2).strip()
        peak[a] = max(peak[a], float(m.group(1).replace(",", "")))
    m = re.search(r"free=([\d.]+)GB", ln)
    if m:
        free.append(float(m.group(1)))
print(f"free memory over the sampled time: min {min(free):.1f}, max {max(free):.1f} GiB, {len(free)} samples")
tot = 0
for job, args in jobs.items():
    if sys.argv[1:] and job not in sys.argv[1:]:
        continue
    ef = os.path.join(R, job + ".log.exit")
    if not os.path.exists(ef):
        print(f"{job:22s} no exit file yet")
        continue
    ex = open(ef).read().strip()
    log = open(os.path.join(R, job + ".log"), encoding="utf-8-sig").read()
    w = re.findall(r"wall (\d+) s$", log, re.M)
    sec = re.findall(r"sigma R = (\d+), m = ([\d.]+): done in (\d+) s", log)
    wall = int(w[0]) if w else -1
    tot += max(wall, 0)
    p = peak.get(args, float("nan"))
    print(f"{job:22s} exit {ex}  wall {wall:6d} s ({wall / 3600:6.2f} h)  peak {p:6.0f} MiB = {p / 1024:5.2f} GiB")
    for s, m, t in sec:
        print(f"    sigma R = {s}, m = {m:>4s}: {t} s")
    for d in sorted(glob.glob(os.path.join(R, job + ".died*.log"))):
        dl = open(d, encoding="utf-8-sig").read()
        ds = re.findall(r"sigma R = (\d+), m = ([\d.]+): done in (\d+) s", dl)
        print(f"    {os.path.basename(d)}: {len(ds)} sectors done before it died")
print(f"sum of wall times {tot} s = {tot / 3600:.2f} h")
