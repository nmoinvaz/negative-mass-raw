import sys, time, cmath
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import root
from coef import N2

def frame1(rhs, s0, s1, chunk, dim=2, rtol=1e-11):
    Y = np.array([1.0 + 0.2j, 0.3 - 0.1j])[:dim]
    Y = Y / np.linalg.norm(Y)
    s = s0; d = np.sign(s1 - s0)
    while abs(s - s1) > 1e-12:
        s2 = s + d * min(abs(s1 - s), chunk)
        sol = solve_ivp(lambda t, y: rhs(t, y), [s, s2], Y.astype(complex), method="DOP853", rtol=rtol, atol=1e-30)
        Y = sol.y[:, -1]; Y = Y / np.linalg.norm(Y); s = s2
    return Y

def D_general(Wv, rhsfun, theta, S=None):
    e = cmath.exp(1j * theta); mu = (Wv * e).real
    S = S or 22.0 / abs(mu); chunk = 6.0 / abs(mu)
    rhs = lambda s, y: e * rhsfun(s * e, Wv * Wv, y)
    yR = frame1(rhs, S, 0.0, chunk); yL = frame1(rhs, -S, 0.0, chunk)
    # fix phases: det of [yL yR]
    return yL[0] * yR[1] - yL[1] * yR[0]

# systems
mine = lambda r, lamv, y: N2(r, lamv, 1.0, 0.0) @ y
def schr(Vf):
    # Z'' = (V - omega^2) Z = (V + lam) Z ; y = (Z, Z')
    return lambda r, lamv, y: np.array([y[1], (Vf(r) + lamv) * y[0]])
Vs = {"mine (invariants)": mine,
      "Z'' = (2/R2 + 1/R4 + lam) Z test scalar l=1": schr(lambda r: 2 / (r * r + 1) + 1 / (r * r + 1)**2),
      "V = 2/R2 - 3/R4 (l>=2 formula at l=1)": schr(lambda r: 2 / (r * r + 1) - 3 / (r * r + 1)**2)}
def qnm(rhsfun, om0, theta=0.5):
    f = lambda v: (lambda d: [d.real, d.imag])(D_general(-1j * (v[0] + 1j * v[1]), rhsfun, theta))
    r = root(f, [om0.real, om0.imag], tol=1e-12)
    return r.x[0] + 1j * r.x[1], r.success
t0 = time.time()
for name, fn in Vs.items():
    for om0 in (0.9 - 0.3j, 1.2 - 0.25j):
        om, ok = qnm(fn, om0)
        print("%-50s start %s -> omega = %.6f %+.6fi ok=%s %.0fs" % (name, om0, om.real, om.imag, ok, time.time() - t0), flush=True)
