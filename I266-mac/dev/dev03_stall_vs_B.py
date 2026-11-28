"""Development: does the near-threshold evolution of G stall (T growing as ln 1/delta) at each B? h = 0.02, p*_h bisected to 1e-14, T at p* -/+ 10^-e."""
import sys, os, json, time
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i266/notes/wormhole_evolution"))
import threshold as th
h = float(sys.argv[1])
Bs = [float(x) for x in sys.argv[2].split(",")]
for B in Bs:
    th.CRIT["G_B"] = B
    X = 28.0
    lo, hi = (0.0, 0.2) if B >= 0.1 else (-0.01, 0.05)
    t0 = time.time()
    run = lambda p: th.point(2, "G", h, X, p)
    # bracket: lo collapse, hi expansion
    lo, hi, st = th.bisect(run, lo, hi, 1e-14)
    ps = 0.5 * (lo + hi)
    row = []
    for e in (4, 6, 8, 10):
        a = th.point(2, "G", h, X, ps - 10.0 ** -e)
        b = th.point(2, "G", h, X, ps + 10.0 ** -e)
        row.append(f"e={e}: T- {a['T']:.3f} (f{a['fate']:+d}) T+ {b['T']:.3f} (f{b['fate']:+d})")
    print(f"B={B} p*={ps:.10e} hi-lo {hi-lo:.1e} ({time.time()-t0:.0f} s) | " + " | ".join(row), flush=True)
