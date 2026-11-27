import sys, time, numpy as np
from fs import *
res_all = {}
# ---------- (a)+(b): planted pure gauge through the slice code path ----------
def planted(c, mutP=None, mutL=None, hs_list=(0.01, 0.005, 0.0025), tag=""):
    bg = Bg(c); sl = Slice(bg, mutP)
    xi  = lambda V: (0.3 + 0.7*V + 0.2*V*V + 0.1*V**3, 0.7 + 0.4*V + 0.3*V*V)
    eta = lambda U: (0.03 + 0.5*U - 0.3*U*U + 0.15*U**3, 0.5 - 0.6*U + 0.45*U*U)
    def gf(V, U):
        x, xp = xi(V); e, ep = eta(U)
        return hs.gaugeK(bg.par, bg.tab, V, U, x, xp, e, ep)
    fn = fd_slice_fn(bg, gf)
    # (a) ODE reproduction from s0 = 0.3 to 1.6
    s0, s1 = 0.3, 1.6
    U0, UT0, UN0, _ = fn(s0)
    def dF(s): return fn(s)[0][1]
    def dFT(s): return fn(s)[1][1]
    def dFN(s): return fn(s)[2][1]
    def dphi(s): return fn(s)[0][2]
    def dphiT(s): return fn(s)[1][2]
    def dphiN(s): return fn(s)[2][2]
    solE = solve_ivp(lambda s, y: sl.rhs_even(s, y, dphi(s), dphiT(s), dF(s), dFT(s)), [s0, s1], [UT0[0]*0 + U0[0], UT0[0]], dense_output=True, method="DOP853", rtol=1e-11, atol=1e-16)
    solO = solve_ivp(lambda s, y: [sl.rhs_odd(s, y[0], dphiN(s), dFN(s))], [s0, s1], [UN0[0]], dense_output=True, method="DOP853", rtol=1e-11, atol=1e-16)
    ss = np.linspace(s0, s1, 14)
    ex = np.array([fn(s)[0][0] for s in ss]); exn = np.array([fn(s)[2][0] for s in ss])
    eA = np.max(np.abs(solE.sol(ss)[0] - ex)) / np.max(np.abs(ex)); eB = np.max(np.abs(solO.sol(ss)[0] - exn)) / np.max(np.abs(exn))
    out = dict(ode_even=eA, ode_odd=eB)
    # (b) evolution of the exact slice data (right half, V in [0, 3])
    c2s = None
    errs = []; c2f = {}
    for h in hs_list:
        J = int(round(3.0/h))
        L0, L1 = layers_from_slice(bg, h, J, fn, mutL)
        Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
        # exact horizon values vs march
        H = Ua[0, :, J]; V = h*np.arange(J+1)
        exact = np.array([gf(v, 0.0)[0] for v in V])
        errs.append(np.max(np.abs(H - exact)) / np.max(np.abs(exact)))
        c1f, c2, rr = hs.horizon_fit(H, V); c2f[h] = c2
    out['err'] = errs
    out['ratio'] = [errs[k]/errs[k+1] for k in range(len(errs)-1)]
    # slice functional vs exact: c2 = 1/2 (dr_T + dr_N) at S; exact horizon c2 = d_V dr(V,0) from the exact solution
    U0, UT0, UN0, _ = fn(0.0); c2_slice = 0.5*(UT0[0] + UN0[0])
    v = [gf(m*1e-3, 0.0)[0] for m in (-2, -1, 1, 2)]; c2_exact = (v[0] - 8*v[1] + 8*v[2] - v[3])/(12e-3)
    out['c2_slice'] = c2_slice; out['c2_exact'] = c2_exact; out['c2_fit'] = c2f
    return out
t0 = time.time()
for c in (-1.0, -1.5):
    o = planted(c)
    print(f"[planted c={c}] ODE reproduces dr: {o['ode_even']:.2e}, n: {o['ode_odd']:.2e}; evolution err(h=.01,.005,.0025)={['%.2e'%e for e in o['err']]} ratios {['%.2f'%r for r in o['ratio']]}; c2 slice {o['c2_slice']:.6e} exact {o['c2_exact']:.6e} fit {['%.6e'%v for v in o['c2_fit'].values()]}", flush=True)
print("time", time.time()-t0)
for m in ('H_P', 'H_eps', 'M_phi', 'M_F'):
    o = planted(-1.0, mutP=m, hs_list=(0.01,))
    print(f"[mut {m}] planted ODE reproduces dr: {o['ode_even']:.2e}, n: {o['ode_odd']:.2e}", flush=True)
for m in ('l1_sign', 'l1_noquad'):
    o = planted(-1.0, mutL=m, hs_list=(0.02, 0.01, 0.005))
    print(f"[mut {m}] evolution err {['%.2e'%e for e in o['err']]} ratios {['%.2f'%r for r in o['ratio']]}", flush=True)
