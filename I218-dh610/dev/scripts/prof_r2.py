import sys, time, math
import numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import _dev_polar as P
fam = P.st.Fam(-10.0, "R2"); p = P.RES["R2"]; W = 5.0; L = 6.0; lam = W * W
rm = P.match_point(fam)
t0 = time.time(); QR = P.far_frame_l2(W, L, fam, rm, p, +1); print("far frame %.2fs" % (time.time() - t0), flush=True)
mu = W / fam.A1
C = P.taylor_S(P.m4_entries, 4, P.S4, fam.c, fam.rh, lam, (L,))
v1, i1 = P.frob_vec(C, 1 + mu, p["z0"], p["nfrob"], 2); v2, i2 = P.frob_vec(C, -1 + mu, p["z0"], p["nfrob"], 2)
print("frob incons", i1, i2, "mu", mu, "rm - rh", rm - fam.rh, flush=True)
nodes = P.hz_nodes(p["z0"], rm - fam.rh, 1 + abs(mu)); print("nodes", len(nodes), nodes[:4], flush=True)
t0 = time.time()
QL = P.integrate_frame(P.rhs4_hz, (lam, L, fam.c, fam.K, fam.rh), p["z0"], rm - fam.rh, np.stack([v1, v2], axis=1), nodes, p["rtol"])
print("hz stage %.2fs" % (time.time() - t0), flush=True)
