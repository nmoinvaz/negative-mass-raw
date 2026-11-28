import sys, os, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i302/notes/black_universe"))
_a = sys.argv; sys.argv = sys.argv[:1]
import full_slice as fs
sys.argv = _a
bg = fs.bgc(-1.0)
for s in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7):
    b = bg.at(s)
    print(s, f"F_Pi {b['Fp']:.12f}  rho/s^2 {b['rho']/s**2:.12f}  pi*G0/2 with G0=rho/s^2: {math.pi/2*b['rho']/s**2:.12f}")
