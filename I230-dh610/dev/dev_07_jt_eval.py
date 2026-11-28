"""#230 development: the jump-test runs of dev_07 (dev/jt/) through the declared checks JTK, JTC, SP1, SP2, WS, and the D = 6 pilots of dev_01 through SP1, SP2."""
import sys, os, glob
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i230/notes/wormhole_evolution"))
import throat_scaling as ts
J = os.path.expanduser("~/Source/negative-mass-raw/I230-dh610/dev/")
jt = [ts.summarize(p) for p in sorted(p for p in glob.glob(J + "jt/D*_S_b*.npz") if "partial" not in p)]
pil = [ts.summarize(p) for p in sorted(glob.glob(J + "dev_01_D6_*.npz"))]
runs = {"JT": jt, "D6c": pil}          # the pilots only through the spatial test (group D6c is read by SP1, SP2 and RES6; RES6 is skipped without D6)
ts.analyze(runs)
print()
for s in jt:
    print(f"  {s['name']:34s} k_inf={s['kinf']:.4f} pred={ts.k_jump(s['n'], s['b']):.4f} rel={s['kinf'] / ts.k_jump(s['n'], s['b']) - 1:+.1e} | c={s['c']:.4f} (r={s['r_c']:.0f}) pred={ts.c_jump(s['n'], s['b']):.4f} rel={s['c'] / ts.c_jump(s['n'], s['b']) - 1:+.1e} | "
          f"spatial " + "; ".join(f"{x:.0f}: {er:.1e}, {ep:.1e}" for x, er, ep in s["spatial"]))
for s in pil:
    print(f"  {s['name']:34s} spatial " + "; ".join(f"{x:.0f}: {er:.1e}, {ep:.1e}" for x, er, ep in s["spatial"]))
