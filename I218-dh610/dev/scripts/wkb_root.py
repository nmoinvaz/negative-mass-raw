import sys, time
from qnm_fast import *
kind = int(sys.argv[1])
t0 = time.time()
f = lambda v: (lambda d: [d.real, d.imag])(D_l1(-1j * (v[0] + 1j * v[1]), 0.5, kind))
for om0 in (1.1 - 0.65j, 1.0 - 0.6j):
    r = root(f, [om0.real, om0.imag], tol=1e-10)
    print("kind %d start %s -> omega = %.8f %+.8fi success=%s resid=%.1e (%.0fs)" % (kind, om0, r.x[0], r.x[1], r.success, np.hypot(*f(r.x)), time.time() - t0), flush=True)
