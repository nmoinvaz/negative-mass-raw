import mpmath as mp, itertools
mp.mp.dps = 20
K = 2 / mp.pi
A = lambda r: -r ** 2 + K * (r + (1 + r ** 2) * mp.atan(r))
roots = []
for x0, y0 in itertools.product([-4, -2, -1, -0.5, 0.5, 1, 2, 4], [-4, -2, -1, -0.5, 0.5, 1, 2, 4]):
    try:
        r = mp.findroot(A, mp.mpc(x0, y0), tol=1e-15, maxsteps=60)
    except Exception:
        continue
    if abs(r) > 1e-6 and all(abs(r - q) > 1e-8 for q in roots):
        roots.append(r)
roots.sort(key=lambda z: abs(z))
for r in roots[:12]:
    print(mp.nstr(r, 10), "|r| =", mp.nstr(abs(r), 6), "A' =", mp.nstr(mp.diff(A, r), 6))
