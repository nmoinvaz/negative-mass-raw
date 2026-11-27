#!/usr/bin/env python3
"""compare_printed_digits.py DIR declared_printed_digits.json: DIR holds none.log and bump_D.log from printed_digits.py (+ 'exit N');
each log's cells that are not 'unchanged' must be exactly the declared ones. Exit 1 otherwise."""
import json
import os
import re
import sys

dec = json.load(open(sys.argv[2]))
bad = 0
for name, want in dec.items():
    if name.startswith("_"):
        continue
    f = os.path.join(sys.argv[1], name.replace(":", "_") + ".log")
    lines = open(f).read().splitlines()
    got = []
    for l in lines:
        m = re.match(r"^\s+(\S+)\s+(\d+)\s+(.+?)\s{2,}.*\s(NEW DIFFERS|printed != old)\s*$", l)
        if m:
            got.append(f"{m.group(1)}/{m.group(2)}/{m.group(3)}")
    code = int(lines[-1].split()[1])
    ok = sorted(got) == sorted(want) and code == (1 if want else 0)
    bad += not ok
    print(f"{name:<8s} declared {len(want)} got {len(got)} exit {code}  {'on target' if ok else 'OFF TARGET'}  {got}")
print(f"{len(dec) - 1} runs, {len(dec) - 1 - bad} on target")
sys.exit(1 if bad else 0)
