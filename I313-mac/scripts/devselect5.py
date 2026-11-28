#!/usr/bin/env python3
"""devselect5.py: the selection rule of the raw README (stage 1) of #313 on the stored tunings at h = 0.02.

Candidates: the TUNED lines of I295-mac's and I305-mac's dev/logs (read as stored, not rerun; (3.5, 0.75) is #295's route N and is a reference, not a candidate; the last log of a candidate
replaces an earlier one). The rule (the issue's):
  (a) all three targets (gamma_1 = 0.012, 0.048, 0.075) have a member (a TUNED line with gamma_1 exists only for a stalling point);
  (b) every one of the three leverages is at most 1.0 and the largest is at least 0.43.
Leverage of a point: L = a^T (A^T A)^-1 a, a = (gamma_1, gamma_1^2, rdot_th) of the member at h = 0.02, A the design of the fifteen fitted points at h = 0.005 (the frozen refit's design);
r_th and M are not used and the refit is not evaluated.
Selected: the largest S = L_1 + L_2 + L_3; candidates whose S is within 0.01 of the largest are ordered by the smaller largest |rdot_th| of their three points.
D (smallest distance from the reference curves B, W, C, N, X at the same gamma_1, in units of 1e-3 in r_th and 1e-4 in rdot_th) is printed for information only; it selects nothing.
Prints every candidate; the last line is SELECTED (or 'no candidate')."""
import glob, json, math, os, re, sys
import numpy as np

sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i313/notes/wormhole_evolution"))
import settled_mass_route3 as s3
r = s3.r
RAWROOT = os.path.expanduser("~/Source/negative-mass-raw")
H = 0.02
RDOT_RANGE = (-6.7e-4, 1.6e-3)                  # printed for information (the fitted range of rdot_th), selects nothing
L_MAX, L_MIN, S_TIE = 1.0, 0.43, 0.01
N_ROUTE = (3.5, 0.75)
LOGDIRS = (f"{RAWROOT}/I295-mac/dev/logs", f"{RAWROOT}/I305-mac/dev/logs")

pts15, _ = s3.points15()
g1v, rdv = (np.array([p[k] for p in pts15]) for k in ("g1", "rdot"))
A15 = s3.design(g1v, rdv, "P4")
G15 = np.linalg.inv(A15.T @ A15)
lev15 = np.einsum("ij,jk,ik->i", A15, G15, A15)


def leverage(g1, rdot):
    a = s3.design([g1], [rdot], "P4")[0]
    return float(a @ G15 @ a)


print(f"fitted design (the fifteen at h = 0.005): leverage max {lev15.max():.4f} ({pts15[int(np.argmax(lev15))]['name']}), mean {lev15.mean():.4f}; gamma_1 in [{g1v.min():.5f}, {g1v.max():.5f}], "
      f"rdot_th in [{rdv.min():+.4e}, {rdv.max():+.4e}]; condition number {np.linalg.cond(A15):.2f}")
print("leverage of the fifteen: " + ", ".join(f"{p['name']} {l:.3f}" for p, l in zip(pts15, lev15)))


def tuned(path):
    return [json.loads(l[6:]) for l in open(path) if l.startswith("TUNED")]


fb = r.fam_b(H)
anchor = (float(fb["g1"][0]), float(fb["rth"][0]), float(fb["rdot"][0]))
refs = {"B": dict(g1=fb["g1"], rth=fb["rth"], rdot=fb["rdot"])}
for key, path in (("W", f"{RAWROOT}/I283-mac/dev/logs/tune_xc3.0_w1.0_h0.02.log"), ("C", f"{RAWROOT}/I283-mac/dev/logs/tune_xc4.0_w0.5_h0.02.log"),
                  ("N", f"{RAWROOT}/I295-mac/dev/logs/tune_xc3.5_w0.75_h0.02.log"), ("X", f"{RAWROOT}/I305-mac/dev/logs/tune_xc4.0_w1.5_h0.02.log")):
    rows = [d for d in tuned(path) if "g1" in d]
    pts = sorted([anchor] + [(d["g1"], d["rth"], d["rdot"]) for d in rows])
    refs[key] = dict(g1=np.array([p[0] for p in pts]), rth=np.array([p[1] for p in pts]), rdot=np.array([p[2] for p in pts]))
