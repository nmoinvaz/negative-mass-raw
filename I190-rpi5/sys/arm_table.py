#!/usr/bin/env python3
"""arm_table.py: the feature-switch runs of record as a markdown table (from the logs, no typed numbers)"""
import re, os
R = os.path.expanduser("~/Source/negative-mass-raw/I190-rpi5")
jobs = [
    ("conical_global.py (checks and controls)", "base", "run_11_base_global"), ("conical_global.py (checks and controls)", "on", "run_32_on_global"),
    ("conical_loglog.py (checks and controls)", "base", "run_09_base_loglog"), ("conical_loglog.py (checks and controls)", "on", "run_30_on_loglog"),
    ("conical_offgrid.py --grid=ctl --no-controls", "base", "run_06_base_offgrid_ctl"), ("conical_offgrid.py --grid=ctl --no-controls", "off", "run_35_off_offgrid_ctl"),
    ("conical_offgrid.py --grid=ctl --no-controls", "on", "run_31_on_offgrid_ctl"), ("conical_offgrid.py --grid=ctl --no-controls", "on (rebased head)", "run_42_on_offgrid_ctl_r2"),
    ("conical_offgrid.py --grid=ctl --controls-only n-drift,recip-dd", "base", "run_33_base_offgrid_ctrl"), ("conical_offgrid.py --grid=ctl --controls-only n-drift,recip-dd", "on", "run_34_on_offgrid_ctrl"),
]
def elapsed(t):
    p = t.split(":")
    s = 0.0
    for x in p: s = s * 60 + float(x)
    return s
print("| script | arm | exit | checks | controls | wall (s) | max rss (MB) | load at start |")
print("|---|---|---|---|---|---|---|---|")
for script, arm, name in jobs:
    lg = os.path.join(R, name + ".log")
    if not os.path.exists(os.path.join(R, name + ".rc")):
        print(f"| {script} | {arm} | not finished | | | | | |"); continue
    t = open(lg).read()
    rc = open(os.path.join(R, name + ".rc")).read().strip()
    ck = re.findall(r"^checks: (\d+) passed, (\d+) failed", t, re.M)
    cc = re.findall(r"^controls: (.*)", t, re.M)
    el = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): (\S+)", t)
    rs = re.search(r"Maximum resident set size \(kbytes\): (\d+)", t)
    ld = re.search(r"load ([0-9. ]+) threads", t)
    print(f"| {script} | {arm} | {rc} | {(ck[0][0] + " passed, " + ck[0][1] + " failed") if ck else "-"} | {cc[0] if cc else '-'} | {elapsed(el.group(1)):.0f} | {int(rs.group(1))/1024:.0f} | {ld.group(1).strip() if ld else ''} |")
