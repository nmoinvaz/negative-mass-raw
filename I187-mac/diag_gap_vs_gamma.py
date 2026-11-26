"""Development diagnostic (#187): the crate's D (dev_jsonl, dd) against scipy's full-precision D (I4-win/I114-win partial files),
relative difference per variant and gamma, l = 4, 5, 6. Is the gap constant in gamma (a static input: star, M_ext) or does it grow
with gamma (scipy's integration error)?"""
import json, os, sys
JD = sys.argv[1] if len(sys.argv) > 1 else "dev_jsonl"   # the folder of the crate's rows (jsonl for the runs of record)
RAW = "/Users/nathan/Source/negative-mass-raw"
NAMES = {"base": "base (rtol1e-10, phi_cut1e-9, R60)", "tol": "rtol 1e-12", "phi": "phi_cut 1e-12 (larger r_m)", "r90": "background R=90", "r0": "r0 = 3e-3"}
for l in (4, 5, 6):
    sf = {}
    for folder in ("I4-win", "I114-win"):
        p = f"{RAW}/{folder}/convergence_l{l}_w0.7603.partial.csv"
        if not os.path.exists(p):
            continue
        for line in open(p):
            if line.startswith("["):
                k, g, v, _ = json.loads(line)
                sf[(k, g)] = v
    got = {}
    for line in open(f"{RAW}/I187-mac/{JD}/rows_l{l}_dd.jsonl"):
        o = json.loads(line)
        if o["cmd"] == "row":
            got[(o["gamma"], o["variant"])] = o["d_f64"]
    gs = sorted({g for g, _ in got})
    print(f"# l = {l}: |D_crate / D_scipy - 1| (scipy rtol 1e-10 unless the column is rtol 1e-12)")
    print("gamma      " + " ".join(f"{v:>9s}" for v in NAMES))
    for g in gs:
        row = []
        for v, name in NAMES.items():
            ref = sf.get((name, g))
            row.append(f"{abs(got[(g, v)] / ref - 1):9.1e}" if ref and (g, v) in got else f"{'-':>9s}")
        print(f"{g:<10g} " + " ".join(row))
