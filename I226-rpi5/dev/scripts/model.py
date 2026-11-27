import sys, json, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import constraint_plateau as cp, dn
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs/"
D, hname, fam, side, Ts = int(sys.argv[1]), sys.argv[2], sys.argv[3], int(sys.argv[4]), float(sys.argv[5])
amps = [float(x) for x in sys.argv[6].split(",")]
X = {5: 18.0, 6: 15.0}[D]; n = D - 2
sm = json.load(open(RAW + f"D{D}_{fam}_h{hname}/summary.json"))
h = sm["h"]; pst = 0.5 * (sm["lo"] + sm["hi"]); A = pst + side * 1e-8
N = int(round(X / h)); s0 = int(round(Ts * cp.SQ2 / h))
d = cp.make_data(n, h, X, fam, A)
sol, q = dn.ellis_dense(n, N * h / cp.SQ2 + 1.0)
eps_m = 2.0 ** -52
def r_static(l): return sol(np.abs(l))[0]
# prediction of the rms of C++ at nodes (i, j = s0 - i) from injected uniform noise of amplitude a*2^-52 relative on r
I = np.arange(max(1, s0 - N), min(N - 1, s0 - 1) + 1)
J = s0 - I
pred = np.zeros(len(I))
for k, (i, j) in enumerate(zip(I, J)):
    jp = np.arange(0, j)                     # injection rows j' < j
    rr = r_static((i - jp) * h / cp.SQ2)
    pred[k] = np.sqrt(2.0 / 3.0) * eps_m / h ** 2 * r_static((i - j) * h / cp.SQ2) ** (-(n - 1)) * np.sqrt(np.sum(rr ** (2 * n)))
st0, info0 = cp.stream(d, stop=False, slices=(s0,), noise=0.0) if False else (None, None)
# row sweep to row s0, with slices
def run(a, seed=1):
    r = cp.stream_diag(d, np.float64, Sc=s0 + 2, noise=a * eps_m, seed=seed, slices=(s0,))
    return r["slices"]["pp"][s0], r["slices"]["mm"][s0]
t0 = time.time()
base_pp, base_mm = run(0.0)
print("base done %.0fs" % (time.time() - t0), flush=True)
ld = cp.ellis_rays_x(n, N, h, pulses=cp.pulses_of(fam, A)[0], symmetric=cp.pulses_of(fam, A)[1], eps=cp.pulses_of(fam, A)[2], dtype=np.longdouble)
ql = cp.stream_diag(ld, np.longdouble, Sc=s0 + 2, slices=(s0,))
qpp, qmm = ql["slices"]["pp"][s0], ql["slices"]["mm"][s0]
print("quad done %.0fs" % (time.time() - t0), flush=True)
l = (I - J) * h / cp.SQ2
bands = [(0, 0.25), (0.25, 0.5), (0.5, 1.0), (1.0, 2.0), (2.0, 3.0), (3.0, 5.0)]
def report(name, field, a_ref):
    print(f"  {name}: |l| band : rms observed (nodes)  rms model(a={a_ref:g})  obs/model")
    for lo, hi in bands:
        m = (np.abs(l) >= lo) & (np.abs(l) < hi) & np.isfinite(field[I])
        if m.sum() < 20: continue
        ob = np.sqrt(np.mean(field[I][m] ** 2)); md = np.sqrt(np.mean(pred[m] ** 2)) * a_ref
        print(f"    [{lo:4.2f},{hi:4.2f}) {ob:.3e} ({m.sum()})   {md:.3e}   {ob/md:.3f}")
print(f"D={D} h={h:.6f} {fam} side {side:+d}, time slice t = {s0*h/cp.SQ2:.3f} (s0 = {s0}); slice nodes {len(I)}")
report("natural roundoff (double - quad), C++", base_pp - qpp, 1.0)
report("natural roundoff (double - quad), C--", base_mm - qmm, 1.0)
for a in amps:
    pp, mm = run(a)
    report(f"injected a={a:g} (noisy - double), C++", pp - base_pp, a)
    report(f"injected a={a:g} (noisy - double), C--", mm - base_mm, a)
