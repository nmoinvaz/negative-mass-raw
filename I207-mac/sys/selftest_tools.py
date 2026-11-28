#!/usr/bin/env python3
"""selftest_tools.py [--mutate=NAME]

The checks of this folder's own tools must be able to fail. On copies of a baseline log and dump (I190's `ctl` run), each case
changes one thing and states what `classify_diff.py` and `compare_eta.py` must do; the exit codes and the kinds are asserted.
Cases (name: change -> expected):
  same:       an unchanged copy -> classify exits 0 with no differing line; compare_eta exits 0 with 0 above the bar
  zero:       one `<err>`-sized number printed as 0.0e+00 in a copy of a line that has one -> kind (i), exit 0
  fit:        a fitted exponent in the line `measured exponent ...` changed -> kind (iii), exit 0
  label:      a class label changed (`F->0` to `a3->0`) -> kind (ii), exit 1
  eta_print:  the 10th printed digit of an eta* in a label line changed -> kind (ii), exit 1
  eta_dump:   one `xstar` of the dump moved by 5e-11 max(1, eta*) -> compare_eta exit 0 at 1e-10, exit 1 at 1e-12
  eta_big:    one `xstar` of the dump moved by 1e-9 max(1, eta*) -> compare_eta exit 1 at 1e-10
  class_dump: one class of the dump changed -> that record is skipped by compare_eta and counted (it is C3's, not C4's)
`--mutate=NAME` runs only that case and prints what it did. Exit 0 if every case behaves as stated."""
import json, os, re, shutil, subprocess, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.expanduser("~/Source/negative-mass-raw/I190-rpi5")
LOG = os.path.join(BASE, "run_06_base_offgrid_ctl.log")
DUMP = os.path.join(BASE, "dump_base_ctl")


def run(*a):
    r = subprocess.run([sys.executable, *a], capture_output=True, text=True)
    return r.returncode, r.stdout


def edit_log(tmp, fn):
    out = os.path.join(tmp, f"log_{len(os.listdir(tmp))}.txt")
    lines = open(LOG).read().split("\n")
    lines = fn(lines)
    open(out, "w").write("\n".join(lines))
    return out


def sub_first(lines, pat, rep, count=1):
    for i, l in enumerate(lines):
        if re.search(pat, l):
            lines[i] = re.sub(pat, rep, l, count=count)
            return lines
    raise SystemExit(f"selftest: no line matches {pat!r}")


def edit_dump(tmp, fn):
    d = tempfile.mkdtemp(prefix="dump_", dir=tmp)
    os.rmdir(d)
    shutil.copytree(DUMP, d)
    fn(d)
    return d


def bump_eta(rel):
    def f(d):
        for name in sorted(os.listdir(d)):
            if not name.startswith("offgrid_"):
                continue
            p = os.path.join(d, name)
            lines = open(p).read().split("\n")
            for i, l in enumerate(lines):
                if l.startswith("{"):
                    o = json.loads(l)
                    if isinstance(o.get("xstar"), float):
                        o["xstar"] += rel * max(1.0, abs(o["xstar"]))
                        lines[i] = json.dumps(o)
                        open(p, "w").write("\n".join(lines))
                        return
        raise SystemExit("selftest: no xstar in the dump")
    return f


def change_class(d):
    for name in sorted(os.listdir(d)):
        if not name.startswith("offgrid_"):
            continue
        p = os.path.join(d, name)
        lines = open(p).read().split("\n")
        for i, l in enumerate(lines):
            if l.startswith("{") and '"class": "SINGULAR"' in l:
                lines[i] = l.replace('"class": "SINGULAR"', '"class": "FLOOR"', 1)
                open(p, "w").write("\n".join(lines))
                return
    raise SystemExit("selftest: no SINGULAR record")


def main():
    only = next((a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--mutate=")), None)
    tmp = tempfile.mkdtemp(prefix="selftest_tools_")
    cl = os.path.join(here, "classify_diff.py")
    ce = os.path.join(here, "compare_eta.py")
    ok = True

    def case(name, got, want):
        nonlocal ok
        if only and only != name:
            return
        good = got == want
        ok &= good
        print(f"{'ok  ' if good else 'FAIL'} {name}: got {got}, want {want}")

    def kinds(out):
        m = re.search(r"\(i\) zero-token (\d+); \(iii\) fitted exponent (\d+); \(ii\) other (\d+)", out)
        return tuple(int(x) for x in m.groups())

    rc, out = run(cl, LOG, LOG)
    case("same", (rc, kinds(out)), (0, (0, 0, 0)))
    rc, out = run(ce, DUMP, DUMP, "1e-12")
    case("same_eta", (rc, "above 1e-12: 0;" in out), (0, True))

    def zero(lines):
        return sub_first(lines, r"worst error \d\.\d+e-\d+", "worst error 0.0e+00")
    rc, out = run(cl, LOG, edit_log(tmp, zero))
    case("zero", (rc, kinds(out)), (0, (1, 0, 0)))

    def fit(lines):
        return sub_first(lines, r"(measured exponent against 2/\(eta\*\^2 \+ 4\): worst relative difference )\S+", r"\g<1>1.1e-09")
    rc, out = run(cl, LOG, edit_log(tmp, fit))
    case("fit", (rc, kinds(out)), (0, (0, 1, 0)))

    def label(lines):
        return sub_first(lines, r"first pass S:a3->0", "first pass S:F->0")
    rc, out = run(cl, LOG, edit_log(tmp, label))
    case("label", (rc, kinds(out)), (1, (0, 0, 1)))

    def etap(lines):
        return sub_first(lines, r"record S:F->0 at (\d+\.\d{8})\d", lambda m: m.group(0)[:-1] + ("1" if m.group(0)[-1] != "1" else "2"))
    rc, out = run(cl, LOG, edit_log(tmp, etap))
    case("eta_print", (rc, kinds(out)), (1, (0, 0, 1)))

    rc, out = run(ce, DUMP, edit_dump(tmp, bump_eta(5e-11)), "1e-10")
    case("eta_dump_loose", rc, 0)
    rc, out = run(ce, DUMP, edit_dump(tmp, bump_eta(5e-11)), "1e-12")
    case("eta_dump_tight", rc, 1)
    rc, out = run(ce, DUMP, edit_dump(tmp, bump_eta(1e-9)), "1e-10")
    case("eta_big", rc, 1)
    rc, out = run(ce, DUMP, edit_dump(tmp, change_class), "1e-10")
    case("class_dump", (rc, bool(re.search(r"records skipped because class, kind, outcome or stop differs: 1;", out))), (0, True))
    shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT:", "every case as stated" if ok else "a case did not behave as stated")
    sys.exit(0 if ok else 1)


main()
