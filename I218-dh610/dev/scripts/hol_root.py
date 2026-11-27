import sys, time, cmath
import numpy as np
from scipy.optimize import newton
import qnm_fast as Q
from qnm_fast import frame, rhs_schr, rhs3c, g3n
def D_hol(Wv, theta, kind):
    e = cmath.exp(1j * theta); mu = (Wv * e).real; S = 22.0 / abs(mu); ch = 6.0 / abs(mu); lam = Wv * Wv
    if kind is None:
        yR = frame(rhs3c, (e, lam), S, 0.0, 3, ch); yL = frame(rhs3c, (e, lam), -S, 0.0, 3, ch)
        g = np.array(Q.g3n(0.0, lam, 1.0, 0.0), dtype=complex)
        return np.linalg.det(np.column_stack([yL / yL[0], yR / yR[0], g / g[0]]))
    yR = frame(rhs_schr, (e, lam, kind), S, 0.0, 2, ch); yL = frame(rhs_schr, (e, lam, kind), -S, 0.0, 2, ch)
    return (yL[0] * yR[1] - yL[1] * yR[0]) / (yL[0] * yR[0])
if __name__ == "__main__":
    kind = None if sys.argv[1] == "polar" else int(sys.argv[1])
    t0 = time.time()
    for om0 in [complex(a) for a in sys.argv[2:]]:
        f = lambda om: D_hol(-1j * om, 0.5, kind)
        try:
            om = newton(f, om0, tol=1e-12, maxiter=80)
            print("kind %s start %s -> omega = %.10f %+.10fi |f| = %.1e (%.0fs)" % (kind, om0, om.real, om.imag, abs(f(om)), time.time() - t0), flush=True)
        except Exception as ex:
            print("kind %s start %s failed: %s (%.0fs)" % (kind, om0, ex, time.time() - t0), flush=True)
