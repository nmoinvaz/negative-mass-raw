#!/usr/bin/env python3
"""Diagnosis of ind139's K2 failure (written after it): rows where #2's csv differs between the Mac and rpi5, whether the
two brackets of each differing row overlap, and their widths."""
import sys
from fractions import Fraction as Fr
a = [ln.rstrip('\n').split(',') for ln in open(sys.argv[1])][1:]
b = [ln.rstrip('\n').split(',') for ln in open(sys.argv[2])][1:]
diff, worst = [], None
for x, y in zip(a, b):
    if x != y:
        cols = [k for k in range(2, 6) if x[k] != y[k]]
        ok = True
        for lo, hi in ((2, 3), (4, 5)):
            o = min(Fr(x[hi]), Fr(y[hi])) - max(Fr(x[lo]), Fr(y[lo]))
            ok &= o >= 0
            worst = o if worst is None else min(worst, o)
        diff.append((int(x[0]), cols, ok))
print(f"{len(diff)} of {len(a)} rows differ; columns differing: "
      f"{sorted(set(c for _, cs, _ in diff for c in cs))}; all differing pairs overlap: {all(o for *_, o in diff)}; "
      f"smallest overlap {float(worst):.3e}")
print("l:", [l for l, _, _ in diff])
