#!/usr/bin/env python3
"""make_jobs_rn.py RECRUNS OUT: the job file of the second roundoff realization: the three new points at h = 0.005 with the bracket (0.98 p*_h, 1.02 p*_h) around the record's p*_h, so the
bisection takes another path to the same p*_h (as #305's)."""
import json, os, sys
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i313/notes/wormhole_evolution"))
import settled_mass_route5 as s5
r = s5.r
root, out = sys.argv[1], sys.argv[2]
lines = []
for nm, spec, tg in s5.POINTS5:
    ps = json.load(open(os.path.join(root, r.tag_of("G", spec), "h0.005", "pstar", "summary.json")))["ps"]
    lines.append(f"{spec[0]:g} {spec[1]:g} {spec[2]:g} 0.005 {0.98 * ps!r} {1.02 * ps!r}")
open(out, "w").write("\n".join(lines) + "\n")
print("\n".join(lines))
