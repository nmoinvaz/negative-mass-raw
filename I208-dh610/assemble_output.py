"""assemble_output.py: order5_output.txt of the code repository from the logs of the runs of record, in order"""
import re, sys
runs = ["run_01_sym", "run_02_evals_pslq_remainder", "run_03_closedform", "run_04_reduce5_a5"]
out = ["# Output of order5.py of record: negative-mass-raw/I208-dh610/run_01 … run_04, four processes, concatenated in this order. See omega3.md and the raw README.",
       "# Code: worktree commit 57710d3 for run_01, run_02 (order5.py sha256 2cd0cbea…); cd37886 for run_03 (adds part closedform); 92d8c8b for run_04 (adds parts reduce5, a5). Exit statuses 0, 1, 0, 0 (run_02: X1 as worded).", ""]
npass = nfail = 0
failed = []
for r in runs:
    rc = open(f"{r}.rc").read().strip()
    t = open(f"{r}.time").read()
    wall = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", t).group(1)
    rss = re.search(r"Maximum resident set size \(kbytes\): (\d+)", t).group(1)
    out.append(f"=== {r}: exit {rc}, wall {wall}, peak RSS {rss} kB")
    log = open(f"{r}.log").read().rstrip("\n").split("\n")
    out.extend(log)
    out.append("")
    for line in log:
        m = re.match(r"(PASS|FAIL)    (\S+):", line)
        if m:
            npass += m.group(1) == "PASS"
            nfail += m.group(1) == "FAIL"
            if m.group(1) == "FAIL":
                failed.append(m.group(2))
out.append(f"=== totals: {npass} PASS, {nfail} FAIL of {npass + nfail} checks; FAIL: {' '.join(failed)}")
open(sys.argv[1], "w").write("\n".join(out) + "\n")
print(out[-1])
