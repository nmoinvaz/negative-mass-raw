#!/usr/bin/env python3
"""s3_steps.py A B [--mutate=NAME] [--out=DIR]: J's table step lists of two binaries, as `jtable` prints them.

Written before the first stage 3 run (README amendment A4, criteria JT2 and JT5). A is #186's own table (the default build),
B the table of multishoot (feature lib_table). For each case the `jtable` records are parsed (x0, x1 as Rust's shortest
round-trip strings: equal strings are equal bits; c0 and c1 as 20-digit strings) and compared:
  * the head record: l, nb, steps, pattern and linear_defect, as strings (steps may differ: reported as such),
  * the number of steps,
  * the breakpoints: every x0 and x1 of the shared index range, the number bitwise equal, the largest relative difference
    |x_B - x_A| / x_A, and whether every one is within 1e-9 relative (the bar of the library's C3),
  * the coefficients of the steps whose x0 and x1 are both bitwise equal, as strings: how many steps are equal.
The cases: l = 2, 3, 4, 5, 6 over [5e-4, 34.7] (`jtable`'s defaults) and l = 2 over [1.5e-3, 24.6] (the r0 = 3e-3 variants' table range).
`--mutate=NAME` passes mutate=NAME to B only (the control: the comparison must fail).
Exit 0: every case has the same step count and every breakpoint within 1e-9. Exit 1 otherwise. Exit 2: usage.
"""
import json
import os
import subprocess
import sys

HERE = "/Users/nathan/Source/negative-mass-i192/phase2/nonradial"
sys.path.insert(0, HERE)
import taylor_polar as tp  # noqa: E402

CASES = [(l, 5e-4, 34.7) for l in (2, 3, 4, 5, 6)] + [(2, 1.5e-3, 24.6)]
BAR = 1e-9


def run(binpath, mutate=None, **kw):
    args = [binpath, "jtable"] + [f"{k}={v}" for k, v in kw.items()]
    if mutate:
        args.append(f"mutate={mutate}")
    env = dict(os.environ, RAYON_NUM_THREADS="2")
    p = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True, env=env, cwd=HERE)
    if p.returncode:
        raise RuntimeError(f"{' '.join(args)[:200]} exited {p.returncode}: {p.stderr[-400:]}")
    recs = [json.loads(x) for x in p.stdout.splitlines() if x.startswith("{")]
    return recs[0], recs[1:]


def main(argv):
    mutate, out = None, None
    args = []
    for a in argv[1:]:
        if a.startswith("--mutate="):
            mutate = a.split("=", 1)[1]
        elif a.startswith("--out="):
            out = a.split("=", 1)[1]
        else:
            args.append(a)
    if len(args) != 2:
        print(__doc__)
        return 2
    a_bin, b_bin = args
    p = subprocess.run(["nice", "-n", "10", a_bin, "star"] + [f"{k}={v}" for k, v in tp.MODEL.items()], capture_output=True, text=True, cwd=HERE)
    st = json.loads([x for x in p.stdout.splitlines() if x.startswith("{")][0])
    star = dict(tp.MODEL, pc=st["pc"], zc=st["zc"])
    ok_all = True
    for l, rmin, rmax in CASES:
        ha, ra = run(a_bin, l=l, rmin=rmin, rmax=rmax, **star)
        hb, rb = run(b_bin, mutate=mutate, l=l, rmin=rmin, rmax=rmax, **star)
        n = min(len(ra), len(rb))
        eq_x = rel_max = 0
        within = True
        for p_, q_ in zip(ra, rb):
            for k in ("x0", "x1"):
                if p_[k] == q_[k]:
                    eq_x += 1
                else:
                    r = abs(q_[k] - p_[k]) / abs(p_[k])
                    rel_max = max(rel_max, r)
                    within &= r <= BAR
        same_series = sum(1 for p_, q_ in zip(ra, rb) if p_["x0"] == q_["x0"] and p_["x1"] == q_["x1"] and p_["c0"] == q_["c0"] and p_["c1"] == q_["c1"])
        same_bp = sum(1 for p_, q_ in zip(ra, rb) if p_["x0"] == q_["x0"] and p_["x1"] == q_["x1"])
        head = {k: (ha[k], hb[k]) for k in ("l", "nb", "pattern", "linear_defect") if ha[k] != hb[k]}
        ok = len(ra) == len(rb) and within and not (set(head) - {"linear_defect"})
        ok_all &= ok
        print(f"l = {l} [{rmin}, {rmax}]: steps {len(ra)} against {len(rb)}; breakpoints bitwise equal {eq_x} of {2 * n}, largest relative difference {rel_max:.2e}, "
              f"all within {BAR:g}: {within}; steps with equal x0, x1: {same_bp} of {n}; with equal coefficient strings too: {same_series}; head fields differing: {head if head else 'none'}"
              f" -> {'ok' if ok else 'FAIL'}", flush=True)
        if out:
            os.makedirs(out, exist_ok=True)
            open(os.path.join(out, f"steps_l{l}_{rmin:g}_{rmax:g}.json"), "w").write(json.dumps({"A": [r["x0"] for r in ra] + [ra[-1]["x1"]], "B": [r["x0"] for r in rb] + [rb[-1]["x1"]]}))
    print(f"SUMMARY: {'every case equal in count and within ' + str(BAR) if ok_all else 'some case differs'}; A {a_bin}, B {b_bin}, mutate = {mutate}")
    return 0 if ok_all else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
