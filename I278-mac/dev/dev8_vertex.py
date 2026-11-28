import sys
sys.argv = ["x"]
sys.path.insert(0, ".")
import numpy as np
import family_causal as fc
from scipy.integrate import solve_ivp
for cq, cf in fc.MEMBERS:
    f = fc.Fam(cf, -1.0)
    sol = fc.eh_backward(f, -7.0)
    ref = float(sol.sol(f.vs + 7.0)[0])
    print(f"== c = {cf}: rho_EH(-7) = {ref:.10f}")
    for rho in (0.0, 0.3, -0.5):
        out = []
        for tau in (1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6):
            v = f.vs - tau
            def rhs(vv, y): return [f.F(vv, np.tan(y[0]))*np.cos(y[0])**2/2]
            s2 = solve_ivp(rhs, (v, -7.0), [np.arctan(rho)], rtol=1e-12, atol=1e-15, method="DOP853")
            r0 = float(np.tan(s2.y[0, -1]))
            x = r0 - ref
            out.append(f"tau {tau:.0e}: x/sqrt(tau) = {x/np.sqrt(tau):.5g}")
        print(f"  rho = {rho}: " + "; ".join(out))
