#!/usr/bin/env python3
"""Reads every mutate_<name>.log and done/mutate_<name>.rc of this folder and compares them with the frozen control table of
README.md: exit code 1, the line 'failed [...] of targets [...] -> FIRED', and failed == targets == the README's targets.
Prints one row per control (name, rc, wall seconds, rss MiB) and exits 1 on any mismatch."""
import os
import re
import sys

here = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(here, "README.md")).read()
rows = re.findall(r"^\| (\d+) \| `([^`]+)` \| .*? \| ([^|]+) \|$", txt, re.M)
bad = 0
print("| # | control | exit | failed checks (= its targets) | wall | rss MiB |")
print("|---|---|---|---|---|---|")
for num, name, tg in rows:
    targets = [t.strip() for t in tg.split(",")]
    log = open(os.path.join(here, "mutate_%s.log" % name)).read()
    rc = open(os.path.join(here, "done", "mutate_%s.rc" % name)).read().strip()
    m = re.search(r"control %s: failed (\[.*?\]) of targets (\[.*?\]) -> (\w+)" % re.escape(name), log)
    failed = eval(m.group(1)) if m else None
    tm = open(os.path.join(here, "mutate_%s.time" % name)).read().strip().splitlines()[-1]
    mt = re.match(r"([\d.]+) s wall, (\d+) KB", tm)
    ok = rc == "1" and m and m.group(3) == "FIRED" and failed == targets and eval(m.group(2)) == targets
    bad += 0 if ok else 1
    print("| %s | `%s` | %s | %s | %s s | %.0f |" % (num, name, rc, ", ".join(failed or []), mt.group(1), int(mt.group(2)) / 1024))
    if not ok:
        print("MISMATCH", name, rc, failed, targets)
print("%d controls, %d mismatches" % (len(rows), bad))
sys.exit(1 if bad else 0)
