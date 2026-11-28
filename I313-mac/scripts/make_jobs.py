#!/usr/bin/env python3
"""make_jobs.py DEVRUNS OUT_REC OUT_REP: the job files of the runs of record, one line "B XC W H LO HI" per (point, h). The bracket of each new point is the one the development set's bisection
started from (the first two amplitudes of its points.jsonl: the bracket scan's), so the runs of record take the same bisection path and are equal to the development set bit for bit. The
reproduction point (#305's X2, h = 0.005) takes the bracket of #305's stored run (its first two amplitudes). h = 0.005 first (the longest jobs start earliest)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i313/notes/wormhole_evolution"))
import settled_mass_route5 as s5
r = s5.r
root, out_rec, out_rep = sys.argv[1], sys.argv[2], sys.argv[3]


def bracket(base):
    pts = [json.loads(l) for l in open(os.path.join(base, "pstar", "points.jsonl"))][:2]
    return pts[0]["A"], pts[1]["A"]


lines = []
for h in (0.005, 0.01):
    for nm, spec, tg in s5.POINTS5:
        lo, hi = bracket(os.path.join(root, "runs", r.tag_of("G", spec), f"h{h:g}"))
        lines.append(f"{spec[0]:g} {spec[1]:g} {spec[2]:g} {h:g} {lo!r} {hi!r}")
open(out_rec, "w").write("\n".join(lines) + "\n")
spec = s5.REP5[1]
lo, hi = bracket(os.path.join(s5.I305, "runs", r.tag_of("G", spec), "h0.005"))
rep = f"{spec[0]:g} {spec[1]:g} {spec[2]:g} 0.005 {lo!r} {hi!r}"
open(out_rep, "w").write(rep + "\n")
print("\n".join(lines + [rep]))
