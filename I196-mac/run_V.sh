#!/bin/bash
# CJV (amendment A4): the exact-J system with the exterior scalar plane in vacuum, rtol 1e-13, 8 realizations per cell
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
S="$PY taylor_drift.py scipy --steps=$RAW/crate_star_steps.jsonl --jtable=$RAW/crate_jtable_l5.jsonl"
J=$RAW/jsonl
E=0,1,2,3,4,5,6,7
$S --out=$J/scipy_CJV.jsonl --plants=crate_j_vac --gammas=3000 --variants=base --rtols=1e-13 --extra-chunks=$E
$S --out=$J/scipy_CJV.jsonl --plants=crate_j_vac --gammas=1000 --variants=base --rtols=1e-13 --extra-chunks=$E
$S --out=$J/scipy_CJV.jsonl --plants=crate_j_vac --gammas=1000 --variants=phi --rtols=1e-13 --extra-chunks=$E
