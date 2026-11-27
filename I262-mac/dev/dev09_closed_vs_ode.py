import sys, time
sys.path.insert(0, ".")
import mpmath as mp
import cm_core as cm
K = cm.setup(45)
t0 = time.time()
N = 60
g1 = 1 / (4 * K)
g = cm.frobenius_s(K, 1, mp.mpf(1) / 2, g1, N)
pts = [mp.mpf(x) for x in ("0.3", "1", "2", "5", "10", "20", "40")]
print("series start: g1 =", g1, " g2 =", g[2], " (5/12 + 3 pi^2/128 =", mp.mpf(5) / 12 + 3 * mp.pi ** 2 / 128, ")")
res = {}
for sgn in (1, -1):
    r0 = sgn * mp.mpf("0.1")
    Y0, Yp0 = cm.Y_frob_s(g, 0.5, r0)
    _, _, _, out = cm.integrate(K, 1, r0, Y0, Yp0, sgn * mp.mpf(40), n=70, record=[sgn * p for p in pts])
    for p in pts:
        r = sgn * p
        Yo = out[r][0] if r in out else None
        if Yo is None:
            continue
        row = {}
        for mut in (None, "R2coef", "kscale", "xsign"):
            Yc = cm.Yref_closed(K, r, mut)
            row[mut] = abs(Yc - Yo) / abs(Yo)
        print("rho = %8s  Y_ode = %s   closed vs ode: %s  | R2coef %s  kscale %s  xsign %s" % (mp.nstr(r, 4), mp.nstr(Yo, 12), mp.nstr(row[None], 4), mp.nstr(row["R2coef"], 4), mp.nstr(row["kscale"], 4), mp.nstr(row["xsign"], 4)), flush=True)
print("time", time.time() - t0)
