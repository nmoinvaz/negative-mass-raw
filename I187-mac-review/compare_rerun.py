#!/usr/bin/env python3
"""compare_rerun.py: each rerun log against the runner's log of the same run, timings and load removed"""
import re
import sys
pairs = [("rows_l2", "run_02_rows_l2"), ("rows_l3", "run_03_rows_l3"), ("rows_l4", "run_04_rows_l4"),
         ("rows_l5_cap5", "run_05_rows_l5_cap5"), ("rows_l6_cap6", "run_06_rows_l6_cap6"),
         ("default_mode", "run_18_default_mode_rerun")]
T = re.compile(r"\d+(\.\d+)?\s?s(?=[\s;),\]]|$)")
L = re.compile(r"load \d+(\.\d+)?")


def norm(p):
    return [L.sub("load L", T.sub("T", ln.rstrip())) for ln in open(p) if not ln.startswith("#")]


bad = 0
for a, b in pairs:
    x, y = norm(f"rerun_{a}.log"), norm(f"../I187-mac/{b}.log")
    rc = (open(f"rerun_{a}.rc").read().strip(), open(f"../I187-mac/{b}.rc").read().strip())
    ok = x == y and rc[0] == rc[1]
    bad += not ok
    print(f"{a} vs {b}: {len(x)} lines, identical after removing timings and load: {x == y}; exit {rc[0]} vs {rc[1]}")
sys.exit(1 if bad else 0)
