"""Growth of the dominant homogeneous solution of method C's ODE along the arc used by P-C2 (explains its error), no new physics:
exp(Re int bt/a dx) along the upper/lower semicircle from x_t + r to x_t - r, bt = 1.3, r = 0.5 sqrt(1+g^2)."""
import cmath, math
import numpy as np
for g in (2.5, 5.0, 10.0):
    bt, r = 1.3, 0.5*math.sqrt(1+g*g)
    for side in (+1, -1):
        th = np.linspace(0, side*math.pi, 20001)
        x = g + r*np.exp(1j*th)
        inv_a = np.exp(-2*g*(np.arctan(x) - math.atan(g)))
        dx = 1j*r*np.exp(1j*th)
        integrand = bt*inv_a*dx
        cum = np.concatenate([[0], np.cumsum(0.5*(integrand[1:]+integrand[:-1])*np.diff(th))])
        print(f"g={g:4.1f} side={side:+d}  max growth exp(max Re int) = {math.exp(cum.real.max()):.3e}   (end: {math.exp(cum.real[-1]):.3e})")
