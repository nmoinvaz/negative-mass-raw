"""the crate's dd and f64 D at the same points of the three thinnest-margin boxes (jsonl_dd against jsonl_rec; unstripped D, so the phase is the strip's too)"""
import json, os, sys
import numpy as np
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for box in ("rep_l4", "s1_l3", "s1_l6"):
    a, b = {}, {}
    for d, f in ((a, f"jsonl_dd/{box}_dd.jsonl"), (b, f"jsonl_rec/{box}_f64.jsonl")):
        for line in open(os.path.join(RAW, f)):
            o = json.loads(line); d[(o["re"], o["im"])] = complex(*o["d_f64"])
    common = sorted(set(a) & set(b))
    ph = max(abs(np.angle(a[k] / b[k])) for k in common)
    md = max(abs(abs(a[k]) / abs(b[k]) - 1) for k in common)
    print(f"{box}: {len(common)} common points (dd {len(a)}, f64 {len(b)}): f64 against dd, worst phase {ph:.2e} rad, worst modulus ratio {md:.2e}")
