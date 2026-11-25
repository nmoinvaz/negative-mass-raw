import sys, time, pickle
exec(open("e7.py").read().split("def ricci_at(pt_c):")[0])
def Qnum(pt_c):
    """det^2 * Ric_bc as polynomials (no division), at theta0 with (c,S) = pt_c, symbolic in r, W."""
    sub = {c: pt_c[0], S: pt_c[1]}
    H = h.subs(sub).applyfunc(sp.expand)
    DH = [[[sp.expand(dh[a][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for a in range(n)]
    DDH = [[[[sp.expand(ddh[a][e][b][cc].subs(sub)) for cc in range(n)] for b in range(n)] for e in range(n)] for a in range(n)]
    det = sp.expand(H.det()); adj = H.adjugate().applyfunc(sp.expand)
    Gl = [[[(DH[b][d][cc] + DH[cc][d][b] - DH[d][b][cc])/2 for cc in range(n)] for b in range(n)] for d in range(n)]
    dGl = [[[[(DDH[e][b][d][cc] + DDH[e][cc][d][b] - DDH[e][d][b][cc])/2 for cc in range(n)] for b in range(n)] for d in range(n)] for e in range(n)]
    dhi_num = [-(adj*sp.Matrix(n, n, lambda i, j: DH[e][i][j])*adj) for e in range(n)]   # d_e(hi) = dhi_num/det^2 + ... careful: hi = adj/det
    # hi = adj/det.  d_e hi = -hi dh hi = -adj dh adj / det^2.
    # Gam^a_bc = sum_d adj[a,d] Gl[d][b][cc] / det =: GN/det
    GN = [[[sum(adj[a, d]*Gl[d][b][cc] for d in range(n)) for cc in range(n)] for b in range(n)] for a in range(n)]
    # d_e Gam^a_bc = [ -sum_d (adj dh adj)[a,d] Gl[d][b][cc]/det^2 ] + [ sum_d adj[a,d] dGl[e][d][b][cc] ]/det
    #   = (T1 + det*T2)/det^2
    Q = {}
    for b in range(n):
        for cc in range(b, n):
            tot = 0
            for a in range(n):
                t1 = -sum(dhi_num[a][a, d]*Gl[d][b][cc] for d in range(n))   # e = a
                t2 = sum(adj[a, d]*dGl[a][d][b][cc] for d in range(n))
                tot += t1 + det*t2
                t1 = -sum(dhi_num[cc][a, d]*Gl[d][a][b] for d in range(n))   # -d_c Gam^a_ab
                t2 = sum(adj[a, d]*dGl[cc][d][a][b] for d in range(n))
                tot -= t1 + det*t2
                for d in range(n):
                    tot += GN[a][a][d]*GN[d][b][cc] - GN[a][cc][d]*GN[d][a][b]
            Q[(b, cc)] = sp.expand(tot)
    return Q, det
if __name__ == "__main__":
    c0, S0 = sp.Rational(sys.argv[1]), sp.Rational(sys.argv[2])
    t0 = time.time()
    Q, det = Qnum((c0, S0))
    out = {}
    for k, v in Q.items():
        v1 = sp.expand(v.subs(r, 1))
        P = sp.Poly(v1, *Wd[:5]) if v1 != 0 else None
        print(k, "terms", len(P.terms()) if P else 0, "degs", P.degree_list() if P else None, "time", time.time()-t0, flush=True)
        out[k] = str(v1)
    out["det"] = str(sp.expand(det.subs(r, 1)))
    pickle.dump(out, open(f"Q_{sys.argv[1].replace('/','_')}_{sys.argv[2].replace('/','_')}.pkl", "wb"))
