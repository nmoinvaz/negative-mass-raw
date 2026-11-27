import sys, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import dn, constraint_plateau as cp
# 1. ellis_rays_x reproduces dn.ellis_rays bit for bit
for fam, A, n, h, X in (("static", 0.0, 3, 0.02, 6.0), ("S", 0.02, 3, 0.02, 6.0), ("G", 0.02, 4, 0.02, 6.0)):
    pulses, sym, eps = cp.pulses_of(fam, A)
    N = int(round(X / h))
    d0 = dn.ellis_rays(n, N, h, pulses=pulses, symmetric=sym, eps=eps)
    d1 = cp.ellis_rays_x(n, N, h, pulses=pulses, symmetric=sym, eps=eps)
    print(fam, "ellis_rays_x vs dn.ellis_rays: max |diff| Sp %.1e Sm %.1e" % (np.abs(d0.Sp - d1.Sp).max(), np.abs(d0.Sm - d1.Sm).max()))
    d2 = cp.ellis_rays_x(n, N, h, pulses=pulses, symmetric=sym, eps=eps, dtype=np.longdouble)
    d3 = cp.ellis_rays_x(n, N, h, pulses=pulses, symmetric=sym, eps=eps, sub=4)
    print("   longdouble vs double r: %.2e; sub=4 vs sub=1 r: %.2e" % (np.abs((d2.Sp[0] - d0.Sp[0]).astype(float)).max(), np.abs(d3.Sp[0] - d0.Sp[0]).max()))
# 2. diag double vs row double
for fam, A, n, h, X in (("static", 0.0, 3, 0.05, 6.0), ("S", 0.02, 3, 0.05, 8.0)):
    d = cp.make_data(n, h, X, fam, A)
    st, info = cp.stream(d, stop=False, slices=(40, 100))
    t0 = time.time()
    dg = cp.stream_diag(d, np.float64, slices=(40, 100))
    print(fam, "row vs diag(float64): time-bin maxima equal:", all(np.array_equal(st.tv[w][:dg['nT']][:len(dg['tv'][w])], dg['tv'][w][:len(st.tv[w])][:len(st.tv[w])]) for w in ("pp", "mm")),
          " max|diff| tv:", max(np.abs(st.tv[w][:min(len(st.tv[w]), dg['nT'])] - dg['tv'][w][:min(len(st.tv[w]), dg['nT'])]).max() for w in ("pp","mm")),
          " slices equal:", all(np.array_equal(np.nan_to_num(info['slices'][w][s0]), np.nan_to_num(dg['slices'][w][s0])) for w in ("pp","mm") for s0 in (40,100)),
          "max slice diff", max(np.nanmax(np.abs(info['slices'][w][s0] - dg['slices'][w][s0])) for w in ("pp","mm") for s0 in (40,100)),
          "%.1fs" % (time.time() - t0))
    ld = cp.stream_diag(cp.make_data(n, h, X, fam, A), np.longdouble, slices=(40, 100))
    print("   quad vs double: max|C| per bin ratio (first bins):", [ "%.4f" % (ld['tv']['pp'][b] / dg['tv']['pp'][b]) for b in range(0, 6)])
print("--- bins inside the diagonal sweep's range")
for fam, A, n, h, X in (("static", 0.0, 3, 0.05, 6.0), ("S", 0.02, 3, 0.05, 8.0)):
    d = cp.make_data(n, h, X, fam, A)
    st, info = cp.stream(d, stop=False)
    dg = cp.stream_diag(d, np.float64)
    nb = int(d.N * h / cp.SQ2 / cp.TW) - 1
    for w in ("pp", "mm"):
        print(fam, w, "bins 0..%d equal:" % nb, np.array_equal(st.tv[w][:nb], dg["tv"][w][:nb]), "node equal:", np.array_equal(st.ti[w][:nb], dg["ti"][w][:nb]) and np.array_equal(st.tj[w][:nb], dg["tj"][w][:nb]))
