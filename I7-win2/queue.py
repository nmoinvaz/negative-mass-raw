"""Job queue of issue 7 on win2: runs the jobs in sequence from phase2/nonradial, one process at a time.

Each job appends to <job>.log here. A finished job is listed in queue_done.txt, so a restarted queue skips it.
The control gates the rest: it must print winding +1.0000 around the QNM and 0 displaced. Nothing here stops or
kills a process for its memory.
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import time

RAW = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\negative-mass-i7"
NR = os.path.join(WT, "phase2", "nonradial")
PY = r"C:\Users\nathan\Source\negative-mass-venv\Scripts\python.exe"
TAG = {"TAG": "_n100"}


JOBS = [
    ("control", ["control_winding2.py"], {}),
    ("scan_085_l3", ["scan_growing.py", "-1", "0.85", "3", "100", "1e-3", "2000"], TAG),
    ("scan_070_l2", ["scan_growing.py", "-1", "0.70", "2", "100", "1e-3", "300"], TAG),
    ("scan_070_l3", ["scan_growing.py", "-1", "0.70", "3", "100", "1e-3", "1000"], TAG),
    ("scan_085_l2", ["scan_growing.py", "-1", "0.85", "2", "100", "1e-3", "300"], TAG),
] + [(f"wind_{w.replace('.', '')}_l{l}", ["winding2.py", "-1", w, str(l), "0.1", "2.0", "2.5"], {})
     for w in ("0.70", "0.85") for l in (2, 3)
] + [(f"conv_{w.replace('.', '')}_l{l}", ["convergence.py", str(l), w], {})
     for w in ("0.70", "0.85") for l in (2, 3)]

# files copied from the worktree into this folder after every job
PATTERNS = ["scan_*_n100.csv", "winding2_cache_eps-1_w0.7_*.pkl", "winding2_cache_eps-1_w0.85_*.pkl"]


def now():
    return time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())


def say(msg):
    with open(os.path.join(RAW, "queue.log"), "a", encoding="utf-8") as f:
        f.write(f"{now()} {msg}\n")


def sync():
    for pat in PATTERNS:
        for p in glob.glob(os.path.join(NR, pat)):
            shutil.copy2(p, RAW)


def done():
    p = os.path.join(RAW, "queue_done.txt")
    return set(open(p).read().split()) if os.path.exists(p) else set()


def gate(txt):
    return bool(re.search(r"around QNM: winding = \+1\.0000", txt)
                and re.search(r"displaced: winding = [+-]?0\.0000", txt))


def main():
    open(os.path.join(RAW, "queue.pid"), "w").write(str(os.getpid()))
    say(f"queue start pid {os.getpid()}, {len(JOBS)} jobs")
    for name, args, extra in JOBS:
        if name in done():
            say(f"{name}: skipped, already done")
            continue
        env = dict(os.environ, PYTHONUNBUFFERED="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
                   MKL_NUM_THREADS="1", **extra)
        logp = os.path.join(RAW, f"{name}.log")
        start = os.path.getsize(logp) if os.path.exists(logp) else 0
        cmd = [PY, "-u"] + args
        t0 = time.time()
        say(f"{name}: start {' '.join(cmd[1:])}" + (f" with {extra}" if extra else ""))
        with open(logp, "ab") as log:
            log.write(f"=== {now()} {name}: {' '.join(cmd[1:])}\n".encode())
            log.flush()
            rc = subprocess.run(cmd, cwd=NR, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
        sync()
        say(f"{name}: exit {rc} after {time.time() - t0:.0f} s")
        if name == "control":
            with open(logp, "rb") as f:
                f.seek(start)
                ok = rc == 0 and gate(f.read().decode(errors="replace"))
            if not ok:
                open(os.path.join(RAW, "STOPPED_control.txt"), "w").write(
                    f"{now()} the control did not print winding +1.0000 around the QNM and 0 displaced (exit {rc})\n")
                say("control failed, queue stopped")
                sys.exit(3)
            say("control passed: winding +1.0000 around the QNM, 0 displaced")
        with open(os.path.join(RAW, "queue_done.txt"), "a") as f:
            f.write(name + "\n")
    say("queue finished")


if __name__ == "__main__":
    main()
