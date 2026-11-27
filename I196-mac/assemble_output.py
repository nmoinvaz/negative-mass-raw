#!/usr/bin/env python3
"""assemble_output.py OUT: taylor_drift_output.txt from the runs of record (run_NN_C_checks, run_NN_ctl_*, run_NN_D_report) in this folder.
Line 1 names the folder and the checks' exit codes; line 2 is the raw repository's commit when assembled. Timings and load lines are kept as they are."""
import glob, os, re, subprocess, sys
D = os.path.dirname(os.path.abspath(__file__))
out = sys.argv[1]
def runs(tag):
    return sorted(glob.glob(os.path.join(D, f"run_*_{tag}.log")))
def body(path):
    return [x for x in open(path).read().splitlines() if not x.startswith("#")]
def rc(path):
    return open(path[:-4] + ".rc").read().strip()
head = subprocess.run(["git", "-C", D, "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
lines = [f"# taylor_drift_output.txt: the runs of record of #196 (raw folder negative-mass-raw/I196-mac, README first)",
         f"# raw repository at {head} when this file was assembled (the folder's last commit is later by this file's own push)", ""]
for p in runs("C_checks"):
    lines += [f"## checks ({os.path.basename(p)}, exit {rc(p)})"] + body(p) + [""]
ctl = sorted(glob.glob(os.path.join(D, "run_*_ctl_*.log")))
lines += ["## controls: each mutation run alone against its target check (exit 1 expected)"]
for p in ctl:
    b = [x for x in body(p) if x.startswith("CHECK") or x.startswith("SUMMARY")]
    lines += [f"-- {os.path.basename(p)[:-4]} (exit {rc(p)})"] + [x[:600] for x in b]
lines += [""]
for p in runs("D_report"):
    lines += [f"## report ({os.path.basename(p)}, exit {rc(p)})"] + body(p)
open(out, "w").write("\n".join(lines) + "\n")
print(f"wrote {out}: {len(lines)} lines")
