import sys, json, time, numpy as np
sys.path.insert(0, "/home/nathan/Source/negative-mass-i226/notes/wormhole_evolution")
import constraint_plateau as cp
RAW = "/home/nathan/Source/negative-mass-raw/I40-dh610/runs/"
PH = {5: ("0.00707107", "0.00353553", "0.00176777"), 6: ("0.005", "0.0025", "0.00125")}
def pstar(D, hname, fam="S"):
    sm = json.load(open(RAW + f"D{D}_{fam}_h{hname}/summary.json")); return sm["h"], 0.5 * (sm["lo"] + sm["hi"])
def go(D, h, fam, A, Tc, X, label, **kw):
    rec, sl = cp.slab_run(D - 2, h, fam, A, Tc, X, **kw)
    kws = " ".join(f"{k}={v}" for k, v in kw.items())
    print(f"{label} D={D} h={h:.6f} Tc={Tc} {kws}: slab max {rec['max']:.4e} ({rec['which']}) at i={rec['i']} j={rec['j']} (x+ {rec['xp']:.3f}, x- {rec['xm']:.3f}, t {rec['t']:.3f})  [{rec['secs']}s]", flush=True)
    return rec
