"""Compares win2's conv_085_l2 rows with the Mac's (negative-mass-raw I7-mac/conv_085_l2.log), at every gamma both printed.

    python compare_cross_machine.py <mac log>      each win2 run in conv_085_l2.log against the Mac's rows
    python compare_cross_machine.py --selftest      the comparison on a copy (must pass) and on a mutated copy (must fail)

Fields compared as printed text: D_base, the sign set, rel.spread, D(r_m~34), q_int, q_ext, and the r_m of each variant.
A run's rows are those after its "=== " header in conv_085_l2.log.
"""
import os
import re
import sys

RAW = os.path.dirname(os.path.abspath(__file__))
ROW = re.compile(r"gamma=\s*(\S+): D_base=(\S+)\s+signs=\[(.*?)\]\s+rel\.spread \(same r_m\)=(\S+)\s+D\(r_m~34\)=(\S+)\s+"
                 r"q_int=(\S+) q_ext=(\S+)")
RM = re.compile(r"^(.*?)\s*: r_m=(\S+)")


def parse(text):
    """{'rm': {variant: r_m}, 'rows': {gamma: (D_base, signs, spread, D34, q_int, q_ext)}} for one run's text"""
    text = re.sub(r"np\.float64\(([^)]*)\)", r"\1", text)
    out = {"rm": {}, "rows": {}}
    for line in text.splitlines():
        m = ROW.search(line)
        if m:
            out["rows"][m.group(1)] = m.groups()[1:]
            continue
        m = RM.match(line)
        if m and "gamma=" not in line:
            out["rm"][m.group(1)] = m.group(2)
    return out


def win2_runs(text):
    chunks = re.split(r"(?m)^=== .*$", text)[1:]
    return [parse(c) for c in chunks]


def compare(a, b):
    """(gammas compared, list of differences) between two parsed runs, over what both printed"""
    diffs = []
    for k in sorted(set(a["rm"]) & set(b["rm"])):
        if a["rm"][k] != b["rm"][k]:
            diffs.append(("r_m " + k, a["rm"][k], b["rm"][k]))
    common = [g for g in a["rows"] if g in b["rows"]]
    names = ("D_base", "signs", "rel.spread", "D(r_m~34)", "q_int", "q_ext")
    for g in common:
        for n, x, y in zip(names, a["rows"][g], b["rows"][g]):
            if x != y:
                diffs.append((f"gamma {g} {n}", x, y))
    return common, diffs


def selftest():
    row = "gamma=   0.3: D_base=-1.090323e-02  signs=[-1.0]  rel.spread (same r_m)=2.5e-04  D(r_m~34)=-5.287e-03  q_int=+3.142643e-01 q_ext=-3.113417e-01  (4s)"
    a = parse("base : r_m=27.94\n" + row)
    print("copy   ->", compare(a, parse("base : r_m=27.94\n" + row)))
    print("mutate ->", compare(a, parse("base : r_m=27.94\n" + row.replace("-1.090323e-02", "-1.090324e-02"))))


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    mac = parse(open(sys.argv[1], encoding="utf-8", errors="replace").read())
    print(f"Mac: r_m for {len(mac['rm'])} variants, rows at gamma {list(mac['rows'])}")
    runs = win2_runs(open(os.path.join(RAW, "conv_085_l2.log"), encoding="utf-8", errors="replace").read())
    bad = 0
    for i, r in enumerate(runs, 1):
        common, diffs = compare(r, mac)
        bad += len(diffs)
        print(f"win2 run {i}: printed gamma {list(r['rows'])}; compared {len(common)} gamma and {len(set(r['rm']) & set(mac['rm']))} "
              f"r_m; {'identical to the printed digits' if not diffs else str(len(diffs)) + ' differences'}")
        for d in diffs:
            print("   ", d)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
