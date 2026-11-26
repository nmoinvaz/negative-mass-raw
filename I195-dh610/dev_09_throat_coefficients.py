import mpmath as mp
mp.mp.dps = 60
D = 5
s = 2*(D-3); eps = mp.mpf(1)/s; kappa = mp.mpf(3)/4; oms = mp.mpf(5)/2
N = 60
def ser(x0, rate):
    return [x0*rate**k/mp.factorial(k) for k in range(N+2)]
e = ser(1, -1); p = ser(1, 2*eps); e2 = ser(1, -2); e3 = ser(1, -3)
f = [(1-e[0])] + [-e[k] for k in range(1, N+2)]
half = mp.mpf(1)/2
g = half + 2*eps
a = [s*kappa*(e[k] + (kappa-1)*e2[k] - kappa*e3[k] + g*(e[k]-e2[k]) + half*e2[k]) for k in range(N+2)]
b = [-2*eps*e[k] for k in range(N+2)]; b[0] += half + 2*eps
y = [mp.mpf(0)]*(N+1); w = [mp.mpf(0)]*(N+1)
y[0] = mp.mpf(1); w[0] = -a[0]/b[0]
for m in range(1, N+1):
    y[m] = eps*w[m-1]/m
    S = a[0]*y[m] + sum(a[j]*y[m-j] + b[j]*w[m-j] for j in range(1, m+1)) - sum(f[j+1]*(m-j)*w[m-j] for j in range(1, m))
    w[m] = S/(m - b[0])
# exact
Y = lambda t: mp.exp(-kappa*(1-mp.exp(-t)))
ex = mp.taylor(Y, 0, N)
for m in [0,1,2,3,5,10,20,30,40,50,60]:
    print(m, mp.nstr(y[m],10), mp.nstr(ex[m],10), mp.nstr(abs(y[m]-ex[m]),3))
