import sys, time, math
import numpy as np
from pol import *

RES = {"R1": dict(rtol=1e-9, rmax0=150.0, rmaxW=30.0, nW=60), "R2": dict(rtol=1e-12, rmax0=300.0, rmaxW=45.0, nW=150)}

def right_frame4(W, L, c, K, rm, p):
    lam = W * W; rfar = max(p["rmax0"], p["rmaxW"] / W)
    rng = np.random.RandomState(3); Y0 = rng.randn(4, 2)
    return integrate_frame(rhs4, (lam, L, c, K), rfar, rm, Y0, chunk=8.0 / W, rtol=p["rtol"])

def left_frame4(W, L, fam, rm, p):
    lam = W * W; c = fam.c; K = fam.K
    if fam.rh is None:   # Ellis, c=0: symmetric, left end at -rfar
        rfar = max(p["rmax0"], p["rmaxW"] / W)
        rng = np.random.RandomState(4); Y0 = rng.randn(4, 2)
        return integrate_frame(rhs4, (lam, L, c, K), -rfar, rm, Y0, chunk=8.0 / W, rtol=p["rtol"])
    rh = fam.rh; mu = W / fam.A1
    C = taylor_S(m4_entries, 4, S4, c, rh, lam, (L,))
    z0 = 0.04
    v1, _ = frob_vec(C, 1 + mu, z0); v2, _ = frob_vec(C, -1 + mu, z0)
    Y0 = np.stack([v1, v2], axis=1)
    # integrate in z to rm - rh
    return integrate_frame(rhs4_hz, (lam, L, c, K, rh), z0, rm - rh, Y0, chunk=1.0, rtol=p["rtol"])

def to_original(Qz, z):
    Q = Qz.copy(); Q[3, :] = Q[3, :] / z; return Q

def D4(W, L, fam, p):
    rm = 1.0 if (fam.rh is None or fam.rh < 0.5) else fam.rh + 1.0
    if fam.rh is None: rm = 0.0
    QR = right_frame4(W, L, fam.c, fam.K, rm, p)
    QL = left_frame4(W, L, fam, rm, p)
    if fam.rh is not None:
        QL = to_original(QL, rm - fam.rh)     # F = Ft / z, then re-orthonormalize
    return QL, QR

def detD(W, L, fam, p):
    QL, QR = D4(W, L, fam, p)
    QL, _ = np.linalg.qr(QL); QR, _ = np.linalg.qr(QR)
    return np.linalg.det(np.hstack([QL, QR]))

if __name__ == "__main__":
    c = float(sys.argv[1]); L = float(sys.argv[2]); res = sys.argv[3]
    fam = st.Fam(c, "R2")
    p = RES[res]
    Ws = np.exp(np.linspace(math.log(0.01), math.log(8.0), p["nW"]))
    t0 = time.time()
    D = []
    for W in Ws:
        D.append(detD(W, L, fam, p))
    D = np.array(D)
    print("c = %g L = %g %s: elapsed %.1f s" % (c, L, res, time.time() - t0))
    sc = [(Ws[i], Ws[i + 1]) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])]
    print("sign changes:", sc)
    print("D first, last, min|D|:", D[0], D[-1], np.min(np.abs(D)))
    for i in range(0, len(Ws), max(1, len(Ws) // 12)):
        print("  W=%.4f D=%.4e" % (Ws[i], D[i]))
