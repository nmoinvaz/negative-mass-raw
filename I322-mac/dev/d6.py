import sys
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
rm.CACHE = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache"
runs = rm.exact_series("g")
print("c2:", [r[1][1] for r in runs])
for k in range(4):
    fl = []
    for r in runs:
        j, V, w = r[2][k]; m = (V >= 8) & (V <= 24)
        fl.append(np.max(np.abs(w[m]) / (abs(r[1][1]) * V[m])))
    R1 = rm.rich_series(runs[0][2][k], runs[1][2][k]); R2 = rm.rich_series(runs[1][2][k], runs[2][2][k])
    fr = []
    for RR in (R1, R2):
        m = (RR[1] >= 8) & (RR[1] <= 24)
        fr.append(np.max(np.abs(RR[2][m]) / (abs(runs[2][1][1]) * RR[1][m])))
    print(f"P1 Pi={rm.PIS_ALL[k]}: raw floors {fl[0]:.2e} {fl[1]:.2e} {fl[2]:.2e} ratios {fl[0]/fl[1]:.2f} {fl[1]/fl[2]:.2f}; Richardson floors R1 {fr[0]:.2e} R2 {fr[1]:.2e}")
# P2
ra = rm.exact_series("g", hl=rm.HL[1:], mod=lambda cs: (cs[0], 0.99*cs[1], cs[2]))
for k in range(3):
    R2 = rm.rich_series(ra[0][2][k], ra[1][2][k])
    al, se, amp, sg = rm.fit_power(R2[1], R2[2])
    a, b, d, res = rm.fit_poly3(R2[1], R2[2])
    c2 = rm.rich(ra[0][1][1]/0.99, ra[1][1][1]/0.99)
    print(f"P2a Pi={rm.PIS[k]}: alpha {al:.5f} se {se:.1e} a/c2 {a/c2:.6f} b {b:.2e} d {d:.2e} res {res:.1e}")
rd = rm.exact_series("d", hl=rm.HL[1:], mod=lambda cs: (cs[0], 0.0, 0.0))
for k in range(3):
    Pi = rm.PIS[k]
    if Pi <= 0: continue
    va, vb = rm.window_for("d", Pi)
    R2 = rm.rich_series(rd[0][2][k], rd[1][2][k])
    al, se, amp, sg = rm.fit_power(R2[1], R2[2], va, vb)
    c2p = rm.rich(rd[0][1][2], rd[1][1][2])
    print(f"P2b Pi={Pi}: window [{va},{vb}] alpha {al:.5f} se {se:.1e} amp/(|c2'|Pi) {amp/(abs(c2p)*Pi):.6f}  c2' {c2p:.9e}")
# P3
for alpha in (2.0, 1.0, 0.0, -1.0):
    eps = 2e-4 / 16.0**alpha
    for k in range(3):
        if rm.PIS[k] <= 0: continue
        sers = [rm.series(r[0], k, r[1], plant=(eps, alpha)) for r in ra]
        R2 = rm.rich_series(sers[0], sers[1])
        al, se, amp, sg = rm.fit_power(R2[1], R2[2])
        print(f"P3 alpha {alpha:+.0f} Pi {rm.PIS[k]}: {al:+.5f} (se {se:.1e}), amp ratio {amp/(eps*rm.PIS[k]):.5f}")
