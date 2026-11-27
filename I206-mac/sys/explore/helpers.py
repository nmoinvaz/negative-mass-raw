import sys, time, random
sys.path.insert(0, '.')
from proto import *
import mpmath as mp

LANES = [("f64", 53, 30, 1.1e-16), ("dd", 106, 60, 1.2e-32), ("qd", 212, 120, 6e-64)]

def inv_pairs(K, tau):
    """series of 1/(1 + (u/tau)^2): non-holonomic-friendly far pair at +-i tau"""
    out = [mpf(0)]*(K+1)
    for k in range(0, K+1, 2):
        out[k] = (-1)**(k//2) / mpf(tau)**k
    return out

def noisy(c, delta, seed):
    if delta == 0: return c
    rnd = random.Random(seed)
    return [v*(1 + mpf(delta)*mpf(rnd.uniform(-3**.5, 3**.5))) for v in c]

def real_case(alpha, sigma, tau=0, amp=1.9, delta=0):
    def build(K, eps):
        c = binom_series(alpha, mpf(sigma), K, amp)
        if tau:
            c = series_mul(c, inv_pairs(K, tau), K)
        return noisy(c, delta*eps if delta else 0, 7)
    def truth():
        return dict(sre=mpf(sigma), sim=mpf(0), alpha=mpf(alpha))
    return build, truth

def pair_case(alpha, mod, ang, tau=0, amp=1.9, delta=0):
    def build(K, eps):
        s = mp.mpc(mpf(mod)*mp.cos(mpf(ang)), mpf(mod)*mp.sin(mpf(ang)))
        c = [2*v for v in real_part(binom_series(alpha, s, K, amp))]
        if tau:
            c = series_mul(c, inv_pairs(K, tau), K)
        return noisy(c, delta*eps if delta else 0, 7)
    def truth():
        return dict(sre=mpf(mod)*mp.cos(mpf(ang)), sim=mpf(mod)*mp.sin(mpf(ang)), alpha=mpf(alpha))
    return build, truth

def two_case(a1, s1, a2, s2, A1=1.0, A2=1.0, delta=0):
    def build(K, eps):
        c1 = binom_series(a1, mpf(s1), K, A1); c2 = binom_series(a2, mpf(s2), K, A2)
        return noisy([x+y for x,y in zip(c1,c2)], delta*eps if delta else 0, 7)
    def truth():
        return dict(sre=mpf(s1), sim=mpf(0), alpha=mpf(a1))
    return build, truth

