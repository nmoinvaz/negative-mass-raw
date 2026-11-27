import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(40)
g, chk = cm.frobenius(K, 1, -1 / (4 * K), 30)
print("order-1 check", chk)
print("g2 (nat)", g[2], "vs 5/12 - pi^2/128 =", mp.mpf(5) / 12 - mp.pi ** 2 / 128)
g0, _ = cm.frobenius(K, 1, 0, 30)
print("g2 (g1=0)", g0[2], "vs", mp.mpf(5) / 12 + mp.pi ** 2 / 128)
print("ratio |g_k+1/g_k|:", [mp.nstr(abs(g[k + 1] / g[k]), 5) for k in range(20, 29)])
# Taylor step vs series: from rho = 0.05 to 0.1
Y0, Yp0 = cm.Y_frob(g, mp.mpf("0.05"))
Y1, Yp1 = cm.step(K, 1, mp.mpf("0.05"), Y0, Yp0, mp.mpf("0.05"), n=40)
Ys, Yps = cm.Y_frob(g, mp.mpf("0.1"))
print("step vs series at 0.1:", mp.nstr(abs(Y1 - Ys) / abs(Ys), 5), mp.nstr(abs(Yp1 - Yps) / abs(Yps), 5))
