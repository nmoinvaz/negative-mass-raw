"""
q(r_m; s) of the rotated-path integration against polar_solver's zerilli_q (D's own Zerilli column) along the two vertical
edges of n3: Re s = -0.001 and Re s = 0.0001, Im s = 0.01 ... 0.23 (#123). Reported, not a criterion.
The ray integration is explore/exp2.py's (the same equations, Jost start and path as zerilli_zeros.py --axis); R_z is the
box's, r_m + (40 + 20 l)/0.01 + 50.
Usage: python column_scan_i123.py L
"""
import os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'explore'))
l = int(sys.argv[1]); sys.argv = [sys.argv[0], str(l)]
from exp2 import *   # rm, M, P, integ_ray (exp1: star, potential, Jost series)
T = (40 + 20 * l) / 0.01 + 50
print(f"l = {l}: r_m = {rm:.2f}, R_z = {rm + T:.1f}; start radius of zerilli_q at |s|: r_m + (40 + 20 l)/|s| + 50")
print("| Re s | Im s | R_start of zerilli_q | exp(2 |Re s| (R_start - r_m)) | relative difference of q |")
print("|---|---|---|---|---|")
for x in (0.0001, -0.001):
    for y in (0.01, 0.02, 0.03, 0.05, 0.1, 0.23):
        s = complex(x, y)
        t0 = time.time()
        y1, y2, _ = integ_ray(s, T)
        q = y2 / y1
        qz = P.zerilli_q(s)
        Rs = rm + (40.0 + 20.0 * l) / abs(s) + 50.0
        print(f"| {x:g} | {y:g} | {Rs:.0f} | {np.exp(2 * abs(x) * (Rs - rm)) if x < 0 else float('nan'):.3g} | {abs(q - qz) / abs(qz):.1e} |", flush=True)
