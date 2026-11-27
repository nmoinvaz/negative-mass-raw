import sys, time, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np
import linear as L

def run(c, hp, hs, P=4.0, sigmax=None):
    ch = L.Chart(c, rho_c=1.0, sig_star=16.0, p_max=P)
    smax = ch.sigma_max(P) if c != 0 else 6.0
    if c != 0:
        Ns = int(round(smax / hs)); 
    else:
        Ns = int(round(6.0/hs))
    Np = int(round(P / hp))
    xi_f = lambda p: (0.01*math.sin(0.7*p+0.3), 0.01*0.7*math.cos(0.7*p+0.3))
    eta_f = lambda s: (0.02*math.cos(0.5*s)+0.01, -0.02*0.5*math.sin(0.5*s))
    Uex = L.gauge_arrays(ch, hp, hs, Np, Ns, xi_f, eta_f)
    UL = np.ascontiguousarray(Uex[:, 0, :]); UR = np.ascontiguousarray(Uex[:, :, 0])
    t0 = time.time()
    U = L.march_full(UL, UR, ch.par, ch.tab, hp, hs)
    err = np.abs(U - Uex).max(axis=(1, 2))
    return err, time.time()-t0, Ns, Np, smax if c != 0 else 6.0

for c in (-1.5, -1.0, -0.3, 0.0):
    print("c =", c)
    prev = None
    for h in (0.04, 0.02, 0.01):
        # for the horizon chart sigma* must be a node: 16 / h integer
        e, t, Ns, Np, smax = run(c, h, h)
        print(f"  h={h}: max err (dr, df, dphi) = {e}, time {t:.2f}s, Ns={Ns}, Np={Np}, sigma_max={smax:.4f}")
        if prev is not None:
            print("      ratios:", prev / e)
        prev = e
