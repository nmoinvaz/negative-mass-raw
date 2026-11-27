#!/bin/bash
# usage: run_mads.sh RES   (runs of record: results/mads_<c>_<res>.json)
cd ~/Source/negative-mass-i218/notes/black_universe
RAW=~/Source/negative-mass-raw/I218-dh610
for c in 0.0001 0.001 0.01 0.03 0.1 0.2 0.5 1.0 2.0 3.0 5.0 10.0; do
  ~/Source/negative-mass-venv314/bin/python polar.py mads $c --res=$1 --out=$RAW/results/mads_${c}_$1.json > $RAW/logs/mads_${c}_$1.log 2>&1
  echo "exit $? c=$c $1"
done
