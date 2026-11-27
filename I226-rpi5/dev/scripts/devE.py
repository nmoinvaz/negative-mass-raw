exec(open("/tmp/claude-1000/-home-nathan-Source-negative-mass-i226/6ce098f9-1c29-4ea1-b637-485e454079a0/scratchpad/slab.py").read())
import numpy as np
def count_slice(rec_sl, frac=0.5):
    out = {}
    for w in ("pp", "mm"):
        a = np.abs(np.nan_to_num(rec_sl[w]))
        out[w] = (a.max(), int((a >= frac * a.max()).sum()))
    return out
cfg = {6: (8.0, 12.0, ("0.005", "0.0025", "0.00125")), 5: (10.0, 15.0, ("0.00707107", "0.00353553", "0.00176777"))}
for D in (6, 5):
    Tc, X, hns = cfg[D]
    for side in (-1, 1):
        recs = []
        for hn in hns:
            h, ps = pstar(D, hn)
            recs.append(go(D, h, "S", ps + side * 1e-8, Tc, X, f"S side {side:+d}"))
        print("   ratios:", ["%.3f" % (recs[k]["max"] / recs[k + 1]["max"]) for k in range(2)])
    h, ps = pstar(D, hns[2])
    for a in (1.0, 16.0):
        go(D, h, "S", ps - 1e-8, Tc, X, f"S- noise {a:g}", engine="diag", noise=a * 2.0 ** -52)
    h0, _ = pstar(D, hns[0])
    go(D, h0, "S", pstar(D, hns[0])[1] - 1e-8, Tc, X, "S- noise 1 coarsest", engine="diag", noise=2.0 ** -52)
    # slice counts at t = Tc
    s0 = int(Tc * cp.SQ2 / h) - 2
    rec, sl = cp.slab_run(D - 2, h, "S", ps - 1e-8, Tc, X, engine="diag", slices=(s0,))
    print("   slice t=Tc count of nodes >= 0.5 max:", {w: v for w, v in count_slice({w: sl[w][s0] for w in ("pp", "mm")}).items()})
    sp = (int(0.5 * s0), int(0.25 * s0), 1e-10)
    rec, sl = cp.slab_run(D - 2, h, "S", ps - 1e-8, Tc, X, engine="diag", slices=(s0,), spike=sp)
    print("   with spike", sp, "slab max %.3e; slice count:" % rec["max"], {w: v for w, v in count_slice({w: sl[w][s0] for w in ("pp", "mm")}).items()})
# bracket runs
for D, Tc, X, hns in ((6, 12.0, 15.0, ("0.005", "0.0025", "0.00125")), (5, 16.0, 18.0, ("0.00707107", "0.00353553", "0.00176777"))):
    for side in ("lo", "hi"):
        recs = []
        for hn in hns:
            ck = json.load(open(RAW + f"D{D}_S_h{hn}/constraints.json")); sm = json.load(open(RAW + f"D{D}_S_h{hn}/summary.json"))
            recs.append(go(D, sm["h"], "S", ck[side]["A"], Tc, X, f"bracket {side}"))
        print("   ratios:", ["%.3f" % (recs[k]["max"] / recs[k + 1]["max"]) for k in range(2)])
