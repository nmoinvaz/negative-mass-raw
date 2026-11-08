"""Compares the rows of a convergence.py rerun with the first run's, in a job log that holds both.

    python compare_conv_rows.py conv_085_l2      first run against the last run in conv_085_l2.log
    python compare_conv_rows.py --selftest       the comparison on a copy (must pass) and on a mutated copy (must fail)

A run starts at a line "=== <time> <job>". Its rows are the "r_m=" lines of the variants and the "gamma=" lines, with
np.float64(...) unwrapped and the trailing "(<n>s)" timing removed, so rows are compared digit for digit. The rerun
may stop early (a crash), so only the rows it printed are compared, and the rows the first run printed beyond them are
counted separately.
"""
import os
import re
import sys

RAW = os.path.dirname(os.path.abspath(__file__))


def runs(text):
    out, cur = [], None
    for line in text.splitlines():
        if line.startswith("=== "):
            cur = []
            out.append(cur)
        elif cur is not None and (line.startswith("gamma=") or re.search(r": r_m=", line)):
            line = re.sub(r"np\.float64\(([^)]*)\)", r"\1", line)
            cur.append(re.sub(r"\s+\(\d+s\)\s*$", "", line.rstrip()))
    return out


def compare(first, last):
    """(rows compared, rows that differ as (index, first, last), rows only the first run has)"""
    n = min(len(first), len(last))
    diff = [(i, first[i], last[i]) for i in range(n) if first[i] != last[i]]
    return n, diff, len(first) - n


def selftest():
    first = ["base : r_m=27.94", "gamma=   0.001: D_base=-3.544223e-02  signs=[-1.0]  rel.spread=1.5e-04", "gamma=   0.03: D_base=-3.444056e-02"]
    print("copy   ->", compare(first, list(first)))
    mutated = list(first)
    mutated[2] = mutated[2].replace("3.444056e-02", "3.444057e-02")
    print("mutate ->", compare(first, mutated))


def main():
    if "--selftest" in sys.argv:
        selftest()
        return
    job = sys.argv[1]
    rs = runs(open(os.path.join(RAW, job + ".log"), encoding="utf-8", errors="replace").read())
    if len(rs) < 2:
        print(f"{job}.log holds {len(rs)} run(s), nothing to compare")
        return
    n, diff, extra = compare(rs[0], rs[-1])
    print(f"{job}: {len(rs)} runs in the log; first run {len(rs[0])} rows, last run {len(rs[-1])} rows")
    print(f"compared {n} rows: {'all identical' if not diff else str(len(diff)) + ' differ'}; "
          f"{extra} rows only in the first run")
    for i, a, b in diff:
        print(f"  row {i}\n    first: {a}\n    last : {b}")
    sys.exit(1 if diff else 0)


if __name__ == "__main__":
    main()
