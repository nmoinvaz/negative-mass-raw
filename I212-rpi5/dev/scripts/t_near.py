from shoot import *
import time, sys
cs = [float(a) for a in sys.argv[1:]]
for c in cs:
    fam = Fam(c)
    Ws = np.concatenate([np.linspace(0.02, 1.0, 25), np.linspace(1.2, 4.0, 8)])
    D = np.array([mismatch(fam, W, rtol=1e-10) for W in Ws])
    sg = np.sign(D)
    roots = []
    for i in range(len(Ws) - 1):
        if sg[i] != sg[i+1]:
            roots.append(brentq(lambda W: mismatch(fam, W, rtol=1e-10), Ws[i], Ws[i+1], xtol=1e-11))
    print(f'c={c}: rho_h={fam.rh:.6f} A1={fam.A1:.5f} pattern {"".join("+" if s>0 else "-" for s in sg)} roots {roots}', flush=True)
