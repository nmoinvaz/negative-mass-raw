import sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import numpy as np
import polar_new3 as P
t0 = time.time()
o1 = P.qnm_root(P.D_qnm_l1, P.L1_START); print("derived l=1 :", o1, "%.0fs" % (time.time() - t0), flush=True)
o2 = P.qnm_root(lambda W: P.D_qnm_schr(W, 0), P.L1_START); print("master shoot:", o2, "%.0fs" % (time.time() - t0), flush=True)
o3 = P.qnm_root(lambda W: P.D_qnm_schr(W, 1), P.L1_START); print("test-scalar l=1 shoot from the same start:", o3, "%.0fs" % (time.time() - t0), flush=True)
for X, N in ((40.0, 2400), (40.0, 4800), (60.0, 4800)):
    a, b = P.cscale_qnm(lambda r: 2/(r*r+1) - 3/(r*r+1)**2, P.QNM_THETA_L1, X, N)
    w1 = a[np.argmin(abs(a - P.L1_START))]; w2 = b[np.argmin(abs(b - P.L1_START))]
    print("eig code X=%g N=%d: %s" % (X, N, np.sqrt((4 * w2**2 - w1**2) / 3)), flush=True)
