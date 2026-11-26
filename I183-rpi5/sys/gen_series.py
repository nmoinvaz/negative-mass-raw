#!/usr/bin/env python3
"""one-time: solve the series of conical_global.py through eta^-17 and cache it as target/series_k17.pkl (as the script does)"""
import sys, time
sys.argv = [sys.argv[0]]
sys.path.insert(0, "/home/nathan/Source/negative-mass-i183/notes/warp")
import conical_global as cg
t = time.time()
g, log = cg.get_series()
print("series terms", len(g.d), "seconds", time.time() - t)
