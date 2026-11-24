"""convergence.py's "rel.spread (same r_m)" takes the variants whose name has no 'phi_cut', and the base variant's
name ('base (rtol1e-10, phi_cut1e-9, R60)') has one, so base is left out. For each partial file given, prints at
every gamma the spread as convergence.py prints it, the spread with base included, and whether the printed two-digit
value differs."""
import json
import sys
import numpy as np

BASE = "base (rtol1e-10, phi_cut1e-9, R60)"
for path in sys.argv[1:]:
    D = {}
    for line in open(path, encoding="utf-8"):
        r = json.loads(line)
        if isinstance(r, list) and r[0] != "q":
            D.setdefault(r[1], {})[r[0]] = r[2]
    changed = []
    for g in sorted(D):
        ds = D[g]
        used = [v for k, v in ds.items() if "phi_cut" not in k]
        incl = [v for k, v in ds.items() if "phi_cut" not in k or k == BASE]
        s0 = (max(used) - min(used)) / abs(np.mean(used))
        s1 = (max(incl) - min(incl)) / abs(np.mean(incl))
        if f"{s0:.1e}" != f"{s1:.1e}":
            changed.append((g, f"{s0:.3e}", f"{s1:.3e}"))
    print(f"{path}: {len(D)} gammas, printed spread changes when base is included at {len(changed)}: {changed}")
