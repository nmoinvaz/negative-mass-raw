import math, numpy as np
import scan4, scan3
from scan4 import *
from scan3 import detD3, gauge_vec
from pol import *
def left_out(W, L, fam, rm, p):
    lam = W * W; c = fam.c; K = fam.K; rh = fam.rh; mu = W / fam.A1
    C = taylor_S(m4_entries, 4, S4, c, rh, lam, (L,))
    z0 = 0.04
    v1, _ = frob_vec(C, 1 - mu, z0); v2, _ = frob_vec(C, -1 - mu, z0)
    Y0 = np.stack([v1, v2], axis=1)
    return integrate_frame(rhs4_hz, (lam, L, c, K, rh), z0, rm - rh, Y0, chunk=1.0, rtol=p["rtol"])
p = RES["R1"]; Ws = np.exp(np.linspace(math.log(0.01), math.log(8.0), p["nW"]))
for c in (-0.3, -1.5):
    fam = st.Fam(c, "R2"); rm = 1.0 if fam.rh < 0.5 else fam.rh + 1.0
    D = []
    for W in Ws:
        QR = right_frame4(W, 6.0, fam.c, fam.K, rm, p)
        QL = left_out(W, 6.0, fam, rm, p); QL = to_original(QL, rm - fam.rh)
        QL, _ = np.linalg.qr(QL); QR, _ = np.linalg.qr(QR)
        D.append(np.linalg.det(np.hstack([QL, QR])))
    D = np.array(D)
    print("c=%g l=2 hz_out: sign changes" % c, [(round(Ws[i], 4), round(Ws[i + 1], 4)) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])], flush=True)
