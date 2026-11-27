import sys, time
import numpy as np
from scipy.optimize import root
from hol_root import *
kind = int(sys.argv[1])
f = lambda v: (lambda d: [d.real, d.imag])(D_hol(-1j * (v[0] + 1j * v[1]), 0.5, kind))
t0 = time.time()
for om0 in [complex(a) for a in sys.argv[2:]]:
    r = root(f, [om0.real, om0.imag], method="lm", tol=1e-12)
    print("kind %d start %s -> %.10f %+.10fi resid %.1e (%.0fs)" % (kind, om0, r.x[0], r.x[1], np.hypot(*f(r.x)), time.time() - t0), flush=True)
