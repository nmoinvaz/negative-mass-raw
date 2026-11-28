#!/usr/bin/env python3
"""devtune.py ROOT XC W H G1 [G1 ...]: development. For a route (centre XC, width W), find B so that gamma_1 at departure (h = H) is within 1 % of each target, by a secant
iteration in (ln B, ln gamma_1) starting from the local law gamma_1 = k B^2 (k from the first run at B = 0.1). Prints one RESULT line per run and a TUNED line per target."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import devpoint as dp

root, xc, w, h = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
targets = [float(x) for x in sys.argv[5:]]
hist = []


def run(B):
    B = float(f"{B:.4g}")
    res = dp.run_point(root, (B, xc, w), h)
    print("RESULT", json.dumps(res), flush=True)
    if res.get("stall") and res.get("g1") == res.get("g1"):
        hist.append((B, res["g1"]))
    return res


for tg in targets:
    # start: local law through the nearest history point, exponent 2
    if hist:
        Bk, gk = min(hist, key=lambda x: abs(math.log(x[1] / tg)))
        B = Bk * math.sqrt(tg / gk)
    else:
        B = 0.1
    done = None
    for it in range(6):
        res = run(B)
        if not (res.get("stall") and res.get("g1") == res.get("g1")):
            print("TUNED", json.dumps(dict(target=tg, B=B, note="no stall or no member", xc=xc, w=w)), flush=True)
            break
        if abs(res["g1"] / tg - 1) <= 0.01:
            done = res
            break
        near = sorted(hist, key=lambda x: abs(math.log(x[1] / tg)))[:2]
        if len(near) >= 2 and abs(math.log(near[0][1] / near[1][1])) > 1e-6:
            (b1, g1_), (b2, g2_) = near
            q = math.log(g2_ / g1_) / math.log(b2 / b1)
            q = min(max(q, 0.8), 4.0)
        else:
            q = 2.0
        Bk, gk = near[0]
        B = Bk * (tg / gk) ** (1.0 / q)
    if done:
        print("TUNED", json.dumps(dict(target=tg, B=done["spec"][0], xc=xc, w=w, g1=done["g1"], rth=done["rth"], rdot=done["rdot"], M=done["M"], ps=done["ps"])), flush=True)
