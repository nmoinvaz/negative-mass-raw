import sys
from fractions import Fraction as Fr
sys.path.insert(0, "/Users/nathan/Source/negative-mass-i167/notes/warp")
import sympy as sp
import det_classify as dc
F0,F1,F2,eta = dc.F0_, dc.F1_, dc.F2_, dc.ETA
P = sp.Poly(sp.expand(dc.conical_N()), F0, F1, F2, eta)
terms = [(a,b,c,m,int(co)) for (a,b,c,m),co in zip(P.monoms(), P.coeffs())]
def mul(x, y, M):
    r = [Fr(0)]*(M+1)
    for i, xi in enumerate(x):
        if xi == 0: continue
        for j, yj in enumerate(y):
            if i + j > M: break
            r[i+j] += xi*yj
    return r
def power(x, n, M):
    r = [Fr(1)] + [Fr(0)]*M
    for _ in range(n): r = mul(r, x, M)
    return r
def Nseries(f, M):
    d1 = [ (i+1)*f[i+1] for i in range(len(f)-1)] + [Fr(0)]
    d2 = [ (i+1)*d1[i+1] for i in range(len(d1)-1)] + [Fr(0)]
    f = f[:M+1]; d1 = d1[:M+1]; d2 = d2[:M+1]
    cache = {}
    def pw(name, s, n):
        k = (name, n)
        if k not in cache: cache[k] = power(s, n, M)
        return cache[k]
    tot = [Fr(0)]*(M+1)
    for a,b,c,m,co in terms:
        t = mul(mul(pw("f", f, a), pw("d1", d1, b), M), pw("d2", d2, c), M)
        for i in range(M+1-m):
            tot[i+m] += co*t[i]
    return tot
def solve(K, f0=1):
    M = 2*K + 2
    coef = [Fr(0)]*(M+2)
    coef[0] = Fr(f0)
    sol = {}
    for k in range(1, K+1):
        # b_k multiplies x^(2k); appears at order 2k+2
        order = 2*k + 2
        vals = []
        for v in (Fr(0), Fr(1)):
            coef[2*k] = v if k > 1 else v
            tot = Nseries(coef, order)
            vals.append(tot[order])
        if k == 1:
            # quartic root: b1 = 2/5 (order 4 is 64 b1^3 (5 b1 - 2)); check and set
            coef[2] = Fr(2,5)
            tot = Nseries(coef, order); assert tot[4] == 0, tot[4]
            continue
        # linear in b_k
        slope = vals[1] - vals[0]
        coef[2*k] = -vals[0]/slope
        tot = Nseries(coef, order); assert tot[order] == 0
    return coef
if __name__ == "__main__":
    K = int(sys.argv[1])
    c = solve(K)
    print([str(c[2*k]) for k in range(1, 8)])
    import pickle; pickle.dump(c, open("even_series_K%d.pkl" % K, "wb"))
