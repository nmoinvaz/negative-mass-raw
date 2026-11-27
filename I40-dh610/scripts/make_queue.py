#!/usr/bin/env python3
"""Writes ../runs/queue.txt: the jobs of record, longest first, G6 first, a barrier before the D = 6 jobs (they start only after G6 exits 0).
G at D = 6 runs at its two coarsest h only (cost of the third: about 4 h, over the 2 h stop; accepted by the coordinator)."""
import os, sys
sys.path.insert(0, os.path.expanduser("~/Source/negative-mass-i40/notes/wormhole_evolution"))
import threshold as th

raw = os.path.expanduser("~/Source/negative-mass-raw/I40-dh610")
jobs = []
for n in (2, 3, 4):
    for fam in ("S", "O", "G"):
        hs = th.CRIT["H"][n]
        if fam == "G" and n == 4:
            hs = hs[:2]
        for k, h in enumerate(hs):
            N = th.CRIT["X"][fam][n] / h
            jobs.append((n + 2, fam, h, N * N, "--cons --stall" + (" --ed" if k == 1 else "")))
a = sorted([j for j in jobs if j[0] < 6], key=lambda j: -j[3])
b = sorted([j for j in jobs if j[0] == 6], key=lambda j: -j[3])
lines = ["G6"] + [f"JOB {D} {fam} {h!r} {fl}" for D, fam, h, _, fl in a] + ["BARRIER g6"] + [f"JOB {D} {fam} {h!r} {fl}" for D, fam, h, _, fl in b]
os.makedirs(f"{raw}/runs", exist_ok=True)
open(f"{raw}/runs/queue.txt", "w").write("\n".join(lines) + "\n")
print(len(a) + len(b), "jobs;", len(lines), "queue lines")
