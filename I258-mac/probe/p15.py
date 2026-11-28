import sys, time, numpy as np
from fs import *
SL, SR = -1.05, 1.05
bg = Bg(-1.0); sl = Slice(bg)
def solve_datum(sl, seed_phi, seed_phiN, corr_phi, corr_phiN, a=SL, b=SR, mass=True, odd=True):
    A0 = sl.even(a, b, seed_phi.f, seed_phi.fT, (0, 0), max_step=0.01).y[0, -1]; Ac = sl.even(a, b, corr_phi.f, corr_phi.fT, (0, 0), max_step=0.01).y[0, -1]
    N0 = sl.odd(a, b, seed_phiN.f, 0.0, max_step=0.01).y[0, -1]; Nc = sl.odd(a, b, corr_phiN.f, 0.0, max_step=0.01).y[0, -1]
    dphi = seed_phi + corr_phi.scaled(-A0/Ac if mass else 0.0); dphiN = seed_phiN + corr_phiN.scaled(-N0/Nc if odd else 0.0)
    solE = sl.even(a, b, dphi.f, dphi.fT, (0, 0), max_step=0.01); solO = sl.odd(a, b, dphiN.f, 0.0, max_step=0.01)
    return dphi, dphiN, solE, solO
def c2_fits(fn, hlist, bgx=bg, Vmax=3.0):
    out = {}
    for h in hlist:
        J = int(round(Vmax/h)); L0, L1 = layers_from_slice(bgx, h, J, fn); Ua = march_diag_full(L0, L1, J, h, bgx.par, bgx.tab)
        out[h] = hs.horizon_fit(Ua[0, :, J], h*np.arange(J+1))
    return out
def rich(vals, hl):
    return [(4*vals[hl[k+1]] - vals[hl[k]])/3 for k in range(len(hl)-1)]
# ---- (i) Schwarzschild scaling: dr = eps r, dF = -2 eps, dphi = 0; dm should be eps/2 at every s; slice constraints H, M residual zero
kcS = hs.KChart(-1.0, pi_max=1e12); parS = kcS.par.copy(); parS[hs.P_KIND2] = 1.0
class BgS:
    par = parS; tab = kcS.tab
    def at(self, s):
        a = max(abs(s), 1e-8)
        x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = hs.jetsK(a, -a, self.par, self.tab, 0.0)
        return dict(rho=x, r=r, rp=rV/a, php=pV/a, Fp=FV/a, E=E, V0=V0, V1=V1)
bgS = BgS(); slS = Slice(bgS)
eps_s = 1e-3
for s in (0.2, 1.0, 5.0):
    b = bgS.at(s)
    dr, dF = eps_s*b['r'], -2*eps_s
    h_ = 1e-4
    drT = eps_s*(bgS.at(s+h_)['r'] - bgS.at(s-h_)['r'])/(2*h_)   # d/ds along slice of eps r
    print(f"[Schwarzschild planted] s={s}: dm = {dm_of(bgS, s, dr, drT, dF):.12e}  (eps/2 = {eps_s/2:.12e})")
# H residual (even, with dF source) : dr'' + P dr' + Q dr + src = 0 with dr = eps r, dF = -2 eps (const), dphi = 0
for s in (0.2, 1.0, 3.0):
    hh = 1e-3
    f = lambda t: eps_s*bgS.at(t)['r']
    drT = (f(s+hh) - f(s-hh))/(2*hh); drTT = (f(s+hh) - 2*f(s) + f(s-hh))/hh**2
    P, Q, b = slS.PQ(s)
    res = drTT + P*drT + Q*f(s) + (b['E']*(1/b['r'] - b['V0']*b['r'])*(-2*eps_s))
    print(f"[Schwarzschild planted] H residual at s={s}: {res:.3e} (terms ~ {abs(drTT):.2e})")
