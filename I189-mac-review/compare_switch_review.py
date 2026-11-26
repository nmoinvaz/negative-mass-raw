#!/usr/bin/env python3
"""compare_switch_review.py: the feature-on reruns (this folder) against the coordinator's feature-off reruns of #187
(I187-mac-review), timings and load removed. Row and header lines must be identical; CHECK lines are reported."""
import re
import sys
T = re.compile(r"\d+(\.\d+)?\s?s(?=[\s;),\]]|$)")
L = re.compile(r"load \d+(\.\d+)?")
NUM = re.compile(r"[-+]?\d+(\.\d+)?(e[-+]?\d+)?")


def norm(p):
    return [L.sub("load L", T.sub("T", ln.rstrip())) for ln in open(p) if not ln.startswith("#")]


bad = 0
for n in ("rows_l2_2", "rows_l4", "rows_l6_cap6", "default_mode"):
    on, off = norm(f"rerun_{n}.log"), norm(f"../I187-mac-review/rerun_{n.replace('_2', '')}.log")
    rc = (open(f"rerun_{n}.rc").read().strip(), open(f"../I187-mac-review/rerun_{n.replace('_2', '')}.rc").read().strip())
    rows_on = [x for x in on if not x.startswith(("CHECK", "SUMMARY"))]
    rows_off = [x for x in off if not x.startswith(("CHECK", "SUMMARY"))]
    rows_ok = rows_on == rows_off
    chk_on = [x for x in on if x.startswith(("CHECK", "SUMMARY"))]
    chk_off = [x for x in off if x.startswith(("CHECK", "SUMMARY"))]
    ntok, ndiff, verdict_same = 0, 0, True
    for a, b in zip(chk_on, chk_off):
        ta, tb = a.split(), b.split()
        verdict_same &= ta[:3] == tb[:3]
        for u, v in zip(ta, tb):
            ntok += 1
            ndiff += u != v
    ok = rows_ok and rc[0] == rc[1] and len(chk_on) == len(chk_off) and verdict_same
    bad += not ok
    print(f"{n}: exit {rc[0]} (on) vs {rc[1]} (off); {len(rows_on)} row/header lines identical: {rows_ok}; "
          f"{len(chk_on)} CHECK/SUMMARY lines, verdicts equal: {verdict_same}, {ndiff} of {ntok} tokens differ")
sys.exit(1 if bad else 0)
