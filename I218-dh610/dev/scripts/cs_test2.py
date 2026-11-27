import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import numpy as np
import polar_new4 as P
Va = lambda r: 2/(r*r+1) - 3/(r*r+1)**2
for X, N in ((40.0, 10000), (40.0, 20000), (60.0, 20000)):
    t0 = time.time(); w = P.cscale_qnm(Va, P.L1_START, 0.9, X, N); print(X, N, w, "%.1fs" % (time.time() - t0), flush=True)
