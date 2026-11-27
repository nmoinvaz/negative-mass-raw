"""dev_02: one-sided families whose threshold is away from A = 0. Ghost pulse (field 0, amplitude A) plus a fixed normal pulse
(field 1, amplitude B), both on the '+' ray. D = 4, h = 0.02, X = 20. Development only; nothing here is declared."""
import math, sys
sys.path.insert(0, "/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution")
import numpy as np
import dn

n, h, X = 2, 0.02, 20.0
N = int(round(X / h))


def run(A, B, xcB=3.0, wB=0.5, rexp=2.0, tol=1e-2):
    pulses = [dict(field=0, ray="+", A=A, xc=3.0, w=0.5)]
    if B != 0:
        pulses.append(dict(field=1, ray="+", A=B, xc=xcB, w=wB))
    d = dn.ellis_rays(n, N, h, pulses=pulses, eps=(-1.0, 1.0))
    res = dn.evolve(d, stop=True, store=False, tol=tol, rexp=rexp)
    ev = res.events
    if not ev:
        return 0, float("nan")
    k = next(iter(ev))
    return (-1 if k == "collapse" else 1), dn.event_time(res, k)[2]


for B in [float(x) for x in sys.argv[1].split(",")]:
    As = np.concatenate([-np.logspace(-3, 0, 19)[::-1], [0.0], np.logspace(-3, 0, 19)])
    row = []
    for A in As:
        f, t = run(A, B)
        row.append(f)
    s = "".join({-1: "c", 1: "E", 0: "."}[f] for f in row)
    flips = [(As[i], As[i + 1]) for i in range(len(row) - 1) if row[i] != row[i + 1]]
    print(f"B={B:+.3f}: {s}   (A from {As[0]:+.3f} to {As[-1]:+.3f}; c collapse, E expand)")
    print("   flips between A:", ", ".join(f"({a:+.4f},{b:+.4f})" for a, b in flips), flush=True)
