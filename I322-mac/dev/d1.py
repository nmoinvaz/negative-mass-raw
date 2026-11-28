import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
rm.CACHE = "/private/tmp/claude-501/-Users-nathan-Source-negative-mass-i322/07a7c86f-beae-4b72-bf6b-2793fd26190f/scratchpad/cache"
hl = [float(x) for x in sys.argv[1].split(",")]
# closed form
cf = rm.closed_form()
print("I0", cf["I0"], "vs", rm.I0_262, "rel", cf["I0"]/rm.I0_262-1)
# exact growing mode
for kind in ("g", "d"):
    t = time.time()
    ros = [rm.run_exact(kind, h) for h in hl]
    print(kind, "runs", time.time()-t, [float(r["wall"]) for r in ros])
    for ro, h in zip(ros, hl):
        cs = rm.c_read(ro, kind)
        print(f"  {kind} h={h} cs = {cs}")
        for k, Pi in enumerate(rm.PIS_ALL):
            j, V, w = rm.series(ro, k, cs if kind=="g" else (cs[0], 0.0, cs[2]) if False else cs)
            if len(V):
                if kind == "g":
                    rat = np.abs(w)/(abs(cs[1])*V)
                    m = (V>=8)&(V<=24)
                    print(f"     Pi={Pi}: max |Yrem/R|/(c2 V) over V in [8,24] = {rat[m].max():.3e}  (valid V {V[0]:.2f}..{V[-1]:.2f})")
                else:
                    m = (V>=4)&(V<=18*Pi)
                    if m.any():
                        # decaying: the remainder is c2' U R already subtracted -> should be ~0; compare to c2' U*
                        rat = np.abs(w)/(abs(cs[2])*Pi/V)
                        print(f"     Pi={Pi}: max |Yrem/R|/|c2' U*| over V in [4,{18*Pi:.0f}] = {rat[m].max():.3e}  (valid V {V[0]:.2f}..{V[-1]:.2f})")
