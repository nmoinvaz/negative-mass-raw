#!/usr/bin/env python3
"""Assembles phase2/nonradial/taylor_polar_output.txt from run_01..run_04 of this folder: the logs of the runs of record,
unchanged, each under a header; the resource lines are the `/usr/bin/time -l` lines of the runs' .err files."""
import json, os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
rawc = subprocess.run(["git", "-C", D, "log", "-1", "--format=%h", "--", "."], capture_output=True, text=True).stdout.strip()


def res(name):
    t = open(os.path.join(D, name)).read()
    real = re.search(r"([\d.]+)\s+real", t)
    rss = re.search(r"(\d+)\s+maximum resident set size", t)
    return f"wall {real.group(1)} s, peak resident {int(rss.group(1)) / 2**20:.0f} MiB (reported only)" if real and rss else "no time -l lines"


o = []
o.append("# taylor_polar_output.txt: the runs of record of #186, assembled by negative-mass-raw/I186-mac/assemble_output.py")
o.append(f"# raw folder I186-mac, last commit touching it when assembled: {rawc}")
o.append("# machine: Apple M5 Mac (10 cores, 32 GB), shared with other sessions; one process at a time, nice 10; the crate is single-threaded;")
o.append("# the load average is the first line of each run's log below")
o.append("")
for title, log, err in (("run_01: the scipy path, base variant (convergence.py's), one evaluation per point, one thread", "run_01_scipy_timing.log", "run_01_scipy_timing.err"),):
    o.append("=" * 120); o.append(title); o.append(res(err)); o.append("=" * 120)
    o.append(open(os.path.join(D, log)).readline().rstrip())
    for line in open(os.path.join(D, "scipy_timing.jsonl")):
        d = json.loads(line)
        o.append(f"l = {d['l']}  gamma = {d['gamma']:<8g} D = {d['D']:+.10e}  wall {d['wall']:8.1f} s  cpu {d['cpu']:8.1f} s  load1 {d['load1']:.2f}  {d['status']}")
    o.append("")
o.append("=" * 120); o.append("run_02: every check (taylor_polar.py --scipy-file=scipy_timing.jsonl)"); o.append(res("run_02_checks.err")); o.append("=" * 120)
o.append(open(os.path.join(D, "run_02_checks.log")).read().rstrip()); o.append("")
o.append("=" * 120); o.append("run_03: every control (taylor_polar.py --mutate=NAME; each must exit 1)"); o.append("=" * 120)
o.append(open(os.path.join(D, "run_03_controls.log")).read().rstrip()); o.append("")
o.append("=" * 120); o.append("run_04: the one-time costs (the star's Newton shooting; the J table of one l, in double-double whatever the lane)"); o.append(res("run_04_setup.err")); o.append("=" * 120)
o.append(open(os.path.join(D, "run_04_setup.log")).read().rstrip())
open(OUT, "w").write("\n".join(o) + "\n")
print(OUT, len(o), "lines")
