"""The 18 re-solved sectors of #119 in one table: the window and its label before (report-old-i118-i111.log, #111's and
#118's files at floor 0.07) and after (report-wide.log, this folder's files first), #75's own window, the real
eigenvalues in the windows, and k reached (eigenvalues returned) with the smallest |mu| v_c of each file. Reads the
two report logs and eig/*.npz beside this file. Run with the venv python, -X utf8, from any directory."""
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SECTORS = [(2.0, m + 0.5) for m in range(11)] + [(4.0, m + 0.5) for m in range(4, 11)]


def read(name):
    out, sig = {}, None
    for ln in open(os.path.join(HERE, name), encoding="utf-8"):
        h = re.match(r"== sigma R = (\d+)", ln)
        if h:
            sig = float(h.group(1))
        if sig is None or not re.match(r"^\s+\d+\.?\d* \| \d+ / \d+ \|", ln):
            continue
        f = [x.strip() for x in ln.split("|")]
        win = re.match(r"([\d.]+) / ([\d.]+) \(([\d.]+)\)", f[7])
        out[(sig, float(f[0]))] = dict(w5=float(win.group(1)), w4=float(win.group(2)), own=float(win.group(3)),
                                       by=f[8], real=f[10], src=f[-1])
    return out


def main():
    old, new = read("report-old-i118-i111.log"), read("report-wide.log")
    vc = {}
    print("| σR | m | window 10⁻⁵ before | set by | window 10⁻⁵ after | set by | #75's own | real, A / B | k, A / B | "
          "smallest \\|μ\\|v_c, A / B | n, A / B |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    bad = 0
    for sig, m in SECTORS:
        o, n = old[(sig, m)], new[(sig, m)]
        info = []
        for d in "AB":
            z = np.load(os.path.join(HERE, "eig", f"s{sig:g}_{d}_m{int(2 * m)}.npz"))
            vc[sig] = float(z["vc"])
            info.append((len(z["mu"]), float(np.abs(z["mu"][-1]) * z["vc"]), int(z["n"])))
        if not n["src"].startswith("I119-win"):
            bad += 1
        fr = "{}/{}"
        print(f"| {sig:g} | {m:g} | {o['w5']:.4f} | {o['by']} | {n['w5']:.4f} | {n['by']} | {o['own']:.4f} | {n['real']} | "
              f"{info[0][0]} / {info[1][0]} | {info[0][1]:.4f} / {info[1][1]:.4f} | {info[0][2]}/{info[1][2]} |")
    print(f"\nsectors read from a directory other than I119-win: {bad}")
    sys.exit(1 if bad else 0)


main()
