#!/usr/bin/env python3
"""Diagnosis of ind136 run 1, J4b:le (written after the failure). From P_table.tsv: with A' ~ -tau, B' ~ z tau, phi ~ v at
large z, S = P/(tau z)^9 = sum_n L_n z^-n + O(e^-z), L_n = sum_i (-1)^(9-k) c_(i, 9-k, k) v^i over terms with j + k = 9,
n = 9 - k = j. Prints L_0..L_3 exactly and S at large z from the expansion."""
import sys
from fractions import Fraction as Fr
from collections import defaultdict
L = defaultdict(lambda: defaultdict(Fr))
for ln in open(sys.argv[1]):
    if ln.startswith('#'):
        continue
    t, _, i, j, k, c = ln.rstrip('\n').split('\t')
    if t == 'P' and int(j) + int(k) == 9:
        L[int(j)][int(i)] += Fr(c) * (-1)**int(j)
for v in (Fr(1, 2), Fr(1)):
    Ln = {n: sum(c * v**i for i, c in L[n].items()) for n in range(10)}
    print(f"v = {v}: " + ', '.join(f"L{n} = {Ln[n]} ({float(Ln[n]):.6g})" for n in range(4)))
    for z in (40, 300, 10**4, 10**6):
        print(f"   z = {z}: sum_n L_n z^-n = {float(sum(Ln[n] / Fr(z)**n for n in range(10))):.9f}")
for n in range(3):
    print(f"n = {n}: polynomial in v: " + ' + '.join(f"{c} v^{i}" for i, c in sorted(L[n].items())))
