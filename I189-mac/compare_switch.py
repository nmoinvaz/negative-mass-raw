#!/usr/bin/env python3
"""compare_switch.py A.log B.log [--only-data]: the crate switch's criterion X3, as the README of this folder words it.

The data lines of two `taylor_polar.py` logs (the five variant header lines `<name>: r_m=...`, the rows `gamma=...`, the CHECK lines
and the SUMMARY line) are split into tokens and compared as strings, after the wall times are replaced (`(12s)` of a row, the
`; 22 s` of a SUMMARY, the `star 0.0 s, J table 3.3 s` of the setup line). A line of one log with no partner (a different count of data
lines) is a mismatch. The # lines (start time, load, md5 of the binary, command) are not compared.

Exit 0 when every token is equal, 1 when any differs (each is printed with its line and tokens), 2 on a usage error.
"""
import re
import sys


def data_lines(path):
    out = []
    for line in open(path):
        line = line.rstrip("\n")
        if line.startswith("#") or not line.strip():
            continue
        if line.startswith(("gamma=", "CHECK ", "SUMMARY")) or re.search(r": r_m=", line):
            line = re.sub(r"\(\d+s\)", "(Ns)", line)
            line = re.sub(r"; \d+ s$", "; N s", line)
            line = re.sub(r"star [\d.]+ s, J table [\d.]+ s", "star X s, J table Y s", line)
            out.append(line)
    return out


def main(argv):
    if len(argv) != 3:
        print(__doc__)
        return 2
    a, b = data_lines(argv[1]), data_lines(argv[2])
    ntok = nbad = 0
    by_kind = {"row": [0, 0], "check": [0, 0]}   # [tokens, mismatches] of the rows and header lines, and of the CHECK and SUMMARY lines
    if len(a) != len(b):
        print(f"MISMATCH: {len(a)} data lines in {argv[1]} against {len(b)} in {argv[2]}")
        nbad += 1
    for i, (x, y) in enumerate(zip(a, b)):
        tx, ty = x.split(), y.split()
        if len(tx) != len(ty):
            print(f"MISMATCH line {i + 1}: {len(tx)} tokens against {len(ty)}\n  A: {x[:200]}\n  B: {y[:200]}")
            nbad += 1
            continue
        kind = by_kind["check" if x.startswith(("CHECK ", "SUMMARY")) else "row"]
        for j, (p, q) in enumerate(zip(tx, ty)):
            ntok += 1
            kind[0] += 1
            if p != q:
                nbad += 1
                kind[1] += 1
                print(f"MISMATCH line {i + 1} token {j + 1}: {p!r} against {q!r}  (A: {x[:90]}...)")
    print(f"{ntok} tokens of {min(len(a), len(b))} data lines compared as strings: {nbad} mismatches "
          f"(rows and headers: {by_kind['row'][1]} of {by_kind['row'][0]}; CHECK and SUMMARY lines: {by_kind['check'][1]} of {by_kind['check'][0]})")
    return 1 if nbad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
