#!/bin/bash
# P0 at rtol 1e-12 from the second slot (resumable: run_A.sh finds finished cases done)
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
S="/Users/nathan/Source/negative-mass/.venv/bin/python taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl"
$S --out=$RAW/jsonl/scipy_P0.jsonl --rtols=1e-12 --gammas=3000,2000,1000 --variants=base,phi --plants=sci
