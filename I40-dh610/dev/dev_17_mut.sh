#!/bin/bash
# usage: dev_17_mut.sh NAME [flags]: D = 4 family S at the three declared h under mutation NAME (second batch of mutation dev runs)
TH=/home/nathan/Source/negative-mass-i40/notes/wormhole_evolution/threshold.py
PY=$HOME/Source/negative-mass-venv314/bin/python
D=$HOME/Source/negative-mass-raw/I40-dh610/dev/dev_17
m=$1; shift
mkdir -p dev_17/$m
for h in 0.02 0.01 0.005; do
  ./unit_run.sh dev_17/$m/job_D4_S_h$h nice -n 10 $PY $TH job --D=4 --family=S --h=$h --out=$D/$m/D4_S_h$h --mutate=$m "$@"
done
