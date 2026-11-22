#!/usr/bin/env python3
"""Compares the frozen control table of this folder's README.md with CONTROLS in he_type3.py: names and target lists, in order.
Run from the negative-mass worktree: python3 <raw>/I102-rpi5/check_controls.py"""
import os
import re
import sys

sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i102/notes/warp"))
import he_type3 as H  # noqa: E402

here = os.path.dirname(os.path.abspath(__file__))
txt = open(os.path.join(here, "README.md")).read()
rows = re.findall(r"^\| (\d+) \| `([^`]+)` \| .*? \| ([^|]+) \|$", txt, re.M)
table = [(nm, [t.strip() for t in tg.split(",")]) for _, nm, tg in rows]
code = [(nm, list(v[0])) for nm, v in H.CONTROLS.items()]
print("README rows %d, CONTROLS %d" % (len(table), len(code)))
bad = [(a, b) for a, b in zip(table, code) if a != b]
if bad or len(table) != len(code):
    print("MISMATCH", bad)
    sys.exit(1)
print("controls match the frozen table")
