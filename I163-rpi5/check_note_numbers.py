#!/usr/bin/env python3
"""Checks that the numbers the #163 part of notes/ellis_efold.md quotes are in notes/ellis_efold_output.txt (the final run).
usage: check_note_numbers.py <path to notes dir>. Exit 1 if a quoted number is not found where it must be."""
import re, sys
d = sys.argv[1]
out = open(f"{d}/ellis_efold_output.txt").read()
note = open(f"{d}/ellis_efold.md").read()
part = note[note.index("# #163:"):]
bad = []

def need(label, ok):
    print(("ok   " if ok else "FAIL ") + label)
    if not ok:
        bad.append(label)

# second-row table: T, printed, diff per gamma_1
for m in re.finditer(r"Table I, second row: gamma_1 = +([0-9.]+)  T = ([0-9.]+)  printed ([0-9.]+)  diff ([+-][0-9.]+)", out):
    g, T, pr, df = m.groups()
    need(f"row 2 gamma_1 = {g}: '{float(g):.1f} |' ... {T} | {pr} | {df}", re.search(rf"\| {float(g):.1f} \| [0-9.]+ \| {T} \| {pr} \| {re.escape(df)} \|", part) is not None)
# b of the table
for m in re.finditer(r"gamma_1 = +([0-9.]+): b = beta-hat = ([0-9.]+)  ", out):
    g, b = m.groups()
    if float(g) >= 2.5:
        need(f"row 2 b at {g}", f"| {float(g):.1f} | {float(b):.9f} |" in part)
# limit equation
m = re.search(r"limit equation: 1/beta-hat = ([0-9.]+) \(A\)", out)
need("1/beta-hat " + m.group(1), m.group(1) in part)
for m in re.finditer(r"limit equation: A beta-hat = ([0-9.]+), B = ([0-9.]+)", out):
    need("beta-hat A " + m.group(1), m.group(1) in part)
need("LE5(a) gap -0.001649", "-0.001649" in out and "−0.001649" in part)
# LE6
for g in (10, 20, 40, 80, 160):
    m = re.search(rf"gamma_1 = +{g}: beta-hat = ([0-9.]+)  \(limit ([0-9.]+)\)  T = ([0-9.]+)", out)
    need(f"beta-hat({g}) = {float(m.group(1)):.9f}", f"{float(m.group(1)):.9f}" in part)
    need(f"T({g}) = {float(m.group(3)):.6f}", f"{float(m.group(3)):.6f}" in part)
m = re.search(r"order p of the gap at each doubling ([0-9., ]+);", out)
for v in m.group(1).split(", "):
    need("order " + v, v in part)
# error bars and worst values
need("worst |T - printed| 0.000489", "worst |T - printed| = 0.000489" in out and "0.000489" in part)
need("G1b worst 3.61e-12", "worst rel 3.61e-12" in out and "3.6e-12" in part)
need("R3 4.60e-15", "worst rel 4.60e-15" in out and "4.6e-15" in part)
need("N1a 8.05e-16", "8.05e-16" in out and "8e-16" in part)
need("N1 premise 8.67e-16", "8.67e-16" in out and "8.7e-16" in part)
need("R2 worst 2.62e-14 / 2.28e-13 / 6.29e-06", all(s in out for s in ("2.62e-14", "2.28e-13", "6.29e-06")) and all(s in part for s in ("2.6e-14", "2.3e-13", "6.29e-6")))
need("P-C2b worst 1.36e-11", "1.36e-11" in out and "1.4e-11" in part)
need("P-C2 errors", all(s in out for s in ("2.29e-11", "9.31e-08", "4.75e+06")) and all(s in part for s in ("2.3e-11", "9.3e-8", "4.8e6")))
need("N3b 1.7e-03 .. 1.7e-11", "1.7e-03, 1.7e-05, 1.7e-07, 1.7e-09, 1.7e-11" in out and "1.7e-3" in part and "1.7e-11" in part)
need("checks line", "checks: 100 run, failed ids: ['P-C2', 'LE5']" in out and "100 checks" in part)
sys.exit(1 if bad else 0)