# mutation of dm: drop the dr_T term
b = bgS.at(1.0); drT = eps_s*(bgS.at(1.0+1e-4)['r'] - bgS.at(1.0-1e-4)['r'])/2e-4
print("[mut dm_noT] dm =", eps_s*b['r']*(0.5 - (1/b['E'])*b['rp']**2) , "vs eps/2 =", eps_s/2)
# ---- (vii) one-sided control: data on [0.55, 1.0] only
seedR = Data([(1e-3, 0.78, 0.22), (-0.6e-3, 0.68, 0.12)]); seedRN = Data([(1e-3, 0.80, 0.2), (0.4e-3, 0.65, 0.1)])
corrR = Data([(1.0, 0.76, 0.24)]); corrRN = Data([(1.0, 0.72, 0.15), (-1.0, 0.86, 0.12)])
dphiR, dphiRN, sEr, sOr = solve_datum(sl, seedR, seedRN, corrR, corrRN)
print(f"[control one-sided] dr(0)={sEr.sol(0.0)[0]:.2e} dr'(0)={sEr.sol(0.0)[1]:.2e} n(0)={sOr.sol(0.0)[0]:.2e}  end values {sEr.y[:, -1]} {sOr.y[0, -1]:.2e}; max|dr| on slice {max(abs(sEr.sol(s)[0]) for s in np.linspace(0.5, 1.05, 100)):.2e}")
fnR = slice_fn_compact(sl, sEr, sOr, dphiR, dphiRN)
hl = (0.01, 0.005, 0.0025, 0.00125); F = c2_fits(fnR, hl)
print("[control one-sided] c2_fit:", {h: '%.3e' % F[h][1] for h in hl}, " ratios:", ['%.2f' % (F[hl[k]][1]/F[hl[k+1]][1]) for k in range(3)])
# ---- finer planted evolution ratios
def planted_evo(c, hs_list):
    bgc = Bg(c)
    xi  = lambda V: (0.3 + 0.7*V + 0.2*V*V + 0.1*V**3, 0.7 + 0.4*V + 0.3*V*V)
    eta = lambda U: (0.03 + 0.5*U - 0.3*U*U + 0.15*U**3, 0.5 - 0.6*U + 0.45*U*U)
    gf = lambda V, U: hs.gaugeK(bgc.par, bgc.tab, V, U, *xi(V), *eta(U))
    fnp = fd_slice_fn(bgc, gf); errs = []
    for h in hs_list:
        J = int(round(3.0/h)); L0, L1 = layers_from_slice(bgc, h, J, fnp); Ua = march_diag_full(L0, L1, J, h, bgc.par, bgc.tab)
        e = 0.0; scale = np.max(np.abs(L0[0]))
        pts = [(0.5, -0.2), (1.0, -0.5), (1.5, -0.3), (2.0, -1.2), (2.5, -0.1), (0.8, -0.4), (0.4, -0.1), (3.0, -0.0)]
        for (V, U) in pts:
            j, i = int(round(V/h)), int(round(U/h)); e = max(e, np.max(np.abs(Ua[:, j, i + J] - gf(j*h, i*h))))
        errs.append(e/scale)
    return errs
for c in (-1.0, -1.5):
    e = planted_evo(c, (0.01, 0.005, 0.0025, 0.00125)); print(f"[planted evo c={c}] fixed points err/scale", ['%.2e' % x for x in e], "ratios", ['%.2f' % (e[k]/e[k+1]) for k in range(3)], flush=True)
# ---- random data
rng = np.random.default_rng(258); rows = []
for k in range(20):
    sp = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    spN = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    dp, dpN, sE, sO = solve_datum(sl, sp, spN, corr_phi, corr_phiN)
    c2s = 0.5*(sE.sol(0.0)[1] + sO.sol(0.0)[0]); fnk = slice_fn_compact(sl, sE, sO, dp, dpN)
    F = c2_fits(fnk, (0.005, 0.0025)); ri = (4*F[0.0025][1] - F[0.005][1])/3
    rows.append((c2s, ri - c2s, max(np.max(np.abs([dp.f(s) for s in np.linspace(-1, 1, 400)])), 0)))
print("[random 20] |c2| min/median/max:", min(abs(r[0]) for r in rows), np.median([abs(r[0]) for r in rows]), max(abs(r[0]) for r in rows), " max |Rich - slice|:", max(abs(r[1]) for r in rows), " max amplitude dphi", max(r[2] for r in rows))
