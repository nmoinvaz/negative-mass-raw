#!/bin/bash
# recmut.sh: each mutation on the stored record (baseline and mutated in one process); logs runs/mut/mut_<name>.log (numbered, never overwritten)
RAW=$HOME/Source/negative-mass-raw/I255-dh610
PY=$HOME/Source/negative-mass-venv314/bin/python
cd $HOME/Source/negative-mass-i255/notes/wormhole_evolution
for m in "$@"; do
  f=$RAW/runs/mut/mut_$m; i=1; while [ -e $f.log ]; do f=$RAW/runs/mut/mut_${m}_r$i; i=$((i+1)); done
  extra=""
  [ "$m" = "pstar_off" ] && extra="--ctl=$RAW/dev/ctl_pstar_off"
  [ "$m" = "bis_loose" ] && extra="--ctl=$RAW/dev/ctl_bis_loose"
  nice -n 10 $PY throat_drift.py mutate --mutate=$m --raw=$RAW/runs $extra > $f.log 2>&1
  echo "$m rc=$? $(tail -2 $f.log | head -1)" >> $RAW/runs/mut/summary.txt
done
