"""dev02: member rows (pair-mean profile) against t for several delta, from dev01's member.json. usage: dev02_rows.py DIR h E1,E2,..."""
import json, sys
import numpy as np
d, h, es = sys.argv[1], float(sys.argv[2]), [float(x) for x in sys.argv[3].split(",")]
M = {e: json.load(open(f"{d}/e{e:g}/h{h:g}/member.json")) for e in es}
def gam(s): return s / np.sqrt(1 - s * s)
print("t     " + "  ".join(f"e={e:g}: r_th      g1        rms" for e in es))
ts = sorted({r["t"] for e in es for r in M[e]["rows"]})
for t in ts:
    out = []
    for e in es:
        rr = [r for r in M[e]["rows"] if abs(r["t"] - t) < 1e-9]
        if rr:
            r = rr[0]; out.append(f"{r['r_th']:.6f}  {r['g1_m']:.6f}  {r['rms_m']:.1e}")
        else:
            out.append(" " * 28)
    print(f"{t:5.1f} " + "  ".join(out))
