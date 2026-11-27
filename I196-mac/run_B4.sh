#!/bin/bash
# process B after amendment A6: P1 at rtol 1e-10, then P0 at rtol 1e-12 (second slot), then the extras
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
S="$PY taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl --jtable=$RAW/crate_jtable_l5.jsonl"
J=$RAW/jsonl
$S --out=$J/scipy_P1.jsonl --rtols=1e-10 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
$S --out=$J/scipy_P0.jsonl --rtols=1e-12 --gammas=1000,2000,3000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=1000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_P1_13.jsonl --rtols=1e-13 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
