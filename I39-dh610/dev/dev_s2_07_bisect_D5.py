import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i39/notes/wormhole_evolution')
import numpy as np, dn
SQ2 = dn.SQ2
W = {2: 1.1819697264877418, 3: 1.727703368738905, 4: 2.1648603980671512}
def run(n, h, A, X, w=0.5, xc=3.0):
    N = int(round(X / h))
    d = dn.ellis_rays(n, N, h, pulses=[dict(field=0, ray='+', A=A, xc=xc, w=w)], symmetric=True)
    return dn.evolve(d, stop=True, store=False)
def fate(res):
    ev = res.events
    return 1 if 'expand' in ev else (-1 if 'collapse' in ev else 0)
def bisect(n, h, X, lo, hi, tol=1e-10):
    flo, fhi = fate(run(n, h, lo, X)), fate(run(n, h, hi, X))
    assert flo == -1 and fhi == 1, (flo, fhi)
    k = 0
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        f = fate(run(n, h, mid, X)); k += 1
        if f == 1: hi = mid
        elif f == -1: lo = mid
        else: raise RuntimeError(f"static through X at A={mid}")
    return lo, hi, k
for n, h, X in ((3, 0.02/np.sqrt(2), 15.0), (3, 0.01/np.sqrt(2), 15.0)):
    t0 = time.time()
    lo, hi, k = bisect(n, h, X, -0.01, 0.01)
    print(f"n={n} h={h}: A* in [{lo:.12e}, {hi:.12e}] after {k} runs, {time.time()-t0:.1f}s")
    for A, name in ((lo, 'collapse side'), (hi, 'expand side')):
        res = run(n, h, A, X)
        dg = res.diag
        H = dg['H']; tau = dg['tau']
        ok = np.isfinite(H) & (np.abs(H) > 0)
        absH = np.abs(H)
        print(f"  {name}: events {res.events} rows {res.rows_done} tau_end {tau[-1]:.2f}, |H| range {np.nanmin(absH[ok]):.2e}..{np.nanmax(absH[ok]):.2e}")
        # local log-slope of |H| vs tau, in windows by |H| level
        lg = np.log(absH[ok]); tt = tau[ok]
        for lo_, hi_ in ((1e-8, 1e-6), (1e-6, 1e-4), (1e-5, 1e-3), (1e-4, 3e-3), (1e-3, 1e-2)):
            m = (absH[ok] >= lo_) & (absH[ok] <= hi_)
            if m.sum() > 5:
                sl = np.polyfit(tt[m], lg[m], 1)[0]
                print(f"    window |H| in [{lo_:.0e}, {hi_:.0e}]: {m.sum()} pts, slope {sl:.5f}  (W = {W[n]:.5f}, rel {sl/W[n]-1:+.2e}), H sign {np.sign(H[ok][m]).mean():+.0f}")
    # untuned
    res = run(n, h, 0.0, X)
    H = res.diag['H']; tau = res.diag['tau']
    idx = np.where(np.abs(H) > 0.01 * W[n])[0]
    print(f"  untuned A=0: events {res.events}, first |H| >= 0.01 W at tau = {tau[idx[0]] if len(idx) else float('nan'):.3f}")
