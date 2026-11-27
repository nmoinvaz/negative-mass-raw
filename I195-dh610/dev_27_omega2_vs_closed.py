# F3k's Omega1, Omega2 medians (run_01..04 logs, the record's fit) against the identified closed forms, to all digits
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
ln2, z3, pi2 = w.LN2, mp.zeta(3), mp.pi**2
om1c = 2*pi2/3 + 8*ln2**2
om2c = 80*z3 - mp.mpf(8)/3*pi2*ln2 - mp.mpf(32)/3*ln2**3
for k, c in (("Om1", om1c), ("Om2", om2c)):
    v = sorted(x[k] for x in adm)
    print(k, "median", mp.nstr(v[len(v)//2 - 1] / 2 + v[len(v)//2] / 2, 45), "closed", mp.nstr(c, 45))
    print("   cells' values minus closed form:", [mp.nstr(x - c, 3) for x in v])
