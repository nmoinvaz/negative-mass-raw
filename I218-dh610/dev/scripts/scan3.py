import sys, time, math
import numpy as np
from pol import *
RES = {"R1": dict(rtol=1e-9, rmax0=150.0, rmaxW=30.0, nW=60), "R2": dict(rtol=1e-12, rmax0=300.0, rmaxW=45.0, nW=150)}

def gauge_vec(rho, lam, c, K):
    As = float(Aval(rho, c, K)); A1 = float(Apval(rho, c, K))
    return np.array(g3n(rho, lam, As, A1))

def detD3(W, fam, p):
    lam = W * W; c = fam.c; K = fam.K
    rm = 1.0 if (fam.rh is None or fam.rh < 0.5) else fam.rh + 1.0
    if fam.rh is None: rm = 0.0
    rfar = max(p["rmax0"], p["rmaxW"] / W)
    rng = np.random.RandomState(3); Y0 = rng.randn(3, 1)
    QR = integrate_frame(rhs3, (lam, c, K), rfar, rm, Y0, chunk=8.0 / W, rtol=p["rtol"])
    if fam.rh is None:
        Y0 = np.random.RandomState(4).randn(3, 1)
        QL = integrate_frame(rhs3, (lam, c, K), -rfar, rm, Y0, chunk=8.0 / W, rtol=p["rtol"])
    else:
        rh = fam.rh; mu = W / fam.A1
        C = taylor_S(m3_entries, 3, S3, c, rh, lam, (), nterm=14)
        z0 = 0.04
        v, _ = frob_vec(C, mu, z0, nrm_idx=2)
        QL = integrate_frame(rhs3_hz, (lam, c, K, rh), z0, rm - rh, v.reshape(3, 1), chunk=1.0, rtol=p["rtol"])
        QL = QL.copy(); QL[1, :] *= (rm - rh); QL = QL / np.linalg.norm(QL)
    g = gauge_vec(rm, lam, c, K); g = g / np.linalg.norm(g)
    return np.linalg.det(np.column_stack([QL[:, 0], QR[:, 0], g]))

if __name__ == "__main__":
    c = float(sys.argv[1]); res = sys.argv[2]
    fam = st.Fam(c, "R2"); p = RES[res]
    Ws = np.exp(np.linspace(math.log(0.01), math.log(8.0), p["nW"]))
    t0 = time.time(); D = np.array([detD3(W, fam, p) for W in Ws])
    print("c = %g l=1 %s: elapsed %.1f s" % (c, res, time.time() - t0))
    print("sign changes:", [(Ws[i], Ws[i + 1]) for i in range(len(Ws) - 1) if np.sign(D[i]) != np.sign(D[i + 1])])
    for i in range(0, len(Ws), max(1, len(Ws) // 12)):
        print("  W=%.4f D=%.4e" % (Ws[i], D[i]))
