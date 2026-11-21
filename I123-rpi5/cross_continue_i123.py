"""
Independent check of q(r_m; s) = f Z'/Z at the points of an --axis log where Re s < 0 (#123).

Reference: the decaying solution integrated on the real axis for Re s > 0 only, where the scaled system of #121 is
stable (Z exp(Psi), principal k, WKB start, Radau; a copy of zerilli_zeros.py's Zrm without --axis), then continued
analytically across Re s = 0 by a Taylor series fitted on a circle in Re s > 0. For a target s_t the circle has
centre 0.002 + i Im s_t and radius 0.0018 (Re s in [0.0002, 0.0038], clear of the poles of q, which lie 0.1 or more
away), N = 12 points, Taylor order K = 8. It shares with the --axis code only the potential V, r_m and Mext (from
background.solve_star); it shares neither the Jost start nor the rotated path.

Usage: python cross_continue_i123.py LOG [--flat] [--mutate=shift]
  LOG      an --axis log of zerilli_zeros.py ("q at the contour points" and "q at the holo points" lines)
  --flat   Mext = 0, and the reference at the targets is the closed form r k_l(s r) as well (a planted-truth control of
           the continuation itself: the continued value must equal the exact one)
  --mutate=shift   evaluates the Taylor series at s_t + 1e-4 (the comparison must fail)
Prints, for every point of the log, |q_log - q_cont|/|q_cont|, and exits 1 if one is above 1e-8 (Re s < 0 and Re s > 0 alike).
"""
import os, re, sys
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import spherical_kn

NR = os.path.expanduser('~/Source/negative-mass-i123/phase2/nonradial'); sys.path.insert(0, NR)
import background as B
from polar_solver import PolarProblem

args = [a for a in sys.argv[1:] if not a.startswith('--')]
opts = [a for a in sys.argv[1:] if a.startswith('--')]
flat, mutate = '--flat' in opts, ('--mutate=shift' in opts)
txt = open(args[0], encoding='utf-8').read()
tagline = txt.splitlines()[0]
m = re.match(r"eps([+-]\d+)_w([\d.]+)_l(\d+)_(\S+?)_(\S+?)_(\S+?)(?:_y0(\S+?))?(?:_z\d+)?(?:_flat)?_axis: ", tagline)
eps, w, l = int(m.group(1)), float(m.group(2)), int(m.group(3))
st = B.solve_star(w, eps); P = PolarProblem(st, l, rtol=1e-8)
rm, M = P.rm, (0.0 if flat else P.Mext)
lam = (l - 1) * (l + 2) / 2.0
Rz_of = lambda smin: rm + (40.0 + 20.0 * l) / smin + 50.0


def V(r):
    f = 1 - 2 * M / r
    return 2 * f * (lam**2 * r**2 * ((lam + 1) * r + 3 * M) + 9 * M**2 * (lam * r + M)) / (r**3 * (lam * r + 3 * M)**2)


def q_real_axis(s, Rz):
    """#121's Zrm (Re s > 0 only): y = (Z, f Z') exp(Psi), Psi = int_{Rz}^r k/f, k = sqrt(s^2 + V), WKB start, Radau."""
    k0 = np.sqrt(s * s + V(Rz)); ya = np.array([k0**-0.5, -k0**0.5], dtype=complex)

    def A(rho):
        r = np.exp(rho); f = 1 - 2 * M / r; k = np.sqrt(s * s + V(r))
        a = (r / f) * np.array([[k, 1.0], [s * s + V(r), k]])
        return np.block([[a.real, -a.imag], [a.imag, a.real]])
    sol = solve_ivp(lambda rho, y: A(rho) @ y, (np.log(Rz), np.log(rm)), np.r_[ya.real, ya.imag], method='Radau',
                    jac=lambda rho, y: A(rho), rtol=1e-11, atol=1e-14)
    z, p = sol.y[0, -1] + 1j * sol.y[2, -1], sol.y[1, -1] + 1j * sol.y[3, -1]
    return p / z


def q_continued(st_, Rz, N=12, K=8, c0=0.002, rho=0.0018):
    sc = complex(c0, st_.imag)
    th = 2 * np.pi * np.arange(N) / N
    vals = np.array([q_real_axis(sc + rho * np.exp(1j * t), Rz) for t in th])
    coef = [np.mean(vals * np.exp(-1j * k * th)) / rho**k for k in range(K + 1)]
    d = st_ - sc + (1e-4 if mutate else 0.0)
    return sum(c * d**k for k, c in enumerate(coef))


def q_exact_flat(s):
    x = s * rm
    return 1 / rm + s * spherical_kn(l, x, derivative=True) / spherical_kn(l, x)


rows = []
for name in ('contour', 'holo'):
    line = next(x for x in txt.splitlines() if x.startswith(f"   q at the {name} points: "))
    for sm, qm in re.findall(r"(\(\S+?\)) ([+-]?\d\.\d+e[+-]\d+[+-]\d\.\d+e[+-]\d+j)", line):
        rows.append((name, complex(sm), complex(qm)))
worst = 0.0
for name, s, qlog in rows:
    Rz = float(re.search(r"R_z = ([\d.]+)", tagline).group(1))  # the box's R_z, the same for every circle point
    qc = q_continued(s, Rz)
    d = abs(qlog - qc) / abs(qc)
    worst = max(worst, d)
    extra = f", exact flat {abs(qlog - q_exact_flat(s)) / abs(q_exact_flat(s)):.1e}, continued vs exact flat " \
            f"{abs(qc - q_exact_flat(s)) / abs(q_exact_flat(s)):.1e}" if flat else ""
    print(f"  {name:7s} s = {s.real:+.6g}{s.imag:+.6g}i  q_log {qlog:.12g}  q_continued {qc:.12g}  relative difference {d:.1e}{extra}",
          flush=True)
ok = worst <= 1e-8
print(f"{'PASS' if ok else 'FAIL'}: worst relative difference {worst:.1e} (limit 1e-8)" + ("  [mutate=shift]" if mutate else ""))
sys.exit(0 if ok else 1)
