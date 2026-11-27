#!/bin/bash
# the analyses of the mutation runs of record: one log per mutation in runs/mut/analysis_<name>.log (expected and fired targets at the end of each)
RAW=${RAW:-$HOME/Source/negative-mass-raw/I40-dh610}
TD=$HOME/Source/negative-mass-i40/notes/wormhole_evolution
PY=$HOME/Source/negative-mass-venv314/bin/python
export NUMBA_NUM_THREADS=1
cd $TD
an() { local log=$1; shift; nice -n 10 $PY threshold.py analyze "$@" > "$RAW/runs/mut/$log" 2>&1; echo "$log rc=$?"; }
for m in bisect_loose ed_unit no_corrector theta_coef ghost_sign finder_sign ellis_charge scalar_coef data_constraint_sign; do
  an analysis_$m.log --raw=$RAW/runs/mut/$m --only=4S --mutate=$m
done
an analysis_pstar_off.log --raw=$RAW/runs --only=4S,planted --mutate=pstar_off
an analysis_pstar_h1.log --raw=$RAW/runs --only=4S --mutate=pstar_h1
an analysis_time_unit_runs.log --raw=$RAW/runs --only=4S,planted --mutate=time_unit
an analysis_time_unit_g6.log --raw=$RAW/runs/mut/time_unit --only=g6 --mutate=time_unit
