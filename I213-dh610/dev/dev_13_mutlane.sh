#!/bin/bash
# dev_13: one lane of mutation runs of expansion.py (reduced size), names on the command line; log per mutation in dev/mut13/
cd /home/nathan/Source/negative-mass-i213/notes/wormhole_evolution
mkdir -p ~/Source/negative-mass-raw/I213-dh610/dev/mut13
for m in "$@"; do
  nice -n 10 ~/Source/negative-mass-venv314/bin/python expansion.py mutate --mutate=$m > ~/Source/negative-mass-raw/I213-dh610/dev/mut13/dev13_$m.log 2>&1
  echo "$m rc=$?" >> ~/Source/negative-mass-raw/I213-dh610/dev/mut13/lane_done.txt
done
