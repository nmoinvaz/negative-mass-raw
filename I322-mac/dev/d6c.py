import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
rm.CACHE = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache"
ra = rm.exact_series("g", hl=rm.HL[1:])
for alpha in (2.0, 1.0, 0.0, -1.0):
    eps = 2e-4 / 16.0**alpha
    for k in range(3):
        if rm.PIS[k] <= 0: continue
        sers = [rm.series(r[0], k, r[1], plant=(eps, alpha)) for r in ra]
        R2 = rm.rich_series(sers[0], sers[1])
        al, se, amp, sg = rm.fit_power(R2[1], R2[2])
        print(f"P3 alpha {alpha:+.0f} Pi {rm.PIS[k]}: {al:+.5f} (se {se:.1e}), amp ratio {amp/(eps*rm.PIS[k]):.5f} sign {sg}")
