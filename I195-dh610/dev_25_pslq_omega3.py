# development only, not a record: is Omega3 (fit of run_07, -652.84010757006...) in the weight-4 basis? Omega3 to 35 digits is
# taken from the driver's F3k median; this script reads it from the driver's printed 14 digits only for display and recomputes
# the full value from the same fit via w2_highprec's functions.
import sys, glob
sys.path.insert(0, "/home/nathan/Source/negative-mass-i195/notes/wormhole_largeD")
import w2_highprec as w
import mpmath as mp
R = "/home/nathan/Source/negative-mass-raw/I195-dh610/"
w.parse_logs(sorted(glob.glob(R + "run_0[1234]_*.log")))
q = w.w2_values("qd", w.DLIST, allow_run=False)
data = {d: mp.mpf(q[d]["W2"]) - 2 * (d - 3) + 4 * w.LN2 for d in w.DLIST}
cells, gate = w.fit_cells(data, mp.mpf("2.97e-54"), "M1", ks=w.KS_K)
adm = [c for c in cells if c["admitted"]]
om3 = sorted(c["Om3"] for c in adm)
rng = om3[-1] - om3[0]
med = (om3[len(om3)//2 - 1] + om3[len(om3)//2]) / 2
print("Omega3", mp.nstr(med, 40), "range", mp.nstr(rng, 3), "cells", len(adm))
ln2, z3, pi2 = w.LN2, mp.zeta(3), mp.pi**2
li4 = mp.polylog(4, mp.mpf(1) / 2)
mp.mp.dps = 60
for tau in ("1e-25", "1e-30", "1e-33"):
    b = [med, pi2**2, pi2 * ln2**2, ln2**4, z3 * ln2, li4]
    r = mp.pslq(b, tol=mp.mpf(tau), maxcoeff=10000, maxsteps=10**6)
    print("weight 4 pure", tau, r, mp.nstr(abs(sum(c * x for c, x in zip(r, b))), 3) if r else "")
b = [med, pi2**2, pi2 * ln2**2, ln2**4, z3 * ln2, li4, z3, pi2 * ln2, ln2**3, pi2, ln2**2, ln2, mp.mpf(1)]
r = mp.pslq(b, tol=mp.mpf("1e-33"), maxcoeff=10000, maxsteps=10**6)
print("weights <= 4", r)
