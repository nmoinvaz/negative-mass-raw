"""P8: where is the pointwise error of the planted static mode through march_K (h = 0.005)?"""
import os, sys, math
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i259/notes/black_universe"))
_a = sys.argv; sys.argv = sys.argv[:1]
import numpy as np
import static_c1 as sc
sys.argv = _a
hs = sc.hs
h = float(sys.argv[1]) if len(sys.argv) > 1 else 0.005
amp = 2e-3
kc = hs.kchart(sc.C)
UL, UR = sc.mode_arrays(h, amp)
U = hs.march_K(UL, UR, sc.V0R, sc.U0R, kc.par, kc.tab, h, h)
m = sc.mode()
st = max(1, int(round(0.05 / h)))
worst = {}
for j in range(0, U.shape[1], st):
    for i in range(0, U.shape[2], st):
        V, Uc = sc.V0R + j * h, sc.U0R + i * h
        Pi = -V * Uc
        if Pi < -0.24:
            continue
        f = m.fields(Pi)
        ex = amp * np.array([f[0], f[3], f[2]])
        e = np.abs(U[:, j, i] - ex)
        for q in range(3):
            if e[q] > worst.get(q, (0,))[0]:
                worst[q] = (e[q], V, Uc, Pi, ex[q])
for q, nm in enumerate(("dr", "dF", "dphi")):
    e, V, Uc, Pi, ex = worst[q]
    print(f"{nm}: max err {e:.3e} at V={V:.3f} U={Uc:.3f} Pi={Pi:.4f} (exact {ex:.4e})")
# error along the horizon U = 0 and on the slice
ih = int(round(-sc.U0R / h))
for V in (0.0, 0.5, 1.0, 2.0, 3.0):
    j = int(round((V - sc.V0R) / h))
    f = m.fields(0.0)
    ex = amp * np.array([f[0], f[3], f[2]])
    print(f"horizon V={V}: U-ex = {U[:, j, ih] - ex}")
