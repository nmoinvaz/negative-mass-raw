import sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i41/notes/wormhole_evolution")
import numpy as np
import settled_mass as sm, dn
h = float(sys.argv[1]); Nc = 480; a = 0.75; p0 = m0 = 1.0
Np = int(round((3.25 - p0) / h)); nm0 = int(round((2 * a * 3.25 + 0.3 - m0 + Nc * h / 4) / h)) + 8
print("Np", Np, "nm0", nm0)
d = dn.roberts_rays(max(Np, nm0), h, a, p0, m0)
import settled_mass
try:
    out = sm.chain(2, d.eps, h, d.Sp[:, :Np + 1], d.Sm, p0, m0, nm0, 0, (2 * a * p0 - m0) / h, 1.0, 1.0, Nc, forced=[3.0, 3.15], require_trapped=False, win=60)
except Exception as e:
    print("ERR", e)
import traceback
