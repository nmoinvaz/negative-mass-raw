import sys, importlib.util
sys.argv = ["order4.py"]
spec = importlib.util.spec_from_file_location("order4", "order4.py"); o = importlib.util.module_from_spec(spec); spec.loader.exec_module(o)
import mpmath as mp
for guard in (0, 30):
    mp.mp.dps = 45 + guard
    Om = [-4*mp.ln2, 2*mp.pi**2/3 + 8*mp.ln2**2, mp.mpf(0), mp.mpf(0)]
    worst = 400
    for s in ("0.3", "0.8", "1.2", "1.5"):
        t = mp.mpf(s)
        def src(p):
            c, lc, l, u, R, s2, Y, L, K, T = o.closed(p, mp.pi/2 - p, False, Om)
            return 2*o.hk(2, Om, l, R, Y, L, om_last=False)/s2
        u = mp.tan(t)
        L2q = -2*Om[1] + u*mp.quad(src, [0, t])
        L2c = o.closed(t, mp.pi/2 - t, False, Om)[7][2]
        worst = min(worst, float(o.digits(L2c, L2q)))
    print("guard", guard, "N3 worst digits", worst)
