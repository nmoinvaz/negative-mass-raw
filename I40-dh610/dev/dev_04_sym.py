"""dev_04: symmetric family, any D. Usage: dev_04_sym.py n h X [fam] [lo hi]. Bisect to 1e-13 (or until static through X), series p* +- 10^-e,
e = 1..13 step 0.5, per-side slopes of T against ln(1/delta) over several windows. Development only; nothing here is declared."""
import math, sys, time
sys.path.insert(0, "/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution")
import numpy as np
import dn

SQ2 = math.sqrt(2.0)
W2 = {2: 1.39705243433350684, 3: 2.98495893035176025, 4: 4.68662054311946479}
n, h, X = int(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
fam = sys.argv[4] if len(sys.argv) > 4 else "sym"
lo, hi = (float(sys.argv[5]), float(sys.argv[6])) if len(sys.argv) > 6 else (-0.01, 0.01)
N = int(round(X / h))
W = math.sqrt(W2[n])


def run(A):
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray="+", A=A, xc=3.0, w=0.5)], symmetric=(fam == "sym"))
    res = dn.evolve(d, stop=True, store=False, tol=1e-2, rexp=2.0)
    if not res.events:
        return 0, float("nan"), None
    k = next(iter(res.events))
    return (-1 if k == "collapse" else 1), dn.event_time(res, k)[2], res.events[k]


t0 = time.time()
f_lo, f_hi = run(lo)[0], run(hi)[0]
print(f"D={n+2} h={h} X={X} N={N} fam={fam} 1/W={1/W:.6f}; bracket [{lo}, {hi}] fates {f_lo:+d} {f_hi:+d}", flush=True)
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
        print(f"static through X at {mid:.16e} (bracket {hi-lo:.2e})")
        break
ps = 0.5 * (lo + hi)
print(f"p*_h = {ps:.14e}  bracket {hi-lo:.2e}  runs {k}  {time.time()-t0:.1f} s", flush=True)
E = np.arange(1.0, 13.01, 0.5)
T = {-1: [], 1: []}
F = {-1: [], 1: []}
for e in E:
    out = f"{e:5.2f}"
    for s in (-1, 1):
        f, t, ev = run(ps + s * 10.0 ** (-e))
        T[s].append(t)
        F[s].append(f)
        out += f"  {s:+d}: {f:+d} T {t:8.4f} ev {ev}"
    print(out, flush=True)
print(f"total {time.time()-t0:.1f} s")
for (a, b) in [(3.0, 11.0), (3.5, 11.0), (4.0, 11.0), (4.0, 12.0), (3.0, 13.0), (5.0, 11.0), (2.0, 11.0), (3.0, 10.0)]:
    m = (E >= a) & (E <= b)
    line = f"window e in [{a},{b}] ({(b-a):.1f} decades):"
    for s in (-1, 1):
        Ts = np.array(T[s])
        ok = m & np.isfinite(Ts)
        if ok.sum() > 3:
            sl, ic = np.polyfit(E[ok] * math.log(10), Ts[ok], 1)
            res = Ts[ok] - (sl * E[ok] * math.log(10) + ic)
            line += f"  side {s:+d}: slope {sl:.5f} ({sl*W-1:+.2e}) rms {res.std():.4f}"
    print(line)
