import sys, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i277/notes/black_universe")
import planted_family as pf
cases = [(-1.5, -0.05, 2.0), (-1.5, 0.05, 2.0), (-1.0, -0.05, 3.0), (-1.0, 0.05, 3.0)]
for c, b, Xp in cases:
    prev = None
    for h in (0.02, 0.01, 0.005, 0.0025):
        o = pf.probe(c, b, h, Xp, 8.0, verbose=False)
        e = o["err"]
        m = [float(np.max(e[q])) for q in range(3)]
        am = np.unravel_index(np.argmax(e[0]), e[0].shape)
        rat = "" if prev is None else "  ratios " + " ".join(f"{p/x:.3f}" for p, x in zip(prev, m))
        print(f"c={c} beta={b:+} h={h}: max err r {m[0]:.4e} f {m[1]:.4e} phi {m[2]:.4e}; argmax r at i={am[0]}/{o['Np']} j={am[1]}/{o['Nm']} v={o['vn'][am[0]]:.3f} rho={o['rho'][am]:.3f}; {o['t_evolve']:.1f}s{rat}", flush=True)
        prev = m
