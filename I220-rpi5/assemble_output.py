"""assemble_output.py OUT: order6_output.txt of the code repository from the logs of the runs of record, in order, and the summaries of the control runs"""
import json
import os
import re
import subprocess
import sys

d = os.path.dirname(os.path.abspath(__file__))
runs = [r for r in ("run_01_sym_exch6", "run_02_evals_G1", "run_03_evals_G2", "run_04_evals_B", "run_05_values_pslq_remainder", "run_06_reduce6")
        if os.path.exists(f"{d}/{r}.rc")]
out = ["# Output of order6.py of record: negative-mass-raw/I220-rpi5/" + " ".join(runs) + ", concatenated in this order, then the summaries of the control runs. "
       "See omega4.md and the raw README.",
       "# Code: worktree commit e7f8c10 for run_01 … run_05 (order6.py sha256 16aa151f…); 7acb933 for run_06 and the controls ctl_* (adds the part reduce6 and the rd_* mutations; the other parts are unchanged).", ""]
npass = nfail = 0
failed = []
for r in runs:
    rc = open(f"{d}/{r}.rc").read().strip()
    t = open(f"{d}/{r}.time").read()
    wall = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", t).group(1)
    rss = re.search(r"Maximum resident set size \(kbytes\): (\d+)", t).group(1)
    env = open(f"{d}/{r}.env").read().split("\n")
    out.append(f"=== {r}: exit {rc}, wall {wall}, peak RSS {rss} kB, started {env[0]}")
    log = open(f"{d}/{r}.log").read().rstrip("\n").split("\n")
    out.extend(log)
    out.append("")
    for line in log:
        m = re.match(r"(PASS|FAIL)    (\S+):", line)
        if m:
            npass += m.group(1) == "PASS"
            nfail += m.group(1) == "FAIL"
            if m.group(1) == "FAIL":
                failed.append(m.group(2))
out.append(f"=== totals of the runs of record: {npass} PASS, {nfail} FAIL of {npass + nfail} checks; FAIL: {' '.join(failed) or 'none'}")
out.append("")
for pre, decl in (("ctl_t1", "declared_t1.json"), ("ctl_t2", "declared_t2.json"), ("ctl_ex", "declared_ex.json"), ("ctl_red", "declared_red.json")):
    if os.path.exists(f"{d}/{decl}"):
        s = subprocess.run([sys.executable, f"{d}/ctl_summary.py", pre, "--declared", f"{d}/{decl}"], capture_output=True, text=True).stdout
        out.append(f"=== control runs {pre}_* against {decl}")
        out.extend(s.rstrip("\n").split("\n"))
        out.append("")
open(sys.argv[1], "w").write("\n".join(out) + "\n")
print(out[len(out) - 1 if not out[-1] else -2][:200])
