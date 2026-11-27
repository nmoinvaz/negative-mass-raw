import numpy as np, time
from scipy.optimize import root
from qnm_ellis import Dfun
def solve(LL, om0, theta=0.5):
    f = lambda v: (lambda d: [d.real, d.imag])(Dfun(-1j * (v[0] + 1j * v[1]), LL, theta))
    r = root(f, [om0.real, om0.imag], tol=1e-12)
    return r.x[0] + 1j * r.x[1], r.success
t0 = time.time()
for LL, om0, pub in [(6.0, 1.74 - 0.305j, "1.74 -0.305i"), (12.0, 2.95 - 0.41j, "2.95 -0.410i"), (20.0, 4.08 - 0.449j, "4.08 -0.449i")]:
    for th in (0.5, 0.8):
        om, ok = solve(LL, om0, th)
        print("L=%g theta=%g: omega = %.6f %+.6fi (published %s) ok=%s %.0fs" % (LL, th, om.real, om.imag, pub, ok, time.time() - t0), flush=True)
