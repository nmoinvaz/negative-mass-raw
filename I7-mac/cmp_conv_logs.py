#!/usr/bin/env python3
"""Compare the rows of two convergence.py logs digit for digit.

    python3 cmp_conv_logs.py REFERENCE.log OTHER.log [--selftest]

Rows are the variants' "r_m=" lines and the "gamma=" lines, with np.float64(...) unwrapped, CR and the trailing
"(<n>s)" timing removed. Exit 1 if the logs hold different numbers of rows or any row differs.
--selftest changes one digit of OTHER's last row and requires the check to fail on it.
"""
import re
import sys


def rows(path):
    out = []
    for line in open(path, encoding="utf-8", errors="replace").read().splitlines():
        if line.startswith("gamma=") or re.search(r": r_m=", line):
            line = re.sub(r"np\.float64\(([^)]*)\)", r"\1", line)
            out.append(re.sub(r"\s+\(\d+s\)\s*$", "", line.rstrip()))
    return out


def compare(ref, other):
    if len(ref) != len(other):
        return False, f"row counts differ: reference {len(ref)}, other {len(other)}"
    diff = [i for i in range(len(ref)) if ref[i] != other[i]]
    if diff:
        i = diff[0]
        return False, f"{len(diff)} of {len(ref)} rows differ, first at row {i}:\n  ref  : {ref[i]}\n  other: {other[i]}"
    return True, f"all {len(ref)} rows identical"


def bend(row):
    """Change the last mantissa digit of D_base (of the first number if the row has none)."""
    m = re.search(r"(?<=D_base=)-?[\d.]*?(\d)(?=e)", row)
    if m:
        return row[:m.start(1)] + str((int(m.group(1)) + 1) % 10) + row[m.end(1):]
    m = re.search(r"\d", row)
    d = str((int(m.group()) + 1) % 10)
    return row[:m.start()] + d + row[m.end():]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    ref, other = rows(args[0]), rows(args[1])
    if "--selftest" in sys.argv:
        bent = list(other)
        if bent:
            bent[-1] = bend(bent[-1])
        ok, msg = compare(ref, bent)
        print(f"selftest (one digit of the last row changed): {'FIRED' if not ok else 'DID NOT FIRE'}: {msg}")
        if ok:
            sys.exit(1)
    ok, msg = compare(ref, other)
    print(f"{'PASS' if ok else 'FAIL'}: {msg}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
