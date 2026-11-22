#!/usr/bin/env python3
"""Probe for #131: he_surface.py --no-controls with he_type_exact wrapped to return sp.nsimplify(D), the return value
before #103. Which checks fail? Not a control of the repository, writes nothing.
usage: python probe_old_return.py   (from the worktree root)"""
import sys

sys.path.insert(0, "notes/warp")
import sympy as sp
import he_surface as hs
import he_type as ht

orig = ht.he_type_exact


def old_return(R4):
    typ, D = orig(R4)
    return typ, sp.nsimplify(D)


ht.he_type_exact = old_return
sys.argv = ["he_surface.py", "--no-controls"]
hs.main()
