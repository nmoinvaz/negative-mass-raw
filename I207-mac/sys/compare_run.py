#!/usr/bin/env python3
"""compare_run.py BASE_LOG RUN_LOG [BASE_DUMP RUN_DUMP]

The comparator of #190 (compare_outputs.py, imported unchanged: same normalization, same gate) plus what it does not gate.
Gated (exit 1 when any): every difference compare_outputs.py reports. Listed, not gated: the error-sized numbers (exponent
<= -6) and the step counts of the log lines that differ between the two runs, and the records of the dump whose step count
differs. One naming difference is removed before the dump comparison: a dump file whose first line holds the command line of
the binary with an absolute path (`ntable --file /<root>/notes/warp/...`) is named by a hash of it, so it has another name
in another checkout; each file of RUN_DUMP that BASE_DUMP lacks is paired with the BASE_DUMP file whose first line equals its
own after the absolute prefix before `notes/warp/` is replaced, and compared under the base's name."""
import importlib.util, os, re, shutil, sys, tempfile

here = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("compare_outputs", os.path.join(here, "compare_outputs.py"))
co = importlib.util.module_from_spec(spec)
spec.loader.exec_module(co)

ERR = re.compile(r"[-+]?\d+\.?\d*[eE]-(?:0[6-9]|[1-9]\d)\b")
STEPS = re.compile(r"\d+(?: (?:and|to) \d+)? steps")


def raw_lines(path):
    out = []
    for l in open(path):
        if l.startswith("#") or l.startswith("\t") or l.startswith("Command being") or not l.strip():
            continue
        if re.match(r"\s*\(series through eta\^-\d+ solved in \d+ s\)", l):
            continue
        out.append(l.rstrip())
    return out


def listing(a, b):
    la, lb = raw_lines(a), raw_lines(b)
    n = nd = 0
    worst = []
    steps_differ = 0
    for i, (x, y) in enumerate(zip(la, lb)):
        ex, ey = ERR.findall(x), ERR.findall(y)
        if len(ex) == len(ey):
            for u, v in zip(ex, ey):
                n += 1
                if u != v:
                    nd += 1
                    fu, fv = float(u), float(v)
                    worst.append((abs(fu - fv) / max(abs(fu), abs(fv), 1e-300), i, u, v, x[:90]))
        if STEPS.findall(x) != STEPS.findall(y):
            steps_differ += 1
    worst.sort(reverse=True)
    print(f"listed, not gated: {n} error-sized numbers on aligned lines, {nd} differ as printed; "
          f"{steps_differ} lines whose step counts differ")
    if worst:
        fac = [w[0] for w in worst]
        print(f"  relative differences of the differing ones: max {fac[0]:.2e}, median {fac[len(fac) // 2]:.2e}; "
              f"{sum(f > 1 for f in fac)} differ by more than a factor 2 (rel > 1), {sum(f > 0.1 for f in fac)} by more than 10%")
        for w in worst[:5]:
            print(f"  line {w[1]}: {w[2]} -> {w[3]}   {w[4]}")


def pair_dump(base, run, tmp):
    shutil.copytree(run, tmp, dirs_exist_ok=True)
    norm = lambda l: re.sub(r"/\S*?/(?=notes/warp/)", "<root>/", l.rstrip())  # noqa: E731
    first = {}
    for f in os.listdir(base):
        first.setdefault(norm(open(os.path.join(base, f)).readline()), []).append(f)
    pairs = []
    for f in sorted(os.listdir(tmp)):
        if os.path.exists(os.path.join(base, f)):
            continue
        cand = [g for g in first.get(norm(open(os.path.join(tmp, f)).readline()), []) if not os.path.exists(os.path.join(tmp, g))]
        if len(cand) == 1:
            os.rename(os.path.join(tmp, f), os.path.join(tmp, cand[0]))
            pairs.append((f, cand[0]))
    return pairs


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    n, d = co.gated_log(a, b)
    print(f"log lines compared: {n}; gated differences: {len(d)}")
    for x in d[:40]:
        print(x)
    bad = len(d)
    listing(a, b)
    if len(sys.argv) > 4:
        tmp = tempfile.mkdtemp(prefix="cmp_dump_")
        pairs = pair_dump(sys.argv[3], sys.argv[4], tmp)
        for f, g in pairs:
            print(f"dump file {f} paired with {g} (first lines equal up to the absolute path)")
        st, dd = co.gated_dump(sys.argv[3], tmp)
        print(f"dump: {st['files']} files, {st['records']} records, {st['str']} string fields, {st['dig']} eta* values compared; "
              f"files missing in the run: {st['missing']}; eta* differing in the 10 printed digits: {len([x for x in dd if 'xstar' in x])}, "
              f"largest relative difference of any eta* {st['maxrel']:.2e}; records whose step count differs (listed, not gated): {st['steps_differ']}")
        for x in dd[:40]:
            print(x)
        bad += len(dd) + st["missing"]
        shutil.rmtree(tmp, ignore_errors=True)
    print("RESULT:", "gated differences found" if bad else "no gated difference")
    sys.exit(1 if bad else 0)
