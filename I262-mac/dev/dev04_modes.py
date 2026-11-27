import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(40)
t0 = time.time()
N = 40
ga = cm.frobenius_s(K, 1, mp.mpf(1) / 2, -1 / (4 * K), N)       # Y_nat (g1 = -1/(4K))
g0 = cm.frobenius_s(K, 1, mp.mpf(1) / 2, 0, N)                  # g1 = 0
gb = cm.frobenius_s(K, 1, mp.mpf(3) / 2, None, N)               # Y_b
print("gb:", [mp.nstr(x, 8) for x in gb[:5]])
r0 = mp.mpf("0.1")
for name, g, s in (("Y_nat", ga, 0.5), ("Y_g1=0", g0, 0.5), ("Y_b", gb, 1.5)):
    Y0, Yp0 = cm.Y_frob_s(g, s, r0)
    res = {}
    for n in (50, 70):
        rho, Y, Yp, _ = cm.integrate(K, 1, r0, Y0, Yp0, mp.mpf(40), n=n)
        res[n] = (Y, Yp)
    print(name, "Y(40) n=50:", mp.nstr(res[50][0], 25), " n=70:", mp.nstr(res[70][0], 25), " rel diff", mp.nstr(abs(res[50][0] - res[70][0]) / abs(res[70][0]), 4), "time", time.time() - t0, flush=True)
