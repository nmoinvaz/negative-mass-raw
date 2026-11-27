#!/usr/bin/env python3
"""Writes runs/queue.txt: one line `name|args` per job of record, longest first (the lanes take the first line left). D = 5 hk 0, 1, 2 = h 0.00707, 0.00354, 0.00177; D = 4 hk 0, 1 = h 0.02, 0.01."""
import os
RAW = os.path.expanduser("~/Source/negative-mass-raw/I255-dh610")
R = RAW + "/runs"
jobs = []
def bs(D, B, hk):
    jobs.append((f"bs_D{D}_B{B:g}_hk{hk}", f"bisect_stall --D={D} --B={B:g} --hk={hk} --out={R}"))
def st(D, B, hk):
    jobs.append((f"st_D{D}_B{B:g}_hk{hk}", f"stall --D={D} --B={B:g} --hk={hk} --delta=1e-10 --out={R}/stall"))
bs(5, 0.04, 2); bs(5, 0.2, 2)
jobs.append(("expand_hk1", f"expand --hk=1 --X=160 --out={R}/expand"))
bs(5, 0.04, 1); bs(5, 0.2, 1)
st(5, 0.1, 2); st(5, 0.1, 1)
bs(5, 0.04, 0); bs(5, 0.2, 0); st(5, 0.1, 0)
jobs.append(("expand_hk0", f"expand --hk=0 --X=160 --out={R}/expand"))
jobs.append(("ctl_D5_hk0", f"ctl --D=5 --hk=0 --out={R}/ctl"))
for B in (0.04, 0.2):
    for hk in (0, 1):
        bs(4, B, hk)
for hk in (0, 1):
    st(4, 0.1, hk)
os.makedirs(R + "/logs", exist_ok=True)
open(R + "/queue.txt", "w").write("".join(f"{n}|{a}\n" for n, a in jobs))
print(len(jobs), "jobs")
