#!/usr/bin/env python3
"""relabel_readers.py OLD NEW: the two readers of w2_output.txt's growth.csv table that key on its source label, run on the
file as committed (OLD) and on a copy whose D = 4 ... 11 labels read `w2_crate qd (#195)` (NEW), as a rerun of w2_highprec.py would print
once growth.csv carries that label (#221). Regexes copied verbatim from notes/black_universe/stability.py:54 and
notes/wormhole_largeD/order4.py:808."""
import re
import sys

def stability(path):
    for line in open(path):
        m = re.match(r"\s+4\s+TS13 Table I\s+\S+\s+(\S+)", line)
        if m:
            return m.group(1)
    return None

def order4(path):
    n = 0
    for line in open(path):
        if re.match(r"\s*(\d+)\s+(?:modes_r\.py|TS13 Table I)\s+(\S+)\s+(\S+)\s", line):
            n += 1
    return n

for tag, p in (("OLD", sys.argv[1]), ("NEW", sys.argv[2])):
    print(f"{tag}: stability.py planted_value -> {stability(p)!r} (None: it raises RuntimeError); order4.py read_w2 matches {order4(p)} table rows")
