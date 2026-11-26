#!/usr/bin/env python3
"""ind30: the windings of #30's counts recomputed from the stored evaluations (criteria in README.md beside this file).

    python3 ind30.py [--mutate=NAME]
"""
import argparse
import glob
import json
import math
import os
import re
import sys
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--mutate", default=None, choices=["orient", "alias-claim"])
MUT = ap.parse_args().mutate
C = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "I30-mac", "counts")
RESULTS = []


def check(name, ok, detail):
    RESULTS.append((name, bool(ok)))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}", flush=True)


def load(fn):
    pts = {}
    for ln in open(fn):
        r = json.loads(ln)
        x, y, a = r["re"], r["im"], r["arg"]
        pts[(x, y)] = a
        if y > 0:
            pts[(x, -y)] = -a
    return pts


def edges(fn):
    rs = Counter(round(json.loads(l)["re"], 9) for l in open(fn))
    ims = Counter(round(json.loads(l)["im"], 9) for l in open(fn))
    xs = sorted(x for x, n in rs.items() if n >= 8)
    ys = sorted(y for y, n in ims.items() if n >= 5 and y > 0)
    return xs, ys


def wind(pts, a, b, c, d, tol=1e-7):
    on = lambda u, v: abs(u - v) < tol
    bpts = [p for p in pts if ((on(p[1], c) or on(p[1], d)) and a - tol <= p[0] <= b + tol)
            or ((on(p[0], a) or on(p[0], b)) and c - tol <= p[1] <= d + tol)]
    bottom = sorted({p for p in bpts if on(p[1], c)}, key=lambda p: p[0])
    right = sorted({p for p in bpts if on(p[0], b)}, key=lambda p: p[1])
    top = sorted({p for p in bpts if on(p[1], d)}, key=lambda p: -p[0])
    left = sorted({p for p in bpts if on(p[0], a)}, key=lambda p: -p[1])
    seq = bottom + right + top + left
    out = []
    for p in seq:  # drop repeated corners
        if not out or out[-1] != p:
            out.append(p)
    if out[-1] != out[0]:
        out.append(out[0])
    if MUT == "orient":
        out = out[::-1]
    tot, mx = 0.0, 0.0
    for p, q in zip(out, out[1:]):
        dl = (pts[q] - pts[p] + math.pi) % (2 * math.pi) - math.pi
        tot += dl
        mx = max(mx, abs(dl))
    return tot / (2 * math.pi), mx, len(out) - 1


def log_windings(logf):
    """the log's per-box 'winding of det M', in order of appearance: plain run first, planted second"""
    runs, cur = [], {}
    for ln in open(logf):
        m = re.search(r"box (\w+)\s+Re \(([-0-9.]+), ([-0-9.]+)\) Im \(([-+0-9.]+), ([-+0-9.]+)\).*winding of det M (-?\d+)", ln)
        if m:
            box = m.group(1)
            if box in cur:
                runs.append(cur)
                cur = {}
            cur[box] = int(m.group(6))
    if cur:
        runs.append(cur)
    return runs


ok1, ok2, ok3, n1, n2, notes, wmax = True, True, True, [], [], [], 0.0
bar = 0.1 if MUT == "alias-claim" else math.pi / 2
for tag in ("D10.0000_M48", "D12.0000_M48", "D20.0437_M32"):
    plainf = os.path.join(C, f"modecount_test_{tag}_evals.jsonl")
    plantf = glob.glob(os.path.join(C, f"modecount_test_{tag}_plant*_evals.jsonl"))[0]
    logw = log_windings(os.path.join(C, f"modecount_test_{tag}.log"))
    xs, ys = edges(plainf)
    aLL, aL, aR = xs[0], xs[1], xs[-1]
    y1, y2 = ys[0], ys[-1]
    boxes = {"B0": (aLL, aL, -y1, y1), "U0": (aLL, aL, y1, y2), "full": (aL, aR, -y2, y2)}
    mine = []
    for fn in (plainf, plantf):
        pts = load(fn)
        w = {}
        for bx, (a, b, c, d) in boxes.items():
            wv, mx, n = wind(pts, a, b, c, d)
            w[bx] = wv
            wmax = max(wmax, mx)
            ok2 &= mx <= bar
        mine.append(w)
    for i, run in enumerate(("plain", "planted")):
        for bx in boxes:
            mw = round(mine[i][bx])
            ok_int = abs(mine[i][bx] - mw) < 1e-6
            lw = logw[i].get(bx) if i < len(logw) else None
            good = ok_int and lw is not None and mw == lw
            ok1 &= good
            notes.append(f"{tag} {run} {bx}: mine {mine[i][bx]:+.6f}, log {lw}")
    d0 = {bx: round(mine[1][bx]) - round(mine[0][bx]) for bx in boxes}
    ok3 &= d0["B0"] == 2 and d0["U0"] == 0 and d0["full"] == 0
    n2.append(f"{tag}: planted - plain = {d0}")
check("W1", ok1, "; ".join(notes))
check("W2", ok2, f"largest |phase step| {wmax:.3f} (bar {bar:.3f})")
check("W3", ok3, "; ".join(n2))
bad = [n for n, ok in RESULTS if not ok]
print(f"\n{len(RESULTS)} criteria, {len(RESULTS) - len(bad)} pass; failed: {bad}", flush=True)
sys.exit(1 if bad else 0)
