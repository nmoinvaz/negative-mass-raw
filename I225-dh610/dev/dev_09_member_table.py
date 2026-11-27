import sys, math, time, json
sys.path.insert(0, "/home/nathan/Source/negative-mass-i225/notes/wormhole_evolution")
import numpy as np
import throat_locus as tl
D = int(sys.argv[1]); h = float(sys.argv[2]); d = sys.argv[3]
La = tl.load_run(f"{d}/stall_D{D}_h{h:g}_side-1.npz"); Lb = tl.load_run(f"{d}/stall_D{D}_h{h:g}_side1.npz")
rows = tl.member_table(La, Lb, D)
W = tl.W_EXACT[D-2]
print(f"{'t':>5} {'tau':>6} {'r_th':>7} {'v':>7} {'f':>7} {'s_th':>8} {'rms':>8} {'qn/qg':>9} {'lam':>7} {'1/lam':>7} {'r/W':>7}  M+(1.5,2,3) M-(1.5,2,3)")
for r in rows:
    ms = [(round(a,5), round(b,5)) for a, b in zip(r['Mp'], r['Mm'])]
    g = r['sth']/math.sqrt(max(1e-12, 1-r['sth']**2)) if np.isfinite(r['sth']) else float('nan')
    print(f"{r['t']:5.1f} {r['tau']:6.2f} {r['r_th']:7.4f} {r['v']:+7.4f} {r['f']:+7.4f} {r['sth']:+8.4f} {r['sth_rms']:8.1e} {r['qratio']:9.3e} {r['lam']:7.4f} {1/r['lam'] if r['lam']>0 else float('nan'):7.4f} {r['r_th']/W:7.4f}  {ms[1:4]}  g1={g:.3f}")
