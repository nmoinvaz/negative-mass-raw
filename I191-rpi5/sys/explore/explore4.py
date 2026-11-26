"""dev_01: do degrees above 5 help dd and qd on product-dressed cases? (exploration cases, not the suite)"""
import sys, time
sys.path.insert(0, '.')
from explore3 import *
import explore3 as e3
CASES = [
 ("X1 real a=.7 s=-1.7 tau=4", "real", dict(alpha=0.7, sigma=-1.7, tau=4, amp=1.9)),
 ("X2 real a=-.4 s=1.1 tau=3", "real", dict(alpha=-0.4, sigma=1.1, tau=3, amp=1.9)),
 ("X3 real a=3e-7 s=1.5 tau=6", "real", dict(alpha=3e-7, sigma=1.5, tau=6, amp=1.9)),
 ("X6 pair a=.35 1.1e^.9i tau=4", "pair", dict(alpha=0.35, mod=1.1, ang=0.9, tau=4, amp=1.9)),
 ("X8 two a=.5 s=1 / a=-.5 s=-1.4", "two", dict(a1=0.5, s1=1.0, a2=-0.5, ratio=-1.4, r=1.0)),
 ("X9 two a=.5 s=1 / a=-.5 s=1.4", "two", dict(a1=0.5, s1=1.0, a2=-0.5, ratio=1.4, r=1.0)),
]
LANES2 = [("dd", 106, 60, 1.2e-32), ("qd", 212, 120, 6e-64)]
for name, kind, p in CASES:
    print(name, flush=True)
    for lane, bits, K, eps in LANES2:
        set_prec(bits)
        c, tr = build(kind, p, K, 0)
        for dmax in (5, 7, 9):
            DA = tuple(range(1, dmax + 1)); DB = tuple(range(2, dmax + 1))
            ta = cells_A(c, DA, PHIS); tb = cells_B(c, DB, PHIS)
            out = []
            for fam, tab in (("A", ta), ("B", tb)):
                ch = choose(tab, 8)
                if ch is None: out.append(f"{fam}: none"); continue
                key, sp = ch; e = tab[key]
                es = float(dist(e, tr) / abs(mp.mpc(tr["sre"], tr["sim"])))
                out.append(f"{fam}{key} spread {float(sp[0]):.1e} err {es:.1e} a_err {float(abs(e['alpha']-tr['alpha'])):.1e} (a_spread {float(sp[1]):.1e})")
            print(f"  [{lane}] dmax {dmax}: " + " | ".join(out), flush=True)
