#!/usr/bin/env python3
"""Probe for #131: what does he_type_exact return at the point #72 found, with ht.MUT = "nsimplify"?
usage: python probe_mut_returns_D.py   (from the worktree root). Not a control, writes nothing."""
import sys
from fractions import Fraction as Fr

sys.path.insert(0, "notes/warp")
import sympy as sp
import he_surface as hs
import he_type as ht
import review_he_derive as rd

v, F, a, b, u, c, s = rd.SYMS
pt = {v: Fr(7, 4), F: Fr(1, 8), a: Fr(-3, 2), b: Fr(0), u: Fr(2, 3), c: Fr(1), s: Fr(0)}
RF = rd.ring_frame(rd.build_C())
R4 = hs.to_R4(hs.R3_at(RF, pt))
(_, D) = hs.cubic_D(hs.R3_at(RF, pt))
Dq = sp.Rational(D.numerator, D.denominator)
print("exact D =", Dq)
print("sp.nsimplify(D) =", sp.nsimplify(Dq))
for mut in (None, "nsimplify"):
    ht.MUT = mut
    typ, Dsp = ht.he_type_exact(R4)
    print(f"ht.MUT = {mut!r}: type {typ}, returned D = {Dsp}, returned == exact: {Dsp == Dq}")
print("sign of nsimplify(D) agrees with the exact sign:", (sp.nsimplify(Dq) < 0) == (Dq < 0))
