import sys
sys.path.insert(0,'.')
from explore3 import *
def run(name, builder, tr_fn):
    print(name)
    for lane,bits,K,eps in LANES:
        set_prec(bits)
        c = builder(K); tr = tr_fn()
        ta = cells_A(c, DA, PHIS); tb = cells_B(c, DB, PHIS)
        out=[]
        for fam,tab in (("A",ta),("B",tb)):
            ch = choose(tab, 8)
            if ch is None: out.append(f"{fam}: none"); continue
            key,sp = ch; e=tab[key]
            es = float(dist(e,tr)/abs(mp.mpc(tr["sre"],tr["sim"])))
            out.append(f"{fam}{key} {e.get('kind','real')} sig=({mp.nstr(e['sre'],6)},{mp.nstr(e['sim'],4)}) spread {float(sp[0]):.1e} err {es:.1e} a_err {float(abs(e['alpha']-tr['alpha'])):.1e}")
        print(f"  [{lane}] "+" | ".join(out))
for ang in (0.02, 0.05, 0.1, 0.2):
    def b(K, ang=ang):
        s = mp.mpc(mpf(1.5)*mp.cos(mpf(ang)), mpf(1.5)*mp.sin(mpf(ang)))
        return [2*v for v in real_part(binom_series(0.4, s, K, 1.3))]
    def t(ang=ang):
        return dict(sre=mpf(1.5)*mp.cos(mpf(ang)), sim=mpf(1.5)*mp.sin(mpf(ang)), alpha=mpf(0.4))
    run(f"pair a=.4 mod 1.5 ang {ang} pure", b, t)
def be(K):
    return [mpf(1)/mp.factorial(k) for k in range(K+1)]
run("entire exp(u)", be, lambda: dict(sre=mpf(1),sim=mpf(0),alpha=mpf(0)))
def bl(K):
    return [mpf(0)]+[ -1/(mpf(k)*mpf(2)**k) for k in range(1,K+1)]
run("log(1-u/2)", bl, lambda: dict(sre=mpf(2),sim=mpf(0),alpha=mpf(0)))
def bg(K):
    return [mpf(1)/mpf(3)**k for k in range(K+1)]
run("geometric 3^-k", bg, lambda: dict(sre=mpf(3),sim=mpf(0),alpha=mpf(-1)))
