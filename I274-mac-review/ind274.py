#!/usr/bin/env python3
"""ind274: the crate's |D| (#274's record files) against the stored winding2 caches, point by point (criteria in README.md).

    python3 ind274.py [--mutate=scale|drop]

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


FOLDER = {"126": "I126-rpi5", "117": "I117-rpi5", "115": "I115-rpi5"}


def cache_name(b):
    tag = f"eps{b['eps']:+d}_w{b['w']}_l{b['l']}_{b['x0']}_{b['x1']}_{b['y1']}"
    if b["y0"] != 0.0:
        tag += f"_y0{b['y0']}"
    if b["rsmult"] != 40.0:
        tag += f"_rs{b['rsmult']:g}"
    if b["zfac"] != 1.0:
        tag += f"_z{b['zfac']:g}"
    return os.path.join(RAW, FOLDER[b["issue"]], "cache", f"winding2_cache_{tag}.pkl")


recs = sorted(glob.glob(os.path.join(RAW, "I274-mac", "results", "record", "*.json")))
k1_bad, k2_worst, npts = [], (0.0, None), 0
for rf in recs:
    b = json.load(open(rf))
    box = b["box"]
    cf = cache_name(b)
    with open(cf, "rb") as fh:
        c = {complex(k): complex(v) for k, v in pickle.load(fh).items()}
    ev = {}
    for line in open(os.path.join(RAW, "I274-mac", "jsonl_rec", f"{box}_f64.jsonl")):
        o = json.loads(line)
        if o.get("cmd") == "dc" and o["l"] == b["l"]:
            ev[complex(o["re"], o["im"])] = complex(o["d_f64"][0], o["d_f64"][1])
    if MUT == "drop":
        ev.pop(next(iter(c)), None)
    missing = [s_ for s_ in c if s_ not in ev]
    asked = (b.get("crate") or {}).get("asked")
    ok1 = not missing and asked == len(c) == b["n_cache"]
    if not ok1:
        k1_bad.append(f"{box}: {len(missing)} stored not evaluated, asked {asked}, cache {len(c)}")
    scale = 1 + 1e-5 if MUT == "scale" else 1.0
    worst = max(abs(abs(ev[s_]) * scale / abs(v) - 1) for s_, v in c.items() if s_ in ev)
    npts += sum(1 for s_ in c if s_ in ev)
    if worst > k2_worst[0]:
        k2_worst = (worst, box)
    print(f"  {box}: {os.path.relpath(cf, RAW)}, {len(c)} stored, {len(ev)} evaluated, {len(missing)} stored not evaluated, "
          f"worst ||D| ratio - 1| {worst:.2e}")

files = recs
check("K1'", len(files) == 36 and not k1_bad, f"{len(files)} record files (35 boxes and #115's extra); failures: {k1_bad or 'none'}")
check("K2", k2_worst[0] <= 1e-6, f"worst | |D_crate|/|D_cache| - 1 | over {npts} points: {k2_worst[0]:.2e} ({k2_worst[1]}); bar 1e-6")
bad = [nm for nm, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}; mutation {MUT}", flush=True)
sys.exit(1 if bad else 0)
