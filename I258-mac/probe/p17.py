import sys, time, numpy as np
from fs import *
exec(open('p15.py').read().split("# ---- (i) Schwarzschild")[0].split("def rich")[0])   # helpers: solve_datum, c2_fits
bg = Bg(-1.0); sl = Slice(bg)
corr_phi  = Data([(1.0, 0.0, 0.6)]); corr_phiN = Data([(1.0, 0.3, 0.3), (-1.0, -0.3, 0.3)])
# ---- Schwarzschild scaling + gauge: dm must stay eps/2; mutation drops the (dF, dr_T) group
kcS = hs.KChart(-1.0, pi_max=1e12); parS = kcS.par.copy(); parS[hs.P_KIND2] = 1.0
class BgS:
    par = parS; tab = kcS.tab
    def at(self, s):
        a = max(abs(s), 1e-8)
        x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = hs.jetsK(a, -a, self.par, self.tab, 0.0)
        return dict(rho=x, r=r, rp=rV/a, php=pV/a, Fp=FV/a, E=E, V0=V0, V1=V1)
bgS = BgS(); eps_s = 1e-3
xi  = lambda V: (0.3 + 0.7*V + 0.2*V*V, 0.7 + 0.4*V)
eta = lambda U: (0.03 + 0.5*U - 0.3*U*U, 0.5 - 0.6*U)
def gf(V, U):
    g = hs.gaugeK(parS, kcS.tab, V, U, *xi(V), *eta(U))
    x, d, r, rV, rU, pV, pU, V0, V1, V2, E, FV, FU, rhoV, rhoU = hs.jetsK(V, U, parS, kcS.tab, 0.0)
    return g + np.array([eps_s*r, -2*eps_s, 0.0])
fn = fd_slice_fn(bgS, gf)
for s in (0.2, 1.0, 5.0):
    U0, UT, UN, _ = fn(s)
    full = dm_of(bgS, s, U0[0], UT[0], U0[1])
    b = bgS.at(s)
    noT = U0[0]*(0.5 - (1/b['E'])*b['rp']**2*s*s)          # mutation: drop the (dF, dr_T) group
    print(f"[Schwarzschild scaling+gauge] s={s}: dm = {full:.10e} (eps/2 = {eps_s/2:.3e}); |dm - eps/2| = {abs(full-eps_s/2):.2e};  mutation dm_noT = {noT:.4e}")
# ---- tails of the mutated solutions at the support edge and in v = kappa s n
SL, SR, SMAX = -1.05, 1.05, 3.0e4
seed_phi  = Data([(1e-3, 0.30, 0.45), (-0.5e-3, -0.25, 0.45)]); seed_phiN = Data([(1e-3, 0.30, 0.45), (0.5e-3, -0.25, 0.45)])
kap = bg.kc.kappa
for lab, kw in (("full", {}), ("mass_off", dict(mass=False)), ("odd_off", dict(odd=False))):
    dp, dpN, sE, sO = solve_datum(sl, seed_phi, seed_phiN, corr_phi, corr_phiN, **kw)
    eE = sE.y[:, -1]; eO = sO.y[0, -1]
    tE = sl.even(SR, SMAX, lambda s: 0.0, lambda s: 0.0, tuple(eE)); tO = sl.odd(SR, SMAX, lambda s: 0.0, eO)
    rows = []
    for s in (1.05, 10.0, 100.0, 1e3, 1e4, 3e4):
        e = tE.sol(s); n = tO.sol(s)[0]
        rows.append((s, dm_of(bg, s, e[0], e[1]), kap*s*n, e[0]))
    print(f"[{lab}] tail (s, dm, v=kappa s n, dr):", ["(%g, %.2e, %.2e, %.2e)" % r for r in rows])
# ---- random data
rng = np.random.default_rng(258); rows = []
for k in range(20):
    sp = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    spN = Data([(rng.normal()*1e-3, rng.uniform(-0.5, 0.5), rng.uniform(0.2, 0.45)) for _ in range(3)])
    dp, dpN, sE, sO = solve_datum(sl, sp, spN, corr_phi, corr_phiN)
    c2s = 0.5*(sE.sol(0.0)[1] + sO.sol(0.0)[0]); fnk = slice_fn_compact(sl, sE, sO, dp, dpN)
    F = c2_fits(fnk, (0.005, 0.0025)); ri = (4*F[0.0025][1] - F[0.005][1])/3
    amp = max(max(abs(dp.f(s)) for s in np.linspace(-1, 1, 400)), max(abs(dpN.f(s)) for s in np.linspace(-1, 1, 400)))
    rows.append((c2s, ri - c2s, amp))
print("[random 20] |c2| min/median/max: %.2e %.2e %.2e; max |Rich - slice| %.2e; amplitude range %.2e..%.2e" % (min(abs(r[0]) for r in rows), np.median([abs(r[0]) for r in rows]), max(abs(r[0]) for r in rows), max(abs(r[1]) for r in rows), min(r[2] for r in rows), max(r[2] for r in rows)))
