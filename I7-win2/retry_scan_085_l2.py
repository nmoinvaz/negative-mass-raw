"""One retry of scan_085_l2 of issue 7, exactly as in the issue (TAG=_n100, pool of 2), then the comparison.

Runs scan_growing.py -1 0.85 2 100 1e-3 300 from phase2/nonradial, appending to scan_085_l2.log. It does not stop a
hung scan, the watcher does that by hand. When the scan finishes it copies the CSV here and compares its D with
diag_085_l2.jsonl at every g (the relative difference must be <= 1e-8) and prints the largest.
"""
import csv
import json
import math
import os
import shutil
import subprocess
import time

RAW = os.path.dirname(os.path.abspath(__file__))
NR = r"C:\Users\nathan\Source\negative-mass-i7\phase2\nonradial"
PY = r"C:\Users\nathan\Source\negative-mass-venv\Scripts\python.exe"
CSV = "scan_eps-1_w0.85_l2_n100.csv"


def now():
    return time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime())


def say(msg):
    with open(os.path.join(RAW, "retry.log"), "a", encoding="utf-8") as f:
        f.write(f"{now()} {msg}\n")


def compare(path):
    """(largest relative difference, its index, verdict) of the scan CSV's D against the diagnostic's"""
    ref = [json.loads(line) for line in open(os.path.join(RAW, "diag_085_l2.jsonl"))]
    rows = list(csv.DictReader(open(path)))
    worst, at = 0.0, None
    for a, b in zip(rows, ref):
        g, D = float(a["gamma"]), float(a["D"])
        rel = abs(D - b["D"]) / abs(b["D"]) if b["D"] != 0 else (0.0 if D == 0 else math.inf)
        if abs(g - b["g"]) > 1e-12 * b["g"]:
            return math.inf, b["i"], f"FAIL, grid mismatch {g!r} vs {b['g']!r}"
        if rel > worst:
            worst, at = rel, b["i"]
    ok = worst <= 1e-8 and len(rows) == len(ref)
    return worst, at, ("PASS" if ok else "FAIL") + f" against 1e-8 ({len(rows)} scan rows, {len(ref)} diagnostic rows)"


def selftest():
    """the comparison on the diagnostic's own values (must pass) and with one D scaled by 1 + 1e-6 (must fail)"""
    import tempfile
    ref = [json.loads(line) for line in open(os.path.join(RAW, "diag_085_l2.jsonl"))]
    for label, scale in (("exact copy", 1.0), ("--mutate: D[50] x (1 + 1e-6)", 1 + 1e-6)):
        p = os.path.join(tempfile.mkdtemp(), "t.csv")
        with open(p, "w") as f:
            f.write("gamma,D\n")
            for r in ref:
                f.write(f"{r['g']!r},{r['D'] * (scale if r['i'] == 50 else 1.0)!r}\n")
        print(label, "->", compare(p))


def main():
    open(os.path.join(RAW, "retry.pid"), "w").write(str(os.getpid()))
    env = dict(os.environ, TAG="_n100", PYTHONUNBUFFERED="1", OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1",
               MKL_NUM_THREADS="1")
    cmd = [PY, "-u", "scan_growing.py", "-1", "0.85", "2", "100", "1e-3", "300"]
    t0 = time.time()
    say("retry start " + " ".join(cmd[1:]) + " with TAG=_n100")
    with open(os.path.join(RAW, "scan_085_l2.log"), "ab") as log:
        log.write(f"=== {now()} scan_085_l2 retry: {' '.join(cmd[1:])}\n".encode())
        log.flush()
        rc = subprocess.run(cmd, cwd=NR, env=env, stdout=log, stderr=subprocess.STDOUT).returncode
    say(f"retry exit {rc} after {time.time() - t0:.0f} s")
    src = os.path.join(NR, CSV)
    if os.path.exists(src):
        shutil.copy2(src, RAW)
        worst, at, verdict = compare(os.path.join(RAW, CSV))
        say(f"compare: largest relative difference {worst:.3e} at i={at}, {verdict}")
    else:
        say("retry wrote no CSV")


if __name__ == "__main__":
    import sys
    selftest() if "--selftest" in sys.argv else main()
