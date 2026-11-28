import sys; sys.path.insert(0, ".")
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from fam import Fam, ray, arccot

def eh_backward(f, v0, tau0=1e-7):
    """unique ray into P* = (v*, -1/K): start at tau0 = v* - v on y = 1 + K rho = -(K A0/3) tau, integrate backward to v0 (tau grows)."""
    K = f.K; vs = f.vstar(); r0 = -1/K; A0 = f.A(r0)
    y0 = -(K*A0/3)*tau0
    def rhs(tau, y):           # d rho/d tau = -F/2 ; y=rho
        return [-f.F(vs - tau, y[0])/2]
    sol = solve_ivp(rhs, (tau0, vs - v0), [r0 + y0/K], rtol=1e-12, atol=1e-14, method="DOP853", dense_output=True)
    return sol, vs
def fwd_class(f, v0, r0):
    sol = ray(f, v0, r0)
    return +1 if sol.y[0, -1] > 0 else -1, sol
for c in (-1.0, -1.5):
    f = Fam(c, -1.0)
    v0 = -10.0
    sol, vs = eh_backward(f, v0)
    rho_eh_v0 = sol.y[0, -1]
    print(f"== c = {c}: K = {f.K:.6f}, v* = {vs}, P* rho = {-1/f.K:.6f}, rho_h = {f.rhoh():.6f}")
    print(f"  backward EH at v0 = {v0}: rho_EH = {rho_eh_v0:.12f}   (static rho_h = {f.rhoh():.6f}, s0 = {f.sv(v0):.3e})")
    # forward bisection
    lo, hi = rho_eh_v0 - 0.3, rho_eh_v0 + 0.3
    assert fwd_class(f, v0, lo)[0] == -1 and fwd_class(f, v0, hi)[0] == +1
    for _ in range(60):
        mid = 0.5*(lo + hi)
        if fwd_class(f, v0, mid)[0] > 0: hi = mid
        else: lo = mid
    print(f"  forward bisection separatrix: {0.5*(lo+hi):.12f}   diff to backward: {0.5*(lo+hi) - rho_eh_v0:.3e}")
    # EH vs AH: sample v
    print("   v      s        rho_EH      rho_AH+    rho_AH-   F_EH     r_EH")
    for v in (-10, -6, -3, -1.5, -0.7, -0.3, -0.1, -0.03):
        tau = vs - v
        rE = sol.sol(tau)[0] if tau <= vs - v0 else np.nan
        s = f.sv(v)
        # AH+ : root of s_AH(rho) = s for rho>0 ; AH- for rho<0
        def g(r): return f.sAH(r) - s
        rp = rm = np.nan
        try:
            xs = np.linspace(1e-6, 5, 5000); gs = g(xs); idx = np.where(gs[:-1]*gs[1:] < 0)[0]
            rp = brentq(g, xs[idx[0]], xs[idx[0]+1]) if len(idx) else np.nan
        except Exception: pass
        try:
            xs = np.linspace(-60, -1e-6, 20000); gs = g(xs); idx = np.where(gs[:-1]*gs[1:] < 0)[0]
            rm = brentq(g, xs[idx[0]], xs[idx[0]+1]) if len(idx) else np.nan
        except Exception: pass
        lam = np.sqrt(1 + s)
        print(f"  {v:6.2f} {s:9.5f} {rE:11.6f} {rp:10.6f} {rm:10.6f} {f.F(v, rE):9.4f} {lam*np.sqrt(1+rE**2):9.5f}")
    # r_* proportional to distance
    print("  vertex check: r_* / (rho0 - rho_sep)")
    for d in (1e-3, 1e-4, 1e-5, 1e-6):
        sl = ray(f, v0, rho_eh_v0 + d)
        rho_end, v_end = np.tan(sl.y[0, -1]), sl.t[-1]
        lam = np.sqrt(max(1 + f.sv(v_end), 0))
        print(f"   d = {d:.0e}: v_end - v* = {v_end - vs:.2e}, rho_end = {rho_end:.4g}, r = {lam*np.sqrt(1+rho_end**2):.6g}, ratio = {lam*np.sqrt(1+rho_end**2)/d:.5g}")
