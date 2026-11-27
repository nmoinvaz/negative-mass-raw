import time, cmath
import numpy as np
from qnm_fast import *
t0 = time.time()
for Wv in (-1j * (1.573 - 0.53j), -1j * (1.0 - 0.3j), 0.7 + 0j):
    t1 = time.time(); d = D_l1(Wv, 0.5 if Wv.real < 0 or Wv.imag != 0 else 0.0); print("W", Wv, "D", d, "%.2fs" % (time.time() - t1), flush=True)
