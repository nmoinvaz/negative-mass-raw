#!/usr/bin/env python3
"""compare_selftest.py: the comparator (compare_outputs.py, unchanged from I190-rpi5/sys, sha256 341f60b7...) can fail.

Each mutation breaks a copy of #190's baseline once, on purpose, and the comparator is run against the unbroken baseline.
Expected: the identity passes, every mutation of an eta*, a class, a kind or a line count makes it exit 1, and a change
inside what the comparator ignores by its documented rules (an error-sized number, an eta* beyond its 10th printed
digit) is silent. Usage: compare_selftest.py I190_RAW_DIR WORK_DIR   Exits 1 if any expectation is not met."""
import json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CMP = os.path.join(HERE, "compare_outputs.py")
RAW190, WORK = sys.argv[1], sys.argv[2]
os.makedirs(WORK, exist_ok=True)


def run(*args):
    r = subprocess.run([sys.executable, CMP, *args], capture_output=True, text=True)
    return r.returncode, r.stdout


def mut_log(src, dst, fn):
    lines = open(src).read().split("\n")
    out = fn(lines)
    open(dst, "w").write("\n".join(out))


def first(lines, pat):
    for i, l in enumerate(lines):
        if re.search(pat, l):
            return i
    raise SystemExit(f"selftest: no line matches {pat}")


def bump_eta(lines):  # the last printed digit of the first eta* of a scan line
    i = first(lines, r"F->0@\d+\.\d+")
    m = re.search(r"F->0@(\d+\.\d+)", lines[i])
    s = m.group(1)
    t = s[:-1] + str((int(s[-1]) + 1) % 10)
    lines[i] = lines[i][: m.start(1)] + t + lines[i][m.end(1):]
    return lines


def flip_class(lines):
    i = first(lines, r"F->0@")
    lines[i] = lines[i].replace("F->0@", "F->inf@", 1)
    return lines


def drop_line(lines):
    del lines[first(lines, r"^\[PASS\] plant_linear")]
    return lines


def err_digit(lines):  # an error-sized number: ignored by the comparator's rules, held to its check's bar
    i = first(lines, r"worst \|dN\|/sum\|terms\| 2\.08e-32")
    lines[i] = lines[i].replace("2.08e-32", "2.09e-32", 1)
    return lines


results = []


def expect(name, code, want, out):
    ok = (code == want)
    results.append(ok)
    print(f"[{'ok' if ok else 'FAILED'}] {name}: exit {code}, expected {want}" + ("" if ok else "\n" + out[:600]))


base = os.path.join(RAW190, "run_11_base_global.log")
copy = os.path.join(WORK, "copy.log")
shutil.copy(base, copy)
c, o = run(base, copy)
expect("log identity", c, 0, o)
for name, fn, want in (("log: eta* last printed digit", bump_eta, 1), ("log: class label", flip_class, 1),
                        ("log: a line removed", drop_line, 1), ("log: error-sized number (silent by rule)", err_digit, 0)):
    p = os.path.join(WORK, "mut.log")
    mut_log(base, p, fn)
    c, o = run(base, p)
    expect(name, c, want, o)

# dump records
dsrc = os.path.join(RAW190, "dump_base_ctl")
fname = sorted(f for f in os.listdir(dsrc) if f.startswith("offgrid_"))[0]
dcopy = os.path.join(WORK, "dump")
shutil.rmtree(dcopy, ignore_errors=True)
shutil.copytree(dsrc, dcopy)
lg = os.path.join(RAW190, "run_06_base_offgrid_ctl.log")
c, o = run(lg, lg, dsrc, dcopy)
expect("dump identity", c, 0, o)


def edit_dump(fn):
    shutil.rmtree(dcopy, ignore_errors=True)
    shutil.copytree(dsrc, dcopy)
    p = os.path.join(dcopy, fname)
    ls = open(p).read().split("\n")
    i = next(k for k, l in enumerate(ls) if l.startswith("{") and '"xstar": ' in l and '"SINGULAR"' in l)
    r = json.loads(ls[i])
    fn(r)
    ls[i] = json.dumps(r)
    open(p, "w").write("\n".join(ls))


def setx(f):
    def g(r):
        r["xstar"] = r["xstar"] * (1 + f)
    return g


for name, fn, want in (("dump: eta* changed at its 10th digit (1e-9)", setx(1e-9), 1),
                        ("dump: eta* changed beyond 10 digits (1e-13), silent by rule", setx(1e-13), 0),
                        ("dump: kind", lambda r: r.__setitem__("kind", "F->inf"), 1),
                        ("dump: class", lambda r: r.__setitem__("class", "REGULAR"), 1),
                        ("dump: steps (listed, not gated)", lambda r: r.__setitem__("steps", r["steps"] + 1), 0)):
    edit_dump(fn)
    c, o = run(lg, lg, dsrc, dcopy)
    expect(name, c, want, o)

print(f"selftest: {sum(results)} of {len(results)} as expected")
sys.exit(0 if all(results) else 1)
