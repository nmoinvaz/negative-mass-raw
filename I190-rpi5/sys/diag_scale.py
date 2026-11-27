import sys, os
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i190/notes/warp"))
import conical_loglog as c
T = os.path.expanduser("~/Source/negative-mass-i190-libs")
for arm in ("base", "on"):
    c.BIN_LL = f"{T}/target-crate-{arm}/release/loglog"
    c.BIN_ID.clear(); c.CACHE.clear()
    for prec, mode in (("dd", "conserve"), ("qd", "conserve"), ("dd", "project"), ("qd", "project")):
        recs, errs = c.plant_run("pl5", c.ex_pl5, "10", 3000, [30, 100, 300, 1000], prec, mode)
        e = recs[-1]
        print(arm, prec, mode, "stop", e["stop"], "steps", e["steps"], "x", e["x"], "err_last", errs[-1][1][1])
