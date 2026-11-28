#!/usr/bin/env python3
"""Read the effect of the run-level mutations (float_cast, noise_f64, quad_h, eta_dropped) with `extended_bisect.py analyze --only=...` on views that put the mutated
run in place of the unmutated one. python3 mut_runs_table.py MUTDIR BASEDIR [--thin]   (MUTDIR from run_mut_runs.sh; BASEDIR has runs/E, runs/f64 of the clean data)"""
import os, subprocess, sys, tempfile, re
NR = os.path.expanduser("~/Source/negative-mass-i227/notes/wormhole_evolution")
PY = os.path.expanduser("~/Source/negative-mass-venv314/bin/python")
mut, base = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
thin = ["--thin"] if "--thin" in sys.argv else []
spec = {   # name: (E dir, pert dir or None, f64 from base, --only)
    "float_cast": ("float_cast_E", ("scaleP16", "float_cast_P16"), "BR,P1"),
    "noise_f64": ("noise_f64", None, "BR,SR,FM,TM,EVC,LL1,LL2,LL3"),
    "h_wrong": ("h_wrong", None, "A2"),
    "eta_dropped": (None, ("scaleP16", "eta_dropped"), "P1"),
}
for name, (edir, pert, only) in spec.items():
    need = ([f"{mut}/{edir}/bisect.json"] if edir else []) + ([f"{mut}/{pert[1]}/bisect.json"] if pert else [])
    if not all(os.path.exists(x) for x in need):
        print(f"{name:12s} not run yet", flush=True)
        continue
    view = f"{mut}/views/{name}"
    os.makedirs(view + "/runs/pert", exist_ok=True)
    for link, tgt in ((view + "/runs/E", f"{mut}/{edir}" if edir else f"{base}/runs/E"), (view + "/runs/f64", f"{base}/runs/f64")) + (((f"{view}/runs/pert/{pert[0]}", f"{mut}/{pert[1]}"),) if pert else ()):
        if os.path.islink(link):
            os.unlink(link)
        os.symlink(tgt, link)
    p = subprocess.run([PY, "extended_bisect.py", "analyze", f"--raw={view}", f"--only={only}"] + thin, cwd=NR, capture_output=True, text=True)
    open(f"{mut}/analyze_{name}.log", "w").write(p.stdout + p.stderr)
    fails = re.findall(r"^\[FAIL\] (\S+):", p.stdout, re.M)
    print(f"{name:12s} exit {p.returncode} only={only:18s} fires: {', '.join(fails) if fails else '-'}", flush=True)
