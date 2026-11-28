import sys; sys.path.insert(0, ".")
import numpy as np
from fam import Fam
np.set_printoptions(linewidth=160)
for c in (-1.0, -1.5):
    f = Fam(c, 1.0)
    print("== c =", c, "K =", f.K, "rho_h =", f.rhoh())
    rr = np.linspace(-6, 8, 57)
    print("rho     A        A'       s_AH")
    for r in rr:
        print(f"{r:7.3f} {f.A(r):9.4f} {f.Ap(r):9.4f} {f.sAH(r):12.5g}")
    # zeros of A'
    from scipy.optimize import brentq
    xs = np.linspace(-8, 8, 4001); ys = f.Ap(xs)
    z = [brentq(f.Ap, xs[i], xs[i+1]) for i in range(len(xs)-1) if ys[i]*ys[i+1] < 0]
    print("zeros of A':", z, " A there:", [f.A(q) for q in z])
