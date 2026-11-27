"""dev_01: first look at lifetimes. D = 4, h = 0.02, X = 20. Symmetric family: bisect from [-0.01, 0.01] to 1e-12, then a series
p* +- 10^-e. One-sided family: scan of the fate in A. Development only; nothing here is declared."""
import math, sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution")
import numpy as np
import dn

SQ2 = math.sqrt(2.0)
n, h, X = 2, float(sys.argv[2]) if len(sys.argv) > 2 else 0.02, 20.0
fam = sys.argv[1] if len(sys.argv) > 1 else "sym"
N = int(round(X / h))


def run(A, tol=1e-2, rexp=2.0):
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=(fam == "sym"))
    res = dn.evolve(d, stop=True, store=False, tol=tol, rexp=rexp)
    ev = res.events
    if not ev:
        return 0, float("nan"), None
    k = next(iter(ev))
    xp, xm, t = dn.event_time(res, k)
    return (-1 if k == "collapse" else 1), t, ev[k]


if fam in ("sym", "one"):
    if fam == "one" and len(sys.argv) > 3:
        As = [float(x) for x in sys.argv[3].split(",")]
        for A in As:
            t0 = time.time()
            f, t, ev = run(A)
            print(f"scan A={A:+.6f} fate {f:+d} T {t:.4f} event {ev} ({time.time()-t0:.1f}s)", flush=True)
        sys.exit()
    lo, hi = (-0.01, 0.01) if len(sys.argv) <= 3 else tuple(float(x) for x in sys.argv[3].split(","))
    f_lo, f_hi = run(lo)[0], run(hi)[0]
    print(f"bracket [{lo}, {hi}] fates {f_lo:+d} {f_hi:+d}", flush=True)
    t0 = time.time()
    k = 2
    while hi - lo > 1e-12:
        mid = 0.5 * (lo + hi)
        f, t, ev = run(mid)
        k += 1
        if f == 1:
            hi = mid
        elif f == -1:
            lo = mid
        else:
            print("static", mid)
            break
    ps = 0.5 * (lo + hi)
    print(f"p*_h = {ps:.14e} lo {lo:.14e} hi {hi:.14e} runs {k} {time.time()-t0:.1f}s", flush=True)
    print("   e      side   fate   T        event(j,i)")
    for e in np.arange(1.0, 11.01, 0.5):
        for s in (-1, 1):
            p = ps + s * 10.0 ** (-e)
            f, t, ev = run(p)
            print(f"{e:5.2f} {s:+d} {f:+d} {t:9.4f} {ev}", flush=True)
