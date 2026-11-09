#!/usr/bin/env python3
"""Tabulates the lowest sigma^2 roots of #9's lowscan.py logs at the 16, 80 and 160 point grids, row by row (matched by
N), and marks where the 16-point row lists a different number of roots or a different lowest root from the 160-point one.
    python roots_table.py [dir]"""
import re
import sys
import os

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))


def rows(path):
    out = {}
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        m = re.match(r"eps=([+-]\d) N=([\d.]+) w=([\d.]+) .*sigma2=\[([^\]]*)\]", line)
        if m:
            out[m.group(2)] = (m.group(3), [x for x in re.findall(r"'([^']*)'", m.group(4))])
    return out


for fam, tag in (("eps=+1", "p"), ("eps=-1", "m")):
    g = {n: rows(os.path.join(d, f"low_{tag}{n}.log")) for n in (16, 80, 160)}
    print(f"{fam}: lowest roots by sigma^2 grid (npos = nneg = 16, 80, 160); '?' = unconfirmed root")
    print(f"{'N':>8} {'w':>9}  {'16 points':<46} {'80 points':<46} {'160 points':<46} 16 vs 160")
    for N in g[160]:
        r = [g[n].get(N, (None, ["missing"]))[1] for n in (16, 80, 160)]
        w = g[160][N][0]
        a, b, c = r
        if a == c: note = "same"
        elif a[0] != c[0]: note = "16 missed the lowest root"
        else: note = "lowest agrees, later roots differ"
        print(f"{N:>8} {w:>9}  {', '.join(a):<46} {', '.join(b):<46} {', '.join(c):<46} {note}")
        if b != c: print(f"{'':>19}!! 80 vs 160 differ at N={N}")
    print()
