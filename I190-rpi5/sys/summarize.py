#!/usr/bin/env python3
"""summarize.py LOG: tables of the planted checks of tests/implicit.rs from a test log (prints markdown)."""
import re, sys, collections
log = open(sys.argv[1]).read().splitlines()
cells = []
for l in log:
    m = re.match(r"\[(PASS|FAIL|met|NOT MET)\] (\(recorded, not gated\) )?(.*)", l)
    if m:
        cells.append((m.group(1), bool(m.group(2)), m.group(3)))
def lane(t): return t.split()[0]
rows = collections.defaultdict(lambda: [0, 0, 0, 0])  # lane, kind -> met gated, not met gated, met rec, not met rec
for st, rec, t in cells:
    if t.startswith("control") or t.startswith("lanes") or t.startswith("Fl") or any(w in t for w in ("WrongStart", "SwitchMid", "WrongForm")):
        continue
    parts = t.split()
    if parts[0] not in ("f64", "dd", "qd", "od"):
        continue
    if "crossings found" in t: kind = "crossings"
    elif "worst sum|dc_k|" in t: kind = "step_sum"
    elif "relative error of c_k" in t: kind = "coeffs"
    elif "x_zero" in t or "no estimate" in t: kind = "fold"
    elif "ZeroPivot" in t and "state finite" in t: kind = "zero_pivot"
    elif "planner" in t: kind = "planner"
    elif "stop" in t and "err" in t: kind = "closed_form"
    else: continue
    ok = st in ("PASS", "met")
    r = rows[(parts[0], kind)]
    r[(2 if rec else 0) + (0 if ok else 1)] += 1
print("| lane | check | met (gated) | not met (gated) | met (recorded) | NOT MET (recorded) |")
print("|---|---|---|---|---|---|")
for (ln, kind), r in sorted(rows.items(), key=lambda kv: (["f64", "dd", "qd", "od"].index(kv[0][0]), kv[0][1])):
    print(f"| {ln} | {kind} | {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
def worst(pat, lane_):
    v = []
    for st, rec, t in cells:
        if t.split()[0] == lane_ and not rec and not any(w in t for w in ("WrongStart", "SwitchMid", "WrongForm", "control")):
            m = re.search(pat, t)
            if m:
                v.append(float(m.group(1)))
    return max(v) if v else float("nan")
print()
print("worst gated values:")
for ln in ("f64", "dd", "qd", "od"):
    ce = worst(r"stop End.* err ([0-9.e+-]+) ", ln)
    cr = worst(r"worst position error ([0-9.e+-]+) ", ln)
    ss = worst(r"h.k\) ([0-9.e+-]+) \(bar 1e6", ln)
    print(f"- {ln}: closed_form err {ce:.2e}; crossings position error {cr:.2e}; step_sum ratio {ss:.2e}")
for l in log:
    if l.startswith("digest"): print(l)
