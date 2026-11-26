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

CASES = {
 "X1 a=.7 s=-1.7 far pair tau=4": real_case(0.7, -1.7, 4),
 "X2 a=-.4 s=1.1 far pair tau=3": real_case(-0.4, 1.1, 3),
 "X3 a=3e-7 s=1.5 far pair tau=6": real_case(3e-7, 1.5, 6),
 "X4 pole s=1.3 far pair tau=3": real_case(-1, 1.3, 3),
 "X5 double pole s=2.1 far pair tau=5": real_case(-2, 2.1, 5),
 "X6 pair a=.35 1.1e^.9i far tau=4": pair_case(0.35, 1.1, 0.9, 4),
 "X7 pair pole 1.6e^.5i far tau=5": pair_case(-1, 1.6, 0.5, 5),
 "X8 two real a=.5 s=1 / a=-.5 s=-1.4": two_case(0.5, 1.0, -0.5, -1.4),
 "X9 two real a=.5 s=1 / a=-.5 s=1.4": two_case(0.5, 1.0, -0.5, 1.4),
 "N1 a=.7 s=-1.7 far tau=4 noise 1e-6^.. ": real_case(0.7, -1.7, 4, delta=1),
 "N2 pair a=.35 1.1e^.9i far tau=4 noise": pair_case(0.35, 1.1, 0.9, 4, delta=1),
 "N3 pure a=.4 s=2 noise": real_case(0.4, 2.0, 0, delta=1),
}
NOISE_POWER = 0.6   # delta = eps^NOISE_POWER
if __name__ != "__main__": raise SystemExit
sel = sys.argv[1:]
for name,(build,truth) in CASES.items():
    if sel and not any(name.startswith(s) for s in sel): continue
    print(name, flush=True)
    for lane,bits,K,eps in LANES:
        t=time.time()
        set_prec(bits)
        d = eps**NOISE_POWER
        c = build(K, d)
        report(name.split()[0], c, truth(), lane)
