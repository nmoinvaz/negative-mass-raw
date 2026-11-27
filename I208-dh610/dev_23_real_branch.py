"""dev_23: the real-target branch of order5.check_pslq on synthetic targets with a known answer (no real Omega3 is used).
member: Omega3' = (13 pi^4 - 7 pi^2 ln^2 2 + 90 zeta(3) ln 2 - 5 ln^4 2 + 11 Li4(1/2))/45 + 3 zeta(3) in P2 (found; absent from P1);
non-member: zeta(5)/pi (not found in any)."""
import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i208/notes/wormhole_largeD")
import mpmath as mp
import order5 as o
mp.mp.dps = 330
pi, ln2, z3 = mp.pi, mp.ln2, mp.zeta(3)
li4 = mp.polylog(4, mp.mpf(1) / 2)
member = (13 * pi**4 - 7 * pi**2 * ln2**2 + 90 * z3 * ln2 - 5 * ln2**4 + 11 * li4) / 45 + 3 * z3
nonmember = mp.zeta(5) / pi
for label, x in (("member", member), ("non-member", nonmember)):
    print("target:", label, mp.nstr(x, 30))
    o.RESULTS.clear()
    ev = {"B3": {"Om3": +x}, "B4": {"Om3": +x}}
    o.check_pslq(ev)
