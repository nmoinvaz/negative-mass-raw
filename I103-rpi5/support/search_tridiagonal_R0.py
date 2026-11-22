# Integer symmetric R0 (3x3), M = eta R0, eta = diag(-1,1,1). D homogeneous of degree 6: D(eps R0) = eps^6 D(R0).
# Want D(R0) = +-j^6 so eps = 1e-10/j gives D = +-1e-60. Tridiagonal R0 = [[a,b,0],[b,c,d],[0,d,e]] first.
import itertools, numpy as np
rng = range(-5, 6)
sixth = {j**6: j for j in range(1, 8)}
found = {1: [], -1: []}
for a, b, c, d, e in itertools.product(rng, rng, rng, rng, rng):
    if b == 0 or d == 0: continue
    # M = [[-a,-b,0],[b,c,d],[0,d,e]]
    c2 = -(-a + c + e)
    c1 = (-a*c + b*b) + (-a*e) + (c*e - d*d)
    det = -a*(c*e - d*d) - (-b)*(b*e - 0)
    c0 = -det
    D = 18*c2*c1*c0 - 4*c2**3*c0 + c2**2*c1**2 - 4*c1**3 - 27*c0**2
    if D > 0 and D in sixth: found[1].append((D, sixth[D], (a,b,c,d,e)))
    if D < 0 and -D in sixth: found[-1].append((D, sixth[-D], (a,b,c,d,e)))
for s in (1, -1):
    fs = sorted(found[s], key=lambda t: (t[1], sum(abs(x) for x in t[2])))
    print(s, len(fs), fs[:8])
