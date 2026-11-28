#!/usr/bin/env python3
"""Run `extended_bisect.py analyze` or `controls` under each mutation and list the checks that fire (FAIL) and the clean run's failures.
python3 mut_table.py analyze RAWVIEW [--thin] NAME ...      or      python3 mut_table.py controls NAME ...   (run with the venv python, from anywhere)"""
import os, re, subprocess, sys
NR = os.path.expanduser("~/Source/negative-mass-i227/notes/wormhole_evolution")
PY = os.path.expanduser("~/Source/negative-mass-venv314/bin/python")
mode = sys.argv[1]
args = sys.argv[2:]
raw = None
thin = []
if mode == "analyze":
    raw, args = args[0], args[1:]
    if args and args[0] == "--thin":
        thin, args = ["--thin"], args[1:]


def run(name):
    cmd = [PY, "extended_bisect.py", mode] + (["--raw=" + raw] if raw else []) + thin + (["--mutate=" + name] if name else [])
    if mode == "controls" and name in ONLY:
        cmd += ["--only=" + ONLY[name]]
    p = subprocess.run(cmd, cwd=NR, capture_output=True, text=True)
    fails = re.findall(r"^\[FAIL\] (\S+):", p.stdout, re.M)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mut", f"{mode}_{name or 'clean'}.log"), "w").write(p.stdout + p.stderr)
    return fails, p.returncode


ONLY = {"diag_S": "K1", "taylor_order": "K2", "ellis_charge": "K3", "quad_h": "K4", "float_cast": "PL", "pert_sign": "PL", "floor_off": "PL"}
os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "mut"), exist_ok=True)
for name in [None] + args:
    f, rc = run(name)
    print(f"{name or 'clean':16s} exit {rc}  fires: {', '.join(f) if f else '-'}", flush=True)
