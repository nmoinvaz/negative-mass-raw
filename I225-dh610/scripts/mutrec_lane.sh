#!/bin/bash
# mutrec_lane.sh RAWDIR OUTDIR NAME...: `throat_locus.py analyze --raw=RAWDIR --mutate=NAME` for each name; logs OUTDIR/mut_NAME.log (never overwritten)
PY=$HOME/Source/negative-mass-venv314/bin/python
RD=$1; OUT=$2; shift; shift
mkdir -p $OUT
cd $HOME/Source/negative-mass-i225/notes/wormhole_evolution
for m in "$@"; do
  i=1; f=$OUT/mut_$m; while [ -e $f.log ]; do f=$OUT/mut_${m}_r$i; i=$((i+1)); done
  /usr/bin/time -v -o $f.time nice -n 10 $PY throat_locus.py analyze --raw=$RD --mutate=$m > $f.log 2>&1; echo $? > $f.rc
done
