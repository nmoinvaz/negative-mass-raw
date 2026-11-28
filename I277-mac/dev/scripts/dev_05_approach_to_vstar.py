import sys, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i277/notes/black_universe")
import planted_family as pf
# approach to v*: Xp from lam^2_end
for c in (-1.5, -1.0):
    K = -2 * c / math.pi
    vs = math.log(20.0) / K
    for l2 in (0.256, 0.1, 0.05, 0.02, 0.01):
        v_end = vs + math.log(1 - l2) / K
        Xp = round(v_end / math.sqrt(2) / 0.04) * 0.04       # multiple of 0.04 so that N is an integer at every h
        prev = None
        for h in (0.02, 0.01, 0.005, 0.0025):
            o = pf.probe(c, -0.05, h, Xp, 8.0, verbose=False)
            e = o["err"]
            m = [float(np.max(e[q])) for q in range(3)]
            L2 = pf.lam2_of(o["G"])
            Lm = L2.mean(axis=1)
            vf, a, b = pf.vstar_fit(o["vn"], Lm, K)
            dev = float(np.max(np.abs(L2 - (1 - 0.05 * np.exp(K * o["vn"]))[:, None])))
            rat = "" if prev is None else f" ratio r {prev / m[0]:.3f}"
            print(f"c={c} lam2_end~{l2} Xp={Xp:.2f} (v_end {math.sqrt(2) * Xp:.3f}, lam2 {1 - 0.05 * math.exp(K * math.sqrt(2) * Xp) * -1 * 1 if False else 1 - 0.05 * math.exp(K * math.sqrt(2) * Xp):.4f}) h={h}: max err r {m[0]:.3e} f {m[1]:.3e} phi {m[2]:.3e}{rat}; "
                  f"v* fit {vf:.6f} (err {vf - vs:+.2e}), a {a:.6f} b {b:.6f}; max|Lam2 - lam^2| {dev:.2e}", flush=True)
            prev = m[0]
