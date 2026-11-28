"""assemble_output.py OUT [CODEHASH]: order8_output.txt of the code repository from the logs of the runs of record, in order, and the summaries of the control runs"""
import os
import re
import subprocess
import sys

d = os.path.dirname(os.path.abspath(__file__))
runs = [r for r in ("run_01_sym_struct_cache", "run_02_evals_G1", "run_03_evals_G2", "run_04_evals_B", "run_05_values_remainder", "run_06a_pslq_F1_F6_X1", "run_06b_pslq_X2_X3",
                    "run_06c_pslq_XF", "run_06d_pslq_XF_H1e10", "run_07_closed6")
        if os.path.exists(f"{d}/{r}.rc")]
code = sys.argv[2] if len(sys.argv) > 2 else "CODEHASH"
out = ["# Output of order8.py of record: negative-mass-raw/I282-rpi5/" + " ".join(runs) + ", concatenated in this order, then the summaries of the control runs. "
       "See omega6.md and the raw README.",
       f"# Code: order8.py of wip/i282-omega6 at {code} (see the raw README, Results of record).", ""]
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
for pre, decl in (("ctl_chk", "declared_chk.json"), ("ctl_t1", "declared_t1.json"), ("ctl_t2", "declared_t2.json"), ("ctl_t2b", "declared_t2b.json"), ("ctl_t2bxf", "declared_t2bxf.json"), ("ctl_st", "declared_st.json")):
    if os.path.exists(f"{d}/{decl}"):
        s = subprocess.run([sys.executable, f"{d}/ctl_summary.py", pre, "--declared", f"{d}/{decl}"], capture_output=True, text=True).stdout
        out.append(f"=== control runs {pre}_* against {decl}")
        out.extend(s.rstrip("\n").split("\n"))
        out.append("")
open(sys.argv[1], "w").write("\n".join(out) + "\n")
print(out[len(out) - 1 if not out[-1] else -2][:200])