for k, cv in refs.items():
    print(f"reference {k} at h {H}: gamma_1 " + ", ".join(f"{x:.5f}" for x in cv["g1"]) + "; r_th " + ", ".join(f"{x:.5f}" for x in cv["rth"]) + "; rdot_th " + ", ".join(f"{x:+.2e}" for x in cv["rdot"]))

cands, src = {}, {}
for d_ in LOGDIRS:
    for f in sorted(glob.glob(f"{d_}/tune_xc*_w*_h0.02*.log")):
        mt = re.match(r"tune_xc([0-9.]+)_w([0-9.]+)_h0\.02(\.\d+)?\.log", os.path.basename(f))
        key = (float(mt.group(1)), float(mt.group(2)))
        if key == N_ROUTE:
            continue
        cands[key] = tuned(f)                                    # a later log of the same candidate replaces the earlier
        src[key] = os.path.basename(os.path.dirname(os.path.dirname(f)))
rows_out = []
for (xc, w), rows in sorted(cands.items()):
    good = [d for d in rows if "g1" in d]
    if len(good) != 3:
        print(f"candidate ({xc}, {w}) [{src[(xc, w)]}]: rejected (a), members at {len(good)} of 3 targets: " + "; ".join(f"target {d['target']} {d.get('note', 'member')}" for d in rows))
        continue
    D, L, rd = float("inf"), [], []
    for d in good:
        L.append(leverage(d["g1"], d["rdot"]))
        rd.append(d["rdot"])
        for k, cv in refs.items():
            q = s3.sep3(d["g1"], (d["rth"], d["rdot"]), (d["rth"], d["rdot"]), cv, k=0.0)["q"]
            D = min(D, math.hypot(q["r_th"]["d"] / 1e-3, q["rdot"]["d"] / 1e-4))
    outside = [x for x in rd if x < RDOT_RANGE[0] or x > RDOT_RANGE[1]]
    ok_b1, ok_b2 = max(L) <= L_MAX, max(L) >= L_MIN
    S, big = sum(L), max(abs(x) for x in rd)
    print(f"candidate ({xc}, {w}) [{src[(xc, w)]}]: B " + ", ".join(f"{d['B']:g}" for d in good) + "; gamma_1 " + ", ".join(f"{d['g1']:.5f}" for d in good) + "; rdot_th " + ", ".join(f"{x:+.2e}" for x in rd)
          + f"; leverage " + ", ".join(f"{x:.3f}" for x in L) + f"; S = {S:.3f}, max L = {max(L):.3f}; largest |rdot_th| {big:.2e}; (b) every L <= {L_MAX}: {'ok' if ok_b1 else 'NO'}, max L >= {L_MIN}: {'ok' if ok_b2 else 'NO'}"
          f"; rdot_th outside the fitted range at {len(outside)} of 3 (information); D {D:.2f} (information)")
    if ok_b1 and ok_b2:
        rows_out.append((S, big, xc, w, L, [d["B"] for d in good]))
if rows_out:
    top = max(x[0] for x in rows_out)
    tied = sorted([x for x in rows_out if x[0] >= top - S_TIE], key=lambda x: x[1])
    S, big, xc, w, L, Bs = tied[0]
    print("counting candidates: " + ", ".join(f"({x[2]}, {x[3]}) S {x[0]:.3f}" for x in sorted(rows_out, key=lambda x: -x[0])))
    print(f"SELECTED: (x_c, w) = ({xc}, {w}), S = {S:.3f}, leverage " + ", ".join(f"{x:.3f}" for x in L) + ", B " + ", ".join(f"{x:g}" for x in Bs)
          + (f" (tie within {S_TIE} with {[(x[2], x[3]) for x in tied[1:]]} broken by the smaller largest |rdot_th|)" if len(tied) > 1 else ""))
else:
    print("no candidate")
