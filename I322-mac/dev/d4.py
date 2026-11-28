import sys, time
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
rm.CACHE = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache2"
items = dict(rm.data_items())
hl = rm.HL[:2]
for n in sys.argv[1].split(","):
    ros = [rm.run_data(items[n], h, n) for h in hl]
    cs = [rm.c_read(r, "S") for r in ros]
    c2 = rm.rich(cs[0][1], cs[1][1])
    g = [rm.horizon_series(r) for r in ros]
    R = rm.rich_series(g[0], g[1])
    m = (R[1] >= rm.VA) & (R[1] <= rm.VB)
    V, y = R[1][m], R[2][m]
    A_ = np.vstack([V**2, V, np.ones_like(V)]).T
    co = np.linalg.lstsq(A_, y, rcond=None)[0]
    print(f"{n} mut={rm.MUT}: A/(c2 G0/I0) = {co[0]/(c2*rm.G0()/rm.I0_262):.5f}  B = {co[1]:.4e}")
