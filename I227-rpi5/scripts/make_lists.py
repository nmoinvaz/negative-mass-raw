#!/usr/bin/env python3
"""Emit the job lists of I227-rpi5: wave1 (bisections E and F, the float64 bisections, controls), wave2 (series, float64 series, perturbed
bisections, stall; needs wave1's p*), mutation runs. python3 make_lists.py wave1|wave2|mut   (run from the raw folder I227-rpi5)."""
import json, os, sys
from decimal import Decimal, getcontext
getcontext().prec = 40
RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYC = "timeout 7200 $PY -u extended_bisect.py"
what = sys.argv[1]
out = []


def pstar(tag):
    b = json.load(open(f"{RAW}/runs/{tag}/bisect.json"))
    return (Decimal(b["lo"]) + Decimal(b["hi"])) / 2


if what == "wave1":
    out += [f"E_bisect|{PYC} bisect --D=4 --h=0.02 --variant=E --lo=-0.01 --hi=0.01 --tol=1e-24 --out=$RAW/runs/E",
            f"F_bisect|{PYC} bisect --D=4 --h=0.02 --variant=F --lo=-0.01 --hi=0.01 --tol=1e-24 --out=$RAW/runs/F",
            f"f64_a|{PYC} f64 --D=4 --h=0.02 --k0=0 --k1=8 --X=34 --f64tol=1e-16 --out=$RAW/runs/f64",
            f"f64_b|{PYC} f64 --D=4 --h=0.02 --k0=8 --k1=16 --X=34 --f64tol=1e-16 --out=$RAW/runs/f64",
            f"controls|{PYC} controls"]
elif what == "wave2":
    for t in ("E", "F"):
        out += [f"{t}_series_m|{PYC} series --D=4 --h=0.02 --side=-1 --e0=3 --e1=20 --out=$RAW/runs/{t}",
                f"{t}_series_p|{PYC} series --D=4 --h=0.02 --side=1 --e0=3 --e1=20 --out=$RAW/runs/{t}",
                f"{t}_f64series|{PYC} f64series --D=4 --h=0.02 --e0=3 --e1=20 --X=34 --out=$RAW/runs/{t}"]
    ps = pstar("E")
    for name, kind, eta, w, tol in (("scaleP16", "--eta-scale", "1e-16", "1e-14", "1e-24"), ("scaleM16", "--eta-scale", "-1e-16", "1e-14", "1e-24"),
                                    ("bumpP8", "--bump", "1e-8", "1e-6", "1e-16"), ("bumpP10", "--bump", "1e-10", "1e-8", "1e-18"),
                                    ("bumpP16", "--bump", "1e-16", "1e-14", "1e-24"), ("bumpM16", "--bump", "-1e-16", "1e-14", "1e-24")):
        lo, hi = ps - Decimal(w), ps + Decimal(w)
        out.append(f"pert_{name}|{PYC} bisect --D=4 --h=0.02 --variant=E {kind}={eta} --lo={float(lo)!r} --hi={float(hi)!r} --tol={tol} --out=$RAW/runs/pert/{name}")
    pf = float(pstar("F"))
    out += [f"stall_D4|{PYC} stall --D=4 --h=0.02 --variant=F --pc={pf!r} --delta=1e-10 --tmax=17 --snap=0.25 --L0=4 --k0=0 --k1=8 --out=$RAW/runs/stall/D4",
            f"stall_D5|{PYC} stall --D=5 --h=0.0070710678118654745 --variant=F --pc=0.0002884790369034818 --delta=1e-10 --tmax=11 --snap=0.25 --L0=4 --k0=0 --k1=8 --out=$RAW/runs/stall/D5",
            f"stall_D6|{PYC} stall --D=6 --h=0.005 --variant=F --pc=0.0011155147989984474 --delta=1e-10 --tmax=8.5 --snap=0.25 --L0=4 --k0=0 --k1=8 --out=$RAW/runs/stall/D6"]
elif what == "wave3":      # the floors at D = 5, 6: binary128 p* (variant F, narrow bracket round #40's float64 p*) and K = 8 float64 bisections
    for D, h, X, pf in ((5, "0.0070710678118654745", 18.0, 0.0002884790369034818), (6, "0.005", 15.0, 0.0011155147989984474)):
        out += [f"D{D}F_bisect|{PYC} bisect --D={D} --h={h} --variant=F --lo={pf - 3e-11!r} --hi={pf + 3e-11!r} --tol=1e-16 --out=$RAW/runs/D{D}F",
                f"f64_D{D}_a|{PYC} f64 --D={D} --h={h} --k0=0 --k1=4 --X={X} --f64tol=1e-16 --out=$RAW/runs/f64_D{D}",
                f"f64_D{D}_b|{PYC} f64 --D={D} --h={h} --k0=4 --k1=8 --X={X} --f64tol=1e-16 --out=$RAW/runs/f64_D{D}"]
open(f"{RAW}/lists/{what}.txt", "w").write("\n".join(out) + "\n")
print("\n".join(l.split("|")[0] for l in out))
