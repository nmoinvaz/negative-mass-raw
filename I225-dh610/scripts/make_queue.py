#!/usr/bin/env python3
"""Writes runs/queue.txt: one job per line, 'name|arguments of throat_locus.py', longest first. Lines are taken by lane.sh (flock) and removed."""
import os
import sys

sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i225/notes/wormhole_evolution"))
import threshold   # noqa: E402

RAW = os.path.expanduser("~/Source/negative-mass-raw/I225-dh610")
H = threshold.CRIT["H"]
Q = []


def hs(D, hk):
    return f"{H[D - 2][hk]:g}"


# series of G: parts of one job go to the same folder (points_<i>of<m>.jsonl)
for D, hk, parts in ((5, 2, 4), (5, 1, 2), (4, 2, 1), (5, 0, 1), (4, 1, 1), (4, 0, 1)):
    out = f"{RAW}/runs/series/D{D}_G_h{hs(D, hk)}"
    for i in range(parts):
        Q.append((f"series_D{D}_hk{hk}_p{i}of{parts}", f"series --D={D} --hk={hk} --part={i}/{parts} --out={out}"))
# the expanding branch on the locus (rectangle X as #213's): G members, and S (A = 0.05, D = 4, h = 0.02) as the control XC
X = {4: 200, 5: 100}
for D, members in ((5, ("tuned", "0.05")), (4, ("tuned", "0.05", "0.2"))):
    for hk in (1, 0):
        for m in members:
            Q.append((f"expand_G_D{D}_{m}_hk{hk}", f"expand --D={D} --hk={hk} --member={m} --X={X[D]} --family=G --out={RAW}/runs/expand"))
Q.append(("expand_S_D4_0.05_hk0", f"expand --D=4 --hk=0 --member=0.05 --X=200 --family=S --out={RAW}/runs/expand"))
# the member at the stall
for D in (5, 4):
    for hk in (2, 1, 0):
        Q.append((f"stall_D{D}_hk{hk}", f"stall --D={D} --hk={hk} --out={RAW}/runs/stall"))
# planted lifetime series
for D, hk, v in ((5, 0, 0.13), (4, 0, 0.5), (4, 0, 0.1), (4, 0, 0.0)):
    Q.append((f"planted_D{D}_hk{hk}_v{v:g}", f"planted --D={D} --hk={hk} --v={v} --out={RAW}/runs/planted"))
os.makedirs(f"{RAW}/runs/logs", exist_ok=True)
open(f"{RAW}/runs/queue.txt", "w").write("".join(f"{n}|{a}\n" for n, a in Q))
print(f"{len(Q)} jobs")
