#!/usr/bin/env python3
"""summarize_i207.py > results_table.md

One table from the logs of the runs of record: exit code, wall time (s), max RSS (MB), checks passed and failed with the names of
the failed ones, controls fired, and against the declared baseline: the comparator's raw count of gated log lines, the kinds of
`classify_diff.py` (zero-token, fitted exponent, other), the records of another class or kind in the dump and the largest eta*
difference (C4's measure, records that keep class and kind), from the `cmp_`, `classify_` and `eta_` files `analyze.sh` wrote."""
import os, re, sys

RAW = os.path.expanduser("~/Source/negative-mass-raw/I207-mac")
RUNS = [
    ("run_06_on_ctl", "on", "`ctl`, 16 checks", "I190 `run_06_base_offgrid_ctl`"),
    ("run_07_on_stage_a", "on", "full grid, stage a (15 checks)", "I183 `run_04a`"),
    ("run_08_on_stage_b", "on", "full grid, stage b (`dd_qd`)", "I183 `run_03b`"),
    ("run_09_off_stage_a", "off", "full grid, stage a", "I183 `run_04a`"),
    ("run_10_off_stage_b", "off", "full grid, stage b", "I183 `run_03b`"),
    ("run_11_off_global", "off", "`conical_global.py`", "I190 `run_11_base_global`"),
    ("run_12_on_global", "on", "`conical_global.py`", "I190 `run_11_base_global`"),
    ("run_13_off_loglog", "off", "`conical_loglog.py`", "I190 `run_09_base_loglog`"),
    ("run_14_on_loglog", "on", "`conical_loglog.py`", "I190 `run_09_base_loglog`"),
    ("run_15_off_ctl", "off", "`ctl`, 16 checks", "I190 `run_06_base_offgrid_ctl`"),
    ("run_16_early_ctl", "early", "`ctl`, 16 checks", "I190 `run_06_base_offgrid_ctl`"),
    ("run_17_late_ctl", "late", "`ctl`, 16 checks", "I190 `run_06_base_offgrid_ctl`"),
    ("run_18_ungated_ctl", "ungated", "`ctl`, 16 checks", "I190 `run_06_base_offgrid_ctl`"),
    ("run_19_on_controls", "on", "`--controls-only locator-side,plant-locator,n-drift,recip-dd`", "I183 `ctl_run_03`"),
]

def rd(p):
    try:
        return open(os.path.join(RAW, p), errors="replace").read()
    except OSError:
        return ""

print("| run | arm | what | rc | wall s | RSS MB | checks | failed | controls | gated log lines (raw) | (i) / (iii) / (ii) | dump records of another class or kind | largest eta* difference | against |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for name, arm, what, base in RUNS:
    log, tm = rd(name + ".log"), rd(name + ".time")
    rc = rd(name + ".rc").strip() or "-"
    wall = re.search(r"([\d.]+)\s+real", tm)
    rss = re.search(r"(\d+)\s+maximum resident", tm)
    m = re.search(r"checks: (\d+) passed, (\d+) failed (\[[^\]]*\])", log)
    chk = f"{m.group(1)} of {int(m.group(1)) + int(m.group(2))}" if m else "-"
    fail = m.group(3) if m else "-"
    nf = len(re.findall(r"^\[FIRED\]", log, re.M))
    ctl = ("all fired on target only" if "controls: all fired on target only" in log else ("%d fired" % nf if nf else "-"))
    cmp_ = rd("cmp_" + name + ".txt")
    g = re.search(r"gated differences: (\d+)", cmp_)
    cl = rd("classify_" + name + ".txt")
    k = re.search(r"\(i\) zero-token (\d+); \(iii\) fitted exponent (\d+); \(ii\) other (\d+)", cl)
    eta = rd("eta_" + name + ".txt")
    sk = re.search(r"records skipped because class, kind, outcome or stop differs: (\d+)", eta)
    lg = re.search(r"largest \|difference\| / max\(1, eta\*\): ([\d.e+-]+)", eta)
    print(f"| {name} | {arm} | {what} | {rc} | {float(wall.group(1)):.0f} | {int(rss.group(1)) // 1048576} | {chk} | {fail} | {ctl} | "
          f"{g.group(1) if g else '-'} | {'%s / %s / %s' % k.groups() if k else '-'} | {sk.group(1) if sk else '-'} | {lg.group(1) if lg else '-'} | {base} |"
          if wall and rss else f"| {name} | {arm} | {what} | {rc} | - | - | {chk} | {fail} | {ctl} | - | - | - | - | {base} |")
