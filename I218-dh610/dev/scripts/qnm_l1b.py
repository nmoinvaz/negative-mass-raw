import time
import numpy as np
from qnm_gen import *
from coef1 import M3, gvec
t0 = time.time()
Mf = lambda r, l: M3(r, l, 1.0, 0.0)
gf = lambda r, l: gvec(r, l, 1.0, 0.0)
# scalar Schroedinger systems
def schr(Vf):
    return lambda r, l: np.array([[0, 1], [Vf(r) + l, 0]], dtype=complex)
cases = [("mine l=1 (H1=0 gauge, 3D + gauge column)", lambda Wv: Dgen(Wv, Mf, 3, 1, 0.5, extra=gf)),
         ("test scalar l=1: V = 2/R2 + 1/R4", lambda Wv: Dgen(Wv, schr(lambda r: 2/(r*r+1) + 1/(r*r+1)**2), 2, 1, 0.5)),
         ("V = 2/R2 - 3/R4", lambda Wv: Dgen(Wv, schr(lambda r: 2/(r*r+1) - 3/(r*r+1)**2), 2, 1, 0.5))]
for name, Df in cases:
    for om0 in (0.9 - 0.3j, 1.3 - 0.25j):
        om, ok = qnm(Df, om0)
        print("%-45s start %s -> omega = %.6f %+.6fi ok=%s %.0fs" % (name, om0, om.real, om.imag, ok, time.time() - t0), flush=True)
