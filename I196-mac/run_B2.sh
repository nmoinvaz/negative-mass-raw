#!/bin/bash
# process B after N1 (amendment A2): the planted noise at the measured amplitude (NOISEROW), the declared per-entry noise (NOISE), P1, then the extras with X_ATOL first
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
S="$PY taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl"
J=$RAW/jsonl
$S --out=$J/scipy_N0.jsonl --rtols=1e-10 --extra-chunks=1 --gammas=1000,2000,3000 --variants=base,phi --plants=sci
$S --out=$J/scipy_N1.jsonl --rtols=1e-10 --extra-chunks=1 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
$S --out=$J/scipy_NOISEROW.jsonl --rtols=1e-10 --gammas=1000 --variants=base --plants=sci --noise-row=1.0 --noise-seeds=1,2,3
$S --out=$J/scipy_NOISEROW.jsonl --rtols=1e-10 --gammas=1000 --variants=base --plants=sci --noise-row=0.1 --noise-seeds=1,2
$S --out=$J/scipy_NOISEROW.jsonl --rtols=1e-10 --gammas=3000 --variants=base --plants=sci --noise-row=1.0 --noise-seeds=1,2
$S --out=$J/scipy_NOISE.jsonl --rtols=1e-10 --gammas=1000 --variants=base --plants=sci --noise-ulp=1.0 --noise-seeds=1,2,3
$S --out=$J/scipy_NOISE.jsonl --rtols=1e-10 --gammas=1000 --variants=base --plants=sci --noise-ulp=0.1 --noise-seeds=1,2
$S --out=$J/scipy_NOISE.jsonl --rtols=1e-10 --gammas=3000 --variants=base --plants=sci --noise-ulp=1.0 --noise-seeds=1,2
for r in 1e-10 1e-13; do
  $S --out=$J/scipy_P1.jsonl --rtols=$r --gammas=1000,2000,3000 --variants=base,phi --plants=crate
done
# extras: X_ATOL first (A2), then X_N0R13, X_P2, X_P1R at rtol 1e-12
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=1000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=3000 --variants=base --plants=sci
$S --out=$J/scipy_X_N0R13.jsonl --rtols=1e-13 --extra-chunks=1 --gammas=1000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_N0R13.jsonl --rtols=1e-13 --extra-chunks=1 --gammas=3000 --variants=base --plants=sci
$S --out=$J/scipy_X_P2.jsonl --rtols=1e-10 --gammas=1000,3000 --variants=base,phi --plants=sci_vac
$S --out=$J/scipy_X_P1R.jsonl --rtols=1e-12 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
