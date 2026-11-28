import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
hs, hb = rm.hs, rm.hb
name = sys.argv[1]; h = float(sys.argv[2]); VMAX = float(sys.argv[3])
Pis = [-0.1, 0.5, 1.0, 2.0]
V0, _, U0, U1 = rm.RECT0
rect = (V0, VMAX, U0, U1)
kc = rm.kchart()
t = time.time()
su = hs.KSetup(-1.0, h, *rect, hb.CLASSES[name], kc=kc)
print("rays", time.time()-t)
ro = rm.stream_run(su.UL, su.UR, rect, h, Pis)
print("march", float(ro["wall"]))
cs = rm.c_at_S(ro)
print("c1,c2,c2'", cs)
hp = ro["hp"]; V = ro["V"]
c1f, c2f, res = hs.horizon_fit(hp[0], V)
print("fit on all V:", c1f, c2f, res)
m = V < 3.0
print("fit on V<3:", hs.horizon_fit(hp[0][m], V[m]))
for k, Pi in enumerate(Pis):
    rho, R = rm.rho_of_Pi(Pi)
    Vj, wr, ws = rm.remainder_series(ro, k, cs)
    print(f"--- Pi={Pi} rho={rho:.4f} R={R:.4f}  valid V in [{Vj[0]:.3f},{Vj[-1]:.3f}]")
    for Vq in (0.5, 1, 2, 3, 5, 8, 12, 16, 20, 25, 30):
        if Vq <= Vj[-1]:
            jj = np.argmin(np.abs(Vj - Vq))
            print(f"  V={Vj[jj]:7.3f}  Yrem/R={wr[jj]: .4e}  c2 V={cs[1]*Vj[jj]: .4e}  ratio={wr[jj]/(cs[1]*Vj[jj]): .3e}")
