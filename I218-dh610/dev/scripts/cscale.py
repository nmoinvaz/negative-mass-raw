import numpy as np, sys
from scipy.linalg import eigvals
def qnms(Vf, theta, X=40.0, N=2400):
    s = np.linspace(-X, X, N + 2)[1:-1]; h = s[1] - s[0]
    e = np.exp(1j * theta)
    V = Vf(s * e)
    main = 2 / h**2 * np.exp(-2j * theta) + V
    off = -np.ones(N - 1) / h**2 * np.exp(-2j * theta)
    H = np.diag(main) + np.diag(off, 1) + np.diag(off, -1)
    ev = eigvals(H)
    om = np.sqrt(ev.astype(complex))
    om = np.where(om.real < 0, -om, om)          # Re omega > 0 branch
    return om
pots = {"test scalar l=1 2/R2+1/R4": lambda r: 2/(r*r+1) + 1/(r*r+1)**2, "l=2 master 6/R2-3/R4": lambda r: 6/(r*r+1) - 3/(r*r+1)**2,
        "V_a=2/R2-3/R4": lambda r: 2/(r*r+1) - 3/(r*r+1)**2, "V_b=1/R4": lambda r: 1/(r*r+1)**2}
for name, Vf in pots.items():
    for th in (0.7, 0.9):
        om = qnms(Vf, th)
        good = om[(om.imag < -0.02) & (om.real > 0.05) & (np.angle(om) > -th + 0.05)]
        good = good[np.argsort(-good.imag)]
        print("%-30s theta=%.1f: %s" % (name, th, [complex(round(z.real, 6), round(z.imag, 6)) for z in good[:4]]), flush=True)
