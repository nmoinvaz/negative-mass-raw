#!/bin/bash
# usage: final_mut.sh NAME...   the declared mutations on the stored record: baseline and mutated analysis, the changed verdicts
RAW=$HOME/Source/negative-mass-raw/I228-dh610
cd $HOME/Source/negative-mass-i228/notes/wormhole_evolution
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1
mkdir -p $RAW/runs/mut
for m in "$@"; do
  nice -n 10 $HOME/Source/negative-mass-venv314/bin/python g_d6.py mutate --base=$RAW/runs --hks=1,2 --mutate=$m > $RAW/runs/mut/mutate_$m.log 2> $RAW/runs/mut/mutate_$m.err
  echo "rc=$?" > $RAW/runs/mut/mutate_$m.rc
done
