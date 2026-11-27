#!/bin/bash
# process B after amendment A3: the exact-J system (crate star, M_ext and J tables): CJE ensembles, CJN planted noise; then P1 at rtol 1e-10; then the extras
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
S="$PY taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl --jtable=$RAW/crate_jtable_l5.jsonl"
J=$RAW/jsonl
E=0,1,2,3,4,5,6,7
for st in "1e-10 1e-14" "1e-13 1e-14" "1e-13 1e-17"; do
  set -- $st
  $S --out=$J/scipy_CJE.jsonl --plants=crate_j --gammas=1000 --variants=base --rtols=$1 --atol=$2 --extra-chunks=$E
  $S --out=$J/scipy_CJE.jsonl --plants=crate_j --gammas=1000 --variants=phi --rtols=$1 --atol=$2 --extra-chunks=$E
  $S --out=$J/scipy_CJE.jsonl --plants=crate_j --gammas=3000 --variants=base --rtols=$1 --atol=$2 --extra-chunks=$E
done
for u in 1.0 10.0 100.0; do
  $S --out=$J/scipy_CJN.jsonl --plants=crate_j --gammas=1000 --variants=base --rtols=1e-10 --noise-ulp=$u --noise-seeds=1,2,3,4 --max-seconds=900
done
for u in 0.01 0.1; do
  $S --out=$J/scipy_CJN.jsonl --plants=crate_j --gammas=1000 --variants=base --rtols=1e-10 --noise-row=$u --noise-seeds=1,2,3,4 --max-seconds=900
done
$S --out=$J/scipy_P1.jsonl --rtols=1e-10 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
# extras
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=1000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_ATOL.jsonl --rtols=1e-13 --atol=1e-17 --gammas=3000 --variants=base --plants=sci
$S --out=$J/scipy_X_P1_13.jsonl --rtols=1e-13 --gammas=1000,2000,3000 --variants=base,phi --plants=crate
$S --out=$J/scipy_X_N0R13.jsonl --rtols=1e-13 --extra-chunks=1 --gammas=1000 --variants=base,phi --plants=sci
$S --out=$J/scipy_X_N0R13.jsonl --rtols=1e-13 --extra-chunks=1 --gammas=3000 --variants=base --plants=sci
$S --out=$J/scipy_X_P2.jsonl --rtols=1e-10 --gammas=1000,3000 --variants=base,phi --plants=sci_vac
$S --out=$J/scipy_X_P3.jsonl --rtols=1e-10 --gammas=3000 --variants=base --plants=int_crate,ext_crate
