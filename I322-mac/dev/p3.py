import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
hs, hb = rm.hs, rm.hb
names = sys.argv[1].split(","); hl = [float(x) for x in sys.argv[2].split(",")]; VMAX = float(sys.argv[3])
Pis = [-0.1, 0.5, 1.0, 2.0]
V0, _, U0, U1 = rm.RECT0
rect = (V0, VMAX, U0, U1)
kc = rm.kchart()
Vq = (1, 2, 3, 5, 8, 12, 16, 20, 30)
for name in names:
    for h in hl:
        su = hs.KSetup(-1.0, h, *rect, hb.CLASSES[name], kc=kc)
        ro = rm.stream_run(su.UL, su.UR, rect, h, Pis)
        cs = rm.c_at_S(ro)
        print(f"== {name} h={h} wall {float(ro['wall']):.1f}s  c1,c2,c2' = {cs[0]:.5e} {cs[1]:.5e} {cs[2]:.5e}", flush=True)
        for k, Pi in enumerate(Pis):
            Vj, wr, ws = rm.remainder_series(ro, k, cs)
            s = []
            for vq in Vq:
                if vq <= Vj[-1] and vq >= Vj[0]:
                    jj = np.argmin(np.abs(Vj - vq))
                    s.append(f"{vq}:{wr[jj]/(cs[1]*Vj[jj]): .3e}")
            print(f"  Pi={Pi:5.2f}  Yrem/(c2 V R)  " + "  ".join(s))
