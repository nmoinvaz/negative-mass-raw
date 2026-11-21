#!/usr/bin/env python3
"""
Cross-check of the chain columns of #128's i126_replay_output.txt by code that shares nothing with replay_i126.py or
diagnose_plant.py. It shares with them the cache files, jobs.txt and the geometry of the contour. Usage:

  python cross_replay_i126.py RAW_I126_FOLDER REPLAY_OUTPUT_TXT [--mutate=thin]     (exit 1 when any box disagrees)

For each of the 61 boxes it orders every cached point on the contour along it by arclength (an independent ordering: the
replay orders by the edge parameter), sums nothing, and takes the principal phase increments of F and of F times the
planted factor between neighbours. It compares with the row of the table: the chain's points equal, and each largest
increment equal to within 0.0006 rad (the table rounds to 3 decimals).
  --mutate=thin   drops every third contour point first (the increments grow and the points shrink: every box must disagree).
"""
import re, sys, os, pickle
import numpy as np

RAW, TXT = sys.argv[1], sys.argv[2]
MUT = next((a.split('=', 1)[1] for a in sys.argv[3:] if a.startswith('--mutate=')), None)
assert MUT in (None, 'thin'), MUT
rows = {}
for ln in open(TXT, encoding='utf-8'):
    c = [x.strip() for x in ln.strip().strip('|').split('|')]
    if len(c) == 11 and re.match(r"[wz]_", c[0]):
        rows[c[0]] = c
bad, n = [], 0
for ln in open(os.path.join(RAW, 'jobs.txt'), encoding='utf-8'):
    job, script, args, _ = ln.strip().split('|')
    if '--mutate=' in args or '--flat' in args:
        continue
    pos = [a for a in args.split() if not a.startswith('--')]
    opt = dict(a[2:].split('=', 1) for a in args.split() if a.startswith('--') and '=' in a)
    eps, w, l = int(pos[0]), float(pos[1]), int(pos[2])
    x0, x1, y1 = (float(a) for a in pos[3:6])
    y0 = float(opt.get('y0', 0.0))
    s0 = complex(*(float(v) for v in opt['plant'].split(',')))
    w_ = script == 'winding2.py'
    name = ('winding2_cache_' if w_ else 'zerilli_zeros_cache_') + f"eps{eps:+d}_w{w}_l{l}_{x0}_{x1}_{y1}" + \
        ('' if y0 == 0.0 else f"_y0{y0}") + (('' if float(opt.get('rsmult', 40)) == 40 else f"_rs{float(opt['rsmult']):g}") if w_ else '') + \
        ('' if float(opt.get('zfac', 1)) == 1 else f"_z{float(opt['zfac']):g}") + '.pkl'
    cache = pickle.load(open(os.path.join(RAW, 'cache', name), 'rb'))
    sym = y0 == 0.0
    cs = [complex(x1, y0), complex(x1, y1), complex(x0, y1), complex(x0, y0)] + ([] if sym else [complex(x1, y0)])
    pf = (lambda s: (s - s0) * (s - np.conj(s0))) if sym else (lambda s: s - s0)
    pts, L = [], 0.0
    for a, b in zip(cs[:-1], cs[1:]):
        d = b - a
        for s in cache:
            u = ((s - a) * np.conj(d)) / abs(d) ** 2          # position along the edge
            if abs(u.imag) * abs(d) < 1e-9 and -1e-9 <= u.real <= 1 + 1e-9:
                pts.append((L + u.real * abs(d), s))
        L += abs(d)
    pts.sort(key=lambda p: p[0])
    if MUT == 'thin':
        pts = [p for i, p in enumerate(pts) if i % 3 != 2]
    npts = len({p[1] for p in pts})
    mx = []
    for f in (lambda s: cache[s], lambda s: cache[s] * pf(s)):
        v = [f(p[1]) for p in pts]
        mx.append(max(abs(np.angle(v[i + 1] / v[i])) for i in range(len(v) - 1)))
    r = rows[job]
    ok = int(r[4]) == npts and abs(float(r[8]) - mx[0]) <= 6e-4 and abs(float(r[9]) - mx[1]) <= 6e-4
    n += 1
    if not ok:
        bad.append(f"{job}: table {r[4]} points, {r[8]} and {r[9]} rad; here {npts}, {mx[0]:.4f} and {mx[1]:.4f}")
big = max((float(r[i]), j) for j, r in rows.items() for i in (8, 9))
print(f"{n} boxes cross-checked against {len(rows)} rows; largest increment in the table {big[0]:.3f} rad ({big[1]})")
print("RESULT: " + ("all boxes agree: chain points equal, largest increments within 0.0006 rad" if not bad and n == 61 == len(rows)
                    else "FAILED: " + "; ".join(bad or [f"{n} boxes, {len(rows)} rows"])) + (f"  [mutate={MUT}]" if MUT else ""))
sys.exit(1 if bad or n != 61 or len(rows) != 61 else 0)
