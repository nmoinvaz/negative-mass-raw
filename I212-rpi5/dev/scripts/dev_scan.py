from shoot import *
import sys, time
cs = [float(a) for a in sys.argv[1:]]
for c in cs:
    t0 = time.time()
    fam = Fam(c) if c != 0 else None
    if c == 0:
        continue
    Ws = np.exp(np.linspace(np.log(0.01), np.log(8.0), 70))
    D = np.array([mismatch(fam, W, rtol=1e-10) for W in Ws])
    sg = np.sign(D)
    roots = []
    for i in range(len(Ws) - 1):
        if sg[i] != sg[i+1]:
            roots.append(brentq(lambda W: mismatch(fam, W, rtol=1e-10), Ws[i], Ws[i+1], xtol=1e-12))
    print(f'c={c}: rho_h={fam.rh:.6f} A1={fam.A1:.5f} n_roots={len(roots)} roots={roots} min|D|={np.min(abs(D)):.3e} D(0.01)={D[0]:.3e} D(8)={D[-1]:.3e} time={time.time()-t0:.0f}s', flush=True)
