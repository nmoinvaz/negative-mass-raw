"""dev probe p3 (#302): is Y_N' + s F_Pi Y_N = O(s^3) on smooth evolved solutions?  Classes A1R, A1L, A0, L through the Kruskal solver at h = 0.01."""
import math, sys, os, time
import numpy as np
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i302/notes/black_universe"))
_a = sys.argv; sys.argv = sys.argv[:1]
import horizon_sector as hs
import full_slice as fs
sys.argv = _a
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.01
names = sys.argv[2].split(",") if len(sys.argv) > 2 else ["A1R", "A1L", "A0", "L"]
kc = hs.kchart(-1.0)
V0R, U0R = hs.RECT[0], hs.RECT[2]
bg = fs.bgc(-1.0)
def Ygrid(U, j, i):
    V = V0R + j * h; Uc = U0R + i * h
    x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = hs.jetsK(V, Uc, kc.par, kc.tab, 0.0)
    return U[0, j, i] - x * r / math.sqrt(2) * U[2, j, i]
for name in names:
    t0 = time.time()
    su = hs.KSetup(-1.0, h, *hs.RECT, hs.CLASSES[name], kc=kc)
    U = su.run()
    print(name, "wall", round(time.time() - t0, 1))
    rows = []
    for s in (0.0, 0.05, 0.1, 0.15, 0.2, 0.3):
        j = int(round((s - V0R) / h)); i = int(round((-s - U0R) / h))
        f = lambda dj, di: Ygrid(U, j + dj, i + di)
        YN = (-f(2, 2) + 8 * f(1, 1) - 8 * f(-1, -1) + f(-2, -2)) / (12 * h)
        YT = (-f(2, -2) + 8 * f(1, -1) - 8 * f(-1, 1) + f(-2, 2)) / (12 * h)
        b = bg.at(s)
        rows.append((s, f(0, 0), YT, YN, b["Fp"]))
    YN0 = rows[0][3]
    for s, Y, YT, YN, Fp in rows:
        print(f"  s={s:5.2f}  Y={Y: .6e}  Y_T={YT: .6e}  Y_N={YN: .6e}  Y_N/Y_N(0)={YN / YN0 if YN0 else float('nan'): .6f}   1 - F_Pi s^2/2 = {1 - 0.5 * Fp * s * s:.6f}")
