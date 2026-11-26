#!/usr/bin/env python3
"""dev_09: the C-mode sensitivity of the independent integration: the start F times (1 + 1e-16) (a float64 rounding), F(20) with and without"""
import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i183/notes/warp")
sys.argv = [sys.argv[0], "--nobuild"]
import conical_offgrid as co
import mpmath as mp
for fi, c in ((5.0, 3000.0), (0.1, 3e4)):
    import subprocess, json
    v = json.loads(subprocess.run([co.BIN, "scan", "--prec", "dd", "--fi", repr(fi), "--c", repr(c)], capture_output=True, text=True).stdout.splitlines()[0])
    L = int(v["l"])
    t0 = time.time()
    y0, n0 = co.indep_run(fi, c, L, 20, False)
    t1 = time.time()
    y1, n1 = co.indep_run(fi, c, L, 20, False, perturb=mp.mpf(10) ** -16)
    mp.mp.dps = 30
    print(f"({fi:g},{c:g}) L={L}: steps {n0}, {t1 - t0:.0f} s; F(20) = {mp.nstr(y0[0], 20)}, F'(20) = {mp.nstr(y0[1], 15)}; start F x (1 + 1e-16): relative change of F(20) {mp.nstr(abs(y1[0] - y0[0]) / abs(y0[0]), 3)}, of F'(20) {mp.nstr(abs(y1[1] - y0[1]) / abs(y0[1]), 3)} ({time.time() - t1:.0f} s)", flush=True)
