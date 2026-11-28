"""assemble_output.py OUT: order7_output.txt of the code repository from the logs of the runs of record, in order, and the summaries of the control runs"""
import json
import os
import re
import subprocess
import sys

d = os.path.dirname(os.path.abspath(__file__))
runs = [r for r in ("run_01_sym_xsym_cache_exch7", "run_02_evals_G1", "run_03_evals_G2", "run_04_evals_B", "run_05_values_remainder", "run_06a_pslq_Q1_Q2_Q3_Q4", "run_06b_pslq_Q5_Q6", "run_06c_pslq_Q7_Q8_Q9", "run_07_reduce7", "run_08_euler7", "run_09_weights7")
        if os.path.exists(f"{d}/{r}.rc")]
out = ["# Output of order7.py of record: negative-mass-raw/I263-rpi5/" + " ".join(runs) + ", concatenated in this order, then the summaries of the control runs. "
       "See omega5.md and the raw README.",
       "# Code: order7.py of wip/i263-omega5 at 7d93fc3 for run_02, run_03; f7f294a for run_01, run_04; 2e70c66 for run_05, run_06a, run_06b; 4f6f020 for run_06c; be7b9cb for run_07; 7c21d83 for run_08, run_09; the controls ctl_* at 2e70c66 … 996c69f. The nominal path of the evaluations (cc, PanelK, omega_chain, run_B, the grids) is the same in all of them; see the raw README, Results of record.", ""]
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
for pre, decl in (("ctl_t1", "declared_t1.json"), ("ctl_t2", "declared_t2.json"), ("ctl_t2b", "declared_t2b.json"), ("ctl_ex", "declared_ex.json"), ("ctl_chk", "declared_chk.json"), ("ctl_red", "declared_red.json")):
    if os.path.exists(f"{d}/{decl}"):
        s = subprocess.run([sys.executable, f"{d}/ctl_summary.py", pre, "--declared", f"{d}/{decl}"], capture_output=True, text=True).stdout
        out.append(f"=== control runs {pre}_* against {decl}")
        out.extend(s.rstrip("\n").split("\n"))
        out.append("")
open(sys.argv[1], "w").write("\n".join(out) + "\n")
print(out[len(out) - 1 if not out[-1] else -2][:200])
