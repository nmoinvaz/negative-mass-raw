#!/usr/bin/env python3
"""ind274: the crate's |D| (#274's record files) against the stored winding2 caches, point by point (criteria in README.md).

    python3 ind274.py [--mutate=scale|extra]

Imports nothing from the repository. Exit 1 when a check fails.
"""
import glob
import json
import os
import pickle
import re
import sys

MUT = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


caches = {}
for f in sorted(glob.glob(os.path.join(RAW, "I126-rpi5", "cache", "winding2_cache_*.pkl"))
                + glob.glob(os.path.join(RAW, "I117-rpi5", "cache", "winding2_cache_*.pkl"))):
    m = re.search(r"_l(\d+)_", os.path.basename(f))
    with open(f, "rb") as fh:
        c = pickle.load(fh)
    caches[f] = (int(m[1]), {complex(k): complex(v) for k, v in c.items()})
print(f"  {len(caches)} caches loaded")


def find(c, s):
    v = c.get(s)
    if v is not None:
        return v
    for k, val in c.items():
        if abs(k - s) <= 1e-12:
            return val
    return None


files = sorted(glob.glob(os.path.join(RAW, "I274-mac", "jsonl_rec", "*.jsonl")))
k1_bad, k2_worst, npts = [], (0.0, None), 0
for jf in files:
    box = os.path.basename(jf).replace("_f64.jsonl", "")
    pts = []
    for line in open(jf):
        o = json.loads(line)
        if o.get("cmd") != "dc":
            continue
        d = complex(o["d_f64"][0], o["d_f64"][1])
        pts.append((o["l"], complex(o["re"], o["im"]), d))
    if MUT == "extra":
        pts.append((pts[0][0], pts[0][1] + 1e-3, pts[0][2]))
    ls = {p[0] for p in pts}
    hits = []
    for cf, (cl, c) in caches.items():
        if {cl} != ls:
            continue
        got = [find(c, s) for _, s, _ in pts]
        if all(g is not None for g in got):
            hits.append((cf, got))
    if len(hits) != 1:
        k1_bad.append(f"{box}: {len(hits)} caches hold all {len(pts)} points")
        print(f"  {box}: l {sorted(ls)}, {len(pts)} points, {len(hits)} matching caches")
        continue
    cf, got = hits[0]
    scale = 1 + 1e-5 if MUT == "scale" else 1.0
    worst = max(abs(abs(d) * scale / abs(g) - 1) for (_, _, d), g in zip(pts, got))
    npts += len(pts)
    if worst > k2_worst[0]:
        k2_worst = (worst, box)
    print(f"  {box}: l {sorted(ls)[0]}, {len(pts)} points, cache {os.path.relpath(cf, RAW)}, worst ||D| ratio - 1| {worst:.2e}")

check("K1", len(files) == 35 and not k1_bad, f"{len(files)} record files; boxes without exactly one matching cache: {k1_bad or 'none'}")
check("K2", k2_worst[0] <= 1e-6, f"worst | |D_crate|/|D_cache| - 1 | over {npts} points: {k2_worst[0]:.2e} ({k2_worst[1]}); bar 1e-6")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
