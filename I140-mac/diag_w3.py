#!/usr/bin/env python3
"""Diagnosis of ind140's W3 failure (written after it): the margin as retab.py defines it, relative to the cut, from exact
squares. ind140's W3 read #140's 1.9e-12 as an absolute margin."""
import os, sys
import numpy as np
from fractions import Fraction as Fr
sys.argv = [sys.argv[0]]
RAW = os.path.expanduser('~/Source/negative-mass-raw')
sq = lambda z: Fr(float(z.real))**2 + Fr(float(z.imag))**2
worst = []
for sig, folder in ((8, 'I96-win'), (16, 'I96-dh610')):
    for m in [k + 0.5 for k in range(11)]:
        d = np.load(os.path.join(RAW, folder, 'eig', f'tanh_sigma{sig}_m{m:g}.npz'))
        A, B = d['muA'] * float(d['vc']), d['muB'] * float(d['vc'])
        top = sorted(np.argsort(-np.abs(A))[:400], key=lambda i: -sq(A[i]))
        for i in top:
            if np.min(np.abs(B - A[i])) / abs(A[i]) > 1e-5:
                c2 = sq(A[i]); break
        cut = float(c2) ** 0.5
        others = [abs(float(sq(z)) ** 0.5 - cut) for z in A[np.abs(A) > 0.9 * cut] if sq(z) != c2]
        worst.append((min(others), min(others) / cut, sig, m))
a = min(worst); r = min(worst, key=lambda t: t[1])
print(f"smallest absolute margin {a[0]:.3e} (sigma R = {a[2]}, m = {a[3]}); smallest relative margin {r[1]:.3e} "
      f"(sigma R = {r[2]}, m = {r[3]}); smallest relative at sigma R = 8: {min(t[1] for t in worst if t[2] == 8):.3e}")
