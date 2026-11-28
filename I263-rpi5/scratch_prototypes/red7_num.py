import sys, time, pickle
sys.path.insert(0, '/home/nathan/Source/negative-mass-i263/notes/wormhole_largeD')
sys.argv = sys.argv[:1]
import sympy as sp, mpmath as mp
from red7_lib import *
import order4 as o4
I, Fs = pickle.load(open('red7_state5.pkl', 'rb'))
Bs = pickle.load(open('red7_bnd.pkl', 'rb'))
v5 = sp.Symbol("v5")
mp.mp.dps = 45
q_ = mp.ln2
f = lambda a: mp.pi / 2 * mp.gamma(a + 1) / mp.gamma(a / 2 + 1) ** 2
tay = mp.taylor(f, 0, 7)
Jt = [mp.factorial(n) * tay[n] for n in range(8)]
print("Jt", [mp.nstr(j, 12) for j in Jt[:5]], mp.nstr(mp.pi**3/24, 12))
const = sum(sp.N(b.subs({Jt2: sp.Float(str(Jt[2]), 45), Jt3: sp.Float(str(Jt[3]), 45), q: sp.log(2)}), 45) for _, b in Bs)
const = mp.mpf(str(const))
print("sum of boundary terms (v5 free?)", mp.nstr(const, 30))
syms = (lt, th, C, D3, K2, v5, q)
If = sp.lambdify(syms, I, "mpmath")
def integrand(v5v):
    def fn(thv, x, tail):
        if tail:
            thv = mp.pi / 2 - x
        with mp.extradps(80):
            ltv = mp.log(2 * mp.cos(thv)) if not tail else mp.log(2 * mp.sin(x))
            a2 = 2 * x if tail else mp.pi - 2 * thv
            Cv = mp.clsin(2, a2)
            D3v = mp.clcos(3, a2) + 3 * mp.zeta(3) / 4
            K2v = o4.Lc2_poly(thv) + q_ * Cv - q_**2 * thv
            r = If(ltv, thv, Cv, D3v, K2v, v5v, q_)
        return +r
    return fn
def G(v5v):
    fn = integrand(v5v)
    return mp.quad(lambda t: fn(t, mp.pi/2 - t, False), [0, mp.mpf(1)/2, 1], method="gauss-legendre") + mp.quad(lambda x: fn(mp.pi/2 - x, x, True), [0, mp.pi/2 - 1])
t0 = time.time()
g0 = G(mp.mpf(0))
print("int I_final (v5 = 0) =", mp.nstr(g0, 30), time.time() - t0)
print("G7(0) =", mp.nstr(const + g0, 30), " method A: 513467.625456446519397870844712")
