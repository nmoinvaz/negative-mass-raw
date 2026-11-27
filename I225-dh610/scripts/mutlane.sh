#!/bin/bash
# mutation runs of the reduced suite: mutlane.sh DIR NAME... ; logs DIR/mut_NAME.log (never overwritten), run from the worktree's notes/wormhole_evolution
PY=$HOME/Source/negative-mass-venv314/bin/python
OUT=$1; shift
mkdir -p $OUT
cd $HOME/Source/negative-mass-i225/notes/wormhole_evolution
for m in "$@"; do
  i=1; f=$OUT/mut_$m; while [ -e $f.log ]; do f=$OUT/mut_${m}_r$i; i=$((i+1)); done
  /usr/bin/time -v -o $f.time nice -n 10 $PY throat_locus.py mutate --mutate=$m > $f.log 2>&1; echo $? > $f.rc
done
