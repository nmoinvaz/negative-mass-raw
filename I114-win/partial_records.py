"""Usage: partial_records.py <partial file> [first_new_line]. Counts the records of a convergence partial file by kind
(result rows, start, done, capped, died) and prints the json records after line first_new_line (default 0, 1-based
count of the lines already there), which for a resumed file are the evaluations the run added."""
import json
import sys

path = sys.argv[1]
skip = int(sys.argv[2]) if len(sys.argv) > 2 else 0
kinds = {}
new = []
for i, line in enumerate(open(path, encoding="utf-8"), 1):
    r = json.loads(line)
    k = "result" if isinstance(r, list) else next(k for k in r if k in ("start", "done", "capped", "died"))
    kinds[k] = kinds.get(k, 0) + 1
    if i > skip:
        new.append(line.rstrip())
print(path, kinds)
for line in new:
    print("  ", line)
