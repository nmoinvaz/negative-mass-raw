#!/usr/bin/env python3
"""summarize.py RUN_NAME...: one markdown row per run from its files in the raw folder (.log header, .rc, .time, cmp_<run>_vs_baseline.txt)."""
import os, re, sys

RAW = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def rd(n):
    p = os.path.join(RAW, n)
    return open(p).read() if os.path.exists(p) else ""


print("| run | exit | checks | controls | gated differences (lines, eta*, class, kind) | error-sized numbers differing as printed | wall (s) | max RSS (MB) | load at start |")
print("|---|---|---|---|---|---|---|---|---|")
for name in sys.argv[1:]:
    log, rc, tm = rd(name + ".log"), rd(name + ".rc").strip(), rd(name + ".time")
    hdr = log.split("\n")[0]
    load = re.search(r"load\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)", hdr)
    ck = re.search(r"^checks: (\d+) passed, (\d+) failed", log, re.M)
    fired = len(re.findall(r"^\[FIRED\]", log, re.M))
    silent = len(re.findall(r"^\[SILENT|^\[NOT FIRED|^\[MISSED", log, re.M))
    ctl = re.search(r"^controls: (.*)$", log, re.M)
    wall = re.search(r"([\d.]+)\s+real", tm)
    rss = re.search(r"(\d+)\s+maximum resident set size", tm)
    cmp_ = rd("cmp_%s_vs_baseline.txt" % "_".join(name.split("_")[:2]))
    g = re.search(r"gated differences: (\d+)", cmp_)
    d = re.search(r"eta\* differing in the 10 printed digits: (\d+), largest relative difference of any eta\* ([\d.e+-]+)", cmp_)
    ed = re.search(r"(\d+) error-sized numbers on aligned lines, (\d+) differ", cmp_)
    gate = "-"
    if g:
        gate = f"{g.group(1)} in the log"
        if d:
            gate += f"; {d.group(1)} of 537 eta* differ, largest relative difference {d.group(2)}"
    print("| {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
        name, rc,
        f"{ck.group(1)} passed, {ck.group(2)} failed" if ck else "-",
        (f"{fired} fired; " if fired else "") + (ctl.group(1) if ctl else "-"),
        gate,
        f"{ed.group(2)} of {ed.group(1)}" if ed else "-",
        f"{float(wall.group(1)):.0f}" if wall else "-",
        f"{int(rss.group(1)) / 1048576:.0f}" if rss else "-",
        " ".join(load.groups()) if load else "-"))
