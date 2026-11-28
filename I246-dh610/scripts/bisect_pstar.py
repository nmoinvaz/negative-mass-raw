#!/usr/bin/env python3
"""Bisection of the fate of family G at D = 6 at h = 0.00125 (the third h of #40's set, not run there), with #40's own threshold.py unchanged:
th.bisect(th.point, ...) over #40's declared bracket (0.005, 0.03) to hi - lo <= 1e-14, X as #40's job (28.0). No series, no stall runs.
Writes RAW/runs/pstar_D6_G_k2.json in the format of settled_mass_d56.py `pstar` (so `job --k=2` reads it) and runs/pstar_D6_G_k2.points.jsonl.
    python3 bisect_pstar.py            (run from notes/wormhole_evolution of the checkout)
"""
import json
import os
import platform
import subprocess
import sys
import time

here = os.path.expanduser("~/Source/negative-mass-i246/notes/wormhole_evolution")
sys.path.insert(0, here)
import threshold as th  # noqa: E402

n, fam, k = 4, "G", 2
h = th.CRIT["H"][n][k]                  # the h exactly as #40's job takes it
X = th.CRIT["X"][fam][n]
lo, hi = th.CRIT["bracket"][fam]
out = os.path.expanduser("~/Source/negative-mass-raw/I246-dh610/runs")
sink = th.Sink(os.path.join(out, "pstar_D6_G_k2.points.jsonl"))
commit = subprocess.run(["git", "-C", here, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
dirty = subprocess.run(["git", "-C", here, "status", "--porcelain", "--", "threshold.py", "dn.py", "checks.py"], capture_output=True, text=True).stdout.strip()
print(f"bisect_pstar: D = {n + 2}, family {fam}, h = {h!r}, X = {X}, bracket ({lo}, {hi}), tol {th.CRIT['bisect_tol']}, {platform.node()}, commit {commit}, "
      f"threshold/dn/checks modified: {bool(dirty)}, {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)
t0 = time.time()
lo_, hi_, stopped = th.bisect(lambda p: th.point(n, fam, h, X, p), lo, hi, th.CRIT["bisect_tol"], sink)
secs = round(time.time() - t0, 1)
res = dict(n=n, D=n + 2, fam=fam, k=k, h=h, h_job_log=repr(h), lo=lo_, hi=hi_, ps=0.5 * (lo_ + hi_), stopped=stopped, X=X, event=None, T=None, M_hor=None,
           source="bisected in #246 on " + platform.node() + " with threshold.py (#40) unchanged; #40 has no job for this h", machine=platform.node(), commit=commit,
           threshold_dn_checks_modified=bool(dirty), bisect_secs=secs, runs=sum(1 for _ in open(os.path.join(out, "pstar_D6_G_k2.points.jsonl"))), bracket=[lo, hi],
           finished=time.strftime("%Y-%m-%d %H:%M:%S"))
json.dump(res, open(os.path.join(out, "pstar_D6_G_k2.json"), "w"), indent=1)
print(json.dumps(res), flush=True)
