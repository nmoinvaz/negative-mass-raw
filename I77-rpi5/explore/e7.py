import sys, time, random
exec(open("e6.py").read().split("t0 = time.time()")[0])
t0 = time.time()
n = 3
Dl = [lambda E: sp.Integer(0), Dr, Dth]
dh = [[[Dl[a](h[b, cc]) for cc in range(n)] for b in range(n)] for a in range(n)]
ddh = [[[[Dl[a](dh[e][b][cc]) for cc in range(n)] for b in range(n)] for e in range(n)] for a in range(n)]
print("derivs", time.time()-t0, flush=True)
def ricci_num(pt_c):
    """Ricci of h at theta0 (c,S numeric), symbolic in r, W: returns list of (b,c, numerator polynomial, power of det)."""
    sub = {c: pt_c[0], S: pt_c[1]}
    H = h.subs(sub).applyfunc(sp.expand)
    DH = [[[sp.expand(dh[a][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for a in range(n)]
    DDH = [[[[sp.expand(ddh[a][e][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for e in range(n)] for a in range(n)]
    det = sp.expand(H.det())
    adj = H.adjugate().applyfunc(sp.expand)  # h^{-1} = adj/det
    # Gamma_{d,bc} (lowered first index) = (dh[b][d][c] + dh[c][d][b] - dh[d][b][c])/2
    Gl = [[[(DH[b][d][cc] + DH[cc][d][b] - DH[d][b][cc])/2 for cc in range(n)] for b in range(n)] for d in range(n)]
    # d_e Gamma_{d,bc}
    dGl = [[[[ (DDH[e][b][d][cc] + DDH[e][cc][d][b] - DDH[e][d][b][cc])/2 for cc in range(n)] for b in range(n)] for d in range(n)] for e in range(n)]
    # Ric_bc = d_a Gam^a_bc - d_c Gam^a_ab + Gam^a_ad Gam^d_bc - Gam^a_cd Gam^d_ab ; Gam^a_bc = hi[a][d] Gl[d][b][c]
    # work with numerators: hi = adj/det.
    out = {}
    for b in range(n):
        for cc in range(b, n):
            # terms with det^2 denominators
            # Gam^a_bc = sum_d adj[a][d] Gl[d][b][cc] / det  -> GN[a][b][cc] / det
            pass
    GN = [[[sp.expand(sum(adj[a, d]*Gl[d][b][cc] for d in range(n))) for cc in range(n)] for b in range(n)] for a in range(n)]
    ddet = [sp.expand(sum(adj[i, j]*DH[a][j][i] for i in range(n) for j in range(n))) for a in range(n)]  # d_a det = tr(adj dh)... careful
    return H, DH, DDH, det, adj, GN, Gl, dGl
H, DH, DDH, det, adj, GN, Gl, dGl = ricci_num((sp.Rational(3,5), sp.Rational(4,5)))
print("setup", time.time()-t0, "det terms", len(sp.Poly(det*r**9, r, *Wd[:3]).terms()), flush=True)

def ricci_at(pt_c):
    sub = {c: pt_c[0], S: pt_c[1]}
    H = h.subs(sub).applyfunc(sp.expand)
    DH = [H.applyfunc(lambda e: 0)] + [None, None]
    DH = [[[sp.expand(dh[a][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for a in range(n)]
    DDH = [[[[sp.expand(ddh[a][e][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for e in range(n)] for a in range(n)]
    det = sp.expand(H.det())
    adj = H.adjugate().applyfunc(sp.expand)
    hi = adj/det
    Gl = [[[(DH[b][d][cc] + DH[cc][d][b] - DH[d][b][cc])/2 for cc in range(n)] for b in range(n)] for d in range(n)]
    dGl = [[[[ (DDH[e][b][d][cc] + DDH[e][cc][d][b] - DDH[e][d][b][cc])/2 for cc in range(n)] for b in range(n)] for d in range(n)] for e in range(n)]
    dhi = [-(hi*sp.Matrix(n, n, lambda i, j: DH[e][i][j])*hi) for e in range(n)]
    Gam = [[[sum(hi[a, d]*Gl[d][b][cc] for d in range(n)) for cc in range(n)] for b in range(n)] for a in range(n)]
    dGam = [[[[sum(dhi[e][a, d]*Gl[d][b][cc] + hi[a, d]*dGl[e][d][b][cc] for d in range(n)) for cc in range(n)] for b in range(n)] for a in range(n)] for e in range(n)]
    Ric = {}
    for b in range(n):
        for cc in range(b, n):
            s = sum(dGam[a][a][b][cc] - dGam[cc][a][a][b] for a in range(n))
            s += sum(Gam[a][a][d]*Gam[d][b][cc] - Gam[a][cc][d]*Gam[d][a][b] for a in range(n) for d in range(n))
            Ric[(b, cc)] = s
    return Ric
t1 = time.time()
Ric = ricci_at((sp.Rational(3,5), sp.Rational(4,5)))
print("ricci built", time.time()-t1, flush=True)
res = {}
for k, e in Ric.items():
    t2 = time.time()
    num, den = sp.fraction(sp.cancel(sp.together(e)))
    P = sp.Poly(sp.expand(num), r, *Wd[:5])
    res[k] = (num, den)
    print(k, "terms", len(P.terms()), "deg", P.total_degree(), "time", time.time()-t2, "den", sp.factor(den), flush=True)
import pickle
pickle.dump({k: (str(v[0]), str(v[1])) for k, v in res.items()}, open("ricnum_35.pkl", "wb"))
