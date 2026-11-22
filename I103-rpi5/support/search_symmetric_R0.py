import itertools, numpy as np
n = 7
rng = np.arange(-n, n + 1, dtype=np.int64)
a, b, c, d, e, f = [x.ravel() for x in np.meshgrid(rng, rng, rng, rng, rng, rng, indexing="ij")]
# R0 = [[a,b,c],[b,d,e],[c,e,f]], M = eta R0 = [[-a,-b,-c],[b,d,e],[c,e,f]]
M = [[-a, -b, -c], [b, d, e], [c, e, f]]
c2 = -(M[0][0] + M[1][1] + M[2][2])
c1 = (M[0][0]*M[1][1] - M[0][1]*M[1][0]) + (M[0][0]*M[2][2] - M[0][2]*M[2][0]) + (M[1][1]*M[2][2] - M[1][2]*M[2][1])
det = (M[0][0]*(M[1][1]*M[2][2] - M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2] - M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1] - M[1][1]*M[2][0]))
c0 = -det
D = 18*c2*c1*c0 - 4*c2**3*c0 + c2**2*c1**2 - 4*c1**3 - 27*c0**2
for sgn in (1, -1):
    hits = []
    for j in range(1, 7):
        idx = np.flatnonzero(D == sgn * j**6)
        cost = np.abs(np.stack([a, b, c, d, e, f])[:, idx]).sum(axis=0)
        order = np.argsort(cost)[:4]
        hits += [(j, tuple(int(x[idx[o]]) for x in (a, b, c, d, e, f)), int(cost[o])) for o in order]
    print(sgn, hits[:14])
