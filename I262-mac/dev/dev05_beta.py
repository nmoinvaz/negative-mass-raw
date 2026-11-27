import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(50)
N = 50
ga = cm.frobenius_s(K, 1, mp.mpf(1) / 2, -1 / (4 * K), N)
gb = cm.frobenius_s(K, 1, mp.mpf(3) / 2, None, N)
r0 = mp.mpf("0.1")
Ya0 = cm.Y_frob_s(ga, 0.5, r0); Yb0 = cm.Y_frob_s(gb, 1.5, r0)
recs = [mp.mpf(x) for x in (20, 40, 60, 80, 100)]
_, _, _, oa = cm.integrate(K, 1, r0, *Ya0, mp.mpf(100), n=70, record=recs)
_, _, _, ob = cm.integrate(K, 1, r0, *Yb0, mp.mpf(100), n=70, record=recs)
for r in recs:
    print("rho", int(r), "  -Y_nat/Y_b =", mp.nstr(-oa[r][0] / ob[r][0], 40), "  from Y':", mp.nstr(-oa[r][1] / ob[r][1], 40))
