import sys, time
from qnm_fast import *
kind = int(sys.argv[1]); om0 = complex(sys.argv[2])
t0 = time.time()
f = lambda v: (lambda d: [d.real, d.imag])(D_l1(-1j * (v[0] + 1j * v[1]), 0.5, kind))
for tol in (1e-8, 1e-11):
    r = root(f, [om0.real, om0.imag], tol=tol)
    print("kind %d start %s tol %g -> omega = %.8f %+.8fi success=%s resid=%.1e (%.0fs)" % (kind, om0, tol, r.x[0], r.x[1], r.success, np.hypot(*f(r.x)), time.time() - t0), flush=True)
    om0 = complex(r.x[0], r.x[1])
