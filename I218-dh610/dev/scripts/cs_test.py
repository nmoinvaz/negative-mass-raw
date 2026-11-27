import numpy as np, sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i218/notes/black_universe")
import polar_new3 as P
Va = lambda r: 2/(r*r+1) - 3/(r*r+1)**2
a, b = P.cscale_qnm(Va, 0.9, 40.0, 2400)
def pick(om, near):
    return om[np.argmin(abs(om - near))]
w1, w2 = pick(a, 0.68-0.618j), pick(b, 0.68-0.618j)
print("N: %s  2N: %s  Richardson: %s" % (w1, w2, (4*w2**2 - w1**2)/3))
rich = np.sqrt((4 * w2**2 - w1**2) / 3); print("Richardson in omega^2 -> omega:", rich)
