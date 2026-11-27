"""Design probe of #188 (development): winding2.py's counter (count(), the --plant check and its four mutations) ported to take
its values F(s) from a cache and nothing else, to see (a) whether the port reproduces the stored result from the stored values
alone and asks for no point the cache lacks, and (b) what each of the counter's mutations does to the planted check.
The port is a line-for-line copy of winding2.py's count() (commit 0d1d376) with `step`, `corners`, `guard` unchanged.
usage: probe_count.py CACHE.pkl x0 x1 y1 [--y0=Y0] [--guard=all] [--plant=RE,IM] [--mutate=NAME]
"""
import sys, pickle, numpy as np

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opts = dict(a[2:].split('=', 1) for a in sys.argv[1:] if a.startswith('--') and '=' in a)
cache = pickle.load(open(args[0], 'rb'))
x0, x1, y1 = (float(a) for a in args[1:4])
y0 = float(opts.get('y0', 0.0)); nseg = 10; mutate = opts.get('mutate')
guard = np.inf if opts.get('guard', '1') == 'all' else int(opts.get('guard', '1'))
plant = complex(*(float(a) for a in opts['plant'].split(','))) if 'plant' in opts else None
sym = (y0 == 0.0)
asked, missing = set(), set()


def Dc(s):
    s = complex(round(s.real, 12), round(s.imag, 12))
    asked.add(s)
    if s not in cache:
        missing.add(s)
        return complex(1.0)    # a missing point: the count is then meaningless, reported
    return cache[s]


if sym:
    corners = [complex(x1, 0), complex(x1, y1), complex(x0, y1), complex(x0, 0)]
else:
    corners = [complex(x1, y0), complex(x1, y1), complex(x0, y1), complex(x0, y0), complex(x1, y0)]
if mutate == 'reverse':
    corners = corners[::-1]


def count(F):
    total, maxstep, nmin = 0.0, 0.0, np.inf
    for a, b in zip(corners[:-1], corners[1:]):
        def step(t0, t1, depth):
            nonlocal maxstep, nmin
            da, db = F(a + (b - a)*t0), F(a + (b - a)*t1)
            dph = np.angle(db / da)
            fine = t1 - t0 <= 1e-5
            if abs(dph) <= 0.4 and depth <= guard and not fine:
                dm = F(a + (b - a)*0.5*(t0 + t1))
                h1, h2 = np.angle(dm / da), np.angle(db / dm)
                if max(abs(h1), abs(h2)) > 0.4 or abs(h1 + h2 - dph) > 0.1:
                    return step(t0, 0.5*(t0 + t1), depth + 1) + step(0.5*(t0 + t1), t1, depth + 1)
            if abs(dph) > 0.4 and not fine:
                return step(t0, 0.5*(t0 + t1), depth + 1) + step(0.5*(t0 + t1), t1, depth + 1)
            maxstep = max(maxstep, abs(dph)); nmin = min(nmin, abs(da))
            return dph
        for t0, t1 in zip(np.linspace(0, 1, nseg + 1)[:-1], np.linspace(0, 1, nseg + 1)[1:]):
            total += step(t0, t1, 0)
    doubled = sym != (mutate == 'wrongdouble')
    return (2 if doubled else 1) * total / (2*np.pi), maxstep, nmin


N, maxstep, nmin = count(Dc)
n_first = len(asked)
print(f"winding = {N:+.4f}  (max phase step {maxstep:.2f} rad, min|D| {nmin:.2e}); points asked {n_first} of {len(cache)} cached, missing {len(missing)}")
if sym:
    print(f"D(x0)={Dc(complex(x0, 0)).real:+.3e}  D(x1)={Dc(complex(x1, 0)).real:+.3e}")
if plant is not None:
    s0 = plant
    inside = x0 < s0.real < x1 and ((0 < abs(s0.imag) < y1) if sym else (y0 < s0.imag < y1))
    expected = (2 if sym else 1) * inside
    s0a = s0 + (10 * (x1 - x0) if mutate == 'misplant' else 0)
    if sym and mutate != 'onesided':
        pf = lambda s: (s - s0a) * (s - np.conj(s0a))
    else:
        pf = lambda s: (s - s0a)
    Np, maxstep_p, nmin_p = count(lambda s: Dc(s) * pf(s))
    got = Np - N
    ok = abs(got - expected) < 0.05 and maxstep_p < 0.45
    print(f"PLANTED s0 = {s0}, expected {expected}; count with the factor {Np:+.4f}, without {N:+.4f}, difference {got:+.4f} "
          f"(max phase step {maxstep_p:.2f} rad) {'PASS' if ok else 'FAIL'}" + (f" [mutate={mutate}]" if mutate else "")
          + f"; points asked in all {len(asked)}, missing {len(missing)}")
