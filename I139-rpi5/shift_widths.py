#!/usr/bin/env python3
"""Confirms, before `--mutate=shift` is relied on, that 1e-12 exceeds the sum of the two bracket widths at its l (README, Controls).
usage: shift_widths.py [L]   (default 1500). Exits 1 if 1e-12 does not exceed the sum for either column at L."""
import csv
import os
import sys
from fractions import Fraction as Fr

RAW = os.path.dirname(os.path.abspath(__file__))
L = int(sys.argv[1]) if len(sys.argv) > 1 else 1500
D = Fr(1, 10 ** 12)
files = {'ours': os.path.join(RAW, 'brackets_i2.csv'), 'theirs': os.path.join(RAW, '..', 'I104-rpi5', 'sweep_brackets.csv')}
w = {}
for n, p in files.items():
    rows = {int(r['l']): r for r in csv.DictReader(open(p))}
    w[n] = {l: (Fr(r['rstar_hi']) - Fr(r['rstar_lo']), Fr(r['rneg_hi']) - Fr(r['rneg_lo'])) for l, r in rows.items()}
    print(f"{n:6s} widest over all l: c r_* {float(max(x[0] for x in w[n].values())):.4e}, c r_neg {float(max(x[1] for x in w[n].values())):.4e}")
ok = True
for i, col in enumerate(('c r_*', 'c r_neg')):
    s = w['ours'][L][i] + w['theirs'][L][i]
    print(f"l = {L} {col}: width ours {float(w['ours'][L][i]):.4e} + theirs {float(w['theirs'][L][i]):.4e} = {float(s):.4e}; 1e-12 > sum: {D > s}; ratio {float(D / s):.2f}")
    ok &= D > s
sys.exit(0 if ok else 1)
