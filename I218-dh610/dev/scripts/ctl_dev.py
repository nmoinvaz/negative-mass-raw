import sys, time, math
import numpy as np
from scan4 import *
import scan4
from scan3 import detD3
import scan3

def signs(D, Ws):
    return [(round(Ws[i], 4), round(Ws[i + 1], 4)) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])]
p = RES["R1"]
Ws = np.exp(np.linspace(math.log(0.01), math.log(8.0), p["nW"]))
# (a) L sign flip, l=2
for c in (0.0, -0.3, -1.5):
    fam = st.Fam(c, "R2")
    for Lv in (6.0, -6.0, -2.0, 0.0):
        D = np.array([detD(W, Lv, fam, p) for W in Ws])
        print("c=%g L=%g: sign changes %s" % (c, Lv, signs(D, Ws)), flush=True)
# (d) rmax too close
p2 = dict(p); p2.update(rmax0=4.0, rmaxW=0.0)
for c in (0.0, -0.3):
    fam = st.Fam(c, "R2")
    D = np.array([detD(W, 6.0, fam, p2) for W in Ws]); print("rmax small c=%g l=2:" % c, signs(D, Ws), flush=True)
    D = np.array([detD3(W, fam, p2) for W in Ws]); print("rmax small c=%g l=1:" % c, signs(D, Ws), flush=True)
