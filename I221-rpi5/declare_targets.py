#!/usr/bin/env python3
"""declare_targets.py SUMMARY OUT.json: the declared targets of the runs of record, read from the development run's summary
(run_mutations.sh's lines 'mutation  checks (exit N)'). Written once, after dev_03 and before any run of record (amendment A1)."""
import json
import re
import sys

dec = {"_note": "Declared after dev_03 (dev_03_summary.log) and before the runs of record. A mutation is on target when exactly these "
                "checks fail. 'none' (no mutation): no check fails, exit 0."}
for line in open(sys.argv[1]):
    m = re.match(r"^(\S+)\s+(.*?)\s+\(exit (\d+)\)\s*$", line)
    if m:
        dec[m.group(1)] = [] if m.group(2) == "none" else m.group(2).split()
json.dump(dec, open(sys.argv[2], "w"), indent=1)
print(len(dec) - 1, "mutations declared")
