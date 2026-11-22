#!/usr/bin/env python3
"""Diagnostic for #131: which check calls `classify` at the point where sp.nsimplify changes the exact D (#72, discrepancy 1).

Runs he_surface.py's main(--no-controls) with `classify` wrapped. The wrapper adds nothing to he_type: it applies
sp.nsimplify to the exact D that the script computes by itself, and records the calling check. It does not use a control,
and it does not touch he_type.MUT.
usage: python locate_nsimp_point.py   (from the worktree root)
"""
import sys
import collections

sys.path.insert(0, "notes/warp")
import sympy as sp
import he_surface as hs

orig = hs.classify
per_check = collections.OrderedDict()
changed = []


def wrapped(RF, pt):
    out = orig(RF, pt)
    caller = sys._getframe(1).f_code.co_name
    D = out[1]
    Dq = sp.Rational(D.numerator, D.denominator)
    Dn = sp.nsimplify(Dq)
    rec = per_check.setdefault(caller, [0, 0])
    rec[0] += 1
    if Dn != Dq:
        rec[1] += 1
        changed.append((caller, Dq, Dn, {str(k): str(v) for k, v in pt.items()}))
    return out


hs.classify = wrapped
sys.argv = ["he_surface.py", "--no-controls"]
try:
    hs.main()
except SystemExit as e:
    print(f"\nhe_surface.main exit code {e.code}")
print("\nclassify calls and nsimplify(D) != D, by calling function:")
tot = 0
for k, (n, m) in per_check.items():
    print(f"  {k}: {n} points, {m} changed")
    tot += n
print(f"  total {tot} points, {len(changed)} changed")
for caller, Dq, Dn, pt in changed:
    print(f"\nchanged in {caller}:\n  D = {Dq}\n  float(D) = {float(Dq):.6e}\n  nsimplify(D) = {Dn}\n  point = {pt}")
