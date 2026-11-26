"""Development diagnostic (#187): the crate's f64 lane against its dd lane per variant at the capped gamma (dd from dev_jsonl). If scipy's
gap at the top gamma is f64 roundoff, the f64 lane should show a similar size and variant pattern."""
import json, os, subprocess, sys
HERE = "/Users/nathan/Source/negative-mass-i187/phase2/nonradial"
BIN = os.path.join(HERE, "taylor_polar/target/release/taylor_polar")
RAW = "/Users/nathan/Source/negative-mass-raw/I187-mac"
MODEL = ["omega=0.7603", "eps=-1.0", "lam=10240.0", "mu=21845333.333333336"]
st = json.loads(subprocess.run([BIN, "star"] + MODEL, capture_output=True, text=True).stdout.splitlines()[0])
for l, g in ((5, 6000.0), (6, 12000.0)):
    dd = {}
    for line in open(f"{RAW}/dev_jsonl/rows_l{l}_dd.jsonl"):
        o = json.loads(line)
        if o["cmd"] == "row" and o["gamma"] == g:
            dd[o["variant"]] = o["d_f64"]
    out = subprocess.run([BIN, "rows", f"l={l}", "lane=f64", f"gammas={g!r}", f"pc={st['pc']}", f"zc={st['zc']}"] + MODEL, capture_output=True, text=True)
    for line in out.stdout.splitlines():
        o = json.loads(line)
        if o["cmd"] == "row":
            print(f"l={l} gamma={g:g} {o['variant']:5s} f64 {o['d_f64']:+.12e} dd {dd[o['variant']]:+.12e} rel {abs(o['d_f64'] / dd[o['variant']] - 1):.2e} wall {o['wall']:.2f} s", flush=True)
