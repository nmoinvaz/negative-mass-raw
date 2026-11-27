# Method B prototype: direct hierarchy on Chebyshev panels in v = sqrt(ln R), right-tail representation of L_k
import mpmath as mp, time, sys
dps = int(sys.argv[1]) if len(sys.argv) > 1 else 100
N = int(sys.argv[2]) if len(sys.argv) > 2 else 40
w = mp.mpf(sys.argv[3]) if len(sys.argv) > 3 else mp.mpf('0.5')
V = int(sys.argv[4]) if len(sys.argv) > 4 else 18
mp.mp.dps = dps
ln2 = mp.log(2)

def cheb_setup(N):
    xs = [mp.cos(mp.pi*(2*i+1)/(2*N)) for i in range(N)][::-1]   # ascending in (-1,1)
    # T_n(x_i)
    Vm = mp.matrix(N, N)
    for i in range(N):
        for n in range(N):
            Vm[i, n] = mp.chebyt(n, xs[i])
    Vinv = mp.inverse(Vm)
    def IT(n, x):   # int_{-1}^x T_n
        if n == 0: return x + 1
        if n == 1: return (x*x - 1)/2
        def part(y):
            return (mp.chebyt(n+1, y)/(n+1) - mp.chebyt(n-1, y)/(n-1))/2
        return part(x) - part(-1)
    Q = mp.matrix(N, N); qend = [mp.mpf(0)]*N
    for n in range(N):
        qend[n] = IT(n, mp.mpf(1))
        for i in range(N):
            Q[i, n] = IT(n, xs[i])
    S = Q*Vinv     # cumulative integral operator on [-1,1]
    wend = [sum(qend[n]*Vinv[n, j] for n in range(N)) for j in range(N)]
    return xs, [[S[i, j] for j in range(N)] for i in range(N)], wend

t0 = time.time()
xs, S, wend = cheb_setup(N)
P = int(mp.ceil(V/w))
half = w/2
nodes = []   # per panel list of v
for p in range(P):
    a = p*w
    nodes.append([a + half*(x+1) for x in xs])

def cum_left(F):    # F: list of panels of lists; returns int_0^{v_i}
    out = []; acc = mp.mpf(0)
    for p in range(P):
        f = F[p]
        out.append([acc + half*sum(S[i][j]*f[j] for j in range(N)) for i in range(N)])
        acc += half*sum(wend[j]*f[j] for j in range(N))
    return out, acc

def cum_right(F):   # int_{v_i}^V
    tot = []; 
    for p in range(P):
        f = F[p]; tot.append(half*sum(wend[j]*f[j] for j in range(N)))
    out = [None]*P; acc = mp.mpf(0)
    for p in range(P-1, -1, -1):
        f = F[p]
        out[p] = [acc + tot[p] - half*sum(S[i][j]*f[j] for j in range(N)) for i in range(N)]
        acc += tot[p]
    return out, acc

# node data
l = [[v*v for v in pv] for pv in nodes]
R = [[mp.exp(x) for x in pl] for pl in l]
Rm1 = [[mp.expm1(x) for x in pl] for pl in l]
u = [[mp.sqrt(x) for x in pr] for pr in Rm1]
def mapn(fn, *arrs): return [[fn(*[a[p][i] for a in arrs]) for i in range(N)] for p in range(P)]
fact = [mp.factorial(j) for j in range(8)]

def cc(m, Om, lv, Rv):
    if m == 1: return Om[0] + 1.5*lv - 1 + 1/Rv
    if m == 2: return Om[0]*lv + Om[1] + lv**2/4 + lv - lv/Rv
    if m == 3: return Om[0]*lv**2/2 + Om[1]*lv + Om[2] + lv**3/4 - lv**2/2 + lv**2/(2*Rv)
    if m == 4: return Om[0]*lv**3/6 + Om[1]*lv**2/2 + Om[2]*lv + Om[3] + lv**4/48 + lv**3/6 - lv**3/(6*Rv)

def hierarchy(Om, kmax):
    """returns Y, L lists (on nodes) for orders 0..kmax-1 and G_k for k = 1..kmax (G_k with h_k)"""
    Y = [mapn(lambda a: mp.mpf(1), l)]; L = []
    Gs = {}
    for k in range(0, kmax+1):
        if k >= 1:
            # Y_k = int_0^l F_{k-1} dl,  F_{k-1} = sum_{j=0}^{k-1} L_{k-1-j} l^j / j!
            Fint = [[2*nodes[p][i]*sum(L[k-1-j][p][i]*l[p][i]**j/fact[j] for j in range(k)) for i in range(N)] for p in range(P)]
            Yk, _ = cum_left(Fint); Y.append(Yk)
        # h_k
        def hk(p, i):
            lv, Rv = l[p][i], R[p][i]
            val = Y[k][p][i]/2 + sum(Y[j][p][i]*cc(k-j, Om, lv, Rv) for j in range(k))
            if k >= 1: val += (1 - 1/Rv)*L[k-1][p][i]
            return val
        thr = mp.mpf(1)/2 if k == 0 else Om[k-1]
        s = [[hk(p, i) - thr for i in range(N)] for p in range(P)]
        # C integrand: s (R-1)^{-3/2} R dl = (s/(R-1)) * R/sqrt(R-1) * 2v dv
        Cint = [[s[p][i]/Rm1[p][i]*R[p][i]/u[p][i]*2*nodes[p][i] for i in range(N)] for p in range(P)]
        Cr, G = cum_right(Cint)
        Gs[k] = G
        Lk = [[-2*thr - u[p][i]*Cr[p][i] for i in range(N)] for p in range(P)]
        L.append(Lk)
    return Y, L, Gs

if __name__ == "__main__":
    O0 = -4*ln2
    print("panels", P, "nodes", P*N, "setup", time.time()-t0, flush=True)
    # order 2: Omega0 from G_2 (k=2): G2 = G(Om0=0) + slope*Om0 ; G_k computed within hierarchy up to k
    def Gk(k, Om):
        Y, L, Gs = hierarchy(Om, k)
        return Gs[k], Gs
    zero = mp.mpf(0)
    g0, _ = Gk(2, [zero, zero, zero, zero]); g1, _ = Gk(2, [mp.mpf(1), zero, zero, zero])
    Om0 = -g0/(g1-g0); print("slope2", g1-g0, " Omega0 =", Om0, " -4ln2 =", O0, " diff", Om0-O0, flush=True)
    g0, Gs = Gk(3, [Om0, zero, zero, zero]); g1, _ = Gk(3, [Om0, mp.mpf(1), zero, zero])
    Om1 = -g0/(g1-g0); print("slope3", g1-g0, " Omega1 =", Om1, " diff from closed", Om1-(2*mp.pi**2/3+8*ln2**2), " G2 resid", Gs[2], flush=True)
    g0, Gs = Gk(4, [Om0, Om1, zero, zero]); g1, _ = Gk(4, [Om0, Om1, mp.mpf(1), zero])
    Om2 = -g0/(g1-g0); print("slope4", g1-g0, " Omega2 =", Om2, flush=True)
    print("195's closed diff", Om2-(80*mp.zeta(3)-mp.mpf(8)/3*mp.pi**2*ln2-mp.mpf(32)/3*ln2**3), " G3 resid", Gs[3], time.time()-t0)
