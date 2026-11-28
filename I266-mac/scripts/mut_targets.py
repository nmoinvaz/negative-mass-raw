#!/usr/bin/env python3
"""mut_targets.py DIR : the fired set of every mutation, from the last rerun of DIR/<name>[.N].log, as a MUTATIONS dict literal."""
import glob, os, re, sys
d = sys.argv[1]
last = {}
for f in glob.glob(os.path.join(d, "*.log")):
    b = os.path.basename(f)[:-4]
    m = re.match(r"^(.*?)(?:\.(\d+))?$", b)
    name, n = m.group(1), int(m.group(2) or 1)
    if name not in last or n > last[name][0]:
        last[name] = (n, f)
for name in sorted(last):
    txt = open(last[name][1]).read()
    m = re.findall(r"^mutation (\S+): fired (\[.*?\]), declared (\[.*?\]): (\w+)", txt, re.M)
    print(f'    "{name}": {eval(m[-1][1]) if m else "MISSING"},' + (f"   # log {os.path.basename(last[name][1])}" if m else f"   # log {os.path.basename(last[name][1])}: NO SUMMARY"))
