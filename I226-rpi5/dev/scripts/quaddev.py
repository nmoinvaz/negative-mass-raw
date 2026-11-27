import sys, json, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import constraint_plateau as cp, dn
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs/"
D, hname, fam, side, Tc = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
X = {5: 18.0, 6: 15.0}[D]; n = D - 2
sm = json.load(open(RAW + f"D{D}_{fam}_h{hname}/summary.json"))
h = sm["h"]; pst = 0.5 * (sm["lo"] + sm["hi"]); A = pst + side * 1e-8
N = int(round(X / h)); Sc = int(Tc * cp.SQ2 / h)
pulses, sym, eps = cp.pulses_of(fam, A)
t0 = time.time()
dd = dn.ellis_rays(n, N, h, pulses=pulses, symmetric=sym, eps=eps)
dg = cp.stream_diag(dd, np.float64, Sc=Sc)
t1 = time.time()
dl = cp.ellis_rays_x(n, N, h, pulses=pulses, symmetric=sym, eps=eps, dtype=np.longdouble)
ql = cp.stream_diag(dl, np.longdouble, Sc=Sc)
t2 = time.time()
nb = int(Tc / cp.TW)
print(f"D={D} h={h:.6f} {fam} side {side:+d} slab t<={Tc}: double {t1-t0:.0f}s, quad {t2-t1:.0f}s")
print("  t     double max|C| (i,j)        quad max|C| (i,j)       double/quad")
for b in range(0, nb, 2):
    row = []
    for w in ("pp", "mm"):
        pass
    vd = max(dg["tv"]["pp"][b], dg["tv"]["mm"][b]); vq = max(ql["tv"]["pp"][b], ql["tv"]["mm"][b])
    wd = "pp" if dg["tv"]["pp"][b] >= dg["tv"]["mm"][b] else "mm"; wq = "pp" if ql["tv"]["pp"][b] >= ql["tv"]["mm"][b] else "mm"
    print("  %5.2f  %.3e (%d,%d)   %.3e (%d,%d)   %.3f" % ((b + .5) * cp.TW, vd, dg["ti"][wd][b], dg["tj"][wd][b], vq, ql["ti"][wq][b], ql["tj"][wq][b], vd / vq))
mx = lambda r: max(r["tv"]["pp"][:nb].max(), r["tv"]["mm"][:nb].max())
print("  slab max: double %.4e quad %.4e" % (mx(dg), mx(ql)))
