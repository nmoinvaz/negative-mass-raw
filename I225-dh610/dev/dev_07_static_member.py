import sys, math
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import throat_locus as tl
# planted: GGS09a closed form vs ODE solver, D = 4
for g in (0.0, 0.3, 0.5, 1.0, 2.0):
    rth, sth, mp, mm = tl.ggs_closed(g)
    a, b = tl.asym_masses(2, rth, sth)
    print(f"gamma {g}: r_th {rth:.6f} s_th {sth:.6f}; m+ closed {mp:.8f} ode {a:.8f} (diff {a-mp:+.1e}); m- closed {mm:.8f} ode {b:.8f} (diff {b-mm:+.1e})")
# the fit recovers s_th from M(r) on both sides
rth, sth, mp, mm = tl.ggs_closed(0.5)
rp = np.array([1.2, 1.5, 2.0, 3.0, 5.0]) * rth
for n in (2, 3):
    Mp, Mm = tl.member_M(n, rth, sth, rp)
    s, rms = tl.fit_asym(n, rth, rp, Mp, Mm)
    print(f"n={n}: planted s_th {sth:.6f} recovered {s:.8f} rms {rms:.1e}; symmetric M check (sth=0): ", [round(x,6) for x in tl.member_M(n, 1.0, 0.0, [1.5, 2.0])[0]], " 1/(2r) at n=2:", [0.5/1.5, 0.5/2.0])
