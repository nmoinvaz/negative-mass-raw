import sys, time, numpy as np
from fs import *
# ---- planted evolution error with the slice scale as normalization; mutations of the layer-1 initializer
def planted_evo(c, mutL=None, hs_list=(0.02, 0.01, 0.005)):
    bg = Bg(c)
    xi  = lambda V: (0.3 + 0.7*V + 0.2*V*V + 0.1*V**3, 0.7 + 0.4*V + 0.3*V*V)
    eta = lambda U: (0.03 + 0.5*U - 0.3*U*U + 0.15*U**3, 0.5 - 0.6*U + 0.45*U*U)
    def gf(V, U):
        x, xp = xi(V); e, ep = eta(U)
        return hs.gaugeK(bg.par, bg.tab, V, U, x, xp, e, ep)
    fn = fd_slice_fn(bg, gf)
    errs = []
    for h in hs_list:
        J = int(round(3.0/h))
        L0, L1 = layers_from_slice(bg, h, J, fn, mutL)
        Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
        # compare the whole triangle with the exact solution at a sample of nodes (every 20th)
        e = 0.0; scale = np.max(np.abs(L0[0]))
        for j in range(0, J + 1, max(1, J // 15)):
            for i in range(-j, 1, max(1, j // 6 + 1)):
                ex = gf(j*h, i*h)
                e = max(e, np.max(np.abs(Ua[:, j, i + J] - ex)))
        errs.append(e/scale)
    return errs, [errs[k]/errs[k+1] for k in range(len(errs)-1)]
for c in (-1.0, -1.5):
    e, r = planted_evo(c); print(f"[planted evo c={c}] err/scale {['%.2e'%x for x in e]} ratios {['%.2f'%x for x in r]}", flush=True)
for m in ('l1_sign', 'l1_noquad'):
    e, r = planted_evo(-1.0, m); print(f"[mut {m}] err/scale {['%.2e'%x for x in e]} ratios {['%.2f'%x for x in r]}", flush=True)

# ---- datum G: independent constraint residuals of the evolved solution, and the diamond
bg = Bg(-1.0); sl = Slice(bg)
SL, SR = -1.05, 1.05
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
A0 = sl.even(SL, SR, seed_phi.f, seed_phi.fT, (0, 0), max_step=0.01).y[0, -1]; Ac = sl.even(SL, SR, corr_phi.f, corr_phi.fT, (0, 0), max_step=0.01).y[0, -1]
N0 = sl.odd(SL, SR, seed_phiN.f, 0.0, max_step=0.01).y[0, -1]; Nc = sl.odd(SL, SR, corr_phiN.f, 0.0, max_step=0.01).y[0, -1]
dphi = seed_phi + corr_phi.scaled(-A0/Ac); dphiN = seed_phiN + corr_phiN.scaled(-N0/Nc)
solE = sl.even(SL, SR, dphi.f, dphi.fT, (0, 0), max_step=0.01); solO = sl.odd(SL, SR, dphiN.f, 0.0, max_step=0.01)
c2s = 0.5*(solE.sol(0.0)[1] + solO.sol(0.0)[0]); c2p = 0.5*(solO.sol(0.0)[0] - solE.sol(0.0)[1])
fn = slice_fn_compact(sl, solE, solO, dphi, dphiN)
def cons_resid(Ua, J, h, idx):
    """C_VV, C_UU of the evolved solution by 4th-order differences; returns max |C| / max term, over the triangle nodes (j, i), i <= 0, interior by 3"""
    bgc = bg
    mx = 0.0; mt = 0.0
    for j in range(3, J - 2, max(1, J//40)):
        for i in range(-j + 3, -2, max(1, j//8 + 1)):
            V, U = j*h, i*h
            x, d, r, rV, rU, pV, pU, V0_, V1_, V2_, E, FV, FU, rhoV, rhoU = hs.jetsK(V, U, bgc.par, bgc.tab, 0.0)
            f = lambda q, dj, di: Ua[q, j + dj, i + di + J]
            d1V = lambda q: (-f(q, 2, 0) + 8*f(q, 1, 0) - 8*f(q, -1, 0) + f(q, -2, 0))/(12*h)
            d1U = lambda q: (-f(q, 0, 2) + 8*f(q, 0, 1) - 8*f(q, 0, -1) + f(q, 0, -2))/(12*h)
            d2V = lambda q: (-f(q, 2, 0) + 16*f(q, 1, 0) - 30*f(q, 0, 0) + 16*f(q, -1, 0) - f(q, -2, 0))/(12*h*h)
            d2U = lambda q: (-f(q, 0, 2) + 16*f(q, 0, 1) - 30*f(q, 0, 0) + 16*f(q, 0, -1) - f(q, 0, -2))/(12*h*h)
            for (d2, d1, Fx, px) in ((d2V, d1V, FV, pV), (d2U, d1U, FU, pU)):
                rx = rV if d1 is d1V else rU
                terms = [d2(0), Fx*d1(0), rx*d1(1), 0.5*EPS*px**2*f(0, 0, 0), EPS*r*px*d1(2)]
                C = sum(terms); mx = max(mx, abs(C)); mt = max(mt, max(abs(t) for t in terms))
    return mx, mt
for h in (0.02, 0.01, 0.005):
    J = int(round(3.0/h))
    L0, L1 = layers_from_slice(bg, h, J, fn); Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
    mx, mt = cons_resid(Ua, J, h, None)
    print(f"[constraints of the evolved solution] h={h}: max|C|={mx:.3e}, max term={mt:.3e}, ratio={mx/mt:.2e}", flush=True)
# mutated data: constraint violated (M_phi coefficient wrong in the slice ODE)
slm = Slice(bg, 'M_phi'); solOm = slm.odd(SL, SR, dphiN.f, 0.0, max_step=0.01)
fnm = slice_fn_compact(sl, solE, solOm, dphi, dphiN)
for h in (0.02, 0.01):
    J = int(round(3.0/h)); L0, L1 = layers_from_slice(bg, h, J, fnm); Ua = march_diag_full(L0, L1, J, h, bg.par, bg.tab)
    mx, mt = cons_resid(Ua, J, h, None); print(f"[mut M_phi] constraints h={h}: ratio {mx/mt:.2e}", flush=True)
# diamond |s| <= 0.6
t0 = time.time()
for h in (0.01, 0.005, 0.0025):
    J = int(round(0.6/h))
    L0, L1 = layers_diamond(bg, h, J, fn)
    Ua = march_diamond(L0, L1, J, h, bg.par, bg.tab)
    V = h*np.arange(0, J+1)
    Hh = np.array([Ua[0, j + J, 0 + J] for j in range(0, J+1)])       # U = 0, V = j h
    Hl = np.array([Ua[0, 0 + J, i + J] for i in range(0, J+1)])       # V = 0, U = i h
    c1a, c2a, ra = hs.horizon_fit(Hh, V); c1b, c2b, rb = hs.horizon_fit(Hl, V)
    print(f"[diamond h={h}] right future horizon c2_fit={c2a:.8e} (slice {c2s:.8e}, diff {c2a-c2s:.2e}); left future horizon c2'_fit={c2b:.8e} (slice {c2p:.8e}, diff {c2b-c2p:.2e}); resid {ra:.1e},{rb:.1e}; max Pi reached {-(J*h)**2:.3f}  {time.time()-t0:.1f}s", flush=True)
