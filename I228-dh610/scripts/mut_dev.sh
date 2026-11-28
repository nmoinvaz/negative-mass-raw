#!/bin/bash
# development mutations of g_d6.py analyze on the h = 0.005 data (dev/): baseline and mutated run each, the verdicts that changed are the effect
RAW=$HOME/Source/negative-mass-raw/I228-dh610
cd $HOME/Source/negative-mass-i228/notes/wormhole_evolution
export NUMBA_NUM_THREADS=1 OMP_NUM_THREADS=1
for m in "$@"; do
  nice -n 10 $HOME/Source/negative-mass-venv314/bin/python g_d6.py mutate --base=$RAW/dev --hks=0 --mutate=$m > $RAW/dev/mut/mutate_$m.log 2> $RAW/dev/mut/mutate_$m.err
  echo "$m rc=$? $(tail -2 $RAW/dev/mut/mutate_$m.log | head -1)" >> $RAW/dev/mut/summary.txt
done
