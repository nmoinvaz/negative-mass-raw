#!/bin/bash
# amendment A7 (time box): P0 at rtol 1e-11 for gamma = 1000 and 2000 only
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
S="/Users/nathan/Source/negative-mass/.venv/bin/python taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl"
$S --out=$RAW/jsonl/scipy_P0.jsonl --rtols=1e-11 --gammas=1000,2000 --variants=base,phi --plants=sci
