import sys, math, pickle
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
SP = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad"
name = sys.argv[1]
d = pickle.load(open(f"{SP}/dev_{name}.pkl", "rb"))
hs_ = sorted(d)[::-1]   # coarse -> fine
Qp = [0.29606224157065886, -0.5737115469767636, -0.732705808874556, -0.8465005631724783]
ser = {}
for h in hs_:
    ro = d[h]; cs = rm.c_at_S(ro)
    print(f"h={h}: c = {cs}")
    ser[h] = [rm.remainder_series(ro, k, cs)[:2] for k in range(4)]
# common V nodes: those of the coarsest
hc = hs_[0]
for k in range(4):
    Vc = ser[hc][k][0]
    tab = {}
    for h in hs_:
        step = int(round(hc / h))
        V, w = ser[h][k]
        # align: pick V values equal to Vc
        idx = np.searchsorted(V, Vc - 1e-9)
        idx = idx[idx < len(V)]
        tab[h] = (V[idx], w[idx])
    n = min(len(tab[h][0]) for h in hs_)
    Vq = tab[hc][0][:n]
    print(f"--- Pi index {k}: V grid {Vq[0]:.3f}..{Vq[-1]:.3f}")
    for vq in (4, 8, 12, 16, 20, 24):
        jj = np.argmin(np.abs(Vq - vq))
        row = [tab[h][1][jj] for h in hs_]
        s = "  ".join(f"{x: .6e}" for x in row)
        # differences
        dif = [row[i] - row[i+1] for i in range(len(row)-1)]
        rat = [dif[i]/dif[i+1] if dif[i+1] != 0 else float('nan') for i in range(len(dif)-1)]
        print(f"  V={Vq[jj]:6.2f}: {s}   ratios {['%.2f' % r for r in rat]}")
