#!/usr/bin/env python3
"""ctl_run.py JOBS [WORKERS]: runs the lines "name|command" of the file JOBS, at most WORKERS (default 2) at a time, each from $WT with devrun.sh
(RAW/name.{log,err,rc}, never overwritten; a job whose .rc exists is skipped, so a restart resumes). env: PY, WT. Writes RAW/JOBS.log (start and end lines)."""
import concurrent.futures
import datetime
import os
import subprocess
import sys

raw = os.path.dirname(os.path.abspath(__file__))
jobs_path = os.path.abspath(sys.argv[1])
workers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
wt = os.environ["WT"]
env = dict(os.environ, OMP_NUM_THREADS="1")
jobs = [ln.rstrip("\n").split("|", 1) for ln in open(jobs_path) if ln.strip() and not ln.startswith("#")]
log = open(jobs_path + ".log", "a")


def now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def run(job):
    name, cmd = job
    if os.path.exists(os.path.join(raw, name + ".rc")):
        return name, "skipped"
    log.write(f"{now()} start {name}\n"); log.flush()
    subprocess.run([os.path.join(raw, "devrun.sh"), name, "nice", "-n", "10", "bash", "-c", cmd], cwd=wt, env=env)
    rc = open(os.path.join(raw, name + ".rc")).read().strip() if os.path.exists(os.path.join(raw, name + ".rc")) else "?"
    log.write(f"{now()} end {name} rc {rc}\n"); log.flush()
    return name, rc


with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
    for name, rc in ex.map(run, jobs):
        print(name, rc, flush=True)
