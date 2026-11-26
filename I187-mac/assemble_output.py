#!/usr/bin/env python3
"""Assembles phase2/nonradial/taylor_rows_output.txt from the runs of record `run_*` of this folder: each log unchanged under a
header; the resource lines are the `/usr/bin/time -l` lines of the runs' .err files and the exit code is the run's .rc.
Usage: python3 assemble_output.py OUT"""
import os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1]
rawc = subprocess.run(["git", "-C", D, "log", "-1", "--format=%h", "--", "."], capture_output=True, text=True).stdout.strip()


def res(base):
    try:
        t = open(os.path.join(D, base + ".err")).read()
    except FileNotFoundError:
        return "no .err file"
    real = re.search(r"([\d.]+)\s+real", t)
    rss = re.search(r"(\d+)\s+maximum resident set size", t)
    rc = open(os.path.join(D, base + ".rc")).read().strip() if os.path.exists(os.path.join(D, base + ".rc")) else "?"
    return (f"exit {rc}, wall {real.group(1)} s, peak resident {int(rss.group(1)) / 2**20:.0f} MiB (reported only)" if real and rss
            else f"exit {rc}, no time -l lines")


RUNS = [l.split("|") for l in open(os.path.join(D, "runs.txt")).read().splitlines() if l.strip() and not l.startswith("#")]
o = ["# taylor_rows_output.txt: the runs of record of #187, assembled by negative-mass-raw/I187-mac/assemble_output.py",
     f"# raw folder I187-mac, last commit touching it when assembled: {rawc}",
     "# machine: Apple M5 Mac (10 cores, 32 GB), shared with other sessions; one process at a time, nice 10; the crate is single-threaded;",
     "# the load average is on the first lines of each run's log below", ""]
for base, title in RUNS:
    o += ["=" * 120, f"{base}: {title}", res(base), "=" * 120]
    o.append(open(os.path.join(D, base + ".log")).read().rstrip())
    o.append("")
open(OUT, "w").write("\n".join(o) + "\n")
print(OUT, len(o), "lines")
