import sys, time
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
rm.CACHE = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache"
rm.horizon_series = lambda ro: (np.arange(3), np.array([1.0, 2.0, 3.0]), np.array([0.0, 0.0, 0.0]))
items = dict(rm.data_items())
for n in sys.argv[1].split(","):
    s = rm.datum_summary(n, items[n])
    print(f"== {n}: c1 {s['c1']:.4e} c2 {s['c2']:.5e} c2' {s['c2p']:.4e}")
    for kk, a in enumerate(s["k"]):
        print(f"  Pi={rm.PIS[kk]:5.2f} Qpred {a['Qpred']:+.5f} Q(R2) {a['Q2']:+.5f} Q(R1) {a['Q1']:+.5f} dQ {a['Q2']-a['Qpred']:+.1e} alpha h2 {a['h2']['alpha']:.4f} h3 {a['h3']['alpha']:.4f} R1 {a['R1']['alpha']:.4f} R2 {a['R2']['alpha']:.4f} se {a['R2']['se']:.0e} "
              f"a {a['R2']['a']:.3e} b {a['R2']['b']:.3e} d {a['R2']['d']:.2e} res {a['R2']['res']:.0e} y1 {a['y1']:.3e} sign {a['R2']['sign']}")
