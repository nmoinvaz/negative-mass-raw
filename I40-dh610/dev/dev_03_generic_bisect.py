"""dev_03: bisect the two-field one-sided family (ghost A tuned, normal pulse B fixed, both on the '+' ray) and print the lifetime series.
D = 4, X = 24. Usage: dev_03_generic_bisect.py B h lo hi. Development only."""
import math, sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution")
import numpy as np
import dn

n, X = 2, 24.0
B, h, lo, hi = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
N = int(round(X / h))


def run(A, tol=1e-2, rexp=2.0):
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5), dict(field=1, ray="+", A=B, xc=3.0, w=0.5)], eps=(-1.0, 1.0))
    res = dn.evolve(d, stop=True, store=False, tol=tol, rexp=rexp)
    ev = res.events
    if not ev:
        return 0, float("nan"), None
    k = next(iter(ev))
    return (-1 if k == "collapse" else 1), dn.event_time(res, k)[2], ev[k]


print("bracket fates", run(lo)[0], run(hi)[0], flush=True)
t0 = time.time()
k = 2
while hi - lo > 1e-13:
    mid = 0.5 * (lo + hi)
    f = run(mid)[0]
    k += 1
    if f == 1:
        hi = mid
    elif f == -1:
        lo = mid
    else:
        print("static at", mid)
        break
ps = 0.5 * (lo + hi)
print(f"A*_h = {ps:.13e}  lo {lo:.14e} hi {hi:.14e}  runs {k}  {time.time()-t0:.1f} s", flush=True)
rows = {-1: [], 1: []}
for e in np.arange(1.0, 11.01, 0.5):
    out = f"{e:5.2f}"
    for s in (-1, 1):
        f, t, ev = run(ps + s * 10.0 ** (-e))
        rows[s].append((e, f, t))
        out += f"  {s:+d}: fate {f:+d} T {t:8.4f} ev {ev}"
    print(out, flush=True)
for s in (-1, 1):
    e = np.array([r[0] for r in rows[s] if r[0] >= 4 and r[0] <= 11])
    T = np.array([r[2] for r in rows[s] if r[0] >= 4 and r[0] <= 11])
    sl = np.polyfit(e * math.log(10), T, 1)[0]
    print(f"side {s:+d}: slope of T against ln(1/delta), delta in [1e-11, 1e-4]: {sl:.5f}  (1/W = 0.846045)")
