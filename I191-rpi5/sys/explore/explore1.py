import sys, time
sys.path.insert(0, '.')
from proto import *
import mpmath as mp

LANES = [("f64", 53, 30), ("dd", 106, 60), ("qd", 212, 120)]

def build(case, bits, K):
    set_prec(bits)
    return case(K)

def case_real(alpha, sigma, beta=0, amp=1.9):
    def f(K):
        c = binom_series(alpha, mpf(sigma), K, amp)
        if beta:
            c = series_mul(c, exp_series(mpf(beta), K), K)
        return c
    truth = dict(sre=mpf(sigma), sim=mpf(0), alpha=mpf(alpha))
    return f, truth

def case_pair(alpha, mod, ang, beta=0, amp=1.9):
    sig = mp.mpc(mod*mp.cos(ang), mod*mp.sin(ang))
    def f(K):
        s = mp.mpc(mpf(mod)*mp.cos(mpf(ang)), mpf(mod)*mp.sin(mpf(ang)))
        c = real_part(binom_series(alpha, s, K, amp))
        c = [2*v for v in c]
        if beta:
            c = series_mul(c, exp_series(mpf(beta), K), K)
        return c
    truth = dict(sre=mpf(mod)*mp.cos(mpf(ang)), sim=mpf(mod)*mp.sin(mpf(ang)), alpha=mpf(alpha))
    return f, truth

def case_two(a1, s1, a2, s2, A1=1.0, A2=1.0):
    def f(K):
        c1 = binom_series(a1, mpf(s1), K, A1)
        c2 = binom_series(a2, mpf(s2), K, A2)
        return [x+y for x,y in zip(c1,c2)]
    truth = dict(sre=mpf(s1), sim=mpf(0), alpha=mpf(a1))
    return f, truth

CASES = {
 "E1 pole s=1.3 dressed": case_real(-1, 1.3, 0.4),
 "E2 a=.7 s=-1.7 dressed": case_real(0.7, -1.7, 0.25),
 "E3 a=-1.3 s=2.2 pure": case_real(-1.3, 2.2),
 "E4 a=.4 s=1.1 dressed": case_real(0.4, 1.1, 0.3),
 "E5 pair a=.35 1.1e^.9i pure": case_pair(0.35, 1.1, 0.9),
 "E6 pair pole 1.6e^.5i pure": case_pair(-1, 1.6, 0.5),
 "E7 pair a=-.6 1.3e^1.2i dressed": case_pair(-0.6, 1.3, 1.2, 0.2),
 "E8 two real a=.5 s=1 / a=-.5 s=-1.4": case_two(0.5, 1.0, -0.5, -1.4),
 "E9 two real same exp a=.3 s=1 / s=1.3": case_two(0.3, 1.0, 0.3, 1.3),
 "E10 a=3e-7 s=1.5 near-dressed": case_real(3e-7, 1.5, 1e-3),
}
sel = sys.argv[1:] 
for name,(f,truth) in CASES.items():
    if sel and not any(name.startswith(s) for s in sel): continue
    print(name, flush=True)
    for lane,bits,K in LANES:
        t=time.time()
        set_prec(bits)
        c = f(K)
        tr = {k: +v for k,v in truth.items()}
        report(name.split()[0], c, tr, lane)
        print(f"    ({time.time()-t:.1f}s)", flush=True)
