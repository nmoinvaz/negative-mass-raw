"""Design probe of #188 (development): the size of three wrong inputs' effect on the stored box's values, from the stored cache alone.
For every cached point s of the box (winding2's normalization, fixed R_s):
  strip_off  D without the phase strip exp(-i Im[(k+ + k-)(R_s - r_m) + (k+ + k- + s) r_m]): phase error = that Im, mod 2 pi
  conj_s     D evaluated at conj(s) (D(conj s) = conj D(s)): phase error 2|arg D|, modulus error 0
  rs_shift   R_s of the integration moved by dR = +1 while the strip keeps the old R_s: phase error Im(k+ + k-) dR (mod 2 pi)
printed: how many points have an error above 1e-9 in phase, and the largest, the median.
"""
import sys, pickle, numpy as np
cache = pickle.load(open(sys.argv[1], 'rb')); w = float(sys.argv[2]); rm = float(sys.argv[3]); Rs = float(sys.argv[4])
ks = lambda s: (np.sqrt(1 + (s - 1j*w)**2), np.sqrt(1 + (s + 1j*w)**2))
wrap = lambda x: abs((x + np.pi) % (2*np.pi) - np.pi)
res = {'strip_off': [], 'conj_s': [], 'rs_shift': []}
for s, d in cache.items():
    kp, km = ks(s)
    res['strip_off'].append(wrap(((kp + km)*(Rs - rm) + (kp + km + s)*rm).imag))
    res['conj_s'].append(wrap(2*np.angle(d)) if abs(s.imag) > 0 else 0.0)
    res['rs_shift'].append(wrap(((kp + km).imag)*1.0))
n = len(cache)
print(f"{n} points, R_s = {Rs}, r_m = {rm}")
for k, v in res.items():
    v = np.array(v)
    print(f"{k:10s}: {int((v > 1e-9).sum()):4d} of {n} points above 1e-9 rad; largest {v.max():.3f}, median {np.median(v):.3f}, smallest nonzero {v[v > 0].min():.2e}")
