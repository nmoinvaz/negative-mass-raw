#!/usr/bin/env python3
"""ind202: TS13 Table I read from arXiv:1309.2058's TeX source against #202's PRINTED and growth.csv (criteria in README.md)."""
import argparse
import csv
import re
import subprocess
import sys
from decimal import ROUND_HALF_EVEN, Decimal

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["digit"])
O = ap.parse_args()
R = []


def check(n, ok, d):
    R.append((n, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {n}: {d}", flush=True)


tex = open("ts13_src/table_lines_680-705.tex").read()
mine = {int(m.group(1)): m.group(2) for m in re.finditer(r"^\s*~*(\d+)&\$~*(-[0-9.]+)", tex, re.M)}
if O.mutate == "digit":
    mine[9] = mine[9][:-1] + "2"
src = subprocess.run(["git", "-C", "/Users/nathan/Source/negative-mass-r202", "show", "HEAD:notes/wormhole_largeD/ts13_digits.py"],
                     capture_output=True, text=True).stdout
blk = src[src.index("PRINTED = {"):src.index("}", src.index("PRINTED = {")) + 1]
printed = {int(k): v for k, v in re.findall(r"(\d+): \"(-[0-9.]+)\"", blk)}
diff1 = [D for D in range(4, 12) if mine.get(D) != printed.get(D)]
check("K1", not diff1 and all(D in mine for D in range(4, 12)),
      f"{len(mine)} entries read from the TeX ({sorted(mine)}); D = 4..11 differing from PRINTED: {diff1 or 'none'}")
main_csv = subprocess.run(["git", "-C", "/Users/nathan/Source/negative-mass", "show", "main:notes/wormhole_largeD/growth.csv"],
                          capture_output=True, text=True).stdout
rows = {int(r["D"]): r["W2a2"] for r in csv.DictReader(main_csv.splitlines())}
diff2, notes = [], []
for D in range(4, 12):
    want = str((-Decimal(mine[D])).quantize(Decimal("1e-12"), rounding=ROUND_HALF_EVEN))
    if rows[D] != want:
        diff2.append(D)
    notes.append(f"D={D} TS13 {mine[D]} -> {want}, csv {rows[D]}")
check("K2", not diff2, "; ".join(notes) + f"; differing: {diff2 or 'none'}")
bad = [n for n, ok in R if not ok]
print(f"\n{len(R)} criteria, {len(R) - len(bad)} pass; failed: {bad}")
sys.exit(1 if bad else 0)
