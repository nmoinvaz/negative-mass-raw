#!/usr/bin/env python3
"""make_jobs.py DEVRUNS OUT: the job file of the runs of record, one line "B XC W H LO HI" per (point, h). The bracket of each of the six points is the one the development
set's bisection started from (the first two amplitudes of its points.jsonl: the bracket scan's), so the runs of record take the same bisection path and are equal to the development
set bit for bit; the reproduction point takes #266's bracket (0.005, 0.03), so its p*_h is #266's. h = 0.005 first (the longest jobs start earliest)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i283/notes/wormhole_evolution"))
import settled_mass_route as r
root, out = sys.argv[1], sys.argv[2]
lines = []
for h in (0.005, 0.01):
    for nm, spec, tg in list(r.POINTS) + [r.REP]:
        if nm == "REP":
            lo, hi = 0.005, 0.03
        else:
            pts = [json.loads(l) for l in open(os.path.join(root, r.tag_of("G", spec), f"h{h:g}", "pstar", "points.jsonl"))][:2]
            lo, hi = pts[0]["A"], pts[1]["A"]
        lines.append(f"{spec[0]:g} {spec[1]:g} {spec[2]:g} {h:g} {lo!r} {hi!r}")
open(out, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
