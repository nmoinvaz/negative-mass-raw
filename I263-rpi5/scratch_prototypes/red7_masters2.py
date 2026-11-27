import sys, time
import mpmath as mp
mp.mp.dps = 70
q_ = mp.ln2
z3, z5, z6 = mp.zeta(3), mp.zeta(5), mp.zeta(6)
pi = mp.pi

def both(f):
    return (mp.quad(lambda t: f(t, pi / 2 - t, False), [0, mp.mpf(1) / 2, 1], method="gauss-legendre")
            + mp.quad(lambda x: f(pi / 2 - x, x, True), [0, pi / 2 - 1]))

def integ(kind):
    def fn(th, x, tail):
        with mp.extradps(60):
            lt = mp.log(2 * mp.sin(x)) if tail else mp.log(2 * mp.cos(th))
            a2 = 2 * x if tail else pi - 2 * th
            r = kind(lt, th if not tail else pi / 2 - x, mp.clsin(2, a2), mp.clcos(3, a2) + 3 * z3 / 4)
        return +r
    return both(fn)

t0 = time.time()
M = {}
M["A=<lt^2 C^2>"] = integ(lambda lt, th, C, D3: lt**2 * C**2)
print("A", time.time() - t0, flush=True)
M["Bm=<lt^3 D3>"] = integ(lambda lt, th, C, D3: lt**3 * D3)
print("B", time.time() - t0, flush=True)
M["Dm=<th^2 lt^2>"] = integ(lambda lt, th, C, D3: th**2 * lt**2)
M["lt2D3"] = integ(lambda lt, th, C, D3: lt**2 * D3)
M["lt D3"] = integ(lambda lt, th, C, D3: lt * D3)
M["D3"] = integ(lambda lt, th, C, D3: D3)
for k, v in M.items():
    print(k, mp.nstr(v, 60))
print("Dm closed 11 pi^5/1440 =", mp.nstr(11 * pi**5 / 1440, 60))
print("lt2D3 closed =", mp.nstr(pi / 4 * (5 * z5 - 2 * pi**2 / 6 * z3) + pi**3 * z3 / 32, 60))
print("D3 closed 3 pi z3/8 =", mp.nstr(3 * pi * z3 / 8, 60))
for name in ("A=<lt^2 C^2>", "Bm=<lt^3 D3>"):
    r = mp.pslq([M[name] / pi, pi**6, z3**2], maxcoeff=10**9, maxsteps=10**6, tol=mp.mpf(10)**-55)
    print(name, "/pi in {pi^6, z3^2}:", r)
