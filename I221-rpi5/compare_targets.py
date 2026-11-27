#!/usr/bin/env python3
"""compare_targets.py SUMMARY declared_targets.json: SUMMARY lines are 'mutation  checks (exit N)' as run_mutations.sh prints
them; prints each mutation's verdict (on target, silent, off target) and exits 1 unless every mutation is on target."""
import json
import re
import sys

dec = json.load(open(sys.argv[2]))
bad = 0
seen = set()
for line in open(sys.argv[1]):
    m = re.match(r"^(\S+)\s+(.*?)\s+\(exit (\d+)\)\s*$", line)
    if not m:
        continue
    name, got, code = m.group(1), m.group(2), int(m.group(3))
    got = [] if got == "none" else got.split()
    want = dec[name]
    seen.add(name)
    ok = got == want and code == (1 if want else 0)
    verdict = "on target" if ok else ("SILENT" if not got and want else "OFF TARGET")
    bad += not ok
    print(f"{name:<16s} declared {' '.join(want) or 'none':<24s} got {' '.join(got) or 'none':<24s} exit {code}  {verdict}")
missing = set(dec) - seen - {"_note"}
print(f"{len(seen)} mutations run, {len(seen) - bad} on target, {bad} not; declared but not run: {sorted(missing)}")
sys.exit(1 if bad or missing else 0)
