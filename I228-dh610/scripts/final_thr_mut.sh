#!/bin/bash
# #40's own mutations through the wrapped analysis of the merged record (the D = 6 G rows included)
RAW=$HOME/Source/negative-mass-raw/I228-dh610
cd $HOME/Source/negative-mass-i228/notes/wormhole_evolution
export NUMBA_NUM_THREADS=1
mkdir -p $RAW/runs/mut
for m in time_unit pstar_off bisect_loose pstar_h1; do
  nice -n 10 $HOME/Source/negative-mass-venv314/bin/python g_d6.py threshold-analyze --raw=$RAW/runs40 --mutate=$m > $RAW/runs/mut/threshold_$m.log 2> $RAW/runs/mut/threshold_$m.err
  echo "rc=$?" > $RAW/runs/mut/threshold_$m.rc
done
