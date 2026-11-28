#!/usr/bin/env python3
"""s3_timing.py A B: JT5 of README A4: the `setup` record of `d` (f64 lane, gamma 1) for l = 2 and 6, three times each, for two binaries:
the table's build time t_table (s), the number of table steps and linear_defect. Reported, no bar."""
import json
import os
import subprocess
import sys

HERE = "/Users/nathan/Source/negative-mass-i192/phase2/nonradial"
sys.path.insert(0, HERE)
import taylor_polar as tp  # noqa: E402


def run(b, cmd, **kw):
    args = [b, cmd] + [f"{k}={v}" for k, v in kw.items()]
    p = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True, cwd=HERE, env=dict(os.environ, RAYON_NUM_THREADS="2"))
    if p.returncode:
        raise RuntimeError(f"{' '.join(args)[:150]} exited {p.returncode}: {p.stderr[-300:]}")
    return [json.loads(x) for x in p.stdout.splitlines() if x.startswith("{")]


a, b = sys.argv[1:3]
s = run(a, "star", **tp.MODEL)[0]
star = dict(tp.MODEL, pc=s["pc"], zc=s["zc"])
for l in (2, 6):
    for name, bin_ in (("own", a), ("multishoot", b)):
        rows = []
        for _ in range(3):
            r = run(bin_, "d", lane="f64", l=l, gammas="1.0", **star)[0]
            rows.append(r)
        ts = [r["t_table"] for r in rows]
        print(f"l = {l} {name}: t_table {', '.join(f'{t:.3f}' for t in ts)} s; table_steps {rows[0]['table_steps']}; linear_defect {rows[0]['linear_defect']:.3e}; setup field table = {rows[0].get('table')}", flush=True)
