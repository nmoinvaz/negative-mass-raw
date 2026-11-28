#!/usr/bin/env python3
"""compare_eta.py BASE_DUMP RUN_DUMP [TOL]

C3 of the README: every eta* (`xstar`, at any depth of a record) of RUN_DUMP within TOL max(1, eta*) of the baseline's
(TOL = 1e-12 by default: the tightest bar of #183, O8, the same point in two lanes). Pairs the dump files as `compare_run.py`
does (a file named by a hash of an absolute path). Records whose class or kind differs, or where one side has no eta*, are
not compared (they are C2's) and are counted. Exit 1 if any compared eta* is above TOL max(1, eta*). Prints the largest
differences with their file's command line, F_inf and C, and the counts above 1e-12, 1e-10 and 1e-8."""
import json, os, shutil, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import compare_run as cr  # noqa: E402  (imports compare_outputs.py unchanged)


def etas(o, path=()):
    """(path, value) of every numeric `xstar` in a record"""
    if isinstance(o, dict):
        for k, v in o.items():
            if k == "xstar" and isinstance(v, (int, float)):
                yield path + (k,), v
            else:
                yield from etas(v, path + (k,))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from etas(v, path + (i,))


def records(p):
    return [json.loads(l) for l in open(p) if l.startswith("{")]


def main():
    base, run = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 1e-12
    tmp = tempfile.mkdtemp(prefix="cmp_eta_")
    cr.pair_dump(base, run, tmp)
    n = 0
    skipped_class = 0
    one_sided = 0
    missing = 0
    worst = []
    for f in sorted(os.listdir(base)):
        if not os.path.exists(os.path.join(tmp, f)):
            missing += 1
            continue
        head = open(os.path.join(base, f)).readline().strip()[:110]
        ra, rb = records(os.path.join(base, f)), records(os.path.join(tmp, f))
        for i, (a, b) in enumerate(zip(ra, rb)):
            if not (isinstance(a, dict) and isinstance(b, dict)):
                continue
            if any(a.get(k) != b.get(k) for k in ("class", "kind", "outcome", "stop")):
                skipped_class += 1
                continue
            ea, eb = dict(etas(a)), dict(etas(b))
            if set(ea) != set(eb):
                one_sided += 1
                continue
            for p, va in ea.items():
                vb = eb[p]
                n += 1
                d = abs(va - vb) / max(1.0, abs(va))
                worst.append((d, f, i, ".".join(map(str, p)), va, vb, head, a.get("fi"), a.get("c")))
    shutil.rmtree(tmp, ignore_errors=True)
    worst.sort(key=lambda w: -w[0])
    over = lambda t: sum(w[0] > t for w in worst)  # noqa: E731
    print(f"eta* compared: {n} (files missing in the run: {missing}; records skipped because class, kind, outcome or stop differs: "
          f"{skipped_class}; records with an eta* on one side only: {one_sided})")
    print(f"largest |difference| / max(1, eta*): {worst[0][0] if worst else 0:.3e}")
    print(f"above 1e-12: {over(1e-12)}; above 1e-10: {over(1e-10)}; above 1e-8: {over(1e-8)}; above TOL = {tol:g}: {over(tol)}")
    for w in worst[:12]:
        if w[0] > 0:
            print(f"  {w[0]:.3e}  {w[1]} record {w[2]} {w[3]}: base {w[4]!r} run {w[5]!r}  (F_inf {w[7]}, C {w[8]})  [{w[6]}]")
    print("RESULT:", "above the bar" if over(tol) else "within the bar")
    sys.exit(1 if over(tol) else 0)


main()
