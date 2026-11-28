#!/usr/bin/env python3
"""devselect.py DEVLOGS: the selection rule of the raw README (stage 1) on the development tuning at h = 0.02. For each candidate (x_c, w) read the TUNED lines of its log (the last
log of the candidate); a candidate counts if all three targets have a member (the stall filter is the tuning's: a TUNED line with a member exists only for a stalling point). D = min over
the three gamma_1 and the three reference curves (family B, route W, route C at h = 0.02) of sqrt((dr_th / 1e-3)^2 + (drdot_th / 1e-4)^2), each difference the smaller of the piecewise-linear
and PCHIP interpolations at the candidate's gamma_1 (extrapolated beyond the last point). The largest D wins."""
import glob, json, math, os, re, sys
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i295/notes/wormhole_evolution"))
import settled_mass_route3 as s3
r = s3.r
dev = sys.argv[1]
H = 0.02
fb = r.fam_b(H)
anchor = (float(fb["g1"][0]), float(fb["rth"][0]), float(fb["rdot"][0]))
refs = {"B": dict(g1=fb["g1"], rth=fb["rth"], rdot=fb["rdot"])}
for key, lg in (("W", "tune_xc3.0_w1.0_h0.02.log"), ("C", "tune_xc4.0_w0.5_h0.02.log")):
    rows = [json.loads(l[6:]) for l in open(os.path.expanduser("~/Source/negative-mass-raw/I283-mac/dev/logs/" + lg)) if l.startswith("TUNED")]
    pts = sorted([(anchor[0], anchor[1], anchor[2])] + [(d["g1"], d["rth"], d["rdot"]) for d in rows])
    refs[key] = dict(g1=np.array([p[0] for p in pts]), rth=np.array([p[1] for p in pts]), rdot=np.array([p[2] for p in pts]))
for k, cv in refs.items():
    print(f"reference {k} at h {H}: gamma_1 " + ", ".join(f"{x:.5f}" for x in cv["g1"]) + "; r_th " + ", ".join(f"{x:.5f}" for x in cv["rth"]) + "; rdot_th " + ", ".join(f"{x:+.2e}" for x in cv["rdot"]))
cands = {}
for f in sorted(glob.glob(dev + "/tune_xc*_w*_h0.02*.log")):
    mt = re.match(r"tune_xc([0-9.]+)_w([0-9.]+)_h0\.02(\.\d+)?\.log", os.path.basename(f))
    key = (float(mt.group(1)), float(mt.group(2)))
    cands[key] = [json.loads(l[6:]) for l in open(f) if l.startswith("TUNED")]          # a later log of the same candidate replaces the earlier
best = None
for (xc, w), rows in sorted(cands.items()):
    good = [d for d in rows if "g1" in d]
    if len(good) != 3:
        print(f"candidate ({xc}, {w}): rejected, members at {len(good)} of 3 targets: " + "; ".join(f"target {d['target']} {d.get('note', 'member')}" for d in rows))
        continue
    D, det = float("inf"), []
    for d in good:
        for k, cv in refs.items():
            s_ = s3.sep3(d["g1"], (d["rth"], d["rdot"]), (d["rth"], d["rdot"]), cv, k=0.0)
            q = s_["q"]
            dr, dv = q["r_th"]["d"], q["rdot"]["d"]
            dd = math.hypot(dr / 1e-3, dv / 1e-4)
            D = min(D, dd)
            det.append(f"{d['target']:g}/{k}: ({dr:.1e}, {dv:.1e}) -> {dd:.2f}")
    print(f"candidate ({xc}, {w}): B " + ", ".join(f"{d['B']:g}" for d in good) + "; gamma_1 " + ", ".join(f"{d['g1']:.5f}" for d in good) + "; r_th " + ", ".join(f"{d['rth']:.5f}" for d in good) + "; rdot_th " + ", ".join(f"{d['rdot']:+.2e}" for d in good) + f"; D = {D:.3f}")
    print("      " + "; ".join(det))
    if best is None or D > best[0]:
        best = (D, xc, w)
print(f"SELECTED: (x_c, w) = ({best[1]}, {best[2]}), D = {best[0]:.3f}" if best else "no candidate")
