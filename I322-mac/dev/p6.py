import sys, math
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i322/notes/black_universe")
import numpy as np
from scipy.integrate import solve_ivp
import remainder as rm
sc = rm.hb.sc
K = 2/math.pi
def PQ(rho, W):
    A, Ap = sc.A_(rho), sc.Ap_(rho)
    R2 = 1 + rho*rho
    P = 2/rho - Ap/A
    Q = 1/R2**2 - Ap/(A*rho*R2) - 2/(A*R2) + W*W/A**2
    return P, Q
def rhs(rho, y, W):
    P, Q = PQ(rho, W)
    return [y[1], P*y[1] + Q*y[0]]
# check Y_ref = R e^{kappa x}: residual of R e^{kx} with x' = 1/A: use Y = R*E, E' = K E/A
def rhs3(rho, y):
    # y = (E)
    return [K*y[0]/sc.A_(rho)]
# check W=kappa solution Y_ref numerically through ODE residual at a point
def resid_ref(rho):
    R = math.sqrt(1+rho*rho); A = sc.A_(rho)
    # E = e^{kappa x}; E'/E = K/A ; E''/E = (K/A)' + (K/A)^2
    Ap = sc.Ap_(rho)
    e1 = K/A; e2 = -K*Ap/A**2 + (K/A)**2
    Rp = rho/R; Rpp = 1/R**3
    Y = R; Yp = Rp + R*e1; Ypp = Rpp + 2*Rp*e1 + R*e2
    P, Q = PQ(rho, K)
    return Ypp - P*Yp - Q*Y
print("Yref residual at 0.5, 1.3, -0.4:", resid_ref(0.5), resid_ref(1.3), resid_ref(-0.4))
# static W=0 regular solution
rhos = [-0.311367, 0.681884, 1.0, 1.369767, 2.353875]
r0 = 1e-4
sol = solve_ivp(rhs, [r0, 5.0], [r0, 1.0], args=(0.0,), method="DOP853", rtol=1e-12, atol=1e-16, dense_output=True)
soln = solve_ivp(rhs, [-r0, -0.9], [-r0, 1.0], args=(0.0,), method="DOP853", rtol=1e-12, atol=1e-16, dense_output=True)
f0 = {}
for r in rhos:
    f0[r] = sol.sol(r)[0] if r > 0 else soln.sol(r)[0]
print("f0:", f0)
ref = f0[0.681884]
print("f0 ratios to rho=0.68:", {r: f0[r]/ref for r in rhos})
# measured (G, h=0.0025, V=40 or 30): Y_rem2 = R*w2
meas = {-0.311367: -2.267e-4*1.0474, 0.681884: 4.452e-4*1.2104, 1.0: 5.759e-4*1.4142, 1.369767: 6.917e-4*1.6960}
mref = meas[0.681884]
print("measured ratios:", {r: meas[r]/mref for r in meas})
