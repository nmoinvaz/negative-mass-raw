#!/usr/bin/env python3
"""fitq_diag.py RAW_SET_A: diagnosis of FITQ (development). For every stored member at h = 0.005 that has member rows (#266's B, #267's delta, #283's W and C, #295's N, this folder's X): the rms of the
fit of M(r) by a static member (#225's fit_asym, as the analysis's FITQ: the largest rms_m among rows with |t - t_dep| <= 0.5), with gamma_1, r_th - 1 and rdot_th at departure. Then rms_m against t for X2 and X3."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i305/notes/wormhole_evolution"))
import settled_mass_route4 as s4
s3, r, b, m = s4.s3, s4.r, s4.b, s4.m
H = 0.005
raw = sys.argv[1]
rows = []


def rms_at(d, t_dep):
    v = [x["rms_m"] for x in d["m"]["rows"] if abs(x["t"] - t_dep) <= 0.5]
    return max(v) if v else float("nan")


R = m.load266(H)
for B in (0.0, 0.025, 0.05, 0.1, 0.125):
    e = R[B]["e"]
    mem = R[B]["mem"]
    rows.append((f"B{B:g}", "B", mem["g1"], mem["r_th"], R[B]["speed"], rms_at(e, mem["t_dep"])))
for ee in s3.E_267:
    base = os.path.join(s3.I267, "runs", m.TAG, f"h{H:g}", f"e{ee:g}")
    d = dict(e=ee, h=H, m=json.load(open(base + "/member/member.json")), loc=dict(np.load(base + "/member/locus.npz")))
    mem = b.member_at(d, 1e-3, "m")
    rows.append((f"e{ee}", "D", mem["g1"], mem["r_th"], m.speed_at(d["loc"], mem["t_dep"]), rms_at(d, mem["t_dep"])))
for nm, spec in s3.POINTS_283:
    e = r.load_point(os.path.join(s3.I283, "runs"), spec, H)
    x = r.read_point(e)
    rows.append((nm, nm[0], x["mem"]["g1"], x["mem"]["r_th"], x["sp"], rms_at(e, x["mem"]["t_dep"])))
for nm, spec, _ in s3.POINTS3:
    e = r.load_point(os.path.join(s4.I295, "runs"), spec, H)
    x = r.read_point(e)
    rows.append((nm, "N", x["mem"]["g1"], x["mem"]["r_th"], x["sp"], rms_at(e, x["mem"]["t_dep"])))
XS = {}
for nm, spec, _ in s4.POINTS4:
    e = r.load_point(os.path.join(raw, "runs"), spec, H)
    x = r.read_point(e)
    XS[nm] = (e, x)
    rows.append((nm, "X", x["mem"]["g1"], x["mem"]["r_th"], x["sp"], rms_at(e, x["mem"]["t_dep"])))
print("point  route  gamma_1   r_th - 1    rdot_th     rms(fit) at departure   (bar 1e-4)")
for nm, rt, g1, rth, sp, rms in rows:
    print(f"{nm:6s} {rt:3s}  {g1:.5f}  {rth - 1:+.5f}  {sp:+.3e}  {rms:.2e}  {'ABOVE' if rms > 1e-4 else ''}")
a = np.array([[x[2], x[3] - 1, x[4], x[5]] for x in rows])
for j, nmj in ((0, "gamma_1"), (1, "r_th - 1"), (2, "rdot_th")):
    print(f"correlation of rms with |{nmj}| over {len(rows)} points: {np.corrcoef(np.abs(a[:, j]), a[:, 3])[0, 1]:+.3f}")
for nm in ("X2", "X3"):
    e, x = XS[nm]
    print(f"\n{nm}: rms_m of the member fit against t (rows every 0.5), t_dep = {x['mem']['t_dep']:.3f}, rdot_th = {x['sp']:+.3e}")
    print("  " + ", ".join(f"{q['t']:.1f}: {q['rms_m']:.1e}" for q in e["m"]["rows"] if 6.0 <= q["t"] <= 16.0))
