"""W-bar conditioning: printed bracket (double) vs stable rewritten bracket (double) vs 60-digit mpmath of the printed bracket.
No eigenvalues. x = 10^k."""
import math, mpmath as mp
mp.mp.dps = 60
def br_printed(x, g, atan, ns):
    at = atan(x); q = 1 + x*x
    F = 1 + g/(1+g*g)*(1+g*x)*at
    Fx = g/(1+g*g)*((1+g*x)/q + g*at)
    r = Fx/F
    return -3/q + 3*(x-g)**2/q**2 + 2*r*r - 4*g/q*r + 4*g/(1+g*g)*(x-g)/(F*q*q)
def br_stable(x, g, atan, ns):
    at = atan(x); q = 1 + x*x
    F = 1 + g/(1+g*g)*(1+g*x)*at
    Fx = g/(1+g*g)*((1+g*x)/q + g*at)
    r = Fx/F
    return 3*(g*g-1-2*g*x)/q**2 + 2*r*r - 4*g/q*r + 4*g/(1+g*g)*(x-g)/(F*q*q)
print("g, x, rel err printed(double), rel err stable(double), br_mp")
for g in (2.5, 10.0):
    for k in (1,2,3,4,6,8,10,12):
        x = 10.0**k
        ref = br_printed(mp.mpf(x), mp.mpf(g), mp.atan, mp)
        ep = abs(br_printed(x, g, math.atan, math)/ref - 1)
        es = abs(br_stable(x, g, math.atan, math)/ref - 1)
        print(f"{g:5.1f} 1e{k:<3d} {float(ep):10.2e} {float(es):10.2e} {float(ref):12.4e}")
