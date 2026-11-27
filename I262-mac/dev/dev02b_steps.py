import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(40)
g, chk = cm.frobenius(K, 1, -1 / (4 * K), 40)
t0 = time.time()
for n in (40, 60):
    rho = mp.mpf("0.05"); Y, Yp = cm.Y_frob(g, rho)
    while rho < mp.mpf("0.2"):
        h = min(mp.mpf("0.25") * rho, mp.mpf("0.2") - rho)
        Y, Yp = cm.step(K, 1, rho, Y, Yp, h, n=n); rho += h
    Ys, Yps = cm.Y_frob(g, rho)
    print("n", n, "rho", rho, "step vs series:", mp.nstr(abs(Y - Ys) / abs(Ys), 5), mp.nstr(abs(Yp - Yps) / abs(Yps), 5), "time", time.time() - t0)
