"""
Diagnostic for a winding2.py box whose planted-zero check failed (I115-rpi5, s1_l5).  Reads only the box's pickle
cache, no evaluation of D.  Usage:  python diagnose_plant.py CACHE_PKL x0 x1 y1 s0re,s0im
Replays the adaptive counter of winding2.py (copied, same rule) on cached values for D and for D*(s-s0)(s-conj s0),
then compares each accepted step with the dense chain of every cached point on the edge, sorted along it.
"""
import sys, pickle, numpy as np
cf, x0, x1, y1 = sys.argv[1], *(float(a) for a in sys.argv[2:5])
s0 = complex(*(float(a) for a in sys.argv[5].split(',')))
cache = pickle.load(open(cf, 'rb'))
corners = [complex(x1, 0), complex(x1, y1), complex(x0, y1), complex(x0, 0)]
key = lambda s: complex(round(s.real, 12), round(s.imag, 12))
D = lambda s: cache[key(s)]
pf = lambda s: (s - s0) * (s - np.conj(s0))
F = {'D': D, 'D*factor': lambda s: D(s) * pf(s)}

def count(f, a, b, nseg=10):
    """accepted leaf steps (t0, t1, measured phase) of winding2.count on one edge"""
    out = []
    def step(t0, t1, depth):
        da, db = f(a + (b - a) * t0), f(a + (b - a) * t1)
        dph = np.angle(db / da)
        fine = t1 - t0 <= 1e-5
        if abs(dph) <= 0.4 and depth <= 1 and not fine:
            dm = f(a + (b - a) * 0.5 * (t0 + t1))
            h1, h2 = np.angle(dm / da), np.angle(db / dm)
            if max(abs(h1), abs(h2)) > 0.4 or abs(h1 + h2 - dph) > 0.1:
                step(t0, 0.5 * (t0 + t1), depth + 1); step(0.5 * (t0 + t1), t1, depth + 1); return
        if abs(dph) > 0.4 and not fine:
            step(t0, 0.5 * (t0 + t1), depth + 1); step(0.5 * (t0 + t1), t1, depth + 1); return
        out.append((t0, t1, dph))
    ts = np.linspace(0, 1, nseg + 1)
    for t0, t1 in zip(ts[:-1], ts[1:]):
        step(t0, t1, 0)
    return out

def chain(f, a, b):
    """all cached points on the edge a->b sorted along it, with the principal increments between neighbours"""
    pts = []
    for s in cache:
        t = ((s - a) / (b - a))
        if abs(t.imag) < 1e-9 and -1e-9 <= t.real <= 1 + 1e-9:
            pts.append((t.real, s))
    pts.sort()
    v = [f(s) for _, s in pts]
    inc = [np.angle(v[i + 1] / v[i]) for i in range(len(v) - 1)]
    return [p[0] for p in pts], inc

print(f"cache {cf}: {len(cache)} points; planted s0 = {s0}")
for name, f in F.items():
    tot_ad, tot_ch = 0.0, 0.0
    print(f"== {name}")
    for a, b in zip(corners[:-1], corners[1:]):
        leaves = count(f, a, b)
        ad = sum(x[2] for x in leaves)
        ts, inc = chain(f, a, b)
        ch = sum(inc)
        tot_ad += ad; tot_ch += ch
        print(f"  edge {a}->{b}: adaptive {ad:+.4f} ({len(leaves)} steps, max {max(abs(x[2]) for x in leaves):.3f}), "
              f"dense chain {ch:+.4f} ({len(inc)} steps, max {max(abs(x) for x in inc):.3f}), "
              f"difference/2pi {(ad - ch) / (2 * np.pi):+.4f}")
        # leaf steps whose measured phase differs from the dense chain over the same interval by a multiple of 2pi
        for t0, t1, dph in leaves:
            sel = [i for i in range(len(inc)) if ts[i] >= t0 - 1e-9 and ts[i + 1] <= t1 + 1e-9]
            if sel:
                c = sum(inc[i] for i in sel)
                if abs(dph - c) > 0.5:
                    print(f"    step t in [{t0:.5f}, {t1:.5f}] (s = {a + (b - a) * t0:.5f} .. {a + (b - a) * t1:.5f}): "
                          f"measured {dph:+.4f}, dense chain {c:+.4f} over {len(sel)} cached steps "
                          f"(max {max(abs(inc[i]) for i in sel):.3f}), difference/2pi {(dph - c) / (2 * np.pi):+.4f}")
    print(f"  total adaptive {tot_ad:+.4f} -> count {2 * tot_ad / (2 * np.pi):+.4f};  dense chain {tot_ch:+.4f} -> "
          f"count {2 * tot_ch / (2 * np.pi):+.4f}")
