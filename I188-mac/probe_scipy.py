"""Design probe of #188 (development, not a run of record): winding2's D at stored points of a box, on this Mac.

For each chosen cached point s of a winding2 cache it computes, with winding2.py's own normalization
(fixed R_s, the phase strip exp(-i Im[(k+ + k-)(R_s - r_m) + (k+ + k- + s) r_m])):
  D8   scipy path at rtol 1e-8 (winding2's default)             -> compared with the stored value (reproduction)
  D12  scipy path at rtol 1e-12                                   -> scipy's own truncation error at 1e-8
  H12  the same at rtol 1e-12 with LAPACK's QR replaced by modified Gram-Schmidt with Hermitian inner product and a
       positive real R diagonal (the crate's convention) -> D is the same function if the gauge argument holds
  B12  as H12 but with the bilinear (conjugate-free) inner product (the control: must differ)
usage: probe_scipy.py CACHE.pkl eps w l x0 x1 y1 [y0] NPOINTS-OR-TARGETS
"""
import sys, os, time, pickle, numpy as np
HERE = os.path.expanduser("~/Source/negative-mass-i188/phase2/nonradial")
sys.path.insert(0, HERE)
import background as B
from polar_solver import PolarProblem

cache_path, eps, w, l, x0, x1, y1 = sys.argv[1], int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), *map(float, sys.argv[5:8])
y0 = float(sys.argv[8]) if len(sys.argv) > 8 else 0.0
sym = (y0 == 0.0)
cache = pickle.load(open(cache_path, "rb"))
targets = [complex(0.1, 0.24), complex(0.1, 1.76), complex(0.1, 2.5), complex(2.0, 0.0), complex(2.0, 2.5), complex(1.0, 1.0), complex(0.1, 0.0),
           complex(0.5, 0.5)]
if len(sys.argv) > 9:
    targets = [complex(t) for t in sys.argv[9].split(";")]
pts = []
for t in targets:
    k = min(cache, key=lambda c: abs(c - t))
    if k not in pts:
        pts.append(k)

st = B.solve_star(w, eps)


def mgs(Y, hermitian=True):
    """modified Gram-Schmidt twice, positive real R diagonal; returns Q and the phase product (1: the diagonal is positive)"""
    Y = Y.astype(complex) if np.iscomplexobj(Y) else Y.copy()
    n, k = Y.shape
    Q = np.zeros_like(Y)
    for c in range(k):
        v = Y[:, c].copy()
        for _ in range(2):
            for p in range(c):
                d = (np.vdot(Q[:, p], v) if hermitian else np.dot(Q[:, p], v))
                v = v - d * Q[:, p]
        nrm = np.sqrt(np.vdot(v, v).real) if hermitian else np.sqrt(np.dot(v, v))
        Q[:, c] = v / nrm
    return Q, 1.0


class PH(PolarProblem):
    @staticmethod
    def _qr(Y):
        return mgs(Y, True)


class PB(PolarProblem):
    """the control: the same Gram-Schmidt with a bilinear (conjugate-free) inner product"""

    @staticmethod
    def _qr(Y):
        return mgs(Y, False)


ks = lambda s: (np.sqrt(1 + (s - 1j * w) ** 2), np.sqrt(1 + (s + 1j * w) ** 2))
cands = [x0 + 1j * y for y in np.linspace(y0, y1, 200)] + [x + 1j * y1 for x in np.linspace(x0, x1, 200)]
if not sym:
    cands += [x1 + 1j * y for y in np.linspace(y0, y1, 200)] + [x + 1j * y0 for x in np.linspace(x0, x1, 200)]
kmin = min(min(k.real for k in ks(c)) for c in cands)


def make(cls, rtol):
    P = cls(st, l, rtol=rtol)
    P.Rs_fixed = P.rm + 40.0 / kmin
    return P


def dw2(P, s):
    kp, km = ks(s)
    t = time.time()
    d = P.D(s) * np.exp(-1j * ((kp + km) * (P.Rs_fixed - P.rm) + (kp + km + s) * P.rm).imag)
    return d, time.time() - t


P8, P12, H12, B12 = make(PolarProblem, 1e-8), make(PolarProblem, 1e-12), make(PH, 1e-12), make(PB, 1e-12)
print(f"# box eps={eps} w={w} l={l} [{x0},{x1}] y1={y1} y0={y0}: r_m={P8.rm!r} R_s fixed={P8.Rs_fixed!r} (kmin {kmin:.5f}); cache {os.path.basename(cache_path)} n={len(cache)}")
print("# columns: s | |stored| | arg stored | rel(modulus) and abs(phase) differences against the stored value: D8, D12, H12, B12 | times D8 D12 H12 (s)")
rel = lambda a, b: abs(abs(a) / abs(b) - 1)
ph = lambda a, b: abs(np.angle(a / b))
for s in pts:
    stored = cache[s]
    r = {}
    for name, P in (("D8", P8), ("D12", P12), ("H12", H12), ("B12", B12)):
        r[name] = dw2(P, s)
    d8, d12, h12, b12 = (r[n][0] for n in ("D8", "D12", "H12", "B12"))
    print(f"s={s.real:.4f}{s.imag:+.4f}j |D|={abs(stored):.4e} arg={np.angle(stored):+.4f} | "
          f"D8 {rel(d8, stored):.1e} {ph(d8, stored):.1e} | D12 {rel(d12, stored):.1e} {ph(d12, stored):.1e} | "
          f"H12 {rel(h12, stored):.1e} {ph(h12, stored):.1e} | H12-D12 {rel(h12, d12):.1e} {ph(h12, d12):.1e} | B12-D12 {rel(b12, d12):.1e} {ph(b12, d12):.1e} | "
          f"t {r['D8'][1]:.1f} {r['D12'][1]:.1f} {r['H12'][1]:.1f}", flush=True)
