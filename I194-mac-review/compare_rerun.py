#!/usr/bin/env python3
"""Compares the review's rerun of run_13_final with taylor_radial_output.txt after removing wall times and loads."""
import re, sys
a = open(sys.argv[1]).read().splitlines()
b = [l for l in open(sys.argv[2]).read().splitlines() if not l.startswith("rc=")]
TIME = re.compile(r'("(wall|secs|t|time|elapsed|t_[a-z_]+)":\s*[-0-9.e+]+)|(\b[0-9]+(\.[0-9]+)?\s*s\b)|(load averages?[^;)]*)|(\b\d+(\.\d+)? (min|h)\b)')
norm = lambda l: TIME.sub("T", l)  # noqa: E731
print(f"lines: record {len(a)}, rerun {len(b)}")
diff = [i + 1 for i, (x, y) in enumerate(zip(a, b)) if norm(x) != norm(y)]
for i in diff[:10]:
    tx, ty = norm(a[i - 1]).split(), norm(b[i - 1]).split()
    j = next((k for k in range(min(len(tx), len(ty))) if tx[k] != ty[k]), 0)
    print(f"line {i}: record '{' '.join(tx[j:j + 3])[:150]}' rerun '{' '.join(ty[j:j + 3])[:150]}'")
print(f"{len(diff)} of {len(a)} lines differ after removing wall times and loads")
sys.exit(1 if diff or len(a) != len(b) else 0)
