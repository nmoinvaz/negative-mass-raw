#!/bin/bash
# devmut.sh: the development suite once per mutation (baseline and mutated in one process); logs dev/mut/mut_<name>.log (numbered, never overwritten)
RAW=$HOME/Source/negative-mass-raw/I255-dh610
PY=$HOME/Source/negative-mass-venv314/bin/python
cd $HOME/Source/negative-mass-i255/notes/wormhole_evolution
for m in "$@"; do
  f=$RAW/dev/mut/mut_$m; i=1; while [ -e $f.log ]; do f=$RAW/dev/mut/mut_${m}_r$i; i=$((i+1)); done
  extra=""
  if [ "$m" = "pstar_off" ]; then
    d=$RAW/dev/ctl_pstar_off; mkdir -p $d
    nice -n 10 $PY throat_drift.py ctl --D=5 --hk=0 --out=$d --mutate=pstar_off > $f.ctl.log 2>&1
    extra="--ctl=$d"
  fi
  if [ "$m" = "bis_loose" ]; then
    d=$RAW/dev/ctl_bis_loose; mkdir -p $d
    nice -n 10 $PY throat_drift.py bisect --D=4 --B=0.1 --hk=0 --out=$d/bisect --mutate=bis_loose > $f.ctl.log 2>&1
    extra="--ctl=$d"
  fi
  nice -n 10 $PY throat_drift.py mutate --mutate=$m $extra > $f.log 2>&1
  echo "$m rc=$? $(tail -2 $f.log | head -1)" >> $RAW/dev/mut/summary.txt
done
