import sys, math, numpy as np
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i277/notes/black_universe")
import planted_family as pf
# x- extent and the expanding sign at the candidate domains Xp = 2.16 (c = -1.5), 3.20 (c = -1)
for c, Xp in ((-1.5, 2.16), (-1.0, 3.20)):
    for b in (0.05, -0.05):
        for Xm in (4.0, 8.0, 12.0, 16.0):
            prev = None
            for h in (0.02, 0.01, 0.005):
                try:
                    o = pf.probe(c, b, h, Xp, Xm, verbose=False)
                except Exception as ex:
                    print(f"c={c} b={b:+} Xm={Xm} h={h}: {ex}")
                    break
                e = o["err"]
                m = [float(np.max(e[q])) for q in range(3)]
                rel = float(np.max(e[0] / o["r_ex"]))
                rat = "" if prev is None else f" ratio r {prev / m[0]:.3f}"
                print(f"c={c} beta={b:+} Xp={Xp} Xm={Xm} h={h}: max err r {m[0]:.3e} (rel {rel:.2e}) f {m[1]:.3e} phi {m[2]:.3e}{rat}; rho0_min {o['rho0'][-1]:.5f}; rho range last row [{o['rho'][-1].min():.3f}, {o['rho'][-1].max():.3f}]; max f_ex {np.max(-o['lnE']):.1f}", flush=True)
                prev = m[0]
