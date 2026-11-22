"""The box comparison's increments and extrapolations at sigma R = 8, dx = 1/32 (tanh_spectrum.md section 7): the box values
(five digits, as the logs print them), their differences from the sectors' value, the increments with L and their ratios,
the geometric-ratio limit as section 6 does it, and a power-law fit as a second model. An estimate, not a bound: the box
values carry about 5e-6 each from the rounding of the print, so every increment about 1e-5. Run with the venv python.
Usage: box_extrap.py [rho_sectors]  (default 0.29951080, sectors-s8.log)"""
import sys

import numpy as np
from scipy.optimize import brentq

rho_s = float(sys.argv[1]) if len(sys.argv) > 1 else 0.29951080
L = np.array([2.0, 2.5, 3.0, 3.5])
box = np.array([0.29732, 0.29843, 0.29890, 0.29912])  # the logs: Mac L = 2 and 2.5, win L = 3 and 3.5
print("L      box      sectors - box")
for l, b in zip(L, box):
    print(f"{l:4.1f}  {b:.5f}  {rho_s - b:+.2e}")
inc = np.diff(box)
print("increments (L -> L + 0.5):", " ".join(f"{x:.2e}" for x in inc))
rat = inc[1:] / inc[:-1]
print("ratios:", " ".join(f"{x:.3f}" for x in rat))
for name, idx in (("last two increments", -1), ("first two increments", 0)):
    r = rat[idx]
    lim = box[-1] + inc[-1] * r / (1 - r)
    print(f"geometric, ratio of the {name} = {r:.3f}: limit {lim:.5f}, sectors - limit {rho_s - lim:+.2e}")
# the rounding of the print: each box value +-5e-6
rng = []
for d in np.ndindex(*(2,) * 4):
    b = box + 5e-6 * (2 * np.array(d) - 1)
    i = np.diff(b)
    r = i[2] / i[1]
    rng.append(b[-1] + i[2] * r / (1 - r))
print(f"geometric limit over the print's rounding (last two increments): {min(rng):.5f} to {max(rng):.5f}")
# power law: rho(L) = rho_inf - c L^-a through the last three points (fixes a from the ratio), and over all four by least squares
def a_of(Ls, v):
    f = lambda a: (v[2] - v[1]) / (v[1] - v[0]) - (Ls[2] ** -a - Ls[1] ** -a) / (Ls[1] ** -a - Ls[0] ** -a)
    return brentq(f, 0.01, 50)
for sl, tag in ((slice(1, 4), "L = 2.5, 3, 3.5"), (slice(0, 3), "L = 2, 2.5, 3")):
    Ls, v = L[sl], box[sl]
    a = a_of(Ls, v)
    c = (v[1] - v[0]) / (Ls[0] ** -a - Ls[1] ** -a)
    inf = v[0] + c * Ls[0] ** -a
    print(f"power law rho_inf - c L^-a through {tag}: a = {a:.2f}, limit {inf:.5f}, sectors - limit {rho_s - inf:+.2e}")
