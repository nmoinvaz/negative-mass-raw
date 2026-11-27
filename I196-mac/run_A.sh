#!/bin/bash
# process A of the runs of record: P0 (scipy's star, 4 rtol), then the extras X_ATOL, X_P3, X_P1R (rtol 1e-11)
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
S="/Users/nathan/Source/negative-mass/.venv/bin/python taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl"
J=$RAW/jsonl
for r in 1e-10 1e-13 1e-11 1e-12; do
  $S --out=$J/scipy_P0.jsonl --rtols=$r --gammas=1000,2000,3000 --variants=base,phi --plants=sci
done
# extras (reported whatever they show)
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=1000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=3000 --variants=base --plants=sci
$S --out=$J/scipy_X_P3.jsonl --rtols=1e-10 --gammas=3000 --variants=base --plants=int_crate,ext_crate
$S --out=$J/scipy_X_P1R.jsonl --rtols=1e-11 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
