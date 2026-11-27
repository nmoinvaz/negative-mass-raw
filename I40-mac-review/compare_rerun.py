#!/usr/bin/env python3
"""Compares the coordinator's rerun jobs (rerun/) with the runner's (I40-dh610/runs): p*_h, and fate and event cell of
each series point with e <= 9. Exits non-zero when an expectation of README.md's "Rerun" fails."""
import json, os, sys
R = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.expanduser("~/Source/negative-mass-raw/I40-dh610/runs")
bad = 0
for name in sorted(os.listdir(os.path.join(R, sys.argv[1] if len(sys.argv) > 1 else "rerun_cmp"))):
    d = os.path.join(R, sys.argv[1] if len(sys.argv) > 1 else "rerun_cmp", name)
    if not os.path.isdir(d):
        continue
    a, b = json.load(open(os.path.join(d, "summary.json"))), json.load(open(os.path.join(RAW, name, "summary.json")))
    pa, pb = 0.5 * (a["lo"] + a["hi"]), 0.5 * (b["lo"] + b["hi"])
    ser = lambda p: {(r["side"], r["e"]): r for r in map(json.loads, open(os.path.join(p, "points.jsonl"))) if r.get("phase") == "series"}
    sa, sb = ser(d), ser(os.path.join(RAW, name))
    keys = sorted(k for k in sb if k[1] <= 9.0)
    diff = [k for k in keys if k not in sa or (sa[k]["fate"], sa[k]["j"], sa[k]["i"]) != (sb[k]["fate"], sb[k]["j"], sb[k]["i"])]
    deep = [k for k in sorted(sb) if k[1] > 9.0 and (k not in sa or (sa[k]["fate"], sa[k]["j"], sa[k]["i"]) != (sb[k]["fate"], sb[k]["j"], sb[k]["i"]))]
    ok = abs(pa - pb) <= 1e-11 and not diff and a["status"] == "done"
    bad += not ok
    print(f"{'ok ' if ok else 'BAD'} {name}: p*_h {pa:.15e} against {pb:.15e} (diff {pa - pb:+.1e}); {len(keys) - len(diff)} of {len(keys)} "
          f"points with e <= 9 equal; e > 9 differing: {deep}")
print(f"{bad} jobs differ from the expectation")
sys.exit(1 if bad else 0)
