#!/usr/bin/env python3
"""s3_records.py OLD NEW [--mutate=NAME] [--complex] [--out=DIR]: the crate's JSON records from two binaries, compared as strings.

Written before the first stage 3 run (README amendment A4, criterion RP2). The same commands, with the same arguments, are run
with each binary (the star's pc and zc come from OLD's `star` and are passed to both, so the star record is the only place the
star solve is compared); every field of every record is compared as a string except the wall times (TIMEKEYS of taylor_polar.py).
`--mutate=NAME` passes mutate=NAME to NEW only: the control (the comparison must report differences).
`--complex` adds the commands of the complex build (`dc`, `cp1`).

Commands (each at nice 10, one process):
  star; d at l = 2, 6 (f64, dd, qd as taylor_polar.py's R1) and an od record; planted const and linear (f64, dd, qd);
  starsteps; jtable l = 2 and l = 6 (the coefficients of every entry, J0 and J1, at every step: table.rs's arithmetic);
  recipcheck (f64, dd, qd, od); tabcheck at four radii; jjets l = 2 at r = 2.
Exit 0: no record differs. Exit 1: some record differs (each is listed with the fields). Exit 2: usage.
"""
import json
import os
import subprocess
import sys
import time

HERE = "/Users/nathan/Source/negative-mass-i192/phase2/nonradial"
sys.path.insert(0, HERE)
import taylor_polar as tp  # noqa: E402  (module-level code only defines; main() is guarded)

TIMEKEYS = {"t_y", "t_q", "t_s", "wall", "t_star", "t_table", "seconds"}
R1_D = [("f64", 2, [0.001, 1.0, 40.0]), ("dd", 2, [0.001, 1.0, 40.0]), ("qd", 2, [0.001, 1.0]),
        ("f64", 6, [0.001, 1.0, 40.0]), ("dd", 6, [0.001, 1.0, 40.0]), ("qd", 6, [0.001, 1.0])]


def run(binpath, cmd, mutate=None, **kw):
    args = [binpath, cmd] + [f"{k}={v}" for k, v in kw.items()]
    if mutate:
        args.append(f"mutate={mutate}")
    env = dict(os.environ, RAYON_NUM_THREADS="2", TP_MAX_SECONDS="3000")
    p = subprocess.run(["nice", "-n", "10"] + args, capture_output=True, text=True, env=env, cwd=HERE)
    if p.returncode:
        raise RuntimeError(f"{' '.join(args)[:200]} exited {p.returncode}: {p.stderr[-400:]}")
    return [json.loads(x) for x in p.stdout.splitlines() if x.startswith("{")]


def commands(star, cplx):
    """(label, cmd, kwargs): the same list for both binaries"""
    out = []
    for lane, l, gs in R1_D:
        out.append((f"d {lane} l={l}", "d", dict(lane=lane, l=l, gammas=",".join(repr(g) for g in gs), **star)))
    out.append(("d od l=2", "d", dict(lane="od", l=2, gammas="1.0", **star)))
    for case in ("const", "linear"):
        for lane in ("f64", "dd", "qd"):
            out.append((f"planted {case} {lane}", "planted", dict(case=case, lane=lane, gamma=10.0, L=1.0, Lz=1.0)))
    out.append(("starsteps", "starsteps", dict(star)))
    for l in (2, 6):
        out.append((f"jtable l={l}", "jtable", dict(l=l, **star)))
    for lane in ("f64", "dd", "qd", "od"):
        out.append((f"recipcheck {lane}", "recipcheck", dict(lane=lane)))
    out.append(("tabcheck l=2", "tabcheck", dict(l=2, r="0.001,0.1,1,5", s=1.0, **star)))
    out.append(("jjets l=2", "jjets", dict(l=2, r=2.0, s=1.0, **star)))
    if cplx:
        for lane, l, gs in R1_D:
            out.append((f"dc {lane} l={l}", "dc", dict(lane=lane, l=l, re=",".join(repr(g) for g in gs), im=",".join("0.0" for _ in gs), **star)))
        for lane in ("f64", "dd", "qd"):
            out.append((f"cp1 {lane}", "cp1", dict(lane=lane, cx=1, x=12.0, f="7.0,-3.0,5.0,-11.0")))
    return out


def strip(rec):
    return {k: v for k, v in rec.items() if k not in TIMEKEYS}


def main(argv):
    mutate, cplx, out = None, False, None
    args = []
    for a in argv[1:]:
        if a.startswith("--mutate="):
            mutate = a.split("=", 1)[1]
        elif a == "--complex":
            cplx = True
        elif a.startswith("--out="):
            out = a.split("=", 1)[1]
        else:
            args.append(a)
    if len(args) != 2:
        print(__doc__)
        return 2
    old, new = args
    s = run(old, "star", **tp.MODEL)[0]
    star = dict(tp.MODEL, pc=s["pc"], zc=s["zc"])
    total = bad = 0
    for label, cmd, kw in commands(star, cplx):
        t = time.time()
        ro = run(old, cmd, **kw)
        rn = run(new, cmd, mutate=mutate, **kw)
        diffs = []
        if len(ro) != len(rn):
            diffs.append(f"{len(ro)} records against {len(rn)}")
        for i, (a, b) in enumerate(zip(ro, rn)):
            a, b = strip(a), strip(b)
            if json.dumps(a, sort_keys=True) != json.dumps(b, sort_keys=True):
                keys = sorted(k for k in set(a) | set(b) if json.dumps(a.get(k), sort_keys=True) != json.dumps(b.get(k), sort_keys=True))
                ex = keys[0] if keys else "?"
                diffs.append(f"record {i}: fields {keys[:8]}; {ex}: {str(a.get(ex))[:60]} against {str(b.get(ex))[:60]}")
        if out:
            os.makedirs(out, exist_ok=True)
            tag = label.replace(" ", "_").replace("=", "")
            open(os.path.join(out, f"old_{tag}.jsonl"), "w").write("\n".join(json.dumps(r) for r in ro) + "\n")
            open(os.path.join(out, f"new_{tag}.jsonl"), "w").write("\n".join(json.dumps(r) for r in rn) + "\n")
        total += len(ro)
        bad += sum(1 for d in diffs if d.startswith("record"))
        print(f"{label}: {len(ro)} records, " + ("equal" if not diffs else f"{len(diffs)} DIFFER") + f" ({time.time() - t:.0f} s)", flush=True)
        for d in diffs:
            print("   " + d, flush=True)
    print(f"SUMMARY: {total} records, {bad} differ; old {old}, new {new}, mutate = {mutate}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
