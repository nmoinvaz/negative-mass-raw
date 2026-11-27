"""dev_05: the profiles of profiles.py at D = 20, 100, 1000 with modes_r.py's W^2 (what profiles.py uses) against the crate's value
(growth.csv's row). Reported, not a gate. Run from notes/wormhole_largeD: python3 profile_sensitivity.py"""
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i200/notes/wormhole_largeD")
import numpy as np
import profiles as p
import modes_r as m

rgrid = np.concatenate([1 + np.geomspace(1e-6, 0.05, 200), np.linspace(1.05, 3.0, 400)[1:]])
rgrid = np.unique(np.concatenate([[1.0 + 1e-7], rgrid]))
crate = p.crate_w2()
for D in (20, 100, 1000):
    w_old = m.W2_of(D)
    w_new = float(p.round12(crate[D]))
    y_old, y_new = p.profile(D, w_old, rgrid), p.profile(D, w_new, rgrid)
    rel = np.abs(y_new - y_old) / np.abs(y_old)
    changed = sum(f"{a:.10e}" != f"{b:.10e}" for a, b in zip(y_old, y_new))
    print(f"D = {D:5d}: W2 modes_r {w_old:.12f}  crate {w_new:.12f}  diff {w_new - w_old:+.2e}; profile max relative change "
          f"{rel.max():.2e}; cells whose printed .10e digits change {changed} of {len(rgrid)}")
