import mpmath as mp, time
mp.mp.dps = 50
z3 = mp.zeta(3); ln2 = mp.log(2)
def make(O0, O1, O2, O3):
    Om = [O0, O1, O2, O3]
    def cc(m, l, R):
        if m == 1: return Om[0] + 1.5*l - 1 + 1/R
        if m == 2: return Om[0]*l + Om[1] + l**2/4 + l - l/R
        if m == 3: return Om[0]*l**2/2 + Om[1]*l + Om[2] + l**3/4 - l**2/2 + l**2/(2*R)
        if m == 4: return Om[0]*l**3/6 + Om[1]*l**2/2 + Om[2]*l + Om[3] + l**4/48 + l**3/6 - l**3/(6*R)
    def funcs(th):
        c = mp.cos(th); lc = mp.log(c); l = -2*lc; u = mp.tan(th); R = 1/c**2; s2 = mp.sin(th)**2
        Cl2 = mp.clsin(2, mp.pi-2*th); Cl3 = mp.clcos(3, mp.pi-2*th)
        K = 2*th*ln2 - Cl2
        T = th/2*Cl2 - Cl3/4 - mp.mpf(3)/16*z3 - ln2*th**2/2
        Y = [mp.mpf(1), -l, -2*Om[0]*l - mp.mpf(3)/2*l*l,
             -2*Om[1]*l + l**3/2 - 16*Om[0]*u*th + 8*Om[0]*l + 8*Om[0]*th**2 - 32*u*K + 8*l*l + 32*K*th + 64*T]
        L = [mp.mpf(-1), -2*Om[0]-2*l,
             -2*Om[1] + 2*Om[0]*l + 4*l*l - 8*Om[0]*u*th - 16*u*K]
        return c, lc, l, u, R, s2, Y, L
    return Om, cc, funcs
def G(k, O0, O1, O2=0, O3=0, nodes=60):
    Om, cc, funcs = make(O0, O1, O2, O3)
    def hk(m, l, R, s2, Y, L):   # h_m
        return s2*L[m-1] + sum(Y[j]*cc(m-j, l, R) for j in range(m)) + Y[m]/2
    def integrand(th):
        c, lc, l, u, R, s2, Y, L = funcs(th)
        t1 = 8*hk(k-1, l, R, s2, Y, L)*lc/s2
        t2 = 2*sum(L[k-1-j]*l**j/mp.factorial(j) for j in range(1, k))
        num = sum(Y[j]*cc(k-j, l, R) for j in range(k))
        thr = Om[k-2+0] if False else None
        return t1, t2, num/s2
    # throat values of sum_j Y_j c_{k-j} : only Y0*c_k(0,1)=Omega_{k-1}
    thr = Om[k-1]
    def f(th):
        t1, t2, t3 = integrand(th)
        s2 = mp.sin(th)**2
        c, lc, l, u, R, s2_, Y, L = funcs(th)
        num = sum(Y[j]*cc(k-j, l, R) for j in range(k)) - thr
        return t1 + t2 + 2*num/s2
    a = mp.quad(f, mp.linspace(0, 1, 3), method='gauss-legendre')
    b = mp.quad(f, [1, mp.pi/2])
    return a + b
O0 = -4*ln2
t=time.time()
g0 = G(3, O0, 0); g1 = G(3, O0, 1)
print("G3(0) =", g0, " slope =", g1-g0, " -4pi =", -4*mp.pi)
O1 = -g0/(g1-g0)
print("Omega1 =", O1)
print("closed =", 2*mp.pi**2/3 + 8*ln2**2, " diff =", O1 - (2*mp.pi**2/3 + 8*ln2**2), time.time()-t)

print("---- order 4")
t=time.time()
O1x = 2*mp.pi**2/3 + 8*ln2**2
h0 = G(4, O0, O1x, 0); h1 = G(4, O0, O1x, 1)
print("G4(0) =", h0, " slope =", h1-h0)
O2 = -h0/(h1-h0)
print("Omega2 =", O2, time.time()-t)
print("195's  =", mp.mpf('74.3693867279333175953847'))
print("closed =", 80*z3 - mp.mpf(8)/3*mp.pi**2*ln2 - mp.mpf(32)/3*ln2**3)
