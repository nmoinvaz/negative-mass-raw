"""P1: does Theta_gen = Theta + mu s r' dF conserve for dF != 0?  i.e. (mu s r_Pi)' == mu E (1/r - V r) at c = -1 (and -1.5)."""
import os, sys, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
import numpy as np
import full_slice as fs

for c in (-1.0, -1.5):
    bg = fs.bgc(c)
    print("c =", c)
    for s in (0.05, 0.3, 0.7, 1.0, 1.5, 3.0, 10.0, 100.0):
        def B(x):
            b = bg.at(x)
            return x * x * b["r"] * b["rp"]          # mu * s * r_Pi = s^2 r r_Pi
        h = 1e-4 * s
        dB = (-B(s + 2 * h) + 8 * B(s + h) - 8 * B(s - h) + B(s - 2 * h)) / (12 * h)
        b = bg.at(s)
        rhs = s * b["r"] * b["E"] * (1.0 / b["r"] - b["V0"] * b["r"])
        print(f"  s={s:8.3f}  d/ds(mu s r')={dB: .10e}  mu E (1/r - V r)={rhs: .10e}  diff={dB-rhs: .2e}  rel={(dB-rhs)/max(abs(rhs),1e-300): .2e}")
