#!/bin/bash
# one lane of the mutation runs of record: mutlane.sh name ...; the reduced suite, log per mutation in runs/mut/
RAW=$HOME/Source/negative-mass-raw/I213-dh610
cd $HOME/Source/negative-mass-i213/notes/wormhole_evolution
for m in "$@"; do
  /usr/bin/time -v -o $RAW/runs/mut/$m.time nice -n 10 $HOME/Source/negative-mass-venv314/bin/python expansion.py mutate --mutate=$m > $RAW/runs/mut/$m.log 2>&1
  echo "$m rc=$?" >> $RAW/runs/mut/lane_done.txt
done
