import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
import remainder as rm
hs, hb = rm.hs, rm.hb
h = 0.01
rect = hb.RECT_H
kc = hs.kchart(-1.0)
su = hs.KSetup(-1.0, h, *rect, hb.CLASSES["A0"], kc=kc)
t=time.time(); U = su.run(); print("march_K", time.time()-t, U.shape)
ih = int(round(-rect[2]/h)); jS = int(round(-rect[0]/h))
Pis = np.array([-0.1, 0.5, 1.0])
t=time.time()
hp, win, ilo, snaps = rm.march_stream(su.UL, su.UR, rect[0], rect[2], kc.par, kc.tab, h, 1e9, ih, Pis, rm.NW, np.array([jS, 10, 200], dtype=np.int64))
print("stream", time.time()-t)
t=time.time()
hp, win, ilo, snaps = rm.march_stream(su.UL, su.UR, rect[0], rect[2], kc.par, kc.tab, h, 1e9, ih, Pis, rm.NW, np.array([jS, 10, 200], dtype=np.int64))
print("stream 2nd", time.time()-t)
print("hp diff", np.abs(hp - U[:, :, ih]).max())
for n, j in enumerate([jS, 10, 200]):
    print("snap", j, np.abs(snaps[n] - U[:, j, :]).max())
# window check
bad = 0; cnt = 0
for j in range(U.shape[1]):
    for k in range(3):
        if ilo[j, k] >= 0:
            cnt += 1
            i0 = ilo[j, k]
            V = rect[0] + j*h
            for m in range(8):
                Uu = rect[2] + (i0+m)*h
                x, d, r = hs.jetsK(V, Uu, kc.par, kc.tab, 0.0)[:3]
                u = (U[0, j, i0+m] - x*r/math.sqrt(2)*U[2, j, i0+m])/r
                if abs(u - win[j,k,m]) > 1e-14: bad += 1
print("windows", cnt, "bad", bad)
# trapezoid
hp2, win2, ilo2, snaps2 = rm.march_stream(su.UL, su.UR, rect[0], rect[2], kc.par, kc.tab, h, 0.15, ih, Pis, rm.NW, np.array([jS], dtype=np.int64))
print("cap0.15: hp diff", np.abs(hp2 - hp).max(), "win diff", np.nanmax(np.abs(win2-win)), "ilo equal", (ilo2==ilo).mean())
