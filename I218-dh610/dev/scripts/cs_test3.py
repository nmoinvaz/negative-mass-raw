import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import numpy as np
import polar_new4 as P
Va = lambda r: 2/(r*r+1) - 3/(r*r+1)**2
for th, X, N in ((0.9, 80.0, 20000), (1.1, 40.0, 20000), (1.1, 60.0, 20000), (1.1, 60.0, 40000), (1.0, 80.0, 40000)):
    t0 = time.time(); w = P.cscale_qnm(Va, P.L1_START, th, X, N); print(th, X, N, "%.10f %+.10fi" % (w.real, w.imag), "%.1fs" % (time.time() - t0), flush=True)
print("shooting: 0.681367187 -0.617753448i")
