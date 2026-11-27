#!/usr/bin/env python3
"""verify_old_rows.py: ts13_digits.OLD_ROWS equals growth.csv's D = 4 ... 11 rows (all three of them, the W2a2 field) at 4bced01 and at
613e866, and those rows carry the source TS13 Table I. Exit 1 otherwise. Run from anywhere."""
import csv
import os
import subprocess
import sys

ND = os.path.expanduser("~/Source/negative-mass-i221/notes/wormhole_largeD")
sys.path.insert(0, ND)
import ts13_digits as t  # noqa: E402

bad = 0
for rev in ("4bced01", "613e866"):
    text = subprocess.run(["git", "-C", ND, "show", f"{rev}:notes/wormhole_largeD/growth.csv"], capture_output=True, text=True,
                          check=True).stdout
    rows = {int(r[0]): (r[1], r[2]) for r in list(csv.reader(text.splitlines()))[1:]}
    ok = all(rows[D] == (t.OLD_ROWS[D], "TS13 Table I") for D in t.D_CSV) and sorted(t.OLD_ROWS) == list(t.D_CSV)
    bad += not ok
    print(f"{rev}: OLD_ROWS equals the D = 4..11 rows and their source label: {ok}")
sys.exit(1 if bad else 0)
