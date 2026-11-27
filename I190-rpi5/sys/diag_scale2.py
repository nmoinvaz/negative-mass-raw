import sys, os
sys.argv = [sys.argv[0]]
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i190/notes/warp"))
import conical_loglog as c
T = os.path.expanduser("~/Source/negative-mass-i190-libs")
orig = c.ll
for arm in ("base", "on"):
    c.BIN_LL = f"{T}/target-crate-{arm}/release/loglog"
    for hs in ("1", "0.999999999", "0.999999", "0.9999", "0.99", "0.9"):
        c.BIN_ID.clear(); c.CACHE.clear()
        c.ll = lambda args, mutate=None, hs=hs: orig(list(args) + ["--hscale", hs], mutate)
        recs, errs = c.plant_run("pl5", c.ex_pl5, "10", 3000, [30, 100, 300, 1000], "dd", "conserve")
        e = recs[-1]
        print(arm, "hscale", hs, "stop", e["stop"], "steps", e["steps"], "x", e["x"], "err", errs[-1][1][1], flush=True)
