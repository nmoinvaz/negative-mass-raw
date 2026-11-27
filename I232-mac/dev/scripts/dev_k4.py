import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i232/notes/black_universe")
import numpy as np, linear as L

def profile(c, h=0.01, p_row=8.0, P=16.0, kappa_or_W=None):
    mem = L.ep.Member(c); b = mem.kappa*math.sqrt(2)
    spec = dict(R=(1e-3, 3.0, 0.5), L=(1e-3, 3.0, 0.5))
    su = L.Setup(c, h, P, spec)
    krow = int(round(p_row/h))
    obs = su.observers((0.0,))
    nk = su.Np // krow + 1
    keep = np.zeros((nk, 3, su.Ns + 1))
    Yobs, Yh = L.march_obs(su.UL, su.UR, su.chart.par, su.chart.tab, su.hp, su.hs, obs, su.jh, krow, keep)
    row = keep[1]
    sig = np.arange(su.Ns + 1) * su.hs
    Ys = np.zeros(su.Ns + 1); rhos = np.zeros(su.Ns + 1); g = 0.0
    for i in range(su.Ns + 1):
        Ys[i], g = L.Ynode(row[:, i], p_row, sig[i], su.chart.par, su.chart.tab, g)
        rhos[i] = L.bg(p_row, sig[i], su.chart.par, su.chart.tab, g)[0]
    m = su.chart.m_of_sigma(sig[:su.jh])
    t = (p_row + m) / math.sqrt(2)
    return su, sig[:su.jh], Ys[:su.jh], rhos[:su.jh], t, mem

for c, W in ((-1.0, None), (-1.5, 0.4941711675)):
    su, sig, Y, rho, t, mem = profile(c)
    rate = mem.kappa if W is None else W
    rh = mem.rh
    delta = rho - rh
    Psi = Y * np.exp(-rate * t)
    # slope of ln|Psi| against ln(delta) over delta in [lo, hi]
    for (lo, hi) in ((2e-5, 2e-4), (2e-4, 2e-3), (2e-3, 2e-2)):
        m = (delta > lo) & (delta < hi)
        if m.sum() > 3:
            sl = np.polyfit(np.log(delta[m]), np.log(np.abs(Psi[m])), 1)[0]
            print(f"c={c}: delta in [{lo:g},{hi:g}] ({m.sum()} nodes): d ln|Y e^(-rate t)| / d ln delta = {sl:.4f}")
    if W is None:
        print("   exponents: outgoing branch 1 - W/(2 kappa) = 0.5 ; ingoing branch 1 + W/(2 kappa) = 1.5 (W = kappa)")
    else:
        print("   exponent W/A'(rho_h) =", W/ (2*mem.kappa))
