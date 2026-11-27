#!/bin/bash
# usage: run_polar.sh ELL MEMBER...   (runs of record: R1 then R2, results/polar_l<ELL>_<c>_<res>.json, logs/)
ell=$1; shift
cd ~/Source/negative-mass-i218/notes/black_universe
RAW=~/Source/negative-mass-raw/I218-dh610
for c in "$@"; do
  for r in R1 R2; do
    ~/Source/negative-mass-venv314/bin/python polar.py count $ell $c --res=$r --out=$RAW/results/polar_l${ell}_${c}_$r.json > $RAW/logs/polar_l${ell}_${c}_$r.log 2>&1
    echo "exit $? l=$ell c=$c $r"
  done
done
