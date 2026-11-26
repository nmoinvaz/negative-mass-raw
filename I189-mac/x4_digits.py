#!/usr/bin/env python3
"""x4_digits.py: criterion X4 of this folder's README. D printed in full by the crate with the feature off and on, and the relative
difference between the two (mpmath, 90 digits) and the number of leading significant digits that agree, at l = 2, gamma = 1 and 40 in f64,
dd and qd (the base variant), and at l = 4, gamma = 300 in dd. Information, not a gate: the step points differ by an ulp or more.

Usage: python x4_digits.py OUT.jsonl     (runs the crate itself, nice 10, through taylor_polar.get_rows; one process at a time)
"""
import json
import os
import sys

NR = "/Users/nathan/Source/negative-mass-i189/phase2/nonradial"
BINS = os.path.join(NR, "taylor_polar", "target", "bins")
sys.path.insert(0, NR)
import mpmath as mp  # noqa: E402
import taylor_polar as tp  # noqa: E402

mp.mp.dps = 90
CASES = [(2, 1.0, "f64"), (2, 40.0, "f64"), (2, 1.0, "dd"), (2, 40.0, "dd"), (2, 1.0, "qd"), (2, 40.0, "qd"), (4, 300.0, "dd")]


def lead(a, b):
    """leading significant digits that agree: -log10 |a - b| / |a|, capped by the digits printed"""
    a, b = mp.mpf(a), mp.mpf(b)
    if a == b:
        return None, 0.0
    rel = abs(a - b) / abs(a)
    return float(-mp.log10(rel)), float(rel)


def main(out):
    tp.JDIR = None
    tp.MUTATE = None
    rec = {}
    for side in ("off", "on"):
        tp.BIN = os.path.join(BINS, side)
        tp._rows_cache.clear()
        tp._star_cache.clear()
        for l, g, lane in CASES:
            setup, got = tp.get_rows(l, [g], lane, ["base"])
            rec[(side, l, g, lane)] = got[(g, "base")]
    with open(out, "w") as f:
        print(f"{'l':>2} {'gamma':>6} {'lane':>4}  {'rel. difference on vs off':>26}  {'agreeing digits':>16}  D (off)")
        for l, g, lane in CASES:
            a, b = rec[("off", l, g, lane)], rec[("on", l, g, lane)]
            n, rel = lead(a["d"], b["d"])
            row = dict(l=l, gamma=g, lane=lane, d_off=a["d"], d_on=b["d"], rel=rel, digits=n, steps_off=a.get("steps_y"), steps_on=b.get("steps_y"))
            f.write(json.dumps(row) + "\n")
            print(f"{l:>2} {g:>6g} {lane:>4}  {rel:>26.3e}  {'identical' if n is None else f'{n:16.1f}'}  {a['d'][:40]}")


if __name__ == "__main__":
    main(sys.argv[1])
