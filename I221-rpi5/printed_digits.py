#!/usr/bin/env python3
"""printed_digits.py [--mutate=bump:D] [--old-rev=REV]: do the printed numbers that read growth.csv's D <= 11 rows change? (#221)

Run from anywhere; reads the checkout ~/Source/negative-mass-i221 (Paper III's main.tex, notes/wormhole_largeD/README.md, growth.csv)
and REV's growth.csv by git (default 4bced01). Exit 1 unless every cell is unchanged (old rounding = new rounding = printed)."""
import csv
import os
import re
import subprocess
import sys
from decimal import Decimal

import mpmath as mp

REPO = os.path.expanduser("~/Source/negative-mass-i221")
ND = os.path.join(REPO, "notes", "wormhole_largeD")
TEX = os.path.join(REPO, "paper", "3-wormhole-largeD", "main.tex")
README = os.path.join(ND, "README.md")
mp.mp.dps = 50
OM0 = -4 * mp.log(2)
OM1 = 2 * mp.pi**2 / 3 + 8 * mp.log(2)**2


def read_rows(text):
    return {int(r[0]): r[1] for r in list(csv.reader(text.splitlines()))[1:]}


def three_term(D, W):
    s = mp.mpf(2 * (D - 3))
    f3 = s + OM0 + OM1 / s
    return abs(W - f3) / W, (W - f3) * s * s


def e_fold(W):
    return 1 / mp.sqrt(W), 1 / (mp.sqrt(2) * mp.sqrt(W))


def dec_of(x_str):
    """(Decimal value, number of decimals) of a printed plain number"""
    return Decimal(x_str), len(x_str.split(".")[1]) if "." in x_str else 0


def at_decimals(x, nd):
    return Decimal(mp.nstr(x, 40)).quantize(Decimal(1).scaleb(-nd))


def at_sig(x, n):
    return Decimal(f"{float(x):.{n - 1}e}")


def parse_sci(cell):
    """printed '$5.9\\times10^{-2}$' or '$0.28$' or '$2.2$' -> (Decimal value, significant digits)"""
    c = cell.strip().strip("$")
    m = re.fullmatch(r"([\d.]+)\\times10\^\{(-?\d+)\}", c)
    mant, ex = (m.group(1), int(m.group(2))) if m else (c, 0)
    nsig = len(mant.replace(".", "").lstrip("0"))
    return Decimal(mant).scaleb(ex), nsig


def main(argv):
    mut, rev = None, "4bced01"
    for a in argv:
        if a.startswith("--mutate="):
            mut = a.split("=", 1)[1]
        elif a.startswith("--rev="):
            rev = a.split("=", 1)[1]
    old = read_rows(subprocess.run(["git", "-C", ND, "show", f"{rev}:notes/wormhole_largeD/growth.csv"], capture_output=True,
                                   text=True, check=True).stdout)
    new = read_rows(open(os.path.join(ND, "growth.csv")).read())
    if mut:
        name, _, arg = mut.partition(":")
        if name != "bump":
            raise SystemExit(f"unknown mutation {mut}")
        new[int(arg)] = str(mp.mpf(new[int(arg)]) + mp.mpf("1e-6"))
    W = {"old": {D: mp.mpf(v) for D, v in old.items()}, "new": {D: mp.mpf(v) for D, v in new.items()}}
    cells = []          # (where, D, quantity, printed string, old rounded, new rounded)

    def add(where, D, q, printed, fn):
        cells.append((where, D, q, printed, fn("old"), fn("new")))

    tex = open(TEX).read().splitlines()
    start1 = next(i for i, l in enumerate(tex) if "\\label{tab:W}" in l)
    start2 = next(i for i, l in enumerate(tex) if "\\label{tab:life}" in l)
    for i in range(start1, len(tex)):
        if "\\bottomrule" in tex[i]:
            break
        m = re.match(r"^(\d+) & (\S+)(?: \(\S+\))? & (.+?) & (.+?) \\\\\s*$", tex[i])
        if m and int(m.group(1)) <= 11:
            D = int(m.group(1))
            w, nd = dec_of(m.group(2))
            add(f"main.tex:{i + 1}", D, "W2a2", m.group(2), lambda k, D=D, nd=nd: at_decimals(W[k][D], nd))
            v3, n3 = parse_sci(m.group(3))
            add(f"main.tex:{i + 1}", D, "rel. diff", m.group(3), lambda k, D=D, n3=n3: at_sig(three_term(D, W[k][D])[0], n3))
            v4, nd4 = dec_of(m.group(4).strip("$"))
            add(f"main.tex:{i + 1}", D, "diff x s^2", m.group(4), lambda k, D=D, nd4=nd4: at_decimals(three_term(D, W[k][D])[1], nd4))
    for i in range(start2, len(tex)):
        if "\\bottomrule" in tex[i]:
            break
        m = re.match(r"^(\d+) & (\d\.\d+) & (\d\.\d+) &", tex[i])
        if m:
            D = int(m.group(1))
            add(f"main.tex:{i + 1}", D, "1/(Wa)", m.group(2), lambda k, D=D: at_decimals(e_fold(W[k][D])[0], 3))
            add(f"main.tex:{i + 1}", D, "slope 1/(sqrt2 W a)", m.group(3), lambda k, D=D: at_decimals(e_fold(W[k][D])[1], 3))
    rd = open(README).read().splitlines()
    for i, l in enumerate(rd):
        m = re.match(r"^\| (\d+) \| ([\d.]+) \| ([\d.]+) \|", l)
        if m and int(m.group(1)) in (4, 10):
            D = int(m.group(1))
            _, nd = dec_of(m.group(3))
            add(f"README.md:{i + 1}", D, "[TS13] column", m.group(3), lambda k, D=D, nd=nd: at_decimals(W[k][D], nd))
        for m in re.finditer(r"([0-9]\.[0-9]{3}) a \(D = (\d+)\)|([0-9]\.[0-9]{3}) a at D = (\d+)\b|At D = 4 it is the ([0-9]\.[0-9]{3}) a", l):
            g = [x for x in m.groups() if x is not None]
            D = int(g[1]) if len(g) == 2 else 4
            if D > 11:                      # the D >= 20 rows are not changed by #221
                continue
            add(f"README.md:{i + 1}", D, "1/W", g[0], lambda k, D=D: at_decimals(e_fold(W[k][D])[0], 3))
    print(f"printed_digits.py  mutate={mut}  old-rev={rev}")
    print(f"  {'where':<14s} {'D':>3s}  {'quantity':<20s} {'printed':<26s} {'old @ digits':<16s} {'new @ digits':<16s} verdict")
    bad = []
    for where, D, q, printed, o, n in cells:
        pv = Decimal(printed.strip("$")) if "times" not in printed else parse_sci(printed)[0]
        pv = Decimal(printed.strip("$").split("\\pm")[0]) if "times" not in printed else pv
        verdict = "unchanged" if (o == n == pv) else ("printed != old" if o != pv else "NEW DIFFERS")
        if verdict != "unchanged":
            bad.append((where, D, q, verdict))
        print(f"  {where:<14s} {D:>3d}  {q:<20s} {printed:<26s} {str(o):<16s} {str(n):<16s} {verdict}")
    print(f"\n{len(cells)} cells, {len(cells) - len(bad)} unchanged; not unchanged: {[(w, D, q, v) for w, D, q, v in bad] or 'none'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
