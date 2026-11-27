#!/usr/bin/env python3
"""diff_summary.py OLD_LOG NEW_LOG: per cell of tests/implicit.rs, the planted error in each log and the ratio (markdown)."""
import re, sys
def cells(path):
    out = {}
    for l in open(path):
        m = re.match(r"\[(?:PASS|FAIL|met|NOT MET)\] (?:\(recorded, not gated\) )?((?:f64|dd|qd|od) \S+ \S+ \S+): (.*)", l)
        if not m:
            m2 = re.match(r"\[(?:PASS|FAIL|met|NOT MET)\] (?:\(recorded, not gated\) )?((?:f64|dd|qd|od) .*?): (.*)", l)
            m = m2
        if not m:
            continue
        key, rest = m.group(1), m.group(2)
        if "control" in key or any(w in key for w in ("WrongStart", "SwitchMid", "WrongForm")):
            continue
        v = None
        for pat in (r"err ([0-9.e+-]+) ", r"position error ([0-9.e+-]+) ", r"\|x_zero\| ([0-9.e+-]+),", r"relative error of c_k.*?: ([0-9.e+-]+) ", r"h.k\) ([0-9.e+-]+) \(bar 1e6"):
            mm = re.search(pat, rest)
            if mm:
                v = float(mm.group(1)); break
        kind = ("crossings" if "crossings found" in rest else "step_sum" if "h^k" in rest else "coeffs" if "c_k" in rest
                else "fold" if "x_zero" in rest else "closed_form" if "stop" in rest and "err" in rest else "other")
        if v is not None:
            out[(kind, key)] = v
    return out
a, b = cells(sys.argv[1]), cells(sys.argv[2])
print("| check | cell | old | new | new / old |")
print("|---|---|---|---|---|")
moved = 0
for k in sorted(a):
    if k in b and a[k] > 0 and b[k] > 0:
        r = b[k] / a[k]
        if r > 3 or r < 1 / 3:
            moved += 1
            print(f"| {k[0]} | {k[1]} | {a[k]:.2e} | {b[k]:.2e} | {r:.2g} |")
print(f"\ncells compared: {len([k for k in a if k in b])}; cells whose value moved by more than a factor 3: {moved}")
for kind in ("closed_form", "crossings", "step_sum", "fold", "coeffs"):
    for lane in ("f64", "dd", "qd"):
        va = [v for (kd, key), v in a.items() if kd == kind and key.startswith(lane + " ") and "Conserve" not in key or False]
        vb = [v for (kd, key), v in b.items() if kd == kind and key.startswith(lane + " ") and "Conserve" not in key or False]
        if va and vb:
            print(f"- {kind} {lane} (Project/gated-like cells): worst old {max(va):.2e}, worst new {max(vb):.2e}")
