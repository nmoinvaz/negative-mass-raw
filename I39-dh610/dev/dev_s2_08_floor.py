import sys, time
sys.path.insert(0, '/home/nathan/Source/negative-mass-i39/notes/wormhole_evolution')
import numpy as np, dn
exec(open('/home/nathan/Source/negative-mass-raw/I39-dh610/dev/dev_s2_06_bisect.py').read().split("for n, h, X in")[0])
W3 = W[3]
n = 3
for h, tol in ((0.01/np.sqrt(2), 1e-10), (0.01/np.sqrt(2), 1e-13), (0.005/np.sqrt(2), 1e-13)):
    X = 15.0
    lo, hi, k = bisect(n, h, X, -0.01, 0.01, tol)
    print(f"h={h:.5f} tol={tol:g}: A* ~ {0.5*(lo+hi):.12e} ({k} runs)")
    for A, name in ((lo, 'collapse'), (hi, 'expand')):
        res = run(n, h, A, X)
        H, tau = res.diag['H'], res.diag['tau']
        print(f"  {name}: tau_end {tau[-1]:.2f}; |H| at tau = 3,4,5,...:  " + " ".join(f"{abs(H[np.argmin(abs(tau-t))]):.1e}" for t in np.arange(3, 17, 1.0)))
        sg = np.sign(H[np.isfinite(H)]); print("    sign changes of H:", int(np.sum(sg[1:] != sg[:-1])))
