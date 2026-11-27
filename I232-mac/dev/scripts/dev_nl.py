import sys, math, time
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/wormhole_evolution")
import numpy as np, linear as L, evolve as ev, dn
from scipy.interpolate import CubicSpline

def nl_response(su, amp_scale=1.0, tend=None):
    """odd part of the nonlinear diag Y for +/- the linear data, divided by 2: compare with the linear solver at the same data."""
    c, h, N = su.c, su.hp, su.Np
    mem = ev.ep.Member(c)
    rc = su.chart.rho_c
    d0 = ev.member_rays(mem, rc, N, h)
    st = ev.Static(mem, rc, N, h)
    par = ev.params(mem)
    # data on the nonlinear rays: right ray = UR (nodes p_j), left ray = UL interpolated from sigma nodes to the tortoise nodes m_k
    m = np.arange(N + 1) * h
    sg = su.chart.sigma_of_m(m)
    sig_nodes = np.arange(su.UL.shape[1]) * su.hs
    UL_m = np.array([CubicSpline(sig_nodes, su.UL[q])(sg) for q in range(3)])
    UR = su.UR[:, :N + 1]
    out = {}
    for sgn in (+1.0, -1.0):
        Sp = d0.Sp + sgn * amp_scale * UR
        Sm = d0.Sm + sgn * amp_scale * UL_m
        d = dn.Data(2, [-1.0], N, h, Sp, Sm, name="lin")
        res = ev.evolve_dep(d, par, st, stop=False, record=True, tend=tend)
        out[sgn] = res["rec"]
    t = out[1.0]["t"]
    Y = (out[1.0]["Y"] - out[-1.0]["Y"]) / 2.0
    Ye = (out[1.0]["Y"] + out[-1.0]["Y"]) / 2.0
    return t, Y, Ye

h = 0.01
P = 14.0
amp = 1e-6
for c in (-1.5, -1.0):
    for name, spec in (("L pulse", dict(L=(amp, 3.0, 0.5))), ("R pulse", dict(R=(amp, 3.0, 0.5))), ("H a0", dict(a0=amp))):
        su = L.Setup(c, h, P, spec)
        r = su.run(xs=(0.0,))
        tl, yl = r["t"][0], r["Y"][0]
        t0 = time.time()
        tn, yn, ye = nl_response(su)
        ok = np.isfinite(yn)
        sp = CubicSpline(tl[np.isfinite(yl)], yl[np.isfinite(yl)])
        print(f"c={c} {name}: nonlinear wall {time.time()-t0:.1f}s")
        for tt in (4, 6, 8, 10, 12, 14, 16, 18):
            i = np.argmin(abs(tn - tt))
            if not ok[i]: continue
            print(f"    t={tn[i]:6.2f}  Y_lin={sp(tn[i]):+.4e}  Y_nl_odd={yn[i]:+.4e}  ratio={yn[i]/sp(tn[i]):.5f}   even part (drift) {ye[i]:+.2e}")
