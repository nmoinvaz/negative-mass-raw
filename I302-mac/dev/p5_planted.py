import sys, os, time, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i302/notes/black_universe"))
sys.argv = [sys.argv[0]] + [a for a in sys.argv[1:] if a.startswith("--")]
import horizon_basis as hb
import numpy as np
kinds = os.environ.get("KINDS", "gd")
hl = [float(x) for x in os.environ.get("HL", "0.02,0.01,0.005").split(",")]
for kind in kinds:
    errs, c2s = [], []
    for h in hl:
        t0 = time.time()
        ro = hb.planted(kind, h)
        rd = hb.readings(ro, h)
        errs.append(float(ro["Yerr"]))
        print(kind, "h", h, "wall", round(time.time() - t0, 1), "Yerr", f"{errs[-1]:.3e}", {k: (v if not isinstance(v, tuple) else tuple(round(x, 12) for x in v)) for k, v in rd.items()})
    print(kind, "ratios", hb.ratios(errs))
