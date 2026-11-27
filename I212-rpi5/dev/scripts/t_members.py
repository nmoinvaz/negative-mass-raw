from shoot import *
import time, sys
cs = [float(a) for a in sys.argv[1:]]
for c in cs:
    fam = Fam(c)
    print(f'c = {c}: K = {fam.K:.6f}, rho_h = {fam.rh:.6f}, A1 = {fam.A1:.6f}', flush=True)
    Ws = np.linspace(0.05, 4.0, 40)
    t = time.time()
    D = scan(fam, Ws)
    print('  scan time', time.time() - t)
    sg = np.sign(D)
    roots = []
    for i in range(len(Ws) - 1):
        if sg[i] != sg[i+1]:
            r = brentq(lambda W: mismatch(fam, W), Ws[i], Ws[i+1], xtol=1e-13)
            roots.append(r)
    print('  sign pattern:', ''.join('+' if s > 0 else '-' for s in sg))
    print('  roots W:', roots, ' W^2:', [r*r for r in roots])
