"""dev_03: amplification of coefficient noise by the estimator (exploration cases with other parameters than the suite's
N1, N2, O8): error / delta for s and alpha, noise delta = 1e-10, 1e-19, 1e-38, three seeds, degrees up to 9"""
import sys, random
sys.path.insert(0, '.')
from explore3 import *
import explore3 as e3
from helpers import inv_pairs
DMAX = 9
DA = tuple(range(1, DMAX + 1)); DB = tuple(range(2, DMAX + 1))
LANES3 = [("f64", 53, 30, 1e-10), ("dd", 106, 60, 1e-19), ("qd", 212, 120, 1e-38)]
CASES = [
 ("W1 real a=.45 s=2.2 c=1.4 tau=1000 s", "real", dict(alpha=0.45, sigma=2.2, tau=2200, amp=1.4)),
 ("W2 real a=-.6 s=-1.9 c=.7 tau=1000 s", "real", dict(alpha=-0.6, sigma=-1.9, tau=1900, amp=0.7)),
 ("W3 pair a=.4 1.0+1.3i c=1.2 tau=1000 s", "pair", dict(alpha=0.4, mod=(1.0**2+1.3**2)**.5, ang=mp.atan2(1.3, 1.0), tau=1640, amp=1.2)),
 ("W4 real a=2e-8 s=1.8 c=1 tau=1800 s", "real", dict(alpha=2e-8, sigma=1.8, tau=1800, amp=1.0)),
]
for name, kind, p in CASES:
    print(name, flush=True)
    for lane, bits, K, delta in LANES3:
        for seed in (1, 2, 3):
            set_prec(bits)
            c, tr = build(kind, p, K, 0)
            rnd = random.Random(seed)
            c = [v * (1 + mpf(delta) * mpf(rnd.uniform(-3**.5, 3**.5))) for v in c]
            ta = cells_A(c, DA, PHIS); tb = cells_B(c, DB, PHIS)
            res = []
            for fam, tab in (("A", ta), ("B", tb)):
                ch = choose(tab, 8)
                if ch is None: continue
                key, sp = ch; e = tab[key]
                res.append((float(sp[0]), fam, key, e))
            if not res:
                print(f"  [{lane}] seed {seed}: none"); continue
            sp, fam, key, e = min(res, key=lambda t: t[0])
            es = float(dist(e, tr) / abs(mp.mpc(tr["sre"], tr["sim"])))
            ea = float(abs(e["alpha"] - tr["alpha"]))
            print(f"  [{lane}] seed {seed}: {fam}{key} spread {sp:.1e} err_s/delta {es/delta:.2e} err_a/delta {ea/delta:.2e}", flush=True)
