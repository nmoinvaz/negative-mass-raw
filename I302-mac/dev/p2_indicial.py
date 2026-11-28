import math, sys, os
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i302/notes/black_universe"))
_a = sys.argv; sys.argv = sys.argv[:1]
import full_slice as fs
sys.argv = _a
bg = fs.bgc(-1.0)
for s in (1e-3, 3e-3, 1e-2, 3e-2):
    b = bg.at(s)
    g = b["rho"] * b["r"] / math.sqrt(2)
    a = g / s**2
    print(s, "rho/s^2", b["rho"]/s**2, "a=g/s^2", a, "E", b["E"], "V0", b["V0"], "V1", b["V1"], "r", b["r"], "php", b["php"], "Fp/s", b["Fp"]/s,
          "kap~ = E V1 r / a", b["E"]*b["V1"]*b["r"]/a, " E V0", b["E"]*b["V0"], "E/r^2", b["E"]/b["r"]**2)
