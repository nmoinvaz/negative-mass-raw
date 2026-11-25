import sys, time, itertools
sys.path.insert(0, "/home/nathan/Source/negative-mass-i157/notes/warp")
import sympy as sp
from sympy.polys.rings import ring
from sympy import QQ
import three_scalars as t3
t0 = time.time()
CC, SS, RW, WJ = t3.CC, t3.SS, t3.RW, t3.WJ
Rg, c, S, W0, W1, W2, W3, W4 = ring([CC, SS] + list(WJ[:5]), QQ)
Rs = t3.wall_frame(None)
R3 = Rs[:3, :3]
h = t3.orbit_metric(R3, WJ[0])
print("h", time.time()-t0, flush=True)
n = 3
D = t3.D_jets
dl = [lambda E: sp.Integer(0), lambda E: D(E, 1), lambda E: D(E, 2)]
def at1(e):
    e = sp.expand(sp.sympify(e).subs(RW, 1))
    return Rg.from_expr(e)
H = [[at1(h[i, j]) for j in range(n)] for i in range(n)]
DH = [[[at1(dl[a](h[b, k])) for k in range(n)] for b in range(n)] for a in range(n)]
DDH = [[[[at1(dl[e](dl[a](h[b, k]))) for k in range(n)] for b in range(n)] for a in range(n)] for e in range(n)]
print("derivs", time.time()-t0, flush=True)
one = Rg.one
def redS(p):
    out = Rg.zero
    pw = {0: one}
    for mon, co in p.terms():
        e = mon[1]
        k = e // 2
        if k not in pw:
            pw[k] = (one - c**2) ** k
        m2 = list(mon); m2[1] = e % 2
        out += pw[k] * Rg.from_dict({tuple(m2): co})
    return out
def det3(M):
    return (M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1]) - M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0]) + M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))
def adj3(M):
    A = [[None]*3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            r_ = [x for x in range(3) if x != j]; c_ = [x for x in range(3) if x != i]
            m = M[r_[0]][c_[0]]*M[r_[1]][c_[1]] - M[r_[0]][c_[1]]*M[r_[1]][c_[0]]
            A[i][j] = m if (i+j) % 2 == 0 else -m
    return A
def mm(A, B): return [[sum((A[i][k]*B[k][j] for k in range(3)), Rg.zero) for j in range(3)] for i in range(3)]
Dt = redS(det3(H)); print("det terms", len(Dt), flush=True)
adj = [[redS(x) for x in row] for row in adj3(H)]
Gl = [[[ (DH[b][d][k] + DH[k][d][b] - DH[d][b][k]) * QQ(1,2) for k in range(n)] for b in range(n)] for d in range(n)]
dGl = [[[[ (DDH[e][b][d][k] + DDH[e][k][d][b] - DDH[e][d][b][k]) * QQ(1,2) for k in range(n)] for b in range(n)] for d in range(n)] for e in range(n)]
# d_e hi = -adj dh_e adj / det^2
dhi_num = [[[x for x in row] for row in mm(adj, mm(DH[e], adj))] for e in range(n)]
dhi_num = [[[-x for x in row] for row in M] for M in dhi_num]
GN = [[[sum((adj[a][d]*Gl[d][b][k] for d in range(n)), Rg.zero) for k in range(n)] for b in range(n)] for a in range(n)]
Q = {}
for b in range(n):
    for k in range(b, n):
        tot = Rg.zero
        for a in range(n):
            t1 = -sum((dhi_num[a][a][d]*Gl[d][b][k] for d in range(n)), Rg.zero) * (-1)  # sign handled below
            # dhi_num already has the minus sign, so d_a Gam^a_bk = (sum_d dhi_num[a][a][d]*Gl[d][b][k] ... )/det^2
            t1 = sum((dhi_num[a][a][d]*Gl[d][b][k] for d in range(n)), Rg.zero)
            t2 = sum((adj[a][d]*dGl[a][d][b][k] for d in range(n)), Rg.zero)
            tot += t1 + Dt*t2
            t1 = sum((dhi_num[k][a][d]*Gl[d][a][b] for d in range(n)), Rg.zero)
            t2 = sum((adj[a][d]*dGl[k][d][a][b] for d in range(n)), Rg.zero)
            tot -= t1 + Dt*t2
            for d in range(n):
                tot += GN[a][a][d]*GN[d][b][k] - GN[a][k][d]*GN[d][a][b]
        Q[(b, k)] = redS(tot)
        print((b, k), len(Q[(b, k)]), time.time()-t0, flush=True)
import pickle
pickle.dump({k: str(v.as_expr()) for k, v in Q.items()}, open(sys.argv[1]+"/Q_all.pkl", "wb"))
# degree in c
for k, v in Q.items():
    print(k, "deg c", max((m[0] for m in v.monoms()), default=None), "deg S", max((m[1] for m in v.monoms()), default=None), "deg W4", max((m[6] for m in v.monoms()), default=None), "total deg W", max((sum(m[2:]) for m in v.monoms()), default=None))
