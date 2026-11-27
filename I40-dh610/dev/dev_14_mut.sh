#!/bin/bash
# usage: dev_14_mut.sh NAME...   D = 4 family S at the three declared h under each mutation, with --ed (the targets are computed from these)
TH=/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution/threshold.py
PY=$HOME/Source/negative-mass-venv314/bin/python
D=$HOME/Source/negative-mass-raw/I40-dh610/dev/dev_14
for m in "$@"; do
  mkdir -p dev_14/$m
  for h in 0.02 0.01 0.005; do
    ./unit_run.sh dev_14/$m/job_D4_S_h$h nice -n 10 $PY $TH job --D=4 --family=S --h=$h --out=$D/$m/D4_S_h$h --ed --mutate=$m
  done
done
