#!/bin/bash
# the planes (amendment A6): eps_Y, eps_Z of scipy's planes against the crate's at (3000, base), and the dose-response of eps_Y to the number of renormalizations at (1000, base)
cd /Users/nathan/Source/negative-mass-i196/phase2/nonradial || exit 1
RAW=/Users/nathan/Source/negative-mass-raw/I196-mac
PY=/Users/nathan/Source/negative-mass/.venv/bin/python
P="$PY taylor_drift.py planes --steps=$RAW/crate_star_steps.jsonl --jtable=$RAW/crate_jtable_l5.jsonl --rtol=1e-13 --atol=1e-14"
J=$RAW/jsonl
for pl in crate_j crate_j_cf025 crate_j_cf05 crate_j_cf2 crate_j_cf4 crate_j_cf8; do
  $P --out=$J/planes_CF.jsonl --gammas=1000 --variant=base --plant=$pl --extra-chunks=0,1,2,3
done
for e in 0,1,2,3; do
  $P --out=$J/planes_3000.jsonl --gammas=3000 --variant=base --plant=crate_j --extra-chunks=$e
done
$P --out=$J/planes_1000phi.jsonl --gammas=1000 --variant=phi --plant=crate_j --extra-chunks=0,1,2,3
