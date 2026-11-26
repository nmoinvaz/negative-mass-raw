"""Development diagnostic (#187): is the crate-vs-scipy difference of D at the capped rows the star? The crate's star started at
r_s = 1e-3 with scipy's leading-order boundary condition (S1's 'matched' start, which agrees with solve_star to 1e-10) against the
exact regular start, both through the crate's `rows` at (l, gamma), compared with scipy's full-precision values (I114-win/I4-win)."""
import json, os, subprocess, sys
HERE = "/Users/nathan/Source/negative-mass-i187/phase2/nonradial"
BIN = os.path.join(HERE, "taylor_polar/target/release/taylor_polar")
RAW = "/Users/nathan/Source/negative-mass-raw"
l, g = int(sys.argv[1]), float(sys.argv[2])
MODEL = ["omega=0.7603", "eps=-1.0", "lam=10240.0", "mu=21845333.333333336"]
NAMES = {"base": "base (rtol1e-10, phi_cut1e-9, R60)", "tol": "rtol 1e-12", "phi": "phi_cut 1e-12 (larger r_m)", "r90": "background R=90", "r0": "r0 = 3e-3"}
sf = {}
for folder in ("I4-win", "I114-win"):
    p = f"{RAW}/{folder}/convergence_l{l}_w0.7603.partial.csv"
    if os.path.exists(p):
        for line in open(p):
            if line.startswith("["):
                k, gg, v, _ = json.loads(line)
                sf[(k, gg)] = v
for rs in ("1e-8", "1e-3"):
    st = json.loads(subprocess.run([BIN, "star"] + MODEL + [f"rs={rs}"], capture_output=True, text=True).stdout.splitlines()[0])
    out = subprocess.run([BIN, "rows", f"l={l}", "lane=dd", f"gammas={g!r}", f"pc={st['pc']}", f"zc={st['zc']}", f"rs={rs}"] + MODEL, capture_output=True, text=True)
    print(f"# rs = {rs}: pc {st['pc']} zc {st['zc']} (rc {out.returncode})", flush=True)
    for line in out.stdout.splitlines():
        o = json.loads(line)
        if o["cmd"] != "row":
            continue
        ref = sf.get((NAMES[o["variant"]], g))
        print(f"rs={rs} l={l} gamma={g:g} {o['variant']:5s} D={o['d_f64']:+.12e} scipy={ref:+.12e} rel {abs(o['d_f64'] / ref - 1):.2e}" if ref else f"rs={rs} {o['variant']} no scipy value", flush=True)
