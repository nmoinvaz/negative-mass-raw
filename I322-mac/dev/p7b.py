import sys, time, math, pickle
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
hs, hb = rm.hs, rm.hb
name = sys.argv[1]; hl = [float(x) for x in sys.argv[2].split(",")]; VMAX = float(sys.argv[3])
Pis = [-0.1, 0.5, 1.0, 2.0]
V0, _, U0, U1 = rm.RECT0
rect = (V0, VMAX, U0, U1)
kc = rm.kchart()
out = {}
for h in hl:
    t = time.time()
    su = hs.KSetup(-1.0, h, *rect, hb.CLASSES[name], kc=kc)
    t1 = time.time()-t
    ro = rm.stream_run(su.UL, su.UR, rect, h, Pis)
    print(f"{name} h={h} rays {t1:.1f}s march {float(ro['wall']):.1f}s", flush=True)
    out[h] = ro
pickle.dump(out, open(f"/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/dev_{name}_b.pkl", "wb"))
