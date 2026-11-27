import sys, time, math
import numpy as np
from scan4 import detD, RES, st
from scan3 import detD3
MEMBERS = [-10.0, -3.0, -2.0, -1.5, -1.1, -1.01, -1.001, -1.0001, -1.0, -0.9999, -0.999, -0.99, -0.95, -0.9, -0.7, -0.5, -0.3, -0.2, -0.1, -0.01, 0.0]
res = sys.argv[1]; p = RES[res]
Ws = np.exp(np.linspace(math.log(0.01), math.log(8.0), p["nW"]))
for c in MEMBERS:
    fam = st.Fam(c, "R2")
    t0 = time.time()
    out = []
    for lab, fn in (("l=2", lambda W: detD(W, 6.0, fam, p)), ("l=1", lambda W: detD3(W, fam, p))):
        try:
            D = np.array([fn(W) for W in Ws])
            sc = [(round(Ws[i], 4), round(Ws[i + 1], 4)) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])]
            out.append("%s: sign changes %d %s, D[0]=%.2e D[-1]=%.2e min|D|=%.2e" % (lab, len(sc), sc, D[0], D[-1], np.min(np.abs(D))))
        except Exception as e:
            out.append("%s: ERROR %r" % (lab, e))
    print("c = %-8g (%.0fs) %s" % (c, time.time() - t0, " | ".join(out)), flush=True)
