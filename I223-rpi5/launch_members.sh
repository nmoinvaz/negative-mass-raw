#!/bin/bash
# usage: [STAGE=low] launch_members.sh RESDIR "res list" id1 id2 ...   (RESDIR under the raw folder; res list e.g. "R1 R2")
# a finished JSON is never overwritten; exit codes in RESDIR/status.txt; one log and one JSON per run
RAW=$HOME/Source/negative-mass-raw/I223-rpi5
PY=$HOME/Source/negative-mass-venv314/bin/python
RESDIR=$RAW/$1; RESLIST=$2; shift 2
STAGE=${STAGE:-main}
mkdir -p $RESDIR
cd $HOME/Source/negative-mass-i223/notes/black_universe || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
for id in "$@"; do
  for res in $RESLIST; do
    f=$RESDIR/${id}_${res}
    [ "$STAGE" = low ] && f=${f}_low
    if [ -f $f.json ]; then continue; fi
    start=$(date +%s)
    /usr/bin/time -v nice -n 10 $PY bounce.py count $id --res=$res --stage=$STAGE --out=$f.json > $f.log 2>&1
    echo "$id $res $STAGE exit $? $(( $(date +%s) - start )) s $(date +%H:%M:%S)" >> $RESDIR/status.txt
  done
done
