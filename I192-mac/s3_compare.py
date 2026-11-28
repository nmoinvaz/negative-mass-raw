#!/usr/bin/env python3
"""s3_compare.py A.log B.log [--show=N]: two logs of `taylor_polar.py` (any mode) compared token by token as strings.

Written before the first stage 3 run (README amendment A4). What is not compared, and nothing else:
  * lines that start with `#` (start time, load average, command, md5 of the binary),
  * wall times: a number directly followed by `s`, or by ` s` (`12s`, `(12s)`, `22 s`, `3.3 s`), replaced by <T>,
  * the load average after the words `load average`.
Every other token of every other line is compared as a string, so a printed digit that moved is a mismatch. Lines are
paired in order; a different count of lines is a mismatch. Every mismatch is printed with its line number, the token
position and both lines (up to --show of them, default all), so no difference is hidden by the summary.

Exit 0: every token equal. Exit 1: any mismatch. Exit 2: usage.
"""
import re
import sys


NORMALIZED = [0]   # how many tokens the two rules replaced, printed in the summary


def norm(line):
    line, n1 = re.subn(r"load average\s+[\d.]+", "load average <L>", line)
    line, n2 = re.subn(r"(?<![\w.])\d+(\.\d+)?(e[-+]?\d+)?\s?s(?![\w])", "<T>", line)
    NORMALIZED[0] += n1 + n2
    return line


def data_lines(path):
    out = []
    for n, line in enumerate(open(path, errors="replace"), 1):
        line = line.rstrip("\n")
        if not line.strip() or line.startswith("#"):
            continue
        out.append((n, line))
    return out


def main(argv):
    show = None
    args = []
    for a in argv[1:]:
        if a.startswith("--show="):
            show = int(a.split("=", 1)[1])
        else:
            args.append(a)
    if len(args) != 2:
        print(__doc__)
        return 2
    a, b = data_lines(args[0]), data_lines(args[1])
    ntok = nbad = nlines_bad = 0
    printed = 0
    if len(a) != len(b):
        print(f"MISMATCH: {len(a)} data lines in {args[0]} against {len(b)} in {args[1]}")
        nbad += 1
    for (na, x), (nb, y) in zip(a, b):
        tx, ty = norm(x).split(), norm(y).split()
        if len(tx) != len(ty):
            nbad += 1
            nlines_bad += 1
            if show is None or printed < show:
                printed += 1
                print(f"MISMATCH lines {na}/{nb}: {len(tx)} tokens against {len(ty)}\n  A: {x[:300]}\n  B: {y[:300]}")
            continue
        bad_here = False
        for j, (p, q) in enumerate(zip(tx, ty)):
            ntok += 1
            if p != q:
                nbad += 1
                bad_here = True
                if show is None or printed < show:
                    printed += 1
                    print(f"MISMATCH lines {na}/{nb} token {j + 1}: {p!r} against {q!r}\n  A: {x[:300]}\n  B: {y[:300]}")
        nlines_bad += bad_here
    print(f"{ntok} tokens of {min(len(a), len(b))} data lines compared as strings: {nbad} mismatches on {nlines_bad} lines "
          f"({NORMALIZED[0]} time and load tokens replaced in the two logs)")
    return 1 if nbad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
