# synthetic probe only: how many digits of Omega_2 can a polynomial-in-eps fit give from 64 points, D = 50..1e4,
# with data good to a relative 1e-60 and asymptotic-series coefficients Omega_k = A (k+1)! c^k
import mpmath as mp, sys
mp.mp.dps = 300
Ds = []
for j in range(64):
    D = round(50*200**(j/63))
    if D not in Ds: Ds.append(D)
c = mp.mpf(73)/mp.mpf('10.4233603787385')/3
A = mp.mpf('10.4233603787385')/(2*c)
def Om(k): return A*mp.factorial(k+1)*c**k
def g(D, kmax=60):
    e = mp.mpf(1)/(2*(D-3))
    # truncate at the smallest term (asymptotic series)
    s = 0; prev = None
    for k in range(1, kmax):
        t = Om(k)*e**k
        if prev is not None and abs(t) > abs(prev): break
        s += t; prev = t
    return s
noise = mp.mpf(10)**-int(sys.argv[1]) if len(sys.argv) > 1 else mp.mpf(10)**-60
import random; random.seed(1)
data = {D: g(D)*(1+noise*(random.random()*2-1)) for D in Ds}
def fit(Dlo, K):
    pts = [D for D in Ds if D >= Dlo]
    if len(pts) < K+3: return None
    e = [mp.mpf(1)/(2*(D-3)) for D in pts]
    M = mp.matrix(len(pts), K); b = mp.matrix(len(pts), 1)
    for i, (D, ei) in enumerate(zip(pts, e)):
        for k in range(K): M[i, k] = ei**k          # data/eps = sum Omega_{k+1} eps^k
        b[i] = data[D]/ei
    x = mp.qr_solve(M, b)[0]
    res = max(abs((M[i, :]*x)[0] - b[i]) for i in range(len(pts)))
    return x, res
print("noise", noise)
for Dlo in (50, 100, 200, 500, 1000):
    for K in (6, 8, 10, 12, 14, 16, 20, 24):
        r = fit(Dlo, K)
        if r is None: continue
        x, res = r
        print(f"Dlo {Dlo:5d} K {K:2d}  err Om1 {mp.nstr(abs(x[0]-Om(1)),3):>10}  err Om2 {mp.nstr(abs(x[1]-Om(2)),3):>10}  rel res {mp.nstr(res,3)}")
